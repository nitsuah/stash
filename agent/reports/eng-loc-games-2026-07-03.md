# ENG LOC Report: games
**Date:** 2026-07-03
**Repo:** games (games)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 829 | `app/lib/asteroid/_comp/Game/Game.jsx` | — |
| 808 | `app/utils/audio/SoundManager.js` | Unused function (heuristic): constructor; Unused function (heuristic): setSoundEnabled; Unused function (heuristic): setSfxVolume; Unused function (heuristic): startThruster; Unused function (heuristic): stopThruster; Unused function (heuristic): playExplosion; Unused function (heuristic): playPowerUpCollect; Unused function (heuristic): playPowerUpActivate; Unused function (heuristic): playPowerUpDeactivate; Unused function (heuristic): playHitImpact; Unused function (heuristic): playLaserShoot; Unused function (heuristic): playShotgunShoot; Unused function (heuristic): playCannonShoot; Unused function (heuristic): playComboMilestone; Unused function (heuristic): updateHeartbeat; Unused function (heuristic): playKillStreak; Unused function (heuristic): playWaveClear; Repeated block (2 occurrences, 10+ lines):     if (!this.soundEnabled) return;
    if (typeof window === 'undefined') retur... |
| 664 | `app/tests/asteroid/_comp/Game/handleTargetHit.test.js` | Unused function (heuristic): describe; Unused function (heuristic): beforeEach; Unused function (heuristic): afterEach; Repeated block (6 occurrences, 10+ lines):     const params = {
      targetId: 1,
      cooldowns: { spread: 0 },
      we... |
| 529 | `app/_components/home/ArcadeLayout.tsx` | Unused function (heuristic): if |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 1 | `app/utils/time.js` | — |
| 1 | `app/__mocks__/fileMock.js` | app/__mocks__/styleMock.js |
| 1 | `app/__mocks__/styleMock.js` | app/__mocks__/fileMock.js |
| 4 | `app/lib/asteroid/_comp/Game/updateScore.js` | app/lib/asteroid/_comp/Game/loadSavedScores.js |
| 5 | `app/pages/fps/_comps/Bullet.jsx` | app/pages/fps/_comps/Controls.js |
| 5 | `app/pages/fps/_comps/Controls.js` | app/pages/fps/_comps/Bullet.jsx |
| 5 | `app/pages/fps/_comps/PlayerLogic.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 5 | `app/pages/fps/_comps/PowerUp.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 5 | `app/pages/fps/_comps/ShatterCube.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 5 | `app/pages/fps/_comps/ShootingHandler.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 7 | `app/next-env.d.ts` | app/middleware.js |
| 7 | `app/lib/asteroid/_comp/Game/loadSavedScores.js` | app/lib/asteroid/_comp/Game/updateScore.js |
| 7 | `app/lib/shared/audio/index.js` | — |
| 7 | `app/lib/shared/input/index.js` | — |
| 7 | `app/pages/fps/_comps/Decal.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 8 | `app/lib/shared/scoring/index.js` | — |
| 9 | `app/lib/asteroid/_comp/UI/ShotReticle.jsx` | app/lib/asteroid/_comp/UI/Crosshair.jsx |
| 9 | `app/lib/breakout/components/Ball.jsx` | app/lib/breakout/components/Paddle.jsx |
| 10 | `app/lib/asteroid/_comp/UI/Crosshair.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 10 | `app/lib/fps/_comps/Crosshair.jsx` | app/lib/fps/_comps/ComboDisplay.jsx |
| 10 | `app/pages/fps/_comps/Crosshair.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 10 | `app/tests/shared/input/index.test.js` | — |
| 11 | `app/e2e/debug-space-invaders.js` | app/e2e/a11y.spec.js |
| 11 | `app/lib/shared/ui/ArcadeHeader.jsx` | app/lib/shared/ui/ArcadeMenu.jsx |
| 12 | `app/middleware.js` | app/next-env.d.ts |
| 12 | `app/lib/asteroid/_comp/Game/handleMiss.js` | app/lib/asteroid/_comp/Game/updateScore.js |
| 12 | `app/lib/fps/_comps/ComboDisplay.jsx` | app/lib/fps/_comps/Crosshair.jsx |
| 12 | `app/tests/shared/scoring/index.test.js` | — |
| 13 | `app/pages/fps/_comps/Target.jsx` | app/pages/fps/_comps/Bullet.jsx |
| 14 | `app/layout.jsx` | app/next-env.d.ts |
| 14 | `app/lib/asteroid/_comp/UI/SlowMotionOverlay.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 14 | `app/public/register-sw.js` | — |
| 15 | `app/lib/breakout/components/Paddle.jsx` | app/lib/breakout/components/Ball.jsx |
| 17 | `app/e2e/a11y.spec.js` | app/e2e/debug-space-invaders.js |
| 17 | `app/lib/asteroid/_comp/UI/OnboardingOverlay.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 17 | `app/lib/breakout/components/Brick.jsx` | app/lib/breakout/components/Ball.jsx |
| 17 | `app/pages/index.tsx` | app/pages/dodge-blocks.jsx |
| 19 | `app/lib/asteroid/_comp/UI/BoundaryBox.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 19 | `app/lib/shared/ui/ArcadeMenu.jsx` | app/lib/shared/ui/ArcadeHeader.jsx |
| 19 | `app/_components/objects/Colosseum.js` | app/_components/objects/Cube.js |
| 19 | `app/_components/objects/Cube.js` | app/_components/objects/Colosseum.js |
| 20 | `app/_components/objects/Floor.js` | app/_components/objects/Colosseum.js |
| 22 | `app/lib/asteroid/_comp/UI/PowerUpPopup.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 22 | `app/lib/asteroid/_comp/UI/ScoreDisplay.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 23 | `app/lib/asteroid/_comp/UI/FlashOverlays.jsx` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
| 25 | `app/lib/asteroid/_comp/Target/TargetList.jsx` | — |
| 25 | `app/lib/breakout/BreakoutCanvas.jsx` | — |
| 25 | `app/_components/shared/gamepad/ShootButton.tsx` | — |
| 26 | `app/lib/asteroid/_comp/Game/handleKeyDown.js` | app/lib/asteroid/_comp/Game/updateScore.js |
| 27 | `app/pages/dodge-blocks.jsx` | app/pages/index.tsx |
| 27 | `app/pages/memory-match.jsx` | app/pages/index.tsx |
| 28 | `app/lib/asteroid/_comp/UI/PointerLockControls.js` | app/lib/asteroid/_comp/UI/ShotReticle.jsx |
