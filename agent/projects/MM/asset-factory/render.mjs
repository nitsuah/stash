// Renders out/<pack>/book.html -> book.pdf + preview.png and out/<pack>/*.svg -> .png, then zips nothing (zip step is in run.sh).
// Playwright is resolved from ../audit-scanner/node_modules so no extra install is needed. Usage: node render.mjs <outDir>
import { createRequire } from 'node:module';
import { readdirSync, existsSync, statSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const require = createRequire(resolve('../audit-scanner/package.json'));
const { chromium } = require('playwright');
const out = resolve(process.argv[2] || 'out');
const browser = await chromium.launch();
for (const pack of readdirSync(out)) {
  const dir = join(out, pack);
  if (!statSync(dir).isDirectory()) continue;
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
  if (existsSync(join(dir, 'book.html'))) {
    await page.goto(pathToFileURL(join(dir, 'book.html')).href);
    await page.pdf({ path: join(dir, 'book.pdf'), format: 'Letter', printBackground: true });
    const pages = page.locator('.pg');
    await pages.nth((await pages.count()) > 1 ? 1 : 0).screenshot({ path: join(dir, 'preview.png') });
  }
  for (const f of readdirSync(dir).filter((n) => n.endsWith('.svg'))) {
    const m = readFileSync(join(dir, f), 'utf8').match(/width='(\d+)' height='(\d+)'/);
    const art = await browser.newPage({ viewport: { width: Number(m[1]), height: Number(m[2]) } });
    await art.goto(pathToFileURL(join(dir, f)).href);
    if (pack.includes('wallpaper')) await art.screenshot({ path: join(dir, f.replace('.svg', '.jpg')), type: 'jpeg', quality: 92 }); else await art.screenshot({ path: join(dir, f.replace('.svg', '.png')) });
    await art.close();
  }
  await page.close();
  console.log('rendered', pack);
}
await browser.close();
