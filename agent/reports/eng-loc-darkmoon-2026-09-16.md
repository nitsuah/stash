---
kind: eng-loc
repo: darkmoon
date: 2026-09-16
---

# LOC Report — darkmoon

> 🧭 [[repos/darkmoon|darkmoon]] · ← [[reports/eng-loc-darkmoon-2026-07-29|2026-07-29]] <!-- nav -->

Mode: `--report` (dry run, no changes made)
Date: 2026-09-16
Source: shallow clone (`--depth 1`) of `nitsuah/darkmoon` @ `6f1e9940659709de47f776c897f7f52f723cb74f`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Additional exclusion applied this run: `src/components/Soldier.glb` — a binary 3D model asset that `wc -l` mis-measured as 6412 "lines"; binary assets are excluded per Phase 0 spec regardless of extension.
Note: shallow clone — churn/author history (many-authors, frequent-edits signal) is **not available**; that structural signal is marked "assumed: not confirmed" throughout.

## Inventory Summary
- Tracked source files (post-exclusion): 276
- Total LOC counted: 42,294

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `docs/CONKER_BFD_BUILD_GUIDE.md` | 1698 | Markdown | Build/design documentation |
| 2 | `src/styles/App.css` | 879 | CSS | App-wide styles |
| 3 | `src/__tests__/useBotAI.test.ts` | 863 | TS | Test file (excluded from risk ranking) |
| 4 | `src/styles/Home.css` | 740 | CSS | Home page styles |
| 5 | `docs/archive/ROADMAP_DETAILED.md` | 713 | Markdown | Archived roadmap doc |
| 6 | `src/pages/Solo/components/ShootingGallery.tsx` | 657 | TSX | Solo-mode shooting gallery minigame |
| 7 | `docs/archive/L7_ENGINEERING_REVIEW.md` | 656 | Markdown | Archived review doc |
| 8 | `docs/archive/ARCHITECTURE_IMPROVEMENTS.md` | 656 | Markdown | Archived architecture doc |
| 9 | `src/pages/Solo.tsx` | 651 | TSX | Solo game-mode top-level page/component |
| 10 | `src/pages/Solo/components/Bots.tsx` | 629 | TSX | Bot entity rendering/logic |

Notable files just outside the numeric top 10 but flagged for risk: `server/index.js` (619 LOC), `src/components/characters/useBotAI.ts` (594 LOC).

## Risk Rank & Rationale

1. **`src/components/characters/useBotAI.ts` — Critical**
   594 lines, and the entire file is effectively **one function**: `useBotAI` spans lines 81–594 (~513 lines) — by far the largest single function seen across all three repos audited this cycle. This is a textbook complexity hotspot by the "functions over ~80 lines" signal alone, independent of size. Notably it is *heavily* tested — `src/__tests__/useBotAI.test.ts` (863 lines) and `src/__tests__/useBotAI.unit.test.tsx` (560 lines), over 1400 lines of test code — so extraction risk is unusually low for a file this size; the tests should catch regressions during a split.

2. **`src/pages/Solo.tsx` — High**
   651 lines. Structural evidence: 20+ `useState` declarations and 9+ `useEffect` hooks in one component, covering socket/networking state, game state, input (keyboard/joystick), tag-game scoring, and debug-mode toggles — a classic React "god component" mixing networking, game logic, input handling, and rendering. Has a dedicated test (`src/__tests__/Solo.test.tsx`), which lowers extraction risk somewhat.

3. **`src/pages/Solo/components/ShootingGallery.tsx` — Medium**
   657 lines but only 3 top-level functions found (`buildTargetDefs`, `computeGalleryAward`, `makeTargetState`) — the bulk of the file is likely the React component body itself (not yet function-boundary-inspected in detail). `computeGalleryAward` is exported and likely the core scoring logic; related test coverage exists at the game-mode level (`gameManager.gallery.test.ts`, `galleryScoring.test.ts`) though no test file targets this component directly by name. Flagged for a closer look next cycle before committing to a specific extraction cut.

4. **`src/pages/Solo/components/Bots.tsx` — Medium**
   629 lines, not yet function-boundary-inspected this pass. Given its role (bot entity rendering) alongside the already-confirmed 513-line `useBotAI` hook it likely consumes, this file is provisionally flagged for the same mixed game-logic/rendering pattern seen in `Solo.tsx` — marked "assumed: not confirmed" pending inspection.

