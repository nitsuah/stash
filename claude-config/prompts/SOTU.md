# SOTU

> Weekly State of the Union. It builds one view of what needs the user, what product work is ready to kick off, how the routines are doing, and what's open across the **tier 1 and tier 2 apps**. It replaces the cloud `week-vigil-check` and the hand-built Portfolio Checklist (2026-09-26, see [[routine-audit-2026-09-26]]). Scope narrowed to vigil tiers 1–2 on 2026-10-16 (user direction).

**Runs:** `week-sotu` local scheduled task, Mondays. It's cheap by design: a script does the gathering and rendering, and the model checks the top of the list against reality and writes a short focus note.

## Scope

- **In scope:** repos that vigil tiers T1 (Critical) or T2 (Important). `sotu.py` reads the tiers live from vigil's `GET https://gh-vigil.netlify.app/api/context` (`repos[].tier`, with `$VIGIL_MCP_KEY`). If vigil can't be read, it falls back to the Tier column in `agent/projects/scope.md` and says so in the report.
- **Out of scope:** T3/T4 and repos vigil doesn't track (`—` in scope.md), stash included. Their tasks, kickoff items and ledger rows are left out. Cross-cutting ledger rows (for example `cloud routines`) stay. To see everything, run with `--all-tiers`, but don't publish that build.
- **Tier drift:** when vigil and scope.md disagree, the report ends with a `scope.md Tier column differs from vigil` line, and the page shows it in the header. Fix it in step 5.
- To move a repo in or out of scope, change its tier in vigil, not here.

## Steps

1. **Usage preflight.** Call `get_usage`. If the weekly window is at 90% or more, stop and make the first line of your output `DEFERRED: weekly <n>%`. [[CATCHUP]] runs it after the reset.
2. **Clean check (before Build, since Build writes the report files).** Run `git -C C:\Users\ajhar\code\stash status --porcelain` and `branch --show-current`, and record whether stash is clean and on `main`. Step 9 uses the answer. You don't need to fetch: `sotu.py` runs `git fetch` in every in-scope repo before reading `origin` refs (60 s timeout each). Repos whose fetch fails are listed in the report as possibly stale.
3. **Routine health.** Write `%TEMP%\sotu-routines.json` in this shape: `{"quota": {"weekly": n, "five_hour": n, "weekly_resets": "..."}, "routines": [{"name", "last_run", "status", "next_run", "note"}]}`. Keep `status` to one word (`succeeded`, `failed`, `running`, `deferred`, `new`) and put any detail in `note`, so the health table stays aligned.
   - Local tasks: `list_scheduled_tasks`, plus `list_task_runs` with limit 1 for each.
   - Cloud routines: `RemoteTrigger get` on each ID in the `reference-cloud-routine-ids` memory. Take only `enabled`, `last_run.status`, `last_run.failure_reason` and `next_run_at` from each response and ignore the prompt text.
   - Mark a run `INCOMPLETE` or `DEFERRED` if its summary starts with that word.
4. **Build.** `python C:\Users\ajhar\code\stash\agent\scripts\sotu.py --routines %TEMP%\sotu-routines.json`.
   - Tasks come from each in-scope repo's TASKS.md on `origin` after the fetch. Don't pass `--vigil-tasks`: vigil's task cache lags same-day merges by hours (on 2026-10-16 it still served a P0 closed that morning).
   - It writes `agent/reports/sotu/sotu-data.json` and `agent/reports/sotu/sotu-<YYYY>-W<ww>.md`.
   - Read the `.md` it wrote. It's about 10 KB; don't read the JSON.
