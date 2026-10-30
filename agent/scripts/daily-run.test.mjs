import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
    localDate, isoWeek, parseScope, guardVerdict, isMergeCandidate, ciState, gateDecision, onlyCodeRabbitBlocks,
    parseStaleHubs, openWorkItems, isFutureQuarter, tasksSection, activitySection, buildHandoff, parseSyncOutput,
    parseCli, runDaily, NOT_AUTOMATED,
} from './daily-run.mjs';

const SCOPE = [
    '# Scope',
    '## Tracked (active)',
    '| Repo | Tier | Local path | GitHub URL | Org | Visibility |',
    '|---|---|---|---|---|---|',
    '| alpha | T1 | `/nonexistent/alpha` | https://github.com/acme/alpha | acme | public |',
    '| beta | — | `/nonexistent/beta` (formerly `old-beta`) | https://github.com/acme/beta (renamed) | acme | **private** |',
    '',
    '## Not tracked',
    '| Repo | Local path |',
    '|---|---|',
    '| fork | `/x` |',
    '',
].join('\n');

test('localDate uses local calendar fields, not UTC', () => {
    assert.equal(localDate(new Date(2026, 9, 30, 23, 30)), '2026-10-30');
    assert.equal(localDate(new Date(2026, 0, 2, 0, 5)), '2026-01-02');
});

test('isoWeek handles the ISO year boundary', () => {
    assert.equal(isoWeek('2027-01-02'), '2026-W53');
    assert.equal(isoWeek('2026-10-30'), '2026-W44');
    assert.equal(isoWeek('2026-10-26'), '2026-W44');
});

test('parseScope reads only the Tracked table with path, slug, aliases and visibility', () => {
    const r = parseScope(SCOPE);
    assert.deepEqual(r.map((x) => x.name), ['alpha', 'beta']);
    assert.equal(r[0].slug, 'acme/alpha');
    assert.equal(r[0].path, '/nonexistent/alpha');
    assert.deepEqual(r[1].aliases, ['old-beta']);
    assert.equal(r[1].private, true);
    assert.equal(r[0].private, false);
});

test('guardVerdict: merged note or exact open PR title means already ran', () => {
    assert.equal(guardVerdict({ noteMerged: false, openPrTitles: ['obn: daily note 2026-10-29'] }, '2026-10-30').ran, false);
    assert.equal(guardVerdict({ noteMerged: true, openPrTitles: [] }, '2026-10-30').ran, true);
    assert.equal(guardVerdict({ noteMerged: false, openPrTitles: ['obn: daily note 2026-10-30'] }, '2026-10-30').ran, true);
    assert.equal(guardVerdict({ noteMerged: false, openPrTitles: ['obn: daily note 2026-10-30 (retry)'] }, '2026-10-30').ran, false);
});

test('isMergeCandidate follows the DAILY conditions exactly', () => {
    const ok = { title: 'obn: daily note 2026-10-29', headRefName: 'obn/daily-note-2026-10-29', isCrossRepository: false, author: { login: 'nitsuah' }, createdAt: new Date(2026, 9, 29, 12).toISOString() };
    assert.equal(isMergeCandidate(ok, '2026-10-30'), true);
    assert.equal(isMergeCandidate(ok, '2026-10-29'), false, 'never merged the day it opens');
    assert.equal(isMergeCandidate({ ...ok, title: 'fix: obn: x' }, '2026-10-30'), false);
    assert.equal(isMergeCandidate({ ...ok, headRefName: 'obn-notes-run' }, '2026-10-30'), false);
    assert.equal(isMergeCandidate({ ...ok, isCrossRepository: true }, '2026-10-30'), false);
    assert.equal(isMergeCandidate({ ...ok, author: { login: 'someone' } }, '2026-10-30'), false);
});

test('ciState and gateDecision', () => {
    assert.equal(ciState([]), 'green');
    assert.equal(ciState([{ conclusion: 'SUCCESS' }, { conclusion: 'SKIPPED' }]), 'green');
    assert.equal(ciState([{ conclusion: 'FAILURE' }]), 'red');
    assert.equal(ciState([{ status: 'IN_PROGRESS', conclusion: '' }]), 'pending');
    assert.deepEqual(gateDecision({ diffOk: true, ci: 'green', isDraft: true }), { action: 'merge', ready: true });
    assert.equal(gateDecision({ diffOk: false, ci: 'green' }).action, 'skip');
    assert.equal(gateDecision({ diffOk: true, ci: 'red' }).action, 'skip');
    assert.equal(gateDecision({ diffOk: true, ci: 'pending' }).action, 'skip');
    const cr = { author: { login: 'coderabbitai' }, state: 'CHANGES_REQUESTED' };
    assert.equal(onlyCodeRabbitBlocks([cr]), true);
    assert.equal(onlyCodeRabbitBlocks([cr, { author: { login: 'human' }, state: 'CHANGES_REQUESTED' }]), false);
    assert.equal(onlyCodeRabbitBlocks([cr, { author: { login: 'coderabbitai' }, state: 'APPROVED' }]), false);
});

