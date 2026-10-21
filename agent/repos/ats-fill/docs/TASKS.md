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

- [x] Fix the home masthead at phone width (journeys review, #142). Done 2026-10-15: standalone masthead stacks under 640px.
  - Priority: P2
  - Problem: at 390px the standalone home masthead (`popup/popup.css:894-902`) keeps its two-column grid, so the intro text is squeezed to one word per line and the stats bar overlaps it.
  - Acceptance Criteria: the masthead stacks under ~640px; the `see-the-home-screen-on-a-phone` journey baseline is regenerated in Docker.

- [x] Rotate the Chrome Web Store OAuth refresh token and re-run the release.
  - Priority: P1
  - Type: Bug · Confidence: High
  - Problem: every `Chrome Web Store Release` run since 2026-09-30 has failed at "Publish". The latest, run #18 ([37741577404](https://github.com/nitsuah/ats-fill/actions/runs/37741577404), 2026-10-08), still logs `OAuth token refresh failed (400): invalid_grant — Token has been expired or revoked`; runs #13–#17 (2026-10-01 to 2026-10-08) failed the same step. The public listing shows **Version 1.0.2, updated October 5, 2026** (checked 2026-10-08), so 1.0.2 reached the store outside this workflow.
  - Why: store users have 1.0.2, but the next release can't be published by the workflow until the token is rotated.
  - Acceptance Criteria: a new refresh token is stored in the production environment secret `CWS_REFRESH_TOKEN`; a `chrome-release.yml` run publishes successfully; the listing's version matches the latest tag (or the item is in review, with the dashboard status noted here).
  - Dependencies: needs the store owner's Google account (a human step; an agent can't do it).
  - Progress 2026-10-14 (stays open until a release publishes): root cause found. `CWS_REFRESH_TOKEN` was set 2026-09-23 22:42 UTC. A run at 09-30 22:15 still authenticated (it failed only on "item is in review"), and every run from 10-01 04:41 got `invalid_grant`: the token died at 7 days, which is Google's limit for refresh tokens of a consent screen in "Testing". Rotating alone would fail again in a week, so set the consent screen to "In production" first, then mint the token with "Use your own OAuth credentials" in OAuth Playground (steps in `docs/release/chrome-web-store.md` → Token health and rotation). The publish script now explains `invalid_grant`, and a weekly **Chrome Web Store token check** workflow catches a dead token before release day.
  - Done 2026-10-14: token re-minted with the consent screen in production; the weekly token check passed 2026-10-14 and 1.0.3 is the published Store version (the 2026-10-15 dispatch runs authenticate and fail only because 1.0.3 is already published, which is the release-cadence item below).
