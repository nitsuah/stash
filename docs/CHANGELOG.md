# Changelog

> 🧭 [stash](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

Notable additions and changes to this repository.

---

## [Unreleased]

### 2026-10-30 — Installer task settings

- **Fixed:** `install-tasks.ps1` now sets StartWhenAvailable, allows running on battery and caps a run at 2 h; the schtasks defaults skipped runs on battery and never caught up after sleep.

### 2026-10-30 — Templated Reflections

- **Changed:** `daily-run.mjs` writes the note's Reflections from counts instead of asking the model, so `skip_model` is true on days with no changed mirror, no stale hub and no Monday/Saturday step. `DAILY-MODEL.md` drops the Reflections item.

### 2026-10-30 — Installer start date

- **Added:** `install-tasks.ps1 -StartDate yyyy-MM-dd` so the code-driven tasks can be registered now and first run after the Nov 4 limit reset.

### 2026-10-30 — Orchestrators and task registration

- **Added:** `agent/scripts/pipeline-run.mjs` (week-sotu, monthly-tire-kick, monthly-pmo-audit as code: pre-step script, model only when needed), `agent/prompts/SOTU-MODEL.md`, and `agent/scripts/install-tasks.ps1` (idempotent Task Scheduler registration, prints unless `-Apply`). Untested by design; the first runs are planned after the Nov 4 limit reset.

### 2026-10-30 — daily-run: DAILY as code

- **Added:** `agent/scripts/daily-run.mjs` runs the deterministic steps of `DAILY.md` with no model: once-per-day guard (fails closed), merge gate for older `obn:` PRs, `sync-repos.ps1`, the four log appends, mirror skip-gate, note skeleton (Repo Activity, vigil Tasks, Notes), vault indexes, link repair and orphan check, Monday weekly skeleton, and branch/commit/push/PR. Default is `--dry-run`; `--apply` pushes and opens the PR. It writes the git-ignored `agent/reports/daily-handoff.json` and calls `routine-run.mjs` with the new `agent/prompts/DAILY-MODEL.md` (hub synthesis, Reflections, Monday goals, Saturday review; no Bash) only when `skip_model` is false. Unautomated steps print `NOT AUTOMATED: <step>`. Tests: `agent/scripts/daily-run.test.mjs`, run in CI.
- **Changed:** `DAILY.md` gains a header saying which steps the script implements; step numbers are unchanged. `ROUTINE-RUN.md` documents the Task Scheduler registration (not registered here).

### 2026-10-30 — Retired routine cleanup

- **Removed:** `analyze-loc.py`/`.ps1` (superseded by the repo-health `loc.py`). **Archived:** backup notes for the four disabled cloud routines under `agent/routines/archive/`. **Retired:** the `ops-catchup` task (audit lives in `local-audit.mjs`).

### 2026-10-30 — Monthly routine pre-steps

- **Added:** `agent/scripts/tire_intake.py` (TIRE section 2 without a model: `bot:repo-health` `## For TIRE` intake, dedup, lockfile re-verification, `tire-input.json` with `skip_model`, ledger edits only with `--apply`), `pmo_prep.py` (per-repo `check-tasks-format` row, merged PRs since the last audit, doc dates, duplicate docs, missing standards files, `changed` flag; full sweep in Jan/Apr/Jul/Oct or `--full`) and `usage_gather.py` (workflow-run, merged PR and commit counts for the previous calendar month; scheduled-task stats or `unavailable: <reason>`). Shared helpers in `prestep_common.py`; tests with stubbed `gh`/`git` run in CI.
- **Changed:** TIRE, PMO and USAGE specs start with "run the script first; read only its JSON" and state model tiers (TIRE haiku for bump PRs, sonnet only if CI fails; PMO sonnet only for `changed` repos; USAGE haiku). TIRE ends after `--apply` when `skip_model` is true. Step numbers and section names are unchanged. The three output JSON files are git-ignored.

### 2026-10-30 — SOTU pre-step in the script

- **Added:** `agent/scripts/sotu.py` now builds routine health by default (`--routines auto`: local task `SKILL.md` names, `obn-health` and `repo-health` Actions runs, open `bot:repo-health` issue counts; unreadable fields are `unknown`), a `delta` block against the previous `sotu-data.json` with a `## Changes since last run` section, and `--verify-hints`, which writes the git-ignored sidecar `sotu-verify.json` (merged-PR keyword hits, backtick path checks, `skip_model`). `--routines path.json` and `--routines none` still work. Tests: `agent/scripts/test_sotu_prestep.py`.
- **Changed:** `agent/prompts/SOTU.md` steps 3 and 6 use these outputs: the model only judges items with hints, a quiet week gets a one-line focus note, haiku for the note and sonnet only for step 6 judgment. Step numbers are unchanged.

### 2026-10-30 — Local routine runner and jobs audit

- **Added:** `agent/scripts/routine-run.mjs` runs a routine prompt through `claude -p` and 9router via the imps kit runner, with a lock, a zero-model `--pre` skip gate (`--skip-exit`), a router probe and a one-line run log; `agent/scripts/local-audit.mjs` is the zero-model CATCHUP "Local jobs audit" (Task Scheduler, imps loop, 9router drift, local task files, obn-health and repo-health runs). Both have node tests, run in CI. Docs: `agent/prompts/ROUTINE-RUN.md`.

### 2026-10-30 — Slimmer DAILY spec

- **Changed:** `agent/prompts/DAILY.md` shrinks from 32 KB to about 16 KB (it is re-sent every turn of the daily routine). History and rationale are trimmed to one-clause rules; repo-sync and worktree prose points at the wrapper and `sync-repos.ps1`; a skip-gate runs step 2 (hub synthesis) only for repos whose mirror changed or whose hub is on the VAULT-MAP Stale hubs line; model tiers are stated; the failed cloud routine lookup and Showcase board publish run weekly (Mondays), and the publish only when the board JSON changed. Step numbers 0-4 are unchanged.
### 2026-10-30 — Routine specs trimmed for CI

- **Changed:** TIRE, SOTU, USAGE, RSI, CATCHUP and PMO now read `bot:repo-health` issues and the `obn-health`/`repo-health` Actions instead of the retired cloud eng-mini, eng-loc, week-vuln and obn-import reports. Dropped the `RemoteTrigger` lookups, the ActivityWatch section and most PR-format boilerplate in PMO; PMO now audits only repos with changes since the last audit (full sweep quarterly); RSI runs quarterly unless TIRE's Aging section is non-empty or a routine failed 2+ times.
- **Docs:** week-vuln, week-eng-loc and week-eng-mini backup notes marked superseded.
### 2026-10-30 — Lean daily brief

- **Changed:** the cloud `daily-brief` no longer writes a sanitized report or opens a PR each weekday (about 8 tool calls); Gmail is read by snippet only. `obn_health.py` drops the daily-brief, week-vuln, eng-loc and eng-mini report cadences, since those are now repo-health Action output.

### 2026-10-30 — Routines to CI: repo-health pilot

- **Added:** `.github/workflows/repo-health.yml` calls the shared `nitsuah/.github` repo-health workflow weekly (Thu 15:00 UTC): osv-scanner advisories, LOC hotspots and root hygiene, with one `bot:repo-health` issue while a HIGH/CRITICAL advisory exists.

### 2026-10-29 — Routines to CI: obn-health

- **Added:** `.github/workflows/obn-health.yml` and `agent/scripts/obn_health.py` (with tests): the weekly notes, report-cadence, placeholder-prompt, untracked-repo and vault-graph checks run with no model and keep a single issue open while red. Replaces the cloud `week-obn-import` routine, which is disabled after the first green run.

### 2026-10-29 — Hardening

- **Changed:** `tech-stack-actor` caches compiled fingerprint regexes, truncates page HTML (1 MB) before matching, and fingerprint lint rejects nested-quantifier patterns.

### 2026-10-28 — Security program plan

- **Added:** `docs/security/SECURITY-ROADMAP.md` (principles, tiers, phases, fix-once controls) and a verified OAuth client inventory; `ENDPOINT-ACL.md` now lists detected routes per repo.
- **Changed:** `docs/security/README.md` no longer treats CodeRabbit output as out of scope and states the private-advisory reporting channel.

### 2026-10-16 — SOTU scoped to tier 1–2 apps

- **Changed:** `sotu.py` reads each repo's tier live from vigil's `/api/context` (falling back to scope.md's Tier column) and covers only T1/T2 repos: ats-fill, bb-mcp, fire, motor-pool, skyview, vhs and vigil. `stash` remains out of scope as the T3 vault. Out-of-scope repos' tasks and ledger rows drop out; `--all-tiers` restores the full list. Tier drift against scope.md is reported in the report and the page header.
- **Changed:** tasks now come from TASKS.md on `origin` by default; vigil's task cache (`--vigil-tasks`) lags same-day merges by hours.
- **Changed:** `agent/prompts/SOTU.md` adds a tier-drift step and a verify step: Needs-you, kickoff and P0/P1 items are checked against merged PRs, issues, code and CI, and done items are closed at the source with docs-only PRs.

### 2026-10-15 — SOTU status sync

- **Fixed:** a full check of every open task against code, merged PRs and CI found ten more done-but-unticked items (ats-fill CWS token and listing-assets job, fire eBay toast/ledger theme/PWA and the Drive follow-up, nitsuah-io journeys-review findings, osrs `recover()`, and the ats-fill/nitsuah-io journeys callers here). They are now closed at the source.
- **Fixed:** the Portfolio Checklist was showing finished work as open. Closed ledger row F-20260930-03 (cloud daily-brief reaches vigil again, verified 10-14 and 10-15), ticked the diagrams/screenshots initiative, and emptied `priorities.json` (both initiatives and the WSJF #1 are done; the done items are kept under `done`). The matching product-repo TASKS fixes are nitsuah/fire#202, Nitsuah-Labs/nitsuah-io#575 and nitsuah/vigil#297.

### 2026-10-15 — Vertical short

- **Added:** `journeys-19s-vert`, a 19 s 1080×1920 narrated cut of the journeys spot with burned-in captions, published to `pages/assets/`. Narration is Kokoro TTS through vigil's `vigil-promo-tts` image (`promo/tts/narrate.sh`, `mix.py`); the voice lines are committed in `promo/journeys-19s-vert/vo/`. `promo/build.sh` reuses another spot's `synth.py` via `"synth"` and mixes narration for spots with `"narration"`; `render.js` exposes the spot config to the page as `window.SPOT`.

### 2026-10-14 — Visual docs CI

- **Added:** `.github/workflows/visual-docs.yml` regenerates the vault graph (`docs/screenshots/vault-graph.*`, from `agent/scripts/vault-graph-gif.js`; no labels are drawn, so no note titles appear) and renders `docs/diagrams/*.mmd` (routine pipeline, showcase loop, vault-graph render) to SVG, rewrites the README block and opens a `bot/visual-docs` PR. Runs on pushes to the prompt/routine/project/topic sources, weekly, and on demand. `scripts/visual-docs-readme.mjs` is vigil's, limited to PNG screenshots.
- **Changed:** the vault graph moved from `pages/assets/` to `docs/screenshots/` so it is committed once; `pages.yml` copies it (and the diagram SVGs) into the Pages artifact at deploy time and now also triggers on `docs/screenshots/**` and `docs/diagrams/**`. `vault-graph-gif.{js,ps1}` write to `docs/screenshots/`.
- **Changed:** `promo/spots.json` gains `"frontend": false`, links Vault Tooling and Projects features to their captures and marks code-reference features `"visual": "none"`.

### 2026-10-14 — Repo tiers

- **Changed:** `sotu.py` tiers, shared by SOTU and the showcase board. vhs and stash move up to tier I. avatar and kryptos drop to tier III, alongside farm-3j, games, gcp and osrs. The showcase board's daily pick only walks tier I, so vhs and stash gaps now get picked.
- **Fixed:** the showcase board's `actions_pr` cell is `na` unless the repo has a visual-docs workflow, matching vigil's `actions_pr_permission` rule (CodeRabbit on stash#226).
- **Fixed:** `build-vault-indexes.py` labels ISO-week reports (`sotu-2026-W41`) by week in prev/next nav instead of `undated` (CodeRabbit on stash#226). Regenerated nav included.

### 2026-10-10 — Showcase board

- **Added:** `agent/scripts/visual_board.py` scans every public tracked repo (promo manifest, screenshots, diagrams, spots, feature links, reels, vertical, brand, Pages, journeys, and the "Actions can create PRs" setting), scores each repo and picks one gap to fix today. `agent/scripts/visual-board-page.html` renders it as the [showcase board](https://claude.ai/artifact/8Atj9Y7d5SqiCFM79idAHp) artifact. `DAILY.md` gains a "Showcase board" step so daily-repo-sync refreshes it and notes the pick.
- **Fixed:** `scope.md` pointed motor-pool at `code\agent-board`, which no longer exists; the clone is `code\motor-pool` (default branch `master`).

### 2026-10-09 — Journeys page and promo spot (additive)

- **Added:** `pages/journeys.html`, a second Pages page for the journeys QA loop (review pass, nightly journeys, issue lifecycle, how to adopt), linked from the main page's nav and "Also in this repo" grid. The one-brain page, its hero video and the vault graph are unchanged.
- **Added:** `journeys-19s` spot (`pages/assets/journeys-19s.mp4`, poster `.jpg`) built from real artifacts: fire's review-pass issues, its journey names and its demo-seed screenshots. Source in `promo/journeys-19s/`; `promo/build.sh` + `render.js` + `Dockerfile` render any compose-only spot in Docker (stash has no app to capture).
- `promo/spots.json`: new `journeys` feature, the spot, and a `journeys-page` reel. The existing `brag-20s` spot and `hero` reel are untouched. FEATURES lists Journeys under AI Agent System.

### 2026-10-09 — Journeys: the low-inference "AI user" loop

- **Added:** `agent/prompts/JOURNEYS.md`: the web-repo inventory, rollout order, the three prompts where AI is used (review pass, write journeys, fix), settled rules, and the run and metrics logs. The harness lives in nitsuah/.github `journeys/` (#19); fire is the pilot.
- **Changed:** 1FLOW Phase 1 takes open `bot:journey` issues before backlog and fixes them with `Refs #N`, so the nightly closes them after 3 green runs. RSI adds input 9: monthly journey metrics, appended to JOURNEYS.md.

### 2026-10-09 — Example-file coverage target met

- **Changed:** Measured coverage of the Atlassian `examples.py` files with the `test-python` CI test list: Jira 84%, Bitbucket 82%, Statuspage 80%, Confluence 72% (all above the 30% target; 80% combined). Closes the P2 TASKS item. No test or code changes.

### 2026-10-09 — Atlassian smoke tests and SaaS header one-liners

- **Added:** `pytest` + `responses` smoke tests for the Bitbucket, Confluence and Statuspage examples (`atlassian/*/test_*_examples.py`), now run by the `test-python` CI job alongside the Jira tests. Mocked HTTP only, example.com-style placeholders, no credentials.
- Each `SAAS/*/examples.py` header gained a one-line `Quick start` example in its `Usage:` block. Comments only, no behavior change.

### 2026-10-09 — SOTU keeps every repo when vigil is reachable

- `sotu.py`: after stash#210 repointed vigil to `gh-vigil.netlify.app`, vigil answered but covered 11 of 17 tracked repos. Repos vigil skips are now filled from their own TASKS.md (source line: `vigil + local TASKS.md (...)`), and `**` markup is stripped from vigil titles. W41 report regenerated: 174 tasks across all tracked repos.

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
