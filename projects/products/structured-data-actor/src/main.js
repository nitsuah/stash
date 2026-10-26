// Structured data validator: crawls a site, parses every JSON-LD block and checks common schema.org types for missing properties.
import { Actor, log } from 'apify';
import { CheerioCrawler } from 'crawlee';
import { asArray, validate } from './validation.js';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);

const WEIGHT = { high: 12, medium: 8, low: 2 };

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const startUrls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')))].slice(0, 20);
const maxPages = clamp(input.maxPages ?? 30, 1, 500);
if (!startUrls.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

function entities(node, out = []) {
    for (const n of asArray(node)) {
        if (n && typeof n === 'object') {
            if (n['@graph']) entities(n['@graph'], out);
            if (n['@type']) out.push(n);
            // Nested entities that matter for validation (offers, questions, list items) are walked too.
            for (const key of ['offers', 'mainEntity', 'itemListElement', 'acceptedAnswer']) if (n[key] && typeof n[key] === 'object') entities(n[key], out);
        }
    }
    return out;
}



const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: maxPages,
    maxConcurrency: 10,
    maxRequestRetries: 1,
    ignoreHttpErrorStatusCodes: [...Array.from({ length: 100 }, (_, i) => 500 + i), 400, 401, 402, 403, 404, 405, 410, 429],
    async requestHandler({ request, $, enqueueLinks, response }) {
        const url = request.loadedUrl ?? request.url;
        const status = response?.statusCode ?? 200;
        if (status >= 400) {
            await Actor.pushData({ url, status, score: 0, types: [], blocks: 0, issues: [{ type: null, rule: 'http-error', property: null, severity: 'high', detail: `Page returns HTTP ${status}` }] });
            return;
        }
        const issues = [];
        const types = new Set();
        let blocks = 0;
        $('script[type="application/ld+json"]').each((_, el) => {
            blocks += 1;
            const raw = $(el).contents().text().trim();
            try {
                for (const e of entities(JSON.parse(raw))) {
                    asArray(e['@type']).forEach((t) => types.add(t));
                    issues.push(...validate(e));
                }
            } catch (err) {
                issues.push({ type: null, rule: 'invalid-json', property: null, severity: 'high', detail: `JSON-LD block ${blocks} is not valid JSON: ${err.message.slice(0, 80)}` });
            }
        });
        const microdata = $('[itemscope]').length;
        if (!blocks) issues.push({ type: null, rule: 'no-json-ld', property: null, severity: 'medium', detail: microdata ? `No JSON-LD (found ${microdata} microdata items; JSON-LD is the format Google recommends)` : 'No structured data found on this page' });
        const penalty = issues.reduce((s, i) => s + WEIGHT[i.severity], 0);
        await Actor.pushData({ url, status, score: Math.max(0, 100 - penalty), types: [...types], blocks, microdataItems: microdata, issues });
        try { await Actor.charge({ eventName: 'page-validated' }); } catch (e) { log.warning(`Charge failed for ${url}: ${e.message}`); }
        await enqueueLinks({ strategy: 'same-hostname' });
    },
    failedRequestHandler: async ({ request }) => {
        await Actor.pushData({ url: request.url, status: null, score: 0, types: [], blocks: 0, issues: [{ type: null, rule: 'unreachable', property: null, severity: 'high', detail: 'Page could not be fetched' }] });
    },
});
await crawler.run(startUrls);
await Actor.setValue('SUMMARY', { finishedAt: new Date().toISOString() });
await Actor.exit();