test('parseStaleHubs, openWorkItems, future quarter filter and sections', () => {
    assert.deepEqual(parseStaleHubs('- **Stale hubs** (no date; DAILY step 2 refreshes these first): [[repos/alpha|alpha]] (never) · [[repos/beta]] (2026-01-01)\n'), ['alpha', 'beta']);
    assert.deepEqual(parseStaleHubs('nothing'), []);
    const items = openWorkItems({ open_work: { p0: [{ repo: 'alpha', title: 'fix it' }], p1: [{ repo: 'beta', title: 'later [2027-Q1]' }], p2: [{ repo: 'alpha', title: 'x' }] } });
    assert.equal(items.length, 2);
    assert.equal(isFutureQuarter('later [2027-Q1]', '2026-10-30'), true);
    assert.equal(isFutureQuarter('now [2026-Q4]', '2026-10-30'), false);
    const t = tasksSection({ keySet: true, ctx: { open_work: items }, active: new Set(['alpha', 'beta']), skips: [{ repo: 'beta', result: 'SKIPPED_DIRTY', note: 'uncommitted changes' }], today: '2026-10-30' });
    assert.deepEqual(t, ['- P0 alpha: fix it', '- Human needed: beta SKIPPED_DIRTY (uncommitted changes)']);
    assert.match(tasksSection({ keySet: false, active: new Set(), skips: [], today: 'x' })[0], /vigil key not set/);
    assert.match(tasksSection({ keySet: true, fetchError: 'HTTP 500', active: new Set(), skips: [], today: 'x' })[0], /unavailable \(HTTP 500\)/);
    assert.deepEqual(activitySection([], '2026-10-30'), ['- No activity on tracked repos on 2026-10-30.']);
});

test('handoff shape and skip_model', () => {
    const base = { today: '2026-10-30', changed: [], stale: [], reflectionsDue: false, mondayGoals: null, saturdayReview: null, noteFile: 'agent/notes/2026-10-30.md' };
    const quiet = buildHandoff(base);
    assert.equal(quiet.skip_model, true);
    assert.deepEqual(Object.keys(quiet).sort(), ['changed_repos', 'date', 'monday_goals', 'not_automated', 'note_file', 'reflections_due', 'saturday_review', 'skip_model', 'stale_hubs']);
    assert.equal(buildHandoff({ ...base, changed: ['alpha'] }).skip_model, false);
    assert.equal(buildHandoff({ ...base, stale: ['b'] }).skip_model, false);
    assert.equal(buildHandoff({ ...base, reflectionsDue: true }).skip_model, false);
    assert.equal(buildHandoff({ ...base, mondayGoals: { due: true } }).skip_model, false);
    assert.equal(buildHandoff({ ...base, saturdayReview: { due: true } }).skip_model, false);
    assert.equal(buildHandoff({ ...base, mondayGoals: { due: false } }).skip_model, true);
});

test('parseSyncOutput and parseCli', () => {
    const r = parseSyncOutput('\n[alpha]\n  [upd] README.md\n  2 file(s) copied\n\n[beta]\n  [prune-held] 30 stale files exceed -MaxPrune 25; nothing deleted.\n  0 file(s) copied\n');
    assert.deepEqual(r.map((x) => [x.repo, x.files, x.held]), [['alpha', 2, 0], ['beta', 0, 30]]);
    assert.equal(parseCli([]).apply, false);
    assert.equal(parseCli(['--apply']).apply, true);
    assert.equal(parseCli(['--apply', '--dry-run']).apply, false);
    assert.throws(() => parseCli(['--bogus']));
    assert.throws(() => parseCli(['--date', 'tomorrow']));
});