5. **`server/index.js` — Medium**
   619 lines. Not yet function-boundary-inspected this pass (route/socket-handler structure not confirmed). Flagged provisionally by size and role (server entrypoints commonly mix HTTP routes, socket handlers, and game-loop orchestration) — "assumed: not confirmed."

6. **CSS files (`App.css`, `Home.css`) — Low (excluded per guardrail)**
   Style-only, large but single-concern. Deferred to a design-system pass.

7. **`docs/*.md` files in top 10 — Low (not applicable)**
   Documentation, not source code subject to refactor risk. `CONKER_BFD_BUILD_GUIDE.md` and the three `docs/archive/*.md` files are large but out of scope for this pass entirely.

## Refactor Opportunities by Phase

**`useBotAI.ts`** (Critical):
- Phase 1: Extract the bot's perception/targeting logic (whatever sub-block computes target selection or line-of-sight, based on a closer read of the 513-line body) into `useBotAI/perception.ts` — smallest safe cut, hook still calls into it.
- Phase 2: Extract movement/pathing logic into `useBotAI/movement.ts`.
- Phase 3: Extract combat/tag-state-transition logic into `useBotAI/combat.ts`, leaving `useBotAI.ts` as a thin composition of the three sub-hooks.
- Given the strong existing test coverage, run the full `useBotAI.test.ts` + `useBotAI.unit.test.tsx` suite after every single extraction, not just at phase boundaries.

**`Solo.tsx`** (High):
- Phase 1: Extract socket/networking state and its `useEffect` handlers into a `useSoloGameSocket` custom hook.
- Phase 2: Extract input handling (keyboard + joystick state) into a `useSoloInput` hook.
- Phase 3: Extract tag-game scoring state (`playerIsIt`, `bot*GotTagged`) into a `useTagScoring` hook, leaving `Solo.tsx` as the composing page component.

## Validation Plan (for eventual `--refactor`)
- `useBotAI.ts`: run `src/__tests__/useBotAI.test.ts` and `useBotAI.unit.test.tsx` before and after every extraction step — this is the best-covered file in the repo, use that coverage fully.
- `Solo.tsx`: run `src/__tests__/Solo.test.tsx`; manually smoke-test a Solo-mode session (movement, tagging, bot AI, gallery minigame) in the dev server after each phase since this is a rendering/interaction-heavy surface — flag for manual QC before merge, not just CI green, per LOC.md's UX guardrail.
- No Dockerfile/devcontainer confirmed in this pass (report mode only) — confirm before assuming host-run is safe for `--refactor`.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| darkmoon | `useBotAI.ts`: single 513-line function (the entire hook body) | Critical | Best next-cycle target; unusually strong existing test coverage (1400+ lines) de-risks the split |

## Ordered Next-Cycle Targets (this repo)
1. `src/components/characters/useBotAI.ts` — split the 513-line hook into perception/movement/combat sub-hooks (Critical, highest ROI — well-tested)
2. `src/pages/Solo.tsx` — extract socket, input, and scoring state into custom hooks (High)
3. `src/pages/Solo/components/ShootingGallery.tsx` — inspect function boundaries, confirm/deny mixed-concerns before committing to a cut (Medium, needs deeper look)
4. `src/pages/Solo/components/Bots.tsx` — inspect function boundaries next cycle (Medium, not yet confirmed)
5. `server/index.js` — inspect route/socket-handler structure next cycle (Medium, not yet confirmed)

## Deferred / Not Flagged
- `src/styles/App.css`, `src/styles/Home.css` — CSS-only, deferred to design-system pass per guardrail.
- `docs/CONKER_BFD_BUILD_GUIDE.md` and `docs/archive/*.md` — documentation, not source complexity risk.
- `src/components/Soldier.glb` — excluded entirely as a binary 3D asset, not source.
- Test files in top-10 by size (`useBotAI.test.ts`) — excluded from refactor ranking; large test files are expected.

## Assumptions / Unconfirmed
- Churn/author-frequency signal: **assumed unavailable** — shallow clone has no history beyond HEAD.
- `ShootingGallery.tsx`, `Bots.tsx`, `server/index.js`: ranked provisionally by size + role only; function-boundary structure not yet inspected — flagged for closer read before any `--refactor` commitment.
