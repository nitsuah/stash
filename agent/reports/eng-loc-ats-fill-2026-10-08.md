---
kind: eng-loc
repo: ats-fill
date: 2026-10-08
---

# LOC Report — ats-fill
HEAD: f56bb1ab28cc47b1d7ea30310bdae1794c91979c

> 🧭 [[repos/ats-fill|ats-fill]] · ← [[reports/eng-loc-auto-apply-plugin-2026-09-01|2026-09-01]] <!-- nav -->

Mode: `--report` (dry run, no changes made)
Date: 2026-10-08
Source: shallow clone (`--depth 1`) of `nitsuah/ats-fill` @ `f56bb1ab28cc47b1d7ea30310bdae1794c91979c`
Method: `git ls-files` (Phase 0 exclusions, **now including `*.md`/`*.mdx`**) + per-file line counts. Shallow clone has no history beyond HEAD, so churn is **assumed unavailable**.

Canaries: 0/0 (no canary file tracked in this repo)

## ⚠️ Resolved since last report (2026-09-01)
`background/service-worker.js` was the last report's #1 Critical finding at **1,314 lines, zero test coverage**. It is now **9 lines** — a thin entrypoint (`setupMessageRouter()` call only) with everything moved to `background/message-router.js` (123 lines) and 10 per-concern handler modules under `background/modules/handlers/` (`answers.js`, `interview.js`, `jobs.js`, `oauth.js`, `tracker.js`, etc., each 30–235 lines). This is exactly the extraction shape LOC.md recommends — already done, no action needed. Worth copying this pattern to the other hotspots below.

## Inventory Summary
- Tracked source files (post-exclusion, docs excluded): 134

## Top LOC Files (remaining source files, docs excluded)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `popup/popup.css` | 3,024 | CSS | Extension popup styling |
| 2 | `lib/job-search.js` | 1,620 | JS | Job-source normalizers (per-provider) |
| 3 | `content/content.js` | 1,232 | JS | Content-script injected into job pages |
| 4 | `popup/tracker/tracker-handlers.js` | 985 | JS | Tracker UI event handlers |
| 5 | `tests/job-search.test.mjs` | 941 | JS | Test file |
| 6 | `popup/tracker/tracker-ui.js` | 930 | JS | Tracker UI rendering |
| 7 | `popup/popup.html` | 910 | HTML | Popup markup |
| 8 | `content/form-filler.js` | 658 | JS | Auto-fill logic |
| 9 | `lib/tracker.js` | 594 | JS | Application tracking data layer |
| 10 | `lib/gemini.js` | 550 | JS | Gemini API client |

## Risk Rank & Rationale

1. **`content/content.js` — Medium-High**
   1,232 lines, 74 functions mixing at least 3 concerns: cross-frame message handling (`handleMessage`, `frameOwnsMessage`), form-filling orchestration (`handleFillForm`, `handleInjectAnswers`), and **per-ATS-vendor DOM scrapers** (`extractGreenhouse`, `extractAshby`, `extractLever`, and presumably more). The vendor-scraper pattern is naturally extensible (new ATS = new function) but doesn't need to share a file with message routing.

2. **`lib/job-search.js` — Medium (lower than its size suggests)**
   1,620 lines, 51 functions, but structurally it's a flat list of per-job-board normalizers (`normalizeRemotiveJob`, `normalizeArbeitnowJob`, `normalizeAdzunaJob`, `normalizeUsaJobsJob`, `normalizeMuseJob`, `normalizeRemoteOkJob`, `normalizeJobicyJob`, `normalizeWorkingNomadsJob`, `normalizeReedJob`, `normalizeJoobleJob`, ...) — same shape as stash's `examples.py` files (single clear concern: "normalize job listings," just with many sources). Per Evidence Rules this is lower risk than its line count implies, but splitting one-file-per-provider would still help navigability given how many providers now exist.

3. **`popup/tracker/tracker-handlers.js` — Low/Medium (tentative)**
   985 lines, 25 functions. Not read in structural depth this cycle; flagged "assumed: event-handler list, plausibly flat — not confirmed."

4. **`popup/popup.css` — Low**
   CSS-only, per Evidence Rules a style/maintainability smell not a complexity risk.

5. **`popup/popup.html` — Low, informational**
   Extension popup markup, not logic.

## Refactor Opportunities by Phase

**`content/content.js`**:
- Phase 1: extract the per-vendor scrapers (`extractGreenhouse`, `extractAshby`, `extractLever`, and any siblings) into `content/extractors/<vendor>.js`, mirroring the `background/modules/handlers/` pattern already proven in this repo.
- Phase 2: extract message-handling (`handleMessage`, `frameOwnsMessage`, `matchesDomain`, the extension-context guards) into `content/message-bridge.js`.
- Phase 3: leave `content.js` as the orchestration entrypoint, importing extractors and the message bridge.

**`lib/job-search.js`** (optional, lower priority given single-concern structure):
- Phase 1: split per-provider normalizers into `lib/job-sources/<provider>.js`, re-exporting all from `job-search.js` as a barrel — purely a navigability improvement, not a correctness-risk fix.

## Validation Plan (for eventual `--refactor`)
- No `Dockerfile`/`docker-compose.yml` found at repo root — this is a browser extension; validate via the existing test suites (`tests/job-search.test.mjs`, `tests/background-router.test.mjs`, `tests/e2e/*.spec.mjs`) plus manual load-unpacked smoke test in a browser.
- `content.js` has no dedicated test file found (`tests/` has `job-search.test.mjs` and `background-router.test.mjs`, nothing named for content-script extraction) — add a smoke test per vendor extractor before splitting, or at minimum a fixture-based test for `extractGreenhouse`/`extractAshby`/`extractLever`.
- Flag `content.js` as needing manual QC on real job-posting pages (Greenhouse/Ashby/Lever) before merge — DOM-scraping logic is brittle to page-structure changes in ways unit tests may not catch.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| ats-fill | `content/content.js` (mixed message-routing + per-vendor scrapers) | Medium-High | Previous #1 finding (`service-worker.js`, 1,314 LOC) is fully resolved via a handler-module split — reuse that pattern here |

## Ordered Next-Cycle Targets (this repo)
1. `content/content.js` — extract per-vendor extractors + message bridge (Medium-High)
2. `lib/job-search.js` — split per-provider normalizers (Low/Medium, optional)
3. `popup/tracker/tracker-handlers.js` — structural read to confirm/deny risk (Low/Medium, tentative)

## Deferred / Not Flagged
- `popup/popup.css` — CSS-only.
- `popup/popup.html` — markup, not logic.
- `background/service-worker.js`, `background/message-router.js`, `background/modules/handlers/*` — already well-factored, confirmed this cycle.

## Assumptions / Unconfirmed
- Churn/author-frequency signals for all files: **assumed unavailable** — shallow clone has no history beyond HEAD.
- `tracker-handlers.js` internal structure: not confirmed by a full read this cycle.
