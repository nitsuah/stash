---
updated: 2026-10-01
up: "[[repos/ats-fill]]"
title: "ats-fill · TASKS"
source: https://github.com/nitsuah/auto-apply-plugin/blob/main/docs/TASKS.md
kind: repo-doc
repo: ats-fill
---

# Tasks

> 🧭 [ats-fill](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

## In Progress

_None._

## Todo

- [ ] Rotate the Chrome Web Store OAuth refresh token and re-run the release.
  - Priority: P1
  - Type: Bug · Confidence: High
  - Problem: the latest `Chrome Web Store Release` run ([36816311174](https://github.com/nitsuah/ats-fill/actions/runs/36816311174), 2026-10-01) failed at "Publish to Chrome Web Store" with `OAuth token refresh failed (400): invalid_grant — Token has been expired or revoked`. The run before it (2026-09-30 22:15) also failed. On 2026-10-01 the public listing still showed **Version 1.0.0**, while `manifest.json` and the `v1.0.2` tag are 1.0.2.
  - Why: no fix since 1.0.0 reaches store users until publishing works again.
  - Acceptance Criteria: a new refresh token is stored in the production environment secret `CWS_REFRESH_TOKEN`; a `chrome-release.yml` run publishes successfully; the listing's version matches the latest tag (or the item is in review, with the dashboard status noted here).
  - Dependencies: needs the store owner's Google account (a human step; an agent can't do it).
- [ ] Fix the release workflow's "Store listing assets" job ("No tests found").
  - Priority: P2
  - Type: Bug · Confidence: Medium
  - Problem: in the same run, the job ran `npx playwright test --config config/playwright.config.mjs tests/e2e/store-assets.spec.mjs` and exited 1 with `Error: No tests found`, though `tests/e2e/store-assets.spec.mjs` exists and `testDir` is `./../tests/e2e`. The root cause wasn't investigated in the 2026-10-01 PMO audit (TBD).
  - Acceptance Criteria: the job generates and validates the store assets on a `workflow_dispatch` run.

_Other planned work is in `docs/ROADMAP.md` 2027 Q1: OAuth/sign-in for personalized job search (blocked on
a partner API), ID.me identity import, analytics-informed apply suggestions, and the response-time accuracy follow-up._

## Done

_Shipped work is recorded in [FEATURES](./FEATURES.md) (capabilities) and [CHANGELOG](./CHANGELOG.md) (one entry per change)._

## Rejected / Won't Do

_None._
