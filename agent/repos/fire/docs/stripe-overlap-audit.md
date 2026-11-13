---
up: "[[repos/fire]]"
title: "fire · stripe-overlap-audit"
source: https://github.com/nitsuah/fire/blob/main/docs/stripe-overlap-audit.md
kind: repo-doc
repo: fire
---

# Stripe overlap audit

> 🧭 [fire](../README.md) · [Integrations](./integrations.md) · [Status matrix](./integration-status-matrix.md) · **Stripe overlap audit** <!-- nav -->

Part of #261 (owner decision 2026-10-28: build a live read-only Stripe connector, after this audit, a canonical-transaction model and server-side credential storage).

## What already writes income

| Source | Where it lands | Identity today |
| --- | --- | --- |
| eBay Order API (`app/lib/ebay-connector.js`) | `state.sideGigLedger` | `id: ebay-<orderId>`, fields `platform, date, description, gross, fees, net, orderId` |
| Etsy Open API (`app/lib/etsy-connector.js`) | `state.sideGigLedger` | `id: etsy-<etsyReceiptId>` |
| Manual side-hustle entries | `state.sideGigLedger` | free-form `id` |
| Plaid transactions and CSV import | `state.spendingTransactions` (spending view, not the side-hustle ledger) | Plaid `transaction_id`, or none for CSV |

Side-hustle income is `getSideGigYTDNet`: the sum of `net` over `state.sideGigLedger`. Anything Stripe adds to that ledger counts as income immediately, so it must be a sale, never a transfer of money already earned.

## Where Stripe can overlap

1. **eBay and Etsy.** Both pay sellers out through their own payment systems, not through the seller's Stripe account. A seller's Stripe account therefore holds none of those sales, and the ledger rows do not collide: eBay and Etsy rows carry their own ids and Stripe rows will carry Stripe ids. The risk is a user who also keeps a manual row for the same sale.
2. **Bank deposits seen by Plaid or CSV.** A Stripe payout lands in a bank account, and Plaid or a CSV import can show it as a deposit. Those rows live in `spendingTransactions`, which is not summed as income, but any future feature that reads deposits as income must exclude Stripe payouts.
3. **The same Stripe sale arriving twice.** A balance transaction can be fetched on several syncs and delivered by webhook as well. This is the main duplicate risk, and the key below solves it.
4. **Refunds and disputes.** They reduce an earlier sale. They are separate balance transactions with their own ids and must be separate negative rows, not edits to the sale row.

## Canonical key

**Canonical key:** `stripe:<account id>:<balance transaction id>`, for example `stripe:acct_123:txn_456`. The ledger row id is `stripe-<balance transaction id>`, matching the `ebay-` and `etsy-` convention. Amount-and-date matching is never used to decide that two rows are the same.

## Counting rules

- Charges and payments are sales: `gross` is the amount, `fees` is Stripe's fee, `net` is gross minus fees.
- Refunds, partial refunds and lost disputes are negative rows with their own ids.
- Stripe fees that are not tied to a charge are rows with `gross` 0 and the fee as `fees`.
- **Payouts are never income.** A payout, payout cancellation or payout failure moves money already counted by its underlying sales, so it is skipped and reported, never added.
- Any other balance transaction type is skipped and reported until a rule is written for it.

## Follow-ups

The canonical-transaction mapper, the server-side credential store (owner-gated), the read-only client, the sync route and the webhook are separate children of #261, in that order.