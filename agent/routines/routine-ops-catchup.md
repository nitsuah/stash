---
up: "[[routines-backup]]"
kind: routine-backup
routine: ops-catchup
runs: local
description: Reset-aware catch-up: after the Wed weekly reset, schedule spaced one-shot re-runs of missed chain-critical routines, per stash/agent/prompts/CATCHUP.md
---

# routine · ops-catchup

> Backup of `~/.claude/scheduled-tasks/ops-catchup/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

You are running ops-catchup, the reset-aware catch-up for chain-critical routines.

Read `C:\Users\ajhar\code\stash\agent\prompts\CATCHUP.md` in full and follow it exactly. If it isn't in the working tree yet, read it with `git -C C:\Users\ajhar\code\stash show origin/main:agent/prompts/CATCHUP.md`. If it isn't there either, stop and report that.

Hard rules:
- Check `get_usage` first. If the weekly window is at 25%+ or the 5-hour window is at 40%+, log one line to `C:\Users\ajhar\code\stash\agent\logs\ops-catchup.log` and stop.
- Only these tasks are critical: monthly-tire-kick, monthly-pmo-audit, monthly-usage-report, monthly-self-improvement, week-sotu. Never catch up daily-repo-sync or any cloud routine.
- NEVER call run_scheduled_task or RemoteTrigger run. Create one-time scheduled tasks (fireAt), spaced 3 hours apart, at most 3 per cycle.
- Push-notify only if something was scheduled. Keep the run short; this is a few tool calls, not a work session.
