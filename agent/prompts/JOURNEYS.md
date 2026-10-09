# JOURNEYS

The low-inference "AI user" loop: nightly Playwright journeys that use each product like a person would, with no AI at run time. Failures become deduplicated `bot:journey` issues, the next nights verify the fixes, and monthly metrics feed [[RSI]]. Think OSRS essence-mining bots: deterministic, repeatable, near-zero tokens.

- **Contract and code:** [nitsuah/.github `journeys/`](https://github.com/nitsuah/.github/tree/main/journeys). Start with `STANDARD.md`. The reusable workflow is `nitsuah/.github/.github/workflows/journeys.yml@main`.
- **This file:** the inventory, the rollout order, the three prompts where AI is used, and the run and metrics logs.
- **Pilot:** fire (2026-10-08/09). Its `tests/journeys/` is the reference implementation.

AI runs only at three points, and each one runs once:

| Point | Prompt | Output |
|---|---|---|
| Adopting a repo | [A. Review pass](#a-one-time-review-pass) | `bot:review` issues, grouped by `area:` |
| Adopting a repo, or a feature ships | [B. Write journeys](#b-write-journeys) | `tests/journeys/*.spec.js` + baselines |
| A `bot:journey` issue opens | [C. Fix](#c-fix-a-botjourney-issue) ([[1FLOW]] Phase 1) | a fix PR with `Refs #N` |

Everything else is code: the nightly run, visual diffs, issue filing, dedup, reopen, auto-close, BUGS.md, and metrics.

## Inventory (2026-10-08)

What already drives each web repo, which this loop reuses rather than duplicates. `spots` = `promo/spots.json` (feature ids for `@feature:` tags).

| Repo | Playwright today | Promo / showcase | Nightly | Journeys status |
|---|---|---|---|---|
| fire | `config/playwright.config.js`, `tests/e2e-ui` (4 specs) + supertest `tests/e2e` | spots, `promo/build.sh`, demo seed | — | ✅ **pilot**: 7 journeys, 19 baselines, coverage 23/92 (before /promo culling) |
| vigil | `playwright.config.ts`, `e2e/`, `visual-docs.yml` | spots, showcase CLI | `e2e.yml`, `smoke.yml` | adopted in vigil#282: 6 journeys, `maxDiffPixels: 20` |
| ats-fill | `config/playwright.config.mjs`, `tests/e2e` | spots, `feature-video.yml` | `playwright-nightly.yml` (artifacts only) | replace the nightly with the journeys caller |
| nitsuah-io | `config/playwright.config.ts`, `tests/e2e` | spots | `playwright-nightly.yml` (artifacts only) | replace the nightly. Nitsuah-Labs org: confirm Actions can call a nitsuah/ reusable workflow (public, so it should). |
| skyview | `config/playwright.config.ts` | spots | `playwright.yml` | after nitsuah-io |
| vhs | `playwright.config.js` | — | — | needs spots.json first (`/promo audit`) |
| darkmoon | `playwright.config.ts`, `e2e/` | — | — | needs spots.json |
| games | `app/playwright.config.js` | — | — | needs spots.json |
| motor-pool (`code/agent-board`) | — | spots | — | needs Playwright + a demo seed |
| stash | — | spots, Pages | — | Pages-only: `@area:site` journeys against the built site |
| farm-3j, kryptos, osrs, avatar | — / `tests/e2e` (kryptos) | — | — | later; check for a UI first |
| bb-mcp, gcp, deployer, windirstat-mcp, 9router | no browser UI | — | — | out of scope (MCP/CLI: use their smoke tests) |

Rollout order: **fire → vigil → ats-fill → nitsuah-io → skyview**, then the rest as spots.json lands. One repo per PR, tracked in stash `docs/TASKS.md` § Journeys rollout.

## A. One-time review pass

> Use the product the way a new user would, in the repo's Docker setup with its **fictional demo seed** (never real data). Cover every tab or page at 1440×900 and 390×844. Also review the GitHub Pages site and the promo/brag materials (spots.json spots, posters, share copy). Collect console errors, 4xx/5xx responses, horizontal overflow, clipped text, numbers that disagree between screens, wrong advice, dead links, and real personal data in demo material.
> Before filing, confirm each finding: read the code for a cause (cite `file:line`) or reproduce it twice. Skip anything that only happens in an embedded/preview browser.
> File **one issue per distinct defect** with labels `bot:review`, `bug`, `area:<app|site|promo|docs>`, title `[area/path] symptom`, and a body with what you saw, where, the cause if known, and a fix sketch. Link existing TASKS items instead of duplicating them.
> A scripted pass is cheaper than clicking through screenshots in the browser pane: one Playwright script that visits every tab at both widths, logs errors and overflow, and saves screenshots. fire's is in the 2026-10-08 run log below.

## B. Write journeys

> Read STANDARD.md § Writing a journey. Turn each confirmed happy path from FEATURES.md into one journey (2–4 `step()`s, user-voiced names, `@feature:<spots id>` tags, real seeded numbers in assertions). Put the repo fixture in `tests/journeys/<repo>.js`: seed, mocks, frozen clock, canvas-animation off, `networkidle`, and teardown settle. Generate baselines in the Playwright Docker image, then soak with `CI=true --retries 0 --repeat-each 3`, three runs, zero failures, before opening the PR. Same PR: caller workflow, `test:journeys` script, README/CHANGELOG/TASKS/FEATURES lines.

## C. Fix a `bot:journey` issue

Covered by [[1FLOW]] Phase 1: claim by self-assigning, reproduce with the issue's Docker command, fix, update baselines if the UI changed, and open the PR with `Refs #N`. The nightly closes the issue after 3 green runs. Never close a `bot:journey` issue by hand unless its journey was deleted.

## Rules settled so far

- **Canvas charts need their animation turned off**, not just CSS. Playwright's `animations: 'disabled'` doesn't reach Chart.js. fire flaked about 1 run in 20 on the allocation donut until an init script set `Chart.defaults.animation = false` (then 70/70 green).
- **Wait for `networkidle` after load, and let debounced saves settle in teardown.** Otherwise one journey's late save lands after the next journey reseeds.
- **`has:` is scoped inside the outer locator.** Use `hasText` for "the card that contains X".
- **A seed written through the app's API may be filtered.** fire's `POST /api/state` drops server-owned `netWorthHistory` (fire#174). Check that the seed you think you loaded is what renders.
- **Use `maxDiffPixels: 1000`, not a ratio.** A 1% ratio (~13k px) let fire's renamed demo wallet (6,029 px) through. Exact zero failed on ~650 px of canvas emoji noise. Measure the noise with `--repeat-each` first.
- **Canvas text is drawn once.** Labels drawn before web fonts load keep the fallback font. Wait for `document.fonts.ready`, then `chart.update('none')`, after load and after each tab switch.
- **Journeys are the screenshot CI too.** `step(..., { docs: '<feature id>' })` + `npm run capture:screenshots` writes `docs/screenshots/<id>.png`; a `visual-docs.yml` PRs them. Don't build a second screenshot suite.
- **Known bugs live in baselines until fixed.** The fix PR updates them, and the PNG diff in that PR is the before/after.

## Run log

### 2026-10-08/09 · fire · pilot (review pass + journeys)

- Harness: nitsuah/.github#19 (reporter, metrics, reusable workflow, STANDARD, templates; 10 unit tests). Reporter dry-run in file mode against nitsuah/fire: correct.
- Review pass: scripted Playwright tour (7 tabs × 2 widths, console, network, overflow) + live Pages check (links, media, 375px). Filed fire#166–#175 (8 app, 2 promo). Highlights: Insights' equity % counts crypto (74% vs 72.6%, `dashboard.js:646`); single-stock warning fires on VTI; the promo seed's 365-day history is silently dropped; the demo seed shows `vitalik.eth`. The Pages site was clean.
- Journeys: 7 (first visit, holdings, projections, side hustle, budget, insights, phone), 19 step baselines, coverage 23/92 (spots.json not yet culled). Soak: 70/70 after the Chart.js fix.
- Cost: one session. The steady-state loop costs 0 tokens per night.

### 2026-10-09 · vigil · review + adopt (nitsuah/vigil#282)

- Ran: scripted tour (dashboard, details, chat, PMO, signed-out, login, 404 × 1440/390) on the visual-docs mocks + Pages site + live app. Filed vigil#275–#279 and #281 (`bot:review`; #278 and #281 fixed in the PR). 6 journeys, 12 baselines, soak 54/54 ×2, sensitivity proven (one letter = 66 px fails).
- Found: the Tasks card's sort ends in `.reverse()` and shows P3 while hiding P2 (#275, P1); the details prefetch is cancelled for good when `repos` changes inside ~240 ms (#281, found by the soak, not the tour); the trend mock never matched after #253 added `?fullName=` (#278).
- Friction: `networkidle` resolves at once after the first idle, so baselines flipped with the prefetch; a 1000 px tolerance let a one-letter change through on a DOM-only app; exact-name locators break when a sort arrow joins the button name. Each soak pass takes ~1.2 min in Docker on Windows.
- Promote: nitsuah/.github#21 (tolerance from measured noise, canvas ~1000 / DOM ~20; `settle()` counts in-flight `/api/` requests). A soak that flips between runs is worth reading as a product race before you widen a timeout.

## Metrics log

Appended monthly by [[RSI]] (`journeys/metrics.mjs`). The first row lands 2026-11-02 for October.