- [x] Fix the release workflow's "Store listing assets" job ("No tests found").
  - Priority: P2
  - Type: Bug · Confidence: Medium
  - Problem: in run #18 (2026-10-08) and the runs before it, the job ran `npx playwright test --config config/playwright.config.mjs tests/e2e/store-assets.spec.mjs` and exited 1 with `Error: No tests found`, though `tests/e2e/store-assets.spec.mjs` exists and `testDir` is `./../tests/e2e`. The root cause hasn't been investigated yet.
  - Acceptance Criteria: the job generates and validates the store assets on a `workflow_dispatch` run.
  - Progress 2026-10-09 (stays open until the acceptance run): root cause was not the Playwright config. `workflow_dispatch` re-ran the job on tag `v1.0.2`, which predates the listing-asset spec and validator (added in #112), so `tests/e2e/store-assets.spec.mjs` did not exist in that checkout. The job now checks the tag for the tooling and skips with a notice when absent; tags cut from this point on generate the assets. Verified in Docker: spec passes on current main (8 assets), and fails with "No tests found" on a `v1.0.2` export. Publish failures stay expected until the CWS refresh token is rotated (separate P1). Close this once a `workflow_dispatch` run on the first tag cut after this fix generates and validates the assets.
  - Done 2026-10-15: the job passes on `workflow_dispatch` from `main` (run 38822129302).
- [ ] Rework how releases reach the Chrome Web Store so they stop queuing behind review.
  - Priority: P2
  - Type: Improvement · Confidence: Medium
  - Problem: every publish goes through Chrome Web Store review, and the project merges often, so releases queue up behind an item still in review (v1.0.3 is in review as of 2026-10-14). Each tag triggers a publish attempt, so a new version can't ship until the pending one clears.
  - Options to evaluate: (a) batch releases on a schedule (e.g. weekly); (b) keep tagging and GitHub Releases on every version, but publish to the Store only from a separate `workflow_dispatch`; (c) skip the publish step while an item is already pending review (the CWS API v2 item status can show this). Pick one or a combination, and note the trade-off between release freshness and review backlog.
  - Related: the `production` environment only allows protected branches, so tag-push runs may be refused (a dispatch from `main` works); `cws-token-check.yml` checks the refresh token weekly.
  - Acceptance Criteria: a decision recorded here (or in `docs/release/chrome-web-store.md`); the release workflow publishes at most one pending review at a time, or only on the chosen schedule; a dispatch from `main` ships a release end to end without a review collision.
  - Found in the 2026-10-14 cross-repo auth audit.

- [x] Show the detected ATS when the application form is embedded in an iframe.
  - Priority: P3
  - Type: Bug · Confidence: High
  - Problem: on company career pages that embed a Greenhouse form (e.g. databricks.com with `job-boards.greenhouse.io/embed/job_app`), Fill works in the iframe but the popup's readiness card says "DETECTED ATS: No job page", because `DETECT_ATS` is answered from the top frame.
  - Same root cause in the tracker: filling the embedded form logged split rows ("Databricks — (no title)" from the iframe and "— Delivery Solutions Architect - Digital Native Business" from the parent page) instead of one entry, so the inbox sync could not tell which Databricks job a confirmation belongs to.
  - Acceptance Criteria: the readiness card names the ATS from the frame that owns the form; an e2e fixture with an embedded Greenhouse iframe covers it, and filling it logs exactly one tracker entry with both company and title.
  - Done 2026-10-16: the host page defers `DETECT_ATS`, `GET_JOB_INFO` and `FILL_FORM` to an embedded ATS form iframe; the embed reads its title from its Remix data and the company from `for`, and records the parent job page as the tracker URL, so a fill logs one entry. Covered by jsdom tests only (no e2e fixture yet).
  - Found 2026-10-16 while battle-testing fill on live forms.

- [ ] Add an opt-in "Full auto" fill mode (attach, fill, then submit) behind its own toggle.
  - Priority: P2
  - Type: Feature · Confidence: Medium
  - Problem: Fill now attaches the saved resume and answers Ashby Yes/No questions, but the user still has to review and press Submit on every application. The owner wants a separate, clearly labelled toggle, off by default, that submits once nothing needs review.
  - Approach: build on the fill report. Submit only when `unresolved` is empty, the resume is attached, the page's required fields are all set, and no legal/attestation or demographic question was answered by ats-fill; otherwise stop and show what needs review. Log every auto-submit to the tracker with the filled answers so it can be audited.
  - Also: keep more than one resume version (today one saved PDF is attached) and pick the version per application.
  - Acceptance Criteria: toggle in Settings, off by default, with a plain warning; journeys cover a form that auto-submits and one that stops for review; the store listing and CHROMEWEBSTORE.md stop saying ats-fill never submits only once this ships.
  - Found 2026-10-16 while battle-testing fill on live Ashby forms (Supabase, Deepgram).

_Other planned work is in `docs/ROADMAP.md` 2027 Q1: OAuth/sign-in for personalized job search (blocked on
a partner API), ID.me identity import, analytics-informed apply suggestions, and the response-time accuracy follow-up._

## Done

_Shipped work is recorded in [FEATURES](./FEATURES.md) (capabilities) and [CHANGELOG](./CHANGELOG.md) (one entry per change)._

## Rejected / Won't Do

_None._
