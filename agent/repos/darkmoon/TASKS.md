# Tasks

Last Updated: 2026-06-11

## In Progress

## Done

- [x] Review debug mode and regular tag logic for edge cases and regressions.
  - Completed: 2026-06-11
  - Evidence: new `src/__tests__/gameManager.edgeCases.test.ts` (8 tests) and a new
    "blocks an immediate IT ping-pong..." case in
    `src/pages/Solo/components/__tests__/Bots.test.tsx` cover tag-back cooldown, freeze
    windows, self-tag rejection, score floor, restart/reset, and last-player-removed
    edge cases. `Bots.tsx`'s debug logging was also migrated to the dev-gated
    `createTagLogger`.

- [x] Diagnose and fix any remaining issues where the bot does not chase the player or where tagging is inconsistent in solo mode.
  - Completed: 2026-06-11
  - Evidence: root cause was a blanket `lastTagTime` cooldown in `GameManager.tagPlayer`
    that blocked a freshly-tagged IT player from tagging _anyone_ for 2s, compounded by
    `useBotAI`'s 2000ms tag-retry gate. Fixed via a scoped `lastTaggedById`-based tag-back
    cooldown (`src/components/GameManager.ts`) and a 200ms `TAG_RETRY_INTERVAL_MS` retry
    loop (`src/components/characters/useBotAI.ts`); covered by 3 new tests in
    `src/__tests__/useBotAI.unit.test.tsx`.

- [x] Ensure all tag cooldowns and freeze logic are respected for both player and bot, and that tag-back is impossible during cooldown.
  - Completed: 2026-06-11
  - Evidence: `GameManager.tagPlayer` now enforces `TAG_BACK_COOLDOWN_MS` (2000ms, scoped
    to the tagger/tagged pair via `lastTaggedById`) and `TAG_FREEZE_MS` (1500ms, blocks
    anyone from re-tagging a just-tagged player), both reset cleanly on
    `startTagGame`/`endGame`. Verified for player and bot — full Docker suite is 378
    passed / 5 skipped, lint (`--max-warnings=0`) and `tsc --noEmit` both clean.

## Todo

- [ ] Stabilize mobile input and mobile layout on physical devices.
  - Priority: P0
  - Problem: mobile touch controls and responsive layout still lack device-level validation.
  - Acceptance Criteria: joystick and camera controls work on iOS Safari and Android Chrome, home and game UI work in portrait and landscape, and regressions are covered.

- [ ] **[Q2-CEO] 21st.dev component integration pass** — replace or augment key game site UI surfaces (lobby, scoreboard, game-over, nav) with 21st.dev components to improve visual quality and interactivity.
  - Priority: P1
  - Problem: current UI is functional but prototype-grade; 21st.dev components can significantly improve look, feel, and animation quality without a full rewrite.
  - Acceptance Criteria: at least lobby, scoreboard, and game-over screens use 21st.dev components; hover states, transitions, and layout quality are demonstrably improved; no regression in game functionality.

- [ ] **[Q2-CEO] UI/UX interactivity improvements** — improve micro-interactions, card layouts, and overall interactivity across the site using 21st.dev patterns.
  - Priority: P1
  - Problem: the site feels static outside of actual gameplay; improving interactivity increases perceived quality and engagement before a player even starts a game.
  - Acceptance Criteria: game cards, stat panels, and navigation have consistent hover/focus states; page transitions are smooth; Lighthouse performance score does not regress.

- [ ] **[Q2-CEO] Open-source safety scrub** — sanitize repository content to remove potentially sensitive, proprietary, or over-specific company and resume details before broader sharing/open sourcing.
  - Priority: P1
  - Problem: historical examples may include details that are too specific for public exposure.
  - Acceptance Criteria: sensitive examples are removed or anonymized; docs are reviewed for proprietary references; a final pass confirms public-share readiness.

- [ ] Fix the Docker production build path.
  - Priority: P0
  - Problem: the documented Docker build path is currently broken.
  - Acceptance Criteria: `.dockerignore` is in place, `docker build` succeeds from repo root, and the run instructions are revalidated.

- [ ] Align product messaging with the deployed experience.
  - Priority: P0
  - Problem: docs still overstate live multiplayer even though solo mode is the live experience.
  - Acceptance Criteria: README.md and FEATURES.md clearly separate playable-now solo work from planned multiplayer work.

