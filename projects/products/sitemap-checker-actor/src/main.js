// Sitemap URL checker: finds a site's sitemaps (robots.txt or /sitemap.xml), lists every URL in them and tests each one.
import zlib from 'node:zlib';
import { Actor, log } from 'apify';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);
const UA = 'Mozilla/5.0 (compatible; SitemapUrlChecker/1.0; +https://apify.com)';
const MAX_SITEMAP_BYTES = 10 * 1024 * 1024;
const MAX_SITEMAP_EXPANDED_BYTES = 20 * 1024 * 1024;
const MAX_SITEMAPS_PER_SITE = 100;

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const sites = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')).map((u) => new URL(u).origin))].slice(0, 20);
const maxUrls = clamp(input.maxUrlsPerSite ?? 200, 1, 5000);
const timeoutMs = clamp(input.timeoutSecs ?? 15, 3, 60) * 1000;
if (!sites.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

async function readLimitedBody(response, limit) {
    if (!response.body) return Buffer.alloc(0);
    const reader = response.body.getReader();
    const chunks = [];
    let total = 0;
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        total += value.byteLength;
        if (total > limit) { await reader.cancel().catch(() => {}); throw new Error('Response exceeds ' + limit + ' byte limit'); }
        chunks.push(Buffer.from(value));
    }
    return Buffer.concat(chunks, total);
}

async function get(url) {
    let res;
    try {
        res = await fetch(url, { redirect: 'follow', headers: { 'user-agent': UA }, signal: AbortSignal.timeout(timeoutMs) });
        let buf = await readLimitedBody(res, MAX_SITEMAP_BYTES);
        if (buf[0] === 0x1f && buf[1] === 0x8b) {
            try { buf = zlib.gunzipSync(buf, { maxOutputLength: MAX_SITEMAP_EXPANDED_BYTES }); }
            catch (err) { if (/maxOutputLength|larger than|buffer/i.test(err.message)) throw new Error('Decompressed sitemap exceeds size limit'); throw err; }
        }
        return { status: res.status, text: buf.toString('utf8') };
    } catch (err) { return { status: res?.status ?? null, text: '', error: err.cause?.code ?? err.message }; }
}

const locs = (xml) => [...xml.matchAll(/<loc>\s*([^<\s][^<]*?)\s*<\/loc>/gi)].map((m) => m[1].replace(/&amp;/g, '&'));

function isValidLastmod(value) {
    const match = /^(\\d{4})-(\\d{2})-(\\d{2})(?:T(\\d{2}):(\\d{2})(?::(\\d{2})(?:\\.(\\d+))?)?(Z|[+-]\\d{2}:\\d{2})?)?$/.exec(value);
    if (!match) return false;
    const [, y, mo, d, hh, mm, ss, , zone] = match;
    const year = Number(y), month = Number(mo), day = Number(d);
    if (month < 1 || month > 12) return false;
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (day < 1 || day > days[month - 1]) return false;
    if (hh !== undefined && (Number(hh) > 23 || Number(mm) > 59 || Number(ss ?? 0) > 59)) return false;
    if (zone && zone !== 'Z') { const zh = Number(zone.slice(1, 3)), zm = Number(zone.slice(4, 6)); if (zh > 14 || zm > 59 || (zh === 14 && zm !== 0)) return false; }
    return true;
}

