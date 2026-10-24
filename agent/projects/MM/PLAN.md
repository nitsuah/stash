# MoneyMakers plan

## Principles

1. **Scripts do the repeatable work; LLMs do judgment only.** Scanning, scraping (within site terms), file conversion, scheduling, and reporting should run as plain code with zero tokens. An LLM is called only for drafting, classifying replies, and quality checks.
2. **Templates before generation.** A report, invoice, or sample is a template filled by code. Generate free-form text only where a client would notice the difference.
3. **State lives in Neon, not in chat.** Each bot reads its project row and its last run from the `moneymakers` database. It doesn't carry conversation history from run to run.
4. **Humans own money, identity, and anything sent to a person.** Accounts, KYC, payouts, ad spend, publishing, and outreach messages go through a human approval step.
5. **Every project has a kill rule and a token budget.** A project that spends more on tokens than it earns gets paused automatically.

## Classification

- **One-and-done:** build once, then sell or earn passively. Bot's job is mostly done after setup.
- **Repeatable, no customer:** runs on a schedule and produces output that is sold or sponsored.
- **Repeatable, customer-driven:** each job needs a customer. The bot can do the work but finding customers is the bottleneck.
- **Hunt-required:** needs outreach (email, LinkedIn, cold calls, ads). Outreach is the bottleneck, and it's human-gated.

## Projects

Estimates are rough, not measured. Token costs are estimates until the first runs are logged.

| Project | Type | Human does | Bot does | Token approach | First $100 path | Kill rule |
|---|---|---|---|---|---|---|
| Digital template packs (Gumroad) | One-and-done, then passive | Gumroad account, final listing click | Builds templates, writes listing copy, exports files | Templates by code, one LLM pass for copy | 5 sales at ~$20 | 5 sales in 60 days or pause |
| Icon and sound packs (itch.io) | One-and-done | itch.io account, publish click | Generates assets with local tools, packs files | Zero LLM after setup | 20 sales at $5 | 0 sales in 90 days |
| Uptime and broken-link monitoring | Repeatable, customer-driven | Client sales | Runs a monitor, sends reports | Zero LLM in run loop | 10 clients at $10/mo | Under 3 clients in 60 days |
| Accessibility and Lighthouse audit | Repeatable, hunt-required | Outreach approval, client calls | Runs pa11y and Lighthouse, fills a report template, drafts outreach | Scans and reports are code. One LLM pass for the summary | 1 audit at $100 | 0 paid audits in 60 days |
| Whisper transcription service | Repeatable, hunt-required | Client intake approval | Runs Whisper and ffmpeg, writes SRT, checks output | Zero LLM for transcription. Light LLM check only | 4 jobs at $25 | 0 paid jobs in 60 days |
| Code-health report (repo-audit) | Repeatable, hunt-required | Outreach approval | Runs audit scripts, fills report | Scans are code. One LLM pass for the summary | 1 report at $200 | 0 paid reports in 60 days |
| Algora bounties | Repeatable, uncertain | GitHub login, PR review, Stripe payouts | Watches bounty feed, drafts PRs for simple issues | Coding costs tokens. Skip bounties that exceed a set token budget | 1 merged bounty at $100 | No merged bounty in 90 days |
| Sponsor and tip pages | One-and-done setup | Account setup | Writes README and profile copy | Zero LLM after setup | $20 in tips | $0 in 90 days |

## Outreach policy

- **Email:** the bot drafts, the human approves and sends. Include your real name, a physical address, and an unsubscribe line. Cap volume at about 20 per day.
- **LinkedIn:** no automated DMs. Automation violates LinkedIn's terms and can get the account restricted. The bot can draft messages, and you send them yourself.
- **Cold calls and ads:** human only. Ads use a capped test budget with a kill rule.
- **Lead lists:** the bot builds them from public sources, respecting each site's terms and robots rules. It doesn't scrape sites that forbid it.

## Bot assignment

- **One bot per project**, each with its own folder under `stash\agent\projects\MM` and one row in the `projects` table.
- **Cadence:** scheduled runs, not always-on loops. Most scripts run on a timer. The bot wakes only when a decision or draft is needed.
- **Budget:** each bot gets a monthly token budget and logs LLM cost as a `cost` row in `money_events`. A bot that exceeds its budget stops until a human resets it.
- **Shared infrastructure:** one Stripe account, one Neon database, drafts in the repo, and one Gmail for drafts.

## Build order

1. **Week 1:** Uptime monitoring and the audit scanner. Both are code-first, and the scanner output can feed the audit product and outreach.
2. **Week 1 in parallel:** One digital pack and one icon or sound pack. These are one-and-done and don't need customers to start.
3. **Week 2:** Whisper transcription and the code-health report, once a lead list exists.
4. **Later or skip:** Algora bounties. Run them only when a bounty fits a small token budget.

## Open questions for you

1. Which projects should go first? My pick is the audit scanner and one digital pack.
2. What monthly token budget is acceptable per bot?
3. Should outreach drafts go to you for approval, or to a shared Gmail drafts folder?
4. Do you want the uptime monitor to run on your own hardware, or on a cheap host?
