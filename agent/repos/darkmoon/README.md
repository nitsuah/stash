---
up: "[[repos/darkmoon]]"
source: https://github.com/nitsuah/darkmoon/blob/main/README.md
---

# DARKMOON.DEV

> 🧭 **darkmoon** · [Features](./docs/FEATURES.md) · [Roadmap](./docs/ROADMAP.md) · [Tasks](./docs/TASKS.md) · [Changelog](./docs/CHANGELOG.md) · [Metrics](./docs/METRICS.md) <!-- nav -->

[![CI](https://github.com/nitsuah/darkmoon/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/darkmoon/actions)
[![Netlify Status](https://api.netlify.com/api/v1/badges/2ae05c81-761a-4d3a-91ac-dcd5980d48d3/deploy-status)](https://app.netlify.com/projects/darkmoon-dev/deploys)

> 3D browser combat game built with React 19, Three Fiber, Socket.io, and Vite. **Solo mode with full combat gameplay is live; multiplayer is planned.**

**Live Demo:** [darkmoon.dev](https://darkmoon.dev)

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md): App boundaries, deployment, and contracts
- [API.md](docs/API.md): HTTP and WebSocket interface reference

## ✨ Features

- `[shipped]` **Combat Gameplay with AI Bots** — Full deathmatch and CTF modes with bot LOS checks, weapon reload system (including timing-based precision snap mechanic), angular spread, bot jumping, tracer beams, hit direction indicators, score tension alerts, and ShotgunVFX cone particle effects.
- `[shipped]` **Shooting Gallery Mode** — Standalone target-practice mode with crosshair and bot tracer improvements.
- `[shipped]` **Mouse-Aimed Firing & Player Reticle** — Ground-plane raycast aiming with GPU-composited CSS crosshair overlay; velocity-based smooth movement with camera-relative A/D strafing.
- `[shipped]` **Pluggable Game Mode Architecture** — `GameModeHandler` interface decouples mode logic; `TagMode` (with health/damage support), `DeathmatchMode`, and `CTFMode` ship as reference implementations.
- `[shipped]` **Modular UI Architecture** — `GameUI` and `Solo.tsx` fully componentized: 15 HUD sub-components, 3 new hooks (`useGameStart`, `useBotPositionHandlers`, `useDebugModes`), and a dedicated `useGameUIState.ts` for all event-driven state.
- `[shipped]` **WebSocket Server Foundation** — Socket.io and server validation are in place for future live modes.
- `[in-progress]` **Multiplayer 3D Gameplay** — Multiplayer foundations exist, but the deployed experience is still solo-first.
- `[in-progress]` **Mobile Support** — Responsive layout and touch controls exist, but device validation is still open.
- `[shipped]` **Modern Tooling** — Vite, Vitest (659 tests), ESLint, Prettier, TypeScript, and CI are wired into the repo.

## Quick Start

```bash
# Dev server (hot reload via Vite)
docker compose -f config/docker-compose.yml up solo
```

Visit `http://localhost:4444`. **Solo mode is the only live experience; multiplayer is not yet available.**

## Development

All checks run via Docker — no local Node.js required.

```bash
# Run all tests (659 tests, Vitest)
docker compose -f config/docker-compose.yml --project-name darkmoon --profile test run --rm test

# Lint
npm run lint:docker

# Production build
docker build --target runner -t darkmoon-prod .
docker run --rm -p 4444:4444 darkmoon-prod
```

**Git hooks** are managed by husky and run Docker automatically:

- **pre-commit**: runs lint-staged via Docker (lint changed files)
- **pre-push**: runs full test suite in Docker

Install hooks after cloning:

```bash
npm install   # triggers husky install via `prepare` script
```

**pre-commit** (optional, adds basic file hygiene on top of husky):

```bash
pip install pre-commit && pre-commit install
```

## Contributing

See [CONTRIBUTING.md](https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md) (org default) for code quality standards and deployment tips.

<!-- docs-index:start -->

## Docs Index

Every doc at the repo root (other than this README) and under `docs/` (the files mirrored into the Obsidian vault), so none of them is orphaned.

- [Darkmoon API Reference](./docs/API.md) — `docs/API.md`
- [Darkmoon Architecture](./docs/ARCHITECTURE.md) — `docs/ARCHITECTURE.md`
- [Changelog](./docs/CHANGELOG.md) — `docs/CHANGELOG.md`
- [DARKMOON Features](./docs/FEATURES.md) — `docs/FEATURES.md`
- [Agent Pickup Instructions](./docs/INSTRUCTIONS.md) — `docs/INSTRUCTIONS.md`
- [Metrics](./docs/METRICS.md) — `docs/METRICS.md`
- [Roadmap](./docs/ROADMAP.md) — `docs/ROADMAP.md`
- [Tasks](./docs/TASKS.md) — `docs/TASKS.md`

**`docs/archive/`**

- [Architecture Improvements - Quick Reference](./docs/archive/ARCHITECTURE_IMPROVEMENTS.md) — `docs/archive/ARCHITECTURE_IMPROVEMENTS.md`
- [Delivery Pipeline Handoff](./docs/archive/HANDOFF-player-tag-fix-20260403.md) — `docs/archive/HANDOFF-player-tag-fix-20260403.md`
- [L7 Engineering Review - Darkmoon](./docs/archive/L7_ENGINEERING_REVIEW.md) — `docs/archive/L7_ENGINEERING_REVIEW.md`
- [DARKMOON Product Roadmap](./docs/archive/ROADMAP_DETAILED.md) — `docs/archive/ROADMAP_DETAILED.md`

**`docs/projects/conkers/`**

- [🐿️ Conker's Bad Fur Day — Open Source Three.js Recreation Guide](./docs/projects/conkers/CONKER_BFD_BUILD_GUIDE.md) — `docs/projects/conkers/CONKER_BFD_BUILD_GUIDE.md`
- [Tech Debt Tracker](./docs/projects/conkers/TECH_DEBT.md) — `docs/projects/conkers/TECH_DEBT.md`

**`docs/projects/multi/`**

- [Multiplayer Readiness Gate](./docs/projects/multi/MULTIPLAYER_GATE.md) — `docs/projects/multi/MULTIPLAYER_GATE.md`
- [Multiplayer Shooter Roadmap — "Robot Conker's Bad Fur Day"](./docs/projects/multi/MULTIPLAYER_SHOOTER_ROADMAP.md) — `docs/projects/multi/MULTIPLAYER_SHOOTER_ROADMAP.md`

<!-- docs-index:end -->

## 📝 License

MIT © 2025 Nitsuah Labs

---

**Inspiration:** [R3F.Multiplayer](https://github.com/juniorxsound/R3F.Multiplayer) by [@juniorxsound](https://github.com/juniorxsound)

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:

- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
