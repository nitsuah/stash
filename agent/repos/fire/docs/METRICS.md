# METRICS.md

## Metrics Table

| Metric                            | Current                                  | Target  | Status       |
| :-------------------------------- | :--------------------------------------- | :------ | :----------- |
| Code Coverage          | 85.37% stmts / 70.13% branch / 82.78% funcs / 85.19% lines | 80% stmts/funcs/lines, 70% branch (`config/vitest.config.ts`) | Met |
| Total Tests                       | 411 (37 files, all passing)              | 100+    | Met          |
| CI/CD Build Status                | Passing (GitHub Actions)                 | Passing | Met          |
| ESLint Violations                 | 0                                        | 0       | Met          |
| Dependency Vulnerabilities        | 1 high (dev deps only, via `npm audit`)  | 0       | Below Target |
| Total Lines of Code (LOC)         | TBD (run `cloc app/`)                    | N/A     | Tracked      |
| Cyclomatic Complexity             | TBD                                      | <10     | Untracked    |
| API Average Response Time         | TBD                                      | <100ms  | Untracked    |
| Client JS Size (app/lib/)         | TBD (no build step, modules served raw)  | N/A     | N/A          |
| Build Success Rate                | N/A (no build step)                      | 99%     | N/A          |
| Deployment Frequency              | TBD                                      | Weekly  | Untracked    |
| Last updated                      | 2026-09-18 (`npm install` + `npm run test:coverage`, native Node 22 — no Docker) |  |    |

## How to Update

To gather and update these metrics, follow these steps:

1.  **Test Coverage (Lines):**
    ```bash
    npm test -- --coverage --coverageReporters=text-lcov | grep -E 'Lines|Statements' | awk '{print $4}'
    # Manually extract the percentage
    ```
