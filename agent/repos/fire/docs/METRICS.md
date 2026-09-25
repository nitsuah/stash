---
up: "[[repos/fire]]"
source: https://github.com/nitsuah/fire/blob/main/docs/METRICS.md
kind: repo-doc
repo: fire
---

# METRICS.md

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Metrics Table

| Metric                            | Current                                  | Target  | Status       |
| :-------------------------------- | :--------------------------------------- | :------ | :----------- |
| Code Coverage | 84.62% stmts / 74.85% branch / 85.15% funcs / 84.85% lines (Docker, 2026-09-24, 484 tests) | 80% stmts/funcs/lines, 70% branch (`config/vitest.config.ts`) | Met. CI now runs `npm run test:coverage`, so a threshold drop fails the PR |
| Total Tests | 484 (43 files, all passing, Docker 2026-09-24) | 100+ | Met |
| CI/CD Build Status                | Passing (GitHub Actions)                 | Passing | Met          |
| ESLint Violations                 | 0                                        | 0       | Met          |
| Dependency Vulnerabilities        | 1 high (dev deps only, via `npm audit`)  | 0       | Below Target |
| Total Lines of Code (LOC)         | TBD (run `cloc app/`)                    | N/A     | Tracked      |
| Cyclomatic Complexity             | TBD                                      | <10     | Untracked    |
| API Average Response Time         | TBD                                      | <100ms  | Untracked    |
| Client JS Size (app/lib/)         | TBD (no build step, modules served raw)  | N/A     | N/A          |
| Build Success Rate                | N/A (no build step)                      | 99%     | N/A          |
| Deployment Frequency              | TBD                                      | Weekly  | Untracked    |
| Last updated | 2026-09-24 (`docker build --target test -t fire-test . && docker run --rm fire-test npm run test:coverage`; `-u root` is no longer needed after the Dockerfile `chown` fix) |  |  |

## How to Update

To gather and update these metrics, follow these steps:

1.  **Test Coverage (Lines):**
    ```bash
    npm test -- --coverage --coverageReporters=text-lcov | grep -E 'Lines|Statements' | awk '{print $4}'
    # Manually extract the percentage
    ```
