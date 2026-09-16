# Metrics

## Core Metrics

| Metric        | Value           | Notes                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Code Coverage | TBD (still broken) | Re-ran `pnpm test:coverage` via Docker on 2026-09-16 (PMO audit): still reproduces the same bug — v8 coverage report shows 0% across all files/stmts/branches/funcs/lines despite all 440 tests passing. Not a regression from the 2026-09-02 finding; the underlying Docker/bind-mount + v8 provider attribution issue is unresolved. Repo-wide thresholds remain enforced per the `thresholds` block in `config/vitest.config.ts` (source of truth). |
| Test Time     | ~14s            | 440 tests across 21 suites confirmed passing (Docker run 2026-09-16, PMO audit)                                                                                                                                                                                                                                                                                                                            |
| Bundle Size   | TBD             | Not measured yet                                                                                                                                                                                                                                                                                                                                                                                |
| Test Files    | 21              | lib/farm (utils, gameLogic, farmReducer, spawner, isometric, terrain, structures, notifications, techTree), lib/api-types, components/ContactModal, components/rts/hooks (spawnHelpers, towerHelpers, mapSelectors, tickFunctions, tickEnemyAI, domainHooks) and more                                                                                                                           |
| Test Cases    | 440             | All tests passing - game logic, terrain, state management, notification, spawn/tower math, map selectors, tick functions, domain hooks, contact modal coverage                                                                                                                                                                                                                                  |

## Health

| Metric        | Value      | Notes                                                                                                   |
| ------------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| Open Issues   | 0          | `gh issue list` — no open issues as of 2026-09-16                                                        |
| PR Turnaround | TBD        | Not enough recent merged-PR data sampled this cycle to estimate reliably                                 |
| Skipped Tests | 0          | All tests passing                                                                                       |
| Health Score  | TBD        | Overall health score                                                                                    |
| Last Updated  | 2026-09-16 | PMO audit: tests re-confirmed passing (440/440) via Docker; coverage figure still broken (see above)    |

<!--
AGENT INSTRUCTIONS:
1. Update these metrics regularly (e.g., before a merge/last commit weekly or after major releases).
2. Use automated tools to fetch values where possible.
3. Keep this file focused on actual project metrics, not feature documentation.
-->
