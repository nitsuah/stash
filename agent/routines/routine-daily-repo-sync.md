---
up: "[[routines-backup]]"
kind: routine-backup
routine: daily-repo-sync
runs: local
description: "Daily git-pull sweep + stale-worktree cleanup across all nitsuah/Nitsuah-Labs owned repos"
---

# routine · daily-repo-sync

> Backup of `~/.claude/scheduled-tasks/daily-repo-sync/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

You are running the daily repo-sync routine defined in `C:\Users\ajhar\code\stash\agent\prompts\DAILY.md`. Read that file first; it is the canonical spec and it wins over anything below. It covers step 0 (once-per-day check + merging open `obn:` PRs), the daily note, the Monday weekly note and the Saturday week review (moved here from the cloud routines on 2026-09-24), and committing `agent/repos/**` via the daily-note PR.

Only if DAILY.md is missing or unreadable, fall back to the repo-sync steps below and skip the note steps entirely.

Repos (all local at `C:\Users\ajhar\code\<repo>`): agent-board, auto-apply-plugin, avatar, bb-mcp, darkmoon, deployer, farm-3j, fire, games, gcp, kryptos, nitsuah-io, osrs, overseer, skyview, stash, vhs.

For each repo:
1. Run `git -C <path> status --short --branch`.
2. If clean and on the default branch (main or master): run `git -C <path> pull --ff-only`. Record PULLED and how many commits came in (0 if already current).
3. If dirty (any uncommitted changes) or on a non-default branch: SKIP — do not stash, do not switch branches, do not touch anything. Record SKIPPED_DIRTY or SKIPPED_BRANCH with a one-line reason.
4. If the pull would not fast-forward (diverged history): SKIP and record SKIPPED_DIVERGED — this needs a human.
5. Never force anything, never discard local work, never resolve conflicts yourself.

Also run a stale-worktree pass: for each repo, `git -C <path> worktree list`; prune broken refs (`git -C <path> worktree prune`); delete worktrees whose branch is already merged into the default branch; flag (list only, don't delete) worktrees older than 30 days that are NOT merged.

Append two new dated sections (do not overwrite prior history) to:
- `C:\Users\ajhar\code\stash\agent\logs\daily-git-sync.log` — table: `| repo | result | commits | note |`
- `C:\Users\ajhar\code\stash\agent\logs\stale-worktrees.log` — same format as prior entries in that file (Actions taken / Live worktrees / Merged remote branches needing review / Stale live worktrees needing review)

The `.log` files are gitignored in stash on purpose: write them locally and never commit them. (Everything under `agent/repos/**` plus the dated notes `agent/notes/YYYY-MM-DD.md` / `agent/notes/YYYY-Www.md` is committed through the daily-note PR per DAILY.md, not left uncommitted.)

At the end, report a one-paragraph summary: how many repos pulled cleanly, how many were skipped and why, any worktrees cleaned up, and flag anything that looks wrong (e.g. a repo skipped for the same reason many days in a row, which usually means someone forgot about a branch).
