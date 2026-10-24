// Renders 512x512 Actor icons to out/icon-<name>.png. Run like covers.mjs (playwright image, MM mounted at /w, cwd /w/cover-factory).
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
const { chromium } = createRequire(resolve('../audit-scanner/package.json'))('playwright');

const tile = (a, b, inner) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient></defs>
<rect width="512" height="512" rx="112" fill="url(#g)"/>${inner}</svg>`;

const icons = {
  accessibility: tile('#1d4ed8', '#0e7490', '<g fill="none" stroke="#fff" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"><circle cx="256" cy="150" r="30" fill="#fff" stroke="none"/><path d="M136 214h240M256 214v110M256 324l-70 90M256 324l70 90"/></g>'),
  'broken-link': tile('#047857', '#0f766e', '<g fill="none" stroke="#fff" stroke-width="38" stroke-linecap="round"><path d="M214 298l-44 44a64 64 0 0 1-90-90l44-44a64 64 0 0 1 90 0"/><path d="M298 214l44-44a64 64 0 0 1 90 90l-44 44a64 64 0 0 1-90 0"/><path d="M256 130v-46M180 156l-30-34M332 156l30-34M256 382v46M180 356l-30 34M332 356l30 34" stroke-width="26"/></g>'),
  seo: tile('#6d28d9', '#be185d', '<g fill="none" stroke="#fff" stroke-width="38" stroke-linecap="round" stroke-linejoin="round"><circle cx="228" cy="228" r="92"/><path d="M296 296l92 92"/></g><g fill="#fff"><rect x="184" y="236" width="20" height="40" rx="6"/><rect x="218" y="206" width="20" height="70" rx="6"/><rect x="252" y="188" width="20" height="88" rx="6"/></g>'),
  'security-headers': tile('#9a3412', '#b91c1c', '<path d="M256 96l132 48v104c0 90-58 146-132 178-74-32-132-88-132-178V144z" fill="none" stroke="#fff" stroke-width="34" stroke-linejoin="round"/><path d="M200 262l42 42 76-84" fill="none" stroke="#fff" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>'),
  'structured-data': tile('#0f766e', '#1d4ed8', '<g fill="none" stroke="#fff" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"><path d="M200 118c-40 0-52 18-52 52v36c0 22-12 38-34 50 22 12 34 28 34 50v36c0 34 12 52 52 52"/><path d="M312 118c40 0 52 18 52 52v36c0 22 12 38 34 50-22 12-34 28-34 50v36c0 34-12 52-52 52"/></g><g fill="#fff"><circle cx="216" cy="256" r="18"/><circle cx="256" cy="256" r="18"/><circle cx="296" cy="256" r="18"/></g>'),
  sitemap: tile('#4338ca', '#0369a1', '<g fill="#fff"><rect x="206" y="92" width="100" height="72" rx="16"/><rect x="82" y="320" width="100" height="72" rx="16"/><rect x="206" y="320" width="100" height="72" rx="16"/><rect x="330" y="320" width="100" height="72" rx="16"/></g><g fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"><path d="M256 164v76M132 320v-80h248v80M256 240v80"/></g>'),
};

mkdirSync('out', { recursive: true });
const browser = await chromium.launch();
for (const [name, svg] of Object.entries(icons)) {
  const page = await browser.newPage({ viewport: { width: 512, height: 512 } });
  writeFileSync(`out/icon-${name}.svg`, svg);
  await page.setContent(`<body style="margin:0;background:transparent">${svg}</body>`);
  await page.screenshot({ path: `out/icon-${name}.png`, omitBackground: true });
  await page.close();
  console.log('icon', name);
}
await browser.close();
