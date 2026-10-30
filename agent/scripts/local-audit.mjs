#!/usr/bin/env node
// local-audit.mjs: zero-model, read-only "Local jobs audit" from agent/prompts/CATCHUP.md.
// Checks Windows Task Scheduler jobs, the imps loop, 9router image drift, Claude local
// scheduled-task files and the last stash workflow runs. Prints a markdown report, appends
// to agent/logs/ops-catchup.log (gitignored) and exits 1 when anything is RED.
// It never enables, edits, runs, rebuilds or restarts anything.
//
//   node agent/scripts/local-audit.mjs [--no-log] [--json]
import { spawnSync } from 'node:child_process';
import { appendFileSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HOUR = 3600_000;
const HERE = dirname(fileURLToPath(import.meta.url));
const LOG = join(HERE, '..', 'logs', 'ops-catchup.log');
const GH_REPO = 'nitsuah/stash';

// Known root-folder jobs (keep in sync with the CATCHUP.md table). Interval in hours.
export const KNOWN_TASKS = {
    'imps-dispatch': 1, 'imps-label-watch': 5 / 60, 'Sync 9router fork': 1,
    'routine-daily-run': 48, 'routine-sotu': 168, 'routine-tire': 744, 'routine-pmo': 744, 'routine-fin-checkin': 744,
};

const row = (id, job, status, detail) => ({ id, job, status, detail });

/** Compare dotted versions; returns <0, 0, >0. */
export function cmpVersion(a, b) {
    const pa = String(a).split('.').map(Number);
    const pb = String(b).split('.').map(Number);
    for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
        const d = (pa[i] || 0) - (pb[i] || 0);
        if (d) return d;
    }
    return 0;
}

/** Parse a simple ISO8601 duration (PT1H, PT30M, P1D) to hours; null when unparseable. */
export function isoHours(s) {
    const m = /^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?)?$/.exec(s || '');
    if (!m || !s || s === 'P' || s === 'PT') return null;
    return Number(m[1] || 0) * 24 + Number(m[2] || 0) + Number(m[3] || 0) / 60;
}

/** Evaluate one scheduled task record from the PowerShell collector. */
export function evalTask(t, now = Date.now()) {
    const reasons = [];
    const known = Object.hasOwn(KNOWN_TASKS, t.Name);
    const interval = known ? KNOWN_TASKS[t.Name] : isoHours(t.Interval);
    if (!known) reasons.push('not in the CATCHUP.md table (add it)');
    if (t.State === 'Disabled') reasons.push('Disabled');
    if (t.LastResult === 267011) reasons.push('never ran (267011)');
    else if (t.LastResult !== 0 && t.LastResult != null) reasons.push(`LastTaskResult ${t.LastResult}`);
    const last = t.LastRun ? Date.parse(t.LastRun) : NaN;
    if (Number.isFinite(last) && interval && now - last > 3 * interval * HOUR) {
        reasons.push(`last run ${Math.round((now - last) / HOUR)}h ago (> 3x ${+interval.toFixed(2)}h)`);
    }
    const detail = `state ${t.State}; last ${t.LastRun || 'never'}; result ${t.LastResult}; next ${t.NextRun || 'none'}`;
    return row('a', `task ${t.Name}`, reasons.length ? 'RED' : 'GREEN', reasons.length ? `${reasons.join('; ')} (${detail})` : detail);
}

/** Evaluate dispatch.jsonl lines over the last 7 days. */
export function evalDispatch(lines, now = Date.now()) {
    const evs = [];
    for (const l of lines) {
        try { const e = JSON.parse(l); if (Date.parse(e.at) >= now - 7 * 24 * HOUR) evs.push(e); } catch { /* skip junk */ }
    }
    const n = (f) => evs.filter(f).length;
    const counts = {
        cycle: n((e) => e.event === 'cycle'), skip: n((e) => e.event === 'skip'), pr: n((e) => e.event === 'pr'),
        'gate-fail': n((e) => e.event === 'gate-fail'), 'fix-sweep': n((e) => e.event === 'fix-sweep'),
        'needs-human': n((e) => e.result === 'needs-human' || e.event === 'needs-human'),
        error: n((e) => /(^|-)error$/.test(e.event || '') && e.event !== 'run-error'), 'run-error': n((e) => e.event === 'run-error'),
    };
    const reasons = [];
    const lastCycle = Math.max(0, ...evs.filter((e) => e.event === 'cycle').map((e) => Date.parse(e.at)));
    if (!lastCycle || now - lastCycle > 3 * HOUR) reasons.push('no cycle in the last 3h');
    if (counts.skip > counts.cycle) reasons.push('more skip than cycle');
    if (counts.error || counts['run-error']) reasons.push(`${counts.error + counts['run-error']} error/run-error`);
    const text = Object.entries(counts).map(([k, v]) => `${k} ${v}`).join(', ');
    return row('b', 'imps loop (7d)', reasons.length ? 'RED' : 'GREEN', `${reasons.length ? `${reasons.join('; ')}. ` : ''}${text}`);
}

