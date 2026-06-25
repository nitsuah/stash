# DARKMOON.DEV

[![CI](https://github.com/nitsuah/darkmoon/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/darkmoon/actions)
[![Netlify Status](https://api.netlify.com/api/v1/badges/2ae05c81-761a-4d3a-91ac-dcd5980d48d3/deploy-status)](https://app.netlify.com/projects/darkmoon-dev/deploys)

> Solo-live 3D browser tag game built with React 19, Three Fiber, Socket.io, and Vite. **Solo mode is the live experience; multiplayer is planned.**

**Live Demo:** [darkmoon.dev](https://darkmoon.dev)

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md): App boundaries, deployment, and contracts
- [API.md](API.md): HTTP and WebSocket interface reference

## ✨ Features

- `[shipped]` **Solo Mode with AI Bots** — Practice against intelligent bot opponents on the live site.
- `[in-progress]` **Multiplayer 3D Gameplay** — Multiplayer foundations exist, but the deployed experience is still solo-first.
- `[shipped]` **WebSocket Server Foundation** — Socket.io and server validation are in place for future live modes.
- `[in-progress]` **Mobile Support** — Responsive layout and touch controls exist, but device validation is still open.
- `[shipped]` **Modern Tooling** — Vite, Vitest, ESLint, Prettier, TypeScript, and CI are wired into the repo.

## Quick Start

```bash
# Dev server (hot reload via Vite)
docker compose -f config/docker-compose.yml up solo
```

Visit `http://localhost:4444`. **Solo mode is the only live experience; multiplayer is not yet available.**

## Development

All checks run via Docker — no local Node.js required.

```bash
# Run all tests (366 tests, Vitest)
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for code quality standards and deployment tips.

## 📝 License

MIT © 2025 Nitsuah Labs

---

**Inspiration:** [R3F.Multiplayer](https://github.com/juniorxsound/R3F.Multiplayer) by [@juniorxsound](https://github.com/juniorxsound)

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:

- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
