# API and Interfaces

Last Updated: 2026-03-28

## Scope

This repository does not currently expose a public HTTP API surface for game operations.

Current behavior:

- No `pages/api` routes are defined.
- Runtime behavior is delivered through browser routes and client-side modules.
- Game state and interactions are handled client-side.

## External Interface Model

External interfaces that do exist today:

1. Browser routes
- `/`
- `/asteroid`
- `/fps`
- `/breakout`
- `/flappy`
- `/pong`
- `/snake`
- `/space-invaders`

2. Frontend runtime contracts
- Route components consume shared context providers for settings/audio.
- Game modules interact with shared utility modules for sound, state helpers, and UI effects.

3. Build and deployment interfaces
- Next.js runtime build commands in `app/package.json`.
- Netlify runtime deployment configuration in `netlify.toml`.
- Docker smoke validation workflows in `.github/workflows`.

## Internal Interface Conventions

The project follows these internal interface rules:

1. Keep game-specific interfaces under `lib/<game>/`.
2. Keep shared cross-game interfaces under `lib/shared/`, `contexts/`, or `utils/`.
3. Prefer explicit prop contracts for route/game component boundaries.
4. Keep cross-route shared state centralized in providers/hooks rather than global mutable state.

## Out of Scope

Not currently supported in this repository:

- Public REST API
- GraphQL endpoint
- Server-side persistence API for user progress
- Authenticated backend service contracts

## Decision Record

Decision: no external API is maintained in this codebase at this time.

Rationale:

- The product is currently a browser-playable arcade with client-driven game loops.
- Stabilization work is focused on runtime reliability, deployment consistency, and route behavior.
- Introducing backend API contracts would add operational and security surface area before platform reliability goals are complete.

Future trigger for API introduction:

- Add an API decision update if features require server persistence, multiplayer/session state, or authenticated user profiles.