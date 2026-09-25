# LOC Report — fire

> 🧭 [[repos/fire|fire]] · ← [[reports/eng-loc-fire-2026-07-29|2026-07-29]] <!-- nav -->

Mode: `--report` (dry run, no changes made)
Date: 2026-09-16
Source: shallow clone (`--depth 1`) of `nitsuah/fire` @ `25a783a594b6753e1a7cfc86abd9440dcb8afac0`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Note: shallow clone — churn/author history (many-authors, frequent-edits signal) is **not available**; that structural signal is marked "assumed: not confirmed" throughout.

## Inventory Summary
- Tracked source files (post-exclusion): 147
- Total LOC counted: 28,677

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `app/index.html` | 1564 | HTML | Main app shell/markup |
| 2 | `app/lib/css/components.css` | 1230 | CSS | Component styles |
| 3 | `app/routes/sync.js` | 942 | JS | eBay + Plaid sync routes (Express router) |
| 4 | `tests/unit/sync-plaid-route.test.mjs` | 722 | JS | Test file (excluded from risk ranking) |
| 5 | `app/lib/finance-parsing.js` | 669 | JS | Financial statement parsing |
| 6 | `app/app.js` | 664 | JS | Front-end state, UI, import/export, notifications |
| 7 | `app/lib/css/layout.css` | 658 | CSS | Layout styles |
| 8 | `app/lib/side-gig.js` | 633 | JS | eBay/Plaid/Etsy/FB side-gig fee calculators + sync UI |
| 9 | `app/lib/csv-import.js` | 619 | JS | CSV/statement import parsing |
| 10 | `app/lib/css/widgets.css` | 607 | CSS | Widget styles |

Notable file just outside the numeric top 10: `app/mcp-server.mjs` (601 LOC).

## Risk Rank & Rationale

1. **`app/routes/sync.js` — Critical**
   942 lines. Structural evidence: the `POST /plaid/transactions` route handler alone spans **lines 544–733 (~189 lines)** — more than double the 80-line guideline in a single Express route callback. The file also mixes two unrelated third-party integrations (eBay OAuth/sync and Plaid Link/sync) plus a templates/webhook CRUD section, all in one router module. Partial test coverage exists (`tests/unit/sync-plaid-route.test.mjs`, `tests/unit/sync-ebay-route.test.mjs`, `tests/e2e/webhook-sync.test.js`), but the giant transactions handler itself is not isolated. Highest-ROI target in this repo.

2. **`app/lib/csv-import.js` — Critical**
   619 lines. `parseFidelityPositions` spans **lines 170–394 (~224 lines)** — a single function nearly as long as some entire files elsewhere in this repo. It mixes CSV row-parsing, statement-format detection, and category/spending logic in one body. Combined with `parseChaseStatement`, `parseCapitalOneStatement`, and `parseSpendingTransactions` in the same file, this module has a clear mixed-parsers-in-one-file structure. No test file found under `tests/` referencing csv-import directly (assumed: not confirmed).

3. **`app/lib/side-gig.js` — High**
   633 lines. `initPlatformCalculators` spans **lines 453–559 (~106 lines)**, past the guideline. File combines eBay connection/sync UI logic, Plaid Link initialization, and fee/profit calculators for eBay, Etsy, and Facebook Marketplace — at least three distinct platform concerns in one module.

4. **`app/app.js` — Medium**
   664 lines, ~30 top-level functions, mostly short (10–40 lines) but spanning state aggregation (net worth, cash, CDs, equities), DOM/UI updates, CSV/JSON import-export, and notification permission handling — classic mixed-concerns "everything file" even though individual functions are reasonably sized. Has a companion `app/server.test.js` (436 lines) but coverage of `app.js` specifically not confirmed.

5. **`app/lib/finance-parsing.js` — Medium**
   669 lines. Single cohesive concern (parsing financial data formats), similar shape to `csv-import.js` but not yet inspected function-by-function this pass — flagged for next-cycle deep dive.

6. **`app/mcp-server.mjs` — Low-Medium**
   601 lines. MCP server definition — likely a flat tool-registration file (single concern). Not deep-dived this pass; assumed lower risk pending inspection.

7. **CSS files (`components.css`, `layout.css`, `widgets.css`, `base.css`) — Low (excluded per guardrail)**
   Style-only, large but single-concern. Deferred to a design-system pass, not this cycle.

8. **`app/index.html` — Low-Medium**
   1564 lines of markup for the main app shell. Not inspected for inline scripts this pass; if it embeds substantial inline JS, re-rank next cycle. Marked "assumed: markup-only, not confirmed."

