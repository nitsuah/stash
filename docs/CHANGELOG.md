# Changelog

> 🧭 [stash](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

Notable additions and changes to this repository.

---

## [Unreleased]

### 2026-10-09 — Journeys: the low-inference "AI user" loop

- **Added:** `agent/prompts/JOURNEYS.md`: the web-repo inventory, rollout order, the three prompts where AI is used (review pass, write journeys, fix), settled rules, and the run and metrics logs. The harness lives in nitsuah/.github `journeys/` (#19); fire is the pilot.
- **Changed:** 1FLOW Phase 1 takes open `bot:journey` issues before backlog and fixes them with `Refs #N`, so the nightly closes them after 3 green runs. RSI adds input 9: monthly journey metrics, appended to JOURNEYS.md.

### 2026-10-08 — Findings ledger: W41 Needs-you cleanup

- Closed F-20260930-04, -05, -09, -12 and -13 after checking them against the live repos: the stale branches are gone, the farm-3j, games and deployer dependabot PRs are merged, and vigil's checkout is back on `main`. SOTU's Needs-you list drops from 6 items to 1.
- F-20260930-03 stays open: cloud daily-brief still can't reach `gh-vigil.netlify.app` (`connect_rejected` 10-05..10-08).
- New P1 task: `sotu.py` and `DAILY.md` point at vigil's old `ghoverseer` host (404). Not repointed yet, because vigil currently covers 11 of the 17 tracked repos.

### 2026-10-07 — Visual showcase

- **Added:** Visual showcase ([standard](https://github.com/nitsuah/.github/blob/main/showcase/STANDARD.md)): `promo/spots.json` lists every shipped FEATURES.md entry and records the existing launch video(s); feature-to-video and screenshot links are still empty and get filled in on the next `/promo` run; the Pages site loads the shared expand kit (click-to-expand images, fullscreen button on videos).

### 2026-10-07 — agent-board → motor-pool, and the last stranded vault edits

- `nitsuah/agent-board` was renamed to `nitsuah/motor-pool` upstream. `scope.md`'s Tracked row now says motor-pool (`formerly \`agent-board\``, local clone still at `code\agent-board`), and the gap note that called motor-pool missing is resolved. Supersedes stash#187.
- Vault: the hub, mirror and KB overview moved to `repos/motor-pool*` and `projects/KB/motor-pool-overview.md`; mirror wikilinks were repointed (0 unresolved links). Old `eng-loc`/`eng-mini` reports keep their `agent-board` filenames as records and map to the new hub via the `formerly` alias.
- `sotu.py`: motor-pool in tier I; a malformed ledger "Seen" cell no longer crashes the build.
- Routine wrappers `routine-daily-repo-sync.md` and `routine-monthly-pmo-audit.md` dropped their cached repo lists (they still said `auto-apply-plugin`, `overseer`, `agent-board`) and read `scope.md` live. `MINI.md` and `sync-repos.ps1` say vigil instead of overseer.
- Findings ledger: fixed two rows whose Last seen date sat in the Seen column; closed F-20261007-02 (rename), -03 (`.github` is already in the Not tracked table), -04 (recovered `notes/2026-10-02.md` from closed stash#184) and -05 (dirty main checkout).
- W41 SOTU report and data; Obsidian plugin manifest bumps (nexus 5.19.1, Excalidraw 2.28.1, Local REST API 5.3.1) and graph arrows on.

### 2026-10-02 — Animated vault graph on the Pages site

- New `agent/scripts/vault-graph-gif.js` + `vault-graph-gif.ps1`: renders the `agent/` vault's link graph as a looping GIF/WebP (plus a PNG poster and a node-count JSON) into `pages/assets/`. Adapted from [U-L-M-S/obsidian-graph-gif](https://github.com/U-L-M-S/obsidian-graph-gif) (MIT): reads forces and filters from `agent/.obsidian/graph.json` and Excluded files (incl. `/regex/` entries) from `app.json`, keys notes by path so the 17 mirrors' README/ROADMAP/TASKS stay separate nodes like in Obsidian, colors nodes by vault folder, and uses the Pages dark palette. The `.ps1` runs it in a throwaway `node:22-bookworm-slim` container with ffmpeg, so nothing is installed on the host; the output is deterministic.
- `pages/index.html`: the animation now opens the "How it works" section, with a folder-color legend; new `vault-graph-gif.ps1` card under Scripts; script count 17 → 18.
- `pages/index.html` hero: 20-second overview video (`pages/assets/stash-brag.mp4`, 3.8 MB, poster `stash-brag.jpg`, `preload="none"` asks the browser not to preload the video data; the 88 KB poster still loads with the page) made with /brag-slim from the same graph simulation; linked from the README.

### 2026-10-01 — Privacy sweep before sharing the repo

- Ran `pii-scan.sh` over every tracked path (not just its default routine folders), gitleaks over all 239 commits and the working tree (clean), and a manual grep for income, holdings, health, relationship and location details.
- Removed `agent/projects/ARGUS/user_memory_index.csv` and `usermem2.csv` (personal memory exports), and reworded one personal detail in `odysseus_ecosystem_memories.csv`.
- `agent/projects/Career.md` and `Finance.md`: income and health context moved out of the repo to `~/.claude/private/<agent>-context.md`, which the prompts read when it exists.
- Reworded health-adjacent lines in two `reports/cloud/daily-checkin/` reports.
- kryptos mirror: a third party's email address was removed upstream (nitsuah/kryptos#237) and in the mirror.
- Removed accidentally committed `.playwright-mcp/` snapshots and gitignored the folder.
- Removed `projects/remora/remora.accdb` (it held a former employer's email address). The VBA source and screenshots stay. The other Access DBs and the sampler test PDF were checked and are clean.
- History still holds removed content. Purging it is a human decision, tracked in `docs/TASKS.md`.

### 2026-10-01 — GitHub Pages overview + setup guide for the agent vault

- New `pages/` static site, deployed by `.github/workflows/pages.yml` (GitHub Actions Pages source). `index.html` is a reference write-up of how the routines, vault scripts and Obsidian plugins keep `agent/` linked across 17 repos and multiple machines, and how the layered privacy model works. `setup.html` is a buildout guide: clone + hooks + clean filter, plugins and the `obsidian` MCP server, the `scope.md` registry, a first manual pipeline run, wrapping `prompts/*.md` as Claude skills, local scheduled tasks vs cloud routines, and adding machines.
- The folder is `pages/` rather than `site/` because `.gitignore` ignores `/site` (mkdocs boilerplate).

### 2026-09-30 — Obsidian vault guide, routine backups, public-vault leak fixes

- New `agent/projects/obsidian-vault-guide.md`: vault layout and what is or isn't committed, plugins, the DAILY sync pipeline, both routine fleets, and the layered "raw stays local, synthesis gets committed" privacy model with rules for anything new that writes to the vault.
- New `agent/routines/`: public-safe backups of the 8 recurring local scheduled tasks (exported by the new `scripts/export-routines.py`, which redacts personal context and refuses to write anything that matches the PII patterns) and the 5 enabled cloud routines (sanitized snapshots from `RemoteTrigger get`), indexed by `routines-backup.md`.
- Leak fixes from a full-repo PII scan plus a gitleaks pass over all 230 commits on `main`:
  - `sync-repos.ps1` skips repos marked private in `scope.md`, and `-Prune` deletes an existing mirror of one. The private `deployer` repo's docs had been mirrored into this public repo since 2026-09-16; that mirror is now removed.
  - Three personal email addresses in `projects/docs/MONEY-MAKERS.md` are replaced with role labels.
  - `agent/.obsidian/plugins/smart-connections/data.json` was tracked despite the ignore rule; it's now untracked.
  - `.gitleaks.toml`: the Jira `clientKey` allowlist never matched in git mode (gitleaks' match starts at `clientKey"`, without the leading quote), so a full-history scan still reported the two triaged hits. With the fix, all 230 commits scan clean.
  - `pii-scan.sh` (CI) and the pre-commit hook now also cover `agent/projects`, `prompts`, `topics`, `templates` and `routines`, not just reports and notes.
- History purge and the `remora.accdb` question are left for a human (see TASKS).

### 2026-09-30 — pre-commit secret scan works from worktrees and fails closed

- `.githooks/pre-commit`: from a linked worktree, the Docker gitleaks run couldn't resolve the worktree's `.git` file (a Windows `gitdir:` path), logged `fatal: not a git repository`, scanned 0 bytes and still reported "no leaks found". The hook now mounts the common git dir and sets `GIT_DIR`/`GIT_WORK_TREE`, checks that git can read the staged diff first, and fails the commit on any gitleaks `ERR` line. Tested from a worktree and a main checkout with a dummy token (blocked), clean staging (passes) and a forced git error (blocked).
- `prompts/TIRE.md`: dropped the note that stash's hook fails from a worktree.

### 2026-09-30 — close tracked items in the same PR

- `AGENT-MAIN.md`, `ENG.md`, `QA.md` and `1FLOW.md` now spell out the close-out order: code and tests, then TASKS/ROADMAP/CHANGELOG/README updates before the last push, then a pre-merge check that the PR diff includes them. `1FLOW.md` gains the Phase 4 (Document and Close) it was missing since it was written.
- `PMO.md` step 5 reconciles merged PRs against open items before carrying anything forward.
- `docs/TASKS.md`: restored two items PR #160 garbled, dropped its duplicate test-coverage item, and flagged its six unsourced additions for review.

### 2026-09-25 — vault hub links replace flat indexes

- Removed `agent/reports/INDEX.md`, `agent/projects/INDEX.md`, `agent/notes/INDEX.md` and `agent/REPOS-INDEX.md`. `build-vault-indexes.py` now writes prev/next nav lines into reports and dated notes, plus generated *Vault links* blocks in repo and project-folder hubs and a *Vault map* in `AGENT-MAIN.md`. New stub folder hubs: `projects/{CLEANUP,COSTS,LOC,MINI,TIRE,docs}.md`.
- `find-orphans.py` reports reachability from `AGENT-MAIN` and gains `--check`. Result: 406/422 notes reachable. The 16 unreachable notes are stale repo mirrors that the next sync fixes.
- `check-generated-diff.py` replaces DAILY's path allowlist for auto-merging `obn:` PRs.
- `agent/README.md` documents the linking conventions. `prompts/DAILY.md` is updated to match.
- The vault home moved from AGENT-MAIN to `agent/VAULT-MAP.md`. Folder hubs are named `<Folder>-hub.md`, so they never collide with `prompts/<Folder>.md`. Cloud reports are named `<routine>-<date>.md` (routine prompts updated too). `find-orphans.py --check` now also fails on duplicate note names and counts unresolved links (ghost nodes).
- `enrich-mirror.py` runs inside `sync-repos.ps1`. It gives every mirrored doc `up: "[[repos/<repo>]]"` frontmatter and turns links to un-mirrored files into GitHub URLs. Result: 0 orphans.
- `fix-doc-links.py` repairs broken relative links upstream (the PMO audit runs it) and in vault notes (DAILY runs it on hubs). The first pass opened fix PRs in kryptos, skyview, agent-board and darkmoon.

### 2026-09-24 — `pmo-ff` 2027 planning reset

- `agent/scripts/sync-repos.ps1` now mirrors `docs/` recursively (subfolder paths preserved, so upstream breadcrumb links such as `../../README.md` resolve in the vault) and gains an opt-in `-Prune` switch for stale mirror copies.
- `agent/scripts/find-orphans.py` — vault orphan finder; baseline 486 notes / 241 orphans.
- `agent/REPOS-INDEX.md` — repo docs hub (outside `agent/repos/`, which the sync rewrites) linked from `AGENT-MAIN.md`.
- `agent/reports/pmo-ff-2026-09-24.md` — cross-repo summary of the 16 upstream `pmo-ff` PRs and next week's vault plan.
- Planning docs: completed 2026 items condensed into FEATURES/CHANGELOG, open 2026 Q3/Q4 items carried into 2027 Q1, breadcrumb navigation + README docs index added.

### Added
- `cloud/aws/examples.py` — boto3 examples for EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53
- `SAAS/github/examples.py` — GitHub REST API examples: repos, issues, PRs, Actions, orgs, webhooks
- `SAAS/datadog/examples.py` — Datadog API examples: metrics, monitors, dashboards, incidents, logs, downtimes
- `SAAS/slack/examples.py` — Slack Bot API examples: messages, channels, users, reactions, files, webhooks
- `SAAS/pagerduty/examples.py` — PagerDuty REST + Events API v2 examples
- `atlassian/` — Full Atlassian Cloud suite examples (Jira, Confluence, Bitbucket, Statuspage) with shared client and validator
- `cloud/iac/ubuntu-userdata.sh` — Ubuntu 22.04 EC2 bootstrap with Docker, CloudWatch, sysctl hardening
- `cloud/iac/windows-userdata.ps1` — Windows Server 2022 EC2 bootstrap with Chocolatey, IIS, CloudWatch, TLS hardening
- `git/cleanup-branches.ps1` — Multi-repo merged branch cleanup utility
- `git/sync-fork.ps1` — Fast-forward-only fork + local clone sync from upstream, with `-Install` scheduled task
- `agent/prompts/SECURITY.md` — Open-source security reconciliation playbook (audit matrix, negative-control tests, live before/after, private disclosure, CI gates, Windows/Docker pitfalls)
- `agent/` — Personal agent system (CFO, Career, Builder) and full product delivery pipeline (PMO → DevOps → QA)
- `projects/auto/` — Single-page car project board (HTML + localStorage)

### Changed
- `README.md` — Full rewrite; each section links to folder-level READMEs
- `.github/copilot-instructions.md` — Updated to reflect actual stack (Python, PowerShell, Bash, VBA, Groovy)
- `windows/bat/ldap-search-users.bat` — Expanded from one line to full set of LDAP search examples
- `projects/resume/` — Sanitized MNPI, internal tool names, employee PII, internal URLs/project keys

### Removed
- `ias/` (lowercase) — malformed scratchpad duplicate of `IAS/` scripts
- `projects/resume/friends/` — PII removed

---

## [0.1.0] — 2018

### Added
- Initial project structure: VBA/Access tools (Remora, Sampler, VMT)
- Power Failure Alarm circuit design
- Windows PowerShell and batch utilities
- Resume project data

[Unreleased]: https://github.com/nitsuah/stash/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/stash/releases/tag/v0.1.0
