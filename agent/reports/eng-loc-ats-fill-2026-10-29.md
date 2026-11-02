---
kind: eng-loc
repo: ats-fill
date: 2026-10-29
---

# eng-loc · ats-fill · 2026-10-29

> 🧭 [[repos/ats-fill|ats-fill]] · ← [[reports/eng-loc-ats-fill-2026-10-08|2026-10-08]] <!-- nav -->

HEAD: d619b02d6671fe28dd46eb21f09e991942cf0793

kind: eng-loc · repo: ats-fill · tier: T1 (vigil snapshot 2026-10-21) · mode: --report · last commit: 2026-10-28 23:24 -0400

Method: `git ls-files` + per-file `wc -l` on a `--depth 1` clone. Same exclusions as fire. Churn/author history is **not available** (shallow clone), marked "assumed: not confirmed". Per-file coverage not measured.

## Inventory Summary
- Code LOC (js/ts/html, excl. tests/promo/CSS/JSON): 17,133
- Test LOC: 11,976 across 62 files. Largest test file `tests/job-search.test.mjs` at 965 LOC, under the threshold.
- Container: `Dockerfile` present.

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `content/content.js` | 1,906 | JS | Content script: message dispatch, job-info enrichment, form answer fill |
| 2 | `lib/job-search.js` | 1,623 | JS | Job search: platform-specific scraping and salary parsing |
| 3 | `popup/tracker/tracker-handlers.js` | 1,022 | JS | Tracker popup DOM handlers |
| 4 | `popup/tracker/tracker-ui.js` | 930 | JS | Tracker popup rendering |
| 5 | `popup/popup.html` | 930 | HTML | Popup markup (structure not inspected) |
| 6 | `lib/tracker.js` | 766 | JS | Application tracker storage/logic |
| 7 | `lib/form-filler.js` | 671 | JS | Form fill logic |
| 8 | `content/form-filler.js` | 658 | JS | Form fill logic (content side) |
| 9 | `lib/gemini.js` | 552 | JS | Gemini API client |
| 10 | `popup/search/job-search.js` | 536 | JS | Popup job-search UI |

Note: `lib/form-filler.js` and `content/form-filler.js` share a name across the lib/content split. Whether they overlap in responsibility is assumed, not verified. Same for `lib/job-search.js` and `popup/search/job-search.js`.

## Risk Rank

- **High — `content/content.js`**: 1,906 LOC content script mixing message dispatch (`switch (msg?.type)` ≈L84), job-info enrichment (`enrichJobInfo`, ≈L424, ~39 lines), and answer filling (≈L203 loop ~36 lines). Mixed concerns in one file, so the rationale is structural.
- **High — `lib/job-search.js`**: 1,623 LOC mixing platform-specific scraping and salary parsing (≈L930), plus entity decoding helpers. A large LinkedIn branch starting ≈L1404 is suspected to be >100 lines, but the closing brace was not confirmed, so it is marked "assumed: not confirmed".
- **Medium — `popup/tracker/tracker-handlers.js`**: 1,022 LOC of DOM handlers, with a ~52-line branch at ≈L111.
- **Medium — `popup/tracker/tracker-ui.js`**: 930 LOC of rendering. Structural signal weak; kept for completeness.
- **Low — `popup/popup.html`**: markup; not a complexity target by itself.

## Refactor Opportunities by Phase (suggested, not executed)

- **Phase 1, content.js**: split message dispatch from enrichment and fill. Keep `content.js` as the entry and re-export barrel. Risk: high, since it runs on third-party pages. Add a smoke test first.
- **Phase 2, job-search.js**: move each platform adapter (LinkedIn first) into its own module, behind the existing export surface. Risk: medium. Validate with `tests/job-search.test.mjs`.
- **Phase 3, tracker-handlers.js**: group handlers by feature area. Risk: low-medium. Manual QC on popup golden paths (tracker, search, interview prep).

## Validation Plan
Per LOC.md Phase 3: run the test suite in the repo's Docker setup, load the extension and smoke-test content-script injection on a sample job page, and spot-check the popup golden paths before each PR. Not run in report mode.

## Repo Summary

| Repo | Top concern | Priority | Notes |
|---|---|---|---|
| ats-fill (T1) | `content/content.js` 1,906 LOC mixed-concern script | High | Overlapping `form-filler` and `job-search` names worth checking |

Canaries: not applicable to this repo.
