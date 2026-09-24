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

**Update 2026-09-24** (from `docs/TASKS.md` dated 2026-09-19, synced from the local `navbar-v2` checkout; PR #229 "docs/ folder support" merged to main 2026-09-23):
- All 5 **P0s** are done: repo-row expand crash from NUMERIC-as-string (PR #225), `RowErrorBoundary`, NUMERIC normalization at the API boundary (`lib/numeric.ts`), repo-list/by-name route access scoping (CWE-639, follow-up to PR #221, which also found `debug` had no auth), and `visibility_verified` backfill that fails closed. **After deploy each user must click Sync once** or their own private repos stay hidden.
- **One open P1 needs a human:** rename GitHub repo `nitsuah/overseer` to `nitsuah/vigil`. The code is ready, but the order matters: merge and deploy first, then `gh repo rename`, `git remote set-url`, Sync, and check smoke. Renaming before deploy creates a duplicate row.
- Other P1s done: keep `ghoverseer.netlify.app` (decision), the Playwright mocked e2e suite in CI, the post-merge prod smoke workflow, and the dispatch bridge (PR #159/#204).

Previous status (2026-09-10): no open P1 items. The one P1 (Agent Task Queue → agent-board dispatch bridge) shipped in PR #159 and was hardened in PR #204.

Note: the previously-tracked P1 "deprioritize stash repo (mark private, block PRs, add sanitization checklist)" is **no longer present** in the current root `TASKS.md`/`ROADMAP.md` — it has no corresponding "shipped" entry in `FEATURES.md` or `CHANGELOG.md` either, so its status is ambiguous (dropped vs. quietly resolved out-of-band). A stale copy of it still exists in `docs/TASKS.md`/`docs/ROADMAP.md` (both dated 2026-06-25, clearly unmaintained duplicates of the root files) — worth a manual check on whether stash was actually deprioritized/privated, since this repo's own doc-hygiene tracking has lost the thread on it.

Most-notable open P2 (flagged 2026-09-11, today, by CodeRabbit on PR #211): **`session?.user?.email` gates the entire shared-key AI rate limiter** — a GitHub OAuth profile with no public/verified email skips the gate entirely, letting that request reach `generateAIContent` with no budget enforcement at all. Confirmed pre-existing (predates PR #211). Needs a stable non-email session identity wired up before it's closed.

Since the last review, three of those open P2s shipped per `TASKS.md` (2026-09-10): **durably persist agent task receipts** (await + surface-failure path, `persistReceipt` now awaited instead of fire-and-forget, 3 new tests), **paginate `reviewThreads`/`refs` GraphQL connections** (both `getZombieBranches` and `getPullRequestReadiness` now page to a documented cap, plus a CodeRabbit-flagged follow-up fix on PR #216 so an incomplete page-walk fails closed instead of false-reporting `staleReview: true`), and **mobile card a11y** (the `role="button"` wrapper around nested focusable links is gone — expand/collapse is now a real sibling `<button>`). Velocity scoring + trending (`repo_snapshots`, trend endpoint, sparkline) also shipped, covering most of what "technical-debt trending" meant.

Other open P2s: stale-review detector for PR readiness (CodeRabbit misses re-approving after all threads resolve), thread `full_name` (not just `name`) through to the trend endpoint, 3D dependency-graph upgrade (current graph is 2D SVG).

Open P3s: zombie-branch detection, dark/light mode toggle, agent session receipts.

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
