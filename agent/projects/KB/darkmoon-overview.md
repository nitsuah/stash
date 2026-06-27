---
name: darkmoon-overview
description: Central synthesis document for the Darkmoon 3D tag game.
metadata:
  type: project
---

# Darkmoon Overview

Darkmoon is a solo-live 3D browser tag game built with modern web technologies, currently deployed as a solo-first experience featuring AI bot opponents.

## Core Pillars

- **3D Web Experience**: Built on [[repos/darkmoon/docs/ARCHITECTURE.md|React Three Fiber]] (R3F).
- **Socket-Based Foundation**: Uses [[repos/darkmoon/docs/API.md|Socket.io]] for real-time communication, providing the infrastructure for planned multiplayer modes.
- **Dockerized Dev/CI**: Employs a strict container-first development lifecycle; all linting, testing, and production builds run within Docker environments.

## Current State & Roadmap

- **Live**: Solo gameplay against AI bots.
- **In-Progress**: Multiplayer 3D gameplay foundation and mobile device validation.
- **Tech Stack**: React 19, Three Fiber, Vite, TypeScript, Vitest.

## Related Resources

- **Source Code**: [[repos/darkmoon/README.md|Darkmoon README]]
- **Architecture**: [[repos/darkmoon/docs/ARCHITECTURE.md|Architecture and App Boundaries]]
- **Multiplayer Plans**: [[repos/darkmoon/docs/MULTIPLAYER_SHOOTER_ROADMAP.md|Multiplayer Shooter Roadmap]]
- **Technical Debt**: [[repos/darkmoon/docs/TECH_DEBT.md|Known Engineering Debt]]
