---
kind: eng-loc
repo: fire
date: 2026-10-29
---

# eng-loc · fire · 2026-10-29

> 🧭 [[repos/fire|fire]] · ← [[reports/eng-loc-fire-2026-10-22|2026-10-22]] <!-- nav -->

HEAD: f5c6ce4a129e62c81f21bb45a13fc2d8c7696632

kind: eng-loc · repo: fire · tier: T1 (vigil snapshot 2026-10-21) · mode: --report · last commit: 2026-10-29 00:17 -0400

Method: `git ls-files` + per-file `wc -l` on a `--depth 1` clone. Excluded: lock/min/map/d.ts, dist/build/vendor/node_modules, docs, binaries, CSS, JSON data, promo/, test files. Churn/author history is **not available** (shallow clone), so the churn signal is "assumed: not confirmed" throughout. Per-file coverage is not measured; test-suite presence is noted only.

## Inventory Summary
- Code LOC (js/ts/html, excl. tests/promo/CSS/JSON): 32,482
- Test LOC: 28,193 across 113 files. Largest test file `tests/e2e-ui/dashboard-layout.spec.js` at 1,186 LOC, under the ~1,500 test-hotspot threshold, so no test-file slot.
- Container: `Dockerfile` present (used for Phase 3 when refactoring).

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `app/index.html` | 1,844 | HTML | App shell markup (structure not inspected) |
| 2 | `app/lib/side-gig.js` | 1,419 | JS | Side-gig calculators, eBay report upload, tab switching |
| 3 | `app/lib/chaos-events.js` | 1,370 | JS | Event simulation (`simulate()`) and event data |
| 4 | `app/lib/layout-manager.js` | 1,171 | JS | Dashboard layout registry and picker UI |
| 5 | `app/lib/cointracker-connector.js` | 1,092 | JS | CoinTracker fetch, parse, and valuation |
| 6 | `app/lib/tables/dashboard.js` | 899 | JS | Dashboard table rendering |
| 7 | `app/lib/projections.js` | 787 | JS | Financial projections |
| 8 | `app/app.js` | 686 | JS | App bootstrap |
| 9 | `app/lib/finance-parsing.js` | 669 | JS | Finance data parsing |
| 10 | `app/lib/csv-import.js` | 627 | JS | CSV import |

## Risk Rank

- **High — `app/lib/side-gig.js`**: `initPlatformCalculators()` spans about 140 lines (≈L1098–1238) and wires the eBay upload init, calculator DOM reads, and tab switching in one function. Calc logic and DOM handling are mixed in a 1,419-line file. Rationale is the >80-line function plus mixed concerns, not size alone.
- **Medium — `app/lib/chaos-events.js`**: `simulate()` is about 57 lines with a nested loop block near L1087 (`while (need > 0 …)`, ~60 lines, boundaries approximate). Simulation logic and event data share one file. Medium because the function is long but the concern is single (simulation).
- **Medium — `app/lib/cointracker-connector.js`**: a for-loop block of about 80 lines (≈L507) inside a file that also covers valuation (≈L848–907). Function boundaries approximate, not confirmed.
- **Medium — `app/lib/layout-manager.js`**: `openPicker()` about 67 lines (L924) plus a 51-line `register()`.
- **Low — `app/index.html`**: markup shell; large but flat. Not a complexity target without a structural finding.
- Others (dashboard.js, projections.js, app.js, finance-parsing.js, csv-import.js): no structural signal recorded this run. Not inspected in depth.

## Refactor Opportunities by Phase (suggested, not executed)

- **Phase 1, side-gig.js**: extract the eBay report upload init into its own module, and move tab switching into a UI module. Keep `side-gig.js` as the re-export barrel. Risk: medium, since DOM wiring is involved. Validate with the e2e-ui spec and unit tests.
- **Phase 2, cointracker-connector.js**: split valuation (≈L848–907) from fetch/parse. Risk: medium. Needs unit coverage added first, since coverage is not confirmed.
- **Phase 3, layout-manager.js**: pull `openPicker()` into picker and registry modules. Risk: low-medium. Manual QC on dashboard layout surfaces (the picker is user-visible).

## Validation Plan
Per LOC.md Phase 3: run the test suite in the repo's Docker setup, smoke-test the dev server, and spot-check the dashboard golden paths before each PR. Not run in report mode.

## Repo Summary

| Repo | Top concern | Priority | Notes |
|---|---|---|---|
| fire (T1) | `side-gig.js` mixed-concern wiring function | High | Largest code file is HTML markup; strong test suite |

Canaries: not applicable to this repo.
