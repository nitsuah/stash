---
updated: 2026-09-24
---

# Roadmap

> 🧭 [auto-apply-plugin](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->
>
> 2027 planning reset (2026-09-24): all 2026 quarters (Q1–Q4) were fully shipped and have been removed from this file — see [FEATURES](./FEATURES.md) and [CHANGELOG](./CHANGELOG.md) (released as v1.0.1/v1.0.2 on the Chrome Web Store).

## 2027 Q1 (Planned)

- [ ] **OAuth / sign-in for personalized job search** — carried forward from TASKS.md P1. Distinct from the shipped LinkedIn/Google profile-import OAuth: this means a job board authenticating the user to return *personalized* search results or recommendations (not just "who is this person"). Blocked on a partner-tier API — LinkedIn's job-search API is enterprise-partner-gated (confirmed while building the LinkedIn profile-import flow), Indeed's public Publisher API doesn't offer per-user personalization, and no other currently-integrated board exposes a consumer OAuth job-search endpoint. A local-first, no-backend extension can't broker this without a board that offers it; revisit if/when a partner API becomes available. In the meantime, the multi-source keyless/keyed search plus this cycle's custom-RSS-source feature cover the discovery need generally.
- [ ] **ID.me identity import** — split out of the 2026 Q4 "identity-provider imports" item (Google shipped 2026-09-02). ID.me is an identity-verification/KYC service rather than a standard consumer OIDC provider, so it needs its own design pass (different consent language, different data returned, different trust model) rather than reusing the Google/LinkedIn BYO-OAuth generalization as-is.
- [ ] **Analytics-informed apply suggestions** — new idea (2026-08-28): once analytics has enough history, surface a one-line nudge on the tracker card itself ("boards like this one respond 2x more often") rather than requiring a trip to the analytics panel. Reuses the same aggregation the panel already computes.
- [ ] **Response-time accuracy follow-up** — the analytics panel's historical response-time figures are approximate for applications logged before the first-response timestamp existed; consider a one-time backfill pass using each application's stored status-change log where available, or an explicit "approximate" badge on entries predating a chosen cutoff date so the panel doesn't imply more precision than the data supports.

## Notes

- Local-first and consent-first remain the product guardrails.
- Scrape from the page or JD before asking the user to type.
- Detailed execution work stays in `TASKS.md`.
