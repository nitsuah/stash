// Loads the extension in headless Chromium and runs it against a deliberately inaccessible page. Run in the playwright image:
//   node test.mjs   (cwd = this folder; resolves playwright from ../audit-scanner)
import { createRequire } from 'node:module';
import { cpSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
const { chromium } = createRequire(resolve('../audit-scanner/package.json'))('playwright');

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
await popup.waitForSelector('#score, #out p', { timeout: 60000 }); await popup.waitForTimeout(8000); console.log('OUT', (await popup.textContent('#out')).slice(0, 300));
console.log('SCORE', await popup.textContent('#score'));
console.log('ITEMS', await popup.locator('li').count());
await ctx.close();
