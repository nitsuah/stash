
# Metrics

**Last Validated:** 2026-09-01 (full re-run in Docker — Jest via `config/Dockerfile.unit`, Playwright via `config/docker-compose.test.yml`)

## Core Metrics

| Metric        | Value                                        | Notes                                        |
| ------------- | --------------------------------------------- | --------------------------------------------- |
| Code Coverage | 97.21% stmts / 81.37% branch / 83.33% funcs   | Jest unit tests (214 passing)                |
| Test Suites   | 17                                            | Jest unit test suites                        |
| TypeScript    | Strict mode                                  | Assumed zero errors — not re-run this pass    |
| Lines of Code | ~21.8K                                        | Not re-measured this pass; excludes tests/generated/config |

## Health

| Metric          | Value      | Notes                          |
| --------------- | ---------- | ------------------------------ |
| Passing Tests   | 214 Jest + 11 Playwright = 225 | 100% of tests actually run |
| Skipped Tests   | 9          | Wallet-connection Playwright tests, intentionally gated pending a local wallet mock (see `docs/TASKS.md` P2) |
| Security Alerts | Not re-run this pass | Last known: 0 (npm audit, zero high/critical, 2026-04-13) |
| Last Updated    | 2026-09-01 | Metrics audit date |

## Test Breakdown

| Test Suite      | Count | Status | Notes |
| ---------------- | ----- | ------ | ----- |
| Jest Unit Tests   | 214   | ✅ 214/214 passing | React Testing Library, 17 suites |
| Playwright A11y   | 5     | ✅ 5/5 passing | `tests/accessibility/critical.spec.ts`, WCAG 2.1 AA (axe-core) |
| Playwright Nav    | 1     | ✅ 1/1 passing | `tests/e2e/labs/navigation.spec.ts` |
| Playwright Smoke  | 5     | ✅ 5/5 passing | `tests/smoke.spec.ts` |
| Playwright Wallet | 9     | ⏭️ 0/9 (intentionally skipped) | `tests/e2e/labs/wallet-connection.spec.ts` — gated until a local wallet mock exists |

The previously published "Resume Tests" (8) and "Visual Tests" (9) rows no longer correspond to anything in the repo — there is no `tests/**/resume*.spec.ts` or visual-regression spec under `tests/` today. The full current Playwright surface is exactly 4 spec files / 20 tests, confirmed by running `config/docker-compose.test.yml` with `FORCE_BROWSER_E2E=1` (same flag the Nightly workflow uses).

## Docker Testing

| Metric | Value | Notes |
| ------ | ----- | ----- |
| Unit test image (`config/Dockerfile.unit`) | `node:22.13.0-slim` | Built and run 2026-09-01; `npm run test:coverage` passed (214/214) |
| Playwright image (`config/Dockerfile.test`) | `mcr.microsoft.com/playwright:v1.62.1-noble` | Version bumped from v1.57.0 since last validation |
| Playwright run | `docker-compose -f config/docker-compose.test.yml run --rm -e FORCE_BROWSER_E2E=1 playwright` | 20 tests, 11 passed, 9 intentionally skipped, 27.3s |

## Notes

- **Bug found and fixed while refreshing these numbers**: `npm run test:e2e:docker` (`config/docker-compose.test.yml`) ran `npx playwright test` with no `--config` flag. Since `config/playwright.config.ts` isn't at the repo root, Playwright silently fell back to zero-config discovery and picked up the `src/**/__tests__/*.test.tsx` Jest files too, which crashed with `ReferenceError: describe is not defined` for every Jest file. Fixed by pointing the compose command at `--config config/playwright.config.ts`.
- **Code Coverage**: 97.21% statements / 81.37% branch / 83.33% functions, measured via Jest coverage report, re-run 2026-09-01 in Docker (`config/Dockerfile.unit`). 214 tests across 17 suites — up from the previously recorded 213/16.
- **Build Performance / Bundle Size**: not re-measured this pass; previous values (35.13s build, 324.90 MB `.next`) are stale and removed rather than re-published unverified.
- **Test Status**: both Jest and Playwright were re-verified this pass (see Test Breakdown above) — the only gap is `npm audit` and manual bundle/build timing, which weren't re-run.
- **Lines of Code**: not re-measured this pass; previously recorded at ~21.8K (2026-04-13).
- **Security**: not re-run this pass; previously zero npm audit vulnerabilities as of 2026-04-13.
- **Accessibility**: re-verified 2026-09-01 — the 5 critical WCAG 2.1 AA checks in `tests/accessibility/critical.spec.ts` all pass. The previous claim of "20 A11y tests" and "13 pages fully audited" wasn't reproduced; only the critical-path suite exists today.

Last validated: 2026-09-01 — full Jest + Playwright suite re-run in Docker.

<!--
AGENT INSTRUCTIONS:
This file tracks project health metrics.
1. Update values based on the latest code analysis or CI/CD outputs.
2. "Code Coverage": Percentage of code covered by tests.
3. "Build Time": Time taken for the build process.
4. "Bundle Size": Size of production assets.
5. "Health": General health indicators like open issues count.
6. Ensure values are accurate and reflect the current state of the codebase.
7. Can allow custom attribute value pairs, but leave existing.
-->
