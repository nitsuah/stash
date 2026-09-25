---
up: "[[repos/darkmoon]]"
source: https://github.com/nitsuah/darkmoon/blob/main/docs/ROADMAP.md
---

# Roadmap

> 🧭 [darkmoon](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): 2025 Q4 foundation, the beyond-scope combat phases (BC–BM, Deathmatch, CTF),
> and every completed 2026 item (Docker prod build, solo-mode docs alignment, multiplayer readiness gate,
> ARCHITECTURE/API docs, measured METRICS, server-side tag parity, pre-push stale-image fix) were removed from this
> file — see [FEATURES](./FEATURES.md) and [CHANGELOG](./CHANGELOG.md). All open 2026 Q1–Q4 items and the old
> undated "2027 (Deferred)" list were merged into 2027 Q1 below, de-duplicated.

## 2027 Q1 - Multiplayer Launch & Public Polish (Planned)

### Committed

- [ ] **Ship the first validated multiplayer-capable experience** _(carried from 2026 Q3)_ — the readiness gate passes (PR #418) and server-side tag parity is fixed (#448); remaining work is a shipped client experience driving the existing socket events.
- [ ] **Open-source safety scrub** _(carried from 2026 Q2 CEO priorities)_ — remove or anonymize sensitive, proprietary, or employer-identifying content so the repo can be shared publicly.
- [ ] **21st.dev component integration + UI/UX interactivity pass** _(carried from 2026 Q2 CEO priorities)_ — lobby, scoreboard, game-over, and nav surfaces; see TASKS.md for acceptance criteria.
- [ ] **CORS wildcard/allowlist operator doc** _(carried from 2026 Q3)_ — a short "how to safely add an origin" note in [`docs/projects/multi/MULTIPLAYER_GATE.md`](./projects/multi/MULTIPLAYER_GATE.md) stating the drop-a-bare-wildcard and single-label-only rules, so a hand-edited `ALLOWED_ORIGINS` can't silently revert the #418 fixes.
- [ ] **Validate mobile controls and responsive layouts on real devices** _(carried from 2026 Q1; deferred)_ — the #417 overhaul was only verified via browser emulation.

### Needs scoping

- [ ] **Crosshair vs. actual aim point under pointer lock** — the reticle (`Crosshair.tsx`) is positioned from raw `mousemove` `clientX/clientY`, which Pointer Lock freezes at lock time, while firing raycasts from screen-center in `PlayerWeapon.tsx`. Needs a design decision (snap the reticle to center on lock, or drive it from camera-forward) before implementing.
- [ ] **Over-the-shoulder aim camera + combat music layer** — Phase E remaining items; see [`docs/projects/multi/MULTIPLAYER_SHOOTER_ROADMAP.md`](./projects/multi/MULTIPLAYER_SHOOTER_ROADMAP.md) Phase E "Remaining".
- [ ] **Re-scope the remaining refactor backlog** against the current codebase _(carried from 2026 Q2)_.
- [ ] **Additional gameplay modes** — revisit only after the live multiplayer foundation is stable _(carried from 2026 Q3)_.
- [ ] **Identity, progression, and social systems** — evaluation only _(carried from 2026 Q4, exploratory)_.
- [ ] **Native mobile packaging** — evaluation only _(carried from 2026 Q4, exploratory)_.
