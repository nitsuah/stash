// Reads reports/ci.json written by scan.mjs and fails (exit 1) when counts exceed a11y.config.json failOn.
import { readFileSync } from 'node:fs';
const cfg = JSON.parse(readFileSync(new URL('./a11y.config.json', import.meta.url), 'utf8'));
const data = JSON.parse(readFileSync('reports/ci.json', 'utf8'));
const pages = data.pages ?? data.results ?? data;
const count = { critical: 0, serious: 0, moderate: 0, minor: 0 };
for (const p of pages) for (const v of p.violations ?? []) {
  if (cfg.ignoreRules.includes(v.id)) continue;
  count[v.impact] = (count[v.impact] ?? 0) + (v.nodes?.length ?? 1);
}
console.log('Accessibility counts:', count);
let bad = false;
for (const [lvl, max] of Object.entries(cfg.failOn)) if (count[lvl] > max) { console.error(`FAIL: ${lvl} ${count[lvl]} > ${max}`); bad = true; }
process.exit(bad ? 1 : 0);
