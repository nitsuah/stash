---
kind: eng-loc
repo: fire
date: 2026-10-22
---

# LOC Report — fire (2026-10-22)

> 🧭 [[repos/fire|fire]] · ← [[reports/eng-loc-fire-2026-09-16|2026-09-16]] <!-- nav -->

HEAD: 861c5307c8072c5ffb5b086e5dc23c52a3ce0650

Mode: `--report` (dry run, no changes made)
Date: 2026-10-22
Repo: `nitsuah/fire` · Tier: **T1** · Latest commit: 2026-10-22 04:12 -0400
Method: `git clone --depth 1`, `git ls-files`, Grep line counts, Read/awk structural checks. Churn signal **assumed unavailable** (shallow clone, 1 commit visible).

## Inventory (Phase 0)
- Tracked files: 362 · after exclusions: 275
- Source LOC (js/mjs/py/sh, incl. tests): ~48,902 across 203 files
- Test LOC: ~18,027 across 81 files — noted here, not ranked. Largest single test: `tests/e2e-ui/dashboard-layout.spec.js` (1,164) — below the ~1,500 test-file threshold, so no test-file hotspot.
- Excluded: docs, `promo/` media builds, CSV/mermaid/data files.

## Top 10 code files (non-test)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `app/lib/chaos-events.js` | 1,370 | JS (UMD) | Seeded life-event catalog + timeline engine |
| 2 | `app/lib/side-gig.js` | 1,356 | JS | Side-gig UI wiring + tax/platform logic |
| 3 | `app/lib/layout-manager.js` | 1,171 | JS | Dashboard layout manager (one object literal) |
| 4 | `app/lib/cointracker-connector.js` | 1,092 | JS | CoinTracker API connector |
| 5 | `app/lib/tables/dashboard.js` | 886 | JS | Dashboard table renderers |
| 6 | `app/lib/projections.js` | 787 | JS | Projection engine |
| 7 | `app/mcp-server.mjs` | 776 | MJS | MCP server tool definitions + dispatch |
| 8 | `app/app.js` | 684 | JS | App bootstrap/UI glue |
| 9 | `app/lib/finance-parsing.js` | 669 | JS | Statement parsing |
| 10 | `app/lib/csv-import.js` | 627 | JS | CSV import |

CSS: largest is in `app/` styles (style smell, not ranked).

## Risk rank

- **High — `app/lib/layout-manager.js` (1,171).** A single `const LayoutManager = {…}` object literal spanning ~1,000 lines with **41 methods** (counted at 4-space indent). Mixed concerns (layout state, DOM, persistence — assumed from method names, not fully read). **No test file references it** (confirmed by search of `tests/`).
- **High — `app/lib/side-gig.js` (1,356).** 56 top-level declarations; three init functions are 113–142 lines each (`initSideGigManager`, `initPlaidLink`, `initPlatformCalculators`), with nesting to 40 spaces. Wiring + calculation logic in one file. One test file references it.
- **High — `app/mcp-server.mjs` (776).** `handleTool()` is a ~430-line function with **16 `case` branches** plus a ~170-line `TOOLS` schema array. Mitigated by 7 test files touching the MCP server.
- **Medium-High — `app/lib/cointracker-connector.js` (1,092).** `createMcpSession` (~112 lines) and `normalizeWallets` (~130 lines) exceed the 80-line threshold; 68 declarations. One test file (`tests/unit/cointracker-connector.test.mjs`, 923 lines) covers it.
- **Medium — `app/lib/chaos-events.js` (1,370).** Mostly a data catalog (8 categories, event entries) plus a seeded timeline engine. Size is driven by data, so structural risk is lower than LOC suggests; the engine/catalog split is clean. One test file covers it. Per LOC.md, flagged for the split, not for size.
- **Medium — `app/lib/tables/dashboard.js` (886).** Contains a ~295-line `DIVERSIFICATION_TIPS` constant (data — extract-only, low risk) and several 90–110 line render functions. Three test files reference it.
- **Low — `app/app.js`, `app/lib/finance-parsing.js`, `app/lib/csv-import.js`.** Large but single-concern (bootstrap, parsing); no >80-line function found in the structural pass.

## Refactor opportunities by phase (for a future `--refactor`)

- **layout-manager.js:** add a characterization test first (no coverage exists), then split the `LayoutManager` object into `layout/state.js`, `layout/persistence.js`, `layout/render.js`, keeping `layout-manager.js` as the re-export barrel so existing imports still resolve.
- **side-gig.js:** move each `init*` function to its own module under `app/lib/side-gig/`; leave `side-gig.js` as the barrel. Extract pure tax/platform calculators first (lowest DOM coupling).
- **mcp-server.mjs:** move `TOOLS` schema to `app/mcp/tools.mjs`; split `handleTool` cases into per-domain handler maps. Existing MCP tests validate behavior before and after.
- **cointracker-connector.js:** pull `normalizeWallets` into `cointracker-normalize.js` (pure function, easy to test in isolation); the session code stays put.
- **chaos-events.js:** move the `CATEGORIES` and event catalog into `app/lib/chaos/catalog.js`; engine stays in `chaos-events.js` as the UMD barrel.
- **tables/dashboard.js:** move `DIVERSIFICATION_TIPS` to a data module — zero-behavior-change first phase.

## Validation plan (per phase)
- `Dockerfile` and `compose.yaml` exist → run tests and the dev server inside the compose setup before any commit.
- Unit suite (`tests/unit/**`, Node test runner) for each touched module; the e2e-ui and journey Playwright specs (`config/playwright.*.config.js`) for dashboard/layout changes.
- Layout and side-gig changes are user-visible rendering → manual golden-path QC (dashboard layout drag/reset, side-gig calculator entry) before merge, in addition to CI green.
- MCP server changes: run `tests/unit/mcp-server-read-only.test.mjs` and `mcp-net-worth.test.mjs` as the gate.

## Repo summary

| Repo | Top concern | Priority | Notes |
|------|-------------|----------|-------|
| fire | Untested 1,171-line `LayoutManager` object; 430-line MCP `handleTool` dispatch; side-gig init functions | High | T1. Largest test-backed hotspots: mcp-server, cointracker-connector |

## Notes
- Deferred: none in this run (report mode only).
- `chaos-events.js` is the largest raw file, but its size is mostly catalog data; ranked Medium on structure, not LOC.
