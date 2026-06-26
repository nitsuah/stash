# Testing Guide

## Overview

This repo uses a split strategy:

- Fast, deterministic checks in required CI
- Browser-heavy Playwright coverage in manual/nightly workflow
- Docker-first local verification for CI parity

## Test Types

### 1. Unit Tests (Jest + React Testing Library)
- **What:** Component logic, utility functions, hooks
- **When:** Development, pre-commit, pre-push, CI Fast
- **Command:** `npm test`

### 2. Playwright Smoke (deterministic)
- **What:** Route/HTML smoke checks in `tests/smoke.spec.ts`
- **When:** CI Fast + local
- **Command:** `npm run test:smoke`

### 3. Playwright Browser/A11y (full browser)
- **What:** Browser navigation + accessibility checks
- **When:** Local runs, Playwright Nightly workflow, manual dispatch
- **Commands:** `npm run test:e2e`, `npm run test:a11y`

## Precheck Workflow

Run this before pushing significant changes:

```bash
npm run precheck:docker
```

What it does:
1. Builds/refreshes the Playwright Docker image (`npm run test:e2e:docker:build`)
2. Runs the Playwright suite in Docker (`npm run test:e2e:docker`)

## Manual Commands

```bash
# Recommended path (Docker-first)
npm run precheck:docker

# Unit tests
npm test
npm run test:watch
npm run test:coverage

# Playwright
npm run build:skip-wagmi
npm run test:e2e
npm run test:e2e:ui
npm run test:e2e:headed

# Smoke and accessibility
npm run test:smoke
npm run test:a11y
npm run test:a11y:quick

# Docker
npm run test:e2e:docker:build
npm run test:e2e:docker
```

## CI Workflows

### CI Fast (`.github/workflows/ci.yml`)
- `build-and-test`: typecheck, lint, unit tests, build
- `security-scan`: npm audit
- `lighthouse-check`: PR performance audit

### Playwright Nightly (`.github/workflows/playwright-nightly.yml`)
- Scheduled + manual browser run
- Uses `FORCE_BROWSER_E2E=1` to run browser-gated tests in CI context

## Git Hooks

### Pre-commit (`.husky/pre-commit`)
- `npm run typecheck`
- `npm run lint`
- `lint-staged` (auto-format/fix)
- `npm test`

### Pre-push (`.husky/pre-push`)
- `npm run typecheck`
- `npm test`
- E2E is intentionally skipped here; run `npm run precheck:docker` manually when needed

Bypass hooks only when necessary:

```bash
git commit --no-verify
git push --no-verify
```

## Troubleshooting

### Playwright fails locally

```bash
npm run precheck:docker
```

### Need CI-like isolation

```bash
npm run precheck:docker
```

### `.next` missing

```bash
npm run build:skip-wagmi
npm run test:e2e
```

## Resources

- [Playwright Docs](https://playwright.dev)
- [Jest Docs](https://jestjs.io)
- [Testing Library](https://testing-library.com)
- [axe-core](https://github.com/dequelabs/axe-core)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
