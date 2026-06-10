# Productization & Tiering

**Last Updated:** 2026-06-10

**Purpose:** Tracks promotion-readiness and monetization/portfolio value across all repos, and drives an overall **Tier** assignment per repo. Use this doc to pick the next batch of work each cycle — repos move between tiers as blockers clear or priorities shift.

---

## How to use this doc

1. At the start of a cycle, scan the Tier table below.
2. Pull picks primarily from **Tier 1** (promote now) and **Tier 2** (build toward promotion).
3. **Tier 3** gets occasional maintenance passes only — don't let it crowd out Tier 1/2.
4. **Tier 4** is held — only revisit if its trigger condition fires.
5. After a cycle, update "Next Action" per repo, re-tier if status changed, and log picks in the Rotation Log at the bottom.

---

## Tier Definitions

| Tier | Meaning | Criteria |
| --- | --- | --- |
| **1 — Promote Now** | Live, working, demoable. Actively push content/visibility this cycle. | Live URL or shipped artifact, no P0 blockers, clear audience/use case |
| **2 — Build Toward Promotion** | Strong potential, but needs dev work before a promo push pays off. | Functional but has P0/P1 blockers, UX gaps, or missing "story" |
| **3 — Maintain / Portfolio** | Stable, low-touch. Good portfolio evidence, not an active growth lever. | Working, low blocker count, niche/personal-use audience |
| **4 — Hold / Archive** | Paused by explicit call or a blocker that needs a pivot decision. | User has deprioritized, archived, or blocker requires rethinking scope |

---

## Tier Assignments

### Tier 1 — Promote Now

| Repo | Why Tier 1 | Channel | Blocker | Next Action |
| --- | --- | --- | --- | --- |
| **nitsuah-io** | Live portfolio hub — the "storefront" for everything else. Q2 ask: redesign home as a project-card landing page surfacing Tier 1/2 work. | Personal site (live) | P0: `Dockerfile.test` Playwright image pin `v1.56.1-noble` → `v1.57.0-noble` | Fix the Playwright pin (1 line), then resume the home-landing-redesign HANDOFF (card grid for agent-board/overseer/darkmoon/etc.) |
| **overseer** | Live free tool, 71.5% test coverage, real "paydirt" potential per Q2 notes. Closest thing to an actual product with a growth loop. | Live site (ghoverseer.netlify.app) | P1: `docs/AUDIT.md` stale (3.5mo) | Refresh AUDIT.md, continue the BYOK quota-fallback HANDOFF, scope the "simple mode" UX |
| **agent-board** | Local AI agent dashboard — directly demonstrates the "Claude Skills" story the user wants to promote. Demo video scripts + SRT captions already drafted. | Demo video / portfolio, npm/Docker | Stability/memory issues under Docker (Q2 feedback) | Stabilize default config (lighter footprint, FS read/write, MCP container manager) before pushing promo content |
| **darkmoon** | Live multiplayer 3D game, CI green, demoable — strong visual content. | Live (darkmoon.dev) | UI/UX polish (21st dev components), player-tag bugs | Use the `opencut` skill to capture a gameplay clip; fix player-tag bugs; scope laser-tag mode |

### Tier 2 — Build Toward Promotion

| Repo | Why Tier 2 | Channel | Blocker | Next Action |
| --- | --- | --- | --- | --- |
| **opencut-controller** | Already shipped as an npm package — 161-tool MCP server. A concrete "I built this" artifact, and the `opencut` Claude Skill maps directly to it. | npm package | None major | Use `content-gen` for a short "what is this and why" write-up; cross-link from nitsuah-io |
| **skyview** | Static site + client portal, Docker-validated, launch-ready. Real revenue potential via Builder-agent client work. | Client product (Netlify) | Launch checklist incomplete (domain/metadata/search console); METRICS has conflicting values | Close the launch checklist; reconcile METRICS into one dated source of truth |
| **fire** | Complete client-side FIRE calculator — easy personal-finance promo angle once cleaned up. | Standalone tool / niche content | Absolute path links in ROADMAP.md; CSV PII audit unresolved | Fix links, finish PII audit, then promote as a free tool |
| **auto-apply-plugin** | Chrome extension, 63 tests passing — real automation tied to the "Setup Odysseus" career theme. Could go public via Chrome Web Store. | Chrome Web Store (potential) | No store listing yet | Scope a Chrome Web Store submission as a follow-on milestone |

### Tier 3 — Maintain / Portfolio

| Repo | Why Tier 3 | Notes |
| --- | --- | --- |
| **games** | Production-ready (Phase 10+), 218 tests, live on Netlify. Already polished. | Good promo b-roll; review 21st dev component upgrades opportunistically |
| **farm-3j** | v0.dev auto-synced, decent docs. Q2 wants real photos + a simplified RTS-lite refactor. | Portfolio value, but v0.dev sync friction keeps it lower priority |
| **kryptos** | Novel K4 cryptanalysis research platform — strong "interesting" story, niche audience. P0 permission error on runtime. | Fix the P0 (quick), then a content angle: "using AI to attack Kryptos K4" |
| **avatar** | Docker passes, 25 tests, but depends on external Colab — limits standalone promo. | Personal-use tool; maintain only |
| **vhs** | Simple personal VHS collection indexer, complete-ish. | Low priority; occasional use |
| **bb-mcp** | 50% complete, originally scoped against a specific job posting (Anthology). | Re-tier to 1 only if actively pursuing that role again — check [[projects/Career]] first |

### Tier 4 — Hold / Archive

| Repo | Why Tier 4 | Revisit Trigger |
| --- | --- | --- |
| **gcp** | User: "I don't care about this repo as much." Also has a P0 Docker blocker. | Only if a Tier 1/2 repo develops a hard GCP dependency |
| **osrs** | User: "I care less about this repo." P0 blocker (missing `main.py`); Q2 notes lean toward a generalized automation framework instead. | Revisit only when/if scoping that new generalized-automation repo |
| **opencut** | Explicitly archived — superseded by opencut-controller. | None — reference only |
| **nitsuah (v1)** | Archived — superseded by nitsuah-io. | None — reference only |

---

## Claude Skills → Promotion Map

| Skill | Best fit | Use for |
| --- | --- | --- |
| `opencut` (→ opencut-controller MCP) | darkmoon, agent-board, games | Capture/edit gameplay & demo clips |
| `content-gen` | overseer, opencut-controller, agent-board | Write-ups on shipped features |
| `site-gen` | nitsuah-io | Landing page / card-grid scaffolding for the redesign |
| `marketing:content-creation`, `marketing:campaign-plan` | overseer, fire | Launch announcements, ongoing content cadence |
| `marketing:seo-audit`, `marketing:performance-report` | skyview, nitsuah-io | Pre-launch SEO/perf pass |
| `marketing:competitive-brief`, `marketing:brand-review` | skyview (client work) | Client deliverables for Builder-agent engagements |
| `small-business:canva-creator`, `pptx`/`xlsx` | skyview, fire | Client-facing assets, social graphics |
| `marketing:email-sequence` | overseer | Onboarding/drip sequence if user growth becomes a focus |

---

## This Week (2026-06-10)

1. **nitsuah-io** — fix the one-line Playwright Docker pin (P0), then resume the home-landing-redesign HANDOFF to surface Tier 1/2 project cards. Highest leverage: every other promotion effort benefits from a working storefront.
2. **overseer** — refresh the stale `docs/AUDIT.md` (P1, 3.5mo old) and continue the in-progress BYOK quota-fallback HANDOFF.
3. **agent-board** — use the existing demo video scripts/SRT captions with the `opencut` skill to produce a first promo clip; in parallel, scope the Docker stability fixes (lighter default config, FS access, MCP container manager) flagged in Q2 feedback.
4. **fire** — quick cleanup: fix absolute path links in ROADMAP.md, finish the CSV PII audit. Low effort, unblocks Tier 2 promotion.

---

## Rotation Log

| Cycle | Picks | Outcome |
| --- | --- | --- |
| 2026-06-10 | nitsuah-io (P0 fix + redesign), overseer (AUDIT refresh + BYOK), agent-board (demo + stability), fire (cleanup) | _pending_ |

---

## Related

- [[docs/2026Q2|2026Q2]] — source of per-repo CEO feedback driving these tiers
- [[docs/GAPS_AND_IMPROVEMENT_PLAN|Gaps & Improvement Plan]] — repo audit / monetization assessment process this doc formalizes
- [[docs/MONEY-MAKERS|Money Makers]] — monetization themes (social pipeline, Setup Odysseus)
- [[docs/ENHANCEMENT_ROADMAP|Enhancement Roadmap]] — stash's own roadmap (this repo isn't tiered above; it's the tooling that runs the process)
- [[projects/Career|Career]] — check before re-tiering bb-mcp
