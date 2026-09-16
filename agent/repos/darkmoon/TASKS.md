# Tasks

Last Updated: 2026-08-27

## In Progress

## Done

- [x] Fix `.husky/pre-push` silently validating a stale Docker test image.
  - Completed: 2026-09-11
  - Evidence: `docker compose run` (without `--build`) reuses an already-built
    `darkmoon-test:latest` image regardless of whether the Dockerfile/source/
    dependencies changed since it was built. Caught this when the hook reported
    "vitest v4.1.11, 80 files/665 tests" on a push, while a freshly-built image
    of the identical commit correctly reported "vitest v5.0.0, 81 files/673
    tests" (matching package-lock.json's pinned vitest@5.0.0) — the cached
    image dated back to 2026-09-10, a day before the pushed commit even
    existed, so pre-push had been silently validating old code, not what was
    actually being pushed. Added `--build` to both the real and the
    Docker-missing-fallback command in `.husky/pre-push`, so the image is
    rebuilt (fast via Docker's own layer cache when nothing changed) before
    every push. Verified: same command now reports vitest 5.0.0 and 673/673
    tests for the current commit.

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

- [x] **[Phase A] Pluggable game modes** — extract tag logic out of `GameManager` behind a `GameModeHandler` interface (`onStart`/`onTick`/`onAction`/`onPlayerRemoved`/`onEnd`), with a `TagMode` implementation preserving current behavior.
  - Done: `src/components/gameModes/{GameModeHandler,TagMode}.ts`; `GameManager` is now a thin host delegating to the active mode. Existing `gameManager.*.test.ts` and `Bots.test.tsx` pass unchanged.

- [x] **[Phase B] Combat primitives** — `WeaponManager`, projectile/hit-detection, `health`/`respawn` on `Player`, full vertical slice in Solo mode.
  - Done: all primitives plus full combat-feel polish (Phases BG–BM):
    - BG: bot shot tracer effects (visual streaks for every bot shot)
    - BH: per-weapon ammo + reload system (laser auto-reload, R-key manual reload, reload bar HUD, `WeaponManager.startReload/isReloading/getReloadProgress`)
    - BI: bot LOS wall check (`CollisionSystem.hasLineOfSight`, bots can't fire through obstacles)
    - BJ: bot angular spread (2D rotation-matrix deviation so misses fly to a visible off-target point)
    - BK: smooth player movement (velocity scalar lerp — 10×/s accel, 15×/s decel)
    - BL: player reticle + mouse-aimed firing (ground-plane raycast, CSS crosshair) — PR #321
    - BM: shooting gallery mode + crosshair + bot tracer improvements

- [x] **[Phase C] Deathmatch mode** — kill tracking, respawn, and scoreboard via `GameUI`.
  - Done: `DeathmatchMode`, kill-limit win condition, respawn timer, bot combat AI, health/kill HUD; see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase C.

- [x] **[Phase D] Capture the Flag mode** — teams, flag entities, and capture zones.
  - Done: `CTFMode`, team assignment, flag pickup/carry/capture/drop-on-death, bot CTF AI, CTF combat, team HUD; see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase D.

- [x] **[Phase E partial] HUD polish + code quality** — Phase E polish items completed in PR #391:
  - Done: Homepage redesign (glassmorphism cards, feature/roadmap sections, mobile CTA, favicon); ShotgunVFX cone particle effect; reserve ammo system; tag-mode health/damage; reload precision meter v2 (snap mechanic); weapon swap key bindings (Tab/Q/E + GAMEPLAY_KEYS constant); scoreboard rebind to [I]; camera-relative A/D strafing fix; Crosshair GPU-composited positioning (transform instead of top/left); tensionWarning useMemo; crosshair spread setInterval; scoreboard blur reset; GameUI type safety improvements.
  - Completed: 2026-08-07

- [x] **GameUI monolith componentization** — `GameUI.tsx` (2,078 lines) split into 15 sub-components and a dedicated `useGameUIState.ts` hook; barrel re-export preserves all consumer imports unchanged.
  - Done: `src/components/GameUI/components/` (DamageFlash, HitDirectionIndicator, KillAnnouncement, PickupToast, ScoreBoard, KillFeed, MinimapRadar, Crosshair, BottomHUD, DeathScreen, StreakAnnouncement, BonusRoundOverlay, GameStatusPanel, GameResultsScreen, GameLobbyPanel) + `src/components/GameUI/hooks/useGameUIState.ts`
  - Completed: 2026-08-04

- [x] **Solo.tsx modular refactor** — Solo.tsx (previously ~1,002 lines) extracted into focused hooks: `useGameStart`, `useBotPositionHandlers`, `useDebugModes` (botDebugMode, galleryDebugMode, autoRestart).
  - Completed: 2026-08-04

## Todo

- [x] Stabilize mobile input and mobile layout on physical devices.
  - Priority: P0
  - Completed: Browser emulation suggests core controls (joysticks, buttons, touch camera) are functional. Minor UI adjustments remain (e.g., Home screen card layout) but are deferred to broader UI/UX tasks.

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

- [x] Fix the Docker production build path.
  - Priority: P0
  - Evidence: Verified `docker build --target runner -t darkmoon-prod .` succeeds.

- [x] Align product messaging with the deployed experience.
  - Priority: P0
  - Completed: 2026-08-21
  - Evidence: README.md clearly states "Solo mode is the only live experience; multiplayer is not yet available." FEATURES.md uses `[planned]` for Multiplayer Tag and `[in-progress]` for mobile. Messaging is accurate.

- [x] Add architecture and deployment contract documentation.
  - Priority: P1
  - Completed: 2026-08-21
  - Evidence: `docs/ARCHITECTURE.md` covers app boundaries, solo vs. multiplayer split, Docker/Netlify deployment, and health/socket contracts. `docs/API.md` documents HTTP endpoints and WebSocket events. Both files exist and are referenced from README.md.

- [ ] Refresh `METRICS.md` with measured values instead of estimates.
  - Priority: P1
  - Problem: current metrics are still estimate-heavy.
  - Acceptance Criteria: build, test, and coverage values are measured or clearly marked `TBD` with blockers.

- [x] Finish server production-hardening work beyond the current baseline.
  - Priority: P1
  - Completed: 2026-08-27
  - Evidence: `docs/MULTIPLAYER_GATE.md` defines the four readiness criteria
    (deployment, CORS, logging, observability) each with a runnable acceptance
    check, and the repo passes all four. New modules `server/logger.js`
    (structured JSON logging + game event catalogue), `server/cors.js` (shared
    HTTP/WebSocket allow-list), `server/health.js` (`/health` payload),
    `server/port.js` (`PORT` validation), and `server/tagAuthorization.js`
    (pure `player-tagged` authorization decision — impersonation/self-tag/
    unknown-player rejection), plus SIGTERM graceful shutdown in
    `server/index.js`. Covered by 96 new tests across
    `src/__tests__/server.{logger,cors,health,port,tagAuthorization}.test.ts`.
    Full suite (`docker build --target test -t darkmoon:test .` then
    `docker run --rm darkmoon:test`, which runs `npm run test:run` →
    `vitest run --config ./config/vitest.config.ts --configLoader runner`;
    scope excludes only `e2e/**`, matching the 79-file/5-skipped figures
    above): 79 files, 654 passed / 5 skipped; typecheck and lint clean.
  - Note: fixed several latent bugs found while validating — the SPA fallback
    was mounted before the API router (so `/health` returned `index.html` for
    any `Accept: */*` request, including the Docker healthcheck and Render
    probe); the CORS wildcard matcher did not escape regex metacharacters (so
    `darkmoon-dev.netlify.app` also matched look-alike hosts); a bare
    `ALLOWED_ORIGINS=*` combined with `credentials: true` would have reflected
    every origin (CWE-942), so `parseAllowedOrigins` now drops a literal `*`
    entry; the origin wildcard expanded to `.*` (cross-label) instead of
    `[^.]*` (single-label), so a deploy-preview pattern could absorb extra
    attacker-controlled subdomains spliced into the wildcard slot;
    `/health`'s `maxPlayers` was not validated, so `NaN`/negative/
    non-integer values could serialize as `null` or pin the server to
    `degraded` forever; an unset/invalid `PORT` reached `app.listen(NaN)` with
    no diagnostic; and the `player-tagged` handler trusted a client-supplied
    `taggerId`, letting any connected client impersonate the current IT player.

- [ ] Re-baseline the remaining large-file refactor work.
  - Priority: P2
  - Problem: older refactor tasks no longer match the codebase hotspots.
  - Acceptance Criteria: only current, high-value refactors remain and each one ties back to reliability, testability, or performance.

- [x] **[Phase BM] Grenade hold-to-throw + trajectory arc** — hold LMB to charge, release to throw; dotted arc previews the parabolic landing zone.
  - Priority: P2
  - Completed: 2026-08-21
  - Evidence: `src/components/world/GrenadeProjectiles.tsx` implements parabolic projectile physics (gravity + launch angle); `src/components/world/vfx/TrajectoryArc.tsx` renders the charge-progress arc with color shift; `PlayerWeapon.tsx` wires the hold/release mechanic. FEATURES.md lists this as `[shipped]`.

- [ ] **[Phase E remaining] Over-the-shoulder aim camera + combat music** — remaining Phase E items after PR #391 landed most of the polish pass.
  - Priority: P2
  - Note: HUD, ammo, reload bar, kill feed, damage numbers, hit marker, ShotgunVFX, reserve ammo, tag-mode health, reload snap mechanic, homepage redesign, and GameUI/Solo componentization are all done. Remaining: over-the-shoulder aim-mode camera offset and a combat music layer that cross-fades when shooting/hit events occur.
  - Acceptance Criteria: see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase E "Remaining" section.

- [ ] Fix server-side multiplayer tag parity before Multiplayer Tag ships.
  - Priority: P1
  - Problem: `server/index.js`'s `player-tagged` handler has no cooldown/freeze enforcement, and its `disconnect` handler doesn't reassign or clear `itPlayerId` if the IT player disconnects.
  - Note (2026-08-27): the client-supplied tagger/tagged ID trust issue is fixed — `taggerId` is now bound to `client.id`, self-tags are rejected, and the broadcast payload always carries the authenticated IDs rather than whatever the client sent. Cooldown/freeze enforcement and IT-disconnect handoff remain open.
  - Acceptance Criteria: see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` "Server-side tag parity"; must be resolved before Multiplayer Tag moves out of `[planned]` in `FEATURES.md`.

## See also: docs/INSTRUCTIONS.md for agent handoff and workflow best practices.

- The deployed site presents solo mode as live and multiplayer or tournament work as planned.
