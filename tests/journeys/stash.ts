// Fixture for the nightly journeys: pages/ served by serve.mjs. Web fonts and the
// Showcase expand.js CDN script are blocked so a flaky third party cannot fail
// (or reshape) the page; the site must work without them.
import type { Page } from '@playwright/test';
import { test as base, expect } from '@playwright/test';

export { expect };
export { step } from './journey';

export const test = base.extend({
  page: async ({ page }, use) => {
    await page.route(/^https:\/\/(fonts\.(googleapis|gstatic)\.com|cdn\.jsdelivr\.net)\//, route => route.abort());
    await use(page);
  },
});

/** Collect uncaught page errors; the journey asserts the list is empty at the end. */
export function trackPageErrors(page: Page): string[] {
  const errors: string[] = [];
  page.on('pageerror', e => errors.push(`${e.message}\n${e.stack ?? ''}`));
  return errors;
}
