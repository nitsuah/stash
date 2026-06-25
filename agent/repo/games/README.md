# Games Collection

> Browser arcade collection built with Next.js, Three.js, and React Three Fiber. The live routes are shipped; the current work is release-path reliability and runtime cleanup.

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
│   └── space-invaders.tsx # Space invaders
├── lib/             # Game-specific logic
│   ├── asteroid/    # Asteroid game code
│   ├── fps/         # FPS game code
│   ├── breakout/    # Breakout game code
│   ├── flappy/      # Flappy game code
│   ├── pong/        # Pong game code
│   ├── snake/       # Snake game code
│   ├── space-invaders/ # Space invaders code
│   └── shared/      # Shared systems (physics, audio, UI)
├── _components/     # Global effects and reusable components
├── e2e/             # E2E tests (Playwright)
└── scripts/         # Build/test scripts
```

## 📊 Testing & Quality

- **Unit Tests**: 218 passing (Jest)
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

- ✅ All 7 games fully playable and tested
- ✅ Code quality improvements (TypeScript types, documentation)
- ✅ Performance optimizations (game loops, physics)
- ✅ Comprehensive test coverage (218 unit tests)
- ✅ E2E testing for all game flows
- ✅ Accessibility improvements (keyboard navigation, ARIA labels)
- ✅ Asteroid audio startup race fixed (`bgm` readiness-gated on route init)

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
- **lodash (4.17.23)**: Fixed Prototype Pollution vulnerability.
- **tmp (0.2.4)**: Tightened from `^0.2.4` to exact version for environment stability.

## 🔧 Technical Stack

- **Framework**: Next.js 16.1.6
- **3D Graphics**: Three.js 0.182.0, React Three Fiber 9.5.0
- **Physics**: @react-three/cannon 6.6.0
- **Styling**: Styled Components 6.3.9
- **Animation**: GSAP 3.14.2
- **Testing**: Jest 30.2.0, Playwright 1.56.1
- **Build Tools**: ESLint 9.38.0, Prettier 3.6.2

---

Built with ❤️ using Next.js, Three.js, React Three Fiber

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
