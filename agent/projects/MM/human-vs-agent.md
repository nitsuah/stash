# Human vs. agent: who does what

## Human only (you)

These need your identity, your money, or your judgment. Agents should not attempt them.

- **Accounts and identity:** creating or verifying accounts on Stripe, Gumroad, Etsy, Algora, Upwork, Fiverr, and similar. Identity checks (KYC), tax IDs, and legal acceptance of terms.
- **Passwords and 2FA:** any password entry or 2FA code. Agents don't enter credentials.
- **Money movement:** activating Stripe payouts, linking a bank account, transfers between accounts, bids and purchases, ad spend.
- **Public and outward-facing actions:** publishing a listing, posting a product page, sending an email or message, submitting a bounty claim, accepting an invoice, or replying to a client.
- **Decisions:** pricing, which project to kill or keep, and whether to take a client job.
- **Taxes:** filing and anything that changes your tax position.

## Agent can do (with your go-ahead per action)

These are safe to draft or run. The agent prepares the work; you approve anything that goes public or moves money.

- **Research:** compare rates, read marketplace listings, find bounties and buyers, and summarize terms.
- **Drafts:** product descriptions, listing copy, proposals, sample outputs, and email drafts. Saved as drafts only.
- **Local builds:** scripts, templates, and sample files in the repo or in `stash`.
- **Tracker upkeep:** update the `projects` and `money_events` rows in Neon with hours, costs, and status. Read-only checks on FIRE data.
- **Browser checks** (your browser, your sessions): read pages, check listing status, and fill forms up to, but not including, the final submit or buy click. Anything irreversible needs your explicit yes first.
- **Stripe and Neon setup:** draft products and prices in Stripe as inactive, and create Neon schemas or tables for project data. Activation and any live keys stay with you.

## Browser rules

- Read-only browsing is fine.
- Forms: fill in, then stop. You click submit.
- Never enter payment details, bank details, or passwords. You do that yourself.
- Before any irreversible click (buy, send, publish, post, delete), confirm with you first.

## Setup overlap

These shared pieces make each project faster to start:

1. One Stripe account for all products (human sets it up once).
2. One Neon database for project data, with one table per project type.
3. Drafts live in the repo under `stashgent\projects\MM`.
4. One Gmail for outbound drafts, reviewed before sending.
5. `money_events` in Neon for all money events.
