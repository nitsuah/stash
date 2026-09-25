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

Round 1 (flat indexes → hubs): 406/422 reachable, 16 orphans (stale mirrors).

Round 2 (names, mirrors, links):
- Home moved to [[VAULT-MAP]]; [[AGENT-MAIN]] is the process guide again
- Unique names: folder hubs `<Folder>-hub`, cloud reports `<routine>-<date>` (4 cloud routines updated), `ARGUS/odysseus-automation-tasks`
- `enrich-mirror.py` in the sync: `up:`/`source:` frontmatter on every mirrored doc → **0 orphans**, one named cluster per repo
- `fix-doc-links.py`: ghost links 100 → 61. Upstream PRs: kryptos#224, skyview#152, agent-board#83, darkmoon#462
- Now 423/424 reachable, VAULT-MAP is the only star hub (51 links)

Still open:
- Remaining ghost links: `motor-pool` references in agent-board archive docs (wikilinks upstream), missing ARGUS attachments (png/csv), `darkmoon/docs/projects/conkers/TECH_DEBT.md` → `TODO.md`, and the in-progress `projects/KB/agent-board-overview.md`
- Graph labels are file names. To show `title:` instead, install the *Front Matter Title* community plugin (human decision)

#### Later ideas

- Smart Connections: suggest-only pass for notes that are reachable only through a chain. Never auto-write links.
- `projects/docs/` holds 2026 Q2 leftovers (two `AUDIT_GRAPH_2026_06_09*` near-duplicates): archive or fold into project hubs.
