# Metrics

## Core Metrics

| Metric           | Value  | Notes                                                    |
| ---------------- | ------ | -------------------------------------------------------- |
| Code Coverage    | 96.10% | Measured by Vitest v8 (Docker), statements at 95.16%     |
| Build Time       | ~5s    | Vite production build (measured on M1 Mac, Mar 2026)     |
| Bundle Size      | 2.1MB  | Measured: `dist/` output, Mar 2026                       |
| Test Files       | 62     | Vitest unit and integration tests                        |
| Test Cases       | 371    | Total test cases (366 passing, 5 skipped)                |
| Source Files     | 64     | TypeScript/TSX files in src/ (excluding tests and types) |
| Lines of Code    | ~8K    | Estimated (excluding node_modules and generated files)   |
| API Routes       | 1      | WebSocket server with /health endpoint                   |
| Dependencies     | 9      | Production dependencies (see package.json)               |
| Dev Dependencies | 22     | Development and testing tools                            |

## Health

| Metric           | Value      | Notes                                                           |
| ---------------- | ---------- | --------------------------------------------------------------- |
| Open Issues      | 0          | As of Mar 2026                                                  |
| Open PRs         | 0          | As of Mar 2026                                                  |
| Health Score     | 100        | Overseer calculated, Mar 2026                                   |
| Last Updated     | 2026-05-24 | Metrics refresh (Docker coverage run, extended scoped excludes) |
| CI Status        | ✅ Passing | All tests passing, build successful                             |
| TypeScript       | ✅ Strict  | Strict mode enabled, 0 type errors                              |
| Linting          | ✅ Clean   | ESLint with --max-warnings=0                                    |
| Pre-commit Hooks | ✅ Active  | Husky + lint-staged enforcing quality gates                     |
