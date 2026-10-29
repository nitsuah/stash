import test from 'node:test';
import assert from 'node:assert/strict';
import { isValidLastmod, isSameHostname, readLimitedBody, locs, lastmodOf, sitemapsFromRobots } from '../src/validation.js';

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
