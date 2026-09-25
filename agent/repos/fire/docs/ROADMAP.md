---
up: "[[repos/fire]]"
source: https://github.com/nitsuah/fire/blob/main/docs/ROADMAP.md
---

# 🗺️ FIRE Tracker Roadmap

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

updated: 2026-09-24

> 2027 planning reset (2026-09-24): 2026 Q2 (foundation & calculators), 2026 Q3 (side hustle hub), all shipped
> 2026 Q4 items, and every shipped PROD Phase 1–3 item were removed from this file — see [FEATURES](./FEATURES.md)
> and [CHANGELOG](./CHANGELOG.md). Open 2026 Q4 items were carried into 2027 Q1. PROD Phases 2–4 keep their existing
> 2027 Q2–Q4 slots with only their open items. Full productionization detail: [prod-plan.md](./prod-plan.md).

---

## 2027 Q1 — PROD Phase 1 Close-out + Carried Items 🧪

PROD Phase 1 (real-time data connectors: eBay API, Web3 wallets across 9 chains, vehicle value, encrypted Drive backup) is shipped; these are what's left, plus open 2026 Q4 items.

- [ ] Model real eBay marginal fee brackets per category (needs per-category cap/tier data) *(PROD Phase 1)*
- [ ] Tax drag estimation engine (custom federal/state brackets, capital gains) *(carried from 2026 Q4; side-gig tax tagging #120 is a first input)*
- [ ] Lightweight PWA packaging *(carried from 2026 Q4; the installable/offline PWA in Phase 4 builds on this)*

---

## PROD Phase 2 — Financial Institution Integration (2027 Q2) 🏦

Goal: real-time read-only position and balance sync from major brokerages and banks.

### Real-Time Price Improvements
- [ ] Unit tests for `app/lib/prices-provider.js` (Alpha Vantage / Polygon / fallback paths)

### Car Values
- [ ] KBB API requires Cox Automotive partner agreement

---

## PROD Phase 3 — Security Hardening (2027 Q3) 🔐

Goal: harden the system for shared-machine and LAN-facing use.
Full detail: [security-hardening.md](./security-hardening.md)

- [ ] Penetration testing checklist (see [security-hardening.md](./security-hardening.md))

---

## PROD Phase 4 — Feature Parity (2027 Q4) 🚀

Goal: match Fidelity NetBenefits + Rocket Money from a tracking standpoint while preserving local-first privacy.

- [~] Portfolio rebalancing suggestions — v1 tool shipped on the Insights tab (target vs. actual); suggestions/refinements pending
- [~] Tax-loss harvesting alerts — v1 table shipped on the Insights tab; threshold config and notifications pending
- [ ] Income vs. expense 12-month rolling trend
- [ ] PWA — installable, offline-capable
- [~] Notification system — in-app alerts bell and browser-notification settings shipped; push/outbound delivery pending
- [ ] Optional multi-user mode (separate encrypted db.json per user, auth-gated)
- [ ] **Unified sync-health widget** — one settings panel showing last-sync time, status, and a manual "sync now" per connector (eBay, Plaid, each wallet chain, Drive backup), instead of a separate last-sync indicator per integration.
- [ ] **Outbound webhook / notification hook** — the webhook framework (`app/lib/webhook-integration.js`) is inbound-only today. A scheduled outbound POST of a net-worth/FIRE-progress snapshot to a user-supplied webhook URL (Discord, Slack, ntfy) would reuse the existing HMAC + JSONata infrastructure in reverse and is a natural pairing with the planned CD-maturity notification system.

## Ideas — not yet scheduled

- **Sequence-of-returns risk indicator** — the retirement projection already models bull/bear scenarios and drawdown after retirement age; surface a single risk badge (e.g. "vulnerable to a down year in your first 5 retired years") derived from the existing SWR curve math rather than adding a new calculation engine.
