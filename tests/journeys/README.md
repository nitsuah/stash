# Journeys: stash Pages site

Nightly "AI user" journeys for the overview site in `pages/` (the only UI in this repo). Contract: [nitsuah/.github journeys/STANDARD.md](https://github.com/nitsuah/.github/blob/main/journeys/STANDARD.md). Failures become deduplicated `bot:journey` issues; no model is involved.

- `site.spec.ts`: a reader tours landing -> Journeys -> Imps -> Setup (every local link, image and video resolves), then opens each page at 390 px with no horizontal scroll.
- `stash.ts` blocks Google Fonts and the Showcase `expand.js` CDN script; `serve.mjs` serves `pages/` with no dependencies.
- Visual baselines are Linux-only. Only the landing hero is baselined; regenerate it in the pinned image:

```sh
docker run --rm -v "$PWD:/w" -w /w/tests/journeys mcr.microsoft.com/playwright:v1.65.1-jammy \
  sh -c "npm ci && npx playwright test -c playwright.config.ts --update-snapshots"
```

Run them (what CI does): `cd tests/journeys && npm ci && npm run test:journeys` inside that image with `CI=true`. Keep `@playwright/test` in `package.json` in step with the image tag in `.github/workflows/journeys.yml`.
