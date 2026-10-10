---
kind: repo-hub
repo: skyview
---

# skyview - Static marketing site and client portal

**Last Validated:** 2026-10-10 | PMO audit - Docker-first validation
**Repo:** https://github.com/nitsuah/skyview
**Branch convention:** pmo/skyview/planning-alignment-YYYY-MM-DD

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | PASS | Nginx static image builds successfully |
| Container runtime | PASS | HTTP 200 observed from container on localhost |
| Docs baseline | PASS | Core planning and governance docs are present |

---

## Stack

- Static HTML/CSS/JavaScript site with modular scripts
- Netlify deployment model + Decap CMS admin flow
- Playwright E2E and Vitest unit test setup

---

## PMO Findings

- Client-portal login gate is now server-verified this cycle: `netlify/functions/api-portal.mjs` validates access codes via HMAC-SHA256 (mandatory `PORTAL_SALT`, fail-closed — 503 if unconfigured). The remaining half — signed file delivery for `client-gallery.html` — is still a client-side prototype and stays open as P2.
- CodeRabbit's CWE-598 finding (PR #121, 2026-09-10 — portal access token traveling in the URL query string) is now fixed: `client-portal.html` redirects to the gallery via URL fragment (`#session=<token>`), never a query param, scrubbed from the address bar via `history.replaceState` and cached in `sessionStorage` for the tab; the original access code is never reused after login.
- Follow-on finding from CodeRabbit on PR #131 (2026-09-11, still open): today's demo files live under `/assets/gallery`, the site's own public marketing gallery (already served statically with no auth) — so the signed-link flow doesn't yet demonstrate real access control end-to-end. A real per-client store needs to serve files that live outside any statically-published directory (read as bytes, or via a private-bucket presigned URL) rather than redirecting to a public path.
- Marketplace platform SPA is now built and served by the Docker preview image (previously Docker-only previews never included `/app`), matching the Netlify production build.
- Launch is blocked purely on a data-entry task: real business phone/email, service-area address/geo, and real social profile URLs — no code work remaining for that item (P1).

- PMO 2026-10-01: `netlify/functions/api-bookings.mjs` (375 LOC, the Stripe create/cancel/capture paths) is run by no test: e2e specs stub `/api/bookings` via `page.route`. Covered under TASKS.md "Native scheduling hardening" P2 — needs Neon-branch (or driver-compatible proxy) integration test before live-Stripe cutover ([skyview#164](https://github.com/nitsuah/skyview/pull/164)).

---

## Open P0/P1 Tasks

**P1:** Complete the launch checklist with verified production identity data (real phone, email, address/geo, social URLs) — config plumbing is done; blocked only on the business owner supplying real values.

**P1 (partly done 2026-09-27):** Bring the marketplace backend live in production. Production Neon DB is migrated through 006 and all 8 env vars (incl. the Stripe webhook and `PORTAL_SALT`) are set in Netlify. Remaining: switch `STRIPE_SECRET_KEY` and the webhook secret to live mode once the Stripe account is set up, then one real end-to-end booking pass. (`netlify dev:exec` can't migrate production because secret env vars are masked; use the Neon console connection string.)

**Downgraded to P2 (2026-09-26):** production email/auth verification. Now blocked on the domain/DNS decision (move nitsuah.io DNS to Cloudflare, or buy a dedicated domain); `skyviewdynamics.com` may be a placeholder. New P2 note: the stylelint pre-commit hook reports 134 pre-existing errors in `styles/style.css`, so any CSS commit fails until they're fixed or the two rules are relaxed.

Both remaining P1s need human or owner access (business data, Stripe account). None is blocked on code.

## Priority Focus

1. Close the P1 launch-identity data-entry blocker (needs business-owner input, not code).
2. Move demo client files out of the publicly-served `/assets/gallery` directory into a real per-client store so the signed-link flow demonstrates genuine access control end-to-end (P2, per CodeRabbit PR #131). The CWE-598 URL-token finding is already fixed.
3. Reconcile `METRICS.md`'s stale coverage values (last validated 2026-05-24 per CHANGELOG) into one authoritative source.

---

## Key Commands

```bash
docker build -t pmo-skyview-audit .
docker run -d -p 18080:80 pmo-skyview-audit
# Validate with HTTP GET to http://localhost:18080
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities. Recent (Unreleased): server-side client-portal token validation (HMAC-SHA256, mandatory `PORTAL_SALT`, fail-closed); drone cursor hover-offset + spotlight beam; Docker preview now builds/serves the marketplace SPA at `/app`; `config.js` identity fields (address/geo/facebook) wired into schema.org JSON-LD; fixed a `config/docker-compose.yml` relative-path bug breaking documented repo-root Docker commands; `netlify-cli` upgraded for an `extract-zip` CVE fix (PR #120).

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/skyview/docs/ROADMAP|ROADMAP]] · [[repos/skyview/docs/TASKS|TASKS]] · [[repos/skyview/docs/FEATURES|FEATURES]] · [[repos/skyview/METRICS|METRICS]] · [[repos/skyview/docs/CHANGELOG|CHANGELOG]] · [[repos/skyview/README|README]]

**docs/:** [[repos/skyview/docs/DEPLOYMENT_GUIDE|Deployment Guide]] · [[repos/skyview/docs/GETTING_STARTED|Getting Started]] · Quick Reference · [[repos/skyview/docs/OWNER_GUIDE|Owner Guide]] · [[repos/skyview/docs/SEO_GUIDE|SEO Guide]] · [[repos/skyview/docs/ANALYTICS_SETUP|Analytics Setup]] · [[repos/skyview/docs/CLIENT_PORTAL|Client Portal]] · [[repos/skyview/docs/PERFORMANCE_CHECKLIST|Performance Checklist]] · [[repos/skyview/docs/ASSET_MANAGEMENT|Asset Management]]

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/skyview/README|README]] (every doc hangs off its Docs Index)
- Latest LOC report: [[reports/eng-loc-skyview-2026-09-16|2026-09-16]] (older ones chain from it)
- Latest MINI report: [[reports/eng-mini-skyview-2026-10-02|2026-10-02]] (older ones chain from it)
<!-- vault-links:end -->