5. **Tier drift.** If the report has a tier-drift line, update the Tier column in `agent/projects/scope.md` to match vigil, set the pull date in the paragraph above the table, and commit it with the report in step 9. Don't change tiers in vigil yourself.
6. **Verify the top of the list.** TASKS.md checkboxes go stale: agents ship the work and forget to tick the item (16 such items were found on 2026-10-16). Before you write the focus note, check every **Needs you** item, every **kickoff** item and every open **P0/P1** against reality:
   - merged PRs in that repo since the item was filed (`gh pr list -R <repo> --state merged --search "merged:>=<date>"`), and their bodies;
   - the issues the item names (`gh issue view`);
   - the code on the default branch (does the function or file the item describes now exist or behave as asked?);
   - CI or release runs where the item is about a pipeline (for example a release that now authenticates).
   - Results:
     - **Done, with unambiguous evidence** (a merged PR or closed issue that names the item, or code that meets its acceptance criteria): close it at the source. Open one docs-only PR per repo from a worktree that ticks the item, or removes it where the repo condenses Done items into CHANGELOG. Add the CHANGELOG line that repo's convention needs, and link the evidence in the PR body. Turn on auto-merge. This is the one write this routine makes outside stash.
     - **Partly done:** don't tick it. Rewrite the item down to what's left, in the same PR.
     - **Unclear** (it needs a live run or the user's word): leave it, and name it in the focus note as "check: …".
   - Once those PRs merge, re-run step 4 so the page reflects them. If they haven't merged within the run, publish anyway and say which PRs are pending.
7. **Priorities.** Open `agent/reports/sotu/priorities.json` (the top 2 initiatives and the WSJF top 5). Drop any item whose task, finding or PR is now done (move it to `done` with its evidence) and renumber. Drop items for repos that are out of scope. Don't re-rank or add items yourself: say in the focus note that a slot is free, and the user picks the next one. If you changed the file, re-run the step 4 Build command and commit it with the report.
8. **Focus note and publish.**
   - Write 2–4 plain sentences: what changed since last week's `sotu-*.md`; the one thing that most needs the user; which kickoff item looks most worth starting, and why; plus any "check: …" items from step 6.
   - Put the note in the `.md` in place of the `<!-- focus -->` line. Also set it as `"focus"` in `sotu-data.json`: load the JSON with a one-line Python command, set the key, and write it back.
   - `Artifact read` on https://claude.ai/artifact/EwZkbsE5ZBGZASFSZpJNbm (a small shell, about 10 KB), then `Artifact publish` with that `url`, `file_path` = `agent/scripts/sotu-page.html`, and `files` = `{"sotu-data.json": "agent/reports/sotu/sotu-data.json"}`. If the publish asks you to read `sotu-data.json` first, list the artifact's files instead (`action: list`, `scope: files`). Leave the icon alone.
9. **Save.** Commit `agent/reports/sotu/sotu-<week>.md`, `sotu-data.json`, and (if steps 5 or 7 changed them) `agent/projects/scope.md` and `priorities.json` on a branch `sotu/<week>` cut from `origin/main`.
   - Use the step 2 answer. If stash was clean and on main, `git switch -c sotu/<week> origin/main` there. If it was dirty or off main **before** Build, run `git worktree add .claude/worktrees/sotu-<week> -b sotu/<week> origin/main` instead, copy the files in, commit there, and remove the worktree once pushed. The pre-commit hook works from a worktree (stash#171). Commit exactly those paths; if anything else changed, leave it alone.
   - Push and open a PR. It's a machine-generated report, so run `gh pr merge --squash --auto --delete-branch`. If CodeRabbit requests changes, fix what's real and rebut the rest with a reason (it reviews against the vault mirrors in `agent/repos/*/docs/`, which lag the real repos). If the merge is still refused, leave the PR open and say so.
10. **Output.** One line: the artifact link, the counts line, the number of items closed at the source, and the focus note's first sentence. Then end the run. Don't take follow-up work in this session; start a new one.

## Rules

- Product repos: read-only, except the step 6 docs-only TASKS.md/CHANGELOG PRs.
- stash is PUBLIC. Task titles from public repos are fine. For private repos (scope.md Visibility = private), `sotu.py` keeps titles only and drops criteria, owner and section before writing either output.
- `VIGIL_MCP_KEY` must be a Windows **user** environment variable, so scheduled tasks inherit it. Restart the desktop app after setting it. Without it, tiers come from scope.md and the report says `tiers from scope.md`.
- The user edits `- Owner: you` sub-bullets in TASKS.md to route items into **Needs you**. Don't hand-edit the JSON to move items.
- To change what the page shows, change `sotu.py` or `sotu-page.html` in a PR. Never regenerate the page by hand.

## Initiatives vs single-app work (added 2026-09-26, user direction)

- **Portfolio initiatives** are cross-repo items. Since 2026-10-16 the curated list in `priorities.json` is the source, because stash (where most were filed) is tier 3 and out of scope. An in-scope TASKS item that says "every/all/each repo" is still marked `initiative` and weighted 1.5×. A P2 initiative therefore outranks a P2 app item, but a P1 app item still outranks it. Single-app items keep their own priority, plus a small bump for tier 1 apps.
- The kickoff queue takes at most one item per app repo and at most two initiatives.
- **Routine candidates** are initiatives that act on other routines' output: reports, ledger, run history, generator results. They're the pool for new Claude routines. In the focus note, name any routine candidate that has appeared in 3+ weekly reports without moving. [[RSI]] reads the `sotu-*.md` files and proposes a routine for those (or folds the item into an existing routine's spec) rather than leaving it in a backlog.
- As an initiative gets broken down into per-repo processes (for example a vigil best practice plus a CI recipe), its per-repo tasks show up as ordinary app items.
