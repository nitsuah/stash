import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, existsSync, utimesSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { parseArgs, splitTools, truncate, acquireLock, logLine, buildPrompt, main, PRE_OUTPUT_MAX } from './routine-run.mjs';

const tmp = () => mkdtempSync(join(tmpdir(), 'rr-'));
const NOW = Date.parse('2026-10-30T12:00:00Z');

function setup(extra = []) {
    const dir = tmp();
    const argv = ['--prompt', 'agent/prompts/DEMO.md', '--cwd', dir, ...extra];
    return { dir, argv, log: join(dir, 'agent/logs/routine-run.log'), out: join(dir, 'agent/logs/routine-out') };
}
const okKit = (calls = []) => ({
    runClaude: async (a) => {
        calls.push(a);
        return { end: 'success', finalText: 'report', turns: 4, tokens: { input: 10, output: 5, cacheRead: 1, cacheWrite: 0 } };
    },
});

test('parseArgs applies defaults and parses flags', () => {
    const o = parseArgs(['--prompt', 'a/B.md', '--cwd', tmpdir()]);
    assert.equal(o.model, 'MAX');
    assert.equal(o.skipExit, 3);
    assert.equal(o.maxTurns, 30);
    assert.equal(o.minutes, 15);
    const p = parseArgs(['--prompt', 'x.md', '--model', 'cheap', '--budget', '0.5', '--skip-exit', '7', '--pre', 'node a.mjs', '--cwd', tmpdir()]);
    assert.deepEqual([p.model, p.budget, p.skipExit, p.pre], ['cheap', 0.5, 7, 'node a.mjs']);
});

test('parseArgs rejects bad input', () => {
    assert.throws(() => parseArgs([]), /--prompt/);
    assert.throws(() => parseArgs(['--prompt', 'x', '--nope', '1']), /unknown flag/);
    assert.throws(() => parseArgs(['--prompt', 'x', '--budget']), /missing value/);
    assert.throws(() => parseArgs(['--prompt', 'x', '--minutes', 'abc']), /minutes/);
});

test('splitTools keeps commas inside parentheses', () => {
    assert.deepEqual(splitTools('Read,Bash(node *),Write'), ['Read', 'Bash(node *)', 'Write']);
    assert.deepEqual(splitTools('Bash(a,b), Read'), ['Bash(a,b)', 'Read']);
});

test('truncate caps bytes and notes the drop', () => {
    assert.equal(truncate('short'), 'short');
    const t = truncate('x'.repeat(PRE_OUTPUT_MAX + 100));
    assert.ok(t.startsWith('x'.repeat(PRE_OUTPUT_MAX)));
    assert.match(t, /\[truncated 100 bytes\]/);
    assert.ok(buildPrompt('p.md', 'y'.repeat(50000)).length < PRE_OUTPUT_MAX + 200);
});

test('lock: fresh blocks, stale (>3h) is replaced', () => {
    const f = join(tmp(), 'l.lock');
    const NOW = Date.now();
    assert.equal(acquireLock(f, NOW), true);
    assert.equal(acquireLock(f, NOW), false);
    const old = (NOW - 4 * 3600_000) / 1000;
    utimesSync(f, old, old);
    assert.equal(acquireLock(f, NOW), true);
});

test('logLine format strips separators', () => {
    assert.equal(logLine({ date: 'd', routine: 'r', outcome: 'a|b', turns: 2, tokens: 9 }), 'd | r | a b | 2 | 9');
});

test('skip-exit logs idle and never touches the model', async () => {
    const s = setup(['--pre', 'gate', '--skip-exit', '3']);
    let probed = false;
    const code = await main(s.argv, {
        now: () => NOW,
        runPre: () => ({ code: 3, stdout: '' }),
        kit: { runClaude: () => assert.fail('model ran') },
        probe: async () => { probed = true; return true; },
    });
    assert.equal(code, 0);
    assert.equal(probed, false);
    assert.match(readFileSync(s.log, 'utf8'), /2026-10-30 \| DEMO \| idle/);
    assert.equal(existsSync(join(s.out, '.DEMO.lock')), false);
});

test('other non-zero pre fails open and the model runs', async () => {
    const s = setup(['--pre', 'gate']);
    const calls = [];
    const code = await main(s.argv, {
        now: () => NOW, runPre: () => ({ code: 1, stdout: 'partial', stderr: 'boom' }), kit: okKit(calls), probe: async () => true,
    });
    assert.equal(code, 0);
    assert.equal(calls.length, 1);
    assert.match(calls[0].prompt, /^Read agent\/prompts\/DEMO\.md and follow it\./);
    assert.match(calls[0].prompt, /pre-step failed/);
    const lines = readFileSync(s.log, 'utf8').trim().split('\n');
    assert.match(lines[0], /pre-failed exit 1/);
    assert.match(lines[1], /DEMO \| success \| 4 \| 16/);
    assert.equal(readFileSync(join(s.out, '2026-10-30.md'), 'utf8'), 'report');
});

test('router down skips and logs', async () => {
    const s = setup();
    const code = await main(s.argv, { now: () => NOW, kit: { runClaude: () => assert.fail() }, probe: async () => false });
    assert.equal(code, 0);
    assert.match(readFileSync(s.log, 'utf8'), /skip-9router-down/);
});

test('fresh lock short-circuits; model failure exits 1', async () => {
    const s = setup();
    assert.equal(acquireLock(join(s.out, '.DEMO.lock')), true);
    assert.equal(await main(s.argv, { kit: { runClaude: () => assert.fail() }, probe: async () => true }), 0);
    assert.match(readFileSync(s.log, 'utf8'), /locked/);
    const s2 = setup();
    const kit = { runClaude: async () => ({ end: 'killed-max-turns', finalText: '', turns: 31, tokens: {} }) };
    assert.equal(await main(s2.argv, { now: () => NOW, kit, probe: async () => true }), 1);
});

test('large pre output is truncated in the prompt', async () => {
    const s = setup(['--pre', 'gate']);
    const calls = [];
    await main(s.argv, { now: () => NOW, runPre: () => ({ code: 0, stdout: 'z'.repeat(30000) }), kit: okKit(calls), probe: async () => true });
    assert.ok(calls[0].prompt.length < PRE_OUTPUT_MAX + 200);
    assert.match(calls[0].prompt, /\[truncated/);
});
