# DAILY

> Tasks to automate daily.

**Status:** this file was created empty on 2026-06-25 (PR #58/#60) and never filled in — which is why `daily-git-sync` and `stale-worktrees` stopped producing logs that same day and stayed silent for 69+ days. Filled in 2026-09-02 and wired to a real trigger: Claude Code scheduled task `daily-repo-sync` (see `~/.claude/scheduled-tasks/daily-repo-sync/SKILL.md`), which runs this routine on a cron instead of relying on someone remembering to invoke it.

**Reordered 2026-09-16:** `obn` (below) now runs *first*, not last. `obn-review.log` showed this file's sections only completed end-to-end on Jun 25, Sep 11, and Sep 16 — big gaps — because the old order made a single session churn through 17 repos of sync + worktree pruning before ever reaching the daily note, so the note (the part actually worth reading day to day) was the most likely thing to get dropped when a run ran long. There were also 3 separate cloud routines (`daily-git-sync`, `obn-repo`, `obn-notes`) independently trying to cover this same ground with their own drifted, simpler prompts instead of reading this file — disabled 2026-09-16 in favor of this file being the single source of truth, run to completion by `daily-repo-sync`.

**Priority if a run is short on time/turns:** finish `obn` completely (all 3 sub-steps, including the daily note) before spending remaining budget on repo sync across all 17 repos or worktree pruning. A daily note that never got written is a bigger silent failure than a repo that syncs a day late.

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
One line per repo *that had activity today*, checked across the same repo list as the "Repo sync" section below. For each repo:
- `gh pr list --repo nitsuah/<repo> --search "updated:>=<YYYY-MM-DD>"` — PRs opened/updated/merged today.
- `gh issue list --repo nitsuah/<repo> --search "updated:>=<YYYY-MM-DD>"` — issues opened/closed/commented today.
- `git -C C:\Users\<user>\code\<repo> log --since="<YYYY-MM-DD> 00:00" --oneline` — local commits today (catches WIP not yet pushed, which `daily-git-sync.log` shows is most repos most days).

**Owner caveat (added 2026-09-24):** not every repo lives under `nitsuah/`. `deployer` and `nitsuah-io` are under `Nitsuah-Labs/`, and `gh` returns "Could not resolve to a Repository" for `nitsuah/<repo>`, which is easy to misread as "no activity". Derive the owner from `git -C <path> remote get-url origin` instead of hardcoding it.

Format: `- **<repo>**: <PR #N title (state)>; <N commits>; <notable issue activity>` — include only the pieces that actually happened. Skip repos with zero activity entirely; don't list all 17 repos as "no activity", that's noise.

**## Tasks**
Open P0/P1 items pulled straight from each active-today repo's synthesis file (`agent/repos/<repo>.md`, "Open P0/P1 Tasks" section, just refreshed by obn-review above), plus anything today's dated section of `agent/logs/daily-git-sync.log` explicitly flags as needing a human (a branch parked N+ days, a diverged pull, a recurring `SKIPPED_DIRTY`/`SKIPPED_BRANCH`) — if repo sync (below) hasn't run yet this session, skip this source rather than reading yesterday's stale log entry.

**## Notes**
A factual roll-up of what today's automation runs actually did, read from today's dated entries in `agent/logs/daily-git-sync.log`, `agent/logs/stale-worktrees.log`, `agent/logs/obn-repo.log`, and `agent/logs/obn-review.log`: counts of PULLED/SKIPPED_* results, worktrees pruned or flagged, `.md` files staged per repo, repos reviewed. Summary of the logs, not commentary — save interpretation for Reflections. If repo sync/worktree cleanup haven't run yet this session, note that plainly rather than reading a prior day's log.

**## Reflections**
1-3 sentences of actual synthesis across the sections above — a pattern worth a human's attention (e.g. several repos stuck on the same shared branch for a week, a repo with no activity in a long stretch, a blocker recurring across runs). This is the one section allowed to be interpretive, but every sentence must point back to something concrete already named above — never a generic platitude, and never left empty.

**Before writing today's note, close the loop on yesterday's** (auto-merge-later, added 2026-09-16 — distinct from [[METRICS]]'s immediate merge-on-green, since note content is narrative rather than machine-verified and deserves a real review window):

1. `gh pr list --repo nitsuah/stash --search "obn: daily note in:title" --state open` — find any prior day's note PR still open. Skip this whole step if none found (e.g. first run, or yesterday's already merged/closed).
2. For each one found, it has now had at least a day for review by definition (today's run is happening a day later):
   - If it's still draft, mark it ready: `gh pr ready <PR>`.
   - If CI is green (or no CI is configured on this repo) and there are no unresolved review comments: merge it — `gh pr merge <PR> --squash --delete-branch`.
   - If CI is red or there's an unresolved review comment: leave it open, and name it in today's `## Notes` section instead of merging.
3. Only after that, create and open today's note.

Open today's note as a **regular, non-draft PR** in `stash` (draft PRs are why the old batch of `obn: daily note` PRs piled up unmerged — same lesson as [[METRICS]]) — title `obn: daily note <date>`, branch `obn/daily-note-<date>`.

**The daily-note PR carries all of today's stash writes, not just the note** (added 2026-09-24). Steps 1–2 above plus Repo sync and Stale worktree cleanup below all write `agent/repos/**` into this vault. (They also append to `agent/logs/*.log`, but `*.log` is gitignored on purpose, so logs stay local and never go in the PR.) Before this rule the `agent/repos/**` writes were never committed. They piled up as 88+ uncommitted files on `main`, which made the Repo sync step skip `stash` as `SKIPPED_DIRTY` every day. Worse, every cloud routine clones `stash` from GitHub and reads `agent/repos/*.md`, so it was working from a snapshot several days stale while the local copies stayed current. So:
- Create the `obn/daily-note-<date>` branch **from the working tree as-is**, so the uncommitted writes come along. Commit the note and `agent/repos/**` together in the first commit.
- **Last step of the whole run, after Stale worktree cleanup:** commit whatever is still uncommitted under `agent/repos/` onto the same branch, then `git push`. The open PR picks it up automatically. Never leave commits on the branch unpushed; a squash-merge would orphan them.
- Then `git checkout main`. Do not `git pull` yet: those files are now committed on the branch, so `main` should be clean. If `git status` on `main` still shows changes under `agent/repos/`, the sweep missed something. Name it in the log instead of ignoring it.
- Only commit paths under `agent/repos/` and `Daily Notes/`. Any other uncommitted file in `stash` is a human's in-progress work: leave it alone and mention it in `## Notes`.

## Repo sync

For each repo in the list below, checked out at `C:\Users\<user>\code\<repo>`:

1. `git status --short --branch`.
2. If clean and on the default branch (`main`/`master`): `git pull --ff-only`. Log `PULLED` with the commit count pulled.
3. If dirty (uncommitted changes) or on a non-default branch: **skip, do not stash, do not switch branches.** Log `SKIPPED_DIRTY` or `SKIPPED_BRANCH` with a one-line reason. This is someone's in-progress work — never touch it automatically.
4. If the pull would not fast-forward (diverged history): skip and log `SKIPPED_DIVERGED` — this needs a human to resolve, not automation.

Canonical repo list: `agent/projects/scope.md`'s "Tracked" table. The list below is a cached copy kept in sync manually — if you notice it's drifted from scope.md, trust scope.md and fix this line: `agent-board`, `auto-apply-plugin`, `avatar`, `bb-mcp`, `darkmoon`, `deployer`, `farm-3j`, `fire`, `games`, `gcp`, `kryptos`, `nitsuah-io`, `osrs`, `overseer`, `skyview`, `stash`, `vhs`.

Log to `stash/agent/logs/daily-git-sync.log`, appending a new dated section in the same `| repo | result | commits | note |` table format as prior runs — don't overwrite history.

## Stale worktree cleanup

For each repo with local git worktrees (`git worktree list`):

- Prune broken worktree refs (`git worktree prune`).
- Delete worktrees for branches already merged to the default branch.
- Flag (don't delete) worktrees older than 30 days that are *not* merged — those need a human decision.

Log to `stash/agent/logs/stale-worktrees.log` in the same format as prior runs.

## Non-goals

This routine never: force-pushes, discards uncommitted work, rewrites history, or merges a note PR the same day it was opened. It only fast-forwards clean checkouts, prunes already-merged worktrees, and merges a *previous* day's note PR once it's clean and had a full review window — everything else is logged for a human to act on.

## Continuous improvement

After each run, if something in this file caused a silent failure, a repeated no-op, or avoidable manual cleanup, fix it here directly rather than letting it recur — that's exactly how the two "Status" fixes above (the empty-file silence and the `agent/repo/` vs `agent/repos/` path bug) got caught. Note briefly what changed and why when you do.
