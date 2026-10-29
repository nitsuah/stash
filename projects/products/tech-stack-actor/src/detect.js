// Pure technology detection: no network, no Apify. Given what a page returned, find which technologies it uses from fingerprint data.
//
// A fingerprint (see fingerprints/*.json) looks like:
//   { "name": "WordPress", "category": "CMS", "match": { "html": ["regex"], "scripts": ["regex"], "links": ["regex"],
//     "headers": { "x-powered-by": "regex" }, "cookies": ["regex"], "meta": { "generator": "regex" } },
//     "implies": ["PHP"], "example": { ...input that must make this fingerprint match... } }
// Every regex is case-insensitive and tested with .test(), so write the smallest pattern that is still specific.

/** @typedef {{html?: string, scripts?: string[], links?: string[], headers?: Record<string,string>, cookies?: string[], meta?: Record<string,string>}} PageData */

const compiled = new Map();
const re = (pattern) => {
    let r = compiled.get(pattern);
    if (!r) { r = new RegExp(pattern, 'i'); compiled.set(pattern, r); }
    return r;
};

// Page HTML is truncated before matching (boundPage below clips the other values).
export const MAX_HTML_CHARS = 1_000_000;
const capHtml = (s) => (s.length > MAX_HTML_CHARS ? s.slice(0, MAX_HTML_CHARS) : s);

// Remote values are untrusted: clip each string and cap the counts so a fingerprint regex cannot be driven into quadratic scans.
export const MAX_VALUE_LENGTH = 1024;
export const MAX_VALUES = 500;
const clip = (s) => String(s).slice(0, MAX_VALUE_LENGTH);
export function boundPage(page) {
    const list = (a) => (a ?? []).slice(0, MAX_VALUES).map(clip);
    const dict = (o) => Object.fromEntries(Object.entries(o ?? {}).slice(0, MAX_VALUES).map(([k, v]) => [k, clip(v)]));
    return { ...page, scripts: list(page.scripts), links: list(page.links), cookies: list(page.cookies), headers: dict(page.headers), meta: dict(page.meta) };
}

