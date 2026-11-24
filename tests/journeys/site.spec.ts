import { test, expect, step, trackPageErrors } from './stash';

const PAGES = [
  { link: 'Journeys', path: 'journeys.html', h1: /QA before you have/ },
  { link: 'Imps', path: 'imps.html', h1: /One issue\. One small/ },
  { link: 'Setup guide', path: 'setup.html', h1: /Build your own/ },
];

test('reader tours the overview site and every local link resolves', { tag: ['@feature:journeys'] }, async ({ page, request }) => {
  const errors = trackPageErrors(page);

  await step(
    page,
    'open the landing page',
    async () => {
      await page.goto('/');
      await expect(page.getByRole('heading', { level: 1 })).toContainText('one Obsidian brain');
    },
    { target: page.locator('header.hero h1') }
  );

  for (const p of PAGES) {
    await step(
      page,
      `follow the ${p.link} nav link`,
      async () => {
        await page.goto('/');
        await page.locator('nav.nav').getByRole('link', { name: p.link, exact: true }).click();
        await expect(page).toHaveURL(new RegExp(`${p.path}$`));
        await expect(page.getByRole('heading', { level: 1 })).toHaveText(p.h1);
      },
      { screenshot: false }
    );
  }

  await step(
    page,
    'every local link, image and video on every page resolves',
    async () => {
      const missing: string[] = [];
      for (const url of ['/', ...PAGES.map(p => `/${p.path}`)]) {
        await page.goto(url);
        const refs = await page.evaluate(() => {
          const attr = (sel: string, name: string) =>
            [...document.querySelectorAll(sel)].map(e => e.getAttribute(name) ?? '');
          return [
            ...attr('a[href]', 'href'),
            ...attr('img[src]', 'src'),
            ...attr('video[poster]', 'poster'),
            ...attr('source[src]', 'src'),
            ...attr('link[rel=stylesheet]', 'href'),
          ];
        });
        for (const ref of new Set(refs)) {
          if (!ref || /^(https?:|mailto:|data:|#|javascript:)/.test(ref)) continue;
          const target = new URL(ref.split('#')[0] || url, page.url()).pathname;
          const res = await request.get(target);
          if (!res.ok()) missing.push(`${url} -> ${ref} (${res.status()})`);
        }
      }
      expect(missing, 'broken local references').toEqual([]);
    },
    { screenshot: false }
  );

  expect(errors, 'uncaught page errors').toEqual([]);
});

test('reader opens the setup guide on a phone', { tag: ['@feature:journeys'] }, async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const errors = trackPageErrors(page);

  for (const path of ['/', '/setup.html', '/journeys.html', '/imps.html']) {
    await step(
      page,
      `${path === '/' ? 'landing' : path.slice(1)} fits a 390 px screen`,
      async () => {
        await page.goto(path);
        await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        expect(overflow, 'horizontal overflow in px').toBeLessThanOrEqual(0);
      },
      { screenshot: false }
    );
  }

  expect(errors, 'uncaught page errors').toEqual([]);
});
