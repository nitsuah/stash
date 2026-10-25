// Accessibility audit Actor: runs axe-core (WCAG 2.x A/AA by default) on each URL and returns a score plus violations.
import { Actor } from 'apify';
import { PlaywrightCrawler } from 'crawlee';
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const axeSource = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const axeVersion = require('axe-core/package.json').version;
const WEIGHT = { critical: 10, serious: 5, moderate: 2, minor: 1 };
const MAX_URLS = 200;

await Actor.init();

const input = (await Actor.getInput()) ?? {};
const tags = input.standards?.length ? input.standards : ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const maxNodes = Math.min(Math.max(input.maxNodesPerViolation ?? 3, 1), 20);
const urls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter(Boolean))]
    .filter((u) => /^https?:\/\//i.test(u))
    .slice(0, MAX_URLS);

if (!urls.length) {
    await Actor.fail('Provide at least one http(s) URL in startUrls.');
}

const crawler = new PlaywrightCrawler({
    maxRequestRetries: 1,
    requestHandlerTimeoutSecs: 90,
    navigationTimeoutSecs: 45,
    launchContext: { launchOptions: { args: ['--no-sandbox'] } },
    async requestHandler({ page, request }) {
        await page.waitForLoadState('load');
        const responseStatus = await page.evaluate(() => performance.getEntriesByType('navigation')[0]?.responseStatus ?? 0);
        if (responseStatus >= 400) {
            throw new Error(`Page returned HTTP ${responseStatus}; accessibility audit was not run.`);
        }
        // evaluate() runs through the debugger protocol, so a page's Content-Security-Policy cannot block axe.
        await page.evaluate(axeSource);
        const result = await page.evaluate((runTags) => window.axe.run(document, { runOnly: { type: 'tag', values: runTags } }), tags);
        const counts = { critical: 0, serious: 0, moderate: 0, minor: 0 };
        const violations = result.violations.map((v) => {
            counts[v.impact] = (counts[v.impact] ?? 0) + 1;
            return {
                rule: v.id,
                impact: v.impact,
                help: v.help,
                helpUrl: v.helpUrl,
                affectedElements: v.nodes.length,
                examples: v.nodes.slice(0, maxNodes).map((n) => ({ selector: n.target.join(' '), html: n.html.slice(0, 300) })),
            };
        });
        const penalty = Object.entries(counts).reduce((sum, [k, n]) => sum + (WEIGHT[k] ?? 0) * n, 0);
        await Actor.charge({ eventName: 'page-audited' });
        await Actor.pushData({
            url: request.loadedUrl ?? request.url,
            title: await page.title(),
            score: Math.max(0, 100 - penalty),
            violationCount: violations.length,
            byImpact: counts,
            passedRules: result.passes.length,
            violations,
            standards: tags,
            axeVersion,
            auditedAt: new Date().toISOString(),
        });
    },
    async failedRequestHandler({ request }) {
        await Actor.pushData({ url: request.url, error: (request.errorMessages?.slice(-1)[0] ?? 'Page failed to load').split('\n')[0], auditedAt: new Date().toISOString() });
    },
});

await crawler.run(urls);
await Actor.exit();
