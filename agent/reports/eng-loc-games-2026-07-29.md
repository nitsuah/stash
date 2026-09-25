---
kind: eng-loc
repo: games
date: 2026-07-29
---

# ENG LOC Report — games (2026-07-29)

> 🧭 [[repos/games|games]] · ← [[reports/eng-loc-games-2026-07-04|2026-07-04]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 829 | games/app/lib/asteroid/_comp/Game/Game.jsx | Main game component - extract systems |
| 808 | games/app/utils/audio/SoundManager.js | Sound manager - extract audio systems |
| 664 | games/app/tests/asteroid/_comp/Game/handleTargetHit.test.js | Test - split by hit scenarios |
| 529 | games/app/_components/home/ArcadeLayout.tsx | Arcade layout - extract sections |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | games/app/__mocks__/styleMock.js | Merge with test mocks |
| 1 | games/app/__mocks__/fileMock.js | Merge with test mocks |
| 1 | games/app/utils/time.js | Merge with utils |
| 4 | games/app/lib/asteroid/_comp/Game/updateScore.js | Merge with game |
| 4 | games/app/tests/shared/scoring/StatsTracker.test.js | Merge with scoring tests |
| 4 | games/app/tests/shared/input/MouseManager.test.js | Merge with input tests |
| 5 | games/app/pages/fps/_comps/PowerUp.jsx | Merge with FPS components |
| 5 | games/app/pages/fps/_comps/ShatterCube.jsx | Merge with FPS components |
| 5 | games/app/pages/fps/_comps/PlayerLogic.jsx | Merge with FPS components |
| 5 | games/app/pages/fps/_comps/Bullet.jsx | Merge with FPS components |
| 5 | games/app/tests/asteroid/_comp/Target/splitTarget.test.js | Merge with target tests |
| 5 | games/app/pages/fps/_comps/Controls.js | Merge with FPS components |
| 5 | games/app/lib/breakout/BreakoutGame.tsx | Check if needed |
| 5 | games/app/utils/audio/DynamicMusicSystem.js | Merge with SoundManager |
| 5 | games/app/lib/shared/audio/AudioManager.js | Merge with SoundManager |
| 7 | games/app/pages/fps/_comps/Decal.jsx | Merge with FPS components |
| 7 | games/app/lib/shared/input/index.js | Merge with input barrel |
| 7 | games/app/lib/shared/scoring/index.js | Merge with scoring barrel |
| 7 | games/app/lib/breakout/components/Ball.jsx | Merge with Breakout |
| 9 | games/app/lib/breakout/components/Paddle.jsx | Merge with Breakout |
| 9 | games/app/lib/asteroid/_comp/UI/ShotReticle.jsx | Merge with asteroid UI |
| 9 | games/app/lib/fps/_comps/Crosshair.jsx | Merge with FPS |
| 9 | games/app/lib/asteroid/_comp/UI/Crosshair.jsx | Merge with asteroid UI |
| 10 | games/app/tests/shared/input/index.test.js | Merge with input tests |
| 10 | games/app/lib/breakout/components/Brick.jsx | Merge with Breakout |
| 11 | games/app/lib/shared/ui/ArcadeHeader.jsx | Merge with shared UI |
| 11 | games/app/e2e/debug-space-invaders.js | Check if debug script |
| 11 | games/app/pages/fps/_comps/Crosshair.jsx | Duplicate |
| 11 | games/app/lib/asteroid/_comp/UI/OnboardingOverlay.jsx | Merge with asteroid UI |
| 11 | games/app/lib/breakout/components/Brick.jsx | Duplicate |
| 12 | games/app/lib/asteroid/_comp/Game/handleMiss.js | Merge with game |
| 12 | games/app/middleware.js | Check if middleware |
| 12 | games/app/tests/shared/scoring/index.test.js | Merge with scoring tests |
| 14 | games/app/public/register-sw.js | Service worker |
| 14 | games/app/lib/fps/_comps/ComboDisplay.jsx | Merge with FPS |
| 14 | games/app/lib/asteroid/_comp/Target/splitTarget.test.js | Merge with target |
| 15 | games/app/lib/breakout/BreakoutCanvas.jsx | Merge with Breakout |
| 15 | games/app/pages/index.tsx | Check if page entry |
| 17 | games/app/lib/asteroid/_comp/UI/PowerUpPopup.jsx | Merge with asteroid UI |
| 17 | games/app/_components/shared/gamepad/ShootButton.tsx | Merge with gamepad |
| 17 | games/app/_components/objects/Colosseum.js | Merge with objects |
| 17 | games/app/_components/objects/Cube.js | Merge with objects |
| 17 | games/app/lib/shared/ui/ArcadeMenu.jsx | Merge with shared UI |
| 19 | games/app/lib/asteroid/_comp/UI/FlashOverlays.jsx | Merge with asteroid UI |
| 19 | games/app/lib/asteroid/_comp/UI/ScoreDisplay.jsx | Merge with asteroid UI |
| 19 | games/app/lib/asteroid/_comp/Target/TargetList.jsx | Merge with asteroid target |
| 20 | games/app/_components/objects/Floor.js | Merge with objects |
| 22 | games/app/lib/asteroid/_comp/UI/PowerUpPopup.jsx | Duplicate |
| 25 | games/app/lib/breakout/BreakoutCanvas.jsx | Duplicate |
| 25 | games/app/pages/dodge-blocks.jsx | Check if page |
| 25 | games/app/pages/memory-match.jsx | Check if page |
| 27 | games/app/_components/shared/gamepad/ShootButton.tsx | Duplicate |
| 28 | games/app/lib/asteroid/_comp/UI/PointerLockControls.js | Merge with asteroid UI |

---

*Generated: 2026-07-29*
