# CATCHUP

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

A run counts as **not successful** if its status is `failed`, or its summary starts with `DEFERRED` or `INCOMPLETE`. `daily-repo-sync` is never caught up: the next morning's run covers the sync, and a missed day's note isn't worth the burn.

## Steps

1. **Usage gate.** Call `get_usage`. If the weekly window is at 25% or more, or the 5-hour window is at 40% or more, write one line to the log and stop. The reset has either not happened or something else is already spending the window.
2. **Find misses.** `list_task_runs` with limit 3 for each critical task. Build the missed list in the order above.
3. **Schedule, don't run.** For each missed task, create a **one-time** scheduled task (`create_scheduled_task` with `fireAt`) named `catchup-<task>-<YYYY-MM-DD>`. Its prompt is "Read `C:\Users\ajhar\.claude\scheduled-tasks\<task>\SKILL.md` and follow it exactly." Space the fires **6 hours apart** (the 5-hour window plus a 1-hour runtime buffer), starting 15 minutes from now, so no two land in the same 5-hour window. Skip any task that already has a pending `catchup-*` one-shot.
4. **Log.** Append one line per action to `C:\Users\ajhar\code\stash\agent\logs\ops-catchup.log`: `<date> | <task> | scheduled <fireAt> | reason`. Also log `nothing missed` or `gated: weekly n%`.
5. **Notify** (push notification) only when something is scheduled. List the tasks and their fire times.
6. **Clean up.** Delete `catchup-*` one-shots older than 7 days that have already fired.

## Rules

- Never call `run_scheduled_task` or `RemoteTrigger run` directly. Scheduling spaced one-shots is the whole point.
- Never catch up more than 3 tasks in one cycle. If more were missed, schedule the first 3 in order and log the rest for next week.
- Each caught-up routine still runs its own usage preflight and defers itself if the window is tight.
