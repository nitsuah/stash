# Playwright Stability Notes

## Current Strategy

Playwright is split into two paths:

1. **CI Fast** (`.github/workflows/ci.yml`)
	- Keeps deterministic checks required for PR merge
	- Avoids long-running flaky browser assertions in required CI

2. **Playwright Nightly** (`.github/workflows/playwright-nightly.yml`)
	- Runs full browser suite on schedule or manual dispatch
	- Uses `FORCE_BROWSER_E2E=1` to enable browser-gated tests in CI context

## Why this changed

Previous CI behavior had repeated long Playwright hangs and flaky failures
driven by browser timing and frame-detachment issues. The current split keeps
required CI reliable while retaining deeper browser coverage in nightly runs.

## Current test entry points

- Smoke checks: `tests/smoke.spec.ts`
- Accessibility checks: `tests/accessibility/critical.spec.ts`
- Browser navigation checks: `tests/e2e/labs/navigation.spec.ts`
- Wallet flow (already intentionally skipped where appropriate):
  `tests/e2e/labs/wallet-connection.spec.ts`

## Useful commands

```powershell
# Full Playwright local run
npm run test:e2e

# Smoke only
npm run test:smoke

# Accessibility only
npm run test:a11y

# CI-like local pass
npm run precheck

# Docker isolation
npm run precheck:docker
```

## Historical note

If you see references to removed specs (for example `tests/visual/*` or
`tests/accessibility/all-pages.spec.ts`) in older discussions, treat them as
legacy context from the pre-split CI approach.
