---
updated: 2026-06-08
---

# Tasks

## In Progress

- [/] Polish the popup into a true job-workspace view.
  - Priority: P1
  - Context: the tracker is now useful, but the remaining work is mostly fit-and-finish: wider workspace sizing, tighter review loops, and lower-scroll editing.
  - Acceptance Criteria: tracker/profile views feel roomy, the user can manage job context without fighting the popup, and the workspace stays aligned with the local-first/review-first product promise.
  - Progress: landed wider workspace behavior, responsive lane/grid cleanup, final-stage (Rejected/Retired) collapse controls, tracker status placement near header actions, status-select dark-mode polish, split Profile actions (Save Profile vs Parse/Upload Resume), editable card URL, grouped card editor boxes, restored submitted/updated date editing block, structured pay controls, verdict dropdown, location selector, drag-lock while editing, and larger description editing area.
  - Progress (2026-05-31): tracker lanes now render every item as a contracted, draggable bubble (first 3 per active section auto-expand on open); cards moved via a hover-reveal left-rail grab handle (kept clear of content via a reserved gutter, incl. the standalone view); clicking a card body expands it and Save drops it back one level.
  - Progress (2026-05-31, FE pass 3): job-search reorganized like the pipeline toolbar — centered panel, an expanding "⚙ Filters" sub-bar (sources + pay), fixed the results grid (was losing to a flex fallback), compact grid cards with a truncated description and icon-only actions (↗ open post / 💾 save, text on hover). Pay filter redesigned: Annual/Hourly toggle, min/max sliders paired with editable number boxes treated as K (90 → $90k), seeded from saved salary prefs; locked source chips now route to AI settings to add credentials. Tracker: sentiment emojis swapped to discernible 🔥/👍/➖/👎/❌/🔍 (click to cycle), star score is now click-to-set directly on the collapsed card (reverse-flex hover-fill) without expanding it. Reverted the standalone home/back tab-close — Profile/main just load in app mode. section bubbles now sit inline with the subtitle (less vertical space); card meta is emoji-first — location flag, employment-type indicator, remote 🏠/🏢, sentiment emoji, and score stars (with the prior text moved to hover/aria), all compacted onto an indicators row + a pay row. Job Search now opens in the expanded workspace (not the popup), with a pinned header (back button top-right), a results grid, source filter chips, and a pay filter (annual/hourly toggle, dual slider, seeded from saved salary prefs, keeps unknown-salary jobs). Home/logo and job-search Back return to the popup from a standalone tab. Per-source API setup links (Adzuna, USAJOBS) match the Gemini "Get a free key →" affordance. Pay parsing/filter covered by `tests/job-search.test.mjs` (46 tests). Profile reorg: Core profile / Preferences (incl. merged answer defaults) two-up row; Memory (col A) vs red protected Demographic (col B); Memory, Ignore list, and Sensitive memory are collapsible sections whose items render as expandable bubble chips, fully contracted by default. iframe (iCIMS) fill, path-scoped custom-domain ATS detection, pay-slider rework, and expanded legal/privacy + consent date also landed.
  - Remaining: refresh `screenshots/` gallery for the new tracker/profile UI; monitor follow-up FE feedback during the current review pass.

- [/] Keep local-first autofill and privacy controls trustworthy.
  - Priority: P1
  - Context: privacy consent, help/reset flows, and profile-adjacent Memory now exist; the next work is tightening clarity and keeping the controls easy to trust.
  - Acceptance Criteria: the privacy story remains explicit, Memory stays easy to review/correct, and reset/delete flows remain one click away.
  - Progress: memory rendering/edit/ignore/restore flows now reliably display and persist; sensitive memory grouping remains visible; status messaging and profile workflows were clarified without weakening consent-first/local-first behavior.
  - Remaining: continue monitoring for wording regressions as future changes land; current QA pass closed without privacy/help wording regressions.

- [/] Start a practical `apply-bot` rebrand pass.
  - Priority: P2
  - Context: the product needs a clearer visual and messaging system, but it should stay grounded in the current MVP goals: local-first autofill, review-first trust, and a real job-workspace feel.
  - Acceptance Criteria: define an achievable naming/branding checklist for popup copy, icons, and docs without derailing the core application workflow.
  - Progress: user-facing copy now shifts toward "Apply Workspace" across the manifest, popup header, tracker labels, and README positioning; rebrand pass remains partial and intentionally scoped to copy/UI touchpoints for now.

