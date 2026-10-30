import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cmpVersion, isoHours, evalTask, evalDispatch, evalDrift, evalRuns, render } from './local-audit.mjs';

const NOW = Date.parse('2026-10-30T12:00:00Z');
const ago = (h) => new Date(NOW - h * 3600_000).toISOString();

test('cmpVersion and isoHours', () => {
    assert.ok(cmpVersion('0.5.99', '0.5.104') < 0);
    assert.equal(cmpVersion('1.0.0', '1.0.0'), 0);
    assert.equal(isoHours('PT1H'), 1);
    assert.equal(isoHours('PT30M'), 0.5);
    assert.equal(isoHours('P1D'), 24);
    assert.equal(isoHours(''), null);
});

test('evalTask: green, disabled, never-run, stale, unknown', () => {
    const ok = { Name: 'imps-dispatch', State: 'Ready', LastRun: ago(1), LastResult: 0 };
    assert.equal(evalTask(ok, NOW).status, 'GREEN');
    assert.equal(evalTask({ ...ok, State: 'Disabled' }, NOW).status, 'RED');
    assert.match(evalTask({ ...ok, LastResult: 267011 }, NOW).detail, /never ran/);
    assert.match(evalTask({ ...ok, LastRun: ago(4) }, NOW).detail, /3x/);
    const unk = evalTask({ Name: 'new-job', State: 'Ready', LastRun: ago(1), LastResult: 0 }, NOW);
    assert.equal(unk.status, 'RED');
    assert.match(unk.detail, /CATCHUP/);
});

test('evalDispatch: counts, skip>cycle, errors, old events ignored', () => {
    const ev = (event, h, extra = {}) => JSON.stringify({ at: ago(h), event, ...extra });
    const good = [ev('cycle', 1), ev('cycle', 2), ev('skip', 3), ev('cycle', 400)];
    const g = evalDispatch(good, NOW);
    assert.equal(g.status, 'GREEN');
    assert.match(g.detail, /cycle 2/);
    assert.equal(evalDispatch([ev('cycle', 5)], NOW).status, 'RED');
    assert.match(evalDispatch([ev('cycle', 1), ev('skip', 2), ev('skip', 3)], NOW).detail, /more skip than cycle/);
    assert.match(evalDispatch([ev('cycle', 1), ev('run-error', 2)], NOW).detail, /1 error/);
});

test('evalDrift', () => {
    assert.equal(evalDrift('v0.5.104', 'ghcr.io/x/9router:0.5.99').status, 'RED');
    assert.equal(evalDrift('v0.5.104', '9router:0.5.104').status, 'GREEN');
    assert.equal(evalDrift('', '9router:latest').status, 'YELLOW');
    assert.equal(evalDrift('v0.5.112', 'x/9router:latest', '', '2026-10-01T00:00:00Z', '2026-10-20T00:00:00Z').status, 'RED');
    assert.equal(evalDrift('v0.5.112', 'x/9router:latest', '', '2026-10-25T00:00:00Z', '2026-10-20T00:00:00Z').status, 'GREEN');
});

test('evalRuns uses latest completed run; render lists RED count', () => {
    assert.equal(evalRuns('w', [{ status: 'in_progress' }, { status: 'completed', conclusion: 'failure', createdAt: 'x' }]).status, 'RED');
    assert.equal(evalRuns('w', [{ status: 'completed', conclusion: 'success', createdAt: 'x' }]).status, 'GREEN');
    const md = render([{ id: 'a', job: 'j', status: 'RED', detail: 'a|b' }], '2026-10-30');
    assert.match(md, /\*\*1 RED\*\*/);
    assert.match(md, /a\/b/);
});
