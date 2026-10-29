import test from 'node:test';
import assert from 'node:assert/strict';
import { locs } from '../src/main.js';

test('fixed regex handles pathological input under 100ms', () => {
    const pathological = '<loc>' + '/'.repeat(50000) + '</loc>';
    const start = Date.now();
    const result = locs(pathological);
    const elapsed = Date.now() - start;
    assert.ok(elapsed < 100, `Fixed regex took ${elapsed}ms, expected < 100ms`);
    assert.equal(result.length, 1);
    assert.equal(result[0], '/'.repeat(50000));
});

test('fixed regex handles valid sitemap inputs correctly', () => {
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/page1</loc></url>
  <url><loc>https://example.com/page 2</loc></url>
  <url><loc>https://example.com/page&param=1</loc></url>
</urlset>`;
    const result = locs(xml);
    assert.equal(result.length, 3);
    assert.ok(result.some(r => r.includes('page1')));
    assert.ok(result.some(r => r.includes('page 2')));
    assert.ok(result.some(r => r.includes('&')));
});

test('fixed regex correctly replaces &', () => {
    const xml = '<loc>https://example.com/?a=1&b=2</loc>';
    const result = locs(xml);
    assert.equal(result[0], 'https://example.com/?a=1&b=2');
});