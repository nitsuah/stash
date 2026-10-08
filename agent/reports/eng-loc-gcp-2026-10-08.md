# LOC Report — gcp
HEAD: c58f7290134b154bb234fdbfef8c7a73e08b0d8f

---
kind: eng-loc
repo: gcp
date: 2026-10-08
---

> 🧭 [[repos/gcp|gcp]] · ← [[reports/eng-loc-gcp-2026-07-29|2026-07-29]] <!-- nav -->

Mode: `--report` (dry run, no changes made)
Date: 2026-10-08
Source: shallow clone (`--depth 1`) of `nitsuah/gcp` @ `c58f7290134b154bb234fdbfef8c7a73e08b0d8f`
Method: `git ls-files` (Phase 0 spec exclusions applied) + per-file line counts — actual counts, not estimated. Shallow clone has no history beyond HEAD, so churn signals are **assumed unavailable**.

Canaries: 0/0 (no canary file tracked in this repo)

## Inventory Summary
- Tracked source files (post-exclusion): 52
- Small repo; top-by-size list is almost entirely code (Python + JS) and tests, with `LICENSE` as the only non-code outlier.

## Top LOC Files (all tracked files, unfiltered by type)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `gcp/copy_folder.py` | 1,079 | Python | **Code** — Drive folder copy/sync tool |
| 2 | `LICENSE` | 674 | Text | License file |
| 3 | `apps/server.js` | 635 | JS | Express server (OAuth + API routes) |
| 4 | `tests/test_q3_features.py` | 602 | Python | Test file |
| 5 | `tests/test_gcp_setup.py` | 562 | Python | Test file |
| 6 | `apps/public/styles.css` | 513 | CSS | Stylesheet |
| 7 | `tests/test_roadmap_2026.py` | 498 | Python | Test file |
| 8 | `tests/test_main.py` | 377 | Python | Test file |
| 9 | `gcp/gcp_setup.py` | 376 | Python | Setup/config script |
| 10 | `tests/test_copy_folder_extended.py` | 369 | Python | Test file |

## Top Code Files (the actual refactor-candidate pool, excluding tests)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `gcp/copy_folder.py` | 1,079 | Python | Drive folder copy/sync tool |
| 2 | `apps/server.js` | 635 | JS | Express server |
| 3 | `gcp/gcp_setup.py` | 376 | Python | Setup/config |
| 4 | `apps/public/app.js` | 324 | JS | Frontend script |

## Risk Rank & Rationale

1. **`gcp/copy_folder.py` — Medium**
   1,079 lines across 22 top-level functions. Structural signal confirmed: at least 6 distinct concerns live in one file — MIME filtering (`_mime_matches`, `_file_passes_filter`), auth/service setup (`authenticate_and_authorize`, `create_drive_service`), recursive copy (`copy_child_objects` spans lines 429–572, **~143 lines**, over the ~80-line threshold), permission copying (`_copy_permissions`, 86 lines), duplicate detection (`find_duplicate_files`), and CSV reporting (`write_duplicate_report`, `compare_csv_files`). Risk is tempered by **confirmed test coverage**: `tests/test_copy_folder.py` (10 tests) + `tests/test_copy_folder_extended.py` (23 tests) exercise this file directly, so a phased extraction has a safety net already in place — this is why it's Medium rather than High despite the size and function-length signal.

2. **`apps/server.js` — Medium-High**
   635 lines mixing token encryption/decryption (`encrypt`/`decrypt`), token persistence (`loadTokens`/`saveTokens`), OAuth client construction (`getAuthenticatedClient`), and ~9 Express route handlers (`/api/config`, `/oauth2callback`, `/api/gmail/list`, `/api/calendar/create`, `/api/gemini/query`, etc.) all in one file — a classic "kitchen sink" server entrypoint. **No test file found** for `server.js` (`find . -iname "*server*.spec.js" -o -iname "*.test.js"` returned nothing), so this carries more risk than `copy_folder.py` despite being smaller, per Evidence Rules' coverage signal.

3. **`gcp/gcp_setup.py` — Low (tentative)**
   376 lines, not read in structural depth this cycle. Flagged as "assumed: setup/config script, likely procedural and flat — not confirmed" per Evidence Rules; defer a closer read to next cycle before ranking higher.

4. **`apps/public/styles.css` — Low**
   CSS-only, per Evidence Rules a style/maintainability smell not a complexity risk.

## Refactor Opportunities by Phase

**`gcp/copy_folder.py`**:
- Phase 1 (lowest risk): extract MIME filtering helpers (`_resolve_mime_aliases`, `_mime_matches`, `_file_passes_filter`) into `gcp/mime_filters.py`. Existing tests should cover this via the public `copy_child_objects` entrypoints — re-export from `copy_folder.py` to keep call sites unchanged.
- Phase 2: extract duplicate-detection + CSV reporting (`find_duplicate_files`, `_csv_safe`, `write_duplicate_report`, `compare_csv_files`) into `gcp/dedup_report.py`.
- Phase 3 (highest risk, do last): split the 143-line `copy_child_objects` into a smaller orchestration function plus extracted helpers for permission copying and progress tracking (`_copy_permissions`, `_create_progress_tracker`, `_log_progress_if_needed`, `_log_progress_summary` are already separate — the remaining body is the actual recursive-copy loop).

**`apps/server.js`**:
- Phase 1: extract `encrypt`/`decrypt`/`loadTokens`/`saveTokens` into `apps/lib/token-store.js`.
- Phase 2: extract `getOAuthCredentials`/`isDemoModeActive`/`getAuthenticatedClient` into `apps/lib/auth.js`.
- Phase 3: split the route handlers into an Express router module per concern (e.g. `routes/auth.js`, `routes/gmail.js`, `routes/calendar.js`, `routes/gemini.js`), mounted from a thin `server.js`.
- Needs a smoke test added first (no existing coverage) per the Validation Plan below.

## Validation Plan (for eventual `--refactor`)
- `Dockerfile` found at `apps/` root (`apps/Dockerfile`) — use it to run `apps/server.js` for smoke testing per LOC.md Phase 3 guidance.
- `gcp/copy_folder.py`: run `pytest tests/test_copy_folder.py tests/test_copy_folder_extended.py` after each extraction phase — tests already exist and should catch regressions.
- `apps/server.js`: **no test suite exists** — add at minimum a smoke test (server boots, `/api/config` responds) before any extraction, since there's currently no automated safety net for this file. Flag OAuth/token-handling changes for manual QC regardless of test results — security-sensitive surface.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| gcp | `apps/server.js` (mixed concerns, zero test coverage) | Medium-High | `copy_folder.py` is bigger but already has 33 tests covering it; `server.js` has none |

## Ordered Next-Cycle Targets (this repo)
1. `apps/server.js` — add smoke test, then extract token-store + auth modules (Medium-High)
2. `gcp/copy_folder.py` — extract MIME filters and dedup/report modules first, defer the 143-line copy loop to last (Medium)
3. `gcp/gcp_setup.py` — structural read to confirm/deny refactor need (Low, tentative)

## Deferred / Not Flagged
- `apps/public/styles.css` — CSS-only, style smell not complexity risk.
- `LICENSE` — not source code.
- `tests/*.py` — test files, not refactor targets themselves.

## Assumptions / Unconfirmed
- Churn/author-frequency signals for all files: **assumed unavailable** — shallow clone has no history beyond HEAD.
- `gcp/gcp_setup.py` structural shape: not confirmed by a line-level read this cycle.
