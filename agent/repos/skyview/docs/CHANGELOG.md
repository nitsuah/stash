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

### Fixed

- `docs/PERFORMANCE_CHECKLIST.md` no longer contains a committed stash-conflict block; its Related links point at the Lighthouse reports and Deployment Guide.
- Signed-in platform pages fit a phone width: the sidebar nav wraps, so "Sign out" and the dashboard actions stay on screen (#189).
- `/pages/privacy.html` loads the shared site script as a module, so the mobile menu and tracking initialise again (#190).

### 2026-10-14 — Nightly journeys

- **Added — `tests/journeys/` and `.github/workflows/journeys.yml`:** 9 journeys (landing hero to gallery, phone layout, conversion dashboard, portal expiry and lockout, marketplace dashboard and operators, post a job, book an operator, operator availability) with 15 visual baselines, tagged with the feature ids in `promo/spots.json`. Backend-free (mocked `/api`, frozen clock, fictional demo data). The nightly caller uses the shared `nitsuah/.github` harness, so failures become deduplicated `bot:journey` issues with no AI. `npm run test:journeys`; the existing e2e config ignores `tests/journeys`.
- **Found:** the one-time review pass filed #189 (platform pages scroll sideways at phone width) and #190 (privacy page loads `main.js` as a classic script).

### 2026-10-14 — Promo spots published

- **Added — showcase videos:** published `site-14s`, `portal-12s` and the `hero-30s` hero cut to `showcase/media/`, plus a new narrated 9:16 short `hero-30s-vert` (29.8 s, Kokoro voice, burned-in captions). `promo/pipeline.sh` mixes a spot's `vo/*.wav` over the music; `promo/tts/` holds the narration script (reuses vigil's `vigil-promo-tts` image).

### 2026-10-14 — Removed dead Netlify Identity / Decap CMS login

- **Removed — `/admin` CMS login:** Netlify Identity is not enabled on the site (`/.netlify/identity/settings` returns 404), so the Decap CMS `/admin` login could never work. Removed `admin/` (Decap config and UI), the Identity widget script in `index.html`, the unused `adminCMS` flag in `config.js`, the `/admin/*` CSP block in `netlify.toml`, and `https://identity.netlify.com` from the remaining CSP. Gallery content stays in `assets/gallery.json` and is edited directly.
- **Removed — CMS docs and capture:** `docs/CMS_GUIDE.md`, the Decap screenshot and its visual-docs capture; README, setup, deployment, owner and asset docs no longer describe Identity or Decap.
- **Unchanged:** Google sign-in and JWT auth in `netlify/functions` are untouched. `robots.txt` still disallows `/admin/` so the SPA fallback page is not indexed there.

### 2026-10-10 — Visual docs

- **Added — screenshots and diagrams from CI:** `.github/workflows/visual-docs.yml` runs a backend-free Playwright suite (`tests/visual-docs/`, `config/playwright.visual-docs.config.ts`: mocked `/api`, frozen clock, fictional demo data) and renders `docs/diagrams/*.mmd`, then opens a `bot/visual-docs` PR. 14 screenshots in `docs/screenshots/`, named after the feature ids in `promo/spots.json`, plus `architecture` and `booking-flow` diagrams. Screenshots are written through `toHaveScreenshot` with a small tolerance, so a file changes only when the UI does. The README has a generated "Screenshots & diagrams" block (`scripts/visual-docs-readme.mjs`).
- **Changed — Pages showcase:** one short page about the booking flow: post a job with where and when, pilots whose coverage radius includes it see it, book a time they are free. The 18 s `book-18s` spot is the hero video and three CI screenshots illustrate the steps; Twitter/`og:video` tags and links back to README, Features, Roadmap and Changelog. `pages.yml` copies `docs/screenshots` and `docs/diagrams` into the site at deploy time and redeploys when they change. The old gallery stills and launch reel are removed from `showcase/media/`.
- **Fixed — Pages links:** the showcase linked to `skyview.nitsuah.io`, which no longer resolves; its links now go to `https://skyviewd.netlify.app`.
- **Added — promo spots:** `promo/build.sh <spot>` renders a spot in Docker from one composition (`promo/hero-30s/compose.html`) built on the CI screenshots. Three feature spots (`site-14s`, `book-18s`, `portal-12s`) and one 30 s hero cut replace the 21 s launch reel, whose outro pointed at the dead domain and whose source was never committed. Only `book-18s` is on the page; the others stay renderable. See `promo/README.md`.
- **Changed — `promo/spots.json`:** 11 of the 13 user-visible features have screenshots; 11 entries are marked `"visual": "none"` (headers, tooling, removed or gated features) with a note each; each spot lists the features it shows.

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
