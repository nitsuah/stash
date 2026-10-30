#!/usr/bin/env node
// daily-run.mjs: the deterministic half of agent/prompts/DAILY.md as plain code, so the
// model only runs on changed data. Default is --dry-run (reads, prints what it WOULD do,
// writes nothing tracked); --apply merges, mutates, pushes and opens the PR.
//
//   node agent/scripts/daily-run.mjs [--dry-run | --apply] [--no-model] [--root <stash>] [--date YYYY-MM-DD]
//
// Implements DAILY steps 0-1, the skip-gate, the step-3 note skeleton, the step-4 weekly
// skeleton, the vault-index/link/orphan commands and the branch/commit/push/PR tail. Model
// work (hub synthesis, Reflections, Monday goals, Saturday review) goes to
// agent/prompts/DAILY-MODEL.md via routine-run.mjs, and only when handoff.skip_model is false.
// No secrets here: VIGIL_MCP_KEY comes from the environment and is never printed.
import { spawnSync } from 'node:child_process';
import { appendFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const REPO_SLUG = 'nitsuah/stash';
export const VIGIL_URL = 'https://gh-vigil.netlify.app/api/context';
export const NOT_AUTOMATED = [
    'step 3 Tasks: "Unchanged human-gated P1s" dedup against the last daily note, and the .obsidian/*.json clean-filter check',
    'step 3 Tasks: parked-branch-N-days flags beyond the SKIPPED_* results of today\'s sync',
    'step 3 Notes (Mondays): failed cloud routine runs (needs RemoteTrigger, an MCP tool)',
    'Showcase board (Mondays): Artifact read/publish and the Tasks line (needs the Artifact tool); visual_board.py is not run either',
    'step 4 Monday: "top win" line of Last Week Review and the final choice of 3 goals (model-driven)',
];

// ---------- pure helpers ----------

const pad = (n) => String(n).padStart(2, '0');
/** Local calendar date (the machine runs in America/New_York); never UTC. */
export const localDate = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
export const localTime = (d) => `${pad(d.getHours())}:${pad(d.getMinutes())}`;

/** ISO week label `YYYY-Www` (ISO year, Monday start) for a YYYY-MM-DD date. */
export function isoWeek(dateStr) {
    const [y, m, d] = dateStr.split('-').map(Number);
    const t = new Date(Date.UTC(y, m - 1, d));
    const dow = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - dow);
    const yearStart = Date.UTC(t.getUTCFullYear(), 0, 1);
    return `${t.getUTCFullYear()}-W${pad(Math.ceil(((t - yearStart) / 86400000 + 1) / 7))}`;
}
export function addDays(dateStr, n) {
    const [y, m, d] = dateStr.split('-').map(Number);
    const t = new Date(Date.UTC(y, m - 1, d + n));
    return `${t.getUTCFullYear()}-${pad(t.getUTCMonth() + 1)}-${pad(t.getUTCDate())}`;
}
/** 0=Sunday .. 6=Saturday for a YYYY-MM-DD date. */
export const weekday = (dateStr) => new Date(`${dateStr}T12:00:00Z`).getUTCDay();

/** Parse the "## Tracked" table of scope.md (same semantics as obn_health.tracked_repos, plus path/url/visibility). */
export function parseScope(text) {
    const repos = [];
    let inTracked = false;
    for (const line of text.split(/\r?\n/)) {
        if (line.startsWith('## ')) { inTracked = line.startsWith('## Tracked'); continue; }
        if (!inTracked || !line.startsWith('|')) continue;
        const cells = line.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
        const name = cells[0].replace(/[` ]/g, '');
        if (!name || name.toLowerCase() === 'repo' || /^[-: ]+$/.test(name)) continue;
        const path = (cells[2] || '').match(/`([^`]+)`/)?.[1] || null;
        const gh = (cells[3] || '').match(/github\.com\/([^/\s)]+)\/([^/\s)]+)/);
        repos.push({
            name,
            aliases: [...line.matchAll(/formerly `([\w.-]+)`/g)].map((m) => m[1]),
            path,
            slug: gh ? `${gh[1]}/${gh[2].replace(/[.,;]+$/, '')}` : null,
            private: /private/i.test(cells[5] || ''),
        });
    }
    return repos;
}

/** The once-per-day guard verdict. Throws nothing; `ran` is true when a note or open PR for `today` exists. */
export function guardVerdict({ noteMerged, openPrTitles }, today) {
    const title = `obn: daily note ${today}`;
    const prHit = openPrTitles.includes(title);
    return { ran: Boolean(noteMerged) || prHit, noteMerged: Boolean(noteMerged), prHit };
}

/** Merge-gate candidate filter: exactly DAILY step 0 (title, branch, not a fork, author, opened before today). */
export function isMergeCandidate(pr, today) {
    return String(pr.title || '').startsWith('obn: ')
        && String(pr.headRefName || '').startsWith('obn/')
        && pr.isCrossRepository === false
        && pr.author?.login === 'nitsuah'
        && localDate(new Date(pr.createdAt)) < today;
}

/** Roll a statusCheckRollup into green | red | pending. No checks counts as green. */
export function ciState(rollup) {
    let pending = false;
    for (const c of rollup || []) {
        const v = String(c.conclusion || c.state || c.status || '').toUpperCase();
        if (['FAILURE', 'ERROR', 'TIMED_OUT', 'CANCELLED', 'ACTION_REQUIRED', 'STARTUP_FAILURE'].includes(v)) return 'red';
        if (!['SUCCESS', 'NEUTRAL', 'SKIPPED', 'COMPLETED'].includes(v)) pending = true;
        if (v === 'COMPLETED' && c.conclusion && !['SUCCESS', 'NEUTRAL', 'SKIPPED'].includes(String(c.conclusion).toUpperCase())) return 'red';
    }
    return pending ? 'pending' : 'green';
}

/** True when every CHANGES_REQUESTED review (latest per author) is from CodeRabbit (a stale bot block). */
export function onlyCodeRabbitBlocks(reviews) {
    const latest = new Map();
    for (const r of reviews || []) if (r.state !== 'COMMENTED') latest.set(r.author?.login || '', r.state);
    const blockers = [...latest].filter(([, s]) => s === 'CHANGES_REQUESTED').map(([a]) => a);
    return blockers.length > 0 && blockers.every((a) => /coderabbit/i.test(a));
}

/** Decide what to do with one candidate PR. Pure: input is the already-gathered facts. */
export function gateDecision({ diffOk, ci, isDraft }) {
    if (!diffOk) return { action: 'skip', reason: 'not routine-owned (check-generated-diff failed)' };
    if (ci === 'red') return { action: 'skip', reason: 'CI red' };
    if (ci === 'pending') return { action: 'skip', reason: 'CI pending' };
    return { action: 'merge', ready: Boolean(isDraft) };
}

/** Names on the "Stale hubs" line of VAULT-MAP.md. */
export function parseStaleHubs(vaultMap) {
    const line = vaultMap.split(/\r?\n/).find((l) => l.includes('**Stale hubs**'));
    if (!line) return [];
    const after = line.slice(line.indexOf('):') + 2 || 0);
    return [...after.matchAll(/\[\[([^\]]+)\]\]/g)].map((m) => {
        const target = m[1].split('|');
        return (target[1] || target[0].split('/').pop()).replace(/\.md$/, '').trim();
    });
}

