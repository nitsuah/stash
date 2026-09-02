# DAILY

> Tasks to automate daily.

**Status:** this file was created empty on 2026-06-25 (PR #58/#60) and never filled in — which is why `daily-git-sync` and `stale-worktrees` stopped producing logs that same day and stayed silent for 69+ days. Filled in 2026-09-02 and wired to a real trigger: Claude Code scheduled task `daily-repo-sync` (see `~/.claude/scheduled-tasks/daily-repo-sync/SKILL.md`), which runs this routine on a cron instead of relying on someone remembering to invoke it.

## Repo sync

For each repo in the list below, checked out at `C:\Users\<user>\code\<repo>`:

1. `git status --short --branch`.
2. If clean and on the default branch (`main`/`master`): `git pull --ff-only`. Log `PULLED` with the commit count pulled.
3. If dirty (uncommitted changes) or on a non-default branch: **skip, do not stash, do not switch branches.** Log `SKIPPED_DIRTY` or `SKIPPED_BRANCH` with a one-line reason. This is someone's in-progress work — never touch it automatically.
4. If the pull would not fast-forward (diverged history): skip and log `SKIPPED_DIVERGED` — this needs a human to resolve, not automation.

Repos: `agent-board`, `auto-apply-plugin`, `avatar`, `bb-mcp`, `darkmoon`, `deployer`, `farm-3j`, `fire`, `games`, `gcp`, `kryptos`, `nitsuah-io`, `osrs`, `overseer`, `skyview`, `stash`, `vhs`.

Log to `stash/agent/logs/daily-git-sync.log`, appending a new dated section in the same `| repo | result | commits | note |` table format as prior runs — don't overwrite history.

## Stale worktree cleanup

For each repo with local git worktrees (`git worktree list`):

- Prune broken worktree refs (`git worktree prune`).
- Delete worktrees for branches already merged to the default branch.
- Flag (don't delete) worktrees older than 30 days that are *not* merged — those need a human decision.

Log to `stash/agent/logs/stale-worktrees.log` in the same format as prior runs.

## obn (daily note)

Generate today's daily note per the existing `agent/prompts/AUTO.md`/vault convention and open it as a draft PR in `stash`, same as the existing `obn: daily note <date>` PRs. Keep this lightweight — it's low priority relative to the sync and worktree steps above.

## Non-goals

This routine never: force-pushes, discards uncommitted work, rewrites history, or merges its own PRs. It only fast-forwards clean checkouts and prunes already-merged worktrees — everything else is logged for a human to act on.
