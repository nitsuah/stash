
# Tasks

> 🧭 [skyview](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

**Last Updated:** 2026-09-24

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
  - Acceptance Criteria: `db:migrate` run against production Neon DB (through migration 006, incl. the `bookings_no_operator_overlap` constraint); `STRIPE_SECRET_KEY`/`STRIPE_WEBHOOK_SECRET`/`RESEND_API_KEY`/`JWT_SECRET`/`PORTAL_SALT`/`DATABASE_URL` set in Netlify; one real end-to-end pass: register as operator -> set availability -> register as client -> post a job -> book -> operator accepts.

- [ ] Verify production auth/env end-to-end (left open by the 2026-09 auth + scheduling pass; nothing here could be checked without Netlify/Google/Resend access).
  - Priority: P1
  - Acceptance Criteria: (a) confirm `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`/`DATABASE_URL`/`JWT_SECRET`/`RESEND_API_KEY` are set in Netlify; (b) Google Cloud Console has `https://skyviewd.netlify.app/api/auth/google/callback` as an authorized redirect URI; (c) a human completes one real "Continue with Google" sign-in on production (the routing 404 is fixed and unit-tested, but the OAuth round trip itself was never exercised); (d) a real password-reset email is sent, received, and its link works (confirm the `noreply@skyviewdynamics.com` sender domain is verified in Resend).

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
