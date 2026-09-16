
# Tasks

**Last Updated:** 2026-09-11

> **Delivery split:** public FE covers the marketing site and funnel. `/admin` is a separate CMS surface. Secure client portal/download auth is a separate backend workstream.

## Done (2026-09 cycle)

- [x] Server-side client-portal token validation — HMAC-SHA256, mandatory `PORTAL_SALT`, fail-closed. See `netlify/functions/api-portal.mjs`, `netlify/functions/utils/portal.js`. Was the top half of "Build secure client delivery backend"; the remaining half (signed file delivery for `client-gallery.html`) is the entry directly below.
- [x] Build secure client delivery backend (file delivery half). `netlify/functions/utils/portal.js` gained `generateSessionToken`/`verifySessionToken` (1-hour, domain-separated `sess.` tokens, HMAC-SHA256/PORTAL_SALT, fail-closed) and `generateSignedDownloadToken`/`verifySignedDownloadToken` (5-minute, single-file-scoped `dl.` tokens) plus `logPortalAccess()`. `api-portal.mjs` now exchanges a valid access code for a session token in `/verify`, and adds `/files` (session-gated manifest fetch, `netlify/functions/utils/portal-manifest.js`), `/download` (mints a signed link), and `/file` (verifies the signed link, 302s to the real asset). CWE-598 fix (PR #121, CodeRabbit, 2026-09-10): `client-portal.html` now redirects to the gallery via URL fragment (`#session=<token>`), never a query param, and the gallery reads it once, scrubs it from the address bar via `history.replaceState`, and caches it in `sessionStorage` for the tab; the original 30-day access code is never reused after login. `client-gallery.html` fully rebuilt to fetch the manifest and download links from the server instead of hardcoded/mock data. Unit tests added in `tests/unit/portal-token.test.js`; `tests/drone-and-portal.spec.ts` updated to mock `/api/portal/files` and assert no `code=`/`session=` ever appears in the gallery URL. Still open: the manifest itself is a single shared demo manifest, not a real per-client storage backend, and bulk ZIP download remains a placeholder — see `docs/CLIENT_PORTAL.md`. Also flagged by CodeRabbit on PR #131 (2026-09-11): today's demo files live under `/assets/gallery`, the site's own public marketing gallery (already served statically with no auth), so the signed-link flow doesn't yet demonstrate real access control end-to-end — a real per-client store must serve files that live outside any statically-published directory, read as bytes (or via a private-bucket presigned URL) rather than a redirect to a public path.
- [x] Drone cursor hover offset (up-and-right of pointer) + transparent spotlight/laser beam from drone to cursor — `scripts/drone-cursor.js`, `styles/style.css`.
- [x] Marketplace platform SPA now built and served by the Docker preview (`Dockerfile`, `config/nginx.conf`) — previously only the Netlify build produced `/app`.
- [x] Identity data config plumbing — `config.js` `contact.address`, `contact.geo`, and `contact.social.facebook` added and wired into the schema.org JSON-LD via `updateStructuredData()`, so populating real values is a single-place edit. See P1 item below for what's still needed from the client.
- [x] Fixed `config/docker-compose.yml` relative-path bug that broke the documented `docker compose -f config/docker-compose.yml run --rm unit` / `... up --build web` commands when run from the repo root (relative paths were resolving against `config/`, not the repo root).
- [x] Fixed Vitest 5 regression (dependabot PR #127, `@vitest/coverage-v8` 4→5) that broke 4 test files: `window.pageYOffset`/`window.scrollY` became getter-only in Vitest 5's jsdom/happy-dom environment, so direct assignment (`window.pageYOffset = X`) silently no-oped instead of throwing, making scroll-dependent assertions fail. Switched to `vi.stubGlobal('pageYOffset', X)` (auto-restored, works regardless of whether the property is a getter) across `tests/unit/{integration,smooth-scroll,ui}.test.js`. Also fixed a related ordering bug in `performance-monitor.test.js`: `delete global.performance` before the dynamic `import()` broke Vitest's own module-transform instrumentation (which calls `performance.now()` internally); reordered to import first, then `vi.stubGlobal('performance', undefined)` only around the function call under test. All 103 tests passing.

## In Progress

- [ ] Complete the launch checklist with verified production identity data.
  - Priority: P1
  - Blocker: config plumbing is done (see Done above) — this is now purely a data-entry task blocked on the business owner supplying real values. Specifically still needed: **real business phone number**, **real business email** (confirm if `contact@skyviewdynamics.com` is real or a placeholder), **service-area city/region** (or full street address) for `contact.address` in `config.js`, **approximate service-area GPS coordinates** for `contact.geo`, and **real social profile URLs** for `contact.social` (facebook/twitter/instagram/youtube — currently generic homepage URLs, not the business's actual profiles).
  - Acceptance Criteria: production identity fields populated in `config.js`; no placeholder values remain in the rendered page or schema.org JSON-LD; `/admin` invite-only; separation documented.

## Todo

- [ ] Activate marketplace platform in production (Calendly cutover). See ROADMAP.md "Marketplace Platform / Calendly Cutover" for full context.
  - Priority: P2
  - Acceptance Criteria: `db:migrate` run against production Neon DB; Stripe/Resend/JWT/PORTAL_SALT env vars set in Netlify; `features.platform: true` in `config.js`; Calendly script/CSP removed once verified working end-to-end.

## Maintenance

- [ ] Activate analytics provider (Plausible or Netlify Analytics) and set conversion goals.
  - Priority: P2
  - Acceptance Criteria: page view, booking, and contact-form events tracked in dashboard.

- [ ] Enable testimonials section once real client reviews are collected.
  - Priority: P3
  - Acceptance Criteria: `testimonials: true` in config.js; at least 3 verified reviews displayed.

- [ ] Activate A/B experiments.
  - Priority: P3
  - Acceptance Criteria: `experiments.enabled: true` in config.js; variant assignment wired to analytics; results analysed after 2 weeks.

- [ ] Dependency audit and update.
  - Priority: P3
  - Progress: netlify-cli upgraded (extract-zip vulnerability fix, PR #120, 2026-09-02).
  - Acceptance Criteria: `npm audit` clean; Playwright, Vitest, and netlify-cli on latest minor versions.