/** Flatten vigil's open_work block (array or {p0:[],p1:[]}) to [{repo,title,priority}]. */
export function openWorkItems(ctx) {
    const ow = ctx?.open_work;
    let items = [];
    if (Array.isArray(ow)) items = ow;
    else if (ow && typeof ow === 'object') {
        for (const [k, v] of Object.entries(ow)) if (Array.isArray(v)) items.push(...v.map((i) => ({ priority: k.toUpperCase(), ...i })));
    }
    return items.map((i) => ({
        repo: i.repo || i.repo_name || i.repoName || '',
        title: String(i.title || i.text || '').trim(),
        priority: String(i.priority || i.p || '').toUpperCase(),
    })).filter((i) => i.repo && i.title && /^P[01]$/.test(i.priority));
}

const FUTURE_TAG = /\[(\d{4})-Q([1-4])\]/;
export function isFutureQuarter(title, today) {
    const m = title.match(FUTURE_TAG);
    if (!m) return false;
    const [y, mo] = today.split('-').map(Number);
    return Number(m[1]) * 4 + Number(m[2]) > y * 4 + Math.ceil(mo / 3);
}

/** Build the `## Tasks` lines. `active` is the set of repo names with activity today. */
export function tasksSection({ keySet, ctx, fetchError, active, skips, today }) {
    const out = [];
    if (!keySet) out.push('- Open work: vigil key not set (VIGIL_MCP_KEY); P0/P1 not listed.');
    else if (fetchError) out.push(`- Open work: vigil unavailable (${fetchError}); P0/P1 not listed.`);
    else {
        const items = openWorkItems(ctx).filter((i) => active.has(i.repo) && !isFutureQuarter(i.title, today));
        for (const i of items) out.push(`- ${i.priority} ${i.repo}: ${i.title}`);
        if (!items.length) out.push('- No P0/P1 tasks for repos active today.');
    }
    for (const s of skips) out.push(`- Human needed: ${s.repo} ${s.result} (${s.note})`);
    return out;
}

/** Repo Activity lines. `rows` = [{repo, prs:[{number,title,state}], issues:[...], commits:n}]. */
export function activitySection(rows, today) {
    const out = [];
    for (const r of rows) {
        const parts = [];
        if (r.prs.length) parts.push(r.prs.map((p) => `PR #${p.number} ${p.title} (${String(p.state).toLowerCase()})`).join(', '));
        if (r.commits) parts.push(`${r.commits} commit${r.commits === 1 ? '' : 's'}`);
        if (r.issues.length) parts.push(r.issues.map((p) => `issue #${p.number} ${p.title} (${String(p.state).toLowerCase()})`).join(', '));
        if (parts.length) out.push(`- **${r.repo}**: ${parts.join('; ')}`);
        if (r.error) out.push(`- **${r.repo}**: activity lookup failed (${r.error})`);
    }
    return out.length ? out : [`- No activity on tracked repos on ${today}.`];
}

export function renderNote({ today, activity, tasks, notes, reflections }) {
    return `# ${today}\n\n## Repo Activity\n${activity.join('\n')}\n\n## Tasks\n${tasks.join('\n')}\n\n## Notes\n${notes.join('\n')}\n\n## Reflections\n${reflections}\n`;
}

export const REFLECTIONS_PENDING = '_(pending model synthesis)_';
export const GOALS_PENDING = '- [ ] _(pending model goal seeding)_';
export const GOALS_FALLBACK = '- No goals seeded (model step did not run); set them by hand.';
export const REFLECTIONS_FALLBACK = 'Synthesis unavailable: the model step did not run today.';

/** Monday weekly-note skeleton. */
export function renderWeekNote({ week, monday, friday, review, activeProjects, linkSuggestions }) {
    const goals = review.exists ? GOALS_PENDING : '- No last review to seed goals from.';
    const links = linkSuggestions != null ? `\n- [ ] review ${linkSuggestions} link suggestions` : '';
    const lastWeek = review.exists ? `Last week (${review.week}): ${review.coverage || 'review present.'}` : 'No review last week.';
    return `# Week ${week.split('-W')[1]} — Mon ${monday} to Fri ${friday}\n\n## Goals\n${goals}${links}\n\n## Last Week Review\n${lastWeek}\n\n## Key Dates\n\n## Active Projects\n${activeProjects.length ? activeProjects.map((p) => `- ${p}`).join('\n') : 'None this week.'}\n`;
}

