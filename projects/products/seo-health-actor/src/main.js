// SEO health Actor: crawls a site and flags missing or weak titles, descriptions, headings, canonicals, noindex tags and sitemap/robots problems.
import { Actor } from 'apify';
import { CheerioCrawler } from 'crawlee';
import { readTextCapped } from './body.js';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);
const TITLE = { min: 15, max: 60 };
const DESC = { min: 70, max: 160 };
const MAX_CHECK_BYTES = 2 * 1024 * 1024; // robots.txt / sitemap.xml are read at most this far (decoded bytes)

await Actor.init();

const input = (await Actor.getInput()) ?? {};
const startUrls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')))].slice(0, 20);
const maxPages = clamp(input.maxPages ?? 50, 1, 1000);
if (!startUrls.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

const pages = [];
const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: maxPages,
    maxConcurrency: 10,
    maxRequestRetries: 1,
    ignoreHttpErrorStatusCodes: [400, 401, 402, 403, 404, 405, 410, 429],
    async requestHandler({ request, $, enqueueLinks, response }) {
        const url = request.loadedUrl ?? request.url;
        const status = response?.statusCode ?? 200;
        if (status >= 400) {
            pages.push({ url, status, issues: [{ rule: 'http-error', severity: 'high', detail: `Page returns HTTP ${status}` }] });
            return;
        }
        const title = $('head > title').first().text().trim();
        const description = ($('meta[name="description"]').attr('content') ?? '').trim();
        const robots = ($('meta[name="robots"]').attr('content') ?? '').toLowerCase();
        const canonical = ($('link[rel="canonical"]').attr('href') ?? '').trim();
        const h1s = $('h1').length;
        const imagesTotal = $('img').length;
        const imagesNoAlt = $('img').filter((_, i) => $(i).attr('alt') === undefined).length;
        const issues = [];
        const add = (rule, severity, detail) => issues.push({ rule, severity, detail });

        if (!title) add('title-missing', 'high', 'No <title> tag');
        else if (title.length < TITLE.min) add('title-short', 'low', `Title is ${title.length} characters (aim for ${TITLE.min}-${TITLE.max})`);
        else if (title.length > TITLE.max) add('title-long', 'low', `Title is ${title.length} characters (aim for ${TITLE.min}-${TITLE.max})`);
        if (!description) add('description-missing', 'medium', 'No meta description');
        else if (description.length < DESC.min || description.length > DESC.max) add('description-length', 'low', `Description is ${description.length} characters (aim for ${DESC.min}-${DESC.max})`);
        if (h1s === 0) add('h1-missing', 'medium', 'No <h1> heading');
        else if (h1s > 1) add('h1-multiple', 'low', `${h1s} <h1> headings`);
        if (/noindex/.test(robots)) add('noindex', 'high', 'Page has a noindex robots meta tag');
        if (!canonical) add('canonical-missing', 'low', 'No canonical link');
        if (!($('html').attr('lang') ?? '').trim()) add('lang-missing', 'low', 'No lang attribute on <html>');
        if (imagesNoAlt) add('img-alt-missing', 'medium', `${imagesNoAlt} of ${imagesTotal} images have no alt attribute`);
        if (!$('meta[property="og:title"]').length) add('og-missing', 'low', 'No Open Graph title for link previews');

        pages.push({ url, status, title, description, canonical, issues });
        await enqueueLinks({ strategy: 'same-hostname' });
    },
    failedRequestHandler: async ({ request }) => {
        pages.push({ url: request.url, status: null, issues: [{ rule: 'unreachable', severity: 'high', detail: 'Page could not be fetched' }] });
    },
});
await crawler.run(startUrls);

// Duplicates need the whole crawl, so they are found afterwards.
const markDuplicates = (field, rule, label) => {
    const groups = new Map();
    for (const p of pages) if (p[field]) groups.set(p[field], [...(groups.get(p[field]) ?? []), p]);
    for (const group of groups.values()) if (group.length > 1) for (const p of group) p.issues.push({ rule, severity: 'medium', detail: `${label} is shared with ${group.length - 1} other page(s)` });
};
markDuplicates('title', 'title-duplicate', 'Title');
markDuplicates('description', 'description-duplicate', 'Description');

// Site-level checks: robots.txt and sitemap.xml for each origin.
const siteChecks = [];
for (const origin of new Set(startUrls.map((u) => new URL(u).origin))) {
    const get = async (path) => {
        try {
            const r = await fetch(origin + path, { signal: AbortSignal.timeout(15000) });
            if (!r.ok) { await r.body?.cancel().catch(() => {}); return { status: r.status, text: '' }; }
            return { status: r.status, text: await readTextCapped(r, MAX_CHECK_BYTES) };
        } catch { return { status: null, text: '' }; }
    };
    const robots = await get('/robots.txt');
    const sitemap = await get('/sitemap.xml');
    siteChecks.push({
        origin,
        robotsTxt: robots.status === 200,
        robotsBlocksAll: /^\s*Disallow:\s*\/\s*$/im.test(robots.text) && /^\s*User-agent:\s*\*/im.test(robots.text),
        robotsMentionsSitemap: /^\s*Sitemap:/im.test(robots.text),
        sitemapXml: sitemap.status === 200,
        sitemapUrlCount: (sitemap.text.match(/<loc>/g) ?? []).length,
    });
}

const WEIGHT = { high: 10, medium: 4, low: 1 };
for (const p of pages) {
    const penalty = p.issues.reduce((s, i) => s + WEIGHT[i.severity], 0);
    const broken = p.status === null || p.status >= 400; // a page that cannot be fetched has no SEO value at all
    await Actor.pushData({ url: p.url, status: p.status, score: broken ? 0 : Math.max(0, 100 - penalty), issueCount: p.issues.length, title: p.title ?? null, issues: p.issues });
}
await Actor.setValue('SUMMARY', {
    pagesCrawled: pages.length,
    pagesWithHighIssues: pages.filter((p) => p.issues.some((i) => i.severity === 'high')).length,
    totalIssues: pages.reduce((s, p) => s + p.issues.length, 0),
    site: siteChecks,
    finishedAt: new Date().toISOString(),
});
if (pages.length) await Actor.charge({ eventName: 'page-checked', count: pages.length }).catch(() => {});
await Actor.exit();
