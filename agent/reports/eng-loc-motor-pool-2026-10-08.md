---
kind: eng-loc
repo: motor-pool
date: 2026-10-08
---

# LOC Report — motor-pool

> 🧭 [[repos/motor-pool|motor-pool]] <!-- nav -->

HEAD: 42cb1f47749b054551b50d2cd833680ac3f07ce0


Mode: `--report` (dry run, no changes made)
Date: 2026-10-08
Source: shallow clone (`--depth 1`) of `nitsuah/motor-pool` @ `42cb1f47749b054551b50d2cd833680ac3f07ce0`
Method: `git ls-files` (Phase 0 exclusions, **now including `*.md`/`*.mdx` — docs are out of scope per updated LOC.md**) + per-file line counts. Shallow clone has no history beyond HEAD, so churn is **assumed unavailable**.

Canaries: 0/0 (no canary file tracked in this repo)

## ⚠️ Resolved since last report (2026-07-29)
The last report flagged `tools/opencut/...` and `tools/content-gen/modules/MoneyPrinterTurbo/...` as the top 8 hotspots (1,819 down to 1,039 LOC: `countries-data.ts`, `voice.py`, `Main.py`, `keyframes.ts`, `timeline-element.tsx`, `video.py`, `llm.py`, `projects/page.tsx`). **All of these no longer exist** — the `tools/opencut` subtree and the `MoneyPrinterTurbo` module have been removed from the repo entirely. This isn't a refactor to verify, it's a deletion; no action needed, but note it so nobody goes looking for files that are gone.

## Inventory Summary
- Tracked source files (post-exclusion, docs excluded): 208
- Remaining `tools/` subtrees: `content-gen` (minus MoneyPrinterTurbo), `llm-openllm`, `website` — all much smaller now.

## Top LOC Files (all tracked files, unfiltered by type, docs excluded)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `dashboard/src/App.css` | 4,408 | CSS | Dashboard stylesheet |
| 2 | `dashboard/src/components/LiminalDashboard.jsx` | 883 | JSX | 3D service-graph visualization |
| 3 | `dashboard/server.js` | 742 | JS | Dashboard backend bootstrap |
| 4 | `dashboard/src/App.jsx` | 698 | JSX | Dashboard root component |
| 5 | `dashboard/routes/docker.js` | 636 | JS | Docker control route handlers |
| 6 | `dashboard/src/components/WorkspaceView.jsx` | 625 | JSX | Workspace panel view |
| 7 | `config/docker-compose.yml` | 535 | YAML | Compose config |
| 8 | `dashboard/modules/agent-tools.js` | 497 | JS | Agent tool registry |
| 9 | `dashboard/routes/sessions.js` | 488 | JS | Session route handlers |
| 10 | `dashboard/routes/worktrees.js` | 444 | JS | Worktree route handlers |

## Risk Rank & Rationale

1. **`dashboard/src/App.jsx` — High**
   698 lines, but it's **one function**: `function App() {` (line 22) runs to the file's end (line 698) — a single ~676-line component. This is the same shape as nitsuah-io's `crypto/page.tsx` flagged in the last cycle's cross-repo run: one giant component mixing state, effects, and rendering. Needs a structural read to confirm sub-sections, but the single-function signal alone clears the ~80-line threshold by 8x.

2. **`dashboard/src/components/LiminalDashboard.jsx` — Medium-High**
   883 lines. Confirmed mixed concerns: color/geometry helpers (`hexNumToRgbStr`, `goldenPos`, `radialPlacement`), graph construction (`buildGraph`, ~175 lines), a physics simulation step (`physicsStep`, ~60 lines), and the `LiminalDashboard` component itself (line 369 onward, ~514 lines) all in one file. At minimum 3 distinct concerns (data/graph building, physics, rendering) that don't need to live together.

