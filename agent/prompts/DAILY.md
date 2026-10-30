# DAILY

> Run by the scheduled task `daily-repo-sync` (wrapper `~/.claude/scheduled-tasks/daily-repo-sync/SKILL.md`, backup in `agent/routines/`). This file is the canonical spec and wins over the wrapper.

**If short on time/turns:** finish `obn` (steps 0-4) before repo sync or worktree pruning. Other files cite steps 0-4 by number (`RSI.md`, `build-vault-indexes.py`): keep them.

**Model tiers.** Everything not listed is a plain command: run it, don't reason about it. Model work: step 2 hub synthesis (sonnet; haiku when a hub's mirror diff is a few lines; **only for changed or stale repos**, see skip-gate), `## Reflections`, Monday goal seeding, Saturday week review (all haiku). Repo Activity / Tasks / Notes are command output plus a log roll-up (haiku).

## obn

Run steps in order from 0; each logs to its own file, and a no-op run still appends a dated entry.

### 0. Once per day, and close the loop first

**Guard.** Today's run already happened if `agent/notes/<today>.md` exists on `origin/main` or an open PR is titled exactly `obn: daily note <today>`. `<today>` is the **local (America/New_York) date**, computed once into `$today` and substituted (a literal placeholder in a filter matches nothing and defeats the guard):

```powershell
$today = Get-Date -Format 'yyyy-MM-dd'
git -C C:\Users\<user>\code\stash fetch -q origin
if ($LASTEXITCODE -ne 0) { throw "git fetch failed" }
git -C C:\Users\<user>\code\stash cat-file -e "origin/main:agent/notes/$today.md" 2>$null
$noteMerged = switch ($LASTEXITCODE) { 0 { $true } 128 { $false } default { throw "cat-file failed" } }  # 128 = missing (expected)
$filter = '.[] | select(.title == "obn: daily note ' + $today + '") | .title'   # concatenate: escaped quotes break the filter in PowerShell 7
$openPr = @(gh pr list --repo nitsuah/stash --state open --limit 100 --json title --jq $filter)
if ($LASTEXITCODE -ne 0) { throw "gh pr list failed" }
```

**Fail closed:** if any check throws, log it in `obn-review.log`, make the first output line `INCOMPLETE: once-per-day guard could not run`, and stop (a failed check looks like "no note yet" and makes a duplicate PR). If `$noteMerged` or `$openPr` hits, create no second note/PR: still run close-the-loop, Repo sync and Stale worktree cleanup, append the logs, and stop.

**Close the loop on open `obn:` PRs, before steps 1-2** (they rewrite `agent/repos/**`, so pulling a merged PR touching the same files would fail). Unlike [[METRICS]]'s merge-on-green, notes get a review window.

