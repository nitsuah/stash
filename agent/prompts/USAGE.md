# USAGE

> Monthly Claude Code usage report — surfaces what you actually used Claude time on this month and flags recurring manual work worth automating. This is about *your* usage of Claude Code, not the simulated product team's — unrelated to [[AUTO]].

**Status:** created 2026-09-16 following the routine-pipeline audit (see [[notes/2026-09-16|that day's note]] and [[reports/pmo-audit-2026-09-16|PMO audit]]). First scheduled run: 1st of next month.

## Scope

Data sources, gather all before writing anything:

1. **Claude session/usage data** — `mcp__ccd_session_mgmt__list_sessions` (last ~30 days), `get_usage` for plan/quota trend, `mcp__scheduled-tasks__list_scheduled_tasks` + `list_task_runs` for every registered task.
   - *Learned 2026-09-24:* `list_sessions` (pass `include_archived: true`, `limit: 200`) only has `lastActivityAt` + title + cwd — no start time, no skill usage — and ~75% of sessions run from `C:\Users\<user>\code`, so derive "top work areas" from titles, not cwd. `get_usage` is a point-in-time snapshot, not a history; quota trend comes from the error strings on failed `list_task_runs` entries.
   - *Learned 2026-10-28:* `list_task_runs` returns only 10 runs by default and silently truncates; pass `limit: 50` (the maximum) or run counts and fail rates will be wrong. Name the report for the month it actually covers and say the window in its intro.
   - **Reporting window (defined 2026-10-28):** the scheduled run on the 1st covers the previous completed calendar month (the 10/01 run covers September, so `usage-report-<YYYY-MM>` is that month). A catch-up or manual run before month end covers the partial current month, states the exact dates in its intro, and is superseded by the full-month report if that one is later written.
2. **Shipped-work signal** — `git log --since="1 month ago" --oneline` across the owned repo list (see [[DAILY]] for the list); PR counts per repo via `gh pr list --state merged` if `gh` is authenticated. *Learned 2026-10-01:* local dir names drift from origins (`vigil` was `overseer`; `ats-fill` → `nitsuah/auto-apply-plugin`), so resolve each repo by its `origin` URL, and exclude forks (`gh repo view --json isFork`; e.g. `9router`), whose `--all` commits are upstream authors.
3. **Routine-run findings (if present)**: any `stash/agent/reports/routine-run-findings-<YYYY-MM-DD>.md` from this month. It has cited quota and failure evidence from manual catch-up sessions. Fold it into the scheduled-task health section.

## Rules

- Never fabricate a number. If a data source is unreachable, write "unavailable — <reason>", never a guess.
- This routine is **read-only** against your repos and Claude account — it never touches product repos, never merges, and never edits scheduled-task configuration. The one write it makes is step 3: the usage report committed on its own branch in stash, shipped as an unmerged PR. [[RSI]] reads that report as an input and owns every spec or configuration change.

## Steps

1. Gather sources 1-3 above.
2. Build the report:
   - **Claude usage trend** — 5hr/weekly % samples if available, sessions started this month, top 5 repos/skills touched by session count.
   - **Scheduled-task health** — per task: run count, success/fail rate, most common failure reason. Same table shape as the 2026-09-16 audit, so months are comparable.
     - **"Succeeded" isn't enough (added 2026-09-24).** Count a run as succeeded only if its output landed. A `daily-repo-sync` run shorter than ~60 s, or one with no dated entry in `agent/logs/daily-git-sync.log` for that day, is a **suspected no-op**. A cloud routine whose report PR was closed without merging (check `gh pr list --repo nitsuah/stash --state closed` for PRs with no `mergedAt`) is **output lost**. Report both in their own column rather than as successes. Also count **hijacked** runs: scheduled-task runs whose `list_task_runs` `last_activity_at` is more than 2 h after their `started_at` (both fields are on every run; cloud routines have `created_at` / `last_event_at` in `RemoteTrigger list_runs`), meaning the session was reused for other work (added 2026-09-26: daily-repo-sync on 9/26 ran 7.5 h and 568 messages). For automation, a failure signal is `gh run list -R nitsuah/stash --workflow obn-health.yml` and `gh run list -R nitsuah/stash --workflow repo-health.yml` (conclusion `failure` in the month). Report the 5-hour and weekly window at run time, and count runs that started with `DEFERRED:` separately. *Learned 2026-10-01:* `list_task_runs` often returns no `summary`, so for a run that succeeded in under ~2 min, read its first assistant message via `mcp__ccd_session_mgmt__list_events` to spot `DEFERRED:`. A hijacked run's final status reflects the later work, not the scheduled run (week-sotu 9/28 shows succeeded while `ops-catchup.log` recorded it failed), so mark its status as unreliable. Evidence: `daily-repo-sync` 9/03 "succeeded" in 10 s; `week-metrics` 9/18 "succeeded" but its stash#99 closed unmerged.
   - **Shipped work** — commits/PRs per repo this month.
   - **Automation candidates** — a ranked list of manual, repeated actions observed this month, each with a one-line proposed fix (e.g. "daily-repo-sync failed 5/11 times on weekly-limit hits — consider retiming").
3. Write the report to `agent/reports/usage-report-<YYYY-MM>.md` and ship it on its own PR (changed 2026-10-07: the September report sat uncommitted in the shared checkout for a week. [[RSI]] and the cloud routines read stash from GitHub, so they never saw it, and it kept daily-repo-sync skipping stash as dirty):
   - `git -C C:\Users\<user>\code\stash fetch origin`, then `git worktree add .claude/worktrees/usage-<YYYY-MM> -b usage/<YYYY-MM> origin/main` from the stash root. Write the report there, not in the main checkout. The pre-commit hook works from a worktree (stash#171).
   - Commit only that file. If this run's spec fixes (Continuous improvement, below) touched `agent/prompts/USAGE.md`, commit that too, as a separate commit on the same branch.
   - Push and `gh pr create`. Don't merge it. RSI reads the PR branch if it hasn't merged yet. Then `git worktree remove` the worktree.
4. Report a 5-8 line summary to the user: usage trend headline, scheduled-task health headline, top 2 automation candidates.

## Continuous improvement

After each run, if a data source turned out to be unreachable in a way this file didn't anticipate, or a metric proved misleading/unmeasurable as specified, fix this file directly rather than producing the same "unavailable" line every month. [[RSI]] also reviews this file monthly with cited evidence — but don't wait for it if the fix is obvious in the moment.
