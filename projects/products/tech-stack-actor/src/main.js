// Website technology detector Actor: fetches each URL once and reports the CMS, frameworks, analytics, servers and CDNs it can fingerprint.
import { Actor, log } from 'apify';
import * as cheerio from 'cheerio';
import { detect } from './detect.js';
import { loadFingerprints } from './load.js';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);
const UA = 'Mozilla/5.0 (compatible; TechStackDetector/1.0; +https://apify.com)';
const MAX_HTML_BYTES = 2_000_000;

async function readLimited(res, limit) {
    const reader = res.body.getReader();
    const chunks = [];
    let total = 0;
    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            total += value.length;
            if (total > limit) {
                reader.releaseLock();
                throw new Error(`Response body exceeds ${limit} byte limit`);
            }
            chunks.push(value);
        }
    } finally {
        reader.releaseLock();
    }
    return new TextDecoder().decode(Buffer.concat(chunks));
}

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const urls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')))].slice(0, 200);
const timeoutMs = clamp(input.timeoutSecs ?? 20, 3, 60) * 1000;
if (!urls.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');
const fingerprints = loadFingerprints();

async function inspect(url) {
    const row = { url, finalUrl: null, status: null, technologies: [], technologyCount: 0, checkedAt: new Date().toISOString() };
    try {
        const res = await fetch(url, { redirect: 'follow', headers: { 'user-agent': UA, accept: 'text/html,*/*' }, signal: AbortSignal.timeout(timeoutMs) });
        row.status = res.status;
        row.finalUrl = res.url;
        const html = await readLimited(res, MAX_HTML_BYTES);
        const $ = cheerio.load(html);
        const headers = Object.fromEntries([...res.headers.entries()]);
        const cookies = typeof res.headers.getSetCookie === 'function' ? res.headers.getSetCookie().map((c) => c.split(';')[0]) : [];
        const meta = {};
        $('meta[name]').each((_, el) => { meta[($(el).attr('name') ?? '').toLowerCase()] = $(el).attr('content') ?? ''; });
        const page = {
            html,
            headers,
            cookies,
            meta,
            scripts: $('script[src]').map((_, el) => $(el).attr('src')).get(),
            links: $('link[href]').map((_, el) => $(el).attr('href')).get(),
        };
        row.technologies = detect(page, fingerprints);
        row.technologyCount = row.technologies.length;
    } catch (err) {
        row.error = err.cause?.code ?? err.message;
    }
    return row;
}

let next = 0;
let ok = 0;
async function worker() {
    while (next < urls.length) {
        const row = await inspect(urls[next++]);
        await Actor.pushData(row);
        if (!row.error) {
            ok += 1;
            try { await Actor.charge({ eventName: 'site-analyzed' }); } catch (e) { log.warning(`Charge failed for ${row.url}: ${e.message}`); }
        }
    }
}
await Promise.all(Array.from({ length: 5 }, worker));
await Actor.setValue('SUMMARY', { urls: urls.length, analyzed: ok, fingerprints: fingerprints.length, finishedAt: new Date().toISOString() });
await Actor.exit();
