// Run: node --test projects/products/tech-stack-actor/test   (Node 22, no dependencies)
import test from 'node:test';
import assert from 'node:assert/strict';
import { detect, lintFingerprints, MAX_HTML_CHARS, MAX_VALUE_CHARS } from '../src/detect.js';
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
        { name: 'G', category: 'CMS', match: { scripts: ['ab\\.cd'] }, example: { scripts: ['ab.cd'] } },
        { name: 'H', category: 'CMS', match: { scripts: ['(?<slug>[a-z0-9]+)'] }, example: { scripts: ['acme'] } },
        { name: 'I', category: 'CMS', match: { scripts: ['\\u0061'] }, example: { scripts: ['a'] } },
        { name: 'J', category: 'CMS', match: { scripts: ['/api/|specific-library'] }, example: { scripts: ['/api/'] } },
        { name: 'K', category: 'CMS', match: { scripts: ['/api/.{0,50}'] }, example: { scripts: ['/api/x'] } },
    ]);
    assert.equal(generic.filter((p) => /too generic/.test(p)).length, 9);
    assert.ok(generic.some((p) => p.includes('E: pattern too generic')));
    assert.ok(generic.some((p) => p.includes('F: pattern too generic')));
    assert.ok(!generic.some((p) => p.startsWith('D:')));
    assert.ok(!generic.some((p) => p.startsWith('G:')), 'escaped literal punctuation counts toward specificity');
    assert.ok(generic.some((p) => p.includes('H: pattern too generic')), 'named-group metadata is not counted as matched text');
    assert.ok(generic.some((p) => p.includes('I: pattern too generic')), 'Unicode escapes count as one decoded character');
    assert.ok(generic.some((p) => p.includes('J: pattern too generic')), 'every regex alternative must be sufficiently specific');
    assert.ok(generic.some((p) => p.includes('K: pattern too generic')), 'quantifier bounds do not count as literal specificity');
});

test('lint reports non-string content patterns without throwing or skipping later patterns', () => {
    const problems = lintFingerprints([{ name: 'X', category: 'CMS', match: { scripts: [42, 'specific-library-name'] }, example: { scripts: ['specific-library-name'] } }]);
    assert.equal(problems.filter((p) => p.includes('X: pattern must be a string 42')).length, 1);
    assert.ok(!problems.some((p) => p.includes('specific-library-name')));
});

test('lint catches bad data', () => {
    const problems = lintFingerprints([{ name: 'X', category: 'CMS', match: { html: ['('] }, example: { html: 'x' } }, { name: 'X', category: 'CMS', match: {} }]);
    assert.ok(problems.some((p) => /invalid regex/.test(p)));
    assert.ok(problems.some((p) => /duplicate name/.test(p)));
    assert.ok(problems.some((p) => /no match patterns/.test(p)));
});

test('lint rejects a nested-quantifier pattern but accepts the shipped data', () => {
    const bad = [{ name: 'X', category: 'CMS', match: { html: ['(abcde+)+fghij'] }, example: { html: 'abcdefghij' } }];
    assert.ok(lintFingerprints(bad).some((p) => p.includes('nested quantifier')));
    assert.deepEqual(lintFingerprints(all), []);
});

test('matching work is bounded: oversized html and values are truncated before matching', () => {
    const fp = [{ name: 'Tail', category: 'CMS', match: { html: ['needle-at-the-very-end'], scripts: ['needle-at-the-very-end'] } }];
    const big = 'a'.repeat(MAX_HTML_CHARS + 10) + 'needle-at-the-very-end';
    assert.deepEqual(detect({ html: big }, fp), []);
    assert.deepEqual(detect({ scripts: ['b'.repeat(MAX_VALUE_CHARS + 10) + 'needle-at-the-very-end'] }, fp), []);
    assert.equal(detect({ html: 'x needle-at-the-very-end' }, fp).length, 1);
});
