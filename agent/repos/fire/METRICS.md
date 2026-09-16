# METRICS.md

## Metrics Table

| Metric                            | Current                                  | Target  | Status       |
| :-------------------------------- | :--------------------------------------- | :------ | :----------- |
| Code Coverage          | 81.1% stmts / 68.33% branch / 75.67% funcs / 80.9% lines | 80% stmts/funcs/lines, 70% branch (`config/vitest.config.ts`) | Below Target (branch, funcs) |
| Total Tests                       | 251 (16 files, all passing)              | 100+    | Met          |
| CI/CD Build Status                | Passing (GitHub Actions)                 | Passing | Met          |
| ESLint Violations                 | 0                                        | 0       | Met          |
| Dependency Vulnerabilities        | 1 high (dev deps only, via `npm audit`)  | 0       | Below Target |
| Total Lines of Code (LOC)         | TBD (run `cloc app/`)                    | N/A     | Tracked      |
| Cyclomatic Complexity             | TBD                                      | <10     | Untracked    |
| API Average Response Time         | TBD                                      | <100ms  | Untracked    |
| Client JS Size (app/lib/)         | TBD (no build step, modules served raw)  | N/A     | N/A          |
| Build Success Rate                | N/A (no build step)                      | 99%     | N/A          |
| Deployment Frequency              | TBD                                      | Weekly  | Untracked    |
| Last updated                      | 2026-08-28 (`npm ci` + `npm run test:coverage` in a bare `node:22-alpine` container — not the project's own Dockerfile, which uses `npm install`; dependency resolution should be identical against the committed lockfile) |  |    |

## How to Update

To gather and update these metrics, follow these steps:

1.  **Test Coverage (Lines):**
    ```bash
    npm test -- --coverage --coverageReporters=text-lcov | grep -E 'Lines|Statements' | awk '{print $4}'
    # Manually extract the percentage
    ```
