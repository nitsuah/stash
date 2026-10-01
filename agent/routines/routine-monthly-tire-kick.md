---
up: "[[routines-backup]]"
kind: routine-backup
routine: monthly-tire-kick
runs: local
description: "Monthly findings fix queue + Docker health check across tracked repos, per stash/agent/prompts/TIRE.md"
---

# routine · monthly-tire-kick

> Backup of `~/.claude/scheduled-tasks/monthly-tire-kick/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

**USAGE PREFLIGHT (added 2026-09-26; do this before anything else):** call `get_usage`. If the weekly window is at 75% or more, or the 5-hour window is at 50% or more, make the first line of your output `DEFERRED: weekly <n>% / 5h <n>%` and stop without doing any work. The `ops-catchup` routine (stash/agent/prompts/CATCHUP.md) schedules a spaced re-run after the next weekly reset. A DEFERRED run is expected and costs almost nothing. A run that starts and dies mid-way on quota wastes the tokens it already spent.

You are running the Tire Kick cycle: the findings fix queue plus the repo health check.

1. Read `C:\Users\ajhar\code\stash\agent\prompts\TIRE.md` in full and follow it exactly. It is the canonical spec: git triage, findings intake into `agent/reports/findings-ledger.md`, fixing `quick` items (at most 5 PRs), the Docker health check sweep, and the report + ledger PR to stash.
2. Before starting, `git -C C:\Users\ajhar\code\stash pull --ff-only` so you read the latest reports and ledger. If stash is dirty or not on main, don't touch the user's checkout and don't use a worktree (stash's gitleaks pre-commit hook fails from one, 2026-09-24): still run the §3 fixes and the §4 sweep, but put the ledger and report changes in your final output for a human to land.
3. Repos come live from the "Tracked" table in `C:\Users\ajhar\code\stash\agent\projects\scope.md`. Don't use a hardcoded list.
4. Hard rules:
   - Never commit straight to main/master. One branch and one PR per fix.
   - Skip changes to any repo that is dirty, off its default branch, or has a user worktree outside `.claude/worktrees/`.
   - Run npm, node, pytest and builds inside Docker, not on the Windows host. Pass `-p <repo>` for `config/docker-compose*.yml` files.
   - Never force-push, rewrite history, change repo settings, rulesets or secrets, or use `--no-verify`.
   - stash is a PUBLIC repo. The ledger and report contain repo, file and package names and public advisory IDs only. No secrets, tokens, emails or personal details.
   - Only merge PRs this run opened, and only when CI is green.
5. Budget your time. If you're running long, finish the fixes you started, write the report and ledger, and list what wasn't reached, rather than doing a shallow pass.

Final output: one line each for items added, fixed (with PR links), handed off, and aging.
