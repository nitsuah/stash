// Pure technology detection: no network, no Apify. Given what a page returned, find which technologies it uses from fingerprint data.
//
// A fingerprint (see fingerprints/*.json) looks like:
//   { "name": "WordPress", "category": "CMS", "match": { "html": ["regex"], "scripts": ["regex"], "links": ["regex"],
//     "headers": { "x-powered-by": "regex" }, "cookies": ["regex"], "meta": { "generator": "regex" } },
//     "implies": ["PHP"], "example": { ...input that must make this fingerprint match... } }
// Every regex is case-insensitive and tested with .test(), so write the smallest pattern that is still specific.

/** @typedef {{html?: string, scripts?: string[], links?: string[], headers?: Record<string,string>, cookies?: string[], meta?: Record<string,string>}} PageData */

const re = (pattern) => new RegExp(pattern, 'i');

/** Returns the evidence strings for one fingerprint against one page, empty when nothing matched. */
export function evidenceFor(fp, page) {
    const m = fp.match ?? {};
    const found = [];
    for (const p of m.html ?? []) if (re(p).test(page.html ?? '')) found.push(`html:${p}`);
    for (const p of m.scripts ?? []) if ((page.scripts ?? []).some((s) => re(p).test(s))) found.push(`script:${p}`);
    for (const p of m.links ?? []) if ((page.links ?? []).some((s) => re(p).test(s))) found.push(`link:${p}`);
    for (const [name, p] of Object.entries(m.headers ?? {})) {
        const value = (page.headers ?? {})[name.toLowerCase()];
        if (value !== undefined && re(p).test(String(value))) found.push(`header:${name}`);
    }
    for (const p of m.cookies ?? []) if ((page.cookies ?? []).some((c) => re(p).test(c))) found.push(`cookie:${p}`);
    for (const [name, p] of Object.entries(m.meta ?? {})) {
        const value = (page.meta ?? {})[name.toLowerCase()];
        if (value !== undefined && re(p).test(String(value))) found.push(`meta:${name}`);
    }
    return found;
}

/**
 * @param {PageData} page
 * @param {object[]} fingerprints
 * @returns {{name: string, category: string, website?: string, evidence: string[], implied?: boolean}[]}
 */
export function detect(page, fingerprints) {
    const hits = new Map();
    for (const fp of fingerprints) {
        const evidence = evidenceFor(fp, page);
        if (evidence.length) hits.set(fp.name, { name: fp.name, category: fp.category, website: fp.website, evidence });
    }
    // Implied technologies (WordPress implies PHP) are added once, marked as implied, unless seen directly.
    for (const fp of fingerprints) {
        if (!hits.has(fp.name)) continue;
        for (const impliedName of fp.implies ?? []) {
            const target = fingerprints.find((f) => f.name === impliedName);
            if (target && !hits.has(impliedName)) hits.set(impliedName, { name: target.name, category: target.category, website: target.website, evidence: [`implied by ${fp.name}`], implied: true });
        }
    }
    return [...hits.values()].sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name));
}

// html, script and link patterns need at least this many literal characters and must not be a common path.
const MIN_LITERAL = 5;
const GENERIC = new Set(['/api/', '/api', '/graphql', '/static/', '/build/', '/assets/', '/dist/', '/js/', '/css/', '/img/', '/images/', '/scripts/', '/vendor/', '/lib/', '/public/', '/media/', '/files/', '/cdn/', 'script', 'style', 'bundle', 'main.js', 'app.js', 'vendor.js']);

/** Checks fingerprint data for mistakes. Returns a list of problem strings, empty when the data is sound. */
export function lintFingerprints(fingerprints) {
    const problems = [];
    const names = new Set();
    for (const fp of fingerprints) {
        const id = fp?.name ?? '(no name)';
        if (!fp.name || typeof fp.name !== 'string') problems.push(`${id}: missing name`);
        if (names.has(fp.name)) problems.push(`${id}: duplicate name`);
        names.add(fp.name);
        if (!fp.category) problems.push(`${id}: missing category`);
        const m = fp.match ?? {};
        const patterns = [...(m.html ?? []), ...(m.scripts ?? []), ...(m.links ?? []), ...(m.cookies ?? []), ...Object.values(m.headers ?? {}), ...Object.values(m.meta ?? {})];
        if (!patterns.length) problems.push(`${id}: has no match patterns`);
        let valid = true;
        for (const p of patterns) {
            try { re(p); } catch { valid = false; problems.push(`${id}: invalid regex ${p}`); }
        }
        // Content patterns must be specific: a short or common path matches thousands of sites that do not use the technology.
        for (const p of [...(m.html ?? []), ...(m.scripts ?? []), ...(m.links ?? [])]) {
            const plain = p.replace(/\\(.)/g, '$1').trim().toLowerCase();
            const literal = plain.replace(/[\^$.*+?()[\]{}|]/g, '');
            if (literal.length < MIN_LITERAL || GENERIC.has(plain)) problems.push(`${id}: pattern too generic ${p}`);
        }
        if (!fp.example) problems.push(`${id}: missing example`);
        else if (valid && patterns.length && !detect(fp.example, [fp]).some((h) => h.name === fp.name)) problems.push(`${id}: its own example does not match`);
    }
    for (const fp of fingerprints) for (const i of fp.implies ?? []) if (!names.has(i)) problems.push(`${fp.name}: implies unknown technology ${i}`);
    return problems;
}
