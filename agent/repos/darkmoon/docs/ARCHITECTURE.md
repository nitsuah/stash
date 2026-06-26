# Darkmoon Architecture

## Overview

Darkmoon is a solo-first 3D browser game built with React 19, Three Fiber, Vite, Express, and Socket.io. The architecture supports both solo and future multiplayer modes.

## Components

- **Frontend**: Vite + React 19 + Three Fiber (src/)
- **Server**: Express + Socket.io (server/)
- **Build Tooling**: Vite, Vitest, ESLint, Prettier
- **Deployment**: Docker, Netlify

## App Boundaries

- **Solo Mode**: All gameplay logic and AI run client-side, with server for health and future multiplayer.
- **Multiplayer (Planned)**: WebSocket server (Socket.io) for real-time sync, validation, and room management.

## Deployment

- **Docker**: Multi-stage build for production. See Dockerfile and README for details.
- **Netlify**: Static site deployment for frontend only (solo mode).

## Health/Socket Contracts

- **/health**: HTTP GET returns 200 OK if server is running.
- **WebSocket**: Socket.io events for multiplayer (planned), not active in solo mode.

## Related
- [[repos/darkmoon/docs/archive/ARCHITECTURE_IMPROVEMENTS|Architecture Improvements]] — actionable improvement plan
- [[repos/darkmoon/docs/archive/L7_ENGINEERING_REVIEW|L7 Engineering Review]] — source analysis
