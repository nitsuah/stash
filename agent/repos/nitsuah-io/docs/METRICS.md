---
up: "[[repos/nitsuah-io]]"
title: "nitsuah-io · METRICS"
source: https://github.com/Nitsuah-Labs/nitsuah-io/blob/main/docs/METRICS.md
kind: repo-doc
repo: nitsuah-io
---


# Metrics

> 🧭 [nitsuah-io](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

**Last Validated:** 2026-09-24 (PMO audit: Jest unit/coverage re-run in Docker via `config/Dockerfile.unit`. Playwright was last run 2026-09-01 via `config/docker-compose.test.yml` and not re-run this pass)

## Core Metrics

| Metric        | Value                                        | Notes                                        |
| ------------- | --------------------------------------------- | --------------------------------------------- |
| Code Coverage | 97.37% stmts / 84.56% branch / 84% funcs / 97.37% lines | Jest unit tests (223 passing, Docker 2026-09-24) |
| Test Suites   | 19                                            | Jest unit test suites (Docker 2026-09-24)    |
| TypeScript    | Strict mode                                  | Assumed zero errors — not re-run this pass    |
| Lines of Code | ~21.8K                                        | Not re-measured this pass; excludes tests/generated/config |

## Health

| Metric          | Value      | Notes                          |
| --------------- | ---------- | ------------------------------ |
| Passing Tests   | 223 Jest (2026-09-24) + 11 Playwright (2026-09-01) = 234 | 100% of tests actually run |
| Skipped Tests   | 9          | Wallet-connection Playwright tests, intentionally gated pending a local wallet mock (see `docs/TASKS.md` P2) |
| Security Alerts | Not re-run this pass | Last known: 0 (npm audit, zero high/critical, 2026-04-13) |
| Last Updated    | 2026-09-24 | PMO audit: Jest coverage re-run in Docker |

## Test Breakdown

| Test Suite      | Count | Status | Notes |
| ---------------- | ----- | ------ | ----- |
| Jest Unit Tests   | 223   | ✅ 223/223 passing | React Testing Library, 19 suites (Docker 2026-09-24) |
| Playwright A11y   | 5     | ✅ 5/5 passing | `tests/accessibility/critical.spec.ts`, WCAG 2.1 AA (axe-core) |
| Playwright Nav    | 1     | ✅ 1/1 passing | `tests/e2e/labs/navigation.spec.ts` |
| Playwright Smoke  | 5     | ✅ 5/5 passing | `tests/smoke.spec.ts` |
| Playwright Wallet | 9     | ⏭️ 0/9 (intentionally skipped) | `tests/e2e/labs/wallet-connection.spec.ts` — gated until a local wallet mock exists |

The previously published "Resume Tests" (8) and "Visual Tests" (9) rows no longer correspond to anything in the repo — there is no `tests/**/resume*.spec.ts` or visual-regression spec under `tests/` today. The full current Playwright surface is exactly 4 spec files / 20 tests, confirmed by running `config/docker-compose.test.yml` with `FORCE_BROWSER_E2E=1` (same flag the Nightly workflow uses).

## Docker Testing

| Metric | Value | Notes |
| ------ | ----- | ----- |
| Unit test image (`config/Dockerfile.unit`) | `node:26.10.0-slim` | Built and run 2026-09-27 (Node 26 PR); `npm test` passed 282/282 across 24 suites |
| Playwright image (`config/Dockerfile.test`) | `mcr.microsoft.com/playwright:v1.63.0-noble` + Node 26.10.0 overlay | The upstream image ships Node 24.20.0; the overlay stage makes E2E run on the `.nvmrc` version |
| Playwright run | `docker run --rm --shm-size=2g -e FORCE_BROWSER_E2E=1 <Dockerfile.test image> npx playwright test --config config/playwright.config.ts` | 2026-09-27: 27 tests (incl. 6 in `tests/runtime.spec.ts`), 18 passed, 9 intentionally skipped, ~19.6s on Node 26.10.0; the runtime spec also passes 6/6 on the Node 24.20.0 baseline image |

## Notes

- **Node 26 parity pass (2026-09-27)**: Node 22.22.2/npm 10.9.7 and Node 26.10.0/npm 11.19.1 were run side by side: `npm ci`, typecheck, format check, Jest (282/282 on both, identical coverage table: 96.56% stmts / 88.23% branch / 82.66% funcs), `next build` (same 39 routes, zero warnings) and Docker E2E all matched. Findings: (1) **zustand <5.0.14 throws on the server under Node 25+**: Node now defines a global `localStorage` accessor that returns `undefined` instead of throwing, so zustand's `persist` default storage stopped falling back and `setState` threw `Cannot read properties of undefined (reading 'setItem')`. `@wagmi/core` (5.0.0) and `@base-org/account` (5.0.3) shipped affected copies, so a `zustand: 5.0.15` npm override now dedupes every copy to a fixed version; `scripts/__tests__/node-runtime.test.js` checks every zustand copy in the lockfile. (2) npm 11 skips 9 dependency install scripts that have no `allowScripts` entry (esbuild, bufferutil, utf-8-validate, @parcel/watcher, unrs-resolver, protobufjs, @reown/appkit); the installed files were byte-identical, and the same test file asserts each native package still loads its prebuilt binary.
- **Bug found and fixed while refreshing these numbers**: `npm run test:e2e:docker` (`config/docker-compose.test.yml`) ran `npx playwright test` with no `--config` flag. Since `config/playwright.config.ts` isn't at the repo root, Playwright silently fell back to zero-config discovery and picked up the `src/**/__tests__/*.test.tsx` Jest files too, which crashed with `ReferenceError: describe is not defined` for every Jest file. Fixed by pointing the compose command at `--config config/playwright.config.ts`.
- **Code Coverage (2026-09-24)**: 97.37% statements / 84.56% branch / 84% functions, 223 tests across 19 suites. Re-run in Docker (`config/Dockerfile.unit`, `npm run test:coverage`, 6.4s). Previous measurement:
- **Code Coverage (2026-09-01)**: 97.21% statements / 81.37% branch / 83.33% functions, measured via Jest coverage report, re-run 2026-09-01 in Docker (`config/Dockerfile.unit`). 214 tests across 17 suites — up from the previously recorded 213/16.
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
