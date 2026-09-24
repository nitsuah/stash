# Metrics

## Core Metrics

| Metric        | Value  | Notes                                                                                                                                                                                                                                                                                                                                                                            |
| ------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Code Coverage | 96.13% | Overall line coverage (v8) from `pnpm run test:docker` on 2026-09-23 — Stmts 94.71%, Branches 90.82%, Funcs 84.89%, Lines 96.13%. Previously reported 0% because `config/vitest.config.ts` excluded `'app/**'`, which matched every file once the Docker runner mounted the repo at `/app`; exclude removed. Thresholds in `config/vitest.config.ts` remain the source of truth. |
| Test Time     | ~14s   | 440 tests across 21 suites confirmed passing (`pnpm run test:docker`, Docker run 2026-09-16, PMO audit). Unfiltered `vitest run --coverage` scoped to `config/vitest.config.ts`'s `include` — every `*.test.{ts,tsx}`/`*.spec.{ts,tsx}` file discovered under `app/`, `lib/`, and `components/`, not a hand-picked subset.                                                       |
| Bundle Size   | TBD    | Not measured yet                                                                                                                                                                                                                                                                                                                                                                 |
| Test Files    | 21     | lib/farm (utils, gameLogic, farmReducer, spawner, isometric, terrain, structures, notifications, techTree), lib/api-types, components/ContactModal, components/rts/hooks (spawnHelpers, towerHelpers, mapSelectors, tickFunctions, tickEnemyAI, domainHooks) and more                                                                                                            |
| Test Cases    | 440    | All tests passing - game logic, terrain, state management, notification, spawn/tower math, map selectors, tick functions, domain hooks, contact modal coverage                                                                                                                                                                                                                   |

## Health

| Metric        | Value      | Notes                                                                    |
| ------------- | ---------- | ------------------------------------------------------------------------ |
| Open Issues   | 0          | `gh issue list` — no open issues as of 2026-09-16                        |
| PR Turnaround | TBD        | Not enough recent merged-PR data sampled this cycle to estimate reliably |
| Skipped Tests | 0          | All tests passing                                                        |
| Health Score  | TBD        | Overall health score                                                     |
| Last Updated  | 2026-09-23 | Code coverage fixed and measured (96.13% lines) via Docker               |

<!--
AGENT INSTRUCTIONS:
1. Update these metrics regularly (e.g., before a merge/last commit weekly or after major releases).
2. Use automated tools to fetch values where possible.
3. Keep this file focused on actual project metrics, not feature documentation.
-->
