---
up: "[[repos/fire]]"
source: https://github.com/nitsuah/fire/blob/main/docs/TASKS.md
kind: repo-doc
repo: fire
---

# Tasks

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

updated: 2026-09-24

---

## In Progress

_None — PR #111 (Product/UI + reliability pass) merged 2026-09-19; see
`docs/CHANGELOG.md`'s Unreleased section for the full detail and `docs/FEATURES.md`
for shipped capabilities. Its follow-up items are below._

---

## Follow-ups from PR #111 — Sep 2026

- [ ] Manual step: register the public HTTPS notification URL + verification token in the eBay Developer Portal (cannot be verified in CI)
- [ ] Stop exposing browser helpers as classic-script globals (`app/lib/fetch-utils.js` `fetchJson`, and the rest of `app/lib/**`)
  - Priority: P3 (maintainability) — deferred from PR #111 review (CodeRabbit, `fetch-utils.js` thread).
  - Context: the SPA loads ~40 plain `<script>` files that share one global scope, so any helper is a cross-file global by design. Fixing just `fetchJson` would mean converting every consumer to `import`; doing it properly means moving the frontend to ES modules with a bundler (or native `type="module"`) as one migration.
  - Acceptance Criteria: decision recorded (native modules vs. bundler), helpers exported/imported explicitly, `no-undef` lint enforced for cross-file references, and the Playwright suite still green.

---

## PROD Phase 1 — Real-Time Data Connectors ✅ (open items in ROADMAP.md 2027 Q1)

- [ ] Model real eBay fee brackets in `calculateEbayFeesTotal` (`app/lib/side-gig.js`), not just a flat rate + order fee.
  - Priority: P2
  - Context: flagged by CodeRabbit on PR #103 (2026-09-10) — the calculator (pre-existing, not introduced by that PR) applies one percentage across the whole transaction value with the pre-#103-corrected $0.30 order fee. Real eBay fee structure has marginal percentage tiers above each category's sale cap, and several categories' effective rate changes at that cap. The $0.30-vs-$0.40 order-fee threshold was fixed directly (order value ≤$10 vs. >$10); the marginal-bracket-per-category modeling was not — it needs each category's actual cap/tier data (not currently captured anywhere in this codebase) and a real per-category fee-rule schema, not a scalar percentage dropdown.
  - Acceptance Criteria: `ebay-category-rate` stores a fee-rule identifier (not a bare percentage), and `calculateEbayFeesTotal` resolves that rule's tiers/caps rather than multiplying one flat rate across the full transaction value.
  - Also covers: `/ebay/refresh` remains the one eBay sync route without a route-level (HTTP) test.

---

## PROD Phase 2 — Financial Institution Integration ✅ (see ROADMAP.md 2027 Q2)

Plaid transaction sync implementation detail (cursor handling, category
resolution, partial-failure edge cases) moved to `CHANGELOG.md`. Known gaps:
`/plaid/create-link-token`, `/plaid/exchange`, `/plaid/positions`, and
`/plaid/accounts` remain without route-level (HTTP) tests; no automated e2e
test confirms the disabled Fidelity CSV drop-zone is actually inert while
Plaid sync is active (only the underlying status the gate reads is covered).

### Real-Time Price Improvements
- [ ] Write tests for `app/lib/prices-provider.js` (Alpha Vantage + Polygon paths)

---

## PROD Phase 3 — Security Hardening ✅ (see ROADMAP.md 2027 Q3; remaining item below)

See [security-hardening.md](./security-hardening.md) for full remediation detail.

- [ ] Run full penetration testing checklist from docs/security-hardening.md
  - Reviewed the checklist (see docs/security-hardening.md) and triaged which items
    are checkable from this sandboxed dev environment vs. which need a real deployment:
    - **Checkable here (sandbox/unit-test level):** all of Authentication & Authorization
      except session-cookie forgery edge cases already covered incidentally; all of
      Injection; all of Information Disclosure; all of Denial of Service; MCP-Specific
      "no write tools" (now covered) and "audit log excludes response content" (log
      format is inspectable directly). Rate-limit-window-reset is checkable but needs
      fake timers or a real 60s wait.
    - **Needs a live/running deployment:** the entire Transport section (HTTP→HTTPS
      redirect, `Strict-Transport-Security` header, `Secure` cookie flag) requires an
      actual TLS handshake through the new Caddy container — doable locally via
      `docker compose -f config/docker-compose.yml up -d` + `curl -kv https://localhost`,
      but not a unit test. MCP "makes no external network calls" is only rigorously
      verifiable with the process's network access physically disabled (OS-level
      firewall / no-network container) — mocking `fetch` in a test is a reasonable
      proxy but not proof. OAuth CSRF replay and `tokens.json` encryption-after-callback
      both need a real (or fully mocked) OAuth provider round-trip, which exists only
      partially in the current test suite.
  - Not attempted as part of this pass — flagging for a follow-up task.

_Coverage: branch coverage is back above the 70% threshold (74.85%, 484 tests, #119) and CI now enforces it via `npm run test:coverage`; see `docs/METRICS.md`._

---

## PROD Phase 4 — Feature Parity (2027 Q4)

- [~] Portfolio rebalancing suggestions — v1 tool on the Insights tab (targets vs. current); suggestion polish pending
- [~] Tax-loss harvesting alert — v1 table on the Insights tab; threshold config/notifications pending
- [ ] Income vs. expense 12-month rolling trend view
- [ ] PWA: `manifest.json` + service worker for installable offline mode
- [~] CD maturity and FIRE milestone notification system — in-app alerts bell + browser-notification settings shipped; push/outbound delivery pending
- [ ] Optional multi-user mode (separate encrypted db.json per user, HTTP Basic auth gate)

---

## Completed ✅

_Fully condensed into `docs/FEATURES.md` (shipped capabilities), `docs/ROADMAP.md`
(milestones), and `docs/CHANGELOG.md` (change-by-change history) — see those
files rather than a duplicated list here._