/** Returns the evidence strings for one fingerprint against one page, empty when nothing matched. */
export function evidenceFor(fp, page) {
    const m = fp.match ?? {};
    const found = [];
    for (const p of m.html ?? []) if (re(p).test(capHtml(page.html ?? ''))) found.push(`html:${p}`);
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
    const safe = boundPage(page);
    const hits = new Map();
    for (const fp of fingerprints) {
        const evidence = evidenceFor(fp, safe);
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
            if (typeof p !== 'string') {
                valid = false;
                problems.push(`${id}: pattern must be a string ${p}`);
                continue;
            }
            try { re(p); } catch { valid = false; problems.push(`${id}: invalid regex ${p}`); continue; }
            // A quantified group that itself ends in a quantifier, e.g. (a+)+ or (.*)*, can backtrack exponentially.
            if (/\([^()]*[+*][^()]*\)[+*{]/.test(p)) problems.push(`${id}: nested quantifier can backtrack catastrophically: ${p}`);
        }
        // Content patterns must be specific: a short or common path matches thousands of sites that do not use the technology.
        for (const p of [...(m.html ?? []), ...(m.scripts ?? []), ...(m.links ?? [])]) {
            if (typeof p !== 'string') {
                continue; // already reported by the validity loop above
            }
            const plain = p.trim().toLowerCase();
            // Count matched literals, not regex metadata, character-class contents, or operators.
            // Evaluate each alternation separately so a generic branch cannot hide behind a specific one.
            const alternatives = [{ literal: '', constrainedClassTokens: 0 }];
            const current = () => alternatives[alternatives.length - 1];
            let groupDepth = 0;
            for (let i = 0; i < plain.length; i += 1) {
                const ch = plain[i];
                if (ch === '(') {
                    if (plain[i + 1] === '?' && plain[i + 2] === '<') {
                        const marker = plain[i + 3];
                        // Skip lookbehind operators and named-group declarations; neither matches text.
                        groupDepth += 1;
                        if (marker === '=' || marker === '!') { i += 3; continue; }
                        const close = plain.indexOf('>', i + 3);
                        if (close !== -1) { i = close; continue; }
                    }
                    if (plain[i + 1] === '?' && [':', '=', '!', '>'].includes(plain[i + 2])) {
                        groupDepth += 1;
                        i += 2;
                        continue;
                    }
                    groupDepth += 1;
                    continue;
                }
                if (ch === ')') { if (groupDepth > 0) groupDepth -= 1; continue; }
                if (ch === '\\') {
                    const next = plain[i + 1];
                    if (next === undefined) continue;
                    if (next === 'u') {
                        if (plain[i + 2] === '{') {
                            const close = plain.indexOf('}', i + 3);
                            const hex = close === -1 ? '' : plain.slice(i + 3, close);
                            const codePoint = /^[0-9a-f]+$/i.test(hex) ? Number.parseInt(hex, 16) : NaN;
                            if (Number.isInteger(codePoint) && codePoint >= 0 && codePoint <= 0x10ffff) current().literal += String.fromCodePoint(codePoint);
                            i = close === -1 ? plain.length : close;
                            continue;
                        }
                        const hex = plain.slice(i + 2, i + 6);
                        if (/^[0-9a-f]{4}$/i.test(hex)) { current().literal += String.fromCharCode(Number.parseInt(hex, 16)); i += 5; continue; }
                    }
                    if (next === 'x') {
                        const hex = plain.slice(i + 2, i + 4);
                        if (/^[0-9a-f]{2}$/i.test(hex)) { current().literal += String.fromCharCode(Number.parseInt(hex, 16)); i += 3; continue; }
                    }
                    if (/^[dDsSwW]$/.test(next)) { current().constrainedClassTokens += 1; i += 1; continue; }
                    if (/^[pP]$/.test(next) && plain[i + 2] === '{') {
                        const close = plain.indexOf('}', i + 3);
                        if (close !== -1) { current().constrainedClassTokens += 1; i = close; continue; }
                    }
                    if (next === 'k' && plain[i + 2] === '<') {
                        const close = plain.indexOf('>', i + 3);
                        if (close !== -1) { i = close; continue; }
                    }
                    if (/^[bBAZzG]$/.test(next)) { i += 1; continue; }
                    current().literal += next;
                    i += 1;
                    continue;
                }
                if (ch === '[') {
                    i += 1;
                    while (i < plain.length) {
                        if (plain[i] === '\\') { i += 2; continue; }
                        if (plain[i] === ']') break;
                        i += 1;
                    }
                    continue;
                }
                if (ch === '|') { if (groupDepth === 0) alternatives.push({ literal: '', constrainedClassTokens: 0 }); continue; }
                // Quantifier bounds describe repetition, not matched literal text.
                // A leading or otherwise invalid { sequence remains a literal in non-u regexes.
                if (ch === '{' && i > 0 && !/[|(^$*+?{]/.test(plain[i - 1])) {
                    const quantifier = /^\{\d+(?:,\d*)?\}/.exec(plain.slice(i));
                    if (quantifier) { i += quantifier[0].length - 1; continue; }
                }
                if (!/^[.^$*+?(){}]$/.test(ch)) current().literal += ch;
            }
            const tooGeneric = alternatives.some(({ literal, constrainedClassTokens }) => {
                const specificity = [...literal].length + constrainedClassTokens;
                return specificity < MIN_LITERAL || GENERIC.has(literal);
            });
            if (tooGeneric || GENERIC.has(plain)) {
                problems.push(`${id}: pattern too generic ${p}`);
            }
        }
        if (!fp.example) problems.push(`${id}: missing example`);
        else if (valid && patterns.length && !detect(fp.example, [fp]).some((h) => h.name === fp.name)) problems.push(`${id}: its own example does not match`);
    }
    for (const fp of fingerprints) for (const i of fp.implies ?? []) if (!names.has(i)) problems.push(`${fp.name}: implies unknown technology ${i}`);
    return problems;
}