/** Handoff for the model step. skip_model is true when nothing needs synthesis. */
export function buildHandoff({ today, changed, stale, reflectionsDue, mondayGoals, saturdayReview, noteFile, notAutomated = NOT_AUTOMATED }) {
    const handoff = {
        date: today,
        note_file: noteFile,
        changed_repos: changed,
        stale_hubs: stale,
        reflections_due: reflectionsDue,
        monday_goals: mondayGoals,
        saturday_review: saturdayReview,
        not_automated: notAutomated,
    };
    handoff.skip_model = !(changed.length || stale.length || reflectionsDue || mondayGoals?.due || saturdayReview?.due);
    return handoff;
}

/** Interpret `sync-repos.ps1` stdout: per-repo staged-file counts, prunes and held prunes. */
export function parseSyncOutput(stdout) {
    const repos = [];
    let cur = null;
    for (const raw of stdout.split(/\r?\n/)) {
        const line = raw.trim();
        const head = line.match(/^\[([\w.-]+)\]$/);
        if (head && !['NEW', 'upd', 'sync', 'prune', 'SKIP', 'ERROR', 'WARN', 'PRIVATE', 'prune-held'].includes(head[1])) { cur = { repo: head[1], files: 0, pruned: [], held: 0, skipped: null }; repos.push(cur); continue; }
        if (!cur) continue;
        let m;
        if ((m = line.match(/^(\d+) file\(s\)/))) cur.files = Number(m[1]);
        else if ((m = line.match(/^\[prune-held\] (\d+) stale/))) cur.held = Number(m[1]);
        else if ((m = line.match(/^\[prune\] (?:removed|would remove) (.+)$/)) || (m = line.match(/^\[prune\] (\S+)$/))) cur.pruned.push(m[1]);
        else if (line.startsWith('[SKIP]') || line.startsWith('[ERROR]') || line.startsWith('[PRIVATE]')) cur.skipped = line;
    }
    return repos;
}

// ---------- process runner ----------

export function defaultRun(cmd, args, opts = {}) {
    const r = spawnSync(cmd, args, { cwd: opts.cwd, encoding: 'utf8', windowsHide: true, maxBuffer: 64 * 1024 * 1024, timeout: opts.timeout || 10 * 60_000 });
    return { code: r.status ?? (r.error ? 127 : 1), stdout: r.stdout || '', stderr: r.stderr || (r.error?.message ?? '') };
}

const PY = process.platform === 'win32' ? 'python' : 'python3';

function makeCtx(opts = {}) {
    const root = resolve(opts.root || join(dirname(fileURLToPath(import.meta.url)), '..', '..'));
    const now = opts.now ? opts.now() : new Date();
    const lines = [];
    const ctx = {
        root,
        apply: Boolean(opts.apply),
        noModel: Boolean(opts.noModel),
        now,
        today: opts.date || localDate(now),
        run: opts.run || defaultRun,
        env: opts.env || process.env,
        fetch: opts.fetch || ((url, init) => fetch(url, init)),
        out: opts.out || ((l) => { lines.push(l); console.log(l); }),
        lines,
    };
    ctx.git = (args, o = {}) => ctx.run('git', args, { cwd: o.cwd || root });
    ctx.gh = (args) => ctx.run('gh', args, { cwd: root });
    ctx.py = (script, args = []) => ctx.run(PY, [join('agent', 'scripts', script), ...args], { cwd: root });
    ctx.p = (...parts) => join(root, ...parts);
    return ctx;
}

const readJson = (r, what) => {
    if (r.code !== 0) throw new Error(`${what} failed: ${r.stderr.trim().slice(0, 200)}`);
    try { return JSON.parse(r.stdout || 'null'); } catch { throw new Error(`${what} returned invalid JSON`); }
};

// ---------- step 0: guard, merge gate ----------

/** Once-per-day guard. Throws if any check cannot run (caller fails closed). */
export function runGuard(ctx) {
    const f = ctx.git(['fetch', '-q', 'origin']);
    if (f.code !== 0) throw new Error('git fetch failed');
    const c = ctx.git(['cat-file', '-e', `origin/main:agent/notes/${ctx.today}.md`]);
    if (c.code !== 0 && c.code !== 128) throw new Error('cat-file failed');
    const prs = readJson(ctx.gh(['pr', 'list', '--repo', REPO_SLUG, '--state', 'open', '--limit', '100', '--json', 'title']), 'gh pr list');
    return guardVerdict({ noteMerged: c.code === 0, openPrTitles: prs.map((p) => p.title) }, ctx.today);
}

