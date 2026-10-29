import test from 'node:test';
import assert from 'node:assert/strict';
import { extractLocs, extractLastmod } from '../src/validation.js';

test('extractLocs stays fast on a long loc body with surrounding whitespace', () => {
    const xml = `<loc>${' '.repeat(50000)}x${' '.repeat(50000)}</loc>`;
    const start = Date.now();
    const out = extractLocs(xml);
    assert.ok(Date.now() - start < 100);
    assert.deepEqual(out, ['x']);
});

test('extractLocs stays fast on an unterminated loc with long whitespace', () => {
    const start = Date.now();
    extractLocs(`<loc>${' '.repeat(100000)}`);
    assert.ok(Date.now() - start < 100);
});

test('extractLocs keeps valid behaviour: trims, decodes &amp;, skips empty', () => {
    const xml = '<loc> https://a.example/x?a=1&amp;b=2 </loc><loc>   </loc><loc>https://a.example/y</loc>';
    assert.deepEqual(extractLocs(xml), ['https://a.example/x?a=1&b=2', 'https://a.example/y']);
});

test('extractLastmod trims and returns null when missing or blank', () => {
    assert.equal(extractLastmod('<lastmod> 2026-01-02 </lastmod>'), '2026-01-02');
    assert.equal(extractLastmod('<lastmod>  </lastmod>'), null);
    assert.equal(extractLastmod('<url></url>'), null);
    const start = Date.now();
    extractLastmod(`<lastmod>${' '.repeat(100000)}`);
    assert.ok(Date.now() - start < 100);
});
