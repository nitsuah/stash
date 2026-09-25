# overseer

> Reviewed: 2026-09-24

## Overview

Meta-repository intelligence layer and GitHub portfolio dashboard at overseer.nitsuah.io. Enforces documentation standards (ROADMAP, TASKS, METRICS, FEATURES), provides AI-powered repo summaries (Gemini/OpenAI/Anthropic failover), one-click PR creation for missing docs, health scoring, an MCP server (7 tools) + LLM context endpoint, PMO mode with a chat-driven doc-edit panel, and an agent task queue with a working dispatch bridge into agent-board. Next.js 16 + Neon Postgres + Netlify Functions + NextAuth GitHub OAuth.

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

None open (updated 2026-09-25). The root `TASKS.md` reads "P0: None open — P0 hardening shipped in #225/#226" and "P1: None open — see CHANGELOG for the #221–#233 work". The one human-gated P1 from 2026-09-24, renaming the GitHub repo `nitsuah/overseer` to `nitsuah/vigil`, is done: the GitHub repo is `nitsuah/vigil`, and the local clone moved to `C:\Users\ajhar\code\vigil` (clean on `main`). The routines still call it `overseer`; see `agent/projects/scope.md`. The `navbar-v2` checkout and the `pr-229-merge-conflicts` worktree flagged on 2026-09-24 went with the old clone.

Still worth tracking (P2, from 2026-09-11): **`session?.user?.email` gates the shared-key AI rate limiter**. A GitHub OAuth profile with no public email skips the budget gate. Re-check it against the current TASKS.md before assuming it's still open.

## Blockers

None hard-blocking.

## Recent Changes (Unreleased)

- **In-progress rebrand: "Overseer" → "Vigil"** — on unmerged branch `feat/vigil-rebrand-and-chat-auth` (commit `c39be6c` "finish overseer -> vigil rebrand", plus two follow-up commits `fdea75b`/`339876d` hardening chat auth/localStorage-key migration). README.md and FEATURES.md already read "Vigil" on this branch; root docs on `main` still say "Overseer". Same branch also makes per-repo chat require authentication and meters it by a stable session identity instead of the email-based gate flagged as an open P2 below — worth re-checking that P2 once this branch merges, it may close it as a side effect. Tracked in open PR #221 ("Require auth for repo chat; finish overseer -> vigil rebrand"); the branch's working copy also has 13 modified/untracked files beyond the 3 pushed commits as of 2026-09-18.
- **Shared-key rate limiter moved to a Neon-backed store** — replaces a process-local `Map` that reset per cold-started serverless instance (each instance effectively got its own budget); now a `shared_key_rate_limits` table with atomic upsert-based fixed-window counting
- **Reserve-before-fallback rate-limit fix (CWE-770)** — a configured-but-failing personal AI key used to fall through to the shared key *after* the spend already happened; the limiter now reserves a slot before the call and only releases it on success, closing the budget-bypass window
- **Agent dispatch bridge shipped** — `motorPoolBridge.dispatch()` creates a session via agent-board's API, delivers the queued task, and writes status/result back onto the task; falls back to simulated execution if the runtime is unreachable (PR #159, hardened PR #204)
- **Portfolio Intelligence batch (PR #204):** chat-driven doc-edit proposals (propose → diff card → apply via existing PR flow), cross-repo dependency graph, token-density + comment-to-code ratio metrics, `docs/db-scaling-assessment.md`, velocity/health-score trending via `repo_snapshots`
- **v2 Launch (PR #200):** sync button force-refreshes all filtered repos (not just new ones), maintenance-mode badge (90+ days no commits), velocity score (0-100)
- Several CodeRabbit-flagged follow-ups from PR #204 (2026-09-09)/PR #211 (2026-09-10/11) have since shipped per `TASKS.md` (2026-09-10): durable agent-task receipts, `reviewThreads`/`refs` GraphQL pagination (plus a PR #216 correctness follow-up), and mobile-card a11y restructuring. The `session?.user?.email` rate-limiter gap (see Open P2s above) remains the most notable one still open.

## Verified Runbook (PMO 2026-09-24)

> Commands verified during the 2026-09-24 PMO audit (`agent/reports/pmo-audit-2026-09-24.md` §7). **obn-review: keep this section when refreshing the summary.**

- GitHub repo is `nitsuah/vigil` (renamed). `docker compose -p vigil-pmo -f config/docker-compose.test.yml run --rm coverage`. METRICS' Verification section leaves out the `config/` prefix.
- The lint-staged prettier hook formats `*.md` on commit.
