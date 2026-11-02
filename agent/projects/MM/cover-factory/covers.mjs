// Zero-LLM cover factory: renders a 1280x720 cover and a 600x600 thumbnail per product from products.mjs.
// Run in the playwright image with MM mounted at /w:  node covers.mjs   (cwd /w/cover-factory). Output: out/<slug>-cover.png, out/<slug>-thumb.png
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync, readdirSync, readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { products } from './products.mjs';
const { chromium } = createRequire(resolve('../audit-scanner/package.json'))('playwright');

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function visualHtml(v, mode) {
  if (v.grid) {
    const dir = `/w/${v.grid}`;
    const icons = readdirSync(dir).filter((f) => f.endsWith('.svg')).slice(0, mode === 'thumb' ? 24 : 32).map((f) => readFileSync(`${dir}/${f}`, 'utf8'));
    return `<div class="grid">${icons.map((s) => `<div class="ic">${s.replace(/width="24" height="24"/, 'width="46" height="46"')}</div>`).join('')}</div>`;
  }
  if (v.code && mode === 'thumb' && v.thumbCode) return `<div class="code"><div class="code-bar"><i></i><i></i><i></i><span>${esc(v.file ?? '')}</span></div><pre>${v.thumbCode}</pre></div>`;
  if (v.img) return `<img class="vis-img" src="file:///w/${v.img}" style="object-position:${v.pos ?? 'top'};--fit:${v.fit ?? 'cover'}">`;
  if (v.page) return `<iframe class="vis-page" src="file:///w/${v.page}" scrolling="no" style="transform:scale(${v.scale ?? 0.6});width:${100 / (v.scale ?? 0.6)}%;height:${100 / (v.scale ?? 0.6)}%"></iframe>`;
  if (v.code) return `<div class="code"><div class="code-bar"><i></i><i></i><i></i><span>${esc(v.file ?? '')}</span></div><pre>${v.code}</pre></div>`;
  if (v.list) return `<div class="list">${v.list.map(([a, b]) => `<div class="row"><b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div>`;
  if (v.table) return `<div class="tbl">${v.table.map((r, i) => `<div class="tr ${i === 0 ? 'th' : ''}">${r.map((c) => `<span>${esc(c)}</span>`).join('')}</div>`).join('')}</div>`;
  return '';
}

// Fail before launching Chromium if the generated source assets are missing.
for (const p of products) {
  const v = p.visual || {};
  const asset = v.grid ? `/w/${v.grid}` : v.img ? `/w/${v.img}` : v.page ? `/w/${v.page}` : null;
  if (asset && !existsSync(asset)) {
    throw new Error(`Missing visual asset for ${p.slug}: ${asset}. Run ./run.sh from cover-factory to build inputs first.`);
  }
  if (v.grid && readdirSync(asset).filter((name) => name.endsWith('.svg')).length === 0) {
    throw new Error(`No SVG icons found for ${p.slug}: ${asset}. Run ./run.sh from cover-factory to build inputs first.`);
  }
}

const CSS = `
*{box-sizing:border-box;margin:0}html,body{height:100%}
body{font-family:Inter,system-ui,Segoe UI,Arial,sans-serif;color:#fff;overflow:hidden}
.card{position:relative;width:100%;height:100%;background:linear-gradient(135deg,var(--a) 0%,var(--b) 100%);display:flex}
.card:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 15%,rgba(255,255,255,.18),transparent 45%)}
.brand{position:absolute;left:56px;top:40px;font-size:15px;letter-spacing:.22em;font-weight:700;opacity:.85}
.copy{position:relative;z-index:1;width:50%;padding:92px 20px 52px 56px;display:flex;flex-direction:column}
h1{font-size:58px;line-height:1.04;font-weight:800;letter-spacing:-.02em}
.tag{margin-top:18px;font-size:23px;line-height:1.35;opacity:.92;max-width:520px}
ul{list-style:none;padding:0;margin:26px 0 0}
li{font-size:20px;margin:9px 0;display:flex;gap:12px;align-items:flex-start;opacity:.95}
li:before{content:"\\2713";font-weight:800;color:var(--c)}
.chips{margin-top:auto;padding-top:22px;display:flex;gap:10px;flex-wrap:wrap}
.chip{padding:7px 14px;border-radius:999px;background:rgba(255,255,255,.16);font-size:15px;font-weight:600}
.frame{position:relative;z-index:1;width:50%;padding:48px 56px 48px 12px;display:flex;align-items:center}
.panel{width:100%;height:100%;max-height:560px;background:#fff;border-radius:18px;box-shadow:0 30px 70px rgba(0,0,0,.45);overflow:hidden;position:relative;color:#111}
.vis-img{width:100%;height:100%;object-fit:var(--fit,cover);display:block;background:#fff}
.vis-page{border:0;transform-origin:0 0;background:#fff;pointer-events:none}
.code{background:#0d1117;height:100%;color:#e6edf3;font:15px/1.5 Consolas,Menlo,monospace}
.code-bar{display:flex;gap:7px;align-items:center;padding:12px 16px;background:#161b22;font-size:13px;color:#8b949e}
.code-bar i{width:11px;height:11px;border-radius:50%;background:#444;display:block}.code-bar i:nth-child(1){background:#ff5f56}.code-bar i:nth-child(2){background:#ffbd2e}.code-bar i:nth-child(3){background:#27c93f}.code-bar span{margin-left:10px}
.code pre{padding:18px 20px;white-space:pre-wrap;margin:0;font:inherit}
.k{color:#79c0ff}.s{color:#a5d6ff}.c{color:#8b949e}.g{color:#7ee787}
.list{padding:20px;display:flex;flex-direction:column;gap:9px;height:100%;background:#f6f8fa;justify-content:center}
.row{display:flex;flex-direction:column;background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:9px 16px}
.row b{font-size:18px}.row span{font-size:14px;color:#57606a;margin-top:1px}
.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;padding:26px;height:100%;background:#fff;align-content:center}
.ic{display:flex;align-items:center;justify-content:center;aspect-ratio:1;border:1px solid #e4e4e7;border-radius:12px;color:#18181b;background:#fafafa}
.thumb .grid{grid-template-columns:repeat(6,1fr);padding:14px;gap:6px}.thumb .ic svg{width:30px;height:30px}
.thumb .code{font-size:12.5px}.thumb .code pre{padding:12px 16px}
.thumb .list{padding:12px;gap:6px}.thumb .row{padding:6px 12px}.thumb .row b{font-size:15px}.thumb .row span{display:none}
.thumb .tbl{padding:12px;gap:5px;font-size:13px}.thumb .tr{padding:6px 10px}
.tbl{padding:22px;background:#f6f8fa;height:100%;display:flex;flex-direction:column;gap:8px;font-size:15px}
.tr{display:grid;grid-template-columns:1.3fr 1.6fr 1fr;gap:10px;background:#fff;border:1px solid #d0d7de;border-radius:10px;padding:10px 14px}
.tr.th{background:#0d1117;color:#fff;font-weight:700;border-color:#0d1117}
.thumb .card{flex-direction:column}
.thumb .brand{left:36px;top:26px;font-size:13px}
.thumb .frame{order:1;width:100%;height:52%;padding:62px 36px 0}
.thumb .panel{max-height:none}
.thumb .copy{order:2;width:100%;height:48%;padding:22px 36px 30px}
.thumb h1{font-size:42px}
.thumb .tag,.thumb ul{display:none}
.thumb .chips{margin-top:16px}
.thumb .chip{font-size:14px;padding:6px 12px}
`;

function page(p, mode) {
  return `<!doctype html><html class="${mode}"><head><meta charset="utf-8"><style>${CSS}</style></head><body class="${mode}">
<div class="card" style="--a:${p.a};--b:${p.b};--c:${p.c ?? '#7ee787'}">
<div class="brand">NITSUAH LABS</div>
<div class="copy"><h1>${esc(p.title)}</h1><div class="tag">${esc(p.tagline)}</div><ul>${p.bullets.map((b) => `<li>${esc(b)}</li>`).join('')}</ul><div class="chips">${p.chips.map((c) => `<span class="chip">${esc(c)}</span>`).join('')}</div></div>
<div class="frame"><div class="panel" style="${p.visual.bg ? `background:${p.visual.bg}` : ''}">${visualHtml(p.visual, mode)}</div></div>
</div></body></html>`;
}

mkdirSync('out', { recursive: true });
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
for (const p of products) {
  for (const [mode, w, h] of [['cover', 1280, 720], ['thumb', 600, 600]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const pg = await ctx.newPage();
    writeFileSync(`out/${p.slug}-${mode}.html`, page(p, mode));
    await pg.goto(`file:///w/cover-factory/out/${p.slug}-${mode}.html`);
    await pg.waitForTimeout(400);
    await pg.screenshot({ path: `out/${p.slug}-${mode}.png` });
    await ctx.close();
  }
  console.log('rendered', p.slug);
}
await browser.close();
