---
up: "[[repos/fire]]"
title: "fire · TASKS"
source: https://github.com/nitsuah/fire/blob/main/docs/TASKS.md
kind: repo-doc
repo: fire
---

# Tasks

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

updated: 2026-09-28

---

## Priority product/reliability pass — Sep 27, 2026

These items came from the current browser/production pass. **P0** items are correctness, data-integrity, security, or broken-primary-workflow issues; **P1** items are high-value UX/integration work that should follow immediately.

### P0 — Data integrity & broken primary workflows

- [x] **Fix gold/silver spot-price API 400/non-JSON failures**
  - Completed in PR #138: hosted Netlify routing reaches the metals handler; Yahoo fallback uses browser-like headers plus query1/query2 fallback; non-JSON upstream failures become structured JSON errors.
  - Done 2026-09-28: PR #138 merged

- [x] **Fix wallet/ENS refresh and return aggregate cross-chain USD value**
  - Completed in PR #138: hosted ENS resolution fans out across supported EVM chains, aggregates successful USD values, and returns JSON-safe errors while preserving partial results.
  - Done 2026-09-28: PR #138 merged

- [ ] **Google Drive backup round-trip verification before rollout**
  - Priority: P0. Backup is financial data and must not be considered production-safe until encryption, upload, download, and decryption have been proven end-to-end.
  - Scope: browser-first Google login/connect flow; link the Drive account before exposing backup actions; encrypt locally/server-side with the existing AES-256-GCM design; add an explicit test fixture that uploads an encrypted backup, downloads it, decrypts it, and byte/structure-compares the restored payload.
  - Acceptance Criteria: Google OAuth connect works from the browser; Drive only receives ciphertext; a fresh restore succeeds against a real or deterministic mocked Drive round trip; corrupted/wrong-key backups fail cleanly; UI cannot report a successful backup until the round-trip verification succeeds.
  - Rollout gate: do not change the README/marketing copy to imply backup safety beyond the tested guarantees until this passes.

### P1 — Integration & workflow improvements