/** Merge gate for older obn: PRs. Dry-run evaluates and prints; apply merges. Returns [{number, outcome}]. */
export function runMergeGate(ctx) {
    const cands = readJson(ctx.gh(['pr', 'list', '--repo', REPO_SLUG, '--state', 'open', '--limit', '100', '--json',
        'number,title,headRefName,isCrossRepository,author,createdAt']), 'gh pr list').filter((p) => isMergeCandidate(p, ctx.today));
    const results = [];
    for (const pr of cands) {
        const n = pr.number;
        ctx.git(['fetch', 'origin', 'main', `pull/${n}/head`]);
        const diff = ctx.py('check-generated-diff.py', ['origin/main', 'FETCH_HEAD']);
        const view = readJson(ctx.gh(['pr', 'view', String(n), '--repo', REPO_SLUG, '--json', 'isDraft,statusCheckRollup,reviews']), `gh pr view ${n}`);
        const d = gateDecision({ diffOk: diff.code === 0, ci: ciState(view.statusCheckRollup), isDraft: view.isDraft });
        if (d.action === 'skip') {
            const first = diff.code !== 0 ? ` first path: ${(diff.stdout.split(/\r?\n/).find((l) => l.startsWith('  ')) || '').trim()}` : '';
            results.push({ number: n, outcome: `left open: ${d.reason}${d.reason.startsWith('not routine') ? first : ''}` });
            ctx.out(`gate: #${n} would NOT merge (${d.reason})`);
            continue;
        }
        if (!ctx.apply) { ctx.out(`gate: WOULD ${d.ready ? 'mark ready and ' : ''}merge #${n} (squash, delete branch)`); results.push({ number: n, outcome: 'would merge' }); continue; }
        if (d.ready) ctx.gh(['pr', 'ready', String(n), '--repo', REPO_SLUG]);
        let m = ctx.gh(['pr', 'merge', String(n), '--repo', REPO_SLUG, '--squash', '--delete-branch']);
        if (m.code !== 0 && onlyCodeRabbitBlocks(view.reviews)) m = ctx.gh(['pr', 'merge', String(n), '--repo', REPO_SLUG, '--squash', '--delete-branch', '--admin']);
        results.push({ number: n, outcome: m.code === 0 ? 'merged' : `merge failed: ${m.stderr.trim().slice(0, 120)}` });
        ctx.out(`gate: #${n} ${results.at(-1).outcome}`);
    }
    if (!cands.length) ctx.out('gate: no older obn: PRs to merge');
    return results;
}

/** Step 3 of step 0: back to main and ff-pull when clean. */
export function refreshMain(ctx) {
    if (!ctx.apply) { ctx.out('main: WOULD checkout main and pull --ff-only'); return 'dry-run'; }
    const st = ctx.git(['status', '--porcelain']);
    ctx.git(['checkout', 'main']);
    if (st.stdout.trim()) return 'main not clean; pull skipped';
    return ctx.git(['pull', '--ff-only']).code === 0 ? 'pulled' : 'pull failed';
}

// ---------- step 1: repo pull sweep, sync, logs, skip-gate ----------

export function pullSweep(ctx, repos) {
    const rows = [];
    for (const r of repos) {
        if (!r.path || !existsSync(r.path)) { rows.push({ repo: r.name, result: 'SKIPPED_MISSING', commits: 0, note: 'no local clone' }); continue; }
        const st = ctx.git(['status', '--short', '--branch'], { cwd: r.path });
        const lines = st.stdout.split(/\r?\n/).filter(Boolean);
        const branch = (lines[0] || '').replace(/^## /, '').split('...')[0].trim();
        const head = ctx.git(['symbolic-ref', '--short', 'refs/remotes/origin/HEAD'], { cwd: r.path });
        const def = head.code === 0 ? head.stdout.trim().replace(/^origin\//, '') : (branch === 'master' ? 'master' : 'main');
        if (lines.length > 1) { rows.push({ repo: r.name, result: 'SKIPPED_DIRTY', commits: 0, note: 'uncommitted changes' }); continue; }
        if (branch !== def) { rows.push({ repo: r.name, result: 'SKIPPED_BRANCH', commits: 0, note: `on ${branch}, default ${def}` }); continue; }
        if (!ctx.apply) { rows.push({ repo: r.name, result: 'WOULD_PULL', commits: 0, note: 'dry-run' }); continue; }
        const before = ctx.git(['rev-parse', 'HEAD'], { cwd: r.path }).stdout.trim();
        const pull = ctx.git(['pull', '--ff-only'], { cwd: r.path });
        if (pull.code !== 0) { rows.push({ repo: r.name, result: 'SKIPPED_DIVERGED', commits: 0, note: 'pull --ff-only failed' }); continue; }
        const n = ctx.git(['rev-list', '--count', `${before}..HEAD`], { cwd: r.path }).stdout.trim();
        rows.push({ repo: r.name, result: 'PULLED', commits: Number(n) || 0, note: 'ff-only' });
    }
    return rows;
}

/** Stale-worktree pass: prune, delete clean merged worktrees, flag unmerged ones older than 30 days. */
export function worktreeSweep(ctx, repos) {
    const acts = [], flagged = [];
    for (const r of repos) {
        if (!r.path || !existsSync(r.path)) continue;
        if (ctx.apply) ctx.git(['worktree', 'prune'], { cwd: r.path });
        const list = ctx.git(['worktree', 'list', '--porcelain'], { cwd: r.path }).stdout.split(/\r?\n\r?\n/).filter(Boolean);
        const head = ctx.git(['symbolic-ref', '--short', 'refs/remotes/origin/HEAD'], { cwd: r.path });
        const def = head.code === 0 ? head.stdout.trim() : 'origin/main';
        for (const block of list.slice(1)) { // first entry is the main worktree
            const wt = block.match(/^worktree (.+)$/m)?.[1];
            const br = block.match(/^branch refs\/heads\/(.+)$/m)?.[1];
            if (!wt || !br || resolve(wt) === ctx.root) continue;
            let merged = ctx.git(['merge-base', '--is-ancestor', br, def], { cwd: r.path }).code === 0;
            let via = 'ancestry';
            if (!merged && r.slug) {
                const prs = ctx.gh(['pr', 'list', '--repo', r.slug, '--head', br, '--state', 'merged', '--json', 'number']);
                const arr = prs.code === 0 ? JSON.parse(prs.stdout || '[]') : [];
                if (arr.length) { merged = true; via = `merged PR #${arr[0].number}`; }
            }
            const clean = !ctx.git(['status', '--porcelain'], { cwd: wt }).stdout.trim();
            if (merged && clean) {
                const rm = ctx.apply ? ctx.git(['worktree', 'remove', wt], { cwd: r.path }) : { code: 0 };
                acts.push(`${ctx.apply ? (rm.code === 0 ? 'REMOVED' : 'REMOVE_FAILED') : 'WOULD_REMOVE'} ${r.name} ${br} (${via})`);
            } else if (merged) {
                flagged.push(`${r.name} ${br}: merged (${via}) but has uncommitted changes`);
            } else {
                const age = ctx.git(['log', '-1', '--format=%ct', br], { cwd: r.path }).stdout.trim();
                if (age && (ctx.now.getTime() / 1000 - Number(age)) > 30 * 86400) flagged.push(`${r.name} ${br}: unmerged, older than 30 days`);
            }
        }
    }
    return { actions: acts, flagged };
}

export function appendLog(ctx, name, text) {
    if (!ctx.apply) return;
    const file = ctx.p('agent', 'logs', name);
    mkdirSync(dirname(file), { recursive: true });
    appendFileSync(file, text.endsWith('\n') ? text : `${text}\n`);
}

export const stamp = (ctx) => `${ctx.today} ${localTime(ctx.now)}`;

/** Skip-gate: which tracked repos have a mirror diff, from `git diff --stat` + `git status --short` on agent/repos/<repo>/. */
export function mirrorGate(ctx, repos, staleHubs) {
    const changed = [], detail = {};
    for (const r of repos) {
        const rel = `agent/repos/${r.name}/`;
        const stat = ctx.git(['diff', '--stat', '--', rel]).stdout.trim();
        const status = ctx.git(['status', '--short', '--', rel]).stdout.trim();
        if (stat || status) { changed.push(r.name); detail[r.name] = { stat: stat.split(/\r?\n/).slice(-3).join(' | '), status_lines: status ? status.split(/\r?\n/).length : 0 }; }
    }
    const tracked = new Set(repos.map((r) => r.name));
    return { changed, stale: staleHubs.filter((h) => tracked.has(h)), detail };
}

// ---------- step 3 data ----------

function activityRows(ctx, repos, today) {
    return repos.map((r) => {
        // scope.md's GitHub URL beats the clone's remote: renamed repos keep an old remote URL and
        // `gh ... --search` against the old name returns nothing. Owner fallback is the remote, per DAILY.
        let slug = r.slug;
        if (!slug && r.path && existsSync(r.path)) {
            const u = ctx.git(['remote', 'get-url', 'origin'], { cwd: r.path }).stdout.match(/github\.com[/:]([^/\s]+)\/([^/\s]+?)(?:\.git)?\s*$/);
            if (u) slug = `${u[1]}/${u[2]}`;
        }
        const row = { repo: r.name, prs: [], issues: [], commits: 0 };
        if (!slug) return { ...row, error: 'owner unknown' };
        const q = `updated:>=${today}`;
        const prs = ctx.gh(['pr', 'list', '--repo', slug, '--state', 'all', '--search', q, '--json', 'number,title,state', '--limit', '20']);
        const iss = ctx.gh(['issue', 'list', '--repo', slug, '--state', 'all', '--search', q, '--json', 'number,title,state', '--limit', '20']);
        if (prs.code !== 0) row.error = prs.stderr.trim().split(/\r?\n/)[0].slice(0, 80) || 'gh pr list failed';
        else row.prs = JSON.parse(prs.stdout || '[]');
        if (iss.code === 0) row.issues = JSON.parse(iss.stdout || '[]');
        if (r.path && existsSync(r.path)) row.commits = ctx.git(['log', `--since=${today} 00:00`, '--oneline'], { cwd: r.path }).stdout.split(/\r?\n/).filter(Boolean).length;
        return row;
    });
}

async function vigilTasks(ctx) {
    const key = ctx.env.VIGIL_MCP_KEY;
    if (!key) return { keySet: false };
    try {
        const res = await ctx.fetch(VIGIL_URL, { headers: { Authorization: `Bearer ${key}` }, signal: AbortSignal.timeout(30_000) });
        if (!res.ok) return { keySet: true, fetchError: `HTTP ${res.status}` };
        return { keySet: true, ctx: await res.json() };
    } catch (e) { return { keySet: true, fetchError: String(e.message || e).slice(0, 80) }; }
}

function weeklyChain(ctx, today) {
    const dow = weekday(today), week = isoWeek(today), file = `agent/notes/${week}.md`;
    const info = { mondayGoals: null, saturdayReview: null, weekNote: null };
    if (dow === 1 && !existsSync(ctx.p(file))) {
        const prev = isoWeek(addDays(today, -7));
        const prevPath = ctx.p('agent', 'notes', `${prev}.md`);
        const prevText = existsSync(prevPath) ? readFileSync(prevPath, 'utf8') : '';
        const hasReview = /## Week Review/.test(prevText);
        const coverage = prevText.match(/\*\*Coverage:\*\*\s*(.+)/)?.[1]?.trim();
        const projDir = ctx.p('agent', 'projects');
        const active = existsSync(projDir) ? readdirSync(projDir, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).filter((d) =>
            ctx.git(['log', '--since=7 days ago', '-1', '--format=%ci', '--', `agent/projects/${d}`]).stdout.trim()) : [];
        let links = null;
        if (ctx.apply) {
            const s = ctx.py('suggest-links.py', ['--write']);
            const rep = ctx.p('agent', 'reports', `link-suggestions-${today}.md`);
            if (s.code === 0 && existsSync(rep)) links = readFileSync(rep, 'utf8').split(/\r?\n/).filter((l) => /^- /.test(l)).length;
        }
        info.weekNote = { path: file, text: renderWeekNote({ week, monday: today, friday: addDays(today, 4), review: { exists: hasReview, week: prev, coverage }, activeProjects: active, linkSuggestions: links }) };
        info.mondayGoals = { due: hasReview, file, last_week_file: `agent/notes/${prev}.md` };
        if (!hasReview) info.mondayGoals = { due: false, file, last_week_file: null };
    }
    if (dow === 6) {
        const present = [1, 2, 3, 4, 5].map((i) => addDays(today, i - 6)).filter((d) => existsSync(ctx.p('agent', 'notes', `${d}.md`)));
        const wkExists = existsSync(ctx.p(file));
        info.saturdayReview = { due: wkExists && present.length > 0, file, notes: present.map((d) => `agent/notes/${d}.md`), reason: !wkExists ? 'no weekly note' : present.length ? null : 'no notes this week' };
    }
    return info;
}

// ---------- finishing: model, indexes, placeholders, PR ----------

export function invokeModel(ctx, handoffPath) {
    const args = [join('agent', 'scripts', 'routine-run.mjs'), '--prompt', 'agent/prompts/DAILY-MODEL.md', '--model', 'MAX',
        '--tools', 'Read,Write,Edit,Glob,Grep', '--cwd', ctx.root, '--budget', '1', '--max-turns', '40', '--minutes', '20'];
    if (!ctx.apply || ctx.noModel) { ctx.out(`model: WOULD run node ${args.join(' ')}`); return 'not run'; }
    const r = ctx.run(process.execPath, args, { cwd: ctx.root, timeout: 30 * 60_000 });
    return r.code === 0 ? 'ran' : `failed (exit ${r.code})`;
}

function changedPaths(ctx) {
    const r = ctx.git(['status', '--porcelain', '-z']);
    return new Set(r.stdout.split('\0').filter((e) => e.length > 3).map((e) => e.slice(3)));
}

const COMMIT_PATHS = [/^agent\/repos\//, /^agent\/notes\/.+\.md$/, /^agent\/reports\/.+\.md$/, /^agent\/topics\/.+\.md$/, /^agent\/VAULT-MAP\.md$/];

/** Commit by exact path, run the routine-owned diff check, push, open the PR. Apply only. */
export function openPr(ctx, extraPaths) {
    const date = ctx.today;
    let branch = `obn/daily-note-${date}`;
    const st = ctx.gh(['pr', 'view', branch, '--repo', REPO_SLUG, '--json', 'state', '-q', '.state']);
    const state = st.code === 0 ? st.stdout.trim() : '';
    if (state === 'MERGED' || state === 'CLOSED') branch = `${branch}-${ctx.now.getHours()}${pad(ctx.now.getMinutes())}`;
    ctx.git(['checkout', '-B', branch]);
    const paths = [...new Set([...extraPaths, ...[...changedPaths(ctx)].filter((p) => COMMIT_PATHS.some((re) => re.test(p)))])];
    if (!paths.length) return { branch, pr: null, note: 'nothing to commit' };
    ctx.git(['add', '-A', '--', ...paths]);
    const msg = `obn: daily note ${date}\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\n`;
    const c = ctx.git(['commit', '-m', msg]);
    if (c.code !== 0) throw new Error(`commit failed: ${c.stderr.trim().slice(0, 200)}`);
    const chk = ctx.py('check-generated-diff.py', ['origin/main', 'HEAD']);
    if (chk.code !== 0) {
        const bad = chk.stdout.split(/\r?\n/).filter((l) => l.startsWith('  ')).map((l) => l.trim());
        for (const b of bad) ctx.git(['restore', '--source=origin/main', '--staged', '--', b]);
        ctx.git(['commit', '--amend', '--no-edit']);
    }
    const push = ctx.git(['push', '-u', 'origin', branch]);
    if (push.code !== 0) throw new Error(`push failed: ${push.stderr.trim().slice(0, 200)}`);
    const body = `Daily note and mirror sync for ${date}, produced by agent/scripts/daily-run.mjs.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)`;
    const pr = ctx.gh(['pr', 'create', '--repo', REPO_SLUG, '--base', 'main', '--head', branch, '--title', `obn: daily note ${date}`, '--body', body]);
    ctx.git(['checkout', 'main']);
    return { branch, pr: pr.code === 0 ? pr.stdout.trim() : null, note: pr.code === 0 ? 'opened' : `pr create failed: ${pr.stderr.trim().slice(0, 120)}` };
}

/** "Prove the run did something": a dated entry in each of the four logs. */
export function proveRun(ctx) {
    const missing = [];
    for (const name of ['daily-git-sync.log', 'stale-worktrees.log', 'obn-repo.log', 'obn-review.log']) {
        const f = ctx.p('agent', 'logs', name);
        if (!existsSync(f) || !readFileSync(f, 'utf8').includes(ctx.today)) missing.push(name);
    }
    return missing;
}

// ---------- orchestration ----------

export async function runDaily(opts = {}) {
    const ctx = makeCtx(opts);
    const { today } = ctx;
    ctx.out(`daily-run ${today} (${ctx.apply ? 'APPLY' : 'dry-run'})`);
    const summary = { today, apply: ctx.apply, exit: 0 };

    // step 0 guard: fail closed
    let guard;
    try { guard = runGuard(ctx); } catch (e) {
        ctx.out('INCOMPLETE: once-per-day guard could not run');
        appendLog(ctx, 'obn-review.log', `${today}: guard failed (${e.message}); run stopped.`);
        return { ...summary, exit: 2, incomplete: 'guard' };
    }
    summary.guard = guard;
    ctx.out(`guard: ${guard.ran ? `already ran (note merged: ${guard.noteMerged}, open PR: ${guard.prHit})` : 'first run today'}`);

    summary.gate = runMergeGate(ctx);
    summary.main = refreshMain(ctx);
    const scopePath = ctx.p('agent', 'projects', 'scope.md');
    const repos = parseScope(readFileSync(scopePath, 'utf8'));
    summary.repoCount = repos.length;

    // step 1: pulls + doc sync
    const pulls = pullSweep(ctx, repos);
    summary.pulls = pulls.reduce((a, r) => (a[r.result] = (a[r.result] || 0) + 1, a), {});
    const sync = ctx.run('pwsh', ['-NoProfile', '-File', ctx.p('agent', 'scripts', 'sync-repos.ps1'), '-Prune', ...(ctx.apply ? [] : ['-DryRun'])], { cwd: ctx.root });
    const synced = parseSyncOutput(sync.stdout);
    summary.sync = { exit: sync.code, repos: synced.length, files: synced.reduce((a, r) => a + r.files, 0) };
    if (sync.code !== 0) ctx.out(`sync-repos.ps1 exit ${sync.code}: ${sync.stderr.trim().slice(0, 160)}`);
    const heldLines = synced.filter((r) => r.held).map((r) => `[prune-held] ${r.repo}: ${r.held} stale files over -MaxPrune; nothing deleted`);

    const wt = worktreeSweep(ctx, repos);
    summary.worktrees = { actions: wt.actions.length, flagged: wt.flagged.length };
    ctx.out(`repos: ${repos.length} tracked; pulls ${JSON.stringify(summary.pulls)}; sync exit ${sync.code}, ${summary.sync.files} files across ${synced.length} repos; worktrees ${wt.actions.length} to remove, ${wt.flagged.length} flagged`);

    appendLog(ctx, 'daily-git-sync.log', `\n## daily-git-sync — ${stamp(ctx)}\n| repo | result | commits | note |\n|---|---|---|---|\n${pulls.map((r) => `| ${r.repo} | ${r.result} | ${r.commits} | ${r.note} |`).join('\n')}`);
    appendLog(ctx, 'stale-worktrees.log', `\n## stale-worktrees — ${stamp(ctx)}\nActions taken: ${wt.actions.length ? '\n' + wt.actions.map((a) => `- ${a}`).join('\n') : 'none'}\nStale live worktrees needing review: ${wt.flagged.length ? '\n' + wt.flagged.map((a) => `- ${a}`).join('\n') : 'none'}`);
    appendLog(ctx, 'obn-repo.log', `\n## obn-repo — ${stamp(ctx)}\n${synced.map((r) => [
        r.skipped ? `SKIPPED ${r.repo} — ${r.skipped}` : `OK ${r.repo} — ${r.files} .md files staged`,
        ...(r.pruned.length ? [`PRUNED ${r.repo} — ${r.pruned.join(', ')}`] : []),
        ...(r.held ? [`HELD ${r.repo} — ${r.held} stale files over -MaxPrune; nothing deleted`] : []),
    ].join('\n')).join('\n')}`);

    // skip-gate
    const vaultMap = existsSync(ctx.p('agent', 'VAULT-MAP.md')) ? readFileSync(ctx.p('agent', 'VAULT-MAP.md'), 'utf8') : '';
    const gate = mirrorGate(ctx, repos, parseStaleHubs(vaultMap));
    summary.changed = gate.changed.length;
    summary.stale = gate.stale.length;
    ctx.out(`skip-gate: ${gate.changed.length} changed repos, ${gate.stale.length} stale hubs`);

    if (guard.ran) {
        appendLog(ctx, 'obn-review.log', `${today}: SKIPPED (guard: note/PR already exists)`);
        for (const s of NOT_AUTOMATED) ctx.out(`NOT AUTOMATED: ${s}`);
        const missing = proveRun(ctx);
        if (ctx.apply && missing.length) ctx.out(`INCOMPLETE: missing log entries: ${missing.join(', ')}`);
        ctx.out('guard hit: no note or PR created');
        return { ...summary, noteWritten: false, skip_model: true };
    }

    // step 3: note skeleton
    const rows = activityRows(ctx, repos, today);
    const active = new Set(rows.filter((r) => r.prs.length || r.issues.length || r.commits).map((r) => r.repo));
    const vigil = await vigilTasks(ctx);
    const skips = pulls.filter((p) => p.result.startsWith('SKIPPED_')).map((p) => ({ repo: p.repo, result: p.result, note: p.note }));
    const counts = Object.entries(summary.pulls).map(([k, v]) => `${k} ${v}`).join(', ');
    const notes = [
        `- Repo pull sweep: ${counts || 'no repos'}.`,
        `- Worktrees: ${wt.actions.length} ${ctx.apply ? 'removed' : 'would be removed'}, ${wt.flagged.length} flagged.${wt.flagged.length ? ' ' + wt.flagged.join('; ') + '.' : ''}`,
        `- Mirror sync: ${synced.reduce((a, r) => a + r.files, 0)} files staged across ${synced.length} repos.`,
        ...heldLines.map((l) => `- ${l}`),
        gate.changed.length ? `- Mirror changes: ${gate.changed.join(', ')}.` : '- No mirror changes.',
        gate.stale.length ? `- Stale hubs: ${gate.stale.join(', ')}.` : '- No stale hubs.',
        ...summary.gate.map((g) => `- Merge gate: #${g.number} ${g.outcome}.`),
    ];
    const weekly = weeklyChain(ctx, today);
    const noteFile = `agent/notes/${today}.md`;
    // Reflections are templated from counts (no model): the model runs only for hub synthesis,
    // Monday goals or the Saturday review.
    const reflectionsDue = false;
    const reflections = `${active.size} repo(s) with activity, ${gate.changed.length} mirror change(s), ${gate.stale.length} stale hub(s). No model synthesis.`;
    const note = renderNote({ today, activity: activitySection(rows, today), tasks: tasksSection({ keySet: vigil.keySet, ctx: vigil.ctx, fetchError: vigil.fetchError, active, skips, today }), notes, reflections });
    const handoff = buildHandoff({ today, changed: gate.changed, stale: gate.stale, reflectionsDue, mondayGoals: weekly.mondayGoals, saturdayReview: weekly.saturdayReview, noteFile });
    handoff.mirror_diffs = gate.detail;
    const handoffPath = ctx.p('agent', 'reports', 'daily-handoff.json');
    mkdirSync(dirname(handoffPath), { recursive: true });
    writeFileSync(handoffPath, JSON.stringify(handoff, null, 2) + '\n'); // gitignored, safe in dry-run
    summary.skip_model = handoff.skip_model;
    ctx.out(`handoff: skip_model=${handoff.skip_model} reflections=${reflectionsDue} monday_goals=${Boolean(weekly.mondayGoals?.due)} saturday_review=${Boolean(weekly.saturdayReview?.due)}`);

    if (!ctx.apply) {
        ctx.out(`dry-run: WOULD write ${noteFile}${weekly.weekNote ? ` and ${weekly.weekNote.path}` : ''}, run vault indexes/link repair/orphan check, commit and open PR obn/daily-note-${today}`);
        invokeModel(ctx, handoffPath);
        for (const s of NOT_AUTOMATED) ctx.out(`NOT AUTOMATED: ${s}`);
        return { ...summary, noteWritten: false };
    }

    writeFileSync(ctx.p(noteFile), note);
    if (weekly.weekNote) writeFileSync(ctx.p(weekly.weekNote.path), weekly.weekNote.text);
    summary.model = handoff.skip_model ? 'skipped (nothing to synthesize)' : invokeModel(ctx, handoffPath);
    if (handoff.changed_repos.length || handoff.stale_hubs.length) {
        if (summary.model === 'ran' || handoff.skip_model) {
            appendLog(ctx, 'obn-review.log', `${today}: obn-review run across ${gate.changed.length + gate.stale.length} repos (${[...gate.changed, ...gate.stale].join(', ')}). All synthesis files written to ${ctx.p('agent', 'repos')}.`);
        } else appendLog(ctx, 'obn-review.log', `${today}: obn-review model step ${summary.model}; hubs not refreshed (${[...gate.changed, ...gate.stale].join(', ')}).`);
    } else appendLog(ctx, 'obn-review.log', `${today}: obn-review run across 0 repos (none). All synthesis files written to ${ctx.p('agent', 'repos')}.`);

    // vault indexes, link repair, orphan check
    const before = changedPaths(ctx);
    ctx.py('build-vault-indexes.py');
    ctx.py('fix-doc-links.py', ['--vault', '--under=repos/', '--unlink-dead-mirrors', '--write']);
    const generated = [...changedPaths(ctx)].filter((p) => !before.has(p));
    const orph = ctx.py('find-orphans.py', ['--check']);
    const orphLines = orph.stdout.split(/\r?\n/).filter((l) => /notes|orphans|reachable|unresolved/i.test(l)).map((l) => `- ${l.trim()}`);
    const fileText = readFileSync(ctx.p(noteFile), 'utf8')
        .replace(REFLECTIONS_PENDING, REFLECTIONS_FALLBACK)
        .replace('\n\n## Reflections', `${orph.code !== 0 ? '\n- Orphan check failed: a note has no link path or two share a file name; a human must fix it.' : ''}${orphLines.length ? '\n' + orphLines.join('\n') : ''}\n\n## Reflections`);
    writeFileSync(ctx.p(noteFile), fileText);
    if (weekly.weekNote) writeFileSync(ctx.p(weekly.weekNote.path), readFileSync(ctx.p(weekly.weekNote.path), 'utf8').replace(GOALS_PENDING, GOALS_FALLBACK));
    summary.orphanExit = orph.code;

    const missing = proveRun(ctx);
    summary.pr = openPr(ctx, [noteFile, ...(weekly.weekNote ? [weekly.weekNote.path] : []), ...generated]);
    ctx.out(`pr: ${summary.pr.pr || summary.pr.note}`);
    for (const s of NOT_AUTOMATED) ctx.out(`NOT AUTOMATED: ${s}`);
    if (missing.length) { ctx.out(`INCOMPLETE: missing log entries: ${missing.join(', ')}`); summary.exit = 1; }
    ctx.out('DONE: start a new session for follow-ups.');
    return summary;
}

export function parseCli(argv) {
    const o = { apply: false, noModel: false };
    for (let i = 0; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--apply') o.apply = true;
        else if (a === '--dry-run') o.apply = false;
        else if (a === '--no-model') o.noModel = true;
        else if (a === '--root' || a === '--date') {
            if (i + 1 >= argv.length) throw new Error(`missing value for ${a}`);
            o[a.slice(2)] = argv[++i];
        } else throw new Error(`unknown argument: ${a}`);
    }
    if (o.date && !/^\d{4}-\d{2}-\d{2}$/.test(o.date)) throw new Error('--date must be YYYY-MM-DD');
    return o;
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
    let opts;
    try { opts = parseCli(process.argv.slice(2)); } catch (e) { console.error(`daily-run: ${e.message}`); process.exit(2); }
    runDaily(opts).then((s) => process.exit(s.exit), (e) => { console.error(`daily-run: ${e.message}`); process.exit(2); });
}
