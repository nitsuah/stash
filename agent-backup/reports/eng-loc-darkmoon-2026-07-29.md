---
kind: eng-loc
repo: darkmoon
date: 2026-07-29
---

# ENG LOC Report — darkmoon (2026-07-29)

> 🧭 [[repos/darkmoon|darkmoon]] · ← [[reports/eng-loc-darkmoon-2026-07-04|2026-07-04]] · [[reports/eng-loc-darkmoon-2026-09-16|2026-09-16]] → <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 2078 | darkmoon/src/components/GameUI.tsx | **Large game UI** - extract HUD, menus, overlays |
| 956 | darkmoon/src/pages/Solo.tsx | Solo game page - extract modes |
| 863 | darkmoon/src/__tests__/useBotAI.test.ts | Bot AI tests - split by behavior |
| 657 | darkmoon/src/pages/Solo/components/ShootingGallery.tsx | Shooting gallery - extract targets |
| 626 | darkmoon/src/pages/Solo/components/Bots.tsx | Bots manager - extract types |
| 594 | darkmoon/src/components/characters/useBotAI.ts | Bot AI hook - extract states |
| 560 | darkmoon/src/__tests__/useBotAI.unit.test.tsx | Unit tests - split by function |
| 513 | darkmoon/src/components/characters/PlayerCharacter.tsx | Player - extract movement/combat |
| 507 | darkmoon/src/components/SoundManager.ts | Sound manager - extract systems |
| 472 | darkmoon/src/components/characters/player/PlayerMovement.tsx | Movement - extract physics |
| 412 | darkmoon/server/index.js | Server entry - extract routes |
| 401 | darkmoon/src/components/GameManager.ts | Game manager - extract systems |
| 398 | darkmoon/src/__tests__/PauseMenu.test.tsx | Pause menu tests |
| 381 | darkmoon/src/__tests__/gameManager.deathmatch.test.ts | Deathmatch tests |
| 377 | darkmoon/src/components/SpacemanModel.tsx | 3D model component |
| 367 | darkmoon/src/pages/Solo/components/__tests__/Bots.test.tsx | Bots tests |
| 357 | darkmoon/src/components/characters/player/PlayerWeapon.tsx | Weapon system |
| 343 | darkmoon/src/__tests__/gameManager.ctf.test.ts | CTF tests |
| 331 | darkmoon/src/components/CollisionSystem.ts | Collision system |
| 331 | darkmoon/src/components/gameModes/CTFMode.ts | CTF mode |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | darkmoon/src/pages/Solo/index.tsx | Check if barrel export |
| 7 | darkmoon/src/components/characters/player/index.ts | Merge with player barrel |
| 8 | darkmoon/playwright.config.ts | Check if config |
| 8 | darkmoon/src/index.tsx | Check if entry point |
| 8 | darkmoon/src/types/react-three-fiber-jsx-runtime.d.ts | Check if type def |
| 10 | darkmoon/server/profanity.d.ts | Merge with types |
| 14 | darkmoon/e2e/smoke.spec.ts | Merge with e2e tests |
| 16 | darkmoon/src/global.d.ts | Merge with global types |
| 17 | darkmoon/src/__tests__/camera-controls.test.tsx | Merge with test file |
| 19 | darkmoon/src/components/__tests__/SoundEngine.test.ts | Merge with sound tests |
| 19 | darkmoon/src/types/socket.ts | Merge with types |
| 20 | darkmoon/src/components/Footer.tsx | Merge with layout |
| 23 | darkmoon/src/components/soundNodeFactory.ts | Merge with sound system |
| 23 | darkmoon/server/profanity.js | Merge with server |
| 24 | darkmoon/src/components/__tests__/soundHelpers.test.ts | Merge with sound tests |
| 24 | darkmoon/src/components/soundHelpers.ts | Merge with sound system |
| 25 | darkmoon/src/lib/hooks/useMouseControls.ts | Merge with hooks |
| 25 | darkmoon/src/components/__tests__/ThemeToggle.test.tsx | Merge with UI tests |
| 26 | darkmoon/src/components/world/__tests__/HealthPickups.test.ts | Merge with world tests |
| 27 | darkmoon/src/lib/hooks/useRockPositions.ts | Merge with hooks |
| 27 | darkmoon/src/components/21st.dev/Spinner.tsx | Check if external |
| 28 | darkmoon/src/components/__tests__/ThemeToggle.test.tsx | Duplicate |
| 29 | darkmoon/scripts/run-tests-inprocess.js | Check if test script |

---

*Generated: 2026-07-29*
