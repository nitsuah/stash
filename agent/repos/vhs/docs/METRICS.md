# Metrics

## Core Metrics

| Metric          | Value      | Notes                                   |
| --------------- | ---------- | ---------------------------------------------- |
| Code Coverage   | 85.4%      | Whole tree (`src/server.js` + `src/modules/**`), lines. Docker-measured and config-gated numbers now agree — see note below. |
| Test Files      | 8          | server.test.js, coverage-boost.test.js, debug-jobs.test.js, basic.test.js, test-omdb-enhancements.spec.js, ebay-valuation.test.js, worker.test.js, auth.test.js |
| Unit Test Cases | 231        | All passing (8 test files; per-suite counts below) |
| E2E Test Files  | 14         | Playwright specs in tests_playwright/   |
| Last Updated    | 2026-09-02 |                                         |

## Collection Stats

| Metric          | Value | Notes                              |
| --------------- | ----- | ---------------------------------- |
| Tapes Indexed   | —     | Records in PostgreSQL `tapes` table |
| Data Backend    | PostgreSQL (Neon) | Migrated from flat tapes.json |

## Progress

- [ ] First tape scanned and committed
- [x] Export to CSV working (built into web UI)
- [x] Export to JSON working (built into web UI)
- [x] Print price tags working
- [x] Sell Drafts (eBay/Mercari) export working (built into web UI)
- [x] Valuation script (eBay **active-listing** lookup) — `src/modules/ebay.js` + `POST /api/tapes/:id/valuate`. Asking prices, not sold prices; true sold data needs the Marketplace Insights API (see TASKS.md).

## Test Breakdown

| Test Suite            | Tests | Status  |
| --------------------- | ----- | ------- |
| server.test.js        | 46    | ✅ Pass |
| coverage-boost.test.js| 77    | ✅ Pass |
| debug-jobs.test.js    | 1     | ✅ Pass |
| basic.test.js         | 1     | ✅ Pass |
| test-omdb-enhancements.spec.js | 41 | ✅ Pass |
| ebay-valuation.test.js | 39   | ✅ Pass |
| worker.test.js        | 9     | ✅ Pass |
| auth.test.js           | 17    | ✅ Pass |
| **Total (unit)**      | **231** | **✅ All Pass** |
| tests_playwright/ (14 specs) | — | E2E; run separately |

## Docker Testing

```bash
# Build
docker compose -f config/docker-compose.yml build

# Unit tests
docker run --rm vhs-web npx jest --runInBand

# Whole-tree coverage
docker run --rm vhs-web npx jest --runInBand --coverage
```

### Coverage measurement — Docker and local now agree

As of 2026-09-02 the Dockerfile copies `jest.config.js` into the image (it previously
didn't), so `docker run … npx jest --coverage` and a local `npx jest --coverage` measure
**the same thing**: `collectCoverageFrom: ['src/server.js', 'src/modules/**/*.js']`
(excluding the two confirmed-orphaned files below), gated by `coverageThreshold` in
`jest.config.js`. Previously these disagreed (71.94% config-scoped vs. 74.88%
whole-tree-ungated) because the Docker image silently ignored the config file entirely.

`src/modules/routes/jobs.js` and `src/modules/routes/lookup.js` are excluded from
`collectCoverageFrom` — both are confirmed orphaned (server.js implements those routes
inline and never `require()`s either file; see `docs/TASKS.md`). Counting dead code
against coverage would understate real posture, not overstate it, so this is a scope
correction, not a threshold-gaming move.

**Whole-tree measurement (2026-09-02, Docker, `npx jest --coverage`):**
- Statements: 85.4%
- Branches: 79.78%
- Functions: 88.33%
- Lines: **85.4%**

Coverage history on this basis (whole tree, config honored):

| Date | Lines | Notes |
| --- | --- | --- |
| 2026-08-27 (pre-eBay) | 70.82% | 166 tests, `src/server.js` only |
| 2026-08-27 (post-eBay) | 74.88% | 205 tests, `src/server.js` only — but measured via the *ungated* Docker command; not directly comparable to the config-scoped number of the same date (71.94%) |
| 2026-09-02 | **85.4%** | 231 tests, `src/server.js` + `src/modules/**` (jobs.js/lookup.js excluded as dead code); Docker and config-gated measurement now identical |

The jump from 74.88% to 85.4% is **not** an apples-to-apples improvement on the old
basis — the 2026-09-02 number covers far more code (`src/modules/**` was previously
uncounted entirely) while also removing two dead files from the denominator. The real,
comparable improvement: `worker.js` went from 44% to 100% lines, `auth.js` from 34% to
100% lines, and `system.js` from 52% to 100% lines (the last one via deleting unused
`healthHandler`/`caCertHandler`, not by adding tests to dead code).

`coverageThreshold` in `jest.config.js` is set a few points below the measured
2026-09-02 baseline (82% statements / 77% branches / 85% functions / 82% lines) so it
gates real regressions without being brittle to minor day-to-day drift.
