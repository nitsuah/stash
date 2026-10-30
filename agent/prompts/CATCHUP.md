# CATCHUP

> **Retired 2026-10-30:** the `ops-catchup` task is disabled. Its Local jobs audit is `agent/scripts/local-audit.mjs` (run it by hand or from Task Scheduler); quota catch-up is no longer needed now that the cloud report routines are CI. This spec stays as a reference for the audit table.

> Reset-aware catch-up for routines that the chain depends on. It replaces manual "Try again" re-runs and the hand-made "Claude resets" calendar event (2026-09-26, see [[routine-audit-2026-09-26]]).

**Design rule from the user:** once quota runs out, it stays out until the reset, and the user may be burning it elsewhere (other harnesses and providers). So this routine **never retries into an exhausted window**. It runs once, right after the weekly reset, and schedules the missed chain runs spaced safely apart. It doesn't loop, poll or retry blindly.

**Runs:** `ops-catchup` local scheduled task, Wednesdays 07:45 ET. That's after the Wed 05:00 UTC weekly reset and after that morning's daily-repo-sync.

## What counts as critical

Only these routines get caught up. Everything else, including the daily cloud brief, is time-sensitive or cheap to skip, so it waits for its next normal fire.

| Order | Task (local) | Missed when |
|---|---|---|
| 1 | `monthly-tire-kick` | no successful run since the last 28th |
| 2 | `monthly-pmo-audit` | no successful run since the last 1st |
| 3 | `monthly-usage-report` | no successful run since the last 1st |
| 4 | `monthly-self-improvement` | no successful run since the last 2nd |
| 5 | `week-sotu` | no successful run since the last Monday |

A run counts as **not successful** if its status is `failed`, or its summary starts with `DEFERRED` or `INCOMPLETE`. It also doesn't count if its output never reached GitHub. After `git fetch`, check `origin/main` (or an open PR branch) for the dated file: `tire-kick-<date>.md`, `pmo-audit-<date>.md`, `usage-report-<YYYY-MM>.md`, `rsi-report-<YYYY-MM>.md` or `sotu/sotu-<week>.md`. If the file is missing, log `output not landed` and treat the run as missed. (Added 2026-10-07: the 9/30 tire-kick catch-up "succeeded", but its ledger and report sat in a scratchpad for a week, and this routine logged it as ok.) `daily-repo-sync` is never caught up: the next morning's run covers the sync, and a missed day's note isn't worth the burn.

## Steps

0. **Local jobs audit. This step always runs, even if step 1 gates the rest.** It's read-only and about 6 tool calls. See [Local jobs audit](#local-jobs-audit) below.
1. **Usage gate.** Call `get_usage`. If the weekly window is at 25% or more, or the 5-hour window is at 40% or more, write one line to the log and stop. The reset has either not happened or something else is already spending the window.
2. **Find misses.** `list_task_runs` with limit 3 for each critical task. Build the missed list in the order above.
3. **Schedule, don't run.** For each missed task, create a **one-time** scheduled task (`create_scheduled_task` with `fireAt`) named `catchup-<task>-<YYYY-MM-DD>`. Its prompt is "Read `C:\Users\ajhar\.claude\scheduled-tasks\<task>\SKILL.md` and follow it exactly." Space the fires **6 hours apart** (the 5-hour window plus a 1-hour runtime buffer), starting 15 minutes from now, so no two land in the same 5-hour window. Skip any task that already has a pending `catchup-*` one-shot.
4. **Log.** Append one line per action to `C:\Users\ajhar\code\stash\agent\logs\ops-catchup.log`: `<date> | <task> | scheduled <fireAt> | reason`. Also log `nothing missed` or `gated: weekly n%`.
5. **Notify** (push notification) only when something is scheduled, or when step 0 found a red item. List the tasks and their fire times, then the red items.
6. **Clean up.** Delete `catchup-*` one-shots older than 7 days that have already fired.

## Rules

- Never call `run_scheduled_task` or `RemoteTrigger run` directly. Scheduling spaced one-shots is the whole point.
- Never catch up more than 3 tasks in one cycle. If more were missed, schedule the first 3 in order and log the rest for next week.
- Each caught-up routine still runs its own usage preflight and defers itself if the window is tight.

## Local jobs audit

Added 2026-10-22. Claude now creates jobs that run on this machine **outside** Claude's own scheduler, so nothing else watches them. This weekly check keeps tabs on them. `node agent/scripts/local-audit.mjs` runs these checks with no model (plus the obn-health and repo-health workflow runs) and logs red items; see [[ROUTINE-RUN]]. It **reports only**: never re-enable, edit, run, rebuild or restart anything; the user decides.

**What to check** (shell commands; PowerShell where noted):

| # | Job | Check | Red when |
|---|---|---|---|
| a | Windows Task Scheduler, root folder | PowerShell: list root-level tasks whose action runs something under `~\.imps`, `~\scripts` or `~\code`, or runs node/pwsh/cmd scripts there. Today that's **`imps-dispatch`** (hourly imps dispatcher, runs `~\.imps\hourly.cmd`), **`imps-label-watch`** (every 5 min, `~\.imps\label-watch.cmd`) and **`Sync 9router fork`** (hourly + at logon, `~\scripts\sync-9router-fork.ps1`). For each, get State, LastRunTime, LastTaskResult and NextRunTime (`Get-ScheduledTaskInfo`) | Disabled; LastTaskResult not 0 (267011 means it never ran); last run older than 3× its interval; **a new task that isn't in this table** (add it here in the same PR) |
| b | imps loop | Last 7 days of `~\.imps\dispatch.jsonl`: count `cycle`, `skip` (9router down), `pr`, `gate-fail`, `fix-sweep` results, `needs-human`, `error`, `run-error`. Also `node ~\code\imps-runner\imps\imp.mjs report \| head -2`, and `gh search prs --owner nitsuah --state open --label imp:needs-human` | No `cycle` in the last 3 h while the laptop was on; more `skip` than `cycle`; any `error`/`run-error`; any `imp:needs-human` PR (list them) |
| c | 9router image drift | `git -C ~\code\9router describe --tags --abbrev=0` vs. `docker inspect 9router --format "{{.Config.Image}}"`, plus the last line of `~\scripts\logs\9router-sync.log` | The running image tag is older than the repo's latest tag. The sync job pulls the repo but never rebuilds the container (on 2026-10-22 it ran 0.5.99 while the repo was on 0.5.104). Suggest `docker compose build` + recreate; don't do it |
| d | Claude local scheduled tasks | `list_scheduled_tasks` | Any task disabled, or a `lastRunAt` older than its schedule implies (missed while the app was closed). Monthlies are step 2's job; just list them here |
| e | GitHub Actions jobs | `gh run list -R nitsuah/stash --workflow obn-health.yml --limit 3` and `gh run list -R nitsuah/stash --workflow repo-health.yml --limit 3` (plus `gh run list -R nitsuah/.github --workflow repo-health.yml --limit 3` if present) | Latest run `failure`, or no run in the last 8 days |

**Output:** one log line per red item to `ops-catchup.log` (`<date> | audit | <job> | <what>`), or `audit: all green`. Red items go in the step 5 push notification.
