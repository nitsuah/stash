---
up: "[[routines-backup]]"
kind: routine-backup
routine: week-sotu
runs: local
description: Weekly State of the Union: rebuild the Portfolio Checklist artifact from vigil/TASKS.md, the findings ledger and routine health, per stash/agent/prompts/SOTU.md
---

# routine · week-sotu

> Backup of `~/.claude/scheduled-tasks/week-sotu/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

You are running the weekly State of the Union (week-sotu).

Read `C:\Users\ajhar\code\stash\agent\prompts\SOTU.md` in full and follow it exactly. It's the canonical spec. If it isn't in the working tree yet, read it with `git -C C:\Users\ajhar\code\stash show origin/main:agent/prompts/SOTU.md`. If it isn't there either, stop and report that.

Hard rules:
- Step 1 is a usage check (`get_usage`). At 90%+ weekly, output `DEFERRED: weekly <n>%` as the first line and stop.
- The script `agent/scripts/sotu.py` does the gathering and rendering. Don't hand-write the report or the page, and don't read `sotu-data.json`.
- Publish to the existing artifact https://claude.ai/artifact/EwZkbsE5ZBGZASFSZpJNbm. Read it first, then publish with that url. Never create a new artifact.
- Read-only against product repos. stash is public.
- End with one line (artifact link + counts + focus). Don't take follow-up work in this session.
