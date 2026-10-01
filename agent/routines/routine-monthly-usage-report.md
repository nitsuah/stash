---
up: "[[routines-backup]]"
kind: routine-backup
routine: monthly-usage-report
runs: local
description: "Monthly Claude Code usage + automation-candidate report, per stash/agent/prompts/USAGE.md"
---

# routine · monthly-usage-report

> Backup of `~/.claude/scheduled-tasks/monthly-usage-report/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

**USAGE PREFLIGHT (added 2026-09-26; do this before anything else):** call `get_usage`. If the weekly window is at 90% or more, or the 5-hour window is at 70% or more, make the first line of your output `DEFERRED: weekly <n>% / 5h <n>%` and stop without doing any work. The `ops-catchup` routine (stash/agent/prompts/CATCHUP.md) schedules a spaced re-run after the next weekly reset. A DEFERRED run is expected and costs almost nothing. A run that starts and dies mid-way on quota wastes the tokens it already spent.

You are running the monthly Claude Code usage report. Read `C:\Users\ajhar\code\stash\agent\prompts\USAGE.md` in full and follow it exactly — it is the canonical spec (data sources, rules on what NOT to scrape, report format, output path). Do not skip reading it.

This is a read-only reporting routine: it never commits, opens PRs, or changes any scheduled-task configuration. It exists to feed evidence to the `monthly-self-improvement` task, which runs the next day.

If `C:\Users\ajhar\code\stash\agent\prompts\USAGE.md` is missing or unreadable, stop and report that rather than improvising — the file defines the data sources and the hard rule against scraping third-party platforms or handling credentials, and this routine must not run without it.
