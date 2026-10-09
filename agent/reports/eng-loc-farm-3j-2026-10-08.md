---
kind: eng-loc
repo: farm-3j
date: 2026-10-08
---

# LOC Report — farm-3j

> 🧭 [[repos/farm-3j|farm-3j]] · ← [[reports/eng-loc-farm-3j-2026-07-29|2026-07-29]] <!-- nav -->

HEAD: 7d508d2fdc9f34608980aaca8c39a622fcf1e4d9


Mode: `--report` (dry run, no changes made)
Date: 2026-10-08
Source: shallow clone (`--depth 1`) of `nitsuah/farm-3j` @ `7d508d2fdc9f34608980aaca8c39a622fcf1e4d9`
Method: `git ls-files` (Phase 0 exclusions, **now including `*.md`/`*.mdx`**; also excluded `pnpm-lock.yaml`, missed by the generic lockfile filter last cycle) + per-file line counts. Shallow clone has no history beyond HEAD, so churn is **assumed unavailable**.

Canaries: 0/0 (no canary file tracked in this repo)

## ⚠️ This is the one that needs immediate attention
The last report's #1 finding, `components/rts/hooks/useGameLoop.tsx`, **was** split — it's down from 5,369 lines to **72 lines**, now just `export function useGameLoop(ctx) { ... }` delegating out. That part worked.

But the complexity didn't go away — it moved. The new #1 hotspot, `components/rts/hooks/ai/tickWorkers.ts` at **3,061 lines, is a single function** (`export function tickWorkers(...)` at line 72, running to EOF — nothing else is top-level in the file). A 3,000-line function is a more concentrated risk than the old 5,369-line *file* was, because there's no file boundary left to split along — the whole thing is one call frame. This is the file to prioritize for `--refactor`, not a nice-to-have.

## Inventory Summary
- Tracked source files (post-exclusion, docs + `pnpm-lock.yaml` excluded): 185

## Top LOC Files (all tracked files, unfiltered by type, docs excluded)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `components/rts/hooks/ai/tickWorkers.ts` | 3,061 | TS | Worker-AI tick logic — **one function** |
| 2 | `components/rts/hooks/useRTSHandlers.tsx` | 1,970 | TSX | Input/UI handler hook — **one hook function, ~1,755 lines** |
| 3 | `components/rts/RTSMap.tsx` | 1,321 | TSX | Map rendering — **one component** |
| 4 | `components/rts/map/BuildingsLayer.tsx` | 1,200 | TSX | Building-layer rendering — **one component** |
| 5 | `components/rts/RTSUI.tsx` | 1,171 | TSX | HUD/UI overlay — **one component, ~1,018 lines** |
| 6 | `components/rts/hooks/useRTSGameState.tsx` | 1,073 | TSX | Game-state hook + data constants |
| 7 | `lib/farm/__tests__/farmReducer.test.ts` | 887 | TS | Test file |
| 8 | `lib/farm/__tests__/gameLogic.test.ts` | 728 | TS | Test file |
| 9 | `components/rts/game/constants.ts` | 724 | TS | Game constants |
| 10 | `components/rts/hooks/useWaveSpawner.tsx` | 686 | TSX | Wave-spawning hook |

## Risk Rank & Rationale

1. **`components/rts/hooks/ai/tickWorkers.ts` — Critical**
   3,061 lines as a single exported function with no internal function boundaries at all. This is a severe structural signal: not "mixed concerns across functions" but **one function doing everything** for worker AI — pathing, task assignment, resource gathering, state transitions, presumably all inlined. Test coverage exists (`tickFunctions.test.ts`, `domainHooks.test.ts` both reference it), which gives a safety net for extraction, but the function itself needs to be broken into named sub-steps before it can be safely modified further. **Top priority for next `--refactor` cycle.**

2. **`components/rts/hooks/useRTSHandlers.tsx` — Critical**
   1,970 lines; the actual hook (`useRTSHandlers`, line 215 to EOF) is ~1,755 lines. Everything above it (formation modes, shop items, context types) is config/types, so the risk is concentrated in one hook function almost as large as `tickWorkers`. Same severity class as #1.

3. **`components/rts/RTSMap.tsx` / `components/rts/map/BuildingsLayer.tsx` / `components/rts/RTSUI.tsx` — High**
   Each is a single component function spanning most of its file (RTSMap ~1,250 lines, BuildingsLayer ~1,150 lines, RTSUI ~1,018 lines). This is the same "one giant render function" pattern flagged in nitsuah-io's `crypto/page.tsx` and motor-pool's `App.jsx` this cycle — it's showing up across multiple repos, which may be worth a cross-repo note for whoever's doing these refactors (possibly a shared starting template or habit).

