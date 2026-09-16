
# Skyview Roadmap

**Last Updated:** 2026-09-02
Next Review: 2026-10-01

> **Planning split:** public FE = landing, gallery, booking, contact, and privacy-safe funnel tracking. `/admin` = separate CMS surface. Client delivery / signed-download auth = separate backend workstream.

## Completed (Q1–Q3 2026) ✅

> Production-ready static site, test harnesses, SEO, Docker smoke, funnel tracking, Lighthouse monitoring, CSP headers, gallery governance, conversion funnel reporting, A/B testing framework, campaign personalization, and client portal hardening (CSP, security headers, and funnel posture) all shipped. See FEATURES.md for full details.
>
> **2026-09 cycle:** Server-side client-portal token validation shipped (HMAC-SHA256, mandatory `PORTAL_SALT`, fail-closed — see Client Portal below). Drone cursor now hovers offset from the pointer with a spotlight beam connecting the two. The marketplace platform SPA is now built and served by the Docker preview image, matching the Netlify production build (previously Docker-only previews never included `/app`). `config.js` now centralizes address/geo/social identity fields for the schema.org listing, not just name/email/phone. Fixed a latent path-resolution bug in `config/docker-compose.yml` that made the documented `docker compose -f config/docker-compose.yml run --rm unit` command fail outside of a `--project-directory` override.

## Client Portal Security ✅ (2026-09)

- [x] Server-side portal token validation — `netlify/functions/api-portal.mjs` verifies access codes via HMAC-SHA256 (`netlify/functions/utils/portal.js`), shared with the CLI generator (`scripts/portal-token.js`).
- [x] `PORTAL_SALT` is a mandatory production secret with no fallback; both the CLI and the verification endpoint refuse to operate without it.
- [x] Fail-closed behavior: the endpoint returns 503 (deny) when `PORTAL_SALT` is unconfigured, rather than falling back to a weaker or no-op check.
- [ ] Follow-on (P2, unchanged scope): full signed-download delivery backend for `client-gallery.html` — see TASKS.md. The login gate above is server-verified; the gallery's file listing is still the client-side prototype described in `docs/CLIENT_PORTAL.md`.

## Marketplace Platform / Calendly Cutover

The two-sided marketplace platform (Netlify Functions + Neon DB + Stripe Connect + React SPA at `/app`) shipped in an earlier cycle and already contains the intended Calendly replacement: when `features.platform: true` in `config.js`, the booking section swaps the Calendly widget for an operator-matching CTA (`config.js`, `handle booking section` block). That swap logic was already wired into the frontend, but the Docker preview never built or served the SPA — fixed this cycle (multi-stage `Dockerfile` + `config/nginx.conf` SPA fallback for `/app/*`).

**Not done this cycle, and deliberately not rushed:** flipping `platform: true` by default and removing the Calendly script/CSP entries. That cutover requires the marketplace backend to actually be operational — `db:migrate` run against a provisioned Neon database, and `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` / `RESEND_API_KEY` / `JWT_SECRET` / `PORTAL_SALT` set in the Netlify environment — none of which is a code change. Flipping the flag before that would replace a working Calendly booking flow with a non-functional one.

- [ ] **Activate marketplace platform in production (Calendly cutover).**
  - Priority: P2
  - Acceptance Criteria: `db:migrate` run against production Neon DB; Stripe/Resend/JWT/PORTAL_SALT env vars set in Netlify; `config.js` `features.platform` flipped to `true`; Calendly script tag, CSP entries (`assets.calendly.com`, `frame-src https://calendly.com`), and `features.calendly` removed once the platform CTA is confirmed working end-to-end in production.
  - This is an operational/business decision (two-sided marketplace vs. simple booking), not a rushed code change — see note above.

## Q4 2026 (Planned)

- [ ] Multi-segment campaign personalization — expand `scripts/campaign.js` to support service spotlight targeting and additional hero copy variants.
- [ ] Enable A/B experiments — flip `experiments.enabled: true` in `config.js`, wire variants to analytics, analyse results.
- [ ] **Testimonial carousel** — rotating client quote block on the homepage; content managed through a `testimonials` array in `config.js` so it can be updated without touching markup; supports campaign-segment targeting for social proof alignment.
- [x] ~~Booking calendar embed (Cal.com)~~ — superseded by the marketplace platform activation task above; building a second, parallel booking widget when the platform CTA already exists would be redundant. Removed as a separate item.

## Q1 2027 (PM Goals — Client Outcomes)

- [ ] **Blog / news section** — Decap CMS collection for articles; improves SEO long-tail discovery for drone services.
- [ ] **Expanded service pages** — individual landing pages for Real Estate, Events, Cinematography, and Mapping; separate URLs for SEO.
- [ ] **Testimonial section activation** — enable `testimonials: true` in config.js once real client reviews are collected.
- [ ] **Google My Business** — verify listing, link to live site, enable review collection.
- [ ] **Portfolio case studies** — per-project pages with before/after, deliverables, and client outcome blurb.
- [ ] **Analytics activation** — enable Plausible or Netlify Analytics; set conversion goals for booking and contact events.

## 2027 (Stub — scoping only, not started)

- [ ] **Business plan / end-to-end platform automation document.**
  - Priority: P3 (planning, not code)
  - This is a large, uncertain, non-code planning exercise and was deliberately **not** written in the 2026-09 cycle — it needs deliberate input from the business owner, not a guessed-at draft. Scoping it here so a future session (or the owner directly) can pick it up with the right frame:
  - Should eventually cover: (1) a real business plan — target market, pricing model, competitive position for a solo/small drone services operator vs. the marketplace-platform pivot; (2) marketing automation tracking — campaign personalization (`scripts/campaign.js`), A/B experiments, funnel conversion data, and how they roll up into acquisition-cost / LTV decisions; (3) insurance & compliance automation — FAA Part 107 cert expiry (`netlify/functions/cron-cert-expiry.mjs` already exists), liability insurance tracking, waiver/consent workflows for client shoots; (4) ops automation — booking-to-delivery pipeline once the client portal backend (TASKS.md P2) and marketplace platform (P2 above) are both live; (5) a defined set of front-end metrics (funnel conversion, campaign attribution) and back-end metrics (booking completion rate, operator onboarding time, payout latency) to actually trace whether the automation is working, not just that it shipped.
  - Not scoped further than this list on purpose — the acceptance criteria for each sub-area depend on business decisions (real pricing, real insurance carrier, real service area) that don't exist yet.
