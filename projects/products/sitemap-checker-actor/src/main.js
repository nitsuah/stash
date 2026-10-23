// Sitemap URL checker: finds a site's sitemaps (robots.txt or /sitemap.xml), lists every URL in them and tests each one.
import zlib from 'node:zlib';
import { Actor, log } from 'apify';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);
const UA = 'Mozilla/5.0 (compatible; SitemapUrlChecker/1.0; +https://apify.com)';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const sites = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')).map((u) => new URL(u).origin))].slice(0, 20);
const maxUrls = clamp(input.maxUrlsPerSite ?? 200, 1, 5000);
const timeoutMs = clamp(input.timeoutSecs ?? 15, 3, 60) * 1000;
if (!sites.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

async function get(url) {
    try {
        const res = await fetch(url, { redirect: 'follow', headers: { 'user-agent': UA }, signal: AbortSignal.timeout(timeoutMs) });
        let buf = Buffer.from(await res.arrayBuffer());
        if (buf[0] === 0x1f && buf[1] === 0x8b) buf = zlib.gunzipSync(buf); // .xml.gz sitemaps
        return { status: res.status, text: buf.toString('utf8') };
    } catch (err) {
        return { status: null, text: '', error: err.cause?.code ?? err.message };
    }
}

const locs = (xml) => [...xml.matchAll(/<loc>\s*([^<\s][^<]*?)\s*<\/loc>/gi)].map((m) => m[1].replace(/&amp;/g, '&'));

// Walks sitemap indexes up to three levels deep.
async function collect(sitemapUrl, depth, seen, out, notes) {
    if (seen.has(sitemapUrl) || depth > 3 || out.length >= maxUrls * 2) return;
    seen.add(sitemapUrl);
    const r = await get(sitemapUrl);
    if (r.status !== 200) { notes.push({ sitemap: sitemapUrl, problem: r.error ? `Could not fetch (${r.error})` : `Returned HTTP ${r.status}` }); return; }
    if (/<sitemapindex/i.test(r.text)) {
        for (const child of locs(r.text)) await collect(child, depth + 1, seen, out, notes);
    } else if (/<urlset/i.test(r.text)) {
        for (const block of r.text.split(/<url>/i).slice(1)) {
            const [loc] = locs(block);
            if (loc) out.push({ url: loc, sitemap: sitemapUrl, lastmod: (block.match(/<lastmod>\s*([^<]+?)\s*<\/lastmod>/i) ?? [])[1] ?? null });
        }
    } else {
        notes.push({ sitemap: sitemapUrl, problem: 'Not a valid sitemap (no urlset or sitemapindex element)' });
    }
}

async function probe(url) {
    const opts = (method) => ({ method, redirect: 'manual', headers: { 'user-agent': UA }, signal: AbortSignal.timeout(timeoutMs) });
    try {
        let res = await fetch(url, opts('HEAD'));
        if ([403, 405, 429, 501].includes(res.status) || res.status >= 500) res = await fetch(url, opts('GET'));
        return { status: res.status, location: res.headers.get('location'), noindex: /noindex/i.test(res.headers.get('x-robots-tag') ?? '') };
    } catch (err) {
        return { status: null, error: err.cause?.code ?? err.name };
    }
}

let totalChecked = 0;
for (const origin of sites) {
    const robots = await get(`${origin}/robots.txt`);
    const declared = robots.status === 200 ? [...robots.text.matchAll(/^\s*Sitemap:\s*(\S+)/gim)].map((m) => m[1]) : [];
    const sitemapUrls = declared.length ? declared : [`${origin}/sitemap.xml`];
    const notes = [];
    const entries = [];
    const seen = new Set();
    for (const s of sitemapUrls) await collect(s, 0, seen, entries, notes);

    // De-duplicate and flag duplicates before spending requests.
    const counts = new Map();
    for (const e of entries) counts.set(e.url, (counts.get(e.url) ?? 0) + 1);
    const unique = [...new Map(entries.map((e) => [e.url, e])).values()].slice(0, maxUrls);
    const problems = [];
    for (const [url, n] of counts) if (n > 1) problems.push({ url, issue: 'duplicate', detail: `Listed ${n} times in the sitemaps` });
    for (const e of unique) {
        const u = new URL(e.url);
        if (u.origin !== origin) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'wrong-host', detail: `URL is on ${u.origin}, not ${origin}` });
        if (e.lastmod && Number.isNaN(Date.parse(e.lastmod))) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'bad-lastmod', detail: `lastmod "${e.lastmod}" is not a valid date` });
    }

    let next = 0;
    async function worker() {
        while (next < unique.length) {
            const e = unique[next++];
            const r = await probe(e.url);
            totalChecked += 1;
            if (r.error) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'unreachable', status: null, detail: `Request failed (${r.error})` });
            else if (r.status >= 400) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'error-status', status: r.status, detail: `Returns HTTP ${r.status}` });
            else if (r.status >= 300) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'redirect', status: r.status, redirectsTo: r.location, detail: `Redirects (${r.status}) to ${r.location}` });
            else if (r.noindex) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'noindex', status: r.status, detail: 'X-Robots-Tag says noindex but the URL is in the sitemap' });
        }
    }
    await Promise.all(Array.from({ length: 10 }, worker));

    await Actor.pushData({
        type: 'site', site: origin, robotsTxt: robots.status === 200, sitemapsInRobots: declared.length, sitemapsChecked: [...seen],
        urlsInSitemaps: entries.length, uniqueUrls: counts.size, urlsChecked: unique.length, problemCount: problems.length + notes.length,
        sitemapProblems: notes,
        message: !seen.size || (entries.length === 0 && notes.length) ? 'No usable sitemap found' : problems.length ? `${problems.length} problem(s) found in ${unique.length} URLs` : `All ${unique.length} sitemap URLs look healthy`,
    });
    for (const p of problems) await Actor.pushData({ type: 'url', site: origin, ...p });
}

if (totalChecked > 0) {
    try { await Actor.charge({ eventName: 'sitemap-url-checked', count: totalChecked }); } catch (e) { log.warning(`Charge failed: ${e.message}`); }
}
await Actor.setValue('SUMMARY', { sites: sites.length, urlsChecked: totalChecked, finishedAt: new Date().toISOString() });
await Actor.exit();