4. **`components/rts/hooks/useRTSGameState.tsx` — Medium**
   1,073 lines but more varied: data constants (`DEFAULT_TREES`, `DEFAULT_GOLD_MINES`), small helpers (`makeWorker`, `makeCreeps`), and at least one hook (`useSecondCountdown`) — looks more like a module with multiple small exports than one giant function. Lower risk than #1–3 pending a closer read.

5. **`components/rts/game/constants.ts` — Low**
   724 lines of constants — per Evidence Rules, a flat data/config file is low structural risk regardless of size.

## Refactor Opportunities by Phase

**`components/rts/hooks/ai/tickWorkers.ts`** (do this one first):
- Phase 1 (lowest risk): read the function top-to-bottom and name its internal phases (e.g. pathing, task-selection, gather/deposit, idle-behavior) as comments, with no code movement — this is prep work, not a code change, and should happen before any extraction given the file's size.
- Phase 2: extract the most self-contained phase (likely pathing or idle-behavior) into a sibling function `tickWorkerPathing(...)` / `tickWorkerIdle(...)` in the same file, called from `tickWorkers`. Validate against `tickFunctions.test.ts` after each extraction.
- Phase 3: repeat per identified phase until `tickWorkers` is an orchestrator calling 4–6 named sub-functions.
- Phase 4 (optional, later): move sub-functions to sibling files under `components/rts/hooks/ai/workers/` if the single-file version is still unwieldy.

**`components/rts/hooks/useRTSHandlers.tsx`**:
- Phase 1: extract the formation-mode config (`FormationMode`, `FORMATION_OFFSETS_BY_MODE`) and shop config (`SHOP_ITEMS`) into `components/rts/game/handler-config.ts` — pure data, zero risk.
- Phase 2: split the hook body by handler domain (e.g. movement/formation handlers vs. shop/economy handlers vs. combat handlers) into smaller hooks composed inside `useRTSHandlers`.

**`RTSMap.tsx` / `BuildingsLayer.tsx` / `RTSUI.tsx`**:
- Phase 1 (each, independently): identify 2–3 sub-sections of the render tree (e.g. for `RTSUI`: resource bar, minimap, action panel) and extract each as a child component, following the same shape as the already-split `components/rts/map/*Layer.tsx` files and `components/rts/hud/ResourceBar.tsx` (552 lines, already its own file) — the codebase already has the right pattern for map layers, it just hasn't been applied to these three yet.

## Validation Plan (for eventual `--refactor`)
- Existing test suites to run after each phase: `lib/farm/__tests__/farmReducer.test.ts`, `lib/farm/__tests__/gameLogic.test.ts`, `components/rts/hooks/__tests__/tickFunctions.test.ts`, `tickEnemyAI.test.ts`, `domainHooks.test.ts`, `spawnHelpers.test.ts`, `towerHelpers.test.ts`.
- No `Dockerfile`/`docker-compose.yml` found at repo root — this is a frontend game; validate via `npm test` + dev-server smoke test (load the RTS mode, confirm workers still path/gather, confirm UI panels render) after each phase.
- Flag `RTSMap.tsx`, `BuildingsLayer.tsx`, `RTSUI.tsx`, and `useRTSHandlers.tsx` all as **UX surfaces needing manual QC** before merge — these are rendering/interaction-critical and tests won't catch visual regressions.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| farm-3j | `components/rts/hooks/ai/tickWorkers.ts` (3,061-line single function) | **Critical** | Last cycle's top finding (`useGameLoop.tsx`) was genuinely fixed (5,369→72 lines) but the complexity relocated here and to `useRTSHandlers.tsx` rather than being reduced |

## Ordered Next-Cycle Targets (this repo)
1. `components/rts/hooks/ai/tickWorkers.ts` — break the single 3,061-line function into named phases (Critical)
2. `components/rts/hooks/useRTSHandlers.tsx` — extract config + split by handler domain (Critical)
3. `components/rts/RTSMap.tsx` — extract render sub-sections (High)
4. `components/rts/map/BuildingsLayer.tsx` — extract render sub-sections (High)
5. `components/rts/RTSUI.tsx` — extract render sub-sections (High)

## Deferred / Not Flagged
- `components/rts/game/constants.ts` — flat data/config, low risk regardless of size.
- `components/rts/hooks/useRTSGameState.tsx` — mixed but more varied shape (data + small helpers + one hook); needs a closer read before ranking, not deferred indefinitely.
- `pnpm-lock.yaml` (8,007 lines) — lockfile, excluded from scope (regex gap from last cycle's generic `*.lock` filter, now fixed).

## Assumptions / Unconfirmed
- Churn/author-frequency signals for all files: **assumed unavailable** — shallow clone has no history beyond HEAD.
- `useRTSGameState.tsx` structural shape: partially read, not confirmed in full.
