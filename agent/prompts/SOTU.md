# SOTU

> Weekly State of the Union. It builds one view of what needs the user, what product work is ready to kick off, how the routines are doing, and what's open across the tracked repos. It replaces the cloud `week-vigil-check` and the hand-built Portfolio Checklist (2026-09-26, see [[routine-audit-2026-09-26]]).

**Runs:** `week-sotu` local scheduled task, Mondays 08:00 ET. It's cheap by design: a script does the gathering and rendering, and the model writes only a short focus note.

## Steps

1. **Usage preflight.** Call `get_usage`. If the weekly window is at 90% or more, stop and make the first line of your output `DEFERRED: weekly <n>%`. [[CATCHUP]] runs it after the reset.
2. **Sync.** `git -C C:\Users\ajhar\code\stash fetch -q origin`. Don't touch the checkout; the script reads `origin` refs.
3. **Routine health.** Write `%TEMP%\sotu-routines.json` in this shape: `{"quota": {"weekly": n, "five_hour": n, "weekly_resets": "..."}, "routines": [{"name", "last_run", "status", "next_run"}]}`.
   - Local tasks: `list_scheduled_tasks`, plus `list_task_runs` with limit 1 for each.
   - Cloud routines: `RemoteTrigger get` on each ID in the `reference-cloud-routine-ids` memory. Take only `enabled`, `last_run.status` and `next_run_at` from each response and ignore the prompt text.
   - Mark a run `INCOMPLETE` or `DEFERRED` if its summary starts with that word.
4. **Build.** `python C:\Users\ajhar\code\stash\agent\scripts\sotu.py --routines %TEMP%\sotu-routines.json`.
   - The script uses vigil's `get_open_tasks` when `VIGIL_MCP_KEY` is set. Otherwise it parses each repo's TASKS.md from `origin`.
   - It writes `agent/reports/sotu/sotu-data.json` and `agent/reports/sotu/sotu-<YYYY>-W<ww>.md`.
   - Read the `.md` it wrote. It's about 10 KB; don't read the JSON.
5. **Focus note.** Write 2–4 plain sentences:
   - what changed since last week's `sotu-*.md`;
   - the one thing that most needs the user;
   - which kickoff item looks most worth starting, and why.

   Put the note in the `.md` in place of the `<!-- focus -->` line. Also set it as `"focus"` in `sotu-data.json`: load the JSON with a one-line Python command, set the key, and write it back.
6. **Publish.**
   - `Artifact read` on https://claude.ai/artifact/EwZkbsE5ZBGZASFSZpJNbm. The page is a small shell, about 10 KB.
   - Then `Artifact publish` with that `url`, `file_path` = `agent/scripts/sotu-page.html`, and `files` = `{"sotu-data.json": "agent/reports/sotu/sotu-data.json"}`.
   - Leave the icon alone.
7. **Save.** Commit only `agent/reports/sotu/sotu-<week>.md` and `sotu-data.json`, on a branch `sotu/<week>` cut from `origin/main` (`git switch -c sotu/<week> origin/main` in the clean checkout).
   - If the checkout is dirty or not on main, skip the commit and say so. The artifact is the main output.
   - Push and open a PR. It's a machine-generated report, like TIRE's, so run `gh pr merge --squash --auto --delete-branch` and let it land when CI is green. If the merge is refused, leave the PR open and say so.
8. **Output.** One line: the artifact link, the counts line, and the focus note's first sentence. Then end the run. Don't take follow-up work in this session; start a new one.

## Rules

- Read-only against product repos.
- stash is PUBLIC. Task titles from public repos are fine. For the private `deployer`, titles only.
- The user edits `- Owner: you` sub-bullets in TASKS.md to route items into **Needs you**. Don't hand-edit the JSON to move items.
- To change what the page shows, change `sotu.py` or `sotu-page.html` in a PR. Never regenerate the page by hand.
