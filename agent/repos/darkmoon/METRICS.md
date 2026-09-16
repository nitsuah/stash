# Metrics

## Core Metrics

| Metric           | Value  | Notes                                                                                          |
| ---------------- | ------ | ---------------------------------------------------------------------------------------------- |
| Code Coverage    | 71.18% | Measured by Vitest v8 (Docker, 2026-08-28). Branches: 55.85%, Functions: 76.65%, Lines: 73.65% |
| Build Time       | ~5s    | Vite production build (measured on M1 Mac, Mar 2026)                                           |
| Bundle Size      | 2.1MB  | Measured: `dist/` output, Mar 2026                                                             |
| Test Files       | 79     | Vitest unit and integration tests                                                              |
| Test Cases       | 659    | Total test cases (654 passing, 5 skipped)                                                      |
| Source Files     | ~80    | TypeScript/TSX files in src/ (excluding tests and types)                                       |
| Lines of Code    | ~10K   | Estimated (excluding node_modules and generated files)                                         |
| API Routes       | 1      | WebSocket server with /health endpoint                                                         |
| Dependencies     | 10     | Production dependencies (see package.json)                                                     |
| Dev Dependencies | 31     | Development and testing tools                                                                  |

## Health

| Metric           | Value      | Notes                                                                                                                                     |
| ---------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Open Issues      | 0          | As of Mar 2026                                                                                                                            |
| Open PRs         | 0          | As of Mar 2026                                                                                                                            |
| Health Score     | 100        | Overseer calculated, Mar 2026                                                                                                             |
| Last Updated     | 2026-08-28 | Multiplayer readiness gate merged (#418): logger/cors/health/port/tagAuthorization modules, test suite expanded to 79 files / 654 passing |
| CI Status        | ✅ Passing | All tests passing, build successful                                                                                                       |
| TypeScript       | ✅ Strict  | Strict mode enabled, 0 type errors                                                                                                        |
| Linting          | ✅ Clean   | ESLint with --max-warnings=0                                                                                                              |
| Pre-commit Hooks | ✅ Active  | Husky + lint-staged enforcing quality gates                                                                                               |
