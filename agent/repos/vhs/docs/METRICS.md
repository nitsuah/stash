---
up: "[[repos/vhs]]"
source: https://github.com/nitsuah/vhs/blob/main/docs/METRICS.md
kind: repo-doc
repo: vhs
---

# Metrics

> 🧭 [vhs](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Core Metrics

| Metric          | Value      | Notes |
| --------------- | ---------- | ----- |
| Code Coverage   | 86.86%     | Whole tree (`src/server.js` + `src/modules/**`), lines. Docker-validated Jest run; breakdown below. |
| Unit Test Cases | 252        | All passing (9 suites) |
| Last Updated    | 2026-09-23 |       |

## Coverage

| Metric     | Coverage | Threshold | Status |
|------------|----------|-----------|--------|
| Statements | 86.86% (2030/2337) | 82% | ✅ |
| Branches   | 81.82% (549/671)   | 77% | ✅ |
| Functions  | 87.88% (58/66)     | 85% | ✅ |
| Lines      | 86.86% (2030/2337) | 82% | ✅ |

Percentages are rounded from the counts. Jest's text reporter truncates instead,
so it prints 81.81% for branches and 87.87% for functions.

Back above the thresholds after adding `tests/tmdb.test.js`. `src/modules/tmdb.js`
(added in #55) went from 7.6% to 100% on all four metrics. Before those tests, the
2026-09-23 run was 79.59 / 79.22 / 81.82 / 79.59, down from the 2026-09-02 baseline
in `jest.config.js` (85.40 / 79.78 / 88.33 / 85.40, re-confirmed 2026-09-18).

### Lowest-covered files

| File | Stmts | Branch | Funcs |
|------|-------|--------|-------|
| src/modules/certs.js       | 48.64% | 50%    | 100%   |
| src/server.js              | 73.88% | 75.22% | 100%   |
| src/modules/json-parser.js | 77.41% | 72.22% | 66.66% |
| src/modules/ollama.js      | 80.00% | 44.44% | 66.66% |
| src/modules/activity-log.js | 81.81% | 80%   | 66.66% |

## Tests

| Metric      | Result       |
|-------------|--------------|
| Test Suites | 9 passed / 9 |
| Tests       | 252 passed / 252 |

## CI

Last `CI` workflow run on `main`: ✅ success (#54, 2026-09-11). CI does not currently
enforce the coverage thresholds.

---

Last Validated: 2026-09-23 (Docker `node:22-alpine` image from repo `Dockerfile`, `NODE_ENV=test npx jest --coverage`)