/** 9router drift: running image tag vs repo's latest tag. */
export function evalDrift(repoTag, image, syncLine = '', imageCreated = '', tagDate = '') {
    const rv = /(\d+\.\d+\.\d+)/.exec(repoTag || '')?.[1];
    const iv = /(\d+\.\d+\.\d+)/.exec(image || '')?.[1];
    const tail = syncLine ? `; sync log: ${syncLine}` : '';
    if (rv && !iv && Date.parse(imageCreated) && Date.parse(tagDate)) {
        const stale = Date.parse(imageCreated) < Date.parse(tagDate);
        return row('c', '9router image drift', stale ? 'RED' : 'GREEN', `image ${image} built ${imageCreated.slice(0, 10)}, repo ${rv} tagged ${tagDate.slice(0, 10)}${stale ? '; suggest docker compose build + recreate (not done here)' : ''}${tail}`);
    }
    if (!rv || !iv) return row('c', '9router image drift', 'YELLOW', `cannot compare (repo tag ${repoTag || '?'}, image ${image || '?'})${tail}`);
    if (cmpVersion(iv, rv) < 0) {
        return row('c', '9router image drift', 'RED', `running ${iv}, repo latest ${rv}; suggest docker compose build + recreate (not done here)${tail}`);
    }
    return row('c', '9router image drift', 'GREEN', `running ${iv}, repo ${rv}${tail}`);
}

/** Latest completed workflow run -> status row. */
export function evalRuns(workflow, runs) {
    const done = (runs || []).find((r) => r.status === 'completed');
    if (!done) return row('e', `workflow ${workflow}`, 'YELLOW', 'no completed run found');
    const bad = ['failure', 'timed_out', 'startup_failure'].includes(done.conclusion);
    return row('e', `workflow ${workflow}`, bad ? 'RED' : 'GREEN', `${done.conclusion} ${done.createdAt} ${done.url || ''}`.trim());
}

