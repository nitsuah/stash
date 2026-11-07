---
up: "[[repos/fire]]"
title: "fire · canonical-transactions"
source: https://github.com/nitsuah/fire/blob/main/docs/canonical-transactions.md
kind: repo-doc
repo: fire
---

# Canonical transaction model

> This page distinguishes current Stripe mapper behavior from the future cross-provider reconciliation policy. The mapper does not currently link Stripe, eBay, Etsy, or manual rows together.

## Canonical key and provenance

- The pure Stripe balance-transaction mapper emits a ledger row id of `stripe-<txn id>` and keeps the raw provider id in `stripeTxnId`. The id is source provenance, not proof that another provider row is the same sale.
- The mapper currently has no Stripe account-id input. The account-scoped canonical key described in [the overlap audit](stripe-overlap-audit.md) is `stripe:<account id>:<balance transaction id>`; it is a future storage/reconciliation key, not the current mapper's row id.
- eBay rows keep `ebay-<orderId>`; Etsy rows keep `etsy-<receipt_id>`; manual rows keep their user-created ids. Keep those source ids when reconciling.

## Counting rules (current Stripe mapper)

- Only USD balance transactions with a `txn_` id and a valid UTC `created` date are mapped. Integer minor units become dollars rounded to cents.
- `charge` / `payment` are sale rows. `refund`, `payment_refund`, and `adjustment` are separate negative refund/reversal rows with their own ids. A `stripe_fee` row has zero gross and a fee expense.
- `net = gross - fees`. Payouts, payout cancellations, payout failures, non-USD entries, invalid ids/dates, and unsupported types are skipped with a reason; a payout is never income.
- Duplicate Stripe transaction ids within one input batch are collapsed first-wins. Do not deduplicate by matching amount and date.
- The mapper is pure and offline. It does not fetch transactions, reconcile across providers, or change existing ledger rows.

## Cross-provider overlap

The same economic sale can appear as a Stripe charge, an eBay/Etsy sale, or a manual ledger row. Those records have different source ids and must not be silently merged based on amount/date.

The intended reconciliation policy is an explicit user-confirmed link: retain each source's provenance, count one canonical economic transaction, and store the link so the relationship is auditable. That link/merge workflow is **not implemented by the current mapper**. Fire's current CoinTracker integration imports wallet/balance data only; it does not ingest CoinTracker transactions or cost basis into this ledger. Those MCP capabilities are outside the current Fire integration/transaction model.

## Suspected duplicates and user correction

- The existing CoinTracker card can surface possible manual-wallet duplicates, but there is no Stripe/eBay/Etsy cross-provider duplicate-candidate or link UI today.
- If a user confirms that a ledger row is a duplicate, compare the provider-specific id and source details first. The existing Side Gig Ledger `Delete` action can remove the duplicate row manually; this is a user decision, not an automatic reconciliation step. Do not delete a row based only on amount/date.
- The app currently does not store a cross-provider link when a user deletes a duplicate. If the relationship must remain auditable, keep both source rows and record the need for a future link feature rather than claiming the link is stored.

## Known limitations

- The current Stripe mapper is USD-only and supports only the transaction types listed above.
- It deduplicates repeated Stripe transaction ids only; it does not detect Stripe/eBay/Etsy/manual overlap.
- Account-scoped keys, explicit cross-provider links, and a duplicate-review UI remain future reconciliation work.
