---
up: "[[repos/skyview]]"
title: "skyview · README"
source: https://github.com/nitsuah/skyview/blob/main/tests/journeys/README.md
kind: repo-doc
repo: skyview
---

# Journeys

Nightly "AI user" journeys: the happy paths a visitor, client or operator takes, one visual baseline per step. Run by `.github/workflows/journeys.yml` through the shared harness in `nitsuah/.github` (contract: `journeys/STANDARD.md`). Failures become `bot:journey` issues; `BUGS.md` lives on the `bot/journeys` branch.

- `journey.ts` is the vendored `step()` helper. `skyview.ts` is the fixture: mocked `/api`, fictional demo data, frozen clock (2027-01-15), hero video aborted.
- Journeys are tagged `@feature:<id>` with ids from `promo/spots.json`. `step(..., { docs: '<id>' })` also writes `docs/screenshots/<id>.png` when `DOCS_SCREENSHOTS` is set, so a later `capture:screenshots` script can reuse them.
- Tolerance is `maxDiffPixels: 20` (DOM-only site: 0 px of noise over 81 soak runs).

## Run and update baselines

Baselines are Linux-only. Always use the Playwright image (same version as `@playwright/test`):

```sh
docker run --rm -v "$PWD:/w" -w /w mcr.microsoft.com/playwright:v1.64.0-jammy \
  sh -c "npm ci && npm run test:journeys -- --update-snapshots"
```

Drop `--update-snapshots` to check. CI sets `CI=true`, where a missing baseline fails. Soak new journeys with `CI=true ... --retries 0 --repeat-each 3`.
