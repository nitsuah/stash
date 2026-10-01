---
up: "[[routines-backup]]"
kind: routine-backup
routine: monthly-pmo-audit
runs: local
description: "Monthly PMO doc/metrics audit across all owned repos, per stash/agent/prompts/PMO.md"
---

# routine · monthly-pmo-audit

> Backup of `~/.claude/scheduled-tasks/monthly-pmo-audit/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

**USAGE PREFLIGHT (added 2026-09-26; do this before anything else):** call `get_usage`. If the weekly window is at 75% or more, or the 5-hour window is at 50% or more, make the first line of your output `DEFERRED: weekly <n>% / 5h <n>%` and stop without doing any work. The `ops-catchup` routine (stash/agent/prompts/CATCHUP.md) schedules a spaced re-run after the next weekly reset. A DEFERRED run is expected and costs almost nothing. A run that starts and dies mid-way on quota wastes the tokens it already spent.

You are running the monthly PMO audit cycle. Read `C:\Users\ajhar\code\stash\agent\prompts\PMO.md` in full and follow it exactly — it is the canonical, detailed spec (scope of review, evidence standard, PR governance, deliverable format, definition of done). Do not skip reading it; it has specific rules about never committing directly to default branches, always opening a PR per repo/theme, and never fabricating metrics.

Repos to audit this cycle: the "Tracked" table in `C:\Users\ajhar\code\stash\agent\projects\scope.md` (paths, GitHub URLs, and org already resolved there — nitsuah vs Nitsuah-Labs). Skip stash itself — it's the vault this prompt lives in, not a product repo to audit. As of 2026-09-16 that's: agent-board, auto-apply-plugin, avatar, bb-mcp, darkmoon, deployer, farm-3j, fire, games, gcp, kryptos, nitsuah-io, osrs, overseer, skyview, vhs — but scope.md is the source of truth if this list and that file ever disagree.

Before starting, check each repo's local git status — if a repo is dirty or not on its default branch, skip auditing it this cycle and note that in your report rather than disturbing someone's in-progress work. If it's clean, `git pull --ff-only` first so you're auditing current `main`.

For each repo, per PMO.md: review README/ROADMAP/TASKS/FEATURES/METRICS for staleness and contradictions (e.g. a doc claiming a PR is open when git shows it merged), verify run instructions where feasible (Docker-first), and update TASKS.md/ROADMAP.md/METRICS.md only with evidence-backed changes — never guesses. Every change goes on a branch named `pmo/<repo>/<theme>-<date>` with its own PR (use `gh pr create`), never committed straight to main/master.

After the cycle, write a summary report to `C:\Users\ajhar\code\stash\agent\reports\pmo-audit-<YYYY-MM-DD>.md` covering: repos audited, repos skipped and why, PRs opened (with links), and any doc/reality contradictions found. Keep the actual PR descriptions scoped to PMO.md's required PR body format.

This is a heavy, multi-repo operation — budget your own time, and if you're running long, finish the repos you've started and note which ones didn't get reached this cycle rather than doing a shallow pass on all of them.
