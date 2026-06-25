# overseer

> Reviewed: 2026-06-25

## Overview

Meta-repository intelligence layer and GitHub portfolio dashboard at overseer.nitsuah.io. Enforces documentation standards (ROADMAP, TASKS, METRICS, FEATURES), provides AI-powered repo summaries (Gemini/OpenAI/Anthropic failover), one-click PR creation for missing docs, health scoring, and agent task queue API. Next.js 16 + Neon Postgres + Netlify Functions + NextAuth GitHub OAuth.

## Current Goals / Roadmap Focus

**Q2 2026:** ✅ Completed — AI feature suggestions, inline doc improvement, workflow visualization, real-time webhook sync, PMO mode, DEV-flow handoff, Gemini model evolution resilience, repo-detail query batching

**Q3 2026 (PMO Mode — partially done):**
- [x] PMO mode: portfolio-wide roadmap progress, plan execution status, handoff management
- [x] DEV-flow handoff UI: promote roadmap items into agent task queue
- [ ] AI-assisted roadmap management (auto-suggest from health signals, auto-update from PR/issue state)
- [ ] Chat-driven TASKS/ROADMAP/FEATURES management interface

**Q3 2026 (Analytics & MCP):**
- [ ] Conversational interface foundation (one or two repo-hygiene workflows end-to-end)
- [ ] Advanced analytics: velocity scoring, technical-debt trending, zombie-branch detection
- [ ] Expose overseer repo intelligence as MCP server (`get_repo_health`, `list_tasks`)
- [ ] Cross-repo dependency mapping (interactive 3D graph)

**Q4 2026 (exploratory):**
- Autonomous plan execution (agents read ROADMAP/TASKS, open PRs, close items)
- Portfolio intelligence dashboard (cross-repo health roll-up, trend lines)
- Repo "mood" signal (sentiment from PR descriptions, commit messages, TASKS tone)
- AI PR pairing suggestions (surface co-landing items across repos before merge)
- Mobile-responsive + lightweight PWA

## Open P0/P1 Tasks

- [ ] **P1** Deprioritize stash repo: mark private, block PRs, add sanitization checklist
- [ ] **P2** Connect overseer Agent Task Queue → agent-board local model runtime (dispatch bridge v0)
- [ ] **P2** Conversational interface foundation (messenger-style chat, 1-2 hygiene workflows)
- [ ] **P2** Cross-repo dependency mapping (3D interactive graph)
- [ ] **P2** Expose overseer as MCP server
- [ ] **P2** DB scalability assessment (indexing, query patterns at 100+ repos, connection pooling)
- [ ] **P3** Zombie-branch detection + bulk-action delete dialog
- [ ] **P3** Maintenance-mode detection (inactive repo auto-classification)
- [ ] **P3** Token-density and comment-to-code ratio metrics
- [ ] **P3** Dark/light mode toggle
- [ ] **P3** Velocity scoring and technical-debt trending

## Blockers

None hard-blocking. stash repo decommission is a P1 housekeeping item with no dependencies.

## Recent Changes (Unreleased)

- **Roadmap-to-DEV-flow handoff linkage:** `PATCH /api/repos/[name]/roadmap-items/[id]` links roadmap items to PR/agent task; `lib/sync.ts` merges (not delete+insert) `roadmap_items` so DB-only links survive re-syncs
- **Centralized Gemini Model Discovery:** `gemini-model-discovery.ts` — single source of truth, auto-fallback across model versions, 1-hour cache, unified `GEMINI_MODEL_NAME` env var
- **Repo-detail query batching:** 7 sequential round trips → single `db.transaction()` call (~7× latency reduction)
- Default model updated: `models/gemini-2.0-flash-exp` → `models/gemini-2.5-flash`
