# Architecture

Last Updated: 2026-03-28

## Purpose

This document defines the runtime architecture of the arcade platform in `games/app` and how major systems are composed.

## System Overview

The project is a Next.js runtime application that hosts multiple game routes. Each game route mounts a focused game module while sharing platform-level services for settings, audio, and reusable UI behavior.

Core architectural layers:

1. Route Layer (`pages/`)
- Responsible for route entry, provider composition, and high-level page wiring.

2. Game Feature Layer (`lib/<game>/`)
- Implements game-specific state, mechanics, rendering logic, and domain rules.

3. Shared Platform Layer (`lib/shared/`, `contexts/`, `utils/`, `_components/`)
- Provides reusable audio systems, UX helpers, effects, and cross-route state containers.

4. Quality and Tooling Layer (`tests/`, `e2e/`, scripts, CI workflows)
- Validates correctness, regressions, and release-path behavior.

## Runtime Composition

Typical route composition:

1. Route page mounts provider boundary (for example settings and audio providers).
2. Route loads major game modules dynamically where appropriate to reduce server bundle and startup overhead.
3. Game module orchestrates game-loop state, collision/events, and platform services.
4. Shared systems handle cross-cutting concerns (audio, settings, overlays, persistence utilities).

## Key Modules and Responsibilities

- `pages/`
  - Route entrypoints and route-level composition.

- `lib/asteroid/`, `lib/fps/`, `lib/breakout/`, `lib/flappy/`, `lib/pong/`, `lib/snake/`, `lib/space-invaders/`
  - Game domain logic and route-specific behavior.

- `lib/shared/`
  - Shared gameplay and UI subsystems.

- `contexts/`
  - React context providers for shared route state (for example audio/settings toggles).

- `utils/`
  - Utility helpers for persistence, timing, audio helpers, and low-level behavior.

- `_components/`
  - Reusable visual/effects primitives used by multiple route modules.

## State and Data Flow

The primary data flow is client-side and event-driven:

1. Input events (mouse/keyboard/touch) are captured by route/game modules.
2. Game state is updated through React state and refs within game modules.
3. Shared context state (audio/settings) influences game behavior.
4. UI overlays and indicators render from derived state.
5. Persistent local values (for example scores/settings) are written to browser storage where applicable.

No persistent server-side game-state API is currently used by this repository.

## Audio Architecture

Audio is handled on the client via shared hooks/context and game-specific triggers:

- A shared audio hook/provider pair loads and registers route audio assets.
- Game modules call shared sound functions for SFX and music transitions.
- Readiness gating is used for startup-sensitive playback paths to avoid race conditions during initial route load.

## Deployment and Operations Model

- Application model: Next.js runtime deployment.
- Hosting model: Netlify runtime deployment.
- Local and CI reliability checks include Docker smoke validation.

## Quality Boundaries

- Unit tests cover reusable logic and behavior-critical modules.
- E2E tests validate playable route behavior and game flow.
- CI gates include type-checking, tests, build, and container smoke checks.

## Extension Guidelines

When adding a new game route:

1. Add a route entry in `pages/` with provider composition consistent with existing routes.
2. Keep game logic within a dedicated `lib/<game>/` tree.
3. Reuse shared systems before introducing new cross-route abstractions.
4. Add/extend tests at unit and E2E levels.
5. Update `README.md`, `FEATURES.md`, and this architecture document if boundaries change.