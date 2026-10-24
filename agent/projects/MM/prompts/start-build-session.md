# Start MM build session (paste into a new chat)

Start the MoneyMakers build per `C:\Users\ajhar\code\stash\agent\projects\MM\PLAN.md`. Read `README.md`, `human-vs-agent.md`, `PLAN.md`, and `prompts\project-kickoff.md` first.

**Scope:**
1. Accessibility/Lighthouse audit scanner. Scripts only, with zero LLM calls in the run loop. Outputs a templated report.
2. One digital template pack. Templates built by code, plus one LLM pass for listing copy.

Both are drafts only. Do not publish, send, create accounts, or move money.

**Tracking:** The Neon project `moneymakers` (`divine-surf-90579532`) has tables `projects` and `money_events`, and view `project_pnl`. Update the rows for these two projects. Log any token cost as `cost` rows in `money_events`. Neon is the only tracker; do not use Google Drive or Sheets.

**Defaults to pick and note in the output** (confirm with the user before going past drafts):
- Token budget per bot (PLAN.md open question 2)
- Whether outreach drafts go to the user for approval or to a Gmail drafts folder (question 3)
- Where the uptime monitor runs (question 4)

**Done looks like:**
- The scanner runs on a sample site and produces a report draft.
- One pack has draft files and listing copy saved under `MM`.
- `projects` and cost rows are updated.
- A short summary lists what the human needs to do next: account signups, publish clicks, and outreach approvals.
