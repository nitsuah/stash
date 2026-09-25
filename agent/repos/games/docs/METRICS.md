---
up: "[[repos/games]]"
source: https://github.com/nitsuah/games/blob/main/docs/METRICS.md
---

# Metrics

> 🧭 [games](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Docker-based E2E Test Workflow

All Playwright E2E tests can be run in Docker:

- Build E2E test image: `docker build --target test-e2e -t games-test-e2e .`
- Run all E2E tests: `docker run --rm -it games-test-e2e npm run test:e2e`
- All 8 E2E tests pass in Docker (as of last validation)

## Core Metrics

| Metric                | Value          | Notes                     |
| --------------------- | -------------- | ------------------------- |
| Code Coverage | 98.58% | Docker `npm run test:ci` (2026-09-24): statements 98.58%, branches 92.2%, functions 99.06%, lines 99.47%. Coverage now counts `.ts/.tsx` and `contexts/` (3,804 statements, up from 1,096) and includes audio, asteroid UI/weapons and the TS game components; only canvas/R3F render shells are excluded. CI enforces 85% thresholds. |
| Unit Tests | 1017 passing | 71/71 Jest suites pass in Docker (2026-09-24, coverage expansion). |
| E2E Tests             | 8 passing      | Based on the last validated Playwright Docker run; not rerun in this refresh. |
| Test Files            | 71             | Current `app/tests` file count. |
| Build Time            | TBD            | Pending current run measurement. |
| Bundle Size (JS)      | TBD            | Pending current build artifact analysis. |
| Lighthouse Score      | TBD            | Pending current Lighthouse run. |

## Health

| Metric                | Value      | Notes                     |
| --------------------- | ---------- | ------------------------- |
| Open Issues           | TBD        | Pull from current GitHub state during next metrics refresh. |
| Open PRs              | TBD        | Pull from current GitHub state during next metrics refresh. |
| Health Score          | TBD        | Replace self-rating with computed score source. |
| Last Updated | 2026-09-24 | Coverage expanded to TS/audio/UI; Docker unit coverage re-run. |
| Passing Unit Tests | 1017/1017 | All tests pass, and coverage thresholds pass (2026-09-24). |
| Deploy Success Rate   | TBD        | Pull from provider and CI history. |

## Test Distribution

| Test Group                | Count | Status     |
| ------------------------- | ----- | ---------- |
| Jest Test Suites          | 71    | ✅ Passing |
| Jest Tests                | 1017  | ✅ Passing |
| Playwright E2E Tests      | 8     | ✅ Last validated |
| **Current Unit Coverage** | **98.58% statements** | **✅ Above the 85% threshold; Docker `npm run test:ci` exits 0 (2026-09-24)** |

## Docker-based Test & Coverage Workflow

All unit tests and coverage can be run in Docker:

- Build test image: `docker build --target test-unit -t games-test .`
- Run all unit tests with coverage: `docker run --rm -it games-test npm run test:coverage`
- All 1017 unit tests pass in Docker across 71 suites (2026-09-24, latest validation)

Coverage (statements/branches/functions/lines): 98.58% / 92.2% / 99.06% / 99.47% (Docker, 2026-09-24, over 3,804 statements now that `.ts/.tsx`, audio and asteroid UI are counted). _History: 95.34% earlier the same day measured only 1,096 `.js/.jsx` statements._

_History: 61.09% / 59.13% / 80.99% / 62.55% at the 2026-09-24 PMO audit, before the fix, while `TankGame.jsx` was counted untested. It was 95.41% / 87.66% / 93.77% / 96.87% before Tank Battle was added in #284._

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
| Memory Match   | N/A     | ~0.3s     | ~20MB        |
| Dodge Blocks   | 60      | ~0.3s     | ~20MB        |

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

**Last Updated**: September 24, 2026  
**Data Source**: Latest Docker Jest coverage run plus previously validated Playwright Docker results. Performance rows for Memory Match and Dodge Blocks are estimates (iframe-hosted standalone games; FPS column N/A for Memory Match as it is DOM-based).

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
