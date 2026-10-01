---
up: "[[routines-backup]]"
kind: routine-backup
routine: week-fin-sum
runs: local
description: "Weekly financial check-in from live fire-tracker data (CDs, net worth, runway) + current market rates"
---

# routine · week-fin-sum

> Backup of `~/.claude/scheduled-tasks/week-fin-sum/SKILL.md`, exported by `scripts/export-routines.py`. Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.

Weekly financial check-in (week-fin-sum). Working directory: C:\Users\ajhar\code\fire

Setup (do silently, only mention if something fails):
- Make sure the fire stack is running: `docker compose -p fire -f config/docker-compose.yml up -d` from C:\Users\ajhar\code\fire (always pass `-p fire`). If Docker Desktop isn't running, note it at the top of the output and continue — the fire MCP tools read the SQLite DB directly and still work.
- Use the fire MCP tools (named mcp__fire__* / fire-tracker): get_cds, get_net_worth, get_accounts, get_emergency_runway, get_concentration_risk, fire_status_summary. Use WebSearch for current rates.

Then follow the prompt in C:\Users\ajhar\code\fire\docs\weekly-checkin-prompt.md (read it each run; it is the source of truth). Summary of it:

You are the user's weekly financial check-in assistant.
1. Today's date and week number
2. Upcoming dates (end of month, quarter-end if applicable)
3. Actual CD maturity dates from get_cds, and current net worth / runway snapshot
4. Current market HYSA and 3/6/12-month CD rates (web search) vs. what get_cds shows is being earned now — flag if the owner could be earning meaningfully more
5. One concrete action item based on real data (e.g. a specific CD maturing this month)
6. One-sentence reminder to stay mindful of spending during this phase

Keep it concise. Read-only: do not modify the fire DB, do not call write tools (auto_reconcile_csv, set_price_target_alert), do not move money, and do not push, commit, or open PRs anywhere — output the check-in only.
