// Structured data validator: crawls a site, parses every JSON-LD block and checks common schema.org types for missing properties.
import { Actor, log } from 'apify';
import { CheerioCrawler } from 'crawlee';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);

// Required properties make the entity unusable for rich results; recommended ones improve them. Kept deliberately small and documented in the README.
const RUBRIC = {
    Product: { required: ['name'], recommended: ['image', 'description', 'sku', 'brand', 'aggregateRating', 'offers'] },
    Offer: { required: ['priceCurrency'], recommended: ['availability', 'url'] },
    Article: { required: [], recommended: ['headline', 'image', 'datePublished', 'author', 'dateModified', 'publisher'] },
    LocalBusiness: { required: ['name', 'address'], recommended: ['telephone', 'openingHours', 'openingHoursSpecification', 'image', 'url', 'geo'] },
    Organization: { required: ['name', 'url'], recommended: ['logo', 'sameAs', 'contactPoint'] },
    FAQPage: { required: ['mainEntity'], recommended: [] },
    Question: { required: ['name', 'acceptedAnswer'], recommended: [] },
    BreadcrumbList: { required: ['itemListElement'], recommended: [] },
    ListItem: { required: ['position', 'name'], recommended: ['item'] },
    Event: { required: ['name', 'startDate', 'location'], recommended: ['endDate', 'image', 'offers', 'description'] },
    Recipe: { required: ['name', 'image', 'recipeIngredient'], recommended: ['recipeInstructions', 'author', 'aggregateRating', 'cookTime'] },
    WebSite: { required: ['name', 'url'], recommended: ['potentialAction'] },
    Person: { required: ['name'], recommended: ['url', 'sameAs'] },
    JobPosting: { required: ['title', 'description', 'datePosted', 'hiringOrganization', 'jobLocation'], recommended: ['validThrough', 'baseSalary', 'employmentType'] },
};
const ALIASES = {
    NewsArticle: 'Article', BlogPosting: 'Article', TechArticle: 'Article', Restaurant: 'LocalBusiness', Store: 'LocalBusiness', Dentist: 'LocalBusiness',
    ProfessionalService: 'LocalBusiness', HomeAndConstructionBusiness: 'LocalBusiness', AutoRepair: 'LocalBusiness', MedicalBusiness: 'LocalBusiness',
    CafeOrCoffeeShop: 'LocalBusiness', LegalService: 'LocalBusiness', RealEstateAgent: 'LocalBusiness', Corporation: 'Organization', NGO: 'Organization',
};
const SEVERITY = { required: 'high', recommended: 'low' };
function normalizeType(rawType) {
    const raw = String(rawType);
    let local = raw;
    try {
        const parsed = new URL(raw);
        if (parsed.hostname.toLowerCase() === 'schema.org') local = parsed.pathname.split('/').filter(Boolean).at(-1) ?? raw;
    } catch {
        local = raw.replace(/^schema\.org\//i, '');
    }
    return ALIASES[local] ?? local;
}
const WEIGHT = { high: 12, medium: 8, low: 2 };

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const startUrls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')))].slice(0, 20);
const maxPages = clamp(input.maxPages ?? 30, 1, 500);
if (!startUrls.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

const present = (v) => v !== undefined && v !== null && !(typeof v === 'string' && !v.trim()) && !(Array.isArray(v) && !v.length);
const asArray = (v) => (Array.isArray(v) ? v : v === undefined || v === null ? [] : [v]);

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

function validate(entity) {
    const issues = [];
    for (const rawType of asArray(entity['@type'])) {
        const type = normalizeType(rawType);
        const rule = RUBRIC[type];
        if (!rule) continue;
        for (const level of ['required', 'recommended']) {
            for (const prop of rule[level]) {
                if (!present(entity[prop])) issues.push({ type: rawType, rule: `${level}-missing`, property: prop, severity: SEVERITY[level], detail: `${rawType} is missing ${level === 'required' ? 'required' : 'recommended'} property "${prop}"` });
            }
        }
        if (type === 'Product' && !['offers', 'aggregateRating', 'review'].some((key) => present(entity[key]))) {
            issues.push({ type: rawType, rule: 'required-missing', property: 'offers|aggregateRating|review', severity: 'high', detail: 'Product must provide offers, aggregateRating, or review for a product snippet' });
        }
        if (type === 'Offer') {
            const hasPrice = present(entity.price) || asArray(entity.priceSpecification).some((spec) => spec && typeof spec === 'object' && present(spec.price));
            if (!hasPrice) issues.push({ type: rawType, rule: 'required-missing', property: 'price|priceSpecification.price', severity: 'high', detail: 'Offer must provide price or priceSpecification.price' });
        }
    }
    return issues;
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
