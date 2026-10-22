# LOC Report — darkmoon (2026-10-22)
HEAD: 859e04b9ade44f6cb07bc2e27fac0f3286e88099

Mode: `--report` (dry run, no changes made)
Date: 2026-10-22
Repo: `nitsuah/darkmoon` · Tier: — (not registered in vigil) · Latest commit: 2026-10-21 02:49 -0400
Method: `git clone --depth 1`, `git ls-files`, Grep line counts, Read/awk structural checks. Churn signal **assumed unavailable** (shallow clone).

## Inventory (Phase 0)
- Tracked files: 312 · after exclusions: 278
- Source LOC (ts/tsx/js, incl. tests): ~36,912 across 251 files
- Test LOC: ~16,072 across 102 files — noted here, not ranked. Largest single test: `src/__tests__/useBotAI.test.ts` (863) — below the ~1,500 test-file threshold.
- Excluded: `*.d.ts` shims, `*.md` docs, and build/config output.

## Top 10 code files (non-test)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `server/index.js` | 661 | JS | Express + Socket.IO game server (module-scope state) |
| 2 | `src/pages/Solo/components/ShootingGallery.tsx` | 659 | TSX | Shooting gallery mode scene |
| 3 | `src/pages/Solo/components/Bots.tsx` | 629 | TSX | Bot rendering + behavior glue (single component) |
| 4 | `src/pages/Solo.tsx` | 625 | TSX | Solo mode page / game orchestration |
| 5 | `src/components/characters/useBotAI.ts` | 594 | TS | Bot AI hook (per-frame logic) |
| 6 | `src/components/characters/player/PlayerWeapon.tsx` | 546 | TSX | Player weapon rendering + firing |
| 7 | `src/components/characters/player/PlayerMovement.tsx` | 538 | TSX | Player movement |
| 8 | `src/components/SoundManager.ts` | 507 | TS | Audio manager |
| 9 | `src/components/characters/PlayerCharacter.tsx` | 504 | TSX | Player character composition |
| 10 | `src/components/GameUI/components/GameStatusPanel.tsx` | 446 | TSX | Game status HUD panel |

CSS: none ranked (style smell, not a refactor target).

## Risk rank

- **High — `server/index.js` (661).** Module-scope mutable state (`clients`, `gameState`, `scores`, `rateLimitTrackers`) plus a `ioServer.on("connection")` closure spanning roughly lines 296–640 that registers **six `client.on(...)` handlers** and the score-award logic inline. Mixed concerns: HTTP setup, rate limiting, socket protocol, game state. **No test imports `server/index.js` directly** (search of `src/__tests__/` and `server/`: 0 hits). Helper modules (`cors.js`, `walletAuth.js`, `logger.js`, `tagAuthorization.js`) have `server.*` tests, which mitigates the helpers but not the wiring.
- **High — `src/components/characters/useBotAI.ts` (594).** Per-frame logic in one `useFrame` callback, approx ~430 lines by heuristic (end-line inferred — assumed). Has three test files covering it (incl. `useBotAI.unit.test.tsx`, 560 lines), so the risk is mainly change-cost, not coverage.
- **High — `src/pages/Solo/components/Bots.tsx` (629).** A single `React.FC` body (~617 lines) with 17 hook calls. Two test files reference it. Splitting per bot concern is the cleanest cut.
- **Medium-High — `src/pages/Solo/components/ShootingGallery.tsx` (659).** Large `useFrame` callback (~265 lines by heuristic — assumed) inside the scene component; five test files reference the gallery area.
- **Medium — `src/pages/Solo.tsx` (625).** Orchestration page with a ~164-line `useEffect` and a ~171-line `useAutoRestart({...})` config block. Ten test refs reference Solo overall, so coverage is reasonable.
- **Medium — `PlayerWeapon.tsx` (546), `PlayerMovement.tsx` (538), `PlayerCharacter.tsx` (504).** Component + hook logic together; each already has a few tests. Lower priority.
- **Low — `SoundManager.ts` (507).** Large but single-concern (audio); has unit tests (`SoundManager.unit.test.ts`, `SoundManager.music.test.ts`).

## Refactor opportunities by phase (for a future `--refactor`)

- **server/index.js:** extract the socket connection handlers into `server/sockets/*.js` (one module per event family: join/leave, shooting, scoring) and move score-award and state into `server/state.js`. Keep `index.js` as the composition root that wires `ioServer`. First phase: add a smoke test that boots the server and connects one socket client, so the wiring is covered before any movement.
- **useBotAI.ts:** split the per-frame body into pure steps (`steerBot`, `pickTarget`, `updateTimers`) living in `src/components/characters/bot/*.ts`, which are testable without R3F. Hook keeps the `useFrame` shell.
- **Bots.tsx:** split into `BotList`, `BotBody`, and a `useBotState` hook; keep `Bots.tsx` as the re-export barrel.
- **ShootingGallery.tsx:** lift the `useFrame` body into `useGalleryFrame.ts` next to the existing `useGalleryBot.ts`.
- **Solo.tsx:** move `useAutoRestart` config into `Solo/hooks/` and the mount `useEffect` into a named hook.

## Validation plan (per phase)
- `Dockerfile` and `render.yaml` exist → run inside the container for the server; for the client, run the Vitest suite (`config/vitest.config.ts`) and Playwright smoke (`e2e/smoke.spec.ts`).
- `server/index.js` changes: boot the server, connect two socket clients, verify join/shoot/score events match before and after.
- Bot AI and gallery changes are per-frame rendering → manual QC of a solo round (bot movement, hits, scoring) and multiplayer join, not only CI green.

## Repo summary

| Repo | Top concern | Priority | Notes |
|------|-------------|----------|-------|
| darkmoon | 661-line game server with module-scope state and inline socket handlers, no direct test | High | Tier unregistered (ranks with T2/T3). Client-side hotspots are test-backed |

## Notes
- Deferred: none in this run (report mode only).
- Heuristic function-length figures come from indentation-based declaration gaps and are approximate; flagged as assumed where used.
