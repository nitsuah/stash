---
kind: eng-loc
repo: skyview
date: 2026-09-16
---

# LOC Report — skyview

> 🧭 [[repos/skyview|skyview]] <!-- nav -->

Mode: `--report` (dry run, no changes made)
Date: 2026-09-16
Source: shallow clone (`--depth 1`) of `nitsuah/skyview` @ `76657ed528c0a4a728a19163c9178ff6f4639d79`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Additional exclusion applied this run: `docs/lighthouse-*.report.{json,html}` — auto-generated Lighthouse audit artifacts checked into `docs/`, not hand-authored source (19,758 combined lines that would otherwise swamp the top-10 with noise).
Note: shallow clone — churn/author history (many-authors, frequent-edits signal) is **not available**; that structural signal is marked "assumed: not confirmed" throughout.

## Inventory Summary
- Tracked source files (post-exclusion): 155
- Total LOC counted: 21,932

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `styles/style.css` | 2014 | CSS | Site-wide stylesheet |
| 2 | `pages/client-portal.html` | 561 | HTML/JS | Client-facing booking portal (markup + inline script) |
| 3 | `index.html` | 561 | HTML | Marketing landing page |
| 4 | `docs/DEPLOYMENT_GUIDE.md` | 514 | Markdown | Deployment documentation |
| 5 | `pages/client-gallery.html` | 505 | HTML | Photo/video gallery page |
| 6 | `docs/CONFIG.md` | 490 | Markdown | Config documentation |
| 7 | `config.js` | 440 | JS | Site identity/branding + analytics bootstrap |
| 8 | `docs/archive/SESSION_SUMMARY.md` | 433 | Markdown | Archived session notes |
| 9 | `docs/PERFORMANCE_CHECKLIST.md` | 433 | Markdown | Perf checklist doc |
| 10 | `scripts/conversion-tracking.js` | 390 | JS | Conversion-funnel event tracking |

Notable files just outside the numeric top 10 but flagged for risk (see below): `netlify/functions/api-bookings.mjs` (349 LOC), `platform/src/pages/AdminDashboard.jsx` (325 LOC).

## Risk Rank & Rationale

1. **`netlify/functions/api-bookings.mjs` — High**
   349 lines, 8 async functions. Structural evidence: imports span auth, database (`sql`), Stripe payments, and transactional email (`./utils/{db,auth,stripe,email}.js`) — routing + payment processing + notification concerns all live in one handler file. `createBooking` (~63 lines) and `completeBooking` (~61 lines) are both near the 80-line guideline; `payoutAndInvoice`/`issueInvoice` add a third concern (accounting) on top. No dedicated test file found (`grep -rl` for booking-related test names returned nothing) — assumed: no test coverage, not confirmed via a coverage tool. High refactor ROI given it touches money.

2. **`pages/client-portal.html` — Medium-High**
   561 lines, with a 238-line inline `<script>` block embedded in the markup — mixed concerns (structure + client-side booking logic in one file). No test file found for this page specifically.

3. **`config.js` — Medium**
   440 lines, 7 top-level functions. `applyContactIdentity` (~147 lines, lines 280–427) is far past the 80-line guideline and mixes DOM mutation across many different contact-surface elements. Single clear concern (site identity/branding), so risk is moderate rather than critical — this reads more like a long enumeration than tangled logic, but the one function is a legitimate extraction target.

4. **`platform/src/pages/AdminDashboard.jsx` — Medium**
   325 lines, React component with `useState`/`useEffect` and direct `api` calls — fetching, state, and rendering in one component (typical React "page" mixed-concerns pattern). No dedicated test file found.

5. **`scripts/conversion-tracking.js` — Low-Medium**
   390 lines, 52 function-like declarations (mostly small event-tracking callbacks). Single clear concern (analytics instrumentation). Has direct test coverage (`tests/unit/conversion-tracking.test.js`, `tests/unit/conversion-funnel.test.js`). Low priority.

6. **`index.html` — Low**
   561 lines but all 6 `<script>` tags are external references (0 inline script lines) — pure markup, single concern. Not a refactor target.

7. **`styles/style.css`, `docs/*.md` — Low (excluded per guardrail)**
   CSS-only and documentation files are a maintainability/organization concern, not a complexity risk per LOC.md guardrails. Route `style.css` to a design-system pass if it keeps growing; docs are out of scope entirely.

## Refactor Opportunities by Phase

**`api-bookings.mjs`** (High):
- Phase 1: Extract the Stripe payout + invoice logic (`payoutAndInvoice`, `issueInvoice`) into `netlify/functions/utils/booking-billing.js` — smallest safe cut, no behavior change, handlers call into it the same way.
- Phase 2: Extract the booking-lifecycle transition logic (`confirmBooking`/`declineBooking`/`completeBooking` state changes) into a `booking-lifecycle.js` helper, leaving `api-bookings.mjs` as the thin HTTP routing layer.
- Phase 3 (optional): Add a smoke test around `createBooking`/`completeBooking` before extracting, since no test currently guards this path.

**`config.js`** (Medium):
- Phase 1: Split `applyContactIdentity`'s per-surface DOM updates (phone, email, address, social links) into small named helpers it calls, rather than one 147-line body — mechanical extraction, no logic change.

**`pages/client-portal.html`** (Medium-High):
- Phase 1: Move the 238-line inline `<script>` block into `pages/client-portal.js` as an external file, loaded via `<script src>`. Pure relocation — de-risks future logic changes without touching markup.

## Validation Plan (for eventual `--refactor`)
- For `api-bookings.mjs`: add/confirm a test hitting `createBooking` → `confirmBooking` → `completeBooking` end-to-end before extracting; re-run after each phase and diff response shapes.
- For `config.js`: run `tests/unit/*.js` (existing suite) before/after; visually smoke-test a page that uses `applyContactIdentity`-populated fields.
- For `client-portal.html`: confirm the page still loads and the booking flow fires the same network calls after moving the script (browser devtools network tab, no server changes expected).

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| skyview | `api-bookings.mjs`: payment + email + booking-lifecycle concerns mixed in one Netlify function, no test coverage found | High | Touches money (Stripe) — best next-cycle target |

## Ordered Next-Cycle Targets (this repo)
1. `netlify/functions/api-bookings.mjs` — split billing/invoicing from routing, add coverage first (High, high ROI — payment path)
2. `pages/client-portal.html` — extract inline script to external file (Medium-High, low-risk mechanical move)
3. `config.js` — extract `applyContactIdentity` per-surface helpers (Medium)
4. `platform/src/pages/AdminDashboard.jsx` — monitor; typical React page pattern, not urgent (Medium)

## Deferred / Not Flagged
- `styles/style.css` (2014 lines) — CSS-only, deferred to design-system pass per guardrail.
- `docs/*.md` files in the top 10 by raw size — documentation, not source complexity risk.
- `docs/lighthouse-*.report.{json,html}` — excluded entirely as generated audit artifacts, not source.
- `index.html` — large but single-concern markup with only external script references; deferred.

## Assumptions / Unconfirmed
- Churn/author-frequency signal: **assumed unavailable** — shallow clone has no history beyond HEAD.
- Test coverage for `api-bookings.mjs` and `AdminDashboard.jsx`: assumed absent based on filename search only (`grep -rl` across `tests/`), not a coverage-tool run.
