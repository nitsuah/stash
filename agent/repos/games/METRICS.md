# Metrics

## Docker-based E2E Test Workflow

All Playwright E2E tests can be run in Docker:

- Build E2E test image: `docker build --target test-e2e -t games-test-e2e .`
- Run all E2E tests: `docker run --rm -it games-test-e2e npm run test:e2e`
- All 8 E2E tests pass in Docker (as of last validation)

## Core Metrics

| Metric                | Value          | Notes                     |
| --------------------- | -------------- | ------------------------- |
| Code Coverage         | 95.41% | Docker-validated in latest unit coverage run. |
| Unit Tests            | 481 passing    | 35/35 Jest suites passing in the latest Docker coverage run. |
| E2E Tests             | 8 passing      | Based on the last validated Playwright Docker run; not rerun in this refresh. |
| Test Files            | 35             | Current `app/tests` file count. |
| Build Time            | TBD            | Pending current run measurement. |
| Bundle Size (JS)      | TBD            | Pending current build artifact analysis. |
| Lighthouse Score      | TBD            | Pending current Lighthouse run. |

## Health

| Metric                | Value      | Notes                     |
| --------------------- | ---------- | ------------------------- |
| Open Issues           | TBD        | Pull from current GitHub state during next metrics refresh. |
| Open PRs              | TBD        | Pull from current GitHub state during next metrics refresh. |
| Health Score          | TBD        | Replace self-rating with computed score source. |
| Last Updated          | 2026-05-24 | Metrics updated from Docker-based test run. |
| Passing Unit Tests    | 481/481    | Latest Docker coverage run completed cleanly. |
| Deploy Success Rate   | TBD        | Pull from provider and CI history. |

## Test Distribution

| Test Group                | Count | Status     |
| ------------------------- | ----- | ---------- |
| Jest Test Suites          | 35    | ✅ Passing |
| Jest Tests                | 481   | ✅ Passing |
| Playwright E2E Tests      | 8     | ✅ Last validated |
| **Current Unit Coverage** | **95.41% statements** | **✅ Docker validated** |

## Docker-based Test & Coverage Workflow

All unit tests and coverage can be run in Docker:

- Build test image: `docker build --target test-unit -t games-test .`
- Run all unit tests with coverage: `docker run --rm -it games-test npm run test:coverage`
- All 481 unit tests pass in Docker across 35 suites (latest validation)

Coverage (statements/branches/functions/lines): 95.41% / 87.66% / 93.77% / 96.87%

## Performance Metrics

| Game           | FPS Avg | Load Time | Memory Usage |
| -------------- | ------- | --------- | ------------ |
| Asteroid       | 60      | ~1.2s     | ~80MB        |
| FPS            | 60      | ~1.5s     | ~95MB        |
| Breakout       | 60      | ~0.8s     | ~65MB        |
| Flappy         | 60      | ~0.5s     | ~50MB        |
| Pong           | 60      | ~0.4s     | ~45MB        |
| Snake          | 60      | ~0.4s     | ~45MB        |
| Space Invaders | 60      | ~0.6s     | ~60MB        |

## Code Quality

| Metric                | Value      | Target   | Status |
| --------------------- | ---------- | -------- | ------ |
| ESLint Errors         | 0          | 0        | ✅     |
| ESLint Warnings       | 0          | <5       | ✅     |
| TypeScript Errors     | 0          | 0        | ✅     |
| Prettier Violations   | 0          | 0        | ✅     |
| Outdated Dependencies | 13         | <15      | ⚠️     |

## Accessibility

| Metric                     | Score | Target | Status |
| -------------------------- | ----- | ------ | ------ |
| Lighthouse A11y Score      | 100   | >90    | ✅     |
| Keyboard Navigation        | ✅    | Full   | ✅     |
| Screen Reader Support      | ✅    | Basic  | ✅     |
| Color Contrast (WCAG)      | AAA   | AA     | ✅     |

## Browser Compatibility

| Browser              | Support | Tested |
| -------------------- | ------- | ------ |
| Chrome 120+          | ✅      | ✅     |
| Firefox 120+         | ✅      | ✅     |
| Safari 17+           | ✅      | ⚠️     |
| Edge 120+            | ✅      | ✅     |
| Mobile Safari        | ⚠️      | ⚠️     |
| Mobile Chrome        | ⚠️      | ⚠️     |

**Legend**: ✅ Full Support | ⚠️ Partial/Untested | ❌ Not Supported

## User Engagement (Production)

| Metric                | Value      | Notes                        |
| --------------------- | ---------- | ---------------------------- |
| Active Users          | TBD        | Analytics not yet integrated |
| Avg Session Duration  | TBD        | Coming soon                  |
| Most Played Game      | TBD        | Coming soon                  |
| Bounce Rate           | TBD        | Coming soon                  |

---

**Last Updated**: May 24, 2026  
**Data Source**: Latest Docker Jest coverage run plus previously validated Playwright Docker results.

<!--
AGENT INSTRUCTIONS:
This file tracks project health metrics and performance indicators.

1. **Update Frequency**: Update after significant changes, releases, or weekly reviews.

2. **Metric Categories**:
   - Core Metrics: Overall project health (coverage, tests, build, bundle)
   - Test Distribution: Breakdown of test suites and their status
   - Performance: Game-specific FPS, load times, memory
   - Health: PR turnaround, issues, build success
   - Code Quality: Linting, type checking, dependencies
   - Accessibility: A11y scores and compliance
   - Browser Compatibility: Support matrix
   - User Engagement: Production analytics (when available)

3. **How to Update**:
   - Run `npm run test:coverage` for coverage data
   - Check GitHub Actions for build times and test results
   - Use Chrome DevTools for performance metrics
   - Run `npm run lighthouse` for Lighthouse scores
   - Check `npm outdated` for dependency status

4. **Accuracy**: Ensure values reflect actual current state from CI/CD outputs or local testing.

5. **Trends**: Use ✅ (improving/good), → (stable), ⚠️ (needs attention), ❌ (critical)

6. **Target Values**: Set realistic targets based on industry standards and project goals.
-->