## Todo

### P1 - Job Search & ATS Handoff

- [/] Implement multi-source job search aggregation:
  - Progress (2026-05-31): shipped a keyless MVP — `lib/job-search.js` aggregates Remotive + Arbeitnow, normalizes to a common schema (title, company, location, salary, remote, url, ATS label, source, posted, tags, description), dedupes across sources, and sorts by recency. Fetch runs in the service worker via a new `SEARCH_JOBS` message (host perms added). Results panel now shows remote/salary/type/source badges, a "Go to job post" CTA that upgrades to "Apply on <ATS>" when a known ATS link is detected, and a one-click "Save to Tracker". Covered by `tests/job-search.test.mjs`.
  - Progress (2026-05-31, cont.): added Adzuna as an optional keyed source (BYOK app id/key + country in the AI panel, stored locally; folded into `searchJobs` only when creds are present, graceful when absent).
  - Progress (2026-05-31, registry): refactored sources into a plug-and-play registry (`JOB_SOURCES` in `lib/job-search.js`) — add a board by appending one entry (`id/label/keyless/requires/available(config)/run(query,ctx)`). New `listJobSources`/`resolveActiveSources` + `GET_JOB_SOURCES` message power per-source filter chips in the search panel: every available source is on by default, the user can pick/choose, and keyed/OAuth sources appear locked (🔒) until credentials make them `available`. Config object (`{ adzuna: {...} }`) is the seam for future OAuth tokens. Covered by `tests/job-search.test.mjs` (42 tests total).
  - Progress (2026-05-31, USAJOBS): added USAJOBS (US federal jobs) as a new registry entry — demonstrates the pattern end-to-end: normalizer + `fetchUsaJobs` (Authorization-Key + User-Agent=email headers) + AI-panel email/key fields + config wiring + host permission, no other plumbing touched. Gated on email+key; appears as a locked chip until provided. Caveat to verify live: browsers may strip the `User-Agent` header on fetch, which USAJOBS uses for auth — confirm it returns results once keys are entered (otherwise we'd route it through declarativeNetRequest header rules).
  - Progress (2026-05-31, more sources + prefs): added The Muse as a fifth source (keyless, broadens beyond remote-only boards; fetches recent pages + client-filters by query). The user's source selection AND pay filter (mode/min/max) now persist across sessions in `chrome.storage.local` (`jobSearchPrefs`), seeded from saved salary memory only on first use.
  - Progress (2026-06-02, source expansion): added five more sources via the plug-and-play registry — three keyless (Remote OK, Jobicy, Working Nomads) and two BYOK keyed (Reed UK, Jooble global). Total active keyless sources: 6; keyed: 4. Host permissions added to manifest; AI settings panel has new Reed + Jooble key fields; `buildJobSearchConfig` in the SW wires them in. Added "hide unknown-salary jobs" toggle to the pay filter (`hideUnknown` flag in `payFilter` + persisted in `jobSearchPrefs`). All 63 tests passing.
  - Progress (2026-06-02, more keyless + LinkedIn): added HN Who's Hiring (Algolia, no key), We Work Remotely (RSS), remote.co (RSS) as three more keyless sources (9 keyless total). Added LinkedIn session source — service worker reads JSESSIONID via `chrome.cookies`, relays query + CSRF token to content script on any open LinkedIn tab, content script fetches from Voyager API using page session. `cookies` + `tabs` permissions added. Added ✨/🧹 AI buttons to long preview-answer cards (same `SUMMARIZE_JD` backend). 71 tests passing.
  - Remaining: on-ATS-page detail parsing depth, tracker-side indexing enhancements, OAuth job source once a partner API is available.
  - Integrate with public job APIs (e.g. Adzuna, USAJobs, or RapidAPI job endpoints) and/or scrape LinkedIn, Indeed, etc. via URL endpoint with generic app for auth initially or lazy 3l0 scraping after.

- [ ] Plan for future: OAuth or user sign-in for personalized job search (if API supports it).
- [ ] Plan for future: user-configured job sources like unemployment offices (JOBS4TN.gov) and search criteria.

#### Acceptance Criteria
- User can search jobs from multiple sources in one panel.
- Each result has a clear "Go to job post" action (ATS link if possible).
- User can save jobs to their tracker with one click.
- Tracker search/indexing is fast and reliable.

### P3 - Exploratory

- [/] Begin to implement job search results by scraping and searching multiple job pages.
  - Progress (2026-06-02): LinkedIn session scraping shipped via content-script relay (see job search aggregation progress above). HN/WWR/remote.co RSS/Algolia keyless. Remaining: Indeed scraping, broader page-scraping capability.
- [/] Evaluate identity-based profile import paths.
  - Priority: P3
  - Context: Google sign-in, ID.me, or similar identity sources may help bootstrap profile fields later, but only after the local-first and consent-first path is stable.
  - Acceptance Criteria: any future identity import remains optional, explicit-consent based, and does not weaken the current on-device default.
  - Progress (2026-05-31): shipped BYO-OAuth "Sign in with LinkedIn" (OIDC) via `chrome.identity.launchWebAuthFlow` + `identity` permission. User supplies their own LinkedIn app Client ID/Secret (stored locally), registers the shown redirect URL, and connects to pre-fill name + email into the Profile. SW handles the code→token→userinfo exchange (`lib/oauth.js` mapper is unit-tested). Stays optional/consent-based/local-first. Note: LinkedIn's public API doesn't expose job listings (partner-gated), so this is profile-import only; the job-source registry's `config` seam is ready for any future OAuth job source.

### P4 - Nice to have

- [/] Run an `axe` / a11y audit on the popup and key application-review flows.
  - Priority: P4
  - Context: the UI is becoming more workspace-like, so keyboard support, labels, alt text, and contrast should get a structured pass.
  - Acceptance Criteria: document the biggest accessibility gaps and land the highest-value fixes without bloating the MVP.
  - Progress (2026-05-31): structured manual audit written to `docs/a11y-audit.md`. Landed fixes: `popup/ux/a11y.js` derives accessible names from placeholders/titles for all unlabeled controls (run at init); icon-only Help button labeled; Enter/Space now toggles tracker card expand (the `role=button` summary); `prefers-reduced-motion` block disables non-essential animation. Remaining (documented): keyboard DnD alternative, color-contrast verification, focus-ring audit, live-region sweep, and wiring `axe-core` into Playwright e2e.
- [/] Identify visual overload segments and have AI buttons to make detailed information more concise for consumption.
  - Progress (2026-05-31): added BYOK Gemini "✨ Summarize" and "🧹 Clean up" buttons on both the Quick-add JD field and each tracker card's description. Summarize returns a scannable labeled-bullet brief; Clean up strips nav/cookie/boilerplate noise.
  - Progress (2026-06-02): ✨/🧹 buttons added to job search result cards (hover-reveal) and to preview answer cards with values > 120 chars.
  - Remaining: none — all AI button surfaces now covered.

### Deferred / blocked (FE-pass follow-ups, 2026-05-31)

Captured so they aren't lost; pick up when prioritized.

- [ ] **UX Audit batch 2 (medium priority):** #11 expanded card modal (kanban), #22 popup/standalone state sync, #24 scalar answer preview density, #26 narrative card overflow, #27 sensitive section alarming red, #30 profile single-column, #31 memory bubble hover/connector, #33 memory delete confirm+danger.
- [ ] **Wire `axe-core` into the Playwright e2e.** *Blocked here:* adding `@axe-core/playwright` needs an `npm install` to update `package-lock.json`, and the e2e Docker image runs `npm ci` (requires a matching lock); npm isn't available in the current dev environment.
- [/] **Refresh `screenshots/` gallery**: added `tests/e2e/screenshots.spec.mjs` — Playwright captures from headless Chromium with a chrome mock (shows UI shell/chrome but no live data). Full gallery with real populated data still needs the extension loaded in real Chrome. New captures: main-dashboard, tracker-workspace, profile-memory, job-search, ai-settings all updated.
- [ ] **a11y burndown (remaining from `docs/a11y-audit.md`):** keyboard alternative for bubble/card drag-and-drop (status `<select>` is the current path — document or enhance); automated color-contrast verification of muted text over tinted surfaces + small badges; focus-ring audit at popup vs. standalone widths.

<!--
AGENT INSTRUCTIONS:
1. Keep active items in In Progress and P1-P3 sections.
2. Keep task bullets short and scannable.
3. Move finished work into Done.
-->