// ── collectors (read-only shell-outs) ────────────────────────────────────
const run = (bin, args, opts = {}) => {
    const r = spawnSync(bin, args, { encoding: 'utf8', windowsHide: true, timeout: 60_000, ...opts });
    return { code: r.status, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
};

function collectTasks(home) {
    if (process.platform !== 'win32') return [row('a', 'Task Scheduler', 'YELLOW', 'skipped (not Windows)')];
    const hp = home.replace(/\\/g, '\\\\').replace(/'/g, "''");
    const ps = `$h='${hp}'; $re='(?i)'+$h+'\\\\(\\.imps|scripts|code)';
$r = @(Get-ScheduledTask -TaskPath '\\' | ForEach-Object {
  $a = ($_.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)" }) -join ' ; '
  if ($a -match $re) {
    $i = Get-ScheduledTaskInfo -InputObject $_
    $rep = ($_.Triggers | ForEach-Object { $_.Repetition.Interval } | Where-Object { $_ } | Select-Object -First 1)
    [pscustomobject]@{ Name=$_.TaskName; State=[string]$_.State; Interval=$rep; Action=$a;
      LastRun=$(if($i.LastRunTime.Year -gt 1999){$i.LastRunTime.ToString('o')}); LastResult=[int64]$i.LastTaskResult;
      NextRun=$(if($i.NextRunTime.Year -gt 1999){$i.NextRunTime.ToString('o')}) }
  } })
ConvertTo-Json -InputObject $r -Compress`;
    const r = run('powershell', ['-NoProfile', '-NonInteractive', '-Command', ps]);
    if (r.code !== 0 || !r.out) return [row('a', 'Task Scheduler', 'YELLOW', `query failed: ${r.err.slice(0, 200) || 'no output'}`)];
    try { return [].concat(JSON.parse(r.out)).map((t) => evalTask(t)); } catch (e) { return [row('a', 'Task Scheduler', 'YELLOW', `bad output: ${e.message}`)]; }
}

function collectImps(home) {
    const rows = [];
    const f = join(home, '.imps', 'dispatch.jsonl');
    if (!existsSync(f)) rows.push(row('b', 'imps loop (7d)', 'YELLOW', 'no dispatch.jsonl'));
    else rows.push(evalDispatch(readFileSync(f, 'utf8').split('\n').filter(Boolean)));
    try {
        const kit = readFileSync(join(home, '.imps', 'kit-path.txt'), 'utf8').replace(/^﻿/, '').trim();
        const r = run('node', [join(kit, 'imps', 'imp.mjs'), 'report']);
        if (r.code === 0) rows.push(row('b', 'imps report', 'GREEN', r.out.split('\n').slice(0, 2).join(' / ')));
    } catch { /* kit optional */ }
    const g = run('gh', ['search', 'prs', '--owner', 'nitsuah', '--state', 'open', '--label', 'imp:needs-human', '--json', 'url,repository']);
    if (g.code === 0) {
        try {
            const prs = JSON.parse(g.out);
            rows.push(row('b', 'imp:needs-human PRs', prs.length ? 'RED' : 'GREEN', prs.length ? prs.map((p) => p.url).join(' ') : 'none'));
        } catch { rows.push(row('b', 'imp:needs-human PRs', 'YELLOW', 'bad gh output')); }
    } else rows.push(row('b', 'imp:needs-human PRs', 'YELLOW', 'gh search failed'));
    return rows;
}

function collectDrift(home) {
    const repo = join(home, 'code', '9router');
    const tag = run('git', ['-C', repo, 'describe', '--tags', '--abbrev=0']);
    const img = run('docker', ['inspect', '9router', '--format', '{{.Config.Image}}|{{.Created}}']);
    const logf = join(home, 'scripts', 'logs', '9router-sync.log');
    const last = existsSync(logf) ? readFileSync(logf, 'utf8').trim().split('\n').pop() : '';
    if (tag.code !== 0 || img.code !== 0) return [row('c', '9router image drift', 'YELLOW', `unavailable (git ${tag.code}, docker ${img.code})`)];
    const [image, created] = img.out.split('|');
    const td = run('git', ['-C', repo, 'log', '-1', '--format=%cI', tag.out]);
    return [evalDrift(tag.out, image, last, created, td.out)];
}

function collectClaudeTasks(home) {
    const dir = join(home, '.claude', 'scheduled-tasks');
    if (!existsSync(dir)) return [row('d', 'Claude local tasks', 'YELLOW', 'no scheduled-tasks dir')];
    const names = readdirSync(dir).filter((d) => !d.startsWith('_') && existsSync(join(dir, d, 'SKILL.md')));
    const list = names.map((d) => {
        const m = /^description:\s*(.*)$/m.exec(readFileSync(join(dir, d, 'SKILL.md'), 'utf8'));
        const age = Math.round((Date.now() - statSync(join(dir, d, 'SKILL.md')).mtimeMs) / (24 * HOUR));
        return `${d} (SKILL.md ${age}d old${m ? `: ${m[1].slice(0, 60)}` : ''})`;
    });
    // Enabled state and lastRunAt live in the Claude app (list_scheduled_tasks), not on disk.
    return [row('d', 'Claude local tasks', 'GREEN', `${names.length} task files; run state needs list_scheduled_tasks. ${list.join('; ')}`)];
}

function collectRuns() {
    return ['obn-health.yml', 'repo-health.yml'].map((wf) => {
        const r = run('gh', ['run', 'list', '--repo', GH_REPO, '--workflow', wf, '--limit', '5', '--json', 'status,conclusion,createdAt,url']);
        if (r.code !== 0) return row('e', `workflow ${wf}`, 'YELLOW', 'gh run list failed');
        try { return evalRuns(wf, JSON.parse(r.out)); } catch { return row('e', `workflow ${wf}`, 'YELLOW', 'bad gh output'); }
    });
}

export function render(rows, date) {
    const lines = [`# Local jobs audit ${date}`, '', '| # | Job | Status | Detail |', '|---|---|---|---|'];
    for (const r of rows) lines.push(`| ${r.id} | ${r.job} | ${r.status} | ${r.detail.replace(/\|/g, '/')} |`);
    const red = rows.filter((r) => r.status === 'RED');
    lines.push('', red.length ? `**${red.length} RED**` : 'audit: all green');
    return lines.join('\n');
}

export function main(argv = process.argv.slice(2)) {
    const home = homedir();
    const date = new Date().toISOString().slice(0, 10);
    const rows = [...collectTasks(home), ...collectImps(home), ...collectDrift(home), ...collectClaudeTasks(home), ...collectRuns()];
    console.log(argv.includes('--json') ? JSON.stringify(rows, null, 2) : render(rows, date));
    const red = rows.filter((r) => r.status === 'RED');
    if (!argv.includes('--no-log')) {
        mkdirSync(dirname(LOG), { recursive: true });
        const out = red.length ? red.map((r) => `${date} | audit | ${r.job} | ${r.detail.slice(0, 200)}`) : [`${date} | audit: all green`];
        appendFileSync(LOG, out.join('\n') + '\n');
    }
    return red.length ? 1 : 0;
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) process.exit(main());