- [ ] Add architecture and deployment contract documentation.
  - Priority: P1
  - Problem: the repo ships a Vite frontend plus Express and Socket.io server work without a dedicated architecture or interface reference.
  - Acceptance Criteria: `ARCHITECTURE.md` and `API.md` document app boundaries, socket and health contracts, and deployment expectations.

- [ ] Refresh `METRICS.md` with measured values instead of estimates.
  - Priority: P1
  - Problem: current metrics are still estimate-heavy.
  - Acceptance Criteria: build, test, and coverage values are measured or clearly marked `TBD` with blockers.

- [ ] Finish server production-hardening work beyond the current baseline.
  - Priority: P1
  - Problem: structured logging, graceful shutdown, and operational visibility have not been fully verified.
  - Acceptance Criteria: hardening tasks are documented, implemented, and validated.

- [ ] Re-baseline the remaining large-file refactor work.
  - Priority: P2
  - Problem: older refactor tasks no longer match the codebase hotspots.
  - Acceptance Criteria: only current, high-value refactors remain and each one ties back to reliability, testability, or performance.

- [x] **[Phase A] Pluggable game modes** — extract tag logic out of `GameManager` behind a `GameModeHandler` interface (`onStart`/`onTick`/`onAction`/`onPlayerRemoved`/`onEnd`), with a `TagMode` implementation preserving current behavior.
  - Done: `src/components/gameModes/{GameModeHandler,TagMode}.ts`; `GameManager` is now a thin host delegating to the active mode. Existing `gameManager.*.test.ts` and `Bots.test.tsx` pass unchanged.

- [x] **[Phase B] Combat primitives** — `WeaponManager`, projectile/hit-detection, `health`/`respawn` on `Player`, full vertical slice in Solo mode.
  - Done: all primitives plus full combat-feel polish (Phases BG–BL):
    - BG: bot shot tracer effects (visual streaks for every bot shot)
    - BH: per-weapon ammo + reload system (laser auto-reload, R-key manual reload, reload bar HUD, `WeaponManager.startReload/isReloading/getReloadProgress`)
    - BI: bot LOS wall check (`CollisionSystem.hasLineOfSight`, bots can't fire through obstacles)
    - BJ: bot angular spread (2D rotation-matrix deviation so misses fly to a visible off-target point)
    - BK: smooth player movement (velocity scalar lerp — 10×/s accel, 15×/s decel)
    - BL: player reticle + mouse-aimed firing (ground-plane raycast, CSS crosshair) — PR #321

- [ ] **[Phase BM] Grenade hold-to-throw + trajectory arc** — hold LMB to charge, release to throw; dotted arc previews the parabolic landing zone.
  - Priority: P2
  - Problem: grenade currently fires like a laser (instant, straight-line). Intended mechanic is hold-to-charge + release with a live arc preview.
  - Acceptance Criteria: holding LMB with grenade equipped renders a dotted parabolic arc from player to predicted landing zone; releasing fires along that arc; throw distance scales with hold duration; existing grenade damage/splash radius unchanged.

- [x] **[Phase C] Deathmatch mode** — kill tracking, respawn, and scoreboard via `GameUI`.
  - Done: `DeathmatchMode`, kill-limit win condition, respawn timer, bot combat AI, health/kill HUD; see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase C.

- [x] **[Phase D] Capture the Flag mode** — teams, flag entities, and capture zones.
  - Done: `CTFMode`, team assignment, flag pickup/carry/capture/drop-on-death, bot CTF AI, CTF combat, team HUD; see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase D.

- [ ] **[Phase E] Multiplayer shooter polish** — over-the-shoulder aim camera and combat music cross-fade layer.
  - Priority: P2
  - Note: HUD, ammo, reload bar, kill feed, damage numbers, and hit marker are already done. Remaining: aim-mode camera offset and a combat music layer that cross-fades when shooting/hit events occur.
  - Acceptance Criteria: see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase E.

- [ ] Fix server-side multiplayer tag parity before Multiplayer Tag ships.
  - Priority: P1
  - Problem: `server/index.js`'s `player-tagged` handler has no cooldown/freeze enforcement and trusts client-supplied tagger/tagged IDs, and its `disconnect` handler doesn't reassign or clear `itPlayerId` if the IT player disconnects.
  - Acceptance Criteria: see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` "Server-side tag parity"; must be resolved before Multiplayer Tag moves out of `[planned]` in `FEATURES.md`.

## See also: docs/INSTRUCTIONS.md for agent handoff and workflow best practices.

- Docker-first validation is blocked by the current production build failure.
- The deployed site presents solo mode as live and multiplayer or tournament work as planned.
