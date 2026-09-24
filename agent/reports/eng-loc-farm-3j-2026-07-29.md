# ENG LOC Report — farm-3j (2026-07-29)

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 5369 | farm-3j/components/rts/hooks/useGameLoop.tsx | **Largest file** - main game loop, extract systems |
| 4392 | farm-3j/components/rts/RTSMap.tsx | Map rendering - extract layers |
| 2110 | farm-3j/components/rts/RTSUI.tsx | UI component - extract panels |
| 937 | farm-3j/components/animations/HeaderCropRow.tsx | Animation component |
| 813 | farm-3j/lib/farm/__tests__/farmReducer.test.ts | Test file - split by reducer action |
| 728 | farm-3j/lib/farm/__tests__/gameLogic.test.ts | Test file - split by feature |
| 694 | farm-3j/components/rts/hooks/useWaveSpawner.tsx | Wave spawner hook |
| 608 | farm-3j/components/rts/game/constants.ts | Constants - split by domain |
| 605 | farm-3j/components/rts/map/EnemySiegeCastersLayer.tsx | Map layer |
| 603 | farm-3j/components/rts/hooks/useTowerCombat.tsx | Tower combat hook |
| 601 | farm-3j/components/rts/map/WorkersLayer.tsx | Workers layer |
| 565 | farm-3j/components/rts/hud/ResourceBar.tsx | HUD resource bar |
| 484 | farm-3j/components/rts/map/EnemyGruntsLayer.tsx | Map layer |
| 478 | farm-3j/components/rts/RTSGameRoot.tsx | Game root |
| 477 | farm-3j/components/rts/map/EffectsLayer.tsx | Effects layer |
| 452 | farm-3j/components/rts/hooks/useBotController.ts | Bot controller |
| 425 | farm-3j/components/rts/map/EnemyEliteLayer.tsx | Elite layer |
| 364 | farm-3j/components/rts/game/types.ts | Game types - split by domain |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 2 | farm-3j/coverage/lcov-report/prettify.js | Generated coverage file |
| 2 | farm-3j/coverage/prettify.js | Generated coverage file |
| 2 | farm-3j/global.d.ts | Merge with types |
| 5 | farm-3j/app/rtsfarm/layout.tsx | Check if layout wrapper |
| 5 | farm-3j/app/farm/page.tsx | Check if page wrapper |
| 6 | farm-3j/lib/utils.ts | Merge with utils barrel |
| 7 | farm-3j/app/rtsfarm/page.tsx | Check if page wrapper |
| 8 | farm-3j/config/vitest.setup.ts | Check if test setup |
| 8 | farm-3j/components/animations/index.ts | Merge with animations barrel |
| 8 | farm-3j/app/not-found.tsx | Check if not-found page |
| 9 | farm-3j/app/farm/layout.tsx | Check if layout wrapper |
| 21 | farm-3j/app/global-error.tsx | Check if error boundary |
| 23 | farm-3j/components/rts/ui/Stat.tsx | Merge with UI components |
| 29 | farm-3j/scripts/print-docker-port.js | Script - check if needed |

---

*Generated: 2026-07-29*