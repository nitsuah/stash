#!/usr/bin/env node
// pipeline-run.mjs: week-sotu, monthly-tire-kick and monthly-pmo-audit as code.
//
//   node agent/scripts/pipeline-run.mjs <sotu|tire|pmo> [--apply] [--no-model] [--root <stash>]
//
// Each subcommand runs its deterministic pre-step script first and calls the model (through
// routine-run.mjs and 9router, no plan quota) only when that script says there is something to
// judge. Default is a dry run that prints the plan; --apply runs it for real.
//
//   sotu  sotu.py --verify-hints in a fresh worktree; quiet week => templated focus note;
//         otherwise SOTU-MODEL.md judges the hinted items and writes the note. Opens a PR.
//   tire  tire_intake.py; skip_model => --apply the ledger update and open a PR; otherwise the
//         model runs TIRE.md (fixes, PRs).
//   pmo   pmo_prep.py; no changed repo => idle; otherwise the model runs PMO.md.
//
// NOT AUTOMATED: publishing the SOTU artifact (needs the Claude app's Artifact tool) and the
// SOTU tier-drift edit to scope.md (the report prints the drift line; edit by hand).
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync, appendFileSync, rmSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = resolve(HERE, '..', '..');
const PY = process.platform === 'win32' ? 'python' : 'python3';

export const MODEL_TOOLS = {
    sotu: 'Read,Write,Edit,Bash(gh *)',
    tire: 'Read,Write,Edit,Glob,Grep,Bash(gh *),Bash(git *),Bash(docker *),Bash(npm *),Bash(node *),Bash(python *)',
    pmo: 'Read,Write,Edit,Glob,Grep,Bash(gh *),Bash(git *),Bash(python *)',
};
export const PROMPTS = {
    sotu: 'agent/prompts/SOTU-MODEL.md',
    tire: 'agent/prompts/TIRE.md',
    pmo: 'agent/prompts/PMO.md',
};
export const COMMIT_PATHS = {
    sotu: ['agent/reports/sotu/', 'agent/projects/scope.md'],
    tire: ['agent/reports/findings-ledger.md', 'agent/reports/tire-kick-'],
};

export function pad(n) { return String(n).padStart(2, '0'); }
export function localDate(d = new Date()) { return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; }

/** ISO year-week like 2026-W44 (Thursday-based). */
export function isoWeek(d = new Date()) {
    const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    t.setUTCDate(t.getUTCDate() + 4 - (t.getUTCDay() || 7));
    const y = t.getUTCFullYear();
    const w = Math.ceil(((t - Date.UTC(y, 0, 1)) / 86400000 + 1) / 7);
    return `${y}-W${pad(w)}`;
}

/** True when sotu.py's sidecar says nothing changed and nothing has evidence to judge. */
export function isQuiet(verify) {
    return Boolean(verify && verify.all_skip && verify.delta_empty);
}

/** Replace the `<!-- focus -->` marker in the report with the note. */
export function setFocus(md, note) {
    return md.includes('<!-- focus -->') ? md.replace('<!-- focus -->', note) : `${md}\n${note}\n`;
}

/** Any object with `changed: true` anywhere in pmo-prep.json (shape-agnostic). */
export function anyChanged(node) {
    if (Array.isArray(node)) return node.some(anyChanged);
    if (node && typeof node === 'object') return node.changed === true || Object.values(node).some(anyChanged);
    return false;
}

/** Keep only `git status --porcelain` paths under one of the allowed prefixes. */
export function filterPaths(porcelain, prefixes) {
    return porcelain.split('\n').map((l) => l.slice(3).trim().replace(/^"|"$/g, '')).filter(
        (p) => p && prefixes.some((x) => p.startsWith(x)),
    );
}

function sh(cmd, args, opts = {}) {
    const r = spawnSync(cmd, args, { encoding: 'utf8', windowsHide: true, ...opts });
    return { code: r.status ?? 1, out: r.stdout || '', err: r.stderr || '' };
}

function log(root, line) {
    const dir = join(root, 'agent', 'logs');
    mkdirSync(dir, { recursive: true });
    appendFileSync(join(dir, 'pipeline-run.log'), `${localDate()} | ${line}\n`);
    console.log(line);
}

function routineRun(wt, name, extra = []) {
    const args = [
        join(wt, 'agent', 'scripts', 'routine-run.mjs'), '--cwd', wt, '--prompt', PROMPTS[name],
        '--model', 'MAX', '--tools', MODEL_TOOLS[name], '--budget', name === 'sotu' ? '1' : '3',
        '--minutes', name === 'sotu' ? '20' : '40', '--log', join(wt, 'agent', 'logs', 'routine-run.log'),
        '--out', join(wt, 'agent', 'logs', `${name}-out`), ...extra,
    ];
    return sh(process.execPath, args);
}

function worktree(root, name, branch) {
    const wt = join(root, '.claude', 'worktrees', name);
    sh('git', ['-C', root, 'fetch', '-q', 'origin']);
    if (existsSync(wt)) throw new Error(`worktree ${wt} already exists; remove it first`);
    const r = sh('git', ['-C', root, 'worktree', 'add', '-q', wt, '-b', branch, 'origin/main']);
    if (r.code) throw new Error(`worktree add failed: ${r.err.trim()}`);
    return wt;
}

function commitAndPr(root, wt, branch, title, body, prefixes) {
    const status = sh('git', ['-C', wt, 'status', '--porcelain']).out;
    const paths = filterPaths(status, prefixes);
    if (!paths.length) return 'nothing to commit';
    sh('git', ['-C', wt, 'add', '-f', '--', ...paths]);
    const c = sh('git', ['-C', wt, '-c', 'core.autocrlf=false', 'commit', '-q', '-m',
        `${title}\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`]);
    if (c.code) return `commit failed: ${c.err.trim()}`;
    const p = sh('git', ['-C', wt, 'push', '-q', '-u', 'origin', branch]);
    if (p.code) return `push failed: ${p.err.trim()}`;
    const pr = sh('gh', ['pr', 'create', '--repo', 'nitsuah/stash', '--base', 'main', '--head', branch,
        '--title', title, '--body', `${body}\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)`]);
    return pr.code ? `pr create failed: ${pr.err.trim()}` : pr.out.trim().split('\n').pop();
}

function cleanup(root, wt) {
    sh('git', ['-C', root, 'worktree', 'remove', '--force', wt]);
    if (existsSync(wt)) rmSync(wt, { recursive: true, force: true });
    sh('git', ['-C', root, 'worktree', 'prune']);
}

function runSotu(o) {
    const week = isoWeek();
    const branch = `sotu/${week}`;
    if (!o.apply) return log(o.root, `DRY RUN sotu: would build ${branch} in a worktree, run sotu.py --verify-hints, ${o.noModel ? 'write a templated note' : 'call the model only if not quiet'}, open a PR`);
    const wt = worktree(o.root, `sotu-${week}`, branch);
    try {
        const b = sh(PY, [join(wt, 'agent', 'scripts', 'sotu.py'), '--verify-hints'], { cwd: wt });
        if (b.code) return log(o.root, `sotu: build failed (${b.err.trim().split('\n').pop()})`);
        const dir = join(wt, 'agent', 'reports', 'sotu');
        const verify = existsSync(join(dir, 'sotu-verify.json')) ? JSON.parse(readFileSync(join(dir, 'sotu-verify.json'), 'utf8')) : null;
        const quiet = isQuiet(verify);
        const mdName = readdirSync(dir).filter((f) => /^sotu-\d{4}-W\d{2}\.md$/.test(f)).sort().pop();
        let note = quiet ? 'No change since last run.' : null;
        if (!quiet && !o.noModel) {
            const m = routineRun(wt, 'sotu');
            if (m.code) note = `Model step failed (${m.out.trim().split('\n').pop() || m.err.trim()}); review the hinted items by hand.`;
        } else if (!quiet) {
            note = 'Model step skipped (--no-model); review the hinted items by hand.';
        }
        if (note && mdName) {
            const p = join(dir, mdName);
            writeFileSync(p, setFocus(readFileSync(p, 'utf8'), note));
            const dp = join(dir, 'sotu-data.json');
            if (existsSync(dp)) { const d = JSON.parse(readFileSync(dp, 'utf8')); d.focus = note; writeFileSync(dp, JSON.stringify(d, null, 1)); }
        }
        const res = commitAndPr(o.root, wt, branch, `sotu: ${week}`,
            `Weekly State of the Union (${quiet ? 'quiet week, no model' : 'model-assisted'}). Machine-generated; merge when CI is green. The artifact publish is not automated.`, COMMIT_PATHS.sotu);
        log(o.root, `sotu ${week}: quiet=${quiet} -> ${res}`);
    } finally { cleanup(o.root, wt); }
}