3. **`dashboard/server.js` — Medium**
   742 lines, 28 top-level functions covering at least 4 unrelated concerns: task-state helpers (`normalizeTaskStatus`, `buildTaskSummary`), service health checks (`checkHttpService`, `checkTcpService`), Docker Compose control (`runComposeAction`), and Ollama/LLM endpoint resolution (`ensureRunnableModelForSession`, `resolveEndpointUrl`). Only 6 Express routes are defined inline — most of the file's bulk is these helper concerns, which is itself the signal (a "bootstrap" file growing a second job as a service-health/LLM-orchestration module).

4. **`dashboard/src/App.css` — Low**
   CSS-only, per Evidence Rules a style/maintainability smell not a complexity risk.

5. **`dashboard/routes/docker.js`, `routes/sessions.js`, `routes/worktrees.js` — Low (not read in depth)**
   Already split by concern (one route file per domain) — the architecture here is sound; not flagged without evidence of internal mixed concerns.

## Refactor Opportunities by Phase

**`dashboard/src/App.jsx`**:
- Phase 1: extract state/data-fetching logic into one or more custom hooks (e.g. `useDashboardState()`), following the pattern already used elsewhere in this codebase (`useWorkspaceOps.js` exists as a hook, suggesting this is the established convention — `App.jsx` just hasn't been split the same way).
- Phase 2: split the JSX tree into section components (nav/header, main panels, modals) once the state extraction makes the boundaries visible.

**`dashboard/src/components/LiminalDashboard.jsx`**:
- Phase 1: extract `buildGraph` and its geometry helpers (`hexNumToRgbStr`, `goldenPos`, `radialPlacement`, `findProviderServiceNode`) into `graph-builder.js`.
- Phase 2: extract `physicsStep` into `physics.js`.
- Phase 3: leave `LiminalDashboard` as the render-only component, importing graph/physics as pure functions.

**`dashboard/server.js`**:
- Phase 1: extract Ollama/LLM resolution functions (`resolveEndpointUrl`, `ensureRunnableModelForSession`, `prepareSessionForLlmCall`, `getOllamaModelNames`, `chooseRunnableOllamaModel`) into `modules/llm-resolution.js`.
- Phase 2: extract service-health checks (`checkHttpService`, `checkTcpService`, `runComposeAction`) into `modules/service-health.js` (there's already a `routes/docker.js` — check whether `runComposeAction` belongs there instead of a new module).
- Phase 3: extract task-state helpers into `modules/task-state.js`.

## Validation Plan (for eventual `--refactor`)
- `config/docker-compose.yml` exists at repo root — use it to run the dashboard stack for smoke testing per LOC.md Phase 3 guidance.
- `dashboard/tests/` has existing suites (`e2e-agents.js`, `e2e-services.js`, `worktrees-api.js`, `safety-layer.js`, `plugins-api.js`) — run these after each extraction phase.
- No dedicated test found for `App.jsx` or `LiminalDashboard.jsx` specifically — flag both as needing a smoke test (render without crash) before extraction, and flag `App.jsx` as a UX surface needing manual QC (it's the dashboard's root view).

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| motor-pool | `dashboard/src/App.jsx` (single ~676-line component) | High | Previous top hotspots (`tools/opencut`, MoneyPrinterTurbo) were deleted, not refactored — fully resolved |

## Ordered Next-Cycle Targets (this repo)
1. `dashboard/src/App.jsx` — split into hook + section components (High)
2. `dashboard/src/components/LiminalDashboard.jsx` — extract graph-builder + physics modules (Medium-High)
3. `dashboard/server.js` — extract LLM/service-health/task-state modules (Medium)

## Deferred / Not Flagged
- `dashboard/src/App.css` — CSS-only.
- `config/docker-compose.yml` — config, not logic.
- `dashboard/routes/*.js` — already split by domain, no evidence of internal mixed concerns this pass.

## Assumptions / Unconfirmed
- Churn/author-frequency signals for all files: **assumed unavailable** — shallow clone has no history beyond HEAD.
- Internal structure of `App.jsx`'s ~676-line body (what the sub-sections actually are) — not read line-by-line this cycle; recommend a closer read before committing to a phase plan.
