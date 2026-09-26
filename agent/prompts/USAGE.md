# USAGE

> Monthly Claude Code usage report — surfaces what you actually used Claude time on this month and flags recurring manual work worth automating. This is about *your* usage of Claude Code, not the simulated product team's — unrelated to [[AUTO]].

**Status:** created 2026-09-16 following the routine-pipeline audit (see [[notes/2026-09-16|that day's note]] and [[reports/pmo-audit-2026-09-16|PMO audit]]). First scheduled run: 1st of next month.

## Scope

Data sources, gather all before writing anything:

1. **Claude session/usage data** — `mcp__ccd_session_mgmt__list_sessions` (last ~30 days), `get_usage` for plan/quota trend, `mcp__scheduled-tasks__list_scheduled_tasks` + `list_task_runs` for every registered task.
   - *Learned 2026-09-24:* `list_sessions` (pass `include_archived: true`, `limit: 200`) only has `lastActivityAt` + title + cwd — no start time, no skill usage — and ~75% of sessions run from `C:\Users\<user>\code`, so derive "top work areas" from titles, not cwd. `get_usage` is a point-in-time snapshot, not a history; quota trend comes from the error strings on failed `list_task_runs` entries.
   - Cloud routines (`RemoteTrigger list`) return only the first 20 triggers, newest first, and `list` ignores `cursor` — one-shot `reminder` check-ins crowd out the recurring fleet. Report what the first page shows (duplicate reminders are a useful signal) and mark the recurring fleet as not enumerable unless a paginating path exists.
2. **Shipped-work signal** — `git log --since="1 month ago" --oneline` across the owned repo list (see [[DAILY]] for the list); PR counts per repo via `gh pr list --state merged` if `gh` is authenticated.
3. **Personal usage signal (best-effort)** — try ActivityWatch's local REST API at `http://localhost:5600/api/0/buckets` first (a few-second timeout; only use it if it responds). If unreachable, fall back to a coarse proxy: Security log Event ID 4800/4801 (lock/unlock) to estimate daily active-PC hours. *Learned 2026-09-24:* on this machine 4800/4801 are never logged (the "Audit Other Logon/Logoff Events" policy is off — enabling it is a security-setting change for the human, not this routine), and System 7001/7002 are Winlogon **logon/logoff**, not lock/unlock (~23/month), so they can't yield hours — don't use them as a proxy. If neither is available, omit this section and note that installing ActivityWatch (free, local-only, https://activitywatch.net) would enable a real per-app breakdown next month.
4. **Calendar signal (optional)** — only if a calendar MCP is connected: pull the past month's events and look for recurring meeting types that could be templated or auto-scheduled.
5. **Routine-run findings (if present)**: any `stash/agent/reports/routine-run-findings-<YYYY-MM-DD>.md` from this month. It has cited quota and failure evidence from manual catch-up sessions. Fold it into the scheduled-task health section.

## Rules — read before touching source 3

- Never scrape a social media platform (Instagram, etc.) directly, and never fetch, hold, or enter login credentials for one — this was explicitly ruled out when this routine was scoped. Time-in-app totals from a local tracker are fine; content scraping is not.
- Never fabricate a number. If a data source is unreachable, write "unavailable — <reason>", never a guess.
- This routine is **read-only** against your repos and Claude account — it never commits, opens PRs, or edits scheduled-task configuration. That's [[RSI]]'s job, which reads this report as an input.

## Steps

1. Gather sources 1-5 above.
2. Build the report:
   - **Claude usage trend** — 5hr/weekly % samples if available, sessions started this month, top 5 repos/skills touched by session count.
   - **Scheduled-task health** — per task: run count, success/fail rate, most common failure reason. Same table shape as the 2026-09-16 audit, so months are comparable.
     - **"Succeeded" isn't enough (added 2026-09-24).** Count a run as succeeded only if its output landed. A `daily-repo-sync` run shorter than ~60 s, or one with no dated entry in `agent/logs/daily-git-sync.log` for that day, is a **suspected no-op**. A cloud routine whose report PR was closed without merging (check `gh pr list --repo nitsuah/stash --state closed` for PRs with no `mergedAt`) is **output lost**. Report both in their own column rather than as successes. Also count **hijacked** runs: routine sessions whose last activity is more than 2 h after their start, meaning the session was reused for other work (added 2026-09-26: daily-repo-sync on 9/26 ran 7.5 h and 568 messages). Report the 5-hour and weekly window at run time, and count runs that started with `DEFERRED:` separately. Evidence: `daily-repo-sync` 9/03 "succeeded" in 10 s; `week-metrics` 9/18 "succeeded" but its stash#99 closed unmerged.
   - **Shipped work** — commits/PRs per repo this month.
   - **Personal usage signal** — if available.
   - **Automation candidates** — a ranked list of manual, repeated actions observed this month, each with a one-line proposed fix (e.g. "daily-repo-sync failed 5/11 times on weekly-limit hits — consider retiming").
3. Write the report to `C:\Users\<user>\code\stash\agent\reports\usage-report-<YYYY-MM>.md`. Leave it uncommitted — same as [[DAILY]]'s logs, a human reviews and commits periodically.
4. Report a 5-8 line summary to the user: usage trend headline, scheduled-task health headline, top 2 automation candidates.

## Continuous improvement

After each run, if a data source turned out to be unreachable in a way this file didn't anticipate, or a metric proved misleading/unmeasurable as specified, fix this file directly rather than producing the same "unavailable" line every month. [[RSI]] also reviews this file monthly with cited evidence — but don't wait for it if the fix is obvious in the moment.
