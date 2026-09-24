# USAGE

> Monthly Claude Code usage report — surfaces what you actually used Claude time on this month and flags recurring manual work worth automating. This is about *your* usage of Claude Code, not the simulated product team's — unrelated to [[AUTO]].

**Status:** created 2026-09-16 following the routine-pipeline audit ([[../../reports|see that day's report]] if still present). First scheduled run: 1st of next month.

## Scope

Data sources, gather all before writing anything:

1. **Claude session/usage data** — `mcp__ccd_session_mgmt__list_sessions` (last ~30 days), `get_usage` for plan/quota trend, `mcp__scheduled-tasks__list_scheduled_tasks` + `list_task_runs` for every registered task.
2. **Shipped-work signal** — `git log --since="1 month ago" --oneline` across the owned repo list (see [[DAILY]] for the list); PR counts per repo via `gh pr list --state merged` if `gh` is authenticated.
3. **Personal usage signal (best-effort)** — try ActivityWatch's local REST API at `http://localhost:5600/api/0/buckets` first (a few-second timeout; only use it if it responds). If unreachable, fall back to a coarse proxy: Windows Event Log unlock/lock events (System log, Event ID 7001/7002 or 4801/4800) to estimate daily active-PC hours. If neither is available, omit this section and note that installing ActivityWatch (free, local-only, https://activitywatch.net) would enable a real per-app breakdown next month.
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
   - **Shipped work** — commits/PRs per repo this month.
   - **Personal usage signal** — if available.
   - **Automation candidates** — a ranked list of manual, repeated actions observed this month, each with a one-line proposed fix (e.g. "daily-repo-sync failed 5/11 times on weekly-limit hits — consider retiming").
3. Write the report to `C:\Users\<user>\code\stash\agent\reports\usage-report-<YYYY-MM>.md`. Leave it uncommitted — same as [[DAILY]]'s logs, a human reviews and commits periodically.
4. Report a 5-8 line summary to the user: usage trend headline, scheduled-task health headline, top 2 automation candidates.

## Continuous improvement

After each run, if a data source turned out to be unreachable in a way this file didn't anticipate, or a metric proved misleading/unmeasurable as specified, fix this file directly rather than producing the same "unavailable" line every month. [[RSI]] also reviews this file monthly with cited evidence — but don't wait for it if the fix is obvious in the moment.
