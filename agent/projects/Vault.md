# Vault linking

> Up: [[AGENT-MAIN]] · Branch `vault/hub-links` in `stash`

Goal: every note reachable from [[AGENT-MAIN]] in ≤2 meaningful hops, without flat INDEX stars. Links are derived by `scripts/build-vault-indexes.py` from naming rules + `up:` frontmatter, so routines never hand-pick link targets.

## Baseline (2026-09-25)

- 416 notes · 16 orphans (all nested READMEs in `repos/*` mirrors) · ~122 notes reachable only via an INDEX
- Star hubs: `reports/INDEX` 102 out-links, `projects/INDEX` 52, `REPOS-INDEX` 38, `notes/INDEX` 13

## Rules (target design)

- **Reports** chain prev/next within their kind (and repo); repo reports link `up` to `repos/<repo>`. Home lists the latest of each non-repo kind.
- **Repo hubs** (`repos/<x>.md`) get a generated *Vault links* block: README, KB overview, latest LOC/MINI report.
- **Project subfolders** hang off a folder hub `projects/<Folder>.md` (children block); `KB/` hangs off repo hubs.
- **Dated notes** chain prev/next + week; Home links the latest.
- **scope.md** gets a generated hub-links line; `REPOS-INDEX` retired.
- Anything else: set `up: "[[parent]]"` in frontmatter.

## Progress

- [x] Generator rewrite (`build-vault-indexes.py`): idempotent, second run changes 0 files
- [x] Removed `reports/`, `projects/`, `notes/` INDEX and `REPOS-INDEX`; fixed references (AGENT-MAIN, pmo-ff report, stash docs)
- [x] `find-orphans.py`: reachability from AGENT-MAIN, star hubs, `--check`
- [x] `check-generated-diff.py`: content-based auto-merge gate for `obn:` PRs (replaces the path allowlist)
- [x] Routines: `prompts/DAILY.md` updated; `agent/README.md` documents the naming conventions. Report-writing prompts (LOC, MINI, PMO, RSI, TIRE, USAGE) already follow them. Cloud `reports/cloud/<routine>/<date>.md` is covered.
- [x] Upstream: no PRs needed. Upstream READMEs already index nested docs; the next `sync-repos.ps1` refreshes the stale mirrors (confirmed with `-DryRun`).
- [x] PR: https://github.com/nitsuah/stash/pull/139
- [ ] After merge + next daily run: confirm `find-orphans.py` shows 0 orphans and 422/422 reachable

#### Result (2026-09-25)

- 406/422 reachable from AGENT-MAIN (382 within 3 hops); the 16 left are the stale mirrors above
- Only star hub is AGENT-MAIN's Vault map (63 links, intentional)

#### Later ideas

- Smart Connections: suggest-only pass for notes that are reachable only through a chain. Never auto-write links.
- `projects/docs/` holds 2026 Q2 leftovers (two `AUDIT_GRAPH_2026_06_09*` near-duplicates): archive or fold into project hubs.
