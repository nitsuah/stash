---
up: "[[routines-backup]]"
kind: routine-backup
routine: monthly-self-improvement
runs: local
description: "Monthly self-improvement cycle for the Claude routine stack, full PMO-style auto-PR privileges, per stash/agent/prompts/RSI.md"
---

# routine · monthly-self-improvement

> Backup of `~/.claude/scheduled-tasks/monthly-self-improvement/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

**USAGE PREFLIGHT (added 2026-09-26; do this before anything else):** call `get_usage`. If the weekly window is at 75% or more, or the 5-hour window is at 50% or more, make the first line of your output `DEFERRED: weekly <n>% / 5h <n>%` and stop without doing any work. The `ops-catchup` routine (stash/agent/prompts/CATCHUP.md) schedules a spaced re-run after the next weekly reset. A DEFERRED run is expected and costs almost nothing. A run that starts and dies mid-way on quota wastes the tokens it already spent.

You are running the monthly self-improvement (RSI) cycle. Read `C:\Users\ajhar\code\stash\agent\prompts\RSI.md` in full and follow it exactly before doing anything else — it is the canonical, detailed spec (inputs, what it's allowed to touch and how, PR governance, logging requirements, definition of done).

This routine has real, unattended write access: it can open PRs across your owned repos (same standing as `monthly-pmo-audit`) and can edit other scheduled tasks' prompts and this vault's own files, subject to the logging rules in RSI.md. Do not skip reading RSI.md — it is what keeps this routine's autonomy bounded (evidence-only changes, no touching credentials/settings/permissions, always log before editing a prompt file, never silently disable or delete a scheduled task).

If `C:\Users\ajhar\code\stash\agent\prompts\RSI.md` is missing or unreadable, stop and report that rather than improvising — this routine must not act autonomously without its guardrails present.
