// Journey helpers. Ported to TypeScript from nitsuah/.github
// journeys/templates/journey.js.
//
//   import { test, expect, step } from './stash';
//   test('reader tours the site', { tag: ['@feature:journeys'] }, async ({ page }) => {
//     await step(page, 'open the landing page', async () => { ... });
//   });
//
// Every step() is a test.step, so a failure names the step (the reporter
// fingerprints on it), and ends with a visual baseline (toHaveScreenshot)
// unless { screenshot: false }.
import { test, expect } from '@playwright/test';
import type { Locator, Page } from '@playwright/test';

export { test, expect };

export const slug = (s: string) =>
  s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');

export interface StepOpts {
  /** false to skip the visual baseline for this step */
  screenshot?: boolean;
  /** a Locator to snapshot instead of the whole viewport */
  target?: Locator;
  /** Locators to paint over (live numbers, timestamps) */
  mask?: Locator[];
  /** a feature id: with DOCS_SCREENSHOTS=<dir> set, also save <dir>/<id>.png */
  docs?: string;
}

export async function step(
  page: Page,
  title: string,
  fn: () => Promise<void>,
  opts: StepOpts = {}
) {
  return test.step(title, async () => {
    await fn();
    const target = opts.target ?? page;
    if (opts.screenshot !== false) {
      await expect(target).toHaveScreenshot(`${slug(title)}.png`, {
        mask: opts.mask,
      });
    }
    if (opts.docs && process.env.DOCS_SCREENSHOTS) {
      await target.screenshot({
        path: `${process.env.DOCS_SCREENSHOTS}/${opts.docs}.png`,
        animations: 'disabled',
      });
    }
  });
}