1. **Merge gate** (stash is PUBLIC and this merges unattended). A candidate meets **all**: title starts `obn: ` and branch starts `obn/` (exact filter; never fuzzy `in:title` search, which also hits `obn-notes-run` and code PRs); not from a fork (`isCrossRepository` false); author `nitsuah`; `createdAt` (America/New_York) before today, since a note PR is never merged the day it opens.
   ```powershell
   $candidatesFilter = '.[] | select((.title | startswith("obn: ")) and (.headRefName | startswith("obn/")) and (.isCrossRepository | not) and (.author.login == "nitsuah")) | [.number, .createdAt] | @tsv'
   $candidates = @(gh pr list --repo nitsuah/stash --state open --limit 100 --json number,title,headRefName,isCrossRepository,author,createdAt --jq $candidatesFilter)
   if ($LASTEXITCODE -ne 0) { throw "gh pr list failed" }
   $candidates = @($candidates | ForEach-Object { $n, $c = $_ -split "`t"; if ([datetime]::Parse($c).ToLocalTime().ToString('yyyy-MM-dd') -lt $today) { $n } })
   ```
   None: skip to 3.
2. Per candidate:
   - **Routine-owned check:** run from the stash root `git fetch origin main "pull/$pr/head"` then `python agent/scripts/check-generated-diff.py origin/main FETCH_HEAD`. It allows only dated notes (`agent/notes/YYYY-MM-DD.md` / `YYYY-Www.md`, matched by filename pattern, never the folder: `eng-loc-notes.md` must not be auto-mergeable), `agent/repos/**`, and pure `build-vault-indexes.py` output; a hand edit in `VAULT-MAP.md` or a report fails. Exit 1: **don't merge**; name the PR and first path in `## Notes`.
   - Draft: `gh pr ready <PR>`.
   - CI green (or none): `gh pr merge <PR> --squash --delete-branch`. **Don't wait for CodeRabbit or hold over review comments**; if only a stale CodeRabbit review blocks, add `--admin`. List open threads in `## Notes`. Real stash script bugs get a follow-up PR; mirror doc drift is fixed upstream.
   - CI red: leave open, name it in `## Notes`.
3. `git -C C:\Users\<user>\code\stash checkout main` + `git pull --ff-only` so later steps read merged notes. If `main` isn't clean, log it and continue without pulling.
4. Then run steps 1-4.

### 1. Repo doc sync (obn-repo)

Run `agent/scripts/sync-repos.ps1 -Prune` (its header documents mirroring, pruning and enrichment; it exports from the default branch in git, never the working tree). Copy any `[prune-held]` line into `## Notes`; never raise `-MaxPrune` yourself. No hand-added wikilinks; step 2 must leave the `<!-- vault-links:start/end -->` block alone.

Append to `agent/logs/obn-repo.log` a section headed `## obn-repo — <YYYY-MM-DD HH:MM>` with one line per repo: `OK <repo> — <N> .md files staged`, plus `PRUNED <repo> — <paths>` (only if pruned) and `HELD <repo> — <N> stale files over -MaxPrune; nothing deleted`.

**Skip-gate.** After the sync, for each tracked repo run `git -C C:\Users\<user>\code\stash diff --stat -- agent/repos/<repo>/` (plus `git status --short` on that path for new/deleted files). A repo is **changed** if its mirror differs; a hub is **stale** if listed on the `Stale hubs` line of `agent/VAULT-MAP.md`. Step 2 runs only for changed or stale repos. None: skip step 2, log `0 repos` and say "no mirror changes" in `## Notes`.

### 2. Repo synthesis (log `obn-review.log`; not the weekly review of step 4)

Only for the skip-gate's repos. Refresh **stale hubs first** (even with no activity) and update their `Reviewed:` date. Read the repo's changed mirror files (the diff, not the whole mirror) and refresh `agent/repos/<repo>.md` (**`repos/`, plural**). Append one line per run to `agent/logs/obn-review.log`: `<YYYY-MM-DD>: obn-review run across <N> repos (<repo>, ...). All synthesis files written to C:\Users\<user>\code\stash\agent\repos\.`

### 3. Daily note

Don't delegate to `agent/prompts/AUTO.md` (no daily-note spec). Write `agent/notes/<YYYY-MM-DD>.md` (flat) with exactly four sections; if one is empty write one factual line, never a bare heading.

**## Repo Activity** — one line per repo from `agent/projects/scope.md`'s "Tracked" table that had activity today (skip the rest): `gh pr list --repo <owner>/<repo> --search "updated:>=<date>"`, same for `gh issue list`, and `git -C C:\Users\<user>\code\<repo> log --since="<date> 00:00" --oneline` (unpushed WIP). **Derive `<owner>` from `git -C <path> remote get-url origin`**: `deployer` and `nitsuah-io` are under `Nitsuah-Labs/`, and the wrong owner errors "Could not resolve to a Repository", which reads as no activity. Format: `- **<repo>**: <PR #N title (state)>; <N commits>; <issue activity>`.

**## Tasks** — P0/P1 for repos active today from vigil's MCP `get_open_tasks` (server `vigil`, `https://gh-vigil.netlify.app/api/mcp`). If unavailable, say so in one line and use each repo hub's "Open P0/P1 Tasks". Add human-needed flags from today's `daily-git-sync.log` section (branch parked N+ days, diverged pull, recurring `SKIPPED_*`); skip this source if repo sync hasn't run yet this session (don't read yesterday's entry).
**Don't re-list parked P1s:** skip future-quarter tags (`[2027-Q1]`; the weekly note covers them); list a human-gated item only if new or changed since the last daily note, else one line `Unchanged human-gated P1s: <repo> (<N>), ...`. If `.obsidian/*.json` or `agent/.obsidian/*.json` shows modified, `git -C <stash> config --get filter.obsidian-json.clean`: empty means the clean filter isn't set up here (`agent/scripts/obsidian-json-clean.py`); otherwise it's a human's real edit.

**## Notes** — factual roll-up of today's entries in `daily-git-sync.log`, `stale-worktrees.log`, `obn-repo.log`, `obn-review.log` (PULLED/SKIPPED_* counts, worktrees pruned/flagged, files staged per repo, repos reviewed). No commentary; if repo sync/cleanup hasn't run yet, say so rather than reading an older day.
**Failed cloud routine runs: Mondays only.** For each enabled cloud routine (IDs in memory `reference-cloud-routine-ids`; `RemoteTrigger list` caps at 20) call `RemoteTrigger list_runs`; list non-success runs since the previous Monday with the `get_run_log` reason (spend cap, five_hour/weekly quota, rate limit, provisioning, run-time error): `- ⚠️ <routine> <date>: <status> (<reason>)`, or `No failed cloud routine runs since <last Monday>.` Other days skip the lookup and write nothing. Don't retry here; list retries as a numbered queue in `## Tasks`, **one at a time**, only when the five-hour window has room (six at once hit the cap).

**## Reflections** — 1-3 sentences of synthesis, each pointing to something concrete named above; never a platitude, never empty.

Open a **regular, non-draft PR** (drafts piled up unmerged), title `obn: daily note <date>`, branch `obn/daily-note-<date>`. It carries **all of today's stash writes**, not just the note: uncommitted `agent/repos/**` piles up on `main`, makes Repo sync skip stash as `SKIPPED_DIRTY` and leaves cloud routines reading a stale snapshot. (`agent/logs/*.log` are gitignored; never commit them.)
- Branch **from the working tree as-is**; first commit = note + `agent/repos/**`.
- After the note (and Mon/Sat weekly note) is written: `python agent/scripts/build-vault-indexes.py` (deterministic; keep its printed changed-file list for the commit), then `python agent/scripts/fix-doc-links.py --vault --under=repos/ --unlink-dead-mirrors --write` (repairs stale hub links; add its changed files to the commit).
- `python agent/scripts/find-orphans.py --check`: exit 1 means a note outside the mirrors has no link path from `VAULT-MAP` or two share a file name. Don't hand-link or rename; name it in `## Notes` for a human. Copy its `notes / orphans / reachable / unresolved links` lines into `## Notes`.
- **Last step of the run, after Stale worktree cleanup:** commit, by exact path (never a folder), what is still uncommitted under `agent/repos/`, the dated notes, the files `build-vault-indexes.py` reported, **and stranded generator output** (every other modified `.md` under `agent/reports/`, `agent/notes/`, `agent/topics/`, plus `agent/VAULT-MAP.md`; the script only reports this run's changes, so output from an earlier run whose PR closed unmerged is otherwise orphaned). Then `python agent/scripts/check-generated-diff.py origin/main HEAD` from the stash root; for each file it names (a human edit) `git restore --source=origin/main --staged <path>` and amend. Other uncommitted files are human work: leave them, mention in `## Notes`.
- Push after `gh pr view obn/daily-note-<date> --json state -q .state`: `OPEN` push; `MERGED`/`CLOSED` open a new PR from a fresh branch instead (AGENT-MAIN, "Never push to a merged PR's branch"). Never leave commits unpushed.
- Then `git checkout main` (no `git pull` yet). Changes still under `agent/repos/` on `main` mean the sweep missed something: name it in the log.

### 4. Weekly note chain (Monday and Saturday only)

Both ride in the day's daily-note PR. Weeks are ISO (`YYYY-Www`, Monday start); `YYYY` is the **ISO year** (Sat 2027-01-02 is `2026-W53`). Compute: `python -c "import datetime as d; y,w,_=d.date.today().isocalendar(); print(f'{y}-W{w:02d}')"` or `[System.Globalization.ISOWeek]::GetYear((Get-Date))`/`GetWeekOfYear`; **never** `Get-Date -UFormat %V` (not ISO on Windows).

**Monday:** write `agent/notes/<YYYY>-W<ww>.md` unless it exists:

```
# Week <ww> — Mon <YYYY-MM-DD> to Fri <YYYY-MM-DD>

## Goals
- [ ] <up to 3, seeded from last week's review>

## Last Week Review
<one line: last week's coverage + top win, or "No review last week.">

## Key Dates

## Active Projects
<`projects/` subdirs with commits in the last 7 days (`git log -1 --format=%ci -- projects/<dir>`), or "None this week.">
```

Seed Goals from last week's "Next week priorities", then uncovered "Recurring issues", max 3. No last review: one line saying so, not blank checkboxes. Also run `python agent/scripts/suggest-links.py --write` (writes `agent/reports/link-suggestions-<date>.md`; never edits notes; don't act on it); add "review N link suggestions" under Goals and commit the report.

**Saturday:** Friday's note is merged, so all five weekdays are on `main`. Read only the Mon-Fri notes' `## Repo Activity` and `## Tasks` plus this week's note (no existing script pre-extracts Coverage/Wins yet; tracked in `docs/TASKS.md`), then **append** (never rewrite earlier sections) to `agent/notes/<YYYY>-W<ww>.md`:

```
## Week Review — Saturday <YYYY-MM-DD>
**Coverage:** <N> of 5 daily notes (missing: <dates> or "none").
**Wins:** <merged PRs / pushed commits from Repo Activity, with repo + PR #>
**Recurring issues:** <Tasks items on 2+ days, e.g. same stale worktree or parked branch>
**Goals check:** <per goal: progress shown or not; or "No goals were set.">
**Next week priorities:** <1-3 items from Recurring issues and Reflections, most important first>
```

Don't count `- [x]` (daily notes have none). No notes this week: write nothing, say so in the log. Mention the weekly note/review in the PR body.

## Repo sync

Repos: the "Tracked" table in `agent/projects/scope.md`, read live (no cached list). Per repo, follow the wrapper SKILL.md: fast-forward pull on a clean default branch only; never stash, switch branches or force. Result codes `PULLED` (commit count), `SKIPPED_DIRTY|BRANCH|DIVERGED`, each with a one-line reason. Older logs use the old names `overseer` (now `vigil`) and `auto-apply-plugin` (now `ats-fill`). Append a dated `| repo | result | commits | note |` section to `agent/logs/daily-git-sync.log`.

## Stale worktree cleanup

Per repo, per the wrapper (prune broken refs; delete merged-branch worktrees; flag, never delete, unmerged ones older than 30 days). **Squash merges count:** `git branch --merged` can't see them, so if the branch isn't merged by ancestry check `gh pr list --repo <owner/repo> --head <branch> --state merged --json number`; a merged PR makes the worktree safe to delete, and the log names that PR. Append to `agent/logs/stale-worktrees.log` in the prior format.

## Showcase board

**Mondays only**, after repo sync.
1. `python C:\Users\ajhar\code\stash\agent\scripts\visual_board.py` (writes gitignored `agent/reports/visual/visual-board.json`; don't commit it; output: repo count, portfolio score, today's pick).
2. **Publish only if the board JSON changed** versus the artifact's current `visual-board.json` (`Artifact read` it). Then `Artifact publish` to https://claude.ai/artifact/8Atj9Y7d5SqiCFM79idAHp with that `url`, `file_path` = `agent/scripts/visual-board-page.html`, `files` = `{"visual-board.json": "agent/reports/visual/visual-board.json"}`. Never create a new artifact; if the read shows the page itself was edited there, skip the publish and say so.
3. Add `Showcase: portfolio <n>% · today's pick: <repo> / <check>` to `## Tasks`. Don't do the pick in this session.

A script failure is logged and the run continues (not part of the INCOMPLETE check).

## Before you finish: prove the run did something

Check that today's run left evidence: a dated section in each of `daily-git-sync.log`, `stale-worktrees.log`, `obn-repo.log`, `obn-review.log` (on a guarded run, a one-line `SKIPPED (guard: note/PR already exists)` counts; a skip-gate run logging `0 repos` counts); today's daily-note PR is open (or the guard fired and the log says so); nothing unpushed (`git status -sb` shows no `ahead`). If any is missing, the **first line** of the final output is `INCOMPLETE: <what's missing>`.

**Then end the run.** Final line: `DONE: start a new session for follow-ups.` Take on no follow-up work or CI fixes in this session (a routine session once ran 7.5 h resending this context every turn; USAGE counts routine sessions over 2 h as `hijacked`).

## Non-goals

Never force-push, discard uncommitted work, rewrite history, or merge a note PR the same day it opened. Only fast-forward clean checkouts, prune merged worktrees, and merge a previous day's clean note PR; log everything else for a human.

If something here caused a silent failure, a repeated no-op or avoidable cleanup, fix this file directly and note what changed and why.
