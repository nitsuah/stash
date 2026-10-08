# LOC Report — stash
HEAD: 6921cdd105b7819aab23b0e981c7fdbd5daf47fb

---
kind: eng-loc
repo: stash
date: 2026-10-08
---

> 🧭 [[repos/stash|stash]] · ← [[reports/eng-loc-stash-2026-09-01|2026-09-01]] <!-- nav -->

Mode: `--report` (dry run, no changes made)
Date: 2026-10-08
Source: shallow clone (`--depth 1`) of `nitsuah/stash` @ `6921cdd105b7819aab23b0e981c7fdbd5daf47fb`
Method: `git ls-files` (Phase 0 spec exclusions applied) + per-file line counts — actual counts, not estimated. Shallow clone has no history beyond HEAD, so churn signals are **assumed unavailable** unless noted otherwise.

Canaries: 1/1 detected

## Inventory Summary
- Tracked source files (post-exclusion): 731
- Note: this repo's raw top-by-size list is dominated by Markdown docs, JSON data exports, and one binary image (`pages/assets/vault-graph.webp`, excluded from the code table). `agent/` is a PMO/notes vault embedded in the repo. Per LOC.md's Evidence Rules, size alone isn't a refactor signal — the table below separates **code** hotspots from large **non-code** files (informational only).

## Top LOC Files (all tracked files, unfiltered by type)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `agent/reports/sotu/sotu-data.json` | 2,976 | JSON | Generated report data |
| 2 | `agent/repos/darkmoon/docs/projects/conkers/CONKER_BFD_BUILD_GUIDE.md` | 1,708 | Markdown | Docs (synced from darkmoon repo) |
| 3 | `projects/resume/projects/coinbase.json` | 1,659 | JSON | Resume project data export |
| 4 | `agent/repos/motor-pool/docs/API.md` | 1,537 | Markdown | Docs (synced from motor-pool repo) |
| 5 | `agent/projects/ARGUS/Authentication-hardening.html` | 1,313 | HTML | Static report/doc |
| 6 | `agent/projects/docs/OVERSEER-COMPLIANCE.md` | 1,292 | Markdown | Docs |
| 7 | `agent/notes/eng-loc-notes.md` | 1,132 | Markdown | Prior LOC-agent inventory snapshot (agent-generated) |
| 8 | `atlassian/jira/validate_project.py` | 1,050 | Python | **Code — canary**, finished take-home, not maintained |
| 9 | `agent/repos/darkmoon/docs/archive/ROADMAP_DETAILED.md` | 723 | Markdown | Docs |
| 10 | `agent/repos/farm-3j/docs/Farm_RTS_Game_Manual.md` | 674 | Markdown | Docs |

## Top Code Files (the actual refactor-candidate pool)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `atlassian/jira/validate_project.py` | 1,050 | Python | Canary — excluded from findings (see below) |
| 2 | `cloud/aws/examples.py` | 562 | Python | AWS usage examples, 35 defs |
| 3 | `agent/scripts/vault-graph-gif.js` | 440 | JS | Vault graph render script |
| 4 | `agent/scripts/build-vault-indexes.py` | 439 | Python | Vault index/hub generator |
| 5 | `SAAS/github/examples.py` | 491 | Python | GitHub API usage examples |
| 6 | `SAAS/okta/examples.py` | 481 | Python | Okta API usage examples |
| 7 | `SAAS/datadog/examples.py` | 472 | Python | Datadog API usage examples |
| 8 | `agent/scripts/analyze-loc.ps1` | 394 | PowerShell | LOC scan script (PS port) |
| 9 | `agent/scripts/analyze-loc.py` | 382 | Python | LOC scan script |

## Risk Rank & Rationale

1. **`atlassian/jira/validate_project.py` — Canary, not a finding**
   1,050 LOC. Per LOC.md's canary table this file is a finished interview take-home that will never be fixed — flagged here only to prove detection still works (`Canaries: 1/1 detected`), not filed as a refactor target.

2. **`agent/scripts/analyze-loc.py` — Medium**
   382 lines, but `main()` alone spans **167 lines** (lines 216–382+), well past the ~80-line threshold. Structural signal confirmed: `main()` mixes TOML config parsing, file scanning, and report assembly in one function. Churn assumed unavailable (shallow clone, 1 commit in history).

3. **`agent/scripts/build-vault-indexes.py` — Medium**
   439 lines, 18+ top-level functions mixing path utilities, markdown read/write helpers, report classification, and repo-hub page generation — at least four distinct concerns in one file. No single function is egregiously long, but the concern-mixing is the structural signal per Evidence Rules.

4. **`cloud/aws/examples.py` — Low**
   562 lines, 35 small defs grouped by AWS service (EC2, S3, …). Single clear concern (flat reference snippets). Low structural risk per Evidence Rules even at this size.

5. **`SAAS/*/examples.py` (github, okta, datadog) — Low**
   Same shape as the AWS examples file. Not flagged; deferred as informational.

## Refactor Opportunities by Phase

**`agent/scripts/analyze-loc.py`**:
- Phase 1: extract the TOML/scope config parsing (already partly separated via `parse_toml_config`/`parse_scope`) out of `main()` into a `load_config()` call site, leaving `main()` as orchestration only.
- Phase 2: extract the file-scan loop and report-formatting block from `main()` into `scan_and_report(config)`, re-exporting through `main()` as a thin entrypoint.

**`agent/scripts/build-vault-indexes.py`**:
- Phase 1: extract path/markdown I/O helpers (`path_of`, `exists`, `read`, `write`, `md_files`) into a small `vault_io.py` module.
- Phase 2: extract repo-hub/report classification logic (`report_kind_and_subject`, `repo_hub`, `note_month`, `iso_week`, `chain`, `title_of`, `script_summary`) into a `vault_classify.py` module, leaving the top-level script as orchestration.

## Validation Plan (for eventual `--refactor`)
- No `Dockerfile`/`docker-compose.yml`/devcontainer found at repo root for these scripts.
- No `tests/` coverage found for `agent/scripts/*` — treat as "assumed: no test coverage — not confirmed" per Evidence Rules; add a smoke test (run script against a small fixture vault) before extracting.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| stash | `agent/scripts/analyze-loc.py` (167-line `main()`) | Medium | Canary confirmed (1/1); repo is mostly docs/notes/data by volume, real code hotspots are in `agent/scripts/` |

## Ordered Next-Cycle Targets (this repo)
1. `agent/scripts/analyze-loc.py` — split `main()` (Medium)
2. `agent/scripts/build-vault-indexes.py` — split by concern (Medium)

## Deferred / Not Flagged
- All Markdown/JSON/HTML files in the top-10-by-size table — non-code, informational only.
- `cloud/aws/examples.py`, `SAAS/github/examples.py`, `SAAS/okta/examples.py`, `SAAS/datadog/examples.py` — single clear concern, low risk, deferred.
- `atlassian/jira/validate_project.py` — canary, intentionally never refactored.

## Assumptions / Unconfirmed
- Churn/author-frequency signals for all files: **assumed unavailable** — shallow clone has no history beyond HEAD.
- Test coverage for `agent/scripts/*`: not confirmed — no `tests/` directory match found in this pass.
