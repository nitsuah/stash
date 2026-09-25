# Metrics

> 🧭 [darkmoon](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Core Metrics

| Metric           | Value  | Notes                                                                                          |
| ---------------- | ------ | ---------------------------------------------------------------------------------------------- |
| Code Coverage    | 94.52% | Measured by Vitest v8 (Docker, 2026-09-23). Branches: 76.47%, Functions: 93.64%, Lines: 95.88% |
| Build Time       | ~5s    | Vite production build (measured on M1 Mac, Mar 2026)                                           |
| Bundle Size      | 2.1MB  | Measured: `dist/` output, Mar 2026                                                             |
| Test Files       | 96     | Vitest unit and integration tests                                                              |
| Test Cases       | 794    | Total test cases (789 passing, 5 skipped)                                                      |
| Source Files     | ~80    | TypeScript/TSX files in src/ (excluding tests and types)                                       |
| Lines of Code    | ~10K   | Estimated (excluding node_modules and generated files)                                         |
| API Routes       | 1      | WebSocket server with /health endpoint                                                         |
| Dependencies     | 10     | Production dependencies (see package.json)                                                     |
| Dev Dependencies | 32     | Development and testing tools                                                                  |

## Health

| Metric           | Value      | Notes                                                                                                                                                                                                                              |
| ---------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Open Issues      | 1          | #446 (eslint 10 bump blocked on `eslint-plugin-jsx-a11y`). `gh issue list`, 2026-09-24                                                                                                                                             |
| Open PRs         | 0          | `gh pr list`, 2026-09-24                                                                                                                                                                                                           |
| Health Score     | 100        | Overseer calculated, Mar 2026                                                                                                                                                                                                      |
| Last Updated     | 2026-09-24 | 2026-09-24 PMO audit refreshed Open Issues/Open PRs from `gh`; coverage figures unchanged from 2026-09-23. Coverage push: R3F scene components tested via @react-three/test-renderer; suite now 96 files / 789 passing / 5 skipped |
| CI Status        | ✅ Passing | All tests passing, build successful                                                                                                                                                                                                |
| TypeScript       | ✅ Strict  | Strict mode enabled, 0 type errors                                                                                                                                                                                                 |
| Linting          | ✅ Clean   | ESLint with --max-warnings=0                                                                                                                                                                                                       |
| Pre-commit Hooks | ✅ Active  | Husky + lint-staged enforcing quality gates                                                                                                                                                                                        |