function fixture() {
    const root = mkdtempSync(join(tmpdir(), 'dr-'));
    mkdirSync(join(root, 'agent', 'projects'), { recursive: true });
    writeFileSync(join(root, 'agent', 'projects', 'scope.md'), SCOPE);
    writeFileSync(join(root, 'agent', 'VAULT-MAP.md'), '- **Stale hubs** (x): [[repos/alpha|alpha]] (never)\n');
    return root;
}
const MUTATING = [/^git push/, /^git commit/, /^git checkout/, /^git pull/, /^git add/, /^gh pr merge/, /^gh pr ready/, /^gh pr create/, /^git worktree (remove|prune)/];

function stub(calls, over = {}) {
    return (cmd, args) => {
        const line = `${cmd} ${args.join(' ')}`;
        calls.push(line);
        for (const [re, res] of Object.entries(over)) if (new RegExp(re).test(line)) return res;
        if (/^git cat-file/.test(line)) return { code: 128, stdout: '', stderr: '' };
        if (/^gh pr list .*--json title$/.test(line)) return { code: 0, stdout: '[]', stderr: '' };
        if (/^gh pr list .*isCrossRepository/.test(line)) {
            const pr = { number: 7, title: 'obn: daily note 2026-10-29', headRefName: 'obn/daily-note-2026-10-29', isCrossRepository: false, author: { login: 'nitsuah' }, createdAt: new Date(2026, 9, 29, 9).toISOString() };
            return { code: 0, stdout: JSON.stringify([pr]), stderr: '' };
        }
        if (/^gh pr view 7/.test(line)) return { code: 0, stdout: JSON.stringify({ isDraft: true, statusCheckRollup: [], reviews: [] }), stderr: '' };
        if (/^gh (pr|issue) list/.test(line)) return { code: 0, stdout: '[]', stderr: '' };
        if (/^pwsh/.test(line)) return { code: 0, stdout: '\n[alpha]\n  1 file(s) copied\n', stderr: '' };
        if (/git (diff|status)/.test(line) && /agent\/repos\/alpha/.test(line)) return { code: 0, stdout: ' agent/repos/alpha/README.md | 2 +-\n', stderr: '' };
        return { code: 0, stdout: '', stderr: '' };
    };
}

test('dry-run: no push/merge/commit calls, no tracked writes, handoff written, NOT AUTOMATED listed', async () => {
    const root = fixture();
    const calls = [];
    const out = [];
    const s = await runDaily({ root, date: '2026-10-30', now: () => new Date(2026, 9, 30, 8, 0), run: stub(calls), env: {}, out: (l) => out.push(l) });
    assert.equal(s.exit, 0);
    for (const c of calls) for (const re of MUTATING) assert.ok(!re.test(c), `mutating call in dry-run: ${c}`);
    assert.ok(out.some((l) => l.includes('WOULD') && l.includes('merge #7')));
    assert.ok(calls.some((c) => /^pwsh .*-DryRun/.test(c)), 'sync runs with -DryRun');
    for (const n of NOT_AUTOMATED) assert.ok(out.includes(`NOT AUTOMATED: ${n}`));
    assert.ok(out.some((l) => l.startsWith('model: WOULD run')));
    assert.equal(existsSync(join(root, 'agent', 'notes', '2026-10-30.md')), false);
    assert.equal(existsSync(join(root, 'agent', 'logs')), false);
    const h = JSON.parse(readFileSync(join(root, 'agent', 'reports', 'daily-handoff.json'), 'utf8'));
    assert.deepEqual(h.changed_repos, ['alpha']);
    assert.deepEqual(h.stale_hubs, ['alpha']);
    assert.equal(h.skip_model, false);
});

test('guard failure fails closed with INCOMPLETE and nothing else runs', async () => {
    const root = fixture();
    const calls = [];
    const out = [];
    const s = await runDaily({ root, date: '2026-10-30', run: stub(calls, { '^git fetch -q origin': { code: 1, stdout: '', stderr: 'boom' } }), env: {}, out: (l) => out.push(l) });
    assert.equal(s.exit, 2);
    assert.equal(out[1], 'INCOMPLETE: once-per-day guard could not run');
    assert.ok(!calls.some((c) => /^pwsh|^gh pr merge/.test(c)));
});

test('guard hit: dry-run still evaluates the gate but creates no note', async () => {
    const root = fixture();
    const out = [];
    const s = await runDaily({ root, date: '2026-10-30', run: stub([], { '^git cat-file': { code: 0, stdout: '', stderr: '' } }), env: {}, out: (l) => out.push(l) });
    assert.equal(s.noteWritten, false);
    assert.equal(s.guard.ran, true);
    assert.ok(out.includes('guard hit: no note or PR created'));
});
