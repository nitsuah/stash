---
up: "[[repos/fire]]"
title: "fire · TASKS"
source: https://github.com/nitsuah/fire/blob/main/docs/TASKS.md
kind: repo-doc
repo: fire
---

# Tasks

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

updated: 2026-10-08

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
  - Progress 2026-09-30 (PR #146): `netlify/functions/plaid.mjs` serves all `/api/sync/plaid/*` routes, with unit coverage and the toml routing test; status is verified on the deploy preview. Remaining: a live Link → sync run on lifefire.netlify.app (set `PLAID_HOSTED_ACCESS_KEY` if `PLAID_ENV` isn't sandbox) and browser smoke coverage.
  - Rule going forward (from the PR #111 follow-up, merged here on 2026-10-01): any new `/api/*` route the SPA calls needs a Netlify Function, or a documented browser-only fallback, in the same PR.
  - `docs/integrations.md` already documents the hosted function (`netlify.toml` rewrite, browser-held AES-256-GCM token, `PLAID_HOSTED_ACCESS_KEY`). The privacy-policy update from the same follow-up still needs checking.

- [x] **Split app/routes/sync.js (942 LOC): separate eBay and Plaid routes, extract the transactions handler (F-20260916-05)**
  - Done 2026-09-30 in fire#146: split into `app/routes/ebay.js` and `app/routes/plaid.js`, with token helpers in `app/lib/token-store.js`; `app/routes/sync.js` is now ~300 LOC. Paths and cursor semantics are unchanged and the tests pass. Accounts/positions responses gained `syncedItemIds`/`warning`.
  - Findings ledger: F-20260916-05 · BV 5 · TC 3 · RR 5 · size 3.

- [ ] **Share Plaid operations between Express and the hosted Netlify function**
  - Priority: P2. Left over from the sync.js split (F-20260916-05, fire#146): `netlify/functions/plaid.mjs` still duplicates the Plaid operations instead of importing a transport-agnostic module.
  - Acceptance Criteria: Express and Netlify share one Plaid operations module with no Express router import; existing route contracts and unit tests stay unchanged.

- [ ] **CoinTracker MCP integration for wallet discovery/investigation** _(blocked on CoinTracker: the test account isn't enrolled in MCP early access)_
  - Priority: P1.
  - Goal: reduce manual wallet tracking and avoid unnecessary direct API calls by using CoinTracker's MCP integration where users already have wallet/activity data available.
  - Scope: define a provider boundary rather than coupling wallet UI directly to CoinTracker; use CoinTracker for discovery/investigation/history where appropriate, retain fire's normalized wallet/account model and aggregate USD value, and fall back to existing direct chain providers when CoinTracker is unavailable or incomplete.
  - Acceptance Criteria: provider capabilities and data ownership are documented; duplicate calls are avoided; users can see provider/source and last-refresh state; no private keys or signing capability are ever requested; existing direct-chain tracking remains functional.
  - Progress 2026-10-01 (#139): the connector runs on Express and Netlify. CoinTracker has no REST API or read token, so it uses OAuth 2.1 + PKCE with dynamic client registration and reads balances over the read-only MCP. Balances merge into Crypto accounts with CoinTracker as the source of truth (address/ENS adoption, a possible-duplicate list, exclusions, partial-sync safety). Added the Settings card and source tags, 42 unit tests, and docs in `docs/integrations.md`. Remaining: connect a real CoinTracker account (MCP is paid/early access), confirm the balance tool and payload shape with "Inspect CoinTracker tools", then tighten the normalizer and close this item.
  - 2026-10-01 live test: the OAuth redirect and login work, but the MCP server answered `401 invalid_token` for the issued token. The follow-up sends an Auth0 `audience` and reports the token shape on a 401. Retest on its deploy preview. Retest result: the token is now correct (MCP audience), but `permissions: []`. The test account isn't enrolled in CoinTracker MCP early access, so this item is blocked on CoinTracker enabling it.

- [x] **Multichain crypto account value (ENS/0x)**
  - Done 2026-10-01: ⟳ Refresh on an ENS/0x crypto account totals native coins and priced tokens across Ethereum, Base, Optimism, Arbitrum and Polygon, plus native BNB and AVAX balances on BNB Chain and Avalanche (native only, no tokens) via keyless Blockscout/publicnode lookups (`app/lib/multichain-balance.js`), with a per-chain breakdown and a partial-result warning. The ENS lookup card uses the same source. It replaced the Ethereum-only ETH balance (`nitsuah.eth`: ~$29 ETH-only → ~$445 including PIXL and Base tokens).

- [x] **Restore hosted gold/silver and crypto refreshes**
  - Done 2026-10-01 (#154, #155): `fire-api` crashed on Netlify (`Cannot find module 'ethers'`), which took down metals too; crypto ⟳ Refresh had no hosted route; the hosted metal refresh threw on an undefined variable; and the retired `cloudflare-eth.com` RPC broke ENS refresh. All fixed and verified against the live site.

- [ ] **CoinTracker export-file fallback when MCP isn't available**
  - Priority: P2. CoinTracker has no public REST API, and its OAuth only offers `mcp:read`/`mcp:write`, so there is no same-login fallback. Exchange balances (not on-chain) could instead come from CoinTracker's holdings/portfolio export, imported in the CoinTracker card when MCP reports `cointracker_no_access`, using the same merge/dedupe rules. On-chain wallets are already covered by the multichain lookup.
  - Blocked on: a sample export file to confirm the column format.

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

### Chaos mode, layout customization, Claude skill — Oct 1, 2026

- [x] **Chaos button for random life events on the projection graph**
  - Shipped: 🌪️ Chaos next to Bear/Bull and on the Dashboard chart; 30 events in 8 categories with life-average odds, age windows and predefined outcome buckets; ▲/▼ markers with hover/tap details on Dashboard and Projections (desktop + mobile); density follows the 1Y/5Y/10Y/All window; seeded with 🎲 reroll.
- [x] **Rearrange and collapse cards on every tab; Dashboard widgets from other tabs; persisted across sessions**
  - Shipped: click-to-collapse titles, ✎ Customize (drag + ↑/↓), ＋ Add widget / ✕ remove on the Dashboard, ↺ Reset; saved in localStorage like the growth-chart size.
- [x] **"SKILL" section: FIRE advice + how to use the app, ready to add as a Claude skill**
  - Shipped: `skills/fire-coach/` (SKILL.md, financial playbook, app guide) and `skills/README.md` install steps.
- [x] **Update the GitHub page for Chaos mode and missing feature details**
  - Shipped: landing page Chaos + "Make it yours" sections with the `chaos-24s` video, the skill in the Claude section, the Plaid footnote updated; README/FEATURES updated.

- [x] **Section layouts: a single card fills its row; per-row column layouts (2/3/4, wide-left/right/center) with a Datadog-style builder**
  - Shipped: section board on every tab, fixed per-tab grids removed, builder canvas with highlighted drop targets and "New section" gaps, phone single-column.
- [x] **Chaos realism: more good events, sensible sequencing, costs that outrun inflation, flat wages**
  - Shipped: follow-up chains (parent care → funeral → inheritance/house, wedding → child → daycare ends, job loss → new job), 7 new positive events, real-terms escalation linked to the inflation setting, promotions as bumps or 5–6 years of extra savings.
- [x] **🛡️ Mitigation tips that offset chaos events (e.g. pet insurance)**
  - Shipped: 10 mitigations in Insights → Portfolio Insights that shrink covered hits and charge premiums in the chaos projection, with per-life saves vs. costs.

### Narrated brags + money-maker skills — Oct 7, 2026

- [x] **Narrate every brag; 30s–1min+ spots that cover every feature**
  - Shipped: offline Kokoro TTS narration in the promo pipeline (`promo/narrate.py`, music ducked under the voice, `captions.srt` per spot); `brag-22s` and `chaos-24s` are now narrated; seven narrated tours built from a shared data-driven composer (`promo/tour/`): `tour-85s`, `plan-65s`, `chaos-60s`, `insights-60s`, `hustle-60s`, `connect-55s`, `yours-60s`. `promo/features.md` maps every feature to a spot. The landing page has a new full-tour section (`site/assets/tour.mp4`), and its hero and Chaos videos are narrated.
  - Also fixed: promo capture failed outside a checkout with `data/` and `node_modules/` (worktrees).
- [x] **Fix: Etsy and FB Marketplace fee calculators never opened**
  - Their panels start hidden by a CSS class, and the tab switch cleared only the inline style. Playwright coverage added (`tests/e2e-ui/side-hustle.spec.js`).
- [x] **Money-maker SKILLS: low-touch ("AFK") income**
  - Shipped: `skills/reseller-autopilot/` (comps-based pricing, eBay/Etsy/Mercari/Poshmark/FB net-after-fees, listing templates, cross-listing, weekly routine, tax check via MCP) and `skills/passive-income-lab/` (8 low-touch streams with realistic ranges and red flags, runway-first rules, income → FIRE-date math, 30-day launch plans). fire-coach hands off to both.
- [x] **Marketplace hookups beyond eBay (Etsy, Mercari, Poshmark, FB Marketplace)**
  - Priority: P1.
  - Scope: an Etsy Open API v3 OAuth (PKCE) receipts sync into the Side Gig Ledger, with the same dedupe, tax-tag and cost-basis model as eBay; CSV/report import for platforms with no seller API (Mercari, Poshmark, FB Marketplace); Mercari and Poshmark fee calculators next to eBay/Etsy/FB.
  - Acceptance Criteria: each connector has hosted Netlify parity (or a documented browser-only fallback), unit tests for parsing/dedupe, a Settings/Side Hustle Hub connection state, and docs in `docs/integrations.md`; the `reseller-autopilot` skill and the `hustle-60s` promo are updated to match.
  - Shipped 2026-10-08: Etsy PKCE receipts sync (`app/lib/etsy-connector.js`, `etsy-handlers.js`, `app/routes/etsy.js`, `netlify/functions/etsy.mjs`, `app/lib/etsy-sync.js`), browser-side Mercari/Poshmark/FB CSV import (`app/lib/marketplace-reports.js`, fixtures in `tests/unit/fixtures/marketplaces/`), Mercari/Poshmark calculator tabs, cards in Side Hustle Hub + Settings, docs, skill and promo.
- [ ] **Etsy: exact fees instead of estimates**
  - Priority: P2.
  - Receipts carry no fee data, so synced rows use Etsy's published schedule (`feesEstimated: true`). Reading the shop's payment-account ledger entries (`/shops/{id}/payment-account/ledger-entries`, also `transactions_r`) and matching them to receipts would give real transaction, processing, Etsy Ads and Offsite Ads fees.
  - Acceptance Criteria: synced rows carry actual fees when the ledger entries can be matched, fall back to the estimate otherwise, and the flag says which.
- [ ] **Verify Mercari/Poshmark export headers against real files**
  - Priority: P2.
  - The parsers use assumed column names with aliases (`docs/integrations.md`). Confirm against a current Mercari sales history and Poshmark sales report download, add any missing aliases and replace the fixtures with anonymized real headers.
- [ ] **Etsy live run against a real shop** (self-hosted and lifefire.netlify.app) once an Etsy app keystring is approved; record the result in `docs/integrations.md`.

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
  - Progress 2026-10-07: `promo/capture-tour.js` now captures tax tagging (seeded ledger), eBay sync, the crypto/ENS form, vehicles, alerts, Drive and every Side Hustle Hub card; `promo/features.md` lists 46 rows with the spots that use each. Remaining: Google OAuth backup/linking and notification UX in a spot (gated/unused), a depleting-seed capture for money run-out, and the chain-count reconcile.

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
- [x] Write tests for `app/lib/prices-provider.js` (Alpha Vantage + Polygon paths)
  - Done 2026-10-09: `tests/unit/prices-provider.test.mjs` (26 tests, all HTTP mocked) covers provider selection, Alpha Vantage and Polygon success paths, 429/HTTP-error/empty/malformed responses, Yahoo fallback, crumb refresh and `fetchYahooChart`.
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

_Coverage: 84.31% stmts / 77.16% branch / 84.66% funcs / 84.97% lines (715 tests, 2026-10-01). CI runs `npm run test:coverage`, but its thresholds apply only to the 8 files in `coverage.include` (`app/server.js` plus 7 `app/lib` calculation/aggregation modules). Routes, managers, `gdrive-backup.js`, Netlify Functions and the browser app are not measured, so CI does not enforce coverage for them. See `docs/METRICS.md`. _

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
