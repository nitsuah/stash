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

### Changed

- **Drone Cursor**: Hover offset moved further up-and-right of the pointer.
- **Docker Compose**: Fixed a relative-path resolution bug in `config/docker-compose.yml` that broke the documented `docker compose -f config/docker-compose.yml run --rm unit` / `up --build web` commands when invoked from the repo root.
- **Documentation**: Refreshed `ROADMAP.md`, `TASKS.md`, `FEATURES.md` for the 2026-09 cycle; archived stale docs into `docs/archive/` (see that directory's README for what moved and why). `METRICS.md` is still stale (last validated 2026-05-24) — not part of this refresh.

### Security

- **Dependencies**: `netlify-cli` upgraded to remove an `extract-zip` vulnerability (PR #120).

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
