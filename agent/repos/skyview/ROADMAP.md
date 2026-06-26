
# Skyview Roadmap

**Last Updated:** 2026-06-08
Next Review: 2026-07-01

> **Planning split:** public FE = landing, gallery, booking, contact, and privacy-safe funnel tracking. `/admin` = separate CMS surface. Client delivery / signed-download auth = separate backend workstream.

## Completed (Q1–Q3 2026) ✅

> Production-ready static site, test harnesses, SEO, Docker smoke, funnel tracking, Lighthouse monitoring, CSP headers, gallery governance, conversion funnel reporting, A/B testing framework, campaign personalization, and client portal hardening all shipped. See FEATURES.md for full details.

## Open (Q3 2026)

- [ ] Build secure client delivery / portal backend separately from the public marketing FE.
  - Next: wire `scripts/portal-token.js` to a Netlify Function or edge middleware with `PORTAL_SALT` secret.

## Q4 2026 (Planned)

- [ ] Multi-segment campaign personalization — expand `scripts/campaign.js` to support service spotlight targeting and additional hero copy variants.
- [ ] Enable A/B experiments — flip `experiments.enabled: true` in `config.js`, wire variants to analytics, analyse results.
