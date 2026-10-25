# Project kickoff prompt (MoneyMakers)

Use this prompt to start any MoneyMakers project. Replace the bracketed fields.

---

You are setting up one small earning project for Austin in the MoneyMakers (MM) program.

Project: [name]
Stream type: [service | digital_product | bounty | cash_yield]
Time budget: no more than one day of setup, then monitoring only.

Steps:

1. Read `agent/projects/MM/README.md` and `agent/projects/MM/human-vs-agent.md`. Follow the rules there.
2. Draft a proposed row for the Neon `projects` table (project `moneymakers`, `divine-surf-90579532`), including `status = building`, `kill_rule`, and `kill_date`. Show the proposed values to the user and wait for explicit approval before writing to Neon or starting work.
3. Draft what's needed: listing or product copy, sample output, a setup checklist. Save drafts only.
4. Make a list of anything that needs a human (accounts, KYC, payouts, publishing, ad spend). Put it at the top of the summary.
5. Do not publish, send, submit, or spend money. Stop before any irreversible step and ask.

Return: what you drafted, what the human needs to do (in order), and the `projects` row you updated.
