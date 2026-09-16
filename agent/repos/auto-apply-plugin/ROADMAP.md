---
updated: 2026-09-02
---

# Roadmap

## 2026 Q1 ✅

> Completed. See FEATURES.md for shipped capabilities.

## 2026 Q2 ✅

- [x] Turn the tracker into a real job-workspace view with stored JD metadata, location, employment type, structured pay bands, verdict controls, scorecard fields, search/filter controls, and a wider lower-scroll popup layout.
- [x] Start a lightweight `apply-bot` rebrand pass across popup copy, icons, and docs without over-scoping the MVP.
- [x] Add picker-style job detail capture from the current page or pasted JD text and keep extending it into a stronger import workflow.

## 2026 Q3 ✅

- [x] Expand job search to additional sources — on-ATS-page parsing depth, tracker-side indexing, and OAuth job source once a partner API is available.

## 2026 Q4 (In Progress)

- [x] Begin to implement job search results by scraping and searching multiple job pages, starting with LinkedIn and Indeed, etc. and then expanding to a more general multi-site search and alerting capability.
- [x] Explore optional identity-provider imports (Google, ID.me, etc.) for bootstrapping profile data without breaking local-first/privacy guarantees. But also for email/etc. auto-fill in the tracker and potential future job-board integrations.
  - Shipped Google as a second BYO-OAuth profile-import provider (2026-09-02), generalizing the existing LinkedIn OIDC flow (`lib/oauth.js`, `chrome.identity.launchWebAuthFlow`) — same BYO-app, local-first, consent-based pattern. ID.me deliberately scoped out of this pass: it's a government identity-verification service (KYC-style flows, not a standard consumer OIDC exchange) and doesn't fit the same generalization — see 2027 Q1 below.
- [x] Revisit deeper job-fit scoring, verdict assistance, and richer tracker analytics after the storage and review foundations are stable.
- [x] Run a lightweight `axe` / accessibility audit on popup navigation, labels, contrast, and keyboard flow as the workspace UI settles.
- [x] **Interview prep mode** — from a saved tracker card, generate a Gemini-backed set of likely behavioral and technical questions tailored to the JD and the user's stored profile, with suggested answer structures pre-filled from memory. Keeps interview prep local-first and zero-upload.
- [x] **Application analytics panel** — surface aggregate stats from tracker data: response-rate by source, salary-range effectiveness, and time-to-first-response distribution; gives signal on which boards and bid ranges are yielding callbacks without any external telemetry (PR #57). Required closing two storage gaps first: `job.source` was silently dropped on save, and no first-response timestamp existed, so historical response-time data is approximate.
- [x] **User-configured job sources** — add any RSS-based job board (state workforce boards like JOBS4TN.gov, internal careers feeds, niche boards) from the AI settings panel; merges into the existing plug-and-play source registry so custom sources get filter chips, dedupe, and pay filtering automatically. Requests one-time per-origin permission via `chrome.permissions.request()` rather than broadening default host permissions (2026-09-02).

## 2027 Q1 (Proposed)

- [ ] **OAuth / sign-in for personalized job search** — carried forward from TASKS.md P1. Distinct from the profile-import OAuth above: this means a job board authenticating the user to return *personalized* search results or recommendations (not just "who is this person"). Blocked on a partner-tier API — LinkedIn's job-search API is enterprise-partner-gated (confirmed while building the LinkedIn profile-import flow), Indeed's public Publisher API doesn't offer per-user personalization, and no other currently-integrated board exposes a consumer OAuth job-search endpoint. A local-first, no-backend extension can't broker this without a board that offers it; revisit if/when a partner API becomes available. In the meantime, the multi-source keyless/keyed search plus this cycle's custom-RSS-source feature cover the discovery need generally.
- [ ] **ID.me identity import** — split out of the "identity-provider imports" item above (Google shipped 2026-09-02). ID.me is an identity-verification/KYC service rather than a standard consumer OIDC provider, so it needs its own design pass (different consent language, different data returned, different trust model) rather than reusing the Google/LinkedIn BYO-OAuth generalization as-is.
- [ ] **Analytics-informed apply suggestions** — new idea (2026-08-28): once analytics has enough history, surface a one-line nudge on the tracker card itself ("boards like this one respond 2x more often") rather than requiring a trip to the analytics panel. Reuses the same aggregation the panel already computes.
- [ ] **Response-time accuracy follow-up** — the analytics panel's historical response-time figures are approximate for applications logged before the first-response timestamp existed; consider a one-time backfill pass using each application's stored status-change log where available, or an explicit "approximate" badge on entries predating a chosen cutoff date so the panel doesn't imply more precision than the data supports.

## Notes

- Local-first and consent-first remain the product guardrails.
- Scrape from the page or JD before asking the user to type.
- Detailed execution work stays in `TASKS.md`.
