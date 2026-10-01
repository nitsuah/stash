---
HEAD: a341d34a165ec0bc52664108f332a39cf5aaeb21
kind: eng-loc
repo: games
date: 2026-10-01
---

# ENG LOC Report — games (2026-10-01)

**Mode**: `--report` (dry run, no refactoring performed)
**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `*.lock`, `*-lock.json`, `*.min.*`, `dist/`, `build/`, `vendor/`, `node_modules/`, `__pycache__/`, `*.pyc`, `*.map`, `*.d.ts`, binary assets (incl. `.mp3`, `.glb`)

Source scanned: 261 files, 30,214 LOC. Analyzed from a `--depth 1` clone (single commit) — git history/churn signals are **not available** this run.

---

## Top LOC Files

| File | LOC | Lang | Role |
|---|---|---|---|
| `app/utils/audio/SoundManager.js` | 820 | JS | Web Audio synthesis — one class, ~25 sound-effect methods |
| `app/lib/asteroid/_comp/Game/Game.jsx` | 721 | JSX | Asteroid game root component |
| `app/lib/tank/TankGame.jsx` | 698 | JSX | Tank game component + canvas draw functions |
| `app/tests/asteroid/_comp/Game/handleTargetHit.test.js` | 664 | JS | Test suite |
| `app/_components/home/ArcadeLayout.tsx` | 661 | TSX | Arcade shell layout (mostly styled-components) |
| `app/tests/shared/scoring/StatsTracker.test.js` | 495 | JS | Test suite |
| `app/tests/shared/input/MouseManager.test.js` | 488 | JS | Test suite |
| `app/lib/breakout/BreakoutGame.tsx` | 402 | TSX | Breakout game component |
| `app/utils/audio/DynamicMusicSystem.js` | 366 | JS | Adaptive music engine |
| `app/lib/shared/audio/AudioManager.js` | 362 | JS | Shared audio manager |

5 of 261 source files exceed `max_lines=500`. 50 files are ≤30 lines — mostly small UI subcomponents and single-purpose handler modules (e.g. the `app/lib/asteroid/_comp/Game/handle*.js` family); scanned but not itemized here since LOC.md scopes merge-candidate review to the high end unless requested.

---

## Risk Rank & Rationale

### `app/lib/tank/TankGame.jsx` — **High**
- Structure: 4 canvas-drawing helper functions (lines 26–228, reasonably scoped) followed by a single default-exported component spanning **lines 229–698 (~470 lines)** — far over the ~80-line function signal. That component almost certainly holds game state, input handling, the game loop, and render orchestration together (mixed concerns).
- Test coverage: only one test file found (`app/tests/tank/tankLogic.test.js`) against a 698-line component — thin coverage relative to file size (assumed gap; exact tankLogic.test.js scope not line-verified this run).

### `app/lib/asteroid/_comp/Game/Game.jsx` — **Medium**
- 721 lines including ~20 dynamically-imported UI subcomponent references (lines 11–38) plus the main component body. Mixed concerns (UI composition + game orchestration) are present by structure, but risk is tempered by evidence of prior extraction discipline: game-logic handlers (`handleTargetHit`, `handleGameOver`, `handleHealthDepletion`, `handleMiss`, `handlePlayerHit`, `restartGame`, `updateScore`, `generateTargets`, `colorblindModes`) each live in their own file with a matching test, under `app/tests/asteroid/_comp/Game/`. `Game.jsx` itself is likely mostly wiring/composition rather than raw logic.

### `app/utils/audio/SoundManager.js` — **Low-Medium**
- Single clear concern (procedural sound synthesis), not mixed concerns — per LOC.md guardrails, high LOC with one clear concern is lower structural risk even though it exceeds the threshold.
- Secondary signal: several methods run 50–80 lines each (e.g. `_playExplosion` ~80 lines, `playKillStreak` ~59 lines) — borderline on the function-length signal, but each is independent and swappable (one method per effect). If split, the natural cut is by category (explosions/power-ups/combat/ambient), not by urgency.

### `app/_components/home/ArcadeLayout.tsx` — **Low**
- Lines 1–574 are almost entirely `styled-components` definitions (keyframes + styled elements); actual component logic starts around line 575. This matches the LOC.md guardrail for CSS-heavy files: high LOC, single clear concern (presentation), low structural risk. Has a matching test (`app/tests/home/ArcadeLayout.test.jsx`).

### Large test files (`handleTargetHit.test.js`, `StatsTracker.test.js`, `MouseManager.test.js`) — **Low**
- Expected verbosity for test suites; not flagged as refactor risk.

---

## Refactor Opportunities by Phase (reference only — `--report` mode, no execution)

1. **`TankGame.jsx`, phase 1**: Extract game-state/input logic out of the default component into a `useTankGameState` hook (mirroring the extraction pattern already used in the asteroid game), leaving the component as render + wiring. Smallest safe cut.
2. **`TankGame.jsx`, phase 2**: Move the four canvas `draw*` helpers (lines 26–228) into `tankRenderer.js`, imported back in. Low risk — already free-standing functions taking explicit params.
3. **`SoundManager.js`, deferred**: Split by sound category only if the file keeps growing; current size is tolerable for a single-concern synthesis module. Not a priority this cycle.
4. **`ArcadeLayout.tsx`**: No action recommended — CSS-heavy file, handle in a design-system pass per LOC.md guardrails, not an LOC refactor cycle.

## Validation Plan (if executed)
- Run the existing Vitest/Jest suite (`app/tests/...`) and smoke-test each affected game (`tank`, `asteroid`) in the dev server before any commit.
- `TankGame.jsx` and `Game.jsx` changes touch rendering/interaction — per LOC.md, flag both as needing manual QC on the golden path (move, shoot, game-over, pause) before merge, not CI-green alone.

---

## Summary

| Repo | Top concern | Priority | Notes |
|---|---|---|---|
| games | `TankGame.jsx` bundles a ~470-line component (state+input+loop+render) with thin test coverage | High | Asteroid's `Game.jsx` shows the target pattern (logic extracted to tested handler files) — Tank should follow it |

**Churn/history**: not assessable — analysis ran against a `--depth 1` clone (single commit visible).
**Canaries**: n/a — `stash` (the only tracked canary file's repo) was not in this run's target set.
