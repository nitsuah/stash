---
updated: 2026-09-02
---

# Tasks

## In Progress

- [x] Polish the popup into a true job-workspace view.
  - Priority: P1
  - Context: the tracker is now useful, but the remaining work is mostly fit-and-finish: wider workspace sizing, tighter review loops, and lower-scroll editing.
  - Acceptance Criteria: tracker/profile views feel roomy, the user can manage job context without fighting the popup, and the workspace stays aligned with the local-first/review-first product promise.
  - Progress: landed wider workspace behavior, responsive lane/grid cleanup, final-stage (Rejected/Retired) collapse controls, tracker status placement near header actions, status-select dark-mode polish, split Profile actions (Save Profile vs Parse/Upload Resume), editable card URL, grouped card editor boxes, restored submitted/updated date editing block, structured pay controls, verdict dropdown, location selector, drag-lock while editing, and larger description editing area.
  - Progress (2026-05-31): tracker lanes now render every item as a contracted, draggable bubble (first 3 per active section auto-expand on open); cards moved via a hover-reveal left-rail grab handle (kept clear of content via a reserved gutter, incl. the standalone view); clicking a card body expands it and Save drops it back one level.
  - Progress (2026-05-31, FE pass 3): job-search reorganized like the pipeline toolbar — centered panel, an expanding "⚙ Filters" sub-bar (sources + pay), fixed the results grid (was losing to a flex fallback), compact grid cards with a truncated description and icon-only actions (↗ open post / 💾 save, text on hover). Pay filter redesigned: Annual/Hourly toggle, min/max sliders paired with editable number boxes treated as K (90 → $90k), seeded from saved salary prefs; locked source chips now route to AI settings to add credentials. Tracker: sentiment emojis swapped to discernible 🔥/👍/➖/👎/❌/🔍 (click to cycle), star score is now click-to-set directly on the collapsed card (reverse-flex hover-fill) without expanding it. Reverted the standalone home/back tab-close — Profile/main just load in app mode. section bubbles now sit inline with the subtitle (less vertical space); card meta is emoji-first — location flag, employment-type indicator, remote 🏠/🏢, sentiment emoji, and score stars (with the prior text moved to hover/aria), all compacted onto an indicators row + a pay row. Job Search now opens in the expanded workspace (not the popup), with a pinned header (back button top-right), a results grid, source filter chips, and a pay filter (annual/hourly toggle, dual slider, seeded from saved salary prefs, keeps unknown-salary jobs). Home/logo and job-search Back return to the popup from a standalone tab. Per-source API setup links (Adzuna, USAJOBS) match the Gemini "Get a free key →" affordance. Pay parsing/filter covered by `tests/job-search.test.mjs` (46 tests). Profile reorg: Core profile / Preferences (incl. merged answer defaults) two-up row; Memory (col A) vs red protected Demographic (col B); Memory, Ignore list, and Sensitive memory are collapsible sections whose items render as expandable bubble chips, fully contracted by default. iframe (iCIMS) fill, path-scoped custom-domain ATS detection, pay-slider rework, and expanded legal/privacy + consent date also landed.
  - Remaining: refresh `screenshots/` gallery for the new tracker/profile UI; monitor follow-up FE feedback during the current review pass.

- [x] Keep local-first autofill and privacy controls trustworthy.
  - Priority: P1
  - Context: privacy consent, help/reset flows, and profile-adjacent Memory now exist; the next work is tightening clarity and keeping the controls easy to trust.
  - Acceptance Criteria: the privacy story remains explicit, Memory stays easy to review/correct, and reset/delete flows remain one click away.
  - Progress: memory rendering/edit/ignore/restore flows now reliably display and persist; sensitive memory grouping remains visible; status messaging and profile workflows were clarified without weakening consent-first/local-first behavior.
  - Remaining: continue monitoring for wording regressions as future changes land; current QA pass closed without privacy/help wording regressions.

- [x] Start a practical `apply-bot` rebrand pass.
  - Priority: P2
  - Context: the product needs a clearer visual and messaging system, but it should stay grounded in the current MVP goals: local-first autofill, review-first trust, and a real job-workspace feel.
  - Acceptance Criteria: define an achievable naming/branding checklist for popup copy, icons, and docs without derailing the core application workflow.
  - Progress: user-facing copy now shifts toward "Apply Workspace" across the manifest, popup header, tracker labels, and README positioning; rebrand pass remains partial and intentionally scoped to copy/UI touchpoints for now.

## Todo

### P1 - Job Search & ATS Handoff

- [x] Implement multi-source job search aggregation:
  - Progress: All major job search integrations and scraping capabilities are now implemented and covered by tests, including Indeed RSS with improved company and job ID extraction.
  - Remaining: on-ATS-page detail parsing depth, tracker-side indexing enhancements, OAuth job source once a partner API is available.

- [ ] Plan for future: OAuth or user sign-in for personalized job search (if API supports it).
  - Deferred to ROADMAP.md 2027 Q1 (2026-09-02): no currently-integrated board exposes a consumer OAuth job-search/personalization API — LinkedIn's is enterprise-partner-gated, Indeed's public API doesn't personalize per-user. This is distinct from OAuth *profile import* (shipped for LinkedIn + Google) and needs a partner API this local-first, no-backend extension doesn't have yet.
- [x] Plan for future: user-configured job sources like unemployment offices (JOBS4TN.gov) and search criteria.
  - Progress (2026-09-02): shipped custom RSS job sources — add a name + RSS feed URL from the AI settings panel (`lib/job-search.js`: `normalizeCustomRssJob`, `buildCustomJobSources`), merged into the same registry as built-in boards so they get filter chips, dedupe, and pay filtering for free. Search criteria live in the feed URL itself (most RSS boards accept query params) rather than a separate criteria UI. Fetching an arbitrary user-supplied origin required adding `optional_host_permissions` + a `chrome.permissions.request()` prompt scoped to just that origin, so the extension doesn't need a blanket "read all sites" permission.