## Refactor Opportunities by Phase

**`app/routes/sync.js`** (Critical):
- Phase 1: Extract the `/plaid/transactions` handler's category-mapping and dedup logic into `app/lib/plaid/transactions-sync.js`, leaving the route as a thin HTTP wrapper calling into it.
- Phase 2: Split the file along provider boundaries — `app/routes/sync-ebay.js` and `app/routes/sync-plaid.js` — with the shared `templates`/`webhook` CRUD routes staying in `sync.js` or moving to `app/routes/templates.js`.
- Phase 3: Re-evaluate `sync.js` size after 1–2; it should shrink to a thin router re-exporting the split modules.

**`app/lib/csv-import.js`** (Critical):
- Phase 1: Extract `parseFidelityPositions`'s statement-format detection sub-logic into a small `detectFidelityFormat` helper, then extract the row-to-position mapping loop into `mapFidelityRows` — smallest safe cuts first, no behavior change.
- Phase 2: Once `parseFidelityPositions` is under ~80 lines, consider splitting per-broker parsers (`parseChaseStatement`, `parseCapitalOneStatement`, `parseFidelityPositions`) into `app/lib/csv-import/<broker>.js` modules with `csv-import.js` as the dispatch/re-export barrel.

**`app/lib/side-gig.js`** (High):
- Phase 1: Extract the eBay-specific connection/sync UI functions (`checkEbayConnection` through `runEbaySyncNow`) into `app/lib/side-gig/ebay.js`.
- Phase 2: Extract Plaid-specific functions similarly into `app/lib/side-gig/plaid.js`.
- Phase 3: Extract per-platform fee/profit calculators (`calculateEtsy*`, `calculateFB*`, `calculateEbay*`) into `app/lib/side-gig/calculators.js`, leaving `side-gig.js` as an init/dispatch barrel.

## Validation Plan (for eventual `--refactor`)
- `app/routes/sync.js`: run `tests/unit/sync-plaid-route.test.mjs` and `tests/unit/sync-ebay-route.test.mjs` before/after each phase; add a smoke test for the `/plaid/transactions` category-mapping path first since it's currently the least-covered part of the largest function.
- `app/lib/csv-import.js`: add a smoke test importing a sample Fidelity CSV fixture before extracting (none confirmed to exist); diff parsed output pre/post-extraction for byte-identical results.
- `app/lib/side-gig.js`: run existing test suite; manually smoke-test the eBay/Plaid settings panels and one calculator (e.g. Etsy) in the dev server after each phase, since this file drives live UI panels.
- No Dockerfile/devcontainer confirmed in this pass (report mode only, no filesystem walk beyond `git ls-files`) — confirm before assuming host-run is safe for `--refactor`.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| fire | `app/routes/sync.js`: 189-line `/plaid/transactions` handler + two unrelated integrations (eBay, Plaid) in one router | Critical | Highest-ROI target; partial test coverage exists but not isolated to the largest handler |

## Ordered Next-Cycle Targets (this repo)
1. `app/routes/sync.js` — split eBay/Plaid routes, extract the 189-line transactions handler (Critical, highest ROI)
2. `app/lib/csv-import.js` — extract `parseFidelityPositions` (224-line function) into smaller helpers (Critical)
3. `app/lib/side-gig.js` — split by platform (eBay/Plaid/calculators) (High)
4. `app/app.js` — monitor; mixed concerns but individually small functions (Medium)
5. `app/lib/finance-parsing.js` — deep-dive next cycle, not yet function-inspected (Medium, deferred pending inspection)

## Deferred / Not Flagged
- `app/lib/css/*.css` — CSS-only, deferred to design-system pass per guardrail.
- `app/mcp-server.mjs`, `app/index.html` — flagged Low/Low-Medium on size alone pending a structural inspection; not confirmed as refactor risks this pass.
- Test files in top-10 by size (`tests/unit/sync-plaid-route.test.mjs`) — excluded from refactor ranking; large test files are expected.

## Assumptions / Unconfirmed
- Churn/author-frequency signal: **assumed unavailable** — shallow clone has no history beyond HEAD.
- Test coverage for `csv-import.js`, `app.js`, `finance-parsing.js`: assumed absent/unconfirmed based on filename search only, not a coverage-tool run.
- `app/mcp-server.mjs` and `app/index.html` structural risk: not deep-dived this pass, ranked provisionally by size + role only.
