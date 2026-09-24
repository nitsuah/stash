
# Skyview Roadmap

**Last Updated:** 2026-09-23
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

The two-sided marketplace platform (Netlify Functions + Neon DB + Stripe Connect + React SPA at `/app`) shipped in an earlier cycle and is the intended Calendly replacement. The Docker preview originally never built or served the SPA — fixed a prior cycle (multi-stage `Dockerfile` + `config/nginx.conf` SPA fallback for `/app/*`).

> **2026-09 follow-up cycle:** the marketplace previously matched clients to operators but had no actual scheduling — bookings never carried a `scheduled_at` (the booking modal never sent one), so there was no way to know if a proposed time worked for an operator, and nothing prevented double-booking. Built native operator availability: `operator_availability` (recurring weekly windows) and `operator_blocked_dates` (one-off blackouts), migration `006_operator_availability.sql`; `netlify/functions/utils/scheduling.js`'s `checkOperatorAvailability()` enforces it (booking overlap, blocked dates, declared weekly windows) at both booking creation and confirmation, so no single operator can be given, or accept, overlapping bookings. `OperatorOnboarding.jsx` gained an Availability step (weekly hours + blocked dates); `OperatorProfile.jsx`'s booking modal now proposes a date/time (prefilled from the job's `preferred_date`/`preferred_time`) with a live availability hint, and actually sends `scheduled_at`/`duration_hours`. Also fixed an unrelated but blocking bug found along the way: `scripts/migrate.js` called `sql(stmt)`, which the installed `@neondatabase/serverless` version rejects for non-tagged-template calls — needs `sql.query(stmt)` — so `db:migrate` was broken for any migration, not just this one.

**Calendly cutover (2026-09-19): the marketing site no longer uses Calendly.** The booking section is static markup that links into the platform ("Find a drone operator" / "Post a job" / "List as an operator"), the hero CTA goes to `/app/register`, and the Calendly widget, script, CSP entries, config and CSS were removed (the `features.platform`/`features.calendly` flags with them). Testimonials and the unfinished 3D preview were removed from the markup rather than hidden by JS. Because those CTAs now depend on the marketplace backend, bringing it live in production is the remaining P1 item below.

- [ ] **Bring the marketplace backend live in production.** `db:migrate` against the production Neon DB (through migration 006), and `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` / `RESEND_API_KEY` / `JWT_SECRET` / `PORTAL_SALT` / `DATABASE_URL` set in Netlify, then one real end-to-end pass (operator availability -> client job -> booking -> accept). See TASKS.md.

- [ ] **Production verification of auth + OAuth (open after the 2026-09 auth pass).** The `/api/auth/google` 404 (two Netlify functions claiming overlapping paths) is fixed and regression-tested, but a real Google sign-in, real reset email, and the Netlify env vars were never verified live. See TASKS.md "Verify production auth/env end-to-end".
- [ ] **Native scheduling hardening (P2).** The DB-level double-booking guard (exclusion constraint), transactional availability replace, and public blocked-date privacy shipped with migration 006 / PR #139. Still open: per-operator timezones and cross-midnight windows, availability shown on public operator profiles, and a real-database integration test. See TASKS.md "Native scheduling hardening".

## Q4 2026 (Planned)

- [ ] Multi-segment campaign personalization — expand `scripts/campaign.js` to support service spotlight targeting and additional hero copy variants.
- [ ] Enable A/B experiments — flip `experiments.enabled: true` in `config.js`, wire variants to analytics, analyse results.
- [ ] **Testimonial carousel** — rotating client quote block on the homepage; content managed through a `testimonials` array in `config.js` so it can be updated without touching markup (the placeholder testimonials section was removed from `index.html` on 2026-09-19); supports campaign-segment targeting for social proof alignment.
- [x] ~~Booking calendar embed (Cal.com)~~ — superseded by the native platform scheduling; Calendly is now removed from the marketing site as well.

## Q1 2027 (PM Goals — Client Outcomes)

- [ ] **Blog / news section** — Decap CMS collection for articles; improves SEO long-tail discovery for drone services.
- [ ] **Expanded service pages** — individual landing pages for Real Estate, Events, Cinematography, and Mapping; separate URLs for SEO.
- [ ] **Testimonial section activation** — re-add the testimonials section to `index.html` (it was removed from the markup, not just hidden) once real client reviews are collected, then set `testimonials: true` in config.js.
- [ ] **Google My Business** — verify listing, link to live site, enable review collection.
- [ ] **Portfolio case studies** — per-project pages with before/after, deliverables, and client outcome blurb.
- [ ] **Analytics activation** — enable Plausible or Netlify Analytics; set conversion goals for booking and contact events.

## 2027 (Stub — scoping only, not started)

- [ ] **Business plan / end-to-end platform automation document.**
  - Priority: P3 (planning, not code)
  - This is a large, uncertain, non-code planning exercise and was deliberately **not** written in the 2026-09 cycle — it needs deliberate input from the business owner, not a guessed-at draft. Scoping it here so a future session (or the owner directly) can pick it up with the right frame:
  - Should eventually cover: (1) a real business plan — target market, pricing model, competitive position for a solo/small drone services operator vs. the marketplace-platform pivot; (2) marketing automation tracking — campaign personalization (`scripts/campaign.js`), A/B experiments, funnel conversion data, and how they roll up into acquisition-cost / LTV decisions; (3) insurance & compliance automation — FAA Part 107 cert expiry (`netlify/functions/cron-cert-expiry.mjs` already exists), liability insurance tracking, waiver/consent workflows for client shoots; (4) ops automation — booking-to-delivery pipeline once the client portal backend (TASKS.md P2) and marketplace platform (P2 above) are both live; (5) a defined set of front-end metrics (funnel conversion, campaign attribution) and back-end metrics (booking completion rate, operator onboarding time, payout latency) to actually trace whether the automation is working, not just that it shipped.
  - Not scoped further than this list on purpose — the acceptance criteria for each sub-area depend on business decisions (real pricing, real insurance carrier, real service area) that don't exist yet.