- [ ] **Serve Plaid on the Netlify deploy (lifefire.netlify.app)**
  - Priority: P1. Hosted browser deployment must support the same Plaid Link → exchange → accounts → positions → transactions workflow as Express; a JSON-safe 404/status stub is not sufficient.
  - Scope: split Plaid from app/routes/sync.js, extract transport-agnostic Plaid operations, expose the required Netlify Functions/rewrites, preserve encrypted browser/local-first token handling, and keep Express behavior unchanged.
  - Acceptance Criteria: Link, public-token exchange, account/position refresh, and transaction sync all work on lifefire.netlify.app; each hosted function has unit coverage; browser smoke coverage exercises the hosted routes; no /api/sync/plaid/* request can fall through to an HTML Netlify 404.

- [ ] **Split app/routes/sync.js (942 LOC): separate eBay and Plaid routes, extract the transactions handler (F-20260916-05)**
  - Priority: P1. The route grew with the eBay/Plaid work and should be decomposed before another integration lands.
  - Scope: separate eBay and Plaid route modules, extract the Plaid transactions handler, keep webhook/template routes isolated, and move shared provider logic into transport-agnostic modules where practical.
  - Findings ledger: F-20260916-05 · BV 5 · TC 3 · RR 5 · size 3.
  - Acceptance Criteria: existing Express route paths and response contracts remain unchanged; Plaid and eBay tests pass; transaction pagination/cursor semantics remain unchanged; hosted Netlify Plaid functions can reuse the extracted Plaid operations without importing the Express router.

- [ ] **CoinTracker MCP integration for wallet discovery/investigation**
  - Priority: P1.
  - Goal: reduce manual wallet tracking and avoid unnecessary direct API calls by using CoinTracker's MCP integration where users already have wallet/activity data available.
  - Scope: define a provider boundary rather than coupling wallet UI directly to CoinTracker; use CoinTracker for discovery/investigation/history where appropriate, retain fire's normalized wallet/account model and aggregate USD value, and fall back to existing direct chain providers when CoinTracker is unavailable or incomplete.
  - Acceptance Criteria: provider capabilities and data ownership are documented; duplicate calls are avoided; users can see provider/source and last-refresh state; no private keys or signing capability are ever requested; existing direct-chain tracking remains functional.

- [x] **Move eBay connector into the Side Hustle Hub**
  - Completed in PR #138: eBay is now a compact Side Hustle Hub integration with connection state and manual/automatic sync controls.

- [ ] **Make eBay connection completion a toast + automatic sync**
  - Priority: P1.
  - Current behavior: browser callback shows `eBay connected. Use Settings → eBay Order Sync → Sync Now.`
  - Scope: replace the alert with the site's toast system; immediately start a sync after a successful connection; show progress/success/failure without requiring navigation to Settings.
  - Acceptance Criteria: successful OAuth returns to the Side Hustle Hub, a non-blocking toast appears, sync starts automatically, and the ledger refreshes when complete. Failure leaves the connector connected and gives an actionable retry state.

- [ ] **Normalize Side Gig Ledger form controls to the site theme**
  - Priority: P1.
  - Scope: style `Tag all`, tax-tag selects, and item-cost inputs using the existing CSS tokens/components rather than browser/default white controls.
  - Acceptance Criteria: controls match dark/glass theme in desktop and mobile, retain accessible focus/contrast states, and have Playwright coverage at the Side Hustle Hub viewport sizes.

### P1 — GitHub README / promo parity

- [ ] **README feature-parity and product-story refresh**
  - Priority: P1.
  - Add/verify the user-facing story for: Side Gig tax tagging + cost basis, automatic eBay order sync, encrypted Google Drive backup, vehicle valuation, local-first/privacy model, browser demo, MCP/LLM workflow, diversification/rebalancing/harvesting insights, notifications/alerts, and CSV/Plaid ingestion.
  - Remove or qualify claims that depend on rollout-gated work (especially Google Drive).
  - Add a compact architecture/privacy diagram or equivalent visual explanation and a clearer “Try it / Run it / Ask Claude” path.
  - Acceptance Criteria: every prominent README feature is either demonstrably shipped or explicitly labeled planned; no stale environment/setup instructions remain; links to the live demo, docs, security model, and integration setup are easy to find.

- [ ] **Promo ledger audit**
  - Priority: P1.
  - `promo/features.md` currently has several shipped capabilities marked as capture-needed and several important current capabilities absent from the primary promo story.
  - Add capture targets for tax tagging, automatic eBay sync, Google OAuth backup/linking, wallet aggregate value, vehicle valuation, notification/alert UX, and the Side Hustle Hub connector.
  - Reconcile chain count/source-of-truth claims across README, FEATURES, promo, and `config/chains.json`.
  - Acceptance Criteria: promo claims map one-to-one to README/FEATURES capabilities and no promo asset claims behavior that the product does not currently provide.

- [ ] **Feature-discovery pass for the GitHub landing page**
  - Priority: P1.
  - Add a short “What makes fire different” section emphasizing local-first storage, encrypted-at-rest option, read-only external integrations, MCP/LLM access, and the breadth of tracked asset types.
  - Surface screenshots/demo links and the production/security posture above the long architecture details.
  - Keep README scannable: move implementation-heavy material below the product story rather than deleting technical documentation.

### Follow-up architecture / tests

- [ ] **Add provider-contract tests for all price/balance integrations**
  - Priority: P1. A common failure mode is a provider returning HTML/plain text while the browser assumes JSON.
  - Acceptance Criteria: shared fetch helper tests assert content-type/body diagnostics; route tests assert JSON error envelopes; provider adapters never leak raw HTML into user-facing errors.

- [ ] **Add sync-health state to the Side Hustle Hub**
  - Priority: P1. Pair the eBay move with the roadmap's broader connector-health direction: connected/disconnected, last attempt, last success, and actionable failure.
  - Acceptance Criteria: eBay exposes last sync state in the hub; architecture can later extend the same component to Plaid, wallets, and Drive.

---

## In Progress

_None — PR #111 (Product/UI + reliability pass) merged 2026-09-19; see
`docs/CHANGELOG.md`'s Unreleased section for the full detail and `docs/FEATURES.md`
for shipped capabilities. Its follow-up items are below._

---

## Todo

### Follow-ups from PR #111 — Sep 2026

- [ ] Serve Plaid on the Netlify deploy (lifefire.netlify.app)
  - Priority: P1. Plaid Link, positions, accounts and transactions (`/api/sync/plaid/*`) only exist in Express, so on the static Netlify deploy every call returns 404, even though the Plaid env vars are set there.
  - Approach: follow eBay's pattern from PR #130: v2 Netlify Functions plus `netlify.toml` rewrites, with logic shared with Express via a transport-agnostic module. Plaid access tokens go back to the browser encrypted with `SYNC_MASTER_KEY` instead of being stored server-side, and status and the toggle are computed client-side in browser-only mode.
  - Acceptance Criteria: Link → exchange → accounts/positions/transactions works on the live site; unit tests for each Function; privacy policy and `docs/integrations.md` updated.
  - Rule going forward: any new `/api/*` route the SPA calls needs a Netlify Function (or a documented browser-only fallback) in the same PR.
- [ ] Stop exposing browser helpers as classic-script globals (`app/lib/fetch-utils.js` `fetchJson`, and the rest of `app/lib/**`)
  - Priority: P3 (maintainability) — deferred from PR #111 review (CodeRabbit, `fetch-utils.js` thread).
  - Context: the SPA loads ~40 plain `<script>` files that share one global scope, so any helper is a cross-file global by design. Fixing just `fetchJson` would mean converting every consumer to `import`; doing it properly means moving the frontend to ES modules with a bundler (or native `type="module"`) as one migration.
  - Acceptance Criteria: decision recorded (native modules vs. bundler), helpers exported/imported explicitly, `no-undef` lint enforced for cross-file references, and the Playwright suite still green.

---

### PROD Phase 1 — Real-Time Data Connectors ✅ (open items in ROADMAP.md 2027 Q1)

- [ ] Model real eBay fee brackets in `calculateEbayFeesTotal` (`app/lib/side-gig.js`), not just a flat rate + order fee.
  - Priority: P1
  - Context: flagged by CodeRabbit on PR #103 (2026-09-10) — the calculator (pre-existing, not introduced by that PR) applies one percentage across the whole transaction value with the pre-#103-corrected $0.30 order fee. Real eBay fee structure has marginal percentage tiers above each category's sale cap, and several categories' effective rate changes at that cap. The $0.30-vs-$0.40 order-fee threshold was fixed directly (order value ≤$10 vs. >$10); the marginal-bracket-per-category modeling was not — it needs each category's actual cap/tier data (not currently captured anywhere in this codebase) and a real per-category fee-rule schema, not a scalar percentage dropdown.
  - Acceptance Criteria: `ebay-category-rate` stores a fee-rule identifier (not a bare percentage), and `calculateEbayFeesTotal` resolves that rule's tiers/caps rather than multiplying one flat rate across the full transaction value.
  - Also covers: `/ebay/refresh` remains the one eBay sync route without a route-level (HTTP) test.

---

### PROD Phase 2 — Financial Institution Integration ✅ (see ROADMAP.md 2027 Q2)

Plaid transaction sync implementation detail (cursor handling, category
resolution, partial-failure edge cases) moved to `CHANGELOG.md`. Known gaps:
`/plaid/create-link-token`, `/plaid/exchange`, `/plaid/positions`, and
`/plaid/accounts` remain without route-level (HTTP) tests; no automated e2e
test confirms the disabled Fidelity CSV drop-zone is actually inert while
Plaid sync is active (only the underlying status the gate reads is covered).

### Real-Time Price Improvements
- [ ] Write tests for `app/lib/prices-provider.js` (Alpha Vantage + Polygon paths)
  - Priority: P2
  - Type: Tech debt

---

### PROD Phase 3 — Security Hardening ✅ (see ROADMAP.md 2027 Q3; remaining item below)

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
  - Priority: P2
  - Type: Security
  - Not attempted as part of this pass — flagging for a follow-up task.

_Coverage: branch coverage is back above the 70% threshold (74.85%, 484 tests, #119) and CI now enforces it via `npm run test:coverage`; see `docs/METRICS.md`. Re-run the metrics snapshot after this documentation/test pass._

---

### PROD Phase 4 — Feature Parity (2027 Q4)

- [~] Portfolio rebalancing suggestions — v1 tool on the Insights tab (targets vs. current); suggestion polish pending
- [~] Tax-loss harvesting alert — v1 table on the Insights tab; threshold config/notifications pending
- [ ] Income vs. expense 12-month rolling trend view
  - Priority: P2
  - Type: Feature
- [ ] PWA: `manifest.json` + service worker for installable offline mode
  - Priority: P2
  - Type: Feature
- [~] CD maturity and FIRE milestone notification system — in-app alerts bell + browser-notification settings shipped; push/outbound delivery pending
- [ ] Optional multi-user mode (separate encrypted db.json per user, HTTP Basic auth gate)
  - Priority: P3
  - Type: Feature

---

## Done

- [x] Manual step: turn on eBay connect/sync on Netlify. Set `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_ENVIRONMENT=production`, `EBAY_REDIRECT_URI` (RuName) and `SYNC_MASTER_KEY` in Netlify, and point the RuName's auth-accepted URL at `https://lifefire.netlify.app/api/sync/ebay/callback` (see the Browser-only deploy section of `docs/integrations.md`)
  - Done 2026-09-27: env vars set on Netlify; connect/sync verified working in production.

_Fully condensed into `docs/FEATURES.md` (shipped capabilities), `docs/ROADMAP.md`
(milestones), and `docs/CHANGELOG.md` (change-by-change history) — see those
files rather than a duplicated list here._
