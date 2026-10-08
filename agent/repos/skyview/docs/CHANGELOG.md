---
up: "[[repos/skyview]]"
title: "skyview · CHANGELOG"
source: https://github.com/nitsuah/skyview/blob/main/docs/CHANGELOG.md
kind: repo-doc
repo: skyview
---

# Changelog

> 🧭 [skyview](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](../METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 2026-10-08

- **Changed — Playwright CI install hardened:** `playwright.yml` installs only Chromium (the only project in `config/playwright.config.ts`) instead of all three browsers, caches `~/.cache/ms-playwright` per Playwright version, caps each install attempt at 4 minutes with up to 3 retries, and lowers the job timeout from 60 to 30 minutes. On 2026-10-07 an apt mirror stall in `playwright install --with-deps` hung the stripe 23 PR's run for the full hour. Also `npm install` → `npm ci` with npm caching.

### 2026-10-07 — Visual showcase

- **Added:** Visual showcase ([standard](https://github.com/nitsuah/.github/blob/main/showcase/STANDARD.md)): `promo/spots.json` lists every shipped FEATURES.md entry and records the existing launch video(s); feature-to-video and screenshot links are still empty and get filled in on the next `/promo` run; the Pages site loads the shared expand kit (click-to-expand images, fullscreen button on videos). `og:image` is now an absolute URL so link previews unfurl.

### 2026-10-07

- **Added — unit tests in CI:** `.github/workflows/unit-tests.yml` runs `npm run test:unit` (Vitest) on Node 22 for every PR and push to `main`. Until now only Playwright (`test`) and the Docker smoke ran in CI, so unit tests, including the booking/billing suite, ran only locally.
- **Added — booking payment tests (F-20260916-06):** `tests/unit/api-bookings.test.js` runs the `/api/bookings` handler with `sql`, auth, email, scheduling and Stripe mocked (40 tests). It covers create (validation, verified operator, availability, double-booking gate, overlap constraint, PaymentIntent create, rollback + 502 on Stripe failure), confirm (no Stripe call), decline (PaymentIntent cancel; a cancel failure stays non-fatal) and complete (capture before the job update, `disputed` on capture failure, Connect transfer + invoice, `payout_status` `failed` on payout/invoice errors), plus the no-Stripe mode.
- **Changed — billing split out of `api-bookings.mjs`:** fee split, PaymentIntent authorize/release/capture and `payoutAndInvoice` moved to `netlify/functions/utils/booking-billing.js`; the handler (375 → 292 lines) keeps routing and booking/job state transitions. Route contracts are unchanged and the same tests pass before and after.

### 2026-10-01

- **Added — GitHub Pages showcase:** `showcase/` is a static project page (launch reel, how-it-works flow, gallery, feature overview) deployed by `.github/workflows/pages.yml` on pushes to `main` that touch `showcase/**`. Includes a 21-second launch video (`showcase/media/skyview-launch.mp4`) built from the real site hero and platform UI.

### 2026-09-26

- **Verified — production auth/env:** `DATABASE_URL`, `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`, `JWT_SECRET`, `RESEND_API_KEY` and `STRIPE_SECRET_KEY` are set in Netlify for all deploy contexts, and a real "Continue with Google" sign-in works on production, so the Google redirect URI is registered. The Resend sender domain and the password-reset email moved to a new task, blocked on the DNS/domain decision.

### 2026-09-19 → 2026-09-24

- **Changed — Calendly cutover:** the marketing site no longer uses Calendly. The booking section links into the marketplace platform ("Find a drone operator" / "Post a job" / "List as an operator"), the hero CTA goes to `/app/register`, and the Calendly widget, script, CSP entries, config, CSS and `features.platform`/`features.calendly` flags were removed; the unfinished testimonials and 3D preview sections were removed from the markup.
- **Changed:** `CHANGELOG.md`/`FEATURES.md` moved into `docs/` (#147); pre-commit and Playwright configs moved into `config/` (#148); `docs/archive` reconciled with the live setup docs (#149); METRICS refreshed from a Docker unit/coverage run (#146).
- **Dependencies:** netlify-cli 27.8.0 (#141), @vitest/coverage-v8 5.0.1 (#142), @netlify/blobs 11.1.0 (#143), resend 6.28.1 (#144).
- **Docs:** planning docs reset for 2027 (`pmo-ff`) — completed roadmap sections condensed into FEATURES (new Marketplace Platform section), open 2026 items merged into 2027 Q1, broken `docs/`-relative links in OWNER_GUIDE/DEPLOYMENT_GUIDE/README fixed, breadcrumb navigation + README docs index added.


### Added

- **Client Portal**: Server-side access-code verification (`netlify/functions/api-portal.mjs`) using HMAC-SHA256 with a mandatory `PORTAL_SALT` secret and fail-closed behavior — replaces the previous client-only length check.
- **Drone Cursor**: Transparent spotlight/laser beam rendered from the drone to the pointer.
- **Docker**: `Dockerfile` is now a multi-stage build that runs `scripts/build.js`, so the local Docker preview serves the marketplace platform SPA at `/app` (via `config/nginx.conf` SPA fallback), matching the Netlify production build.
- **Identity Config**: `config.js` `contact.address`, `contact.geo`, and `contact.social.facebook` — schema.org JSON-LD now reflects these via `updateStructuredData()`.
- **Native Operator Scheduling**: `operator_availability`/`operator_blocked_dates` (migration `006_operator_availability.sql`) and `checkOperatorAvailability()` (`netlify/functions/utils/scheduling.js`), enforced on booking creation and confirmation with a DB exclusion constraint (`bookings_no_operator_overlap`) against overlapping bookings; `OperatorOnboarding.jsx` gained a weekly-hours + blocked-dates step, `OperatorProfile.jsx`'s booking modal now proposes and sends a real `scheduled_at`/`duration_hours`.
- **Signed Client-Portal File Delivery**: `generateSessionToken`/`verifySessionToken` (1-hour, HMAC-SHA256) and `generateSignedDownloadToken`/`verifySignedDownloadToken` (5-minute, single-file-scoped) in `netlify/functions/utils/portal.js`; `api-portal.mjs` exchanges an access code for a session token and adds `/files`, `/download`, `/file` endpoints; `client-gallery.html` rebuilt to fetch the manifest/download links from the server instead of mock data.

### Changed

- Agent instructions (`.github/copilot-instructions.md`) now require closing tracked work in the same PR: update `docs/TASKS.md`, `docs/ROADMAP.md` and this changelog before the last push, and confirm `git diff origin/main...HEAD --stat` includes them before merge; added `.github/pull_request_template.md` with a "Closes TASKS item(s)" checklist.
- **Drone Cursor**: Hover offset moved further up-and-right of the pointer.
- **Docker Compose**: Fixed a relative-path resolution bug in `config/docker-compose.yml` that broke the documented `docker compose -f config/docker-compose.yml run --rm unit` / `up --build web` commands when invoked from the repo root.
- **Documentation**: Refreshed `ROADMAP.md`, `TASKS.md`, `FEATURES.md` for the 2026-09 cycle; archived stale docs into `docs/archive/` (see that directory's README for what moved and why). `METRICS.md` was subsequently revalidated 2026-09-18 (native `npx vitest run --coverage`).

### Security

- **Dependencies**: `netlify-cli` upgraded to remove an `extract-zip` vulnerability (PR #120).
- **Client Portal (CWE-598)**: `client-portal.html` now redirects to the gallery via a URL fragment (`#session=<token>`), never a query param; the gallery reads it once, scrubs it from the address bar via `history.replaceState`, and caches it in `sessionStorage` for the tab, so the original access code is never reused after login (PR #121, CodeRabbit).

### Fixed

- **Vitest 5 regression** (dependabot PR #127, `@vitest/coverage-v8` 4→5): `window.pageYOffset`/`window.scrollY` became getter-only in Vitest 5's jsdom/happy-dom environment, silently no-oping direct assignment in scroll-dependent tests; switched to `vi.stubGlobal`. Also fixed a related ordering bug in `performance-monitor.test.js` where `delete global.performance` before a dynamic `import()` broke Vitest's own module-transform instrumentation.

## [0.1.0] - In Progress

### Added
- **Dynamic Gallery**: Implemented `gallery-loader.js` to fetch images from `assets/gallery.json`.
- **E2E Testing**: Added Playwright tests (`tests/site.spec.ts`) covering critical paths.
- **Admin Panel**: Added Decap CMS (`admin/`) for managing gallery assets without code.
- **Documentation**: Added `docs/ASSET_MANAGEMENT.md`.

### Changed
- **Services**: Updated service cards with real-world offerings (Real Estate, Cinematography, Mapping).
- **Contact Form**: Configured for Netlify Forms (`data-netlify="true"`).
- **Structure**: Gallery is now rendered dynamically on page load.
- **Infrastructure**: Replaced incorrect Dockerfile and removed confused linter/test configs. Added `stylelint.config.mjs` and correct valid `Dockerfile` for static serving.