#### Acceptance Criteria
- User can search jobs from multiple sources in one panel.
- Each result has a clear "Go to job post" action (ATS link if possible).
- User can save jobs to their tracker with one click.
- Tracker search/indexing is fast and reliable.

### P2 - Tracker Insights

- [x] Surface aggregate analytics from tracked applications.
  - Priority: P2
  - Context: the tracker accumulated application records but could not answer which sources were worth the time, whether salary targets cost replies, or how long to wait before assuming a no.
  - Acceptance Criteria: response rate by source, salary-band effectiveness, and time-to-first-response are visible from the workspace, computed entirely from local storage with no new API calls or permissions.
  - Progress: shipped the Analytics screen (header nav + tracker toolbar entry points, deep-linkable via `?screen=analytics`). Aggregation lives in `lib/analytics.js` as pure chrome-free functions covered by 16 unit tests. Required closing two storage schema gaps in `lib/tracker.js`: `job.source` was being dropped on save, and no first-response timestamp existed — added a sticky `first_response_at` so progression through interview → offer → rejected does not overwrite the original reply time.
  - Remaining: historical time-to-response is approximate — entries predating `first_response_at` backfill from `updated_at`, which records when the user moved the card rather than when the employer replied. Accurate going forward only. Salary effectiveness is correlational and currently gives no warning on thin buckets.

- [ ] Resolve the Google OAuth client-registration contract for `handleGoogleConnect` (`lib/oauth.js:55-57`, `background/service-worker.js:344-346`).
  - Priority: P2
  - Context: `launchWebAuthFlow` + `chrome.identity.getRedirectURL()` produces an `https://<extension-id>.chromiumapp.org/` redirect, which is not the loopback redirect a Google **Desktop app** OAuth client expects — users who create the documented Desktop/Chrome-app client type can hit `redirect_uri_mismatch`. Flagged by CodeRabbit as CWE-associated (functional correctness / heavy lift); not fixed inline because the actual correct answer depends on a decision made outside this repo (which Google Cloud client type + redirect strategy this extension asks users to register), not a pure code change.
  - Acceptance Criteria: either (a) document that users must register a **Web application** client type with `https://<extension-id>.chromiumapp.org/` as an authorized redirect URI (matches how `launchWebAuthFlow` already behaves — likely the smaller change), or (b) switch the flow to a redirect strategy compatible with the currently-documented Desktop client type. Whichever is chosen, `docs/` setup instructions and the two call sites above must agree.

### P3 - Exploratory

- [x] Begin to implement job search results by scraping and searching multiple job pages.
  - Progress: LinkedIn session scraping, HN/WWR/remote.co RSS/Algolia keyless, and Indeed scraping are all implemented.
  - Remaining: broader page-scraping capability.
- [x] Evaluate identity-based profile import paths.
  - Priority: P3
  - Context: Google sign-in, ID.me, or similar identity sources may help bootstrap profile fields later, but only after the local-first and consent-first path is stable.
  - Acceptance Criteria: any future identity import remains optional, explicit-consent based, and does not weaken the current on-device default.
  - Progress (2026-05-31): shipped BYO-OAuth "Sign in with LinkedIn" (OIDC) via `chrome.identity.launchWebAuthFlow` + `identity` permission. User supplies their own LinkedIn app Client ID/Secret (stored locally), registers the shown redirect URL, and connects to pre-fill name + email into the Profile. SW handles the code→token→userinfo exchange (`lib/oauth.js` mapper is unit-tested). Stays optional/consent-based/local-first. Note: LinkedIn's public API doesn't expose job listings (partner-gated), so this is profile-import only; the job-source registry's `config` seam is ready for any future OAuth job source.

### P4 - Nice to have

- [x] Run an `axe` / a11y audit on the popup and key application-review flows.
  - Progress: All identified accessibility fixes for the popup and key application-review flows have been implemented.
  - Remaining: monitor follow-up FE feedback during the current review pass.
- [x] Identify visual overload segments and have AI buttons to make detailed information more concise for consumption.
  - Progress: All AI button surfaces are now covered.
  - Remaining: none.

### Deferred / blocked (FE-pass follow-ups, 2026-05-31)

Captured so they aren't lost; pick up when prioritized.

- [x] **UX Audit batch 2 (medium priority):** #11 expanded card modal (kanban), #22 popup/standalone state sync, #24 scalar answer preview density, #26 narrative card overflow, #27 sensitive section alarming red, #30 profile single-column, #31 memory bubble hover/connector, #33 memory delete confirm+danger.
  - Progress: All UX audit findings have been addressed.
- [x] **Wire `axe-core` into the Playwright e2e.**
  - Progress: `@axe-core/playwright` is now correctly integrated into `package.json` and `package-lock.json`, and the Docker build process is updated.
- [x] **Refresh `screenshots/` gallery**: added `tests/e2e/screenshots.spec.mjs` — Playwright captures from headless Chromium with a chrome mock (shows UI shell/chrome but no live data). Full gallery with real populated data still needs the extension loaded in real Chrome. New captures: main-dashboard, tracker-workspace, profile-memory, job-search, ai-settings all updated.
- [x] **a11y burndown (remaining from `docs/a11y-audit.md`):** keyboard alternative for bubble/card drag-and-drop (status `<select>` is the current path — document or enhance); automated color-contrast verification of muted text over tinted surfaces + small badges; focus-ring audit at popup vs. standalone widths.
  - Progress: All remaining a11y burndown items have been addressed.
