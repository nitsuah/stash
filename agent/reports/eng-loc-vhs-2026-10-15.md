# ENG LOC Report — vhs (2026-10-15)
HEAD: 717e7abc02fe0fb438fd563373668b5eb968d955

Mode: `--report` (dry run, no changes made)
Date: 2026-10-15
Source: shallow clone (`--depth 1`) of `nitsuah/vhs` @ `717e7abc02fe0fb438fd563373668b5eb968d955`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Note: shallow clone — churn/author history is **not available**; marked "assumed: not confirmed" where used.
Prior report: `eng-loc-vhs-2026-07-29.md` (no recorded HEAD sha in that report to diff against; proceeding as a fresh baseline for this field).

## Inventory Summary
- Tracked source files (post-exclusion, code extensions only): 87
- Total LOC counted: 13,242

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `public/js/ui.js` | 896 | JavaScript | Front-end UI module (tabs, table, bulk actions) |
| 2 | `src/server.js` | 761 | JavaScript | Express server (routes, auth, migrations, proxy) |
| 3 | `tests/coverage-boost.test.js` | 612 | JavaScript | Test suite |
| 4 | `public/js/camera.js` | 527 | JavaScript | Barcode/camera capture module |
| 5 | `tests/server.test.js` | 511 | JavaScript | Test suite |
| 6 | `tests/test-omdb-enhancements.spec.js` | 499 | JavaScript | Test suite |
| 7 | `tests/ebay-valuation.test.js` | 445 | JavaScript | Test suite |
| 8 | `public/js/utils.js` | 403 | JavaScript | Shared front-end utilities |
| 9 | `tests_playwright/collection-features.spec.js` | 379 | JavaScript | E2E test suite |
| 10 | `public/js/review.js` | 321 | JavaScript | Review panel module |
| 11 | `public/js/ai.js` | 306 | JavaScript | AI metadata lookup module |
| 12 | `scripts/audit-metadata.js` | 290 | JavaScript | Metadata audit script |

## Risk Rank and Rationale

| File | Risk | Rationale |
|------|------|-----------|
| `public/js/ui.js` | **High** | Imports from 9 other modules (inventory, db, utils, review, state, camera, ai, table-ux, auth) and mixes tab navigation, CSV export, table rendering, and bulk actions in one file — 18 top-level function/handler boundaries. Mixed concerns per Phase 1 criteria. |
| `src/server.js` | **High** | 35 route-handler registrations (`app.get/post/put/delete/patch`) in a single file alongside auth, migrations, cert setup, and a proxy middleware import. Classic "routing + business logic" mix, though route bodies may delegate to `./modules/*` (not confirmed without a full read). |
| `tests/*.test.js`, `tests_playwright/*.spec.js` | **Low** | Single clear concern (tests). Not refactor targets — size reflects test breadth. |
| `public/js/camera.js` | Medium | Barcode/camera capture — plausibly single-concern (hardware/interaction logic) but large enough to warrant a check for mixed UI+capture-logic. Assumed: not confirmed without full read. |
| `public/js/utils.js` | Low-Medium | "Utils" files often accrete unrelated helpers over time; 403 lines is borderline — worth a pass to check for cohesion, but not flagged as urgent. |
| `public/js/review.js` / `public/js/ai.js` | Low | Under the 500-line historical threshold used by this repo's own prior reports; included here for context, not flagged. |

Test coverage: strong — dedicated `tests/` and `tests_playwright/` directories exist, including `server.test.js` and `coverage-boost.test.js`, suggesting `src/server.js` already has test coverage (not line-by-line confirmed for the specific hotspot functions).

Churn: **assumed: not confirmed** (shallow clone, no history available).

Canaries: N/A (canary list only applies to the `stash` repo; not scanned this run).

## Refactor Opportunities by Phase (handoff notes, not yet actioned)

- **`public/js/ui.js`**: smallest safe extraction is the CSV export helper (`csvCell` + related) into `public/js/csv.js` — self-contained, no shared mutable state with the rest of the UI module. Next phase: split bulk-action handling (`updateBulkBar`, `applyBulkStatus`, `deleteBulk` call sites) into `public/js/bulk-actions.js`.
- **`src/server.js`**: the file already delegates to `./modules/config`, `./modules/auth`, `./modules/db`, `./modules/certs` — suggesting route groups could similarly move to `./modules/routes/*.js` (e.g., auth routes, inventory routes, image-fetch/SSRF-guarded routes) without behavior change, since the modular pattern is already established in this codebase.

## Validation Plan (for a future `--refactor` pass)
- Run the existing `tests/` suite (`server.test.js`, `coverage-boost.test.js`) and `tests_playwright/` E2E suite after each extraction.
- Smoke-test the Express dev server (barcode capture flow, bulk actions, CSV export) since `ui.js` and `camera.js` touch interaction/rendering surfaces — flag for manual QC.

## Repo Summary

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| vhs | `public/js/ui.js` and `src/server.js` — mixed-concern front-end module and route file | High | Existing `./modules/*` pattern in `server.js` makes route extraction low-risk |

## Ordered Next-Cycle Targets (this repo)
1. `public/js/ui.js` (896 LOC) — High, extract CSV/bulk-action helpers
2. `src/server.js` (761 LOC) — High, extract route groups into `./modules/routes/*`
3. `public/js/camera.js` (527 LOC) — Medium, confirm concerns before planning a cut
4. `public/js/utils.js` (403 LOC) — Low-Medium, cohesion pass
