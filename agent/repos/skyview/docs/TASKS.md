---
up: "[[repos/skyview]]"
title: "skyview · TASKS"
source: https://github.com/nitsuah/skyview/blob/main/docs/TASKS.md
kind: repo-doc
repo: skyview
---


# Tasks

> 🧭 [skyview](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

**Last Updated:** 2026-10-07

> **Delivery split:** public FE covers the marketing site and funnel. `/admin` is a separate CMS surface. Secure client portal/download auth is a separate backend workstream.

## Done

Shipped work is condensed into `docs/FEATURES.md` (capabilities) and `docs/CHANGELOG.md`
(change-by-change history, incl. native operator scheduling, signed-link/token generation,
drone cursor, Docker SPA build, identity config plumbing, and the Vitest 5 regression fix).
Open 2026 items are tracked below and in `docs/ROADMAP.md` 2027 Q1.

## In Progress

- [ ] Complete the launch checklist with verified production identity data.
  - Priority: P1
  - Blocker: config plumbing is done (see Done above) — this is now purely a data-entry task blocked on the business owner supplying real values. Specifically still needed: **real business phone number**, **real business email** (confirm if `contact@skyviewdynamics.com` is real or a placeholder), **service-area city/region** (or full street address) for `contact.address` in `config.js`, **approximate service-area GPS coordinates** for `contact.geo`, and **real social profile URLs** for `contact.social` (facebook/twitter/instagram/youtube — currently generic homepage URLs, not the business's actual profiles).
  - Acceptance Criteria: production identity fields populated in `config.js`; no placeholder values remain in the rendered page or schema.org JSON-LD; `/admin` invite-only; separation documented.

## Todo

- [ ] Build a real per-client storage backend for the client portal.
  - Priority: P2
  - Context: today's demo files live under `/assets/gallery`, the site's own public marketing gallery (already served statically with no auth), so the signed-link flow (`generateSignedDownloadToken`) doesn't yet demonstrate real access control end-to-end. The manifest itself is also a single shared demo manifest, not per-client, and bulk ZIP download is a placeholder. See `docs/CLIENT_PORTAL.md`.
  - Acceptance Criteria: delivered files live outside any statically-published directory (served as bytes, or via a private-bucket presigned URL) and the manifest is scoped per client.

- [ ] Bring the marketplace backend live in production (the site's booking CTA now points at it).
  - Priority: P1 — Calendly has been removed from the marketing site; "Find an operator" / "Post a job" / the hero CTA now link straight to `/app/register`, so registration, job posting and booking must work in production.
  - Done 2026-09-27: production Neon DB migrated through 006 (incl. `bookings_no_operator_overlap`); all 8 env vars set in Netlify, incl. the Stripe webhook (`/api/stripe-webhooks`: `payment_intent.payment_failed`, `account.updated`) and `PORTAL_SALT`.
  - Remaining: switch the production `STRIPE_SECRET_KEY` (and the webhook secret) to live mode once the Stripe account is set up, then one real end-to-end pass: register as operator -> set availability -> register as client -> post a job -> book -> operator accepts.
  - Note: `netlify dev:exec` can't migrate production, because the CLI only sees masked values for secret env vars. Run `db:migrate` with the connection string from the Neon console instead.; one real end-to-end pass: register as operator -> set availability -> register as client -> post a job -> book -> operator accepts.

- [ ] Set up the email sending domain (DNS + Resend verification), then prove password reset in production.
  - Priority: P2
  - Blocked on: the domain/DNS decision. The owner is either moving nitsuah.io DNS from Netlify to Cloudflare (CNAME redirection, plus a DMARC investigation to centralize reports and route mail to Gmail) or buying a dedicated domain wired up the way nitsuah.io is through Netlify. `skyviewdynamics.com` may be a placeholder; see the production-identity item.
  - Acceptance Criteria: (a) the sender domain used by `netlify/functions/utils/email.js` shows Verified in Resend (SPF/DKIM, plus a DMARC record); (b) a real password-reset email is sent, received, and its link works on production.

- [ ] Native scheduling hardening (follow-ups to the availability work; none block the cutover).
  - Priority: P2
  - Already done in PR #139 after review: DB exclusion constraint against overlapping active bookings (`bookings_no_operator_overlap`), atomic (transactional) availability replace, and blocked-date reasons hidden from the public endpoint.
  - Availability is interpreted in UTC and windows must fit within one UTC day. Operators need a stored timezone (and cross-midnight windows) before this is correct outside a single timezone.
  - The public operator profile does not yet display availability, and the operator dashboard doesn't flag pending requests that conflict with each other.
  - No test exercises the real handlers against a database: the Neon HTTP driver can't talk to plain local Postgres, so SQL was verified via `pg` and JS logic via mocks. Add a Neon-branch (or driver-compatible proxy) integration test.

## Maintenance

- [ ] Test and tooling debt surfaced by the 2026-09 auth + scheduling pass.
  - Priority: P3
  - `npm run lint:js` is broken: `eslint` is not in `package.json`, so linting has never run in CI (stylelint likewise unverified).
  - The stylelint pre-commit hook now runs (local node hook, stylelint 17.15.0) and reports 134 pre-existing errors in `styles/style.css`, mostly camelCase `@keyframes` names (`keyframes-name-pattern`) and `selector-class-pattern`. Any commit that touches CSS will fail the hook until they're fixed. Either rename them (and update the JS/HTML references), or relax those two rules in `config/stylelint.config.mjs`.
  - `tests/site.spec.ts` "gallery interaction" times out intermittently under heavy parallel load (passes alone and with `--workers=2`); CI uses 1 worker, so low risk, but worth de-flaking.
  - Platform form labels (`Login.jsx`, `ResetPassword.jsx`, etc.) aren't associated with their inputs (no `htmlFor`/`id`), so `getByLabel` fails and screen readers lose the label; e2e specs currently select by placeholder. Fix the markup, then switch tests to `getByLabel`.
  - `vite preview` logs `/api/notifications` proxy errors during e2e (the `Layout` bell polls an unmocked endpoint); mock it in the specs to quiet the noise.
  - Dead code left after the contact form was removed (2026-09-19; people are sent to the platform, contact email/phone live only on `pages/privacy.html`): the `.contact-*` styles in `styles/style.css`, `scripts/form.js` (no-ops without the form), the `contact_submit` step in the admin funnel panel (`scripts/conversion-tracking.js` + tests), and the now-unlinked `pages/thank-you.html` and its `netlify.toml` redirect. Also: the privacy page's phone number is still the `+1 (555) 123-4567` placeholder (see the production-identity item).
  - Add a tablet-width check for the Services cards (only desktop and 375px mobile were measured).
  - CodeRabbit was rate-limited on the native-scheduling PR (#139), so that PR never received an automated review; run one on `main` once capacity resets.

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
