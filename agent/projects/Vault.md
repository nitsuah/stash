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

- [ ] Generator rewrite (`build-vault-indexes.py`)
- [ ] Remove INDEX files + REPOS-INDEX, fix references
- [ ] `find-orphans.py`: flag notes with no hub, CI-style `--check`
- [ ] Update routines (`prompts/DAILY.md`, PMO, scheduled task)
- [ ] Upstream: nested READMEs orphaned in repo mirrors
- [ ] PR + before/after numbers
