import test from 'node:test';
import assert from 'node:assert/strict';
import { isValidLastmod, isSameHostname, readLimitedBody, locs, lastmodOf, sitemapsFromRobots, admitEntry, MAX_LOC_LENGTH, MAX_RETAINED_CHARS } from '../src/validation.js';

test('lastmod validates ISO syntax, real calendar dates, clock and offset ranges', () => {
    assert.equal(isValidLastmod('2026-02-28'), true);
    assert.equal(isValidLastmod('2024-02-29T23:59:59Z'), true);
    assert.equal(isValidLastmod('2026-01-01T10:30:00+14:00'), true);
    assert.equal(isValidLastmod('2026-02-30'), false);
    assert.equal(isValidLastmod('2026-02-30T25:00:00+15:00'), false);
    assert.equal(isValidLastmod('2026-01-01T12:60:00Z'), false);
    assert.equal(isValidLastmod('last tuesday'), false);
});

test('same-host checks compare hostnames rather than scheme or port', () => {
    assert.equal(isSameHostname('https://example.com:8443/page', 'http://example.com'), true);
    assert.equal(isSameHostname('https://other.example/page', 'http://example.com'), false);
    assert.equal(isSameHostname('not-a-url', 'http://example.com'), false);
});

test('sitemap response bodies are bounded before buffering', async () => {
    assert.equal((await readLimitedBody(new Response('abc'), 3)).toString(), 'abc');
    await assert.rejects(readLimitedBody(new Response('abc'), 2), /exceeds 2 byte limit/);
});

test('admitEntry enforces MAX_LOC_LENGTH and MAX_RETAINED_CHARS boundaries', () => {
    const budget = { used: 0 };
    const locAtMax = 'a'.repeat(MAX_LOC_LENGTH);
    const locOverMax = 'a'.repeat(MAX_LOC_LENGTH + 1);

    assert.equal(admitEntry(budget, locAtMax, null), true);
    assert.equal(budget.used, MAX_LOC_LENGTH);

    const budget2 = { used: 0 };
    assert.equal(admitEntry(budget2, locOverMax, null), false);
    assert.equal(budget2.used, 0);

    const budget3 = { used: MAX_RETAINED_CHARS - MAX_LOC_LENGTH };
    const locToBudget = 'b'.repeat(MAX_LOC_LENGTH);
    assert.equal(admitEntry(budget3, locToBudget, null), true);
    assert.equal(budget3.used, MAX_RETAINED_CHARS);

    // Keep the location at its limit so rejection exercises the retained budget.
    const budget4 = { used: MAX_RETAINED_CHARS - MAX_LOC_LENGTH + 1 };
    const locOverBudget = 'b'.repeat(MAX_LOC_LENGTH);
    assert.equal(admitEntry(budget4, locOverBudget, null), false);
    assert.equal(budget4.used, MAX_RETAINED_CHARS - MAX_LOC_LENGTH + 1);
});
