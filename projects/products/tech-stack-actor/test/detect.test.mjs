// Run: node --test projects/products/tech-stack-actor/test   (Node 22, no dependencies)
import test from 'node:test';
import assert from 'node:assert/strict';
import { detect, lintFingerprints } from '../src/detect.js';
import { loadFingerprints } from '../src/load.js';

const all = loadFingerprints();

test('fingerprint data is sound: names unique, regexes compile, every example matches its own fingerprint', () => {
    assert.deepEqual(lintFingerprints(all), []);
});

test('there are fingerprints in every category file', () => {
    const categories = new Set(all.map((f) => f.category));
    for (const c of ['CMS', 'JavaScript frameworks', 'Analytics', 'Web servers', 'CDN', 'E-commerce']) assert.ok(categories.has(c), `no fingerprints for category ${c}`);
});

test('detects WordPress from the generator tag and implies PHP', () => {
    const hits = detect({ html: '', meta: { generator: 'WordPress 6.4.2' }, scripts: ['/wp-includes/js/jquery.js'] }, all);
    const names = hits.map((h) => h.name);
    assert.ok(names.includes('WordPress'));
    assert.ok(names.includes('PHP'));
    assert.equal(hits.find((h) => h.name === 'PHP').implied, true);
});

test('detects a server from a header and Cloudflare from cf-ray', () => {
    const names = detect({ headers: { server: 'cloudflare', 'cf-ray': '8abc-IAD' } }, all).map((h) => h.name);
    assert.ok(names.includes('Cloudflare'));
});

test('a plain page matches nothing', () => {
    assert.deepEqual(detect({ html: '<html><body>hello</body></html>', headers: {}, scripts: [], links: [], cookies: [], meta: {} }, all), []);
});

test('lint rejects patterns that are too generic', () => {
    const generic = lintFingerprints([
        { name: 'A', category: 'CMS', match: { scripts: ['/api/'] }, example: { scripts: ['/api/x'] } },
        { name: 'B', category: 'CMS', match: { scripts: ['/static/'] }, example: { scripts: ['/static/x'] } },
        { name: 'C', category: 'CMS', match: { html: ['abc'] }, example: { html: 'abc' } },
        { name: 'E', category: 'CMS', match: { scripts: ['[a-z0-9]+'] }, example: { scripts: ['anything'] } },
        { name: 'F', category: 'CMS', match: { scripts: ['/api/.*'] }, example: { scripts: ['/api/anything'] } },
        { name: 'D', category: 'CMS', match: { scripts: ['static\\.hotjar\\.com'] }, example: { scripts: ['https://static.hotjar.com/x.js'] } },
    ]);
    assert.equal(generic.filter((p) => /too generic/.test(p)).length, 5);
    assert.ok(generic.some((p) => p.includes('E: pattern too generic')));
    assert.ok(generic.some((p) => p.includes('F: pattern too generic')));
    assert.ok(!generic.some((p) => p.startsWith('D:')));
});

test('lint catches bad data', () => {
    const problems = lintFingerprints([{ name: 'X', category: 'CMS', match: { html: ['('] }, example: { html: 'x' } }, { name: 'X', category: 'CMS', match: {} }]);
    assert.ok(problems.some((p) => /invalid regex/.test(p)));
    assert.ok(problems.some((p) => /duplicate name/.test(p)));
    assert.ok(problems.some((p) => /no match patterns/.test(p)));
});