// Walk sitemap indexes up to three levels deep, with independent fetch and entry budgets.
async function collect(sitemapUrl, depth, seen, out, notes) {
    if (seen.has(sitemapUrl)) return;
    if (depth > 3) { notes.push({ sitemap: sitemapUrl, problem: 'Maximum sitemap nesting depth reached' }); return; }
    const maxEntries = Math.min(maxUrls * 2, 10000);
    if (seen.size >= MAX_SITEMAPS_PER_SITE) { notes.push({ sitemap: sitemapUrl, problem: 'Sitemap fetch budget reached (' + MAX_SITEMAPS_PER_SITE + ')' }); return; }
    if (out.length >= maxEntries) { notes.push({ sitemap: sitemapUrl, problem: 'Sitemap entry budget reached (' + maxEntries + ')' }); return; }
    seen.add(sitemapUrl);
    const r = await get(sitemapUrl);
    if (r.status !== 200) { notes.push({ sitemap: sitemapUrl, problem: r.error ? 'Could not fetch (' + r.error + ')' : 'Returned HTTP ' + r.status }); return; }
    if (/<sitemapindex/i.test(r.text)) {
        for (const child of locs(r.text)) {
            if (seen.size >= MAX_SITEMAPS_PER_SITE || out.length >= maxEntries) { notes.push({ sitemap: sitemapUrl, problem: 'Stopped sitemap traversal at the configured resource budget' }); break; }
            await collect(child, depth + 1, seen, out, notes);
        }
    } else if (/<urlset/i.test(r.text)) {
        for (const block of r.text.split(/<url>/i).slice(1)) {
            if (out.length >= maxEntries) { notes.push({ sitemap: sitemapUrl, problem: 'Stopped collecting entries at the configured limit of ' + maxEntries }); break; }
            const [loc] = locs(block);
            if (loc) out.push({ url: loc, sitemap: sitemapUrl, lastmod: (block.match(/<lastmod>\\s*([^<]+?)\\s*<\\/lastmod>/i) ?? [])[1] ?? null });
        }
    } else notes.push({ sitemap: sitemapUrl, problem: 'Not a valid sitemap (no urlset or sitemapindex element)' });
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

    // Validate every listed entry before de-duplication, so duplicates cannot hide bad lastmod values.
    const problems = [];
    const validEntries = [];
    for (const e of entries) {
        if (e.lastmod && !isValidLastmod(e.lastmod)) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'bad-lastmod', detail: 'lastmod "' + e.lastmod + '" is not a valid ISO calendar date/time' });
        try { const u = new URL(e.url); if (!/^https?:$/.test(u.protocol)) throw new Error('unsupported protocol'); validEntries.push({ ...e, parsedUrl: u }); }
        catch { problems.push({ url: e.url, sitemap: e.sitemap, issue: 'invalid-url', detail: 'Sitemap entry is not a valid absolute http(s) URL' }); }
    }
    const counts = new Map();
    for (const e of validEntries) counts.set(e.url, (counts.get(e.url) ?? 0) + 1);
    const unique = [...new Map(validEntries.map((e) => [e.url, e])).values()].slice(0, maxUrls);
    for (const [url, n] of counts) if (n > 1) problems.push({ url, issue: 'duplicate', detail: 'Listed ' + n + ' times in the sitemaps' });
    const originHost = new URL(origin).hostname;
    for (const e of unique) if (e.parsedUrl.hostname !== originHost) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'wrong-host', detail: 'URL is on ' + e.parsedUrl.hostname + ', not ' + originHost });

    let next = 0;
    let checkedThisSite = 0;
    let stopForChargeLimit = false;
    let chargeFailure = null;
    async function worker() {
        while (next < unique.length && !stopForChargeLimit) {
            const e = unique[next++];
            let charge;
            try { charge = await Actor.charge({ eventName: 'sitemap-url-checked' }); }
            catch (err) { chargeFailure = err; stopForChargeLimit = true; return; }
            if (typeof charge?.chargedCount === 'number' && charge.chargedCount < 1) { stopForChargeLimit = true; return; }
            if (charge?.eventChargeLimitReached) stopForChargeLimit = true;
            const r = await probe(e.url);
            totalChecked += 1;
            checkedThisSite += 1;
            if (r.error) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'unreachable', status: null, detail: 'Request failed (' + r.error + ')' });
            else if (r.status >= 400) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'error-status', status: r.status, detail: 'Returns HTTP ' + r.status });
            else if (r.status >= 300) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'redirect', status: r.status, redirectsTo: r.location, detail: 'Redirects (' + r.status + ') to ' + r.location });
            else if (r.noindex) problems.push({ url: e.url, sitemap: e.sitemap, issue: 'noindex', status: r.status, detail: 'X-Robots-Tag says noindex but the URL is in the sitemap' });
        }
    }
    await Promise.all(Array.from({ length: 10 }, worker));
    if (stopForChargeLimit && !chargeFailure) notes.push({ sitemap: null, problem: 'Actor event charge limit reached; scan results are partial' });
    if (chargeFailure) notes.push({ sitemap: null, problem: 'Actor charge failed: ' + chargeFailure.message });

    await Actor.pushData({
        type: 'site', site: origin, robotsTxt: robots.status === 200, sitemapsInRobots: declared.length, sitemapsChecked: [...seen],
        urlsInSitemaps: entries.length, uniqueUrls: counts.size, urlsChecked: checkedThisSite, problemCount: problems.length + notes.length, sitemapProblems: notes,
        message: chargeFailure ? 'Charge failed; results are incomplete' : stopForChargeLimit ? 'Charge limit reached; checked ' + checkedThisSite + ' URLs, results are partial' : (!seen.size || (entries.length === 0 && notes.length) ? 'No usable sitemap found' : (problems.length || notes.length) ? (problems.length + notes.length) + ' problem(s) found in ' + checkedThisSite + ' URLs' : 'All ' + checkedThisSite + ' sitemap URLs look healthy'),
    });
    for (const p of problems) await Actor.pushData({ type: 'url', site: origin, ...p });
    if (chargeFailure) await Actor.fail('Could not charge for sitemap URL checks: ' + chargeFailure.message);
}

await Actor.setValue('SUMMARY', { sites: sites.length, urlsChecked: totalChecked, finishedAt: new Date().toISOString() });
await Actor.exit();
