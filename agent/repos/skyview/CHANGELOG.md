# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Client Portal**: Server-side access-code verification (`netlify/functions/api-portal.mjs`) using HMAC-SHA256 with a mandatory `PORTAL_SALT` secret and fail-closed behavior — replaces the previous client-only length check.
- **Drone Cursor**: Transparent spotlight/laser beam rendered from the drone to the pointer.
- **Docker**: `Dockerfile` is now a multi-stage build that runs `scripts/build.js`, so the local Docker preview serves the marketplace platform SPA at `/app` (via `config/nginx.conf` SPA fallback), matching the Netlify production build.
- **Identity Config**: `config.js` `contact.address`, `contact.geo`, and `contact.social.facebook` — schema.org JSON-LD now reflects these via `updateStructuredData()`.
- **Native Operator Scheduling**: `operator_availability`/`operator_blocked_dates` (migration `006_operator_availability.sql`) and `checkOperatorAvailability()` (`netlify/functions/utils/scheduling.js`), enforced on booking creation and confirmation with a DB exclusion constraint (`bookings_no_operator_overlap`) against overlapping bookings; `OperatorOnboarding.jsx` gained a weekly-hours + blocked-dates step, `OperatorProfile.jsx`'s booking modal now proposes and sends a real `scheduled_at`/`duration_hours`.
- **Signed Client-Portal File Delivery**: `generateSessionToken`/`verifySessionToken` (1-hour, HMAC-SHA256) and `generateSignedDownloadToken`/`verifySignedDownloadToken` (5-minute, single-file-scoped) in `netlify/functions/utils/portal.js`; `api-portal.mjs` exchanges an access code for a session token and adds `/files`, `/download`, `/file` endpoints; `client-gallery.html` rebuilt to fetch the manifest/download links from the server instead of mock data.

### Changed

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
