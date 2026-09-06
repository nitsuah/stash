# LOC Report — stash

Mode: `--report` (dry run, no changes made)
Date: 2026-09-01
Source: full clone of `nitsuah/stash` @ `c6cdaf6f79e0a9770d7c5f0b7395d0a443b22745`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated. Full history available, so churn signals below are confirmed via `git log`, not assumed.

## Inventory Summary
- Tracked source files (post-exclusion): 429
- Total LOC counted: 57,310
- Note: this repo's raw top-10-by-size list is dominated by Markdown docs and one JSON data file (`agent/` is a PMO/notes vault embedded in the repo, plus a resume JSON export). Per LOC.md's Evidence Rules, size alone isn't a refactor signal — the table below separates **code** hotspots (the actual refactor candidates) from large **non-code** files (informational only).

## Top 10 LOC Files (all tracked files, unfiltered by type)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `projects/resume/projects/coinbase.json` | 1,659 | JSON | Resume project data export |
| 2 | `agent/repos/darkmoon/docs/CONKER_BFD_BUILD_GUIDE.md` | 1,589 | Markdown | Docs (synced from darkmoon repo) |
| 3 | `agent/projects/ARGUS/Authentication-hardening.html` | 1,313 | HTML | Static report/doc |
| 4 | `agent/projects/docs/OVERSEER-COMPLIANCE.md` | 1,292 | Markdown | Docs |
| 5 | `agent/notes/eng-loc-notes.md` | 1,132 | Markdown | Prior LOC-agent inventory snapshot (agent-generated) |
| 6 | `atlassian/jira/validate_project.py` | 1,051 | Python | **Code** — Jira project validation script |
| 7 | `agent/repos/agent-board/docs/API.md` | 1,004 | Markdown | Docs (synced from agent-board repo) |
| 8 | `agent/repos/darkmoon/docs/ROADMAP_DETAILED.md` | 722 | Markdown | Docs |
| 9 | `LICENSE` | 674 | Text | License file |
| 10 | `agent/repos/farm-3j/docs/Farm_RTS_Game_Manual.md` | 664 | Markdown | Docs |

## Top Code Files (the actual refactor-candidate pool)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `atlassian/jira/validate_project.py` | 1,051 | Python | Jira project validation script |
| 2 | `cloud/aws/examples.py` | 562 | Python | AWS usage examples |
| 3 | `projects/sampler/source/mouse-move.vb` | 539 | VB | Sampler tool source |
| 4 | `SAAS/github/examples.py` | 491 | Python | GitHub API usage examples |
| 5 | `SAAS/okta/examples.py` | 481 | Python | Okta API usage examples |
| 6 | `SAAS/datadog/examples.py` | 471 | Python | Datadog API usage examples |

## Risk Rank & Rationale

1. **`atlassian/jira/validate_project.py` — Medium**
   1,051 lines, 31 defs. Confirmed churn via full git history: **14 commits** touching this file — moderate, ongoing edit activity (not single-author-drop-and-forget). This is the only code file in the repo large enough and active enough to warrant a look. Structural rationale needed before calling it Critical — recommend a closer read next cycle to confirm mixed-concerns (validation rules + Jira API calls + reporting output are plausible sub-concerns for a "validate_project" script, but not confirmed in this pass).

2. **`cloud/aws/examples.py` — Low**
   562 lines, 35 defs, but **only 1 commit** in history — a single-drop example/reference file, not actively maintained code. Per Evidence Rules, low structural risk: example scripts are expected to be a flat list of independent snippets (single clear concern: "AWS examples"), not a mixed-concern hotspot.

3. **`SAAS/*/examples.py` files (github, okta, datadog) — Low**
   Same shape as the AWS examples file — a library of independent reference snippets. Not flagged; deferred as informational.

## Refactor Opportunities by Phase

**`atlassian/jira/validate_project.py`** (Medium, tentative pending structural confirmation):
- Phase 1 (next cycle, needs a closer read first): if validation-rule logic and Jira-API-call logic are interleaved, extract the Jira client calls into `atlassian/jira/client.py`, leaving `validate_project.py` as the rules/orchestration layer.
- This report does not have enough structural evidence yet to commit to a phase plan beyond this — flagged as "assumed: mixed concerns plausible, not confirmed" per Evidence Rules. Recommend a Phase-1-only structural read before drafting a full extraction plan.

## Validation Plan (for eventual `--refactor`)
- No `Dockerfile`/`docker-compose.yml`/devcontainer found at repo root in this pass.
- Run any existing test suite covering `atlassian/jira/` before/after extraction; none was found under a `tests/` path in this pass — flag for confirmation, as low/no test coverage would raise this file's risk rank.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| stash | `atlassian/jira/validate_project.py` (1,051 LOC, moderate churn) | Medium | Repo is mostly docs/notes/config by volume; only one real code hotspot surfaced this cycle |

## Ordered Next-Cycle Targets (this repo)
1. `atlassian/jira/validate_project.py` — structural read to confirm/deny mixed concerns before planning extraction (Medium)

## Deferred / Not Flagged
- All Markdown/JSON/HTML files in the top-10-by-size table — non-code, informational only per LOC.md scope (this agent targets source-file complexity, not doc bloat).
- `cloud/aws/examples.py`, `SAAS/github/examples.py`, `SAAS/okta/examples.py`, `SAAS/datadog/examples.py` — single clear concern (example snippets), low churn, deferred.
- `LICENSE` — not source code.

## Assumptions / Unconfirmed
- Test coverage for `atlassian/jira/validate_project.py`: not confirmed — no `tests/` directory match found in this pass; treat as "assumed: no test coverage — not confirmed" per LOC.md Evidence Rules.
- Mixed-concerns claim for `validate_project.py`: plausible from the filename/role but not confirmed by a line-level read this cycle — this report intentionally stops short of a full phase plan until that's verified, per the Evidence Rules ("never flag a file as problematic by size alone").
