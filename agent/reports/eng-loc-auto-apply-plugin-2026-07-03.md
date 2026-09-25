# ENG LOC Report: auto-apply-plugin

> 🧭 [[repos/ats-fill|auto-apply-plugin]] · ← [[reports/eng-loc-auto-apply-plugin-2026-06-25|2026-06-25]] · [[reports/eng-loc-auto-apply-plugin-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** auto-apply-plugin (auto-apply-plugin)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 1504 | `background/service-worker.js` | Unused function (heuristic): switch |
| 1145 | `content/content.js` | — |
| 972 | `popup/tracker/tracker-handlers.js` | — |
| 893 | `popup/tracker/tracker-ui.js` | — |
| 550 | `lib/gemini.js` | — |
| 537 | `lib/form-filler.js` | Unused function (heuristic): setTimeout |
| 537 | `lib/tracker.js` | — |
| 517 | `popup/search/job-search.js` | — |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 16 | `popup/ats/ats.js` | — |
| 19 | `popup/ux/consent.js` | — |
| 26 | `popup/tracker/tracker-state.js` | — |
| 29 | `tests/e2e/chrome-mock.js` | — |
