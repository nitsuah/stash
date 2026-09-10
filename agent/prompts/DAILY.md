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

## obn (repo sync, review, daily note)

Three sub-steps, run in order. Each logs to its own file — an empty/no-op run still appends a dated entry so drift stays visible instead of going silent.

### 1. Repo doc sync (obn-repo)

Run `agent/scripts/sync-repos.ps1` (or an equivalent manual copy) to pull each repo's root PMO files (`CHANGELOG.md`, `FEATURES.md`, `METRICS.md`, `README.md`, `ROADMAP.md`, `TASKS.md`, etc.) and `docs/*.md` into `stash/agent/repos/<repo>/`.

Log to `C:\Users\<user>\code\stash\agent\logs\obn-repo.log`, appending (never overwrite) a new dated section in this exact format, matching prior entries:

```
## obn-repo — <YYYY-MM-DD HH:MM>
OK <repo> — <N> .md files staged
OK <repo> — <N> .md files staged
...
```

### 2. Repo review/synthesis (obn-review)

Read the synced `.md` files per repo and refresh each repo's summary at `stash/agent/repos/<repo>.md`. **Note: `agent/repos/` — plural.** A past log entry pointed at `agent/repo/` (singular), a directory that doesn't exist — that stale path is why this step stopped producing anything findable.

Log to `C:\Users\<user>\code\stash\agent\logs\obn-review.log`, appending (never overwrite) one line per run in this exact format:

```
<YYYY-MM-DD>: obn-review run across <N> repos (<repo>, <repo>, ...). All synthesis files written to C:\Users\<user>\code\stash\agent\repos\.
```

### 3. Daily note (obn)

**Do not delegate content to `agent/prompts/AUTO.md`** — it is a generic automation-agent role description with no daily-note content spec at all, which is why every `obn: daily note <date>` PR to date (#75, #78, #82, #83, #86) shipped as an empty `## Tasks` / `## Notes` / `## Reflections` skeleton and none were ever merged. Use the concrete spec below instead; it draws entirely from data steps 1–2 above already produced plus one live query, so no open-ended research is needed.

Write to `Daily Notes/<YYYY-MM-DD>.md` (vault root, matching the existing `obn: daily note <date>` PRs) with exactly these four sections. If a section genuinely has nothing to report, write one factual line saying so (e.g. "No PR/commit activity across tracked repos today.") — never leave a heading with no content under it.

**## Repo Activity**
One line per repo *that had activity today*, checked across the same repo list as the "Repo sync" section above. For each repo:
- `gh pr list --repo nitsuah/<repo> --search "updated:>=<YYYY-MM-DD>"` — PRs opened/updated/merged today.
- `gh issue list --repo nitsuah/<repo> --search "updated:>=<YYYY-MM-DD>"` — issues opened/closed/commented today.
- `git -C C:\Users\<user>\code\<repo> log --since="<YYYY-MM-DD> 00:00" --oneline` — local commits today (catches WIP not yet pushed, which `daily-git-sync.log` shows is most repos most days).

Format: `- **<repo>**: <PR #N title (state)>; <N commits>; <notable issue activity>` — include only the pieces that actually happened. Skip repos with zero activity entirely; don't list all 17 repos as "no activity", that's noise.

**## Tasks**
Open P0/P1 items pulled straight from each active-today repo's synthesis file (`agent/repos/<repo>.md`, "Open P0/P1 Tasks" section, just refreshed by obn-review above), plus anything today's dated section of `agent/logs/daily-git-sync.log` explicitly flags as needing a human (a branch parked N+ days, a diverged pull, a recurring `SKIPPED_DIRTY`/`SKIPPED_BRANCH`). One line per item, naming the source repo.

**## Notes**
A factual roll-up of what today's automation runs actually did, read from today's dated entries in `agent/logs/daily-git-sync.log`, `agent/logs/stale-worktrees.log`, `agent/logs/obn-repo.log`, and `agent/logs/obn-review.log`: counts of PULLED/SKIPPED_* results, worktrees pruned or flagged, `.md` files staged per repo, repos reviewed. Summary of the logs, not commentary — save interpretation for Reflections.

**## Reflections**
1-3 sentences of actual synthesis across the sections above — a pattern worth a human's attention (e.g. several repos stuck on the same shared branch for a week, a repo with no activity in a long stretch, a blocker recurring across runs). This is the one section allowed to be interpretive, but every sentence must point back to something concrete already named above — never a generic platitude, and never left empty.

Open the note as a draft PR in `stash` — title `obn: daily note <date>`, branch `obn/daily-note-<date>` — same as the existing PRs.

## Non-goals

This routine never: force-pushes, discards uncommitted work, rewrites history, or merges its own PRs. It only fast-forwards clean checkouts and prunes already-merged worktrees — everything else is logged for a human to act on.
