# LOC Report — auto-apply-plugin

Mode: `--report` (dry run, no changes made)
Date: 2026-09-01
Source: shallow clone (`--depth 1`) of `nitsuah/auto-apply-plugin` @ `80abb21cfdc025570566dbb8327ccd70a254f6e9`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Note: shallow clone — churn/author history is **not available**; marked "assumed: not confirmed" where relevant.

## Inventory Summary
- Tracked source files (post-exclusion): 97
- Total LOC counted: 22,854

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `popup/popup.css` | 4,326 | CSS | Extension popup styling |
| 2 | `lib/job-search.js` | 1,454 | JS | Job search core logic |
| 3 | `background/service-worker.js` | 1,314 | JS | Extension background/service worker |
| 4 | `content/content.js` | 1,233 | JS | Content-script injected into job pages |
| 5 | `popup/tracker/tracker-handlers.js` | 976 | JS | Tracker UI event handlers |
| 6 | `popup/tracker/tracker-ui.js` | 893 | JS | Tracker UI rendering |
| 7 | `tests/job-search.test.mjs` | 808 | JS | Test file (excluded from risk ranking) |
| 8 | `popup/popup.html` | 798 | HTML | Popup markup |
| 9 | `content/form-filler.js` | 658 | JS | Auto-fill logic for job application forms |
| 10 | `lib/tracker.js` | 594 | JS | Application tracking data layer |

## Risk Rank & Rationale

1. **`background/service-worker.js` — Critical**
   1,314 lines, ~120 function-like constructs, 7 `require`/`import` statements pulling in multiple unrelated concerns (messaging, storage, scheduling, cross-tab coordination) into one file — classic mixed-concerns signature for a browser-extension service worker. **No dedicated test file** found under `tests/` (only `tracker-storage.test.mjs` and `job-search.test.mjs` exist) — low/no test coverage confirmed by absence, not assumed. Highest-risk file in the repo.

2. **`content/content.js` — High**
   1,233 lines, ~157 function-like constructs, zero `import`/`require` statements (everything inlined in one script, typical of content-script constraints but still a strong mixed-concerns signal — DOM scraping, page-state detection, and messaging all appear to live here based on file role). **No test coverage found.** High risk, but content-script extraction needs care since content scripts often can't use ES modules directly — note as a UX/behavior-preserving constraint for `--refactor` phase.

3. **`lib/job-search.js` — Medium-High**
   1,454 lines, ~94 function-like constructs, imports from other modules already (only 1 import line, suggesting it's mostly self-contained logic). Has direct test coverage (`tests/job-search.test.mjs`, 808 lines) — the largest test file in the repo, suggesting the logic is exercised, which lowers immediate risk relative to the untested files above. Still large enough to warrant a phased split.

4. **`popup/tracker/tracker-handlers.js` — Medium**
   976 lines, ~117 function-like constructs, 10 import lines (already reasonably modularized in terms of dependencies) — suggests many small handlers rather than one sprawling concern, but no test file directly named for it. Assumed: untested — not confirmed via coverage tooling, only via file-name absence in `tests/`.

5. **`popup/tracker/tracker-ui.js` — Medium**
   893 lines, ~86 function-like constructs, 4 imports. Same untested-by-name-match caveat as above. Paired with `tracker-handlers.js` — likely candidates for a joint refactor pass (UI + handlers for the same feature).

6. **`content/form-filler.js` — Low-Medium**
   658 lines. Single clear concern (form filling) by name and role; lower priority than the multi-concern files above pending closer inspection.

7. **`popup/popup.css` (4,326 lines) — Low (excluded per guardrail)**
   CSS-only large file — per LOC.md guardrails, a style/maintainability item, not a complexity risk. Notably the single largest file in the repo by a wide margin; still deferred to a design-system pass per spec, but flagged here since its size dwarfs every code file.

## Refactor Opportunities by Phase

**`background/service-worker.js`** (Critical):
- Phase 1: Extract message-routing/dispatch (the `chrome.runtime.onMessage` handlers) into `background/message-router.js`, re-exported from the original file as the entry point — smallest safe cut.
- Phase 2: Extract storage/state-sync logic into `background/state-sync.js`.
- Phase 3: Extract scheduling/alarm logic (if present) into `background/scheduler.js`.
- Add a smoke test for the message-router extraction before Phase 2, since this file currently has zero coverage.

**`content/content.js`** (High):
- Phase 1: Extract DOM-scraping/selector logic into `content/scrapers.js` — pure functions, easiest and lowest-risk cut given content-script constraints (no bundler assumed).
- Phase 2: Extract page-state detection into `content/page-state.js`.
- Flag for manual QC: content scripts run against live third-party job-site DOMs; any extraction needs a manual smoke test against a real job posting page, not just unit tests, before merge — call this out explicitly in the PR description per LOC.md's UX/QC guardrail.

**`lib/job-search.js`** (Medium-High):
- Phase 1: Extract the largest cohesive sub-concern (search-query building vs. result-parsing, based on file role) into a sibling module; existing test file should catch regressions.

## Validation Plan (for eventual `--refactor`)
- No `Dockerfile`/`docker-compose.yml`/devcontainer found in repo root or `.devcontainer/` in this pass — per LOC.md Phase 3, a `--refactor` cycle should spin up an appropriate Node/Chrome-extension test harness rather than assuming host-run is safe, or confirm none is needed for a browser-extension project.
- Run `node --test` / existing test runner (`tests/job-search.test.mjs`, `tests/tracker-storage.test.mjs`) before and after each extraction.
- For content-script and service-worker changes: manual load-unpacked smoke test in a Chromium instance is the minimum bar beyond automated tests, since these run in a browser extension context that unit tests can't fully cover.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| auto-apply-plugin | `background/service-worker.js`: 1,314 lines, multi-concern, zero test coverage | Critical | Also flag `content/content.js` (untested, 1,233 lines) as a close second |

## Ordered Next-Cycle Targets (this repo)
1. `background/service-worker.js` — extract message routing, then state-sync (Critical, untested)
2. `content/content.js` — extract DOM scraping, needs manual QC on real job pages (High, untested)
3. `lib/job-search.js` — extract search/parse split, has test coverage to lean on (Medium-High)
4. `popup/tracker/tracker-handlers.js` + `popup/tracker/tracker-ui.js` — joint pass, same feature area (Medium)

## Deferred / Not Flagged
- `popup/popup.css` (4,326 lines) — CSS-only, deferred to design-system pass per guardrail, despite being the largest file in the repo.
- `popup/popup.html` (798 lines) — markup, not in scope for LOC/complexity refactor.
- `content/form-filler.js` (658 lines) — single clear concern by name; deferred pending closer inspection, not ruled out.

## Assumptions / Unconfirmed
- Churn/author-frequency signal: **assumed unavailable** — shallow clone has no history beyond HEAD.
- "No test coverage" for `service-worker.js`, `content.js`, `tracker-handlers.js`, `tracker-ui.js` is based on the absence of a like-named file under `tests/`, not a coverage-tool run — noted as a reasonably strong but not 100%-certain signal (a test could exercise these indirectly).
- Function-count / longest-function figures are regex-based approximations (`function`, arrow-with-block, method-shorthand patterns), not AST-parsed — treat as directional, not exact.
