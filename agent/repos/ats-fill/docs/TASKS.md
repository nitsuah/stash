---
updated: 2026-10-08
up: "[[repos/ats-fill]]"
title: "ats-fill · TASKS"
source: https://github.com/nitsuah/ats-fill/blob/main/docs/TASKS.md
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
  - Problem: every `Chrome Web Store Release` run since 2026-09-30 has failed at "Publish". The latest, run #18 ([37741577404](https://github.com/nitsuah/ats-fill/actions/runs/37741577404), 2026-10-08), still logs `OAuth token refresh failed (400): invalid_grant — Token has been expired or revoked`; runs #13–#17 (2026-10-01 to 2026-10-08) failed the same step. The public listing shows **Version 1.0.2, updated October 5, 2026** (checked 2026-10-08), so 1.0.2 reached the store outside this workflow.
  - Why: store users have 1.0.2, but the next release can't be published by the workflow until the token is rotated.
  - Acceptance Criteria: a new refresh token is stored in the production environment secret `CWS_REFRESH_TOKEN`; a `chrome-release.yml` run publishes successfully; the listing's version matches the latest tag (or the item is in review, with the dashboard status noted here).
  - Dependencies: needs the store owner's Google account (a human step; an agent can't do it).
- [/] Fix the release workflow's "Store listing assets" job ("No tests found").
  - Priority: P2
  - Type: Bug · Confidence: Medium
  - Problem: in run #18 (2026-10-08) and the runs before it, the job ran `npx playwright test --config config/playwright.config.mjs tests/e2e/store-assets.spec.mjs` and exited 1 with `Error: No tests found`, though `tests/e2e/store-assets.spec.mjs` exists and `testDir` is `./../tests/e2e`. The root cause hasn't been investigated yet.
  - Acceptance Criteria: the job generates and validates the store assets on a `workflow_dispatch` run.
  - Progress 2026-10-09 (stays open until the acceptance run): root cause was not the Playwright config. `workflow_dispatch` re-ran the job on tag `v1.0.2`, which predates the listing-asset spec and validator (added in #112), so `tests/e2e/store-assets.spec.mjs` did not exist in that checkout. The job now checks the tag for the tooling and skips with a notice when absent; tags cut from this point on generate the assets. Verified in Docker: spec passes on current main (8 assets), and fails with "No tests found" on a `v1.0.2` export. Publish failures stay expected until the CWS refresh token is rotated (separate P1). Close this once a `workflow_dispatch` run on the first tag cut after this fix generates and validates the assets.

_Other planned work is in `docs/ROADMAP.md` 2027 Q1: OAuth/sign-in for personalized job search (blocked on
a partner API), ID.me identity import, analytics-informed apply suggestions, and the response-time accuracy follow-up._

## Done

_Shipped work is recorded in [FEATURES](./FEATURES.md) (capabilities) and [CHANGELOG](./CHANGELOG.md) (one entry per change)._

## Rejected / Won't Do

_None._
