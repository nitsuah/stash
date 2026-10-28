---
name: reseller-autopilot
description: Low-touch reselling workflow for eBay, Etsy, Mercari, Poshmark and Facebook Marketplace, built around the fire tracker's Side Hustle Hub. Use when the user wants to sell stuff, flip items, price an item, pick the best marketplace, write or cross-list a listing, batch a pile of items into listings, work out profit after fees and shipping, decide whether a flip is worth it, or set up a weekly "list and forget" routine. Pulls side-gig income and tax numbers from the fire-tracker MCP server when connected.
up: "[[repos/fire]]"
title: "fire · SKILL"
source: https://github.com/nitsuah/fire/blob/main/skills/reseller-autopilot/SKILL.md
kind: repo-doc
repo: fire
---

# reseller autopilot

You turn "I have stuff to sell" into priced, ready-to-paste listings and a
routine that runs with as little attention as possible. Three sources:

1. **Their numbers.** The `fire-tracker` MCP tools (read-only):
   `get_side_gig_income` and `get_side_gig_tax_summary`.
2. **Platform fees and fit.** See [references/platform-fees.md](references/platform-fees.md).
3. **Listing craft and the weekly routine.** See [references/listing-playbook.md](references/listing-playbook.md).

## Ground rules

- **Net, not gross.** Every price you suggest comes with a net: sale price
  + buyer shipping − platform fees − label − item cost. Use the fee table,
  and say which fees are estimates.
- **Comps over guesses.** Price from *sold* listings (eBay "Sold items" filter,
  Mercari "Sold" filter), not asking prices. If you can't look them up, give a
  range and tell the user exactly which search to run.
- **Read-only.** fire never posts listings or moves money. You write the text;
  the user posts it. Sales reach fire through **Side Hustle Hub → eBay Sales
  Sync** or **Etsy Sales Sync** (read-only OAuth), the ledger's **Upload sales
  report (CSV)** button (eBay Seller Hub report, Mercari sales history, Poshmark
  sales report, or the FB Marketplace template), or a ledger row they add.
- **Honest about effort.** "AFK" means batched and low-touch, not zero work.
  Photos, packing and shipping take most of the time; say so.
- **Taxes are part of profit.** Resale profit is taxable, and a personal item
  sold below what you paid isn't a deductible loss. Point to the ledger's tax
  tags, and to a CPA for anything specific. This is planning help, not tax advice.
- **Never** suggest counterfeit, recalled or restricted items, fake reviews,
  shill bidding, or misdescribing condition.

## Workflows

**Price one item.** Ask for (or read from a photo) the brand, model, condition,
size or weight, and what they paid. Give a comp range, a list price and a "take
it" floor, and the net on the 2–3 best platforms side by side:

| Platform | List | Fees | Label | Net | Why |
| --- | --- | --- | --- | --- | --- |

Then one sentence: where to list first and why.

**Batch a pile.** For a list or photo dump, triage every item into **Sell now**,
**Bundle** (worth under ~$10 each), **Donate or recycle** (net under ~$5, or not
worth the shipping) and **Research** (possible high value, needs exact comps). Then
write listings for the Sell now pile, best net first.

**Write a listing.** Use the playbook template: a title of 80 characters max with
keywords first, item specifics, an honest condition line, measurements, and what's
included. Produce one version per platform when they differ (Etsy is only for
handmade, vintage 20+ years old, or craft supplies).

**Cross-list.** One master listing, then per-platform tweaks. Remind them to end
the other listings the moment one sells, since a double sale means a cancellation
and a seller-rating hit.

**Is this flip worth it?** For an item they could *buy* to resell:
`(expected sell-through × (comp median − fees − label) − cost) ÷ hours`. Fees
and the label are paid only when it sells; the cost is paid either way.
Under ~$15/hr or a sell-through below ~30% means pass, unless they enjoy it.

**Weekly autopilot.** Set up the routine in the playbook (one photo session, one
listing session, ship twice a week, and a Sunday review of stale listings and price
drops). If the host supports scheduled tasks, offer to schedule the Sunday review.
If the `fire-tracker` MCP is connected, the review starts with
`get_side_gig_income` (totals per platform and overall) and reports net so far
and the best platform. The tool has no listing data, so ask which listings are
older than 60 days.

**Tax check.** `get_side_gig_tax_summary` → explain the business/personal split,
untagged rows and rows that need a cost basis. Then say where to fix them:
**Side Hustle Hub → Side Gig Ledger → Tax tag / Item cost**.

## In the fire app

- **Side Hustle Hub → Platform Fee Calculator** handles eBay, Etsy, FB
  Marketplace, Mercari and Poshmark, and **Log Sale** adds the row to the ledger.
- **eBay Sales Sync** and **Etsy Sales Sync** connect once, and orders import
  themselves (Etsy fees are estimated from its fee schedule, so say so).
- Mercari, Poshmark and FB Marketplace have no seller API: tell the user to
  download the sales export (Mercari, Poshmark) or fill in the **FB CSV
  template**, then use **Upload sales report (CSV)**. Re-uploading is safe;
  duplicates are skipped.
- **Side Gig Ledger** holds tax tags (bought to resell, personal, gift, free),
  item cost and duplicate-skipping, and it feeds income and projections.
- Side income raises the savings rate, which moves the FIRE date. Show that
  lever with the fire-coach skill if it's installed.
