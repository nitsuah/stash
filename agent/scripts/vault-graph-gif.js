#!/usr/bin/env node
/**
 * vault-graph-gif.js
 * Render the stash/agent vault's link graph as a looping GIF + WebP, the way
 * Obsidian's Graph View draws it: notes = nodes, [[wikilinks]] = edges, a
 * d3-force simulation settling on screen.
 *
 * Adapted from U-L-M-S/obsidian-graph-gif (MIT, (c) 2026 U-L-M-S):
 * https://github.com/U-L-M-S/obsidian-graph-gif. Changes for stash: vault and
 * output paths come from env vars, nodes are colored by vault folder instead of
 * tag color groups, "Excluded files" regex entries are honored, and the theme
 * matches the GitHub Pages site (pages/).
 *
 * Normally run through vault-graph-gif.ps1 (Docker: Node + ffmpeg, no host
 * toolchain). Direct use:
 *   npm i d3-force@3 pureimage@0.4    (in any scratch dir next to a copy of this file)
 *   VAULT=<stash>/agent OUT_DIR=<stash>/pages/assets node vault-graph-gif.js
 *   PREVIEW=1 ...   → settled last frame only, OUT_DIR/vault-graph-preview.png
 *   SNAPSHOT_JSON=<file> ...  → also dump nodes, edges and per-frame positions
 *                               (for redrawing the animation elsewhere, e.g. a video)
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const pureimage = require('pureimage');

const FFMPEG     = process.env.FFMPEG_PATH || 'ffmpeg';
const VAULT      = path.resolve(process.env.VAULT || path.join(__dirname, '..'));
const OUT_DIR    = path.resolve(process.env.OUT_DIR || path.join(VAULT, '..', 'pages', 'assets'));
const FRAMES_DIR = path.join(os.tmpdir(), 'vault-graph-frames');
const NAME       = 'vault-graph';

// ── Vault settings — read from <vault>/.obsidian at run time ─────────────────
// graph.json: Graph View toggles, forces, size multipliers.
// app.json:   "Excluded files", which the real Graph View never shows.
function readVaultJson(name) {
  try { return JSON.parse(fs.readFileSync(path.join(VAULT, '.obsidian', name), 'utf-8')); }
  catch { return null; }
}
const GRAPH_CFG = readVaultJson('graph.json');
const APP_CFG   = readVaultJson('app.json');

const W          = 1600;  // poster PNG size; frames render at W*SS
const H          = 900;
const SS         = 2;     // supersample factor: render large, ffmpeg downscales → anti-aliasing
const RW         = W * SS;
const RH         = H * SS;
const WEBP_W     = 1200;  // animated WebP: the page shows it at <=1000px
const GIF_W      = 800;   // GIF fallback, smaller to keep the file light
const DRAW_SCALE = (W / 1200) * SS; // node/line sizes, proportional to the original 1200px design
const FPS        = 15;
const FRAMES     = 150;   // ~10 s
const TICKS_PER_FRAME = 2;
const INCLUDE_ORPHANS    = GRAPH_CFG?.showOrphans ?? true;
const INCLUDE_UNRESOLVED = !(GRAPH_CFG?.hideUnresolved ?? false);
const SHOW_TAGS          = GRAPH_CFG?.showTags        ?? true;
const SHOW_ATTACHMENTS   = GRAPH_CFG?.showAttachments ?? true;
const NODE_SIZE_MULT     = GRAPH_CFG?.nodeSizeMultiplier ?? 1;
const LINE_SIZE_MULT     = GRAPH_CFG?.lineSizeMultiplier ?? 1;
const PREVIEW    = !!process.env.PREVIEW;
const ZOOM       = 1.0;

// Graph View "Forces" sliders normalized to 0..1 (repel is stored 0..20,
// linkDistance 30..500 px); lerped onto d3-force parameters in runSimulation().
// Each field falls back on its own, so a partial graph.json can't yield NaN.
const FORCES = {
  center:       GRAPH_CFG?.centerStrength ?? 0.5,
  repel:        (GRAPH_CFG?.repelStrength ?? 10) / 20,
  link:         GRAPH_CFG?.linkStrength ?? 0.8,
  linkDistance: ((GRAPH_CFG?.linkDistance ?? 30) - 30) / 470,
};

// Excluded files: plain prefixes ("logs/") or /regex/ entries ("/\.txt$/").
const IGNORE_FILTERS = (APP_CFG?.userIgnoreFilters ?? []).map(f => {
  const re = f.match(/^\/(.+)\/$/);
  return re ? new RegExp(re[1]) : f.replace(/\\/g, '/').trim();
}).filter(Boolean);
const ignored = rel => IGNORE_FILTERS.some(f =>
  f instanceof RegExp ? f.test(rel) : rel.startsWith(f) || (rel + '/').startsWith(f));
const ATTACH_EXT = /\.(png|jpe?g|gif|svg|webp|avif|pdf|canvas|base|excalidraw)$/i;

// ── Theme: the dark palette of pages/style.css ──────────────────────────────
const BG               = '#131217';
const EDGE_COLOR       = 'rgba(169, 139, 255, 0.16)';
const NODE_COLOR       = '#a7a3b3';
const TAG_COLOR        = '#e0de71';
const ATTACH_COLOR     = '#6b6779';
const UNRESOLVED_COLOR = '#4a4658';
// First matching vault-relative prefix wins.
const FOLDER_COLORS = [
  [/^repos\/[^/]+\.md$/, '#ecebf0'], // repo hubs: the bright centres of each cluster
  [/^repos\//,           '#a98bff'], // mirrored repo docs
  [/^reports\//,         '#3fc79f'], // routine reports
  [/^notes\//,           '#f0975c'], // daily / weekly notes
  [/^(projects|topics)\//, '#5fb3ff'],
  [/^(prompts|routines|templates)\//, '#ff7eb6'],
];

// ── 1. Collect notes (+ attachments) ─────────────────────────────────────────
function collectNotes(dir) {
  const notes = [];
  const attachments = [];
  const skipNames = new Set(['node_modules', '__pycache__']);
  function walk(d) {
    let entries;
    try { entries = fs.readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      if (e.name.startsWith('.') || skipNames.has(e.name)) continue;
      const p = path.join(d, e.name);
      const rel = path.relative(dir, p).split(path.sep).join('/');
      if (ignored(rel)) continue;
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith('.md')) notes.push({ p, rel });
      else if (ATTACH_EXT.test(e.name)) attachments.push(e.name);
    }
  }
  walk(dir);
  return { notes, attachments };
}

// ── 2. Parse a note ──────────────────────────────────────────────────────────
function parseNote({ p, rel }) {
  let content;
  try { content = fs.readFileSync(p, 'utf-8'); } catch { return null; }

  const name = path.basename(p, '.md');
  const links = new Set();
  const linkRe = /\[\[([^\]|#\n]+)/g;
  let m;
  while ((m = linkRe.exec(content)) !== null) {
    const l = m[1].trim();
    if (l) links.add(l);
  }

  // Frontmatter list property: block list or inline [a, b]
  const fmList = (fm, prop) => {
    const block = fm.match(new RegExp(`^${prop}:\\s*\\r?\\n((?:[ \\t]+-[ \\t]+[^\\r\\n]+\\r?\\n?)*)`, 'm'));
    if (block) {
      return (block[1].match(/[ \t]+-[ \t]+([^\r\n]+)/g) || [])
        .map(t => t.replace(/^[ \t]+-[ \t]+/, '').trim());
    }
    const inline = fm.match(new RegExp(`^${prop}:\\s*\\[([^\\]]+)\\]`, 'm'));
    if (inline) return inline[1].split(',').map(t => t.trim().replace(/['"]/g, ''));
    return [];
  };

  let tags = [];
  let aliases = [];
  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (fmMatch) {
    tags = fmList(fmMatch[1], 'tags');
    aliases = fmList(fmMatch[1], 'aliases').filter(Boolean);
  }
  // Inline body #tags count too, like Obsidian's graph (fenced code skipped)
  const body = (fmMatch ? content.slice(fmMatch[0].length) : content).replace(/```[\s\S]*?```/g, '');
  for (const bt of body.match(/(?:^|\s)#([A-Za-z][\w/-]*)/g) || []) tags.push(bt.trim().slice(1));

  return { name, rel, links: [...links], tags: [...new Set(tags)], aliases };
}

// ── 3. Build graph ───────────────────────────────────────────────────────────
function buildGraph(parsed, attachments) {
  // Notes are keyed by vault path, not basename: 17 repo mirrors each have a
  // README/ROADMAP/TASKS, and Obsidian keeps those as separate nodes.
  const byName   = new Map(); // lowercased basename → [ids], for path-less [[links]]
  const byKey    = new Map(); // lowercased tag / attachment / ghost key → id
  const aliasMap = new Map();
  const nodes    = [];
  const norm = s => s.toLowerCase();
  const addNode = node => {
    const id = nodes.length;
    nodes.push({ ...node, id, degree: 0 });
    return id;
  };

  for (const note of parsed) {
    const id = addNode(note);
    const k = norm(note.name);
    byName.set(k, [...(byName.get(k) || []), id]);
    for (const a of note.aliases) if (!aliasMap.has(norm(a))) aliasMap.set(norm(a), id);
  }
  if (SHOW_ATTACHMENTS) {
    for (const a of attachments) {
      if (!byKey.has(norm(a))) byKey.set(norm(a), addNode({ name: a, links: [], tags: [], attachment: true }));
    }
  }

  // Resolve like Obsidian: a [[dir/note]] link matches by path suffix; a bare
  // [[note]] prefers the same folder, then the shortest path; then aliases.
  const dirOf = rel => rel.slice(0, rel.lastIndexOf('/') + 1);
  const resolve = (l, fromRel) => {
    const target = norm(l.trim().replace(/\.md$/i, ''));
    const base = target.split('/').pop();
    const cands = byName.get(base) || [];
    if (target.includes('/')) {
      const hit = cands.find(i => norm(nodes[i].rel.replace(/\.md$/i, '')).endsWith(target));
      if (hit !== undefined) return hit;
    } else if (cands.length) {
      const here = cands.find(i => dirOf(nodes[i].rel) === dirOf(fromRel));
      if (here !== undefined) return here;
      return [...cands].sort((a, b) => nodes[a].rel.length - nodes[b].rel.length)[0];
    }
    return byKey.get(base) ?? aliasMap.get(base);
  };

  const seen  = new Set();
  const edges = [];
  const addEdge = (i, j) => {
    if (i === j) return;
    const key = Math.min(i, j) + '_' + Math.max(i, j);
    if (seen.has(key)) return;
    seen.add(key);
    edges.push([i, j]);
    nodes[i].degree++;
    nodes[j].degree++;
  };

  for (let i = 0; i < parsed.length; i++) {
    for (const l of nodes[i].links) {
      let j = resolve(l, nodes[i].rel);
      if (j === undefined && INCLUDE_UNRESOLVED) {
        const key = norm(l.split('/').pop().trim());
        j = byKey.get(key) ?? addNode({ name: l, links: [], tags: [], unresolved: true });
        byKey.set(key, j);
      }
      if (j !== undefined) addEdge(i, j);
    }
    if (SHOW_TAGS) {
      for (const t of nodes[i].tags) {
        const key = norm('#' + t); // tags merge case-insensitively, like Obsidian
        let j = byKey.get(key);
        if (j === undefined) byKey.set(key, j = addNode({ name: '#' + t, links: [], tags: [], tagNode: true }));
        addEdge(i, j);
      }
    }
  }
  return { nodes, edges };
}

function keepNodes(nodes, edges, keepSet) {
  const remap = new Map();
  const newNodes = [];
  nodes.forEach((n, i) => { if (keepSet.has(i)) { remap.set(i, newNodes.length); newNodes.push(n); } });
  const newEdges = edges
    .filter(([i, j]) => keepSet.has(i) && keepSet.has(j))
    .map(([i, j]) => [remap.get(i), remap.get(j)]);
  newNodes.forEach((n, i) => { n.id = i; });
  return { nodes: newNodes, edges: newEdges };
}

// ── 4. d3-force simulation ───────────────────────────────────────────────────
// Seeded PRNG so runs are reproducible: the same vault renders the same GIF.
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

async function runSimulation(nodes, edges) {
  const d3 = await import('d3-force');
  const links = edges.map(([i, j]) => ({ source: i, target: j }));

  // d3 seeds positions deterministically; jittered orphan centering spreads
  // them into Obsidian's loose halo instead of a hard ring.
  const rng = mulberry32(42);
  for (const n of nodes) n.centerK = n.degree === 0 ? 1.0 + 0.35 * rng() : 1;

  const lerp = (a, b, t) => a + (b - a) * t;
  const centerStrength = lerp(0.005, 0.16, FORCES.center);
  const chargeStrength = -lerp(30, 450, FORCES.repel);
  const linkStrengthK  = lerp(0.3, 1.2, FORCES.link);
  const linkDistance   = lerp(30, 500, FORCES.linkDistance);
  const linkStrength = l => linkStrengthK / Math.min(l.source.degree || 1, l.target.degree || 1);

  const sim = d3.forceSimulation(nodes)
    .velocityDecay(0.55)
    .force('charge',  d3.forceManyBody().strength(chargeStrength))
    .force('center',  d3.forceCenter(0, 0).strength(0.5))
    .force('link',    d3.forceLink(links).distance(linkDistance).strength(linkStrength))
    .force('collide', d3.forceCollide(d => nodeRadius(d) + 8).iterations(3))
    .force('x',       d3.forceX(0).strength(n => centerStrength * n.centerK))
    .force('y',       d3.forceY(0).strength(n => centerStrength * n.centerK))
    .stop();

  const snapshots = [];
  for (let f = 0; f < FRAMES; f++) {
    snapshots.push(nodes.map(n => [n.x, n.y]));
    sim.tick(TICKS_PER_FRAME);
  }
  return snapshots;
}

function nodeRadius(node) {
  return (1.0 + 0.6 * Math.sqrt(node.degree || 0)) * NODE_SIZE_MULT;
}

function nodeColor(node) {
  if (node.tagNode)    return TAG_COLOR;
  if (node.attachment) return ATTACH_COLOR;
  if (node.unresolved) return UNRESOLVED_COLOR;
  for (const [re, color] of FOLDER_COLORS) if (re.test(node.rel)) return color;
  return NODE_COLOR;
}

// ── 5. Camera: fit the settled layout, fixed while nodes glide in ────────────
// Fit to linked nodes only: a few unlinked dots drifting far out would
// otherwise shrink the whole graph.
function computeTransform(finalSnapshot, nodes) {
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  const linked = finalSnapshot.filter((_, i) => nodes[i].degree > 0);
  for (const [x, y] of linked.length ? linked : finalSnapshot) {
    minX = Math.min(minX, x); maxX = Math.max(maxX, x);
    minY = Math.min(minY, y); maxY = Math.max(maxY, y);
  }
  const pad    = RW * 0.04;
  const rangeX = maxX - minX || 1;
  const rangeY = maxY - minY || 1;
  const scale  = Math.min((RW - pad * 2) / rangeX, (RH - pad * 2) / rangeY) * ZOOM;
  return { scale, offX: (RW - rangeX * scale) / 2 - minX * scale, offY: (RH - rangeY * scale) / 2 - minY * scale };
}

// ── 6. Render one frame ──────────────────────────────────────────────────────
async function renderFrame(snapshot, nodes, edges, transform, frameIdx) {
  const img = pureimage.make(RW, RH);
  const ctx = img.getContext('2d');
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, RW, RH);

  const { scale, offX, offY } = transform;
  const px = i => snapshot[i][0] * scale + offX;
  const py = i => snapshot[i][1] * scale + offY;

  ctx.strokeStyle = EDGE_COLOR;
  ctx.lineWidth   = 0.55 * DRAW_SCALE * LINE_SIZE_MULT;
  for (const [i, j] of edges) {
    ctx.beginPath();
    ctx.moveTo(px(i), py(i));
    ctx.lineTo(px(j), py(j));
    ctx.stroke();
  }
  for (let i = 0; i < nodes.length; i++) {
    ctx.fillStyle = nodeColor(nodes[i]);
    ctx.beginPath();
    ctx.arc(px(i), py(i), nodeRadius(nodes[i]) * DRAW_SCALE, 0, Math.PI * 2);
    ctx.fill();
  }

  const framePath = path.join(FRAMES_DIR, `frame_${String(frameIdx).padStart(4, '0')}.png`);
  await new Promise((resolve, reject) => {
    const stream = fs.createWriteStream(framePath);
    stream.on('finish', resolve);
    stream.on('error', reject);
    pureimage.encodePNGToStream(img, stream).catch(reject);
  });
}

const ffmpeg = args => execFileSync(FFMPEG, ['-y', '-loglevel', 'error', ...args], { stdio: 'inherit' });

// ── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  const { notes: files, attachments } = collectNotes(VAULT);
  const parsed = files.map(parseNote).filter(Boolean);
  let { nodes, edges } = buildGraph(parsed, attachments);
  if (!INCLUDE_ORPHANS) {
    ({ nodes, edges } = keepNodes(nodes, edges, new Set(nodes.flatMap((n, i) => n.degree > 0 ? [i] : []))));
  }
  const counts = {
    notes: parsed.length,
    tags: nodes.filter(n => n.tagNode).length,
    attachments: nodes.filter(n => n.attachment).length,
    unresolved: nodes.filter(n => n.unresolved).length,
    nodes: nodes.length,
    edges: edges.length,
  };
  console.log(`vault ${VAULT}: ${JSON.stringify(counts)}`);

  const snapshots = await runSimulation(nodes, edges);
  const transform = computeTransform(snapshots[FRAMES - 1], nodes);
  if (process.env.SNAPSHOT_JSON) {
    const r1 = v => Math.round(v * 10) / 10;
    fs.writeFileSync(process.env.SNAPSHOT_JSON, JSON.stringify({
      counts,
      nodes: nodes.map(n => ({ c: nodeColor(n), r: r1(nodeRadius(n)),
        ...(/^repos\/[^/]+\.md$/.test(n.rel || '') && { hub: n.name }) })),
      edges,
      frames: snapshots.map(s => s.map(([x, y]) => [r1(x), r1(y)])),
    }));
  }

  fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
  fs.mkdirSync(FRAMES_DIR, { recursive: true });
  fs.mkdirSync(OUT_DIR, { recursive: true });

  if (PREVIEW) {
    await renderFrame(snapshots[FRAMES - 1], nodes, edges, transform, 0);
    const preview = path.join(OUT_DIR, `${NAME}-preview.png`);
    ffmpeg(['-i', path.join(FRAMES_DIR, 'frame_0000.png'), '-vf', `scale=${W}:${H}:flags=lanczos`, '-frames:v', '1', preview]);
    console.log(`preview → ${preview}`);
    return;
  }

  for (let f = 0; f < FRAMES; f++) {
    await renderFrame(snapshots[f], nodes, edges, transform, f);
    if (f % 10 === 0) process.stdout.write(`  frame ${f + 1}/${FRAMES}\r`);
  }
  console.log(`  frame ${FRAMES}/${FRAMES}`);

  const frames  = path.join(FRAMES_DIR, 'frame_%04d.png');
  const palette = path.join(FRAMES_DIR, 'palette.png');
  const gifOut  = path.join(OUT_DIR, `${NAME}.gif`);
  const webpOut = path.join(OUT_DIR, `${NAME}.webp`);
  const posterOut = path.join(OUT_DIR, `${NAME}.png`);
  const gifScale = `scale=${GIF_W}:-2:flags=lanczos`;

  // Hold the settled graph for 2 s before the loop restarts.
  const hold = `tpad=stop_mode=clone:stop_duration=2`;
  // bayer dither is temporally stable; floyd_steinberg shimmers on the settled tail.
  ffmpeg(['-framerate', `${FPS}`, '-i', frames, '-vf', `${gifScale},palettegen=max_colors=128:stats_mode=diff`, palette]);
  ffmpeg(['-framerate', `${FPS}`, '-i', frames, '-i', palette, '-lavfi',
    `${gifScale},${hold}[s];[s][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle`, '-loop', '0', gifOut]);
  ffmpeg(['-framerate', `${FPS}`, '-i', frames, '-vf', `scale=${WEBP_W}:-2:flags=lanczos,${hold}`,
    '-vcodec', 'libwebp', '-lossless', '0', '-quality', '72', '-preset', 'drawing', '-compression_level', '6',
    '-loop', '0', '-an', webpOut]);
  ffmpeg(['-i', path.join(FRAMES_DIR, `frame_${String(FRAMES - 1).padStart(4, '0')}.png`),
    '-vf', `scale=${W}:${H}:flags=lanczos`, '-frames:v', '1', posterOut]);
  fs.writeFileSync(path.join(OUT_DIR, `${NAME}.json`), JSON.stringify(counts, null, 2) + '\n');

  const mb = f => (fs.statSync(f).size / 1024 / 1024).toFixed(1) + ' MB';
  console.log(`GIF  → ${gifOut} (${mb(gifOut)})`);
  console.log(`WebP → ${webpOut} (${mb(webpOut)})`);
  console.log(`PNG  → ${posterOut} (${mb(posterOut)})`);
  fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
}

main().catch(err => { console.error(err); process.exit(1); });
