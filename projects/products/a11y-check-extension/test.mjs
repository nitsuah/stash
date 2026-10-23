// Loads the extension in headless Chromium and runs it against a deliberately inaccessible page. Run in the playwright image:
//   npm i playwright && node test.mjs   (inside the playwright Docker image)
import { createRequire } from 'node:module';
import { cpSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
const { chromium } = createRequire(import.meta.url)('playwright');

// Test copy gets host permissions, because activeTab only applies to a real toolbar click.
const dir = '/tmp/ext-under-test';
rmSync(dir, { recursive: true, force: true });
cpSync('.', dir, { recursive: true, filter: (p) => !p.includes('node_modules') });
const m = JSON.parse(readFileSync(`${dir}/manifest.json`, 'utf8'));
m.host_permissions = ['<all_urls>'];
writeFileSync(`${dir}/manifest.json`, JSON.stringify(m));

const ctx = await chromium.launchPersistentContext('/tmp/profile', {
  channel: 'chromium', headless: true,
  args: [`--disable-extensions-except=${dir}`, `--load-extension=${dir}`, '--no-sandbox'],
});
let [sw] = ctx.serviceWorkers();
if (!sw) sw = await ctx.waitForEvent('serviceworker');
const id = new URL(sw.url()).host;

const target = await ctx.newPage();
await target.goto('https://dequeuniversity.com/demo/mars/');
const popup = await ctx.newPage();
await popup.goto(`chrome-extension://${id}/popup.html`);
const tabId = await popup.evaluate(async () => {
  const own = (await chrome.tabs.getCurrent()).id;
  return (await chrome.tabs.query({})).find((t) => t.id !== own && String(t.url || '').includes('dequeuniversity')).id;
});
await popup.goto(`chrome-extension://${id}/popup.html?tab=${tabId}`);
await popup.click('#run');
try {
  await popup.waitForSelector('#score', { timeout: 60000 });
} catch (err) {
  console.error('FAIL no score shown. Popup said:', (await popup.textContent('#out')).slice(0, 300));
  await ctx.close();
  process.exit(1);
}
const score = Number((await popup.textContent('#score')).match(/\d+/)[0]);
const items = await popup.locator('li').count();
console.log('SCORE', score, 'ITEMS', items);
await ctx.close();
// The demo page is deliberately inaccessible, so a perfect score or an empty list means the audit is broken.
if (!(score < 100) || items < 1) {
  console.error('FAIL expected a score below 100 and at least one violation');
  process.exit(1);
}
