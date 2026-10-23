// Broken link checker Actor: crawls a site, collects every link, then reports the ones that fail (4xx, 5xx, timeouts, DNS errors).
import { Actor } from 'apify';
import { CheerioCrawler } from 'crawlee';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);
const MAX_LINKS = 3000;
const UA = 'Mozilla/5.0 (compatible; BrokenLinkChecker/1.0; +https://apify.com)';

await Actor.init();

const input = (await Actor.getInput()) ?? {};
const startUrls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')))].slice(0, 20);
const maxPages = clamp(input.maxPages ?? 50, 1, 1000);
const checkExternal = input.checkExternal !== false;
const timeoutSecs = clamp(input.timeoutSecs ?? 15, 3, 60);

if (!startUrls.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

const originOf = (u) => new URL(u).origin;
const internalOrigins = new Set(startUrls.map(originOf));
const sources = new Map(); // link -> Set of pages it was found on
let pagesCrawled = 0;

const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: maxPages,
    maxConcurrency: 10,
    maxRequestRetries: 1,
    ignoreHttpErrorStatusCodes: [400, 401, 402, 403, 404, 405, 410, 429],
    async requestHandler({ request, $, enqueueLinks, response }) {
        if ((response?.statusCode ?? 200) >= 400) return; // the checking phase reports it
        pagesCrawled += 1;
        const base = request.loadedUrl ?? request.url;
        $('a[href]').each((_, a) => {
            const href = ($(a).attr('href') ?? '').trim();
            if (!href || /^(mailto:|tel:|javascript:|sms:|data:)/i.test(href)) return;
            try {
                const u = new URL(href, base);
                if (!/^https?:$/.test(u.protocol)) return;
                u.hash = '';
                if (!sources.has(u.href)) sources.set(u.href, new Set());
                sources.get(u.href).add(base);
            } catch { /* malformed href: ignore */ }
        });
        await enqueueLinks({ strategy: 'same-hostname' });
    },
    failedRequestHandler: async () => {},
});
await crawler.run(startUrls);
for (const u of startUrls) if (!sources.has(u)) sources.set(u, new Set(['(start URL)']));

let links = [...sources.keys()].filter((l) => checkExternal || internalOrigins.has(originOf(l)));
const truncated = links.length > MAX_LINKS;
links = links.slice(0, MAX_LINKS);

async function probe(url) {
    const opts = (method) => ({ method, redirect: 'follow', headers: { 'user-agent': UA, accept: '*/*' }, signal: AbortSignal.timeout(timeoutSecs * 1000) });
    try {
        let res = await fetch(url, opts('HEAD'));
        if ([403, 405, 429, 501].includes(res.status) || res.status >= 500) res = await fetch(url, opts('GET'));
        return { status: res.status, error: null };
    } catch (headErr) {
        try {
            const res = await fetch(url, opts('GET'));
            return { status: res.status, error: null };
        } catch (err) {
            return { status: null, error: err.cause?.code ?? err.name ?? String(headErr) };
        }
    }
}

let broken = 0;
let next = 0;
async function worker() {
    while (next < links.length) {
        const link = links[next++];
        const { status, error } = await probe(link);
        if (error || status >= 400) {
            broken += 1;
            const found = [...sources.get(link)];
            await Actor.pushData({ brokenLink: link, status, error, internal: internalOrigins.has(originOf(link)), foundOnCount: found.length, foundOn: found.slice(0, 5) });
        }
    }
}
await Promise.all(Array.from({ length: 10 }, worker));

await Actor.setValue('SUMMARY', { pagesCrawled, linksChecked: links.length, brokenLinks: broken, truncatedAt: truncated ? MAX_LINKS : null, checkedExternal: checkExternal, finishedAt: new Date().toISOString() });
if (pagesCrawled > 0) await Actor.charge({ eventName: 'page-crawled', count: pagesCrawled });
await Actor.exit();
