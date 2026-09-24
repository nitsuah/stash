# ENG LOC Report: darkmoon
**Date:** 2026-07-03
**Repo:** darkmoon (darkmoon)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 2078 | `src/components/GameUI.tsx` | Repeated block (2 occurrences, 10+ lines):               <div
                style={{
                  marginBottom: isMi... |
| 956 | `src/pages/Solo.tsx` | Repeated block (2 occurrences, 10+ lines): 
      // Check if any touch is on a joystick element
      const touchesOnJoyst... |
| 863 | `src/__tests__/useBotAI.test.ts` | Repeated block (2 occurrences, 10+ lines):         targetIsIt: false,
        onTagTarget: mockOnTagTarget,
        onPosit... |
| 657 | `src/pages/Solo/components/ShootingGallery.tsx` | — |
| 626 | `src/pages/Solo/components/Bots.tsx` | — |
| 594 | `src/components/characters/useBotAI.ts` | Unused function (heuristic): setTimeout; Repeated block (2 occurrences, 10+ lines):         if (steerFramesLeft.current > 0) {
          steerFramesLeft.current--;
... |
| 560 | `src/__tests__/useBotAI.unit.test.tsx` | Repeated block (2 occurrences, 10+ lines):       targetPositionRef: { current: [5, 0, 0] },
    });

    frameCallback!(nul... |
| 530 | `src/components/characters/PlayerCharacter.tsx` | — |
| 507 | `src/components/SoundManager.ts` | Unused function (heuristic): constructor; Unused function (heuristic): setTimeout |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 1 | `src/pages/Solo/index.tsx` | — |
| 7 | `src/components/characters/player/index.ts` | — |
| 8 | `playwright.config.ts` | — |
| 8 | `src/index.tsx` | src/global.d.ts |
| 8 | `src/types/react-three-fiber-jsx-runtime.d.ts` | src/types/socket.ts |
| 9 | `src/global.d.ts` | src/index.tsx |
| 10 | `server/profanity.d.ts` | server/profanity.js |
| 14 | `e2e/smoke.spec.ts` | — |
| 17 | `src/__tests__/camera-controls.test.tsx` | src/__tests__/profanity.test.ts |
| 19 | `src/components/__tests__/SoundEngine.test.ts` | src/components/__tests__/soundHelpers.test.ts |
| 19 | `src/types/socket.ts` | src/types/react-three-fiber-jsx-runtime.d.ts |
| 20 | `src/components/Footer.tsx` | src/components/soundNodeFactory.ts |
| 23 | `src/components/soundNodeFactory.ts` | src/components/Footer.tsx |
| 24 | `server/profanity.js` | server/profanity.d.ts |
| 24 | `src/components/soundHelpers.ts` | src/components/Footer.tsx |
| 24 | `src/__tests__/profanity.test.ts` | src/__tests__/camera-controls.test.tsx |
| 25 | `src/components/__tests__/soundHelpers.test.ts` | src/components/__tests__/SoundEngine.test.ts |
| 25 | `src/lib/hooks/useMouseControls.ts` | src/lib/hooks/useRockPositions.ts |
| 26 | `src/components/world/__tests__/HealthPickups.test.ts` | src/components/world/__tests__/WeaponPickups.test.ts |
| 27 | `src/components/21st.dev/Spinner.tsx` | — |
| 27 | `src/lib/hooks/useRockPositions.ts` | src/lib/hooks/useMouseControls.ts |
| 27 | `src/__tests__/useSocketConnection.test.tsx` | src/__tests__/camera-controls.test.tsx |
| 28 | `src/vite-env.d.ts` | src/index.tsx |
| 28 | `src/components/__tests__/ThemeToggle.test.tsx` | src/components/__tests__/SoundEngine.test.ts |
| 29 | `scripts/run-tests-inprocess.js` | — |
| 30 | `src/components/world/__tests__/WeaponPickups.test.ts` | src/components/world/__tests__/HealthPickups.test.ts |
| 30 | `src/lib/hooks/useMobileDetection.ts` | src/lib/hooks/useMouseControls.ts |
| 30 | `src/lib/hooks/__tests__/useJetpack.test.ts` | — |
| 30 | `src/__tests__/Footer.test.tsx` | src/__tests__/camera-controls.test.tsx |
