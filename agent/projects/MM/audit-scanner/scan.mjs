// Zero-LLM accessibility scanner: playwright + axe-core -> JSON + templated markdown report.
// Usage: node scan.mjs <baseUrl> <path,path,...> <outName>
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const axeSrc = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const axeVersion = require('axe-core/package.json').version;
const [base, pathsArg = '/', out = 'report'] = process.argv.slice(2);
const paths = pathsArg.split(',');
const W = { critical: 10, serious: 5, moderate: 2, minor: 1 };

const browser = await chromium.launch();
const results = [];
for (const p of paths) {
  const page = await browser.newPage();
  const t0 = Date.now();
  let bytes = 0;
  const pending = [];
  page.on('response', r => pending.push(r.body().then(b => { bytes += b.length; }).catch(() => {})));
  let response;
  try {
    response = await page.goto(new URL(p, base).href, { waitUntil: 'load', timeout: 20000 });
  } catch (error) {
    results.push({ path: p, loadMs: Date.now() - t0, bytes, error: String(error?.message || error), violations: [] });
    await page.close();
    continue;
  }
  if (!response || response.status() >= 400) {
    results.push({ path: p, loadMs: Date.now() - t0, bytes, error: `Page returned HTTP ${response?.status() ?? 'no response'}`, violations: [] });
    await page.close();
    continue;
  }
  const loadMs = Date.now() - t0;
  // Measure response bodies for a bounded window; streaming bodies must not block the audit.
  await Promise.race([Promise.all(pending), new Promise(resolve => setTimeout(resolve, 5000))]);
  const measuredBytes = bytes;
  await page.waitForTimeout(1500);
  await page.evaluate(axeSrc);
  const axe = await page.evaluate(() => axe.run());
  results.push({ path: p, loadMs, bytes: measuredBytes, violations: axe.violations });
  await page.close();
}
await browser.close();

const counts = { critical: 0, serious: 0, moderate: 0, minor: 0 };
let weighted = 0;
let findings = '';
for (const r of results) {
  findings += `### ${r.path}\n`;
  if (r.error) findings += `_Audit incomplete: ${r.error}._\n`;
  if (!r.violations.length && !r.error) findings += '_No automated violations._\n';
  for (const v of r.violations) {
    const imp = v.impact || 'minor';
    counts[imp] += v.nodes.length; weighted += W[imp] * v.nodes.length;
    findings += `- **[${imp}] ${v.help}** (\`${v.id}\`, ${v.nodes.length} element${v.nodes.length > 1 ? 's' : ''}) — ${v.helpUrl}\n` +
      v.nodes.slice(0, 2).map(n => `  - \`${n.html.replace(/`/g, "'").slice(0, 100)}\``).join('\n') + '\n';
  }
  findings += '\n';
}
const total = Object.values(counts).reduce((a, b) => a + b, 0);
const metrics = '| Page | Load (ms) | Transfer (KB) |\n|---|---|---|\n' +
  results.map(r => `| ${r.path} | ${r.loadMs} | ${(r.bytes / 1024).toFixed(1)} |`).join('\n');
const vars = { site: base, date: new Date().toISOString().slice(0, 10), pages: results.length, axe: axeVersion,
  total, ...counts, score: Math.max(0, 100 - weighted), metrics, findings };
const md = readFileSync('report-template.md', 'utf8').replace(/{{(\w+)}}/g, (_, k) => vars[k]);
mkdirSync('reports', { recursive: true });
writeFileSync(`reports/${out}.md`, md);
writeFileSync(`reports/${out}.json`, JSON.stringify(results, null, 2));
console.log(`wrote reports/${out}.md  violations=${total} score=${vars.score}`);
const failedPages = results.filter(r => r.error);
if (failedPages.length) {
  console.error(`Audit incomplete for ${failedPages.length} page(s); see the report for details.`);
  process.exitCode = 1;
}
