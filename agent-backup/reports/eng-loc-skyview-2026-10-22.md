---
kind: eng-loc
repo: skyview
date: 2026-10-22
---

# LOC Report — skyview (2026-10-22)

> 🧭 [[repos/skyview|skyview]] · ← [[reports/eng-loc-skyview-2026-09-16|2026-09-16]] <!-- nav -->

HEAD: e43dd7a793040575544460e4c4899b27b2d1304e

Mode: `--report` (dry run, no changes made)
Date: 2026-10-22
Repo: `nitsuah/skyview` · Tier: — (not registered in vigil) · Latest commit: 2026-10-22 04:18 -0400
Method: `git clone --depth 1`, `git ls-files`, Grep line counts, Read/awk structural checks. Churn signal **assumed unavailable** (shallow clone).

## Inventory (Phase 0)
- Tracked files: 270 · after exclusions: 186
- Code LOC (js/jsx/mjs/ts/tsx/py/sql/sh, incl. tests): ~13,777 across 121 files
- Test LOC: ~4,339 across 37 files (`tests/`, `config/*.config.*`) — noted here, not ranked
- Excluded: docs (`*.md`), `assets/`, `.wav` media, `*.sql` counted only as code (migrations shown but not ranked as complexity)

## Top 10 code files (non-test)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `platform/src/pages/OperatorOnboarding.jsx` | 464 | JSX | Operator onboarding wizard page |
| 2 | `scripts/conversion-tracking.js` | 431 | JS | Analytics / conversion funnel tracking |
| 3 | `netlify/functions/api-operators.mjs` | 363 | MJS | Serverless operator API (routing + logic) |
| 4 | `platform/src/pages/OperatorProfile.jsx` | 359 | JSX | Operator profile page |
| 5 | `config.js` | 347 | JS | Site config (data-like; low structural risk) |
| 6 | `platform/src/pages/AdminDashboard.jsx` | 325 | JSX | Admin dashboard page |
| 7 | `netlify/functions/utils/portal.js` | 302 | JS | Portal helpers |
| 8 | `netlify/functions/api-bookings.mjs` | 292 | MJS | Bookings API handler |
| 9 | `netlify/functions/api-jobs.mjs` | 261 | MJS | Jobs API handler |
| 10 | `scripts/performance-monitor.js` | 220 | JS | Client performance monitor |

CSS: largest is `styles/` (not ranked, style smell per LOC.md Guardrails).
Test-file hotspot: none over ~1,500 lines (largest ~502, `tests/unit/api-bookings.test.js`).

## Risk rank

- **High — `platform/src/pages/OperatorOnboarding.jsx` (464).** One component body (~400 lines by heuristic: a single `useEffect` and render block of ~414 lines, end-line inferred from next declaration — assumed) carrying multi-step wizard state, validation, and API calls. **No test file references it** (grep for the component name across test/spec files in `tests/`: 0 hits).
- **Medium — `netlify/functions/api-operators.mjs` (363).** 12 top-level declarations; route dispatch mixed with data access and business rules in one handler. One unit test references it (`tests/unit/operator-availability-api.test.js`), which covers only part of the surface (assumed).
- **Medium — `scripts/conversion-tracking.js` (431).** 30 top-level declarations mixing DOM hooks, storage, and event shaping in one file. Three test files reference it.
- **Medium — `platform/src/pages/OperatorProfile.jsx` (359)** and **`AdminDashboard.jsx` (325).** Page-level components with data fetch + view logic together; no structural split yet. Lower urgency than onboarding.
- **Low — `config.js` (347).** Config/data-shaped; flagged for size only, no structural rationale → not a refactor target.
- **Low — `netlify/functions/api-bookings.mjs`, `api-jobs.mjs`, `utils/portal.js`.** Handler-per-file pattern already mostly separated; watch for growth.

## Refactor opportunities by phase (for a future `--refactor`)

- **OperatorOnboarding.jsx:** extract each wizard step into its own component (`steps/*.jsx`) and move the validation and submit logic into a `useOnboardingForm` hook. The page file remains the composition root, so the route import doesn't change. First phase should add one smoke test for the step sequence, since no test covers it today.
- **api-operators.mjs:** split route table from handlers — `operators/handlers/*.mjs` by resource, with the original file kept as the thin router/re-export.
- **conversion-tracking.js:** separate the pure event-shaping functions (testable) from the DOM/storage side effects.
- **OperatorProfile.jsx / AdminDashboard.jsx:** lift data loading into hooks (`useOperatorProfile`, `useAdminStats`) — small, low-risk cut.

## Validation plan (per phase)
- Repo has `Dockerfile` / `Dockerfile.dev` / `docker-compose.dev.yml` → use the dev container for tests and the dev server smoke check before any commit.
- Run the Vitest unit suite (`tests/unit/**`) and the Playwright site/journey specs (`config/playwright.*.config.ts`) after each extraction.
- Netlify functions: exercise each touched endpoint once locally (`netlify dev` or the handler directly) before PR.
- UX/QC flag: OperatorOnboarding and OperatorProfile are user-visible flows — require manual golden-path QC (signup → onboarding complete → profile save), not only CI green.

## Repo summary

| Repo | Top concern | Priority | Notes |
|------|-------------|----------|-------|
| skyview | Onboarding wizard is one untested ~460-line page | Medium-High | Tier unregistered (ranks with T2/T3); no direct test on the largest file |

## Notes
- Deferred: none in this run (report mode only).
- Canary check: not applicable (canary lives in `stash`, not scanned this run).