function runTire(o) {
    const day = localDate();
    if (!o.apply) return log(o.root, 'DRY RUN tire: would run tire_intake.py; skip_model => --apply the ledger and open a PR, else call the model with TIRE.md');
    const wt = worktree(o.root, `tire-${day}`, `tire/${day}`);
    try {
        const s = join(wt, 'agent', 'scripts', 'tire_intake.py');
        const dry = sh(PY, [s], { cwd: wt });
        if (dry.code) return log(o.root, `tire: intake failed (${dry.err.trim().split('\n').pop()})`);
        const inp = join(wt, 'agent', 'reports', 'tire-input.json');
        const skip = existsSync(inp) ? JSON.parse(readFileSync(inp, 'utf8')).skip_model === true : false;
        if (skip) {
            const a = sh(PY, [s, '--apply'], { cwd: wt });
            if (a.code) return log(o.root, `tire: apply failed (${a.err.trim().split('\n').pop()})`);
            const res = commitAndPr(o.root, wt, `tire/${day}`, `tire-kick: ledger update ${day}`,
                'Findings intake from repo-health issues; no quick items, so no model ran.', COMMIT_PATHS.tire);
            return log(o.root, `tire ${day}: skip_model -> ${res}`);
        }
        if (o.noModel) return log(o.root, `tire ${day}: quick items present, model skipped (--no-model)`);
        const m = routineRun(wt, 'tire');
        log(o.root, `tire ${day}: model run exit ${m.code}`);
    } finally { cleanup(o.root, wt); }
}

function runPmo(o) {
    if (!o.apply) return log(o.root, 'DRY RUN pmo: would run pmo_prep.py; no changed repo => idle, else call the model with PMO.md');
    const prep = sh(PY, [join(o.root, 'agent', 'scripts', 'pmo_prep.py')], { cwd: o.root });
    if (prep.code) return log(o.root, `pmo: prep failed (${prep.err.trim().split('\n').pop()})`);
    const f = join(o.root, 'agent', 'reports', 'pmo-prep.json');
    const changed = existsSync(f) && anyChanged(JSON.parse(readFileSync(f, 'utf8')));
    if (!changed) return log(o.root, 'pmo: no changed repo, idle');
    if (o.noModel) return log(o.root, 'pmo: changed repos present, model skipped (--no-model)');
    const m = routineRun(o.root, 'pmo');
    log(o.root, `pmo: model run exit ${m.code}`);
}

export function parseArgs(argv) {
    const o = { cmd: argv[0], apply: false, noModel: false, root: DEFAULT_ROOT };
    for (let i = 1; i < argv.length; i++) {
        if (argv[i] === '--apply') o.apply = true;
        else if (argv[i] === '--no-model') o.noModel = true;
        else if (argv[i] === '--root') o.root = resolve(argv[++i] || '');
        else throw new Error(`unknown argument: ${argv[i]}`);
    }
    if (!['sotu', 'tire', 'pmo'].includes(o.cmd)) throw new Error('usage: pipeline-run.mjs <sotu|tire|pmo> [--apply] [--no-model] [--root <dir>]');
    return o;
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
    try {
        const o = parseArgs(process.argv.slice(2));
        ({ sotu: runSotu, tire: runTire, pmo: runPmo })[o.cmd](o);
    } catch (e) {
        console.error(String(e.message || e));
        process.exit(1);
    }
}
