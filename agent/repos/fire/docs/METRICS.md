---
up: "[[repos/fire]]"
title: "fire · METRICS"
source: https://github.com/nitsuah/fire/blob/main/docs/METRICS.md
kind: repo-doc
repo: fire
---

# METRICS.md

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Metrics Table

| Metric                            | Current                                  | Target  | Status       |
| :-------------------------------- | :--------------------------------------- | :------ | :----------- |
| Code Coverage | 84.31% stmts / 77.16% branch / 84.66% funcs / 84.97% lines (Docker, 2026-10-01, 715 tests) | 80% stmts/funcs/lines, 70% branch (`config/vitest.config.ts`) | Met for the measured scope only: thresholds cover the 8 files in `coverage.include`; routes, managers, Netlify Functions and the browser app are unmeasured |
| Total Tests | 715 Vitest (59 files) + 69 Playwright, all passing (Docker, 2026-10-07) | 100+ | Met |
| CI/CD Build Status                | Passing (GitHub Actions)                 | Passing | Met          |
| ESLint Violations                 | 0                                        | 0       | Met          |
| Dependency Vulnerabilities | 2 via `npm audit` (1 high in dev deps; 1 moderate in production deps), 2026-10-01 | 0 | Below Target |
| Total Lines of Code (LOC) | ~31.3k lines in `app/` + `netlify/` source, excluding tests (2026-10-01) | N/A | Tracked |
| Cyclomatic Complexity             | TBD                                      | <10     | Untracked    |
| API Average Response Time         | TBD                                      | <100ms  | Untracked    |
| Client JS Size (app/lib/) | ~714 KB raw across `app/lib/**/*.js` (no build step; includes the Node-only modules) | N/A | N/A |
| Build Success Rate                | N/A (no build step)                      | 99%     | N/A          |
| Deployment Frequency              | TBD                                      | Weekly  | Untracked    |
| Last updated | 2026-10-01 (`docker build --target test -t fire-test . && docker run --rm fire-test npm run test:coverage`; `-u root` is no longer needed after the Dockerfile `chown` fix) |  |  |

## How to Update

To gather and update these metrics, follow these steps:

1.  **Test Coverage (Lines):**
    ```bash
    npm test -- --coverage --coverageReporters=text-lcov | grep -E 'Lines|Statements' | awk '{print $4}'
    # Manually extract the percentage
    ```
