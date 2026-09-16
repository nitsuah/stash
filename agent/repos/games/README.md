# Games Collection

> Browser arcade collection built with Next.js, Three.js, and React Three Fiber. Nine games are live at [nitsuah-arcade.netlify.app](https://nitsuah-arcade.netlify.app); the current work is release-path reliability and runtime cleanup.

[![CI](https://github.com/nitsuah/games/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/nitsuah/games/actions)
[![Netlify Status](https://api.netlify.com/api/v1/badges/25a0a90d-195b-4e53-9d94-9a4107321939/deploy-status)](https://app.netlify.com/projects/nitsuah-arcade/deploys)

## 🎮 Games

### 🎯 Asteroid Space Shooter

**Status**: ✅ Complete | **Playable**: `/asteroid`

- **Controls**: `W A S D` to move, Mouse to aim, Click to shoot
- **Weapons**: Press 1/2/3 to switch (Spread/Laser/Explosive), R to reload
- **Power-ups**: Health (green), Shield (blue), Invincibility (yellow), Rapid Fire (red), Slow Motion (purple), Speed Boost (orange)
- **Features**: Wave system, multiple weapon types, power-up system, high score tracking
- **Goal**: Destroy targets, survive waves, achieve high score

### 🎮 FPS Tank Commander

**Status**: ✅ Complete | **Playable**: `/fps`

- **Controls**: `W A S D` to move, Mouse to aim/shoot, Shift for speed boost
- **Features**: First-person shooter, destructible targets, power-ups, dynamic terrain, health system
- **Physics**: Tokyo drift inertia, realistic projectile ballistics
- **Goal**: Destroy targets, survive, collect power-ups

### 🧱 Breakout Classic

**Status**: ✅ Complete | **Playable**: `/breakout`

- **Controls**: Mouse to move paddle, Click to launch ball, Space to restart
- **Features**: Classic brick-breaking gameplay, power-ups, score tracking, lives system
- **Mechanics**: Wave management, brick patterns, paddle physics
- **Goal**: Clear all bricks, progress through waves, set high scores

### 🐦 Flappy Bird

**Status**: ✅ Complete | **Playable**: `/flappy`

- **Controls**: Spacebar/Click to flap
- **Features**: Procedural pipe generation, high score tracking, smooth animations
- **Mechanics**: Physics-based flight, collision detection, endless gameplay
- **Goal**: Survive as long as possible, avoid pipes, set high scores

### 🏓 Pong

**Status**: ✅ Complete | **Playable**: `/pong`

- **Controls**: Arrow keys or Mouse to move paddle
- **Features**: AI opponent with adjustable difficulty, score tracking, classic arcade feel
- **Mechanics**: Ball physics with paddle spin, progressive difficulty
- **Goal**: First to 11 points wins

### 🐍 Snake

**Status**: ✅ Complete | **Playable**: `/snake`

- **Controls**: Arrow keys to change direction
- **Features**: Classic snake mechanics, high score tracking, progressive difficulty
- **Mechanics**: Grid-based movement, growth system, collision detection
- **Goal**: Eat food, grow longer, avoid walls and self

### 👾 Space Invaders

**Status**: ✅ Complete | **Playable**: `/space-invaders`

- **Controls**: Arrow keys to move, Spacebar to shoot
- **Features**: Formation enemies, shields, wave progression, classic arcade gameplay
- **Mechanics**: Enemy patterns, increasing difficulty, defensive shields
- **Goal**: Destroy all enemies, survive waves, achieve high score

### 🧠 Memory Match

**Status**: ✅ Complete | **Playable**: `/memory-match`

- **Controls**: Click/tap a card to flip it, or focus it and press Enter/Space
- **Features**: 8 pairs of fruit symbols (16 cards), shuffle on restart, win detection, keyboard-accessible cards with ARIA labels
- **Mechanics**: Card-flip matching with timed reveal of non-matching pairs
- **Rendering**: Standalone sandboxed HTML5 game (not a React/Three.js game like the others), embedded via iframe
- **Goal**: Match all 8 pairs to win

### ⬛ Dodge Blocks

**Status**: ✅ Complete | **Playable**: `/dodge-blocks`

- **Controls**: Arrow Left / Arrow Right to move the paddle
- **Features**: Randomly-sized falling blocks, score counter, game-over screen
- **Mechanics**: Score increments each frame while alive; block speed varies randomly
- **Rendering**: Standalone sandboxed vanilla JS + HTML Canvas game (not a React/Three.js game like the others), embedded via iframe
- **Goal**: Survive as long as possible and maximize score

## 🛠️ Development

### Quick Start

```sh
cd app
npm install
npm run dev
```

Open `http://localhost:3000`

### Deployment & Hosting

This project is currently deployed as a **Next.js runtime build on Netlify**, not a static export.

- **Local Production Check**: Use `npm run build && npm start` from `app/` to verify the current runtime deployment path locally.
- **Hosting Provider**: `netlify.toml` uses `@netlify/plugin-nextjs`, publishes `.next`, and pins Node 22 for the deployed build.
- **CI Model**: GitHub Actions validates tests, build, E2E, Lighthouse, and Docker smoke checks; production deployment is handled by Netlify.

### Key Commands

- `npm run dev` - Start development server
- `npm run build` - Build the Next.js app for production
- `npm run start` - Start the Next.js production server locally
- `npm test` - Run unit tests
- `npm run test:e2e` - Run E2E tests with Playwright
- `npm run lint` - Check code quality

#### Docker-based Test & Coverage

To run all unit tests and collect coverage in Docker:

```sh
docker build --target test-unit -t games-test .
docker run --rm -it games-test npm run test:coverage
```

#### Docker-based E2E Tests

To run all Playwright E2E tests in Docker:

```sh
docker build --target test-e2e -t games-test-e2e .
docker run --rm -it games-test-e2e npm run test:e2e
```

This uses a Debian-based Node image to support Playwright browser dependencies. All E2E tests should pass in the container.

### Requirements

- Node.js v22.21.0 (native Windows)
- npm 10.9.4
- Modern browser with WebGL support

### Project Structure

```bash
app/
├── pages/           # Next.js pages
│   ├── asteroid.jsx      # Asteroid space shooter
│   ├── fps.jsx          # FPS tank game
│   ├── breakout.jsx     # Breakout brick breaker
│   ├── flappy.tsx       # Flappy bird clone
│   ├── pong.tsx         # Pong with AI
│   ├── snake.tsx        # Classic snake
│   ├── space-invaders.tsx # Space invaders
│   ├── memory-match.jsx  # Memory card match (embeds public/games/memory-match via iframe)
│   └── dodge-blocks.jsx  # Dodge falling blocks (embeds public/games/dodge-blocks via iframe)
├── lib/             # Game-specific logic
│   ├── asteroid/    # Asteroid game code
│   ├── fps/         # FPS game code
│   ├── breakout/    # Breakout game code
│   ├── flappy/      # Flappy game code
│   ├── pong/        # Pong game code
│   ├── snake/       # Snake game code
│   ├── space-invaders/ # Space invaders code
│   └── shared/      # Shared systems (physics, audio, UI)
├── public/games/    # Standalone HTML5 games, sandboxed via iframe
│   ├── memory-match/    # Memory Match (vanilla JS)
│   └── dodge-blocks/    # Dodge Blocks (vanilla JS; a stray duplicate also exists at repo-root games/, unused at runtime)
├── _components/     # Global effects and reusable components
├── e2e/             # E2E tests (Playwright)
└── scripts/         # Build/test scripts
```

## 📊 Testing & Quality

- **Unit Tests**: 482 passing across 35 suites (Jest)
- **E2E Tests**: Full game flow coverage (Playwright)
- **Test Coverage**: Core game logic covered
- **CI/CD**: GitHub Actions (type-check, test, E2E, Lighthouse audits)
- **Code Quality**: ESLint + Prettier, pre-commit hooks

## 📚 Architecture and Interfaces

- `ARCHITECTURE.md` documents runtime layers, ownership boundaries, and extension guidance.
- `API.md` captures the current no-external-API decision and existing interface surface.

## 📈 Current Status

**Version**: Live arcade foundation shipped; release-path cleanup remains active.

### Recent Milestones

- ✅ All 9 games fully playable (7 React/Three.js games, plus Memory Match and Dodge Blocks as sandboxed HTML5 embeds); Memory Match and Dodge Blocks have unit/E2E tests pending (see TASKS.md)
- ✅ Code quality improvements (TypeScript types, documentation)
- ✅ Performance optimizations (game loops, physics)
- ✅ Comprehensive test coverage (482 unit tests, ~95% statement coverage)
- ✅ E2E testing for all game flows
- ✅ Accessibility improvements (keyboard navigation, ARIA labels)
- ✅ Asteroid audio startup race fixed (`bgm` readiness-gated on route init)
- ✅ Game page UI polish — neon buttons, page titles, back navigation on all game routes; CSP iframe fix

### Active Development

- 📝 Documentation updates and consolidation
- 🔧 Tech debt management (see CONTRIBUTING.md for current guidelines; TECH_DEBT.md retained for legacy reference)
- 🎨 Performance monitoring and optimization
- 🚀 Continuous deployment to Netlify

## 🛡️ Security & Dependencies

### Dependency Pinning
All security overrides in `app/package.json` are pinned to **exact versions** rather than ranges. This ensures:
1. **Reproducibility**: CI/CD and local environments use identical versions.
2. **Security**: Prevents automatic upgrades to major versions that might introduce breaking changes or new vulnerabilities.

### Active Overrides
- **qs (6.15.2)**: Fixed High-severity `arrayLimit` bypass and DoS vulnerabilities.
- **lodash (4.18.1)**: Fixed Prototype Pollution vulnerability.
- **tmp (0.2.7)**: Tightened to exact version for environment stability.

## 🔧 Technical Stack

- **Framework**: Next.js 16.3.3
- **3D Graphics**: Three.js 0.185.1, React Three Fiber 9.7.0
- **Physics**: @react-three/cannon 6.6.0
- **Styling**: Styled Components 6.5.3
- **Animation**: GSAP 3.15.0
- **Testing**: Jest 30.5.0, Playwright 1.62.1
- **Build Tools**: ESLint 9.39.2, Prettier 3.9.6

_(Versions above are the resolved versions in `app/package-lock.json`;
Dependabot keeps these current, so check that file if this drifts again.)_

---

Built with ❤️ using Next.js, Three.js, React Three Fiber

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
