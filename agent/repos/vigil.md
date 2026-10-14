---
kind: repo-hub
repo: vigil
aliases: [overseer]
---

# vigil

> Reviewed: 2026-10-10

## Overview

Meta-repository intelligence layer and GitHub portfolio dashboard at overseer.nitsuah.io. Enforces documentation standards (ROADMAP, TASKS, METRICS, FEATURES), provides AI-powered repo summaries (Gemini/OpenAI/Anthropic failover), one-click PR creation for missing docs, health scoring, an MCP server (7 tools) + LLM context endpoint, PMO mode with a chat-driven doc-edit panel, and an agent task queue with a working dispatch bridge into motor-pool (formerly agent-board). Next.js 16 + Neon Postgres + Netlify Functions + NextAuth GitHub OAuth.

## Current Goals / Roadmap Focus

**Q2 2026:** ✅ Completed — AI feature suggestions, inline doc improvement, workflow visualization, real-time webhook sync, PMO mode, DEV-flow handoff, Gemini model evolution resilience, repo-detail query batching.

**Q3 2026 (PMO Mode — mostly done):**
- [x] PMO mode, DEV-flow handoff UI
- [x] Chat-driven TASKS/ROADMAP/FEATURES management — proposal/apply/dismiss flow shipped (chat proposes a diffable edit → inline card → applies via the existing fix-doc PR flow); direct "check off in TASKS.md from chat" (stage 3) still open
- [ ] AI-assisted roadmap management (auto-suggest from health signals, auto-update from PR/issue state) — still open

