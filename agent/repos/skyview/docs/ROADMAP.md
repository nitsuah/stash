# Skyview Roadmap

> 🧭 [skyview](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

**Last Updated:** 2026-09-24
Next Review: 2026-10-24

> **Planning split:** public FE = landing, gallery, booking, contact, and privacy-safe funnel tracking. `/admin` = separate CMS surface. Client delivery / signed-download auth = separate backend workstream.

> 2027 planning reset (2026-09-24): Q1–Q3 2026 (static site, SEO, funnel tracking, CSP, gallery governance, A/B
> framework, campaign personalization), the 2026-09 client-portal security work (server-side HMAC token validation,
> mandatory `PORTAL_SALT`, fail-closed), the marketplace platform with native operator scheduling, and the Calendly
> cutover are shipped — see [FEATURES](./FEATURES.md) / [CHANGELOG](./CHANGELOG.md). Every open item from the
> Client Portal, Marketplace, and Q4 2026 sections was merged with the existing Q1 2027 goals below.

## 2027 Q1 - Marketplace Go-Live & Client Outcomes (Planned)

### Launch-critical *(carried from 2026 Marketplace / Calendly cutover)*

- [ ] **Bring the marketplace backend live in production.** The site's booking CTAs now depend on it. `db:migrate` against production Neon (through migration 006); set `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` / `RESEND_API_KEY` / `JWT_SECRET` / `PORTAL_SALT` / `DATABASE_URL` in Netlify; then one real end-to-end pass (operator availability → client job → booking → accept). See TASKS.md.
- [ ] **Production verification of auth + OAuth.** The `/api/auth/google` 404 is fixed and regression-tested, but a real Google sign-in, real reset email, and the Netlify env vars were never verified live. See TASKS.md "Verify production auth/env end-to-end".
- [ ] **Native scheduling hardening (P2).** Still open: per-operator timezones and cross-midnight windows, availability on public operator profiles, and a real-database integration test. See TASKS.md "Native scheduling hardening".
- [ ] **Signed-download delivery backend for `client-gallery.html`** *(carried from 2026-09 Client Portal Security)* — the login gate is server-verified; the gallery's file listing is still the client-side prototype described in `docs/CLIENT_PORTAL.md`.

### Growth & client outcomes *(carried from 2026 Q4 + existing Q1 2027 PM goals)*

- [ ] **Analytics activation** — enable Plausible or Netlify Analytics; set conversion goals for booking and contact events.
- [ ] **Enable A/B experiments** — flip `experiments.enabled: true` in `config.js`, wire variants to analytics, analyse results. *(2026 Q4)*
- [ ] **Multi-segment campaign personalization** — expand `scripts/campaign.js` for service spotlight targeting and more hero copy variants. *(2026 Q4)*
- [ ] **Testimonials** — collect real client reviews, then re-add the section to `index.html` (removed 2026-09-19) as a `config.js`-driven rotating carousel with campaign-segment targeting. *(merges the 2026 Q4 carousel and Q1 2027 activation items)*
- [ ] **Google My Business** — verify listing, link to live site, enable review collection.
- [ ] **Blog / news section** — Decap CMS collection for articles; SEO long-tail discovery for drone services.
- [ ] **Expanded service pages** — individual landing pages for Real Estate, Events, Cinematography, and Mapping.
- [ ] **Portfolio case studies** — per-project pages with before/after, deliverables, and client outcome blurb.

## 2027 — Unscheduled Stub (scoping only, not started)

- [ ] **Business plan / end-to-end platform automation document.**
  - Priority: P3 (planning, not code)
  - This is a large, uncertain, non-code planning exercise and was deliberately **not** written in the 2026-09 cycle — it needs deliberate input from the business owner, not a guessed-at draft. Scoping it here so a future session (or the owner directly) can pick it up with the right frame:
  - Should eventually cover: (1) a real business plan — target market, pricing model, competitive position for a solo/small drone services operator vs. the marketplace-platform pivot; (2) marketing automation tracking — campaign personalization (`scripts/campaign.js`), A/B experiments, funnel conversion data, and how they roll up into acquisition-cost / LTV decisions; (3) insurance & compliance automation — FAA Part 107 cert expiry (`netlify/functions/cron-cert-expiry.mjs` already exists), liability insurance tracking, waiver/consent workflows for client shoots; (4) ops automation — booking-to-delivery pipeline once the client portal backend (TASKS.md P2) and marketplace platform (P2 above) are both live; (5) a defined set of front-end metrics (funnel conversion, campaign attribution) and back-end metrics (booking completion rate, operator onboarding time, payout latency) to actually trace whether the automation is working, not just that it shipped.
  - Not scoped further than this list on purpose — the acceptance criteria for each sub-area depend on business decisions (real pricing, real insurance carrier, real service area) that don't exist yet.
