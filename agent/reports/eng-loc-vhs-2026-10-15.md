---
kind: eng-loc
repo: vhs
date: 2026-10-15
---

# ENG LOC Report — vhs (2026-10-15)

> 🧭 [[repos/vhs|vhs]] · ← [[reports/eng-loc-vhs-2026-07-29|2026-07-29]] <!-- nav -->

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

Code files only — test files excluded per `LOC.md` Phase 1 (none in this repo are over the ~1,500-line standalone-callout bar; largest is `tests/coverage-boost.test.js` at 612 lines).

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `public/js/ui.js` | 896 | JavaScript | Front-end UI module (tabs, table, bulk actions) |
| 2 | `src/server.js` | 761 | JavaScript | Express server (routes, auth, migrations, proxy) |
| 3 | `public/js/camera.js` | 527 | JavaScript | Barcode/camera capture module |
| 4 | `public/js/utils.js` | 403 | JavaScript | Shared front-end utilities |
| 5 | `public/js/review.js` | 321 | JavaScript | Review panel module |
| 6 | `public/js/ai.js` | 306 | JavaScript | AI metadata lookup module |
| 7 | `scripts/audit-metadata.js` | 290 | JavaScript | Metadata audit script |
| 8 | `public/js/capture.js` | 275 | JavaScript | Capture-flow module |
| 9 | `public/js/auth.js` | 237 | JavaScript | Client-side auth module |
| 10 | `src/modules/omdb.js` | 230 | JavaScript | OMDB metadata lookup module |

## Risk Rank and Rationale

| File | Risk | Rationale |
|------|------|-----------|
| `public/js/ui.js` | **High** | Imports from 9 other modules (inventory, db, utils, review, state, camera, ai, table-ux, auth) and mixes tab navigation, CSV export, table rendering, and bulk actions in one file — 18 top-level function/handler boundaries. Mixed concerns per Phase 1 criteria. |
| `src/server.js` | **High** | 35 route-handler registrations (`app.get/post/put/delete/patch`) in a single file alongside auth, migrations, cert setup, and a proxy middleware import. Classic "routing + business logic" mix, though route bodies may delegate to `./modules/*` (not confirmed without a full read). |
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

## Ordered Next-Cycle Targets (cross-repo, tier-weighted)

Shared across this run's three reports (vigil, vhs, kryptos) — see each report's own Repo Summary for per-repo context. Tier from `agent/projects/scope.md`: vigil = T1, vhs = T2, kryptos = untiered (not yet registered in vigil; ranks alongside T2/T3 per `LOC.md`).

1. `app/api/mcp/route.ts` (vigil, T1, 893 LOC) — High, extract tool handlers
2. `lib/sync.ts` (vigil, T1, 707 LOC) — High, extract fallback cache
3. `components/dashboard/RepoTableRow.tsx` (vigil, T1, 699 LOC) — High, extract derived-data hook, needs manual QC
4. `src/kryptos/k4/frontier_checks.py` (kryptos, untiered, 1,131 LOC) — High, extract `hill_exhaustive` first
5. `public/js/ui.js` (vhs, T2, 896 LOC) — High, extract CSV/bulk-action helpers
6. `src/server.js` (vhs, T2, 761 LOC) — High, extract route groups into `./modules/routes/*`
7. `src/kryptos/k4/crib_constraints.py` (kryptos, untiered, 877 LOC) — Medium-High, needs direct read before a phase plan

Tier reordered what raw LOC would have suggested: `frontier_checks.py` (1,131 LOC, the largest file in this run) would rank #1 by size alone, but vigil's three T1 findings are weighted ahead of it despite being smaller, since vigil is a T1 (Critical/production) repo and kryptos isn't yet tiered.
