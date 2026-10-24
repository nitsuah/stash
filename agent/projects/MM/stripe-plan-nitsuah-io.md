# Stripe plan: nitsuah.io (interim, from stripe-best-practices skill, NOT the stripe_implementation_planner tool)

Business: professional IT services and consulting. Needs: Payments, Invoicing, Tax. API version 2026-09-30.endive, Node SDK 23.0.0.

## Recommended shape
| Need | Use | Why |
|---|---|---|
| Bill clients for projects and hours | **Invoices API** (hosted invoice page, emailed) | B2B consulting; net terms, no checkout flow needed |
| Retainers / monthly support | **Billing Subscriptions** (`collection_method: send_invoice` or charge_automatically) + Customer Portal | Only if you have recurring clients; no manual renewal loops |
| Quick one-off deposits or fixed-price packages | **Payment Links** or **Checkout Sessions** (omit `payment_method_types`) | No code needed for Payment Links |
| Sales tax | **Stripe Tax** with `automatic_tax: { enabled: true }` on invoices/checkout | Requires head office address + active registration (see below) |

Skip: custom PaymentIntents, Connect, Metronome (no usage billing or marketplace here).

## Setup order
1. **Sandbox first:** `npm i -g @stripe/cli`, then `stripe sandbox create` (or dashboard sandbox). Use a separate sandbox for dev. Use a restricted key (`rk_`), never `sk_`, scoped to Invoices, Customers, Products/Prices, Checkout Sessions, Tax.
2. **Catalog:** one Product per service offering (e.g. "Managed IT support", "Project consulting"); Prices for variants only. Set product tax code from Stripe's Tax Codes API list; you confirm it, don't guess `txcd_`.
3. **Tax Settings:** set head office address (status must be `active`). Then add a registration for each jurisdiction where you are actually registered. Austin is setting up in Tennessee for now and moving to Virginia later. Head office address = the TN address for now; update it on the move. Whether TN (or any state) needs a registration, and whether IT services are taxable there, is a tax advisor question. Until a registration exists, Stripe collects no tax. Without a registration `automatic_tax` silently collects $0.
4. **Customers:** store a full US address (required for tax in the US). Collect tax IDs for B2B.
5. **Invoices:** create draft invoice with `automatic_tax` enabled, finalize, send. Verify with a test Tax Calculation: `taxability_reason` must not be `not_collecting`.
6. **Webhooks (required):** `invoice.paid`, `invoice.payment_failed`, `checkout.session.completed`, `checkout.session.async_payment_succeeded`; with subscriptions add `customer.subscription.*`; add `charge.dispute.created`, `charge.refunded`. Verify signatures; use `StripeClient` instance, not the global key.
7. **Go live:** follow Stripe's go-live checklist; live-mode Tax registrations and keys are set up separately from the sandbox.

## Human-only (per MM rules)
Stripe account activation and KYC, bank link/payouts, live keys, tax registrations, any invoice sent to a real client.
