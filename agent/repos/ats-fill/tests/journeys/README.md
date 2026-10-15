---
up: "[[repos/ats-fill]]"
title: "ats-fill · README"
source: https://github.com/nitsuah/ats-fill/blob/main/tests/journeys/README.md
kind: repo-doc
repo: ats-fill
---

# Journeys

Nightly "AI user" journeys: the happy paths a job seeker takes in the extension, one visual baseline per step. Run by `.github/workflows/journeys.yml` through the shared harness in `nitsuah/.github` (contract: `journeys/STANDARD.md`). Failures become `bot:journey` issues; `BUGS.md` lives on the `bot/journeys` branch.

- `journey.mjs` is the vendored `step()` helper. `ats-fill.mjs` is the fixture: the real built extension (`dist/`) loaded headed in Chromium, seeded with the same fictional demo state as the screenshot suite (`tests/e2e/helpers/demo-state.mjs`), with job search and the active-tab lookups answered from demo data and time frozen at the demo's "now". `fill.spec.mjs` drives the fictional `tests/e2e/fixtures/fake-ats.html` page.
- Journeys are tagged `@feature:<id>` with ids from `promo/spots.json`. `step(..., { docs: '<id>' })` also writes `<dir>/<id>.png` when `DOCS_SCREENSHOTS` is set, so a later `capture:screenshots` script can reuse them.
- Tolerance is `maxDiffPixels: 5` (0 px of noise over 136 soak runs; one changed letter of small text is 12 px).

## Run and update baselines

The extension needs a display, and baselines are Linux-only. Always use the Playwright image (same version as `@playwright/test`):

```sh
docker run --rm -v "$PWD:/w" -w /w mcr.microsoft.com/playwright:v1.64.0-jammy \
  sh -c "npm ci && npm run test:journeys -- --update-snapshots"
```

Drop `--update-snapshots` to check. CI sets `CI=true`, where a missing baseline fails. Soak new journeys with `CI=true ... --retries 0 --repeat-each 3`.
