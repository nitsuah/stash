# DAILY

> Tasks to automate daily.

**Status:** this file was created empty on 2026-06-25 (PR #58/#60) and never filled in — which is why `daily-git-sync` and `stale-worktrees` stopped producing logs that same day and stayed silent for 69+ days. Filled in 2026-09-02 and wired to a real trigger: Claude Code scheduled task `daily-repo-sync` (see `~/.claude/scheduled-tasks/daily-repo-sync/SKILL.md`), which runs this routine on a cron instead of relying on someone remembering to invoke it.

**Reordered 2026-09-16:** `obn` (below) now runs *first*, not last. `obn-review.log` showed this file's sections only completed end-to-end on Jun 25, Sep 11, and Sep 16 — big gaps — because the old order made a single session churn through 17 repos of sync + worktree pruning before ever reaching the daily note, so the note (the part actually worth reading day to day) was the most likely thing to get dropped when a run ran long. There were also 3 separate cloud routines (`daily-git-sync`, `obn-repo`, `obn-notes`) independently trying to cover this same ground with their own drifted, simpler prompts instead of reading this file — disabled 2026-09-16 in favor of this file being the single source of truth, run to completion by `daily-repo-sync`.

**Priority if a run is short on time/turns:** finish `obn` completely (steps 0-4, including the daily note and, on Mon/Sat, the weekly note chain) before spending remaining budget on repo sync across all 17 repos or worktree pruning. A daily note that never got written is a bigger silent failure than a repo that syncs a day late.

## obn (close the loop, repo doc sync, repo synthesis, daily note, weekly note chain)

Run the sub-steps in order, starting with step 0. Each logs to its own file — an empty/no-op run still appends a dated entry so drift stays visible instead of going silent.

### 0. Once per day, and close the loop first

**Run once per day (added 2026-09-24).** Before anything else, check whether today's run already happened: `agent/notes/<today>.md` exists on `origin/main`, or an open PR titled exactly `obn: daily note <today>` exists. "Today" is the **local (America/New_York) date**, the same date used in the note's filename. Compute it once into a variable and substitute it; never run a filter containing a literal `<today>` placeholder, which silently matches nothing and defeats this guard:

```powershell
$today = Get-Date -Format 'yyyy-MM-dd'
git -C C:\Users\<user>\code\stash fetch -q origin
git -C C:\Users\<user>\code\stash cat-file -e "origin/main:agent/notes/$today.md"   # exit 0 = note already merged
$filter = '.[] | select(.title == "obn: daily note ' + $today + '") | .title'   # build by concatenation: backslash/backtick-escaped quotes reach gh literally in PowerShell 7 and break the filter
gh pr list --repo nitsuah/stash --state open --limit 100 --json title --jq $filter   # any output = PR already open
```

(Verified under PowerShell 7.6 on 2026-09-24: an existing date returns the title, a future date returns nothing.)

If either check hits, **don't** create a second note or PR. Do Repo sync and Stale worktree cleanup only, append the logs, and stop. On 2026-09-24 a manual run was followed by the scheduled one hours later; only a quota failure prevented a duplicate note and PR.

**Close the loop on every open `obn:` PR (run before steps 1-2).** Auto-merge-later, added 2026-09-16 and extended 2026-09-24 to cover weekly PRs. Note content is narrative rather than machine-verified, so it gets a real review window, unlike [[METRICS]]'s immediate merge-on-green. This must run **before** steps 1-2: they rewrite `agent/repos/**`, and pulling a merged PR that touched those same files would then fail.

1. **Merge gate (hardened 2026-09-24; stash is PUBLIC, so anyone can open a PR).** This step merges unattended, so a PR is a candidate only if **all** of these hold:
   - the title starts with `obn: ` **and** the branch starts with `obn/`. Use an exact filter, never GitHub's fuzzy search: `"obn: in:title"` also matches unrelated PRs like `obn-notes-run` (#100) and code PRs like #88/#89;
   - it is **not from a fork** (`isCrossRepository` is false). A stranger's fork can use the same title and branch names;
   - the **author is `nitsuah`**, the account every routine and note PR is opened as.

   ```powershell
   $candidatesFilter = '.[] | select((.title | startswith("obn: ")) and (.headRefName | startswith("obn/")) and (.isCrossRepository | not) and (.author.login == "nitsuah")) | .number'
   $candidates = @(gh pr list --repo nitsuah/stash --state open --limit 100 --json number,title,headRefName,isCrossRepository,author --jq $candidatesFilter)
   ```
   Skip to step 3 if there are none.
2. For each candidate (each is at least a day old by definition):
   - **Routine-owned check:** every changed file must be a dated note (`agent/notes/YYYY-MM-DD.md` or `agent/notes/YYYY-Www.md`), under `agent/repos/`, or a file whose **only** changes are `build-vault-indexes.py` output (`<!-- nav -->` lines, `<!-- vault-links -->` blocks, a new folder-hub stub). The script matches the note **filename pattern**, not the `agent/notes/` folder: other files live there (e.g. `eng-loc-notes.md`) and must never become auto-mergeable. It compares content, so a hand edit riding along in `VAULT-MAP.md` or a report fails, even though the generator also touches those files:
     ```powershell
     git -C C:\Users\<user>\code\stash fetch origin main "pull/$pr/head"
     python C:\Users\<user>\code\stash\agent\scripts\check-generated-diff.py origin/main FETCH_HEAD
     ```
     (Run it from the stash repo root.) If it exits 1, **don't merge**. Name the PR and the first path it prints in today's `## Notes` for a human. (Retroactive check: old note PR #92 carried 17 unrelated files, including `agent/.obsidian/` config, and was merged. This gate would have held it.)
   - If it's still a draft, mark it ready: `gh pr ready <PR>`.
   - If CI is green (or no CI is configured) and there are no unresolved review comments, merge: `gh pr merge <PR> --squash --delete-branch`.
   - If CI is red or there's an unresolved review comment, leave it open and name it in today's `## Notes` instead of merging.

   (Gate verified 2026-09-24 against every stash PR: 10 note PRs qualify. #88, #89 and #100 are never candidates, and the path check flags #92. The path regex was changed the same day when notes moved from `Daily Notes/`/`Weekly Notes/` to flat `agent/notes/`; re-verified against note, repo, `eng-loc-notes.md`, subfolder and old-folder paths.)
3. `git -C C:\Users\<user>\code\stash checkout main` and `git pull --ff-only`, so the steps below read the merged notes. `main` should be clean here, because yesterday's end-of-run sweep committed everything. If it isn't, log it and continue without pulling.
4. Only after that, run steps 1-4.

### 1. Repo doc sync (obn-repo)

Run `agent/scripts/sync-repos.ps1 -Prune`. It fetches each repo, then mirrors every `.md` on its **default branch on the remote** (`origin/HEAD`, any depth, paths preserved) into `stash/agent/repos/<repo>/`, exported from git. It never copies the working tree or the checked-out branch, so untracked, staged, locally modified, and unmerged-branch files are never published into this public vault. It skips `.github/` and a root `templates/` folder, which are repo config rather than knowledge. (2026-09-25: the old working-tree copy leaked fire's uncommitted private `docs/weekly-checkin-prompt.md` and had to be deleted by hand.)

`-Prune` removes mirrored `.md` files that no longer exist upstream: old root-level duplicates from before a repo moved its docs into `docs/`, and docs since deleted or archived. The deletions land in the daily-note PR with the rest of `agent/repos/**`. The script has a per-repo cap (`-MaxPrune`, default 25): over it, it deletes **nothing** for that repo and prints `[prune-held]`. Copy any `[prune-held]` line into the daily note's `## Notes` for a human instead of raising the cap yourself. It usually means a repo moved or renamed its docs folder.

After the export, the sync runs `enrich-mirror.py` on the fresh copies. Every mirrored doc gets `up: "[[repos/<repo>]]"` and `source:` frontmatter, and links to files the mirror doesn't carry (LICENSE, images, `.github/`) become GitHub URLs. That's vault-only; upstream is never touched. Mirror docs therefore can't be orphaned, and each repo is one cluster around its named hub.

Don't add wikilinks by hand: every mirrored doc is linked from its repo README's Docs Index, and each `agent/repos/<repo>.md` hub links that README through its generated *Vault links* block. The old "add wikilinks to <repo>.md Vault Index" action and `agent/REPOS-INDEX.md` are both retired. Step 2 may rewrite a hub's prose freely but must leave its `<!-- vault-links:start/end -->` block alone; it is regenerated anyway.

Log to `C:\Users\<user>\code\stash\agent\logs\obn-repo.log`, appending (never overwrite) a new dated section in this exact format, matching prior entries:

```
## obn-repo — <YYYY-MM-DD HH:MM>
OK <repo> — <N> .md files staged
OK <repo> — <N> .md files staged
...
PRUNED <repo> — <path>, <path>   (only when -Prune removed something)
HELD <repo> — <N> stale files over -MaxPrune; nothing deleted
```

### 2. Repo synthesis (logs to `obn-review.log`)

Renamed 2026-09-24 from "obn-review" so it isn't confused with the **weekly review** in step 4. The log file keeps its old name so its history stays in one place.


Read the synced `.md` files per repo and refresh each repo's summary at `stash/agent/repos/<repo>.md`. **Note: `agent/repos/` — plural.** A past log entry pointed at `agent/repo/` (singular), a directory that doesn't exist — that stale path is why this step stopped producing anything findable.

Log to `C:\Users\<user>\code\stash\agent\logs\obn-review.log`, appending (never overwrite) one line per run in this exact format:

```
<YYYY-MM-DD>: obn-review run across <N> repos (<repo>, <repo>, ...). All synthesis files written to C:\Users\<user>\code\stash\agent\repos\.
```

### 3. Daily note (obn)

**Do not delegate content to `agent/prompts/AUTO.md`** — it is a generic automation-agent role description with no daily-note content spec at all, which is why every `obn: daily note <date>` PR to date (#75, #78, #82, #83, #86) shipped as an empty `## Tasks` / `## Notes` / `## Reflections` skeleton and none were ever merged. Use the concrete spec below instead; it draws entirely from data steps 1–2 above already produced plus one live query, so no open-ended research is needed.

Write to `agent/notes/<YYYY-MM-DD>.md` (flat, no subfolders; moved from the vault-root `Daily Notes/` folder on 2026-09-24) with exactly these four sections. If a section genuinely has nothing to report, write one factual line saying so (e.g. "No PR/commit activity across tracked repos today.") — never leave a heading with no content under it.

**## Repo Activity**
One line per repo *that had activity today*, checked across the same repo list as the "Repo sync" section below. For each repo:
- `gh pr list --repo nitsuah/<repo> --search "updated:>=<YYYY-MM-DD>"` — PRs opened/updated/merged today.
- `gh issue list --repo nitsuah/<repo> --search "updated:>=<YYYY-MM-DD>"` — issues opened/closed/commented today.
- `git -C C:\Users\<user>\code\<repo> log --since="<YYYY-MM-DD> 00:00" --oneline` — local commits today (catches WIP not yet pushed, which `daily-git-sync.log` shows is most repos most days).

**Owner caveat (added 2026-09-24):** not every repo lives under `nitsuah/`. `deployer` and `nitsuah-io` are under `Nitsuah-Labs/`, and `gh` returns "Could not resolve to a Repository" for `nitsuah/<repo>`, which is easy to misread as "no activity". Derive the owner from `git -C <path> remote get-url origin` instead of hardcoding it.

Format: `- **<repo>**: <PR #N title (state)>; <N commits>; <notable issue activity>` — include only the pieces that actually happened. Skip repos with zero activity entirely; don't list all 17 repos as "no activity", that's noise.

**## Tasks**
Open P0/P1 items pulled straight from each active-today repo's synthesis file (`agent/repos/<repo>.md`, "Open P0/P1 Tasks" section, just refreshed by repo synthesis in step 2), plus anything today's dated section of `agent/logs/daily-git-sync.log` explicitly flags as needing a human (a branch parked N+ days, a diverged pull, a recurring `SKIPPED_DIRTY`/`SKIPPED_BRANCH`) — if repo sync (below) hasn't run yet this session, skip this source rather than reading yesterday's stale log entry.

**Don't re-list parked P1s** (added 2026-09-26). The W39 review found darkmoon's three `[2027-Q1]` P1s and skyview's owner-access P1s copied into the Tasks section day after day with no change, which buries anything new. So: skip items whose title carries a future-quarter tag like `[2027-Q1]`; the Monday weekly note covers them. List a human-gated item (needs owner access, a funded wallet, an outreach send) only when it is new or changed since the last daily note, and otherwise add one line: `Unchanged human-gated P1s: <repo> (<N>), ...`. Also, if stash shows `.obsidian/*.json` as modified, the clean filter isn't configured in this clone; the setup is in `agent/scripts/obsidian-json-clean.py`.

**## Notes**
A factual roll-up of what today's automation runs actually did, read from today's dated entries in `agent/logs/daily-git-sync.log`, `agent/logs/stale-worktrees.log`, `agent/logs/obn-repo.log`, and `agent/logs/obn-review.log`: counts of PULLED/SKIPPED_* results, worktrees pruned or flagged, `.md` files staged per repo, repos reviewed. Summary of the logs, not commentary — save interpretation for Reflections. If repo sync/worktree cleanup haven't run yet this session, note that plainly rather than reading a prior day's log.

**## Reflections**
1-3 sentences of actual synthesis across the sections above — a pattern worth a human's attention (e.g. several repos stuck on the same shared branch for a week, a repo with no activity in a long stretch, a blocker recurring across runs). This is the one section allowed to be interpretive, but every sentence must point back to something concrete already named above — never a generic platitude, and never left empty.

Open today's note as a **regular, non-draft PR** in `stash` (draft PRs are why the old batch of `obn: daily note` PRs piled up unmerged — same lesson as [[METRICS]]) — title `obn: daily note <date>`, branch `obn/daily-note-<date>`.

**The daily-note PR carries all of today's stash writes, not just the note** (added 2026-09-24). Steps 1–2 above plus Repo sync and Stale worktree cleanup below all write `agent/repos/**` into this vault. (They also append to `agent/logs/*.log`, but `*.log` is gitignored on purpose, so logs stay local and never go in the PR.) Before this rule the `agent/repos/**` writes were never committed. They piled up as 88+ uncommitted files on `main`, which made the Repo sync step skip `stash` as `SKIPPED_DIRTY` every day. Worse, every cloud routine clones `stash` from GitHub and reads `agent/repos/*.md`, so it was working from a snapshot several days stale while the local copies stayed current. So:
- Create the `obn/daily-note-<date>` branch **from the working tree as-is**, so the uncommitted writes come along. Commit the note and `agent/repos/**` together in the first commit.
- **Regenerate the vault links** after today's note (and, on Mon/Sat, the weekly note) is written: `python agent/scripts/build-vault-indexes.py`. The flat INDEX files were retired on 2026-09-25 (see [[projects/Vault]]). The script now links every note through the hub it belongs to:
  - prev/next nav lines in dated notes and reports
  - a *Vault links* block in each `agent/repos/<repo>.md` hub (README, KB overview, latest LOC/MINI report)
  - a *Vault links* block in each `agent/projects/<Folder>.md` folder hub
  - the generated block in `agent/VAULT-MAP.md`, the vault home (latest notes, the latest report of each kind, every repo and project hub)

  It's deterministic, so re-running it changes nothing when nothing is new. It prints the files it changed: keep that list for the commit below.
- **Repair hub links:** `python agent/scripts/fix-doc-links.py --vault --under=repos/ --unlink-dead-mirrors --write`. Step 2 rewrites hub prose from memory, and its `[[repos/<repo>/ROADMAP]]`-style links go stale when a repo moves docs into `docs/`. This repoints them (or unlinks docs that no longer exist). It only touches `agent/repos/*.md`, so the fixes ride along in the daily-note PR. Add the files it changed to the commit list below.
- **Then check the graph:** `python agent/scripts/find-orphans.py --check`. It exits 1 in two cases: a note outside the `agent/repos/<repo>/` mirrors has no link path from `VAULT-MAP`, which means a new note fits none of the generator's naming rules, or two such notes share a file name. Don't hand-link or rename anything in this run. Name it in `## Notes` so a human can add an `up: "[[parent]]"` frontmatter line, a naming rule, or a unique name. Also copy the `notes / orphans / reachable / unresolved links` summary lines into `## Notes`, so the trend is visible day to day.
- **Last step of the whole run, after Stale worktree cleanup:** commit whatever is still uncommitted under `agent/repos/`, the dated notes, and the files `build-vault-indexes.py` reported changing onto the same branch, then `git push`. The open PR picks it up automatically. Never leave commits on the branch unpushed; a squash-merge would orphan them.
- Then `git checkout main`. Do not `git pull` yet: those files are now committed on the branch, so `main` should be clean. If `git status` on `main` still shows changes under `agent/repos/`, the sweep missed something. Name it in the log instead of ignoring it.
- Only commit `agent/repos/**`, the dated note files (`agent/notes/<YYYY-MM-DD>.md`, `agent/notes/<YYYY>-W<ww>.md`), and the files `build-vault-indexes.py` listed as changed, by exact path. Never `git add agent/notes/`, `agent/reports/` or `agent/projects/` as a folder. Before pushing, run `python agent/scripts/check-generated-diff.py origin/main HEAD` from the stash root. If it fails, a human's edit got staged: unstage that file. Any other uncommitted file in `stash` is a human's in-progress work: leave it alone and mention it in `## Notes`.

### 4. Weekly note chain (Monday and Saturday only)

Moved here on 2026-09-24 from the cloud routines `week-obn-notes` (Mon) and `week-obn-review` (Fri), which were then disabled. Those routines read `main` on GitHub, but nothing ever merged their PRs. So Friday's review found no weekly note, Monday's note never saw the review, and the Friday review always missed Friday's still-unmerged daily note. Here, both land in the day's daily-note PR and get merged by step 0, and step 0 runs first, so every read below sees merged notes. Weeks are ISO weeks (`YYYY-Www`, Monday start), and `YYYY` is the **ISO year**, not the calendar year. For example, Sat 2027-01-02 is `2026-W53`, so the review must go into `agent/notes/2026-W53.md`, the same file the Monday of that week created. Compute it with `python -c "import datetime as d; y,w,_=d.date.today().isocalendar(); print(f'{y}-W{w:02d}')"` or `[System.Globalization.ISOWeek]::GetYear((Get-Date))` / `GetWeekOfYear`. **Don't** use PowerShell's `Get-Date -UFormat %V`, which isn't reliably ISO on Windows.

**Monday: create this week's weekly note.** Write `agent/notes/<YYYY>-W<ww>.md` (same flat folder as the daily notes; the `W` in the filename is what tells them apart), unless it already exists, in which case skip:

```
# Week <ww> — Mon <YYYY-MM-DD> to Fri <YYYY-MM-DD>

## Goals
- [ ] <up to 3, seeded from last week's review; see below>

## Last Week Review
<one line pointing to last week's "Week Review" section: coverage + top win, or "No review last week.">

## Key Dates

## Active Projects
<`projects/` subdirectories with commits in the last 7 days (`git log -1 --format=%ci -- projects/<dir>`), or "None this week.">
```

Seed **Goals** from last week's note: its "Next week priorities", then any "Recurring issues" not already covered, up to 3, most important first. If last week has no review, write one line saying so instead of blank checkboxes. Blank goals were the norm before 2026-09-24 and made the Friday goals check meaningless.

**Monday also: link suggestions.** Run `python agent/scripts/suggest-links.py --write`. It writes `agent/reports/link-suggestions-<date>.md`, which ranks notes that are similar to weakly connected notes but not linked to them yet, using the Smart Connections embeddings in `.smart-env/` (Obsidian must have run recently). It never edits notes. Don't act on the suggestions in this run. List the count in the weekly note under Goals as "review N link suggestions", and commit the report with the rest of today's files.

**Saturday: append the week review.** Step 0 has just merged Friday's daily note, so all five weekdays are on `main`. Read `agent/notes/<Mon..Fri date>.md` and this week's weekly note, then append (append only; never rewrite earlier sections) to `agent/notes/<YYYY>-W<ww>.md`:

```
## Week Review — Saturday <YYYY-MM-DD>
**Coverage:** <N> of 5 daily notes (missing: <dates> or "none").
**Wins:** <shipped work from the notes' Repo Activity: merged PRs, pushed commits, with repo + PR #>
**Recurring issues:** <Tasks items that appear on 2+ days, e.g. the same stale worktree or parked branch>
**Goals check:** <per goal: progress shown or not; or "No goals were set.">
**Next week priorities:** <1-3 items, from Recurring issues and Reflections, most important first>
```

Daily notes are prose with four sections (Repo Activity / Tasks / Notes / Reflections) and normally contain **no checkboxes**, so don't count `- [x]`. If the week has no daily notes and no weekly note, write nothing and say so in the log.

Both files are committed on the day's `obn/daily-note-<date>` branch with the daily note. Mention the weekly note or review in the PR body.

## Repo sync

For each repo in the list below, at the **Local path** given for it in `agent/projects/scope.md`. That's `C:\Users\<user>\code\<repo>`. `vigil` was formerly `overseer` and `ats-fill` was formerly `auto-apply-plugin`; older logs still use the old names.

1. `git status --short --branch`.
2. If clean and on the default branch (`main`/`master`): `git pull --ff-only`. Log `PULLED` with the commit count pulled.
3. If dirty (uncommitted changes) or on a non-default branch: **skip, do not stash, do not switch branches.** Log `SKIPPED_DIRTY` or `SKIPPED_BRANCH` with a one-line reason. This is someone's in-progress work — never touch it automatically.
4. If the pull would not fast-forward (diverged history): skip and log `SKIPPED_DIVERGED` — this needs a human to resolve, not automation.

Canonical repo list: `agent/projects/scope.md`'s "Tracked" table. The list below is a cached copy kept in sync manually — if you notice it's drifted from scope.md, trust scope.md and fix this line: `agent-board`, `ats-fill`, `avatar`, `bb-mcp`, `darkmoon`, `deployer`, `farm-3j`, `fire`, `games`, `gcp`, `kryptos`, `nitsuah-io`, `osrs`, `vigil`, `skyview`, `stash`, `vhs`.

Log to `stash/agent/logs/daily-git-sync.log`, appending a new dated section in the same `| repo | result | commits | note |` table format as prior runs — don't overwrite history.

## Stale worktree cleanup

For each repo with local git worktrees (`git worktree list`):

- Prune broken worktree refs (`git worktree prune`).
- Delete worktrees for branches already merged to the default branch. **Squash merges count too.** `git branch --merged` can't see them, so if a worktree's branch isn't merged by ancestry, check `gh pr list --repo <owner/repo> --head <branch> --state merged --json number` (owner/repo from scope.md's GitHub URL). If a merged PR exists, the worktree is safe to delete; log which PR proved it.
- Flag (don't delete) worktrees older than 30 days that are *not* merged — those need a human decision.

Log to `stash/agent/logs/stale-worktrees.log` in the same format as prior runs.

## Before you finish: prove the run did something

Added 2026-09-24. The 2026-09-03 run was recorded as "succeeded" after 10 seconds, which is too short to have synced 17 repos, and nothing flagged it. Before ending, check that today's run left evidence:
- a dated section for today in `daily-git-sync.log`, `stale-worktrees.log`, `obn-repo.log` and `obn-review.log`;
- today's daily-note PR is open (or step 0's once-per-day guard fired, and the log says so);
- the branch has nothing unpushed (`git status -sb` shows no `ahead`).

If any of these is missing, make the **first line** of your final output `INCOMPLETE: <what's missing>`, so the gap shows in the task's run summary instead of hiding behind a green status.

## Non-goals

This routine never: force-pushes, discards uncommitted work, rewrites history, or merges a note PR the same day it was opened. It only fast-forwards clean checkouts, prunes already-merged worktrees, and merges a *previous* day's note PR once it's clean and had a full review window — everything else is logged for a human to act on.

## Continuous improvement

After each run, if something in this file caused a silent failure, a repeated no-op, or avoidable manual cleanup, fix it here directly rather than letting it recur — that's exactly how the two "Status" fixes above (the empty-file silence and the `agent/repo/` vs `agent/repos/` path bug) got caught. Note briefly what changed and why when you do.
