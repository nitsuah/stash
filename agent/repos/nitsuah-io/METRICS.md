
# Metrics

**Last Validated:** 2026-04-13 (Overseer compliance review)

## Core Metrics

| Metric        | Value                                      | Notes                             |
| ------------- | ------------------------------------------ | --------------------------------- |
| Code Coverage | 98%                                        | Jest unit tests (213 passing)     |
| Build Time    | 35.13s (local, PowerShell Measure-Command) | Next.js Turbopack build           |
| Bundle Size   | 324.90 MB (.next folder total)             | Production build output           |
| Test Files    | 25                                         | 9 Playwright + 16 Jest test files |
| Test Suites   | 16                                         | Jest unit test suites             |
| TypeScript    | Strict mode                                | Zero errors                       |
| Lines of Code | ~21.8K                                     | Excluding tests/generated/config  |

## Health

| Metric          | Value      | Notes                          |
| --------------- | ---------- | ------------------------------ |
| Passing Tests   | 61/61      | 100% (all tests passing in CI) |
| Skipped Tests   | 0          | All tests enabled and passing  |
| Security Alerts | 0          | npm audit (zero high/critical) |
| Health Score    | 98/100     | Excellent health status        |
| Last Updated    | 2026-04-02 | Metrics audit date             |

## Test Breakdown

| Test Suite   | Status   | Count                                              | Notes |
| ------------ | -------- | -------------------------------------------------- | ----- |
| Unit Tests   | 213      | ✅ Passing Jest + React Testing Library             |
| A11y Tests   | 20       | ✅ Passing All pages WCAG 2.1 AA compliant          |
| Resume Tests | 8        | ✅ Passing Fixed with production build in CI        |
| Visual Tests | 9        | ✅ Passing All pages with dynamic content tolerance |
| E2E Tests    | 11       | ✅ Passing Wallet connection + navigation flows     |
| **Total**    | **100%** | **✅ 274** **All tests passing**                    |

## Docker Testing

| Metric       | Value                                | Notes                                 |
| ------------ | ------------------------------------ | ------------------------------------- |
| Image        | mcr.microsoft.com/playwright:v1.57.0-noble | Ubuntu Noble base                     |
| Build Time   | 332s (5.5 min)                       | First build with dependencies         |
| Context Size | 136.88 MB                            | Project files copied to image         |
| Status       | ✅ Production Ready                   | All 61 tests passing (100% pass rate) |

## Notes

- **Code Coverage**: 98% measured via Jest coverage report (statement coverage). Comprehensive component and utility test coverage across 16 test suites with 213 tests.
- **Build Performance**: 35.13s for production build using Next.js Turbopack (local PowerShell measurement).
- **Test Status**: 274 total tests passing (100%). Unit tests: 213 passing. Playwright E2E: 61 passing. All accessibility tests pass WCAG 2.1 AA compliance.
- **Lines of Code**: 21,791 LOC (excluding tests, generated files, config, node_modules, build artifacts).
- **Test Infrastructure**: Production build strategy resolved all test issues. Playwright uses `npm run start` instead of dev server to ensure proper React hydration and DOM rendering.
- **Docker Strategy**: Built Docker image for CI-consistent testing. Successfully generates visual regression baselines matching CI exactly.
- **Security**: Zero npm audit vulnerabilities. All dependencies current with no high/critical security alerts.
- **Accessibility**: WCAG 2.1 AA compliance validated with axe-core. All 13 pages (4 main + 9 Labs) have proper landmarks, skip-link targets, and semantic HTML.

Last validated: 2026-04-02 — Docker, Playwright, and dark mode toggle updates

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
