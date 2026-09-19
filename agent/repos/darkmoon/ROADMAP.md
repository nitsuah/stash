# Roadmap

Last Updated: 2026-09-03

## 2025 Q4 ✅

> Completed. Browser-game foundation and baseline gameplay infrastructure shipped.

## Beyond Original Scope — Combat Gameplay (Phases BC–BM) ✅

> Significant combat gameplay shipped beyond the original roadmap scope. Phases BC–BM delivered: auto-restart after results screen, hit direction indicator, bot jumping in deathmatch, score tension warning, bot tracer beams, weapon reload system (R key, ammo limits, HUD bar, timing-based precision snap mechanic), bot LOS wall checks, bot angular spread/miss physics, smooth velocity-based player movement, mouse-aimed firing with player reticle, shooting gallery mode with crosshair improvements, ShotgunVFX cone particle effects, reserve ammo system, tag-mode health/damage support, and camera-relative A/D strafing. Deathmatch (Phase C) and CTF (Phase D) modes also shipped. GameUI and Solo.tsx fully componentized (Phase E partial).

## 2026 Q1 ✅ (Completed / Deferred)

- [x] Fix the Docker production build and validate the run path.
- [x] Align README, FEATURES.md, and roadmap language with solo mode as the live experience.
- [ ] Validate mobile controls and responsive layouts on real devices. _(deferred)_

## 2026 Q2 (Deferred)

### CEO Priorities

- [ ] **21st.dev components integration**: leverage 21st.dev component library to enhance the look, feel, and interactivity of the game site — replace or augment existing UI surfaces with higher-quality, more interactive components.
- [ ] **UI/UX polish pass using 21st.dev**: apply improved card layouts, transitions, and interactive states to the game lobby, scoreboard, and game-over screens.
- [ ] **Open-source safety scrub**: remove or anonymize any sensitive, proprietary, or employer-identifying content so the repo can be shared publicly without exposing confidential details.

### Existing Planned Items

- [x] Define the multiplayer readiness gate around deployment, CORS, logging, shutdown behavior, and operational visibility. _(completed 2026-08-27; see `docs/MULTIPLAYER_GATE.md` — all four criteria pass)_
- [x] Add `ARCHITECTURE.md` and `API.md`. _(completed 2026-08-21; `docs/ARCHITECTURE.md` and `docs/API.md` exist)_
- [x] Measured `METRICS.md` refresh. _(completed 2026-08-28: 71.18% statements / 55.85% branches / 76.65% functions / 73.65% lines, 79 test files / 659 cases, measured in Docker post-#418 merge — PR #419)_
- [ ] Re-scope the remaining refactor backlog against the current codebase.

## 2026 Q3 (In Progress)

- [ ] Ship the first validated multiplayer-capable experience after the readiness gate is met. Readiness gate itself is done (all four criteria pass, PR #418); the two gameplay-parity gaps tracked in TASKS.md (tag cooldown/freeze window, IT-player disconnect handoff) are also now fixed server-side — remaining work is a shipped client experience driving the existing socket events.
- [ ] Revisit additional gameplay modes only after the live foundation is stable.
- [ ] **CORS wildcard/allowlist operator doc** — new idea (2026-08-28): the readiness gate work fixed two subtle CORS bugs (a bare `ALLOWED_ORIGINS=*` combined with `credentials:true`, and a wildcard that matched across DNS labels instead of within one) that would be easy for a future deploy to reintroduce by hand-editing `ALLOWED_ORIGINS`. A short "how to safely add an origin" note in `docs/MULTIPLAYER_GATE.md` — with the drop-a-bare-wildcard and single-label-only rules stated plainly — would prevent the next person (or agent) from silently reverting the fix in `.env`.

## 2026 Q4 (Exploratory)

- [ ] Evaluate identity, progression, and social systems.
- [ ] Evaluate broader platform expansion such as native mobile packaging.

## 2027 (Deferred — larger items not cleanly scoped in the 2026-09 docs/bugfix pass)

> During the 2026-09 docs-and-bugfix cycle (branch `v2026/roadmap-and-docs-2026-09`), the
> P0-class gameplay bugs (downed-player movement, grenade charge input, rocket splash in Tag
> mode, mobile camera inversion, desktop double-jump, home page card cutoff) were fixed and
> verified. The items below were either already tracked as deferred CEO priorities or surfaced
> during this pass but are too large/ambiguous to scope safely alongside a bug-fix PR.

- [ ] **21st.dev component integration + UI/UX interactivity pass** — carried over from 2026
      Q2 CEO priorities (still not started); see TASKS.md for acceptance criteria.
- [ ] **Open-source safety scrub** — carried over from 2026 Q2 CEO priorities.
- [ ] **Over-the-shoulder aim camera + combat music layer** — Phase E remaining items; see
      `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase E "Remaining".
- [ ] **Crosshair vs. actual aim point under pointer lock** — investigated during this pass but
      not fixed: the visible reticle (`Crosshair.tsx`) is positioned from raw `mousemove`
      `clientX/clientY`, which the Pointer Lock spec freezes at lock-acquisition time, while
      actual firing always raycasts from screen-center (NDC 0,0) in `PlayerWeapon.tsx`. If the
      player's cursor wasn't already centered when pointer lock engaged, the crosshair can sit
      off from the true aim point for the rest of the session. Needs a design decision (snap the
      reticle to center on lock, or drive it from camera-forward instead of raw mouse position)
      before implementing — flagging rather than guessing blind.
- [ ] **`config/docker-compose.yml` `test` service silently serves stale images** — discovered
      while verifying this pass's fixes: unlike `solo` (bind-mounted), the `test` service has no
      `volumes:` mount, so `docker compose -f config/docker-compose.yml --project-name darkmoon
  run --rm test` (including the `.husky/pre-push` hook itself) reuses whatever
      `darkmoon-test:latest` image already exists locally and does **not** rebuild on source
      changes unless `docker compose -f config/docker-compose.yml --project-name darkmoon build
  test` is run first. On this branch the local image was 41+ hours stale and the pre-push
      hook was silently validating an old commit on every push until this was caught and the
      image rebuilt by hand. Either add a bind mount to `test` like `solo` has, or have
      `.husky/pre-push` run `docker compose -f config/docker-compose.yml --project-name darkmoon
  build test` before `run`.
