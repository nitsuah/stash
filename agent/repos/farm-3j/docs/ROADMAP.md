# ROADMAP

Last Updated: 2026-09-23

## 2026 Q1 ✅

> Completed. Core Next.js architecture with linting/CI, Farm Tycoon Phase 1 MVP, and Farm Tycoon Phase 2a–2f isometric grid foundation shipped.

## 2026 Q2–Q3: Farm RTS MVP ✅ (feature-complete)

> All core gameplay systems shipped. 25×25 map, 10+ enemy unit types, full economy/combat/building loop, fog of war, day/night cycle, hero unit, 20+ buildings, unit veterancy, tech research, save/load, procedural audio, high-score leaderboard, and wave escalation all live. Codebase refactored with shared SVG component layer (HpBar, StructureDamageSmoke, StructureFireEffect) eliminating duplicated render primitives across all map layer files. Modularization Phase 1 completed (2026-08-04): `RTSUI` decomposed into `BuildMenu`/`WaveTimer`/`HeroPanel`; `HeaderCropRow` background extracted; pure functions isolated in `spawnHelpers`, `towerHelpers`, `mapSelectors` with +55 tests (264 total). Modularization Phase 2a completed (PR #295): `useGameLoop.tsx` decomposed from a single monolith into `useEnemyAI`/`useResourceTick`/`useCombatResolution`/`usePathfinding`/`useBotController` plus a dozen domain-specific tick modules under `hooks/ai/`; the main loop is now a thin orchestrator calling each hook's tick closure inside one `requestAnimationFrame` (preserving React 18 automatic batching — domain hooks return plain `(dt) => void` closures rather than each running its own rAF loop). Vitest coverage scope expanded from `lib/**` only to also include RTS game logic, thresholds raised (see the `thresholds` block in `config/vitest.config.ts` — source of truth — for current lines/statements/functions/branches percentages). Phase 2b completed (2026-09-02): `RTSMap.tsx`'s SVG render tree (pan/zoom viewport + all 12 map layers) now lives in `MapRenderer`; `RTSMap.tsx` is a thin container wiring per-layer prop bags rather than rendering the layer stack inline.

## 2026 Q3: Farm RTS — Round 2

### Technical Health

- [ ] Continue SVG component extraction — worker body shapes, enemy unit torsos, building base rects are next candidates for shared components (see iter109 pattern)
- [x] Extract blacksmith upgrade costs to shared config constants — `BLACKSMITH_STEEL_EDGE_COSTS` and `BLACKSMITH_IRON_HIDE_COSTS` in `constants.ts`; TechTab consumes them (2026-08-07)
- [ ] Profile render loop on 25×25 map with 30+ units; investigate canvas or OffscreenCanvas fallback if SVG drops below 30fps on mobile
- [ ] Add unit tests for remaining core helpers: `tileDist`, `tileToSvg`, A\* pathfinding (damage formulas ✅ covered in towerHelpers/spawnHelpers; map selectors ✅ covered in mapSelectors tests)

### Gameplay Features

- [ ] **Named formations** — move a selected group in line, wedge, or box formation; prevents units stacking on the same tile and adds strategic depth to multi-unit control
- [ ] **Enemy hero unit** — Warlord spawns at wave 20+; unique abilities (War Cry, Shield Bash); harder than Warchief, drops rare item
- [ ] **Dropped hero items** — slain enemy elites drop equippable items Barnabas can pick up (Speed Boots, War Banner, Healing Totem); persists between hero deaths
- [x] **Save slots** — 3 cloud-backed save slots (0/1/2) with localStorage fallback via hybrid persistence; slot picker UI on New Game screen still TBD (2026-08-07)
- [ ] **Challenge / achievement system** — unlock badges for milestone runs (e.g., "Survive 20 waves without losing a building", "Kill 5 Sappers before they explode")
- [ ] **Campaign mode (Phase 1)** — linear sequence of 3 hand-crafted scenarios with scripted objectives beyond simple "defend the barn"

### Content & Polish

- [ ] Background ambient audio loop (farm sounds, wind, distant battle) with independent volume slider
- [ ] More unit voice lines and enemy audio cues (Warchief stomp roar, Sapper countdown tick)
- [ ] Minimap: show dropped hero items and loot crate positions
- [ ] Ensure farmers always render in front of barn and remain selectable when barn is clicked
- [ ] **Post-game replay** — new idea (2026-08-28): the high-score leaderboard already records wave/kills/gold/result; if the save system additionally snapshotted key events (wave starts, hero deaths, boss spawns) rather than just final state, the game-over screen could offer a lightweight timeline scrub of "how the run went" without a full deterministic replay engine.
- [ ] **Adaptive difficulty nudge** — new idea (2026-08-28): Easy/Normal/Hard are fixed presets chosen once at game start; track win/loss and wave-reached across runs (already have the leaderboard for this) and suggest a difficulty adjustment on the New Game screen rather than requiring the player to self-assess.

## 2026 Q4: Product and Content Surface

- [ ] Improve the product gallery and catalog surface.
- [ ] Add a blog or news publishing path.
- [ ] Ship ecommerce phase 1.
- [ ] Evaluate subscription or recurring-order follow-ons.
- [ ] Harden accessibility and SEO for a broader launch.

## Legacy Tycoon Tasks (on hold)

- [ ] Finish the animal needs loop (hunger, thirst, happiness lifecycle).
- [ ] Finish feeding mechanics and inventory interactions.
- [ ] Finish fence placement and terrain editing workflows.
- [ ] Add save/load state and building expansion follow-on work.
- [ ] Validate the full gameplay loop end-to-end in Docker (start game → build → feed animals → save → reload).