**Q3 2026 (Analytics & MCP): ✅ effectively complete**
- [x] Conversational interface foundation — per-repo chat panel (PR #196)
- [x] Velocity scoring + trending — `repo_snapshots` time-series, trend endpoint, sparkline; `TASKS.md` (2026-09-10) now marks this item fully shipped, covering the technical-debt-trending acceptance criteria too
- [x] MCP server — 7 tools + `/api/context` LLM endpoint (PR #181)
- [x] Cross-repo dependency mapping — shipped as a 2D SVG graph (`GET /api/dependencies`), not the originally-scoped interactive 3D graph — that upgrade is now a distinct backlog item

**v2 Launch (2026-09-01) + Portfolio Intelligence Batch (2026-09-03):** both shipped (PR #200, PR #204) — force-refresh sync, maintenance-mode detection, chat doc-edit proposals, token-density/comment-to-code metrics, DB scaling assessment doc.

**Q4 2026 (exploratory):** autonomous plan execution, portfolio intelligence dashboard, repo "mood" signal, AI PR pairing suggestions, mobile-responsive PWA, stale-review detector, agent session receipts.

## Open P0/P1 Tasks

_Refreshed 2026-10-10 against the mirrored `TASKS.md` (updated 2026-10-09). No P0. A new P1 epic, "Visual best practices" (moved here from stash SOTU 2026-W41), shipped its first four items on 2026-10-09: `visual_docs` is now scored, plus the `actions_pr_permission` check, an informational `journeys` practice and `visual_setup` in `/api/context`. Open P1s:_

- [ ] **P1** Journeys in vigil beyond detection: read `bot/journeys` metrics and open `bot:journey`/`bot:review` counts onto repo details with a PMO rollup, an owner-only "Run journeys now", an "Enable nightly journeys" scaffold PR, agent-queued review/adopt/fix runs. Then promote `journeys` out of `INFORMATIONAL_PRACTICES`.
- [ ] **P1** Showcase audit: features no journey covers, plus "features linked" on the dashboard (CLI-only today).
- [ ] **P1** Diagrams-only recipe job for repos with no UI (Excalidraw export, no screenshot plumbing).
- [ ] **P1** Showcase rollout: Pages + one `/brag` spot each for vhs, skyview and nitsuah-io (vigil done; ats-fill held). User-run; turn Actions PRs on for vigil, fire and motor-pool first.
- [ ] **P1** Follow-ups outside vigil: stash `sotu.py` reads `visual_setup`; nitsuah/.github adds the Actions PR setting to `/promo`'s first-run checklist.
- [ ] **P1** Tasks card shows the lowest-priority group first and hides the rest (#275, from the journeys review pass; `TasksSection.tsx` sorts then calls `.reverse()`).

P2 from the same review pass: #276, #277, #279; fold the visual-docs screenshots into the journeys. The old P3 "roll the visual-docs recipe out, then score it" is closed by the epic.

Earlier (2026-10-01): PR #260 (merged 2026-10-01) added repo tiers T1–T4 (`repos.tier`, `PATCH /api/repos/[name]/update-tier`, `tier` filter on MCP `list_repos`) and a `skills/vigil/` Claude Code skill. In P2, chat-driven doc editing is now stages 1–4 complete, the relationship-map foundation is checked off, and a new open P2 asks to grow that map from real evidence.

**Resolved (2026-09-28):** `session?.user?.email` gate on the shared-key rate limiter was a bypass — GitHub OAuth profiles with no public email skipped the budget entirely. Fixed by threading `session.userId` (stable GitHub numeric id) as the primary rate-limiter identity with email as fallback. See TASKS.md item "Give every authenticated session a stable rate-limiter identity" ✅.


## Blockers

None hard-blocking.

## Recent Changes (Unreleased)

- **2026-09-25/26 batch:** cross-repo task rollup (`get_open_tasks`, the 8th MCP tool; `open_work` block in `/api/context`; PMO "Open work" panel; TASKS parser captures priority/owner); MCP endpoint made reachable in production (bearer requests no longer redirected to `/login`) and Streamable-HTTP compatible for `claude mcp add --transport http` (new `docs/MCP.md`); informational `visual_docs` best practice + reusable CI recipe (new `docs/VISUAL_DOCS.md`, not yet scored); `session.userId` fixed to the GitHub numeric id (was a per-login UUID, which broke `/api/sync-progress` and repo-access grants); one health-grade scale across dashboard and MCP; header overflow fix; empty-TASKS state.
- **Rebrand "Overseer" → "Vigil" (done):** shipped via PR #221 (merged 2026-09-18; auth-required repo chat, metered by session identity), then the GitHub repo was renamed `nitsuah/overseer` → `nitsuah/vigil` and the local clone moved to `codeigil`.
- **Shared-key rate limiter moved to a Neon-backed store** — replaces a process-local `Map` that reset per cold-started serverless instance (each instance effectively got its own budget); now a `shared_key_rate_limits` table with atomic upsert-based fixed-window counting
- **Reserve-before-fallback rate-limit fix (CWE-770)** — a configured-but-failing personal AI key used to fall through to the shared key *after* the spend already happened; the limiter now reserves a slot before the call and only releases it on success, closing the budget-bypass window
- **Agent dispatch bridge shipped** — `motorPoolBridge.dispatch()` creates a session via motor-pool's API, delivers the queued task, and writes status/result back onto the task; falls back to simulated execution if the runtime is unreachable (PR #159, hardened PR #204)
- **Portfolio Intelligence batch (PR #204):** chat-driven doc-edit proposals (propose → diff card → apply via existing PR flow), cross-repo dependency graph, token-density + comment-to-code ratio metrics, `docs/db-scaling-assessment.md`, velocity/health-score trending via `repo_snapshots`
- **v2 Launch (PR #200):** sync button force-refreshes all filtered repos (not just new ones), maintenance-mode badge (90+ days no commits), velocity score (0-100)
- Several CodeRabbit-flagged follow-ups from PR #204 (2026-09-09)/PR #211 (2026-09-10/11) have since shipped per `TASKS.md` (2026-09-10): durable agent-task receipts, `reviewThreads`/`refs` GraphQL pagination (plus a PR #216 correctness follow-up), and mobile-card a11y restructuring. The `session?.user?.email` rate-limiter gap was the most notable remaining one and shipped in PR #254 (2026-09-28) — see Resolved above.

## Verified Runbook (PMO 2026-09-24)

> Commands verified during the 2026-09-24 PMO audit (`agent/reports/pmo-audit-2026-09-24.md` §7). **obn-review: keep this section when refreshing the summary.**

- GitHub repo is `nitsuah/vigil` (renamed). `docker compose -p vigil-pmo -f config/docker-compose.test.yml run --rm coverage`. METRICS' Verification section leaves out the `config/` prefix.
- The lint-staged prettier hook formats `*.md` on commit.

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/vigil/README|README]] (every doc hangs off its Docs Index)
- Overview: [[projects/KB/overseer-overview|KB overview]]
- Latest LOC report: [[reports/eng-loc-overseer-2026-07-29|2026-07-29]] (older ones chain from it)
- Latest MINI report: [[reports/eng-mini-vigil-2026-10-02|2026-10-02]] (older ones chain from it)
<!-- vault-links:end -->
