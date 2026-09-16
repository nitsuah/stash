# auto-apply-plugin

> Reviewed: 2026-09-11

## Overview

"Apply Workspace" — Chrome MV3 extension for local-first AI-assisted job applications. Stores profile locally, detects ATS forms, reads JDs from the page, generates tailored answers via user's own Gemini API key, and requires review before form fill. Zero server, zero subscription.

## Current Goals / Roadmap Focus

**2026 Q1–Q4: complete.** Job-workspace popup redesign, `apply-bot` → "Apply Workspace" rebrand, multi-source job search (16 sources + custom RSS), Google + LinkedIn OAuth profile import, application analytics panel, interview prep mode, and the a11y/axe audit all shipped — see FEATURES.md.

**2027 Q1 (proposed):**
- [ ] OAuth / sign-in for *personalized* job search — blocked on a partner API (LinkedIn job-search API is enterprise-partner-gated; Indeed's public API doesn't personalize per-user)
- [ ] ID.me identity import (split out from the Google/LinkedIn profile-import work; needs its own consent/design pass — KYC-style flow, not standard OIDC)
- [ ] Analytics-informed apply suggestions (surface a one-line nudge on tracker cards from existing analytics aggregation)
- [ ] Response-time accuracy follow-up (backfill or badge pre-`first_response_at` analytics entries as approximate)

## Open P0/P1 Tasks

- [ ] **P1** — OAuth / sign-in for personalized job search (deferred to 2027 Q1; blocked on partner API availability — no currently-integrated board exposes a consumer OAuth job-search/personalization endpoint)

No other open P1 items — all Q2–Q4 2026 roadmap goals (popup redesign, rebrand, job search expansion, analytics, interview prep, a11y audit) shipped and are marked done in TASKS.md.

## Blockers

- OAuth job search personalization — LinkedIn's job-search API is partner-gated, Indeed's public API doesn't personalize; scraping/aggregation remains the current path (see 2027 Q1 above)
- Google OAuth redirect-URI mismatch unresolved — `launchWebAuthFlow` produces a `chromiumapp.org` redirect incompatible with the documented Desktop-app Google client type; needs a decision on client type/redirect strategy (`lib/oauth.js:55-57`, `background/service-worker.js:344-346`), flagged by CodeRabbit as a functional-correctness issue (P2, not blocking core autofill)

## Recent Changes (Unreleased)

- Custom user-configured RSS job sources (state workforce boards, internal careers feeds) with per-origin permission requests
- Google OAuth profile import, generalizing the existing LinkedIn BYO-OAuth flow to a second provider
- Application analytics panel — response rate by source, salary-band effectiveness, time-to-first-response distribution (PR #57)
- Interview prep mode — Gemini-backed interview questions and suggested answers from a saved tracker card's JD and profile
- Hackajob job-search source (sitemap + JSON-LD scraping, no public API)
- Tracker module split into focused files under `popup/tracker/`
- CSV import support for tracker history
- ATS receiver auto-recovery path (retries content-script injection)
- Memory controls: edit, ignore, restore, remove
- Fixed: two tracker storage gaps that limited analytics accuracy — `job.source` was silently dropped on save, and no first-response timestamp existed (added sticky `first_response_at`)
