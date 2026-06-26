# Games Collection Features

Status guide: all game entries below are `[shipped]` unless otherwise noted. Planned platform work is called out inline.

## 🎮 Arcade Games

### 🚀 Asteroid Space Shooter

- **6DOF Movement**: Full freedom of movement in 3D space with W/A/S/D controls
- **Multiple Weapon Types**: Three weapon systems - Spread Shot, Laser Beam, and Explosive Rounds (switch with 1/2/3 keys)
- **Power-Up System**: Six power-up types including Health, Shield, Invincibility, Rapid Fire, Slow Motion, and Speed Boost
- **Wave System**: Progressive difficulty with increasing enemy counts and spawn rates
- **High Score Tracking**: LocalStorage-based score persistence across sessions
- **Physics-Based Combat**: Realistic projectile ballistics and collision detection

### 🎯 FPS Tank Commander

- **First-Person Shooter**: Immersive FPS perspective with mouse-aim controls
- **Tokyo Drift Physics**: Inertia-based movement system for realistic tank handling
- **Destructible Targets**: Dynamic target spawning with health systems
- **Speed Boost**: Shift key for temporary speed increase
- **Power-Up Collection**: Health, shield, and weapon upgrades
- **Dynamic Terrain**: 3D terrain navigation with collision detection

### 🧱 Breakout Classic

- **Classic Brick Breaking**: Traditional Breakout gameplay with paddle and ball physics
- **Power-Up System**: Various power-ups that drop from broken bricks
- **Wave Progression**: Multiple brick patterns with increasing difficulty
- **Lives System**: Three-life gameplay with game over conditions
- **Score Tracking**: Points system with high score persistence
- **Paddle Physics**: Ball angle depends on paddle impact location

### 🐦 Flappy Bird

- **One-Button Control**: Simple spacebar/click to flap mechanics
- **Procedural Generation**: Infinite pipe generation with random gaps
- **Physics Simulation**: Gravity-based flight with momentum
- **High Score System**: Best score tracking across sessions
- **Smooth Animations**: 60 FPS gameplay with smooth bird movement
- **Collision Detection**: Precise pipe and ground collision

### 🏓 Pong

- **AI Opponent**: Adjustable difficulty AI paddle with realistic behavior
- **Classic Mechanics**: Traditional Pong physics with ball acceleration
- **Paddle Spin**: Ball direction influenced by paddle movement
- **Score System**: First to 11 points wins
- **Dual Control Options**: Arrow keys or mouse control
- **Progressive Difficulty**: Ball speed increases throughout match

### 🐍 Snake

- **Classic Snake Gameplay**: Grid-based movement with arrow key controls
- **Growth System**: Snake grows longer with each food consumption
- **Progressive Difficulty**: Speed increases as snake grows
- **High Score Tracking**: Best score persistence
- **Collision Detection**: Wall and self-collision with game over
- **Grid-Based Movement**: Precise tile-by-tile movement

### 👾 Space Invaders

- **Formation Enemies**: Classic Space Invaders enemy patterns and movement
- **Defensive Shields**: Destructible shields for player protection
- **Wave Progression**: Increasing difficulty with faster enemy movement
- **Classic Controls**: Arrow keys to move, spacebar to shoot
- **Score System**: Points for each enemy destroyed
- **Arcade Authenticity**: Faithful recreation of original mechanics

## 🎨 Shared Systems

### 🔧 Physics Engine

- **Collision Detection**: Sphere-sphere collision with elastic response
- **Spatial Partitioning**: Optimized O(n log n) collision detection using spatial grid
- **Projectile Physics**: Realistic ballistic trajectories
- **Collision Response**: Physics-based elastic collision calculations

### 🎭 UI Components

- **ArcadeButton**: Neon-styled interactive buttons with glow effects and hover states
- **ArcadeCard**: Reusable game selection cards with multiple display modes
- **ArcadeHeader**: Scanline-effect title headers with retro CRT aesthetic
- **ArcadeMenu**: Overlay menu system with arcade styling
- **Consistent Design**: Unified neon aesthetic across all games (cyan, magenta, yellow)

### 🔊 Audio System `[shipped with active runtime bug]`

- **Sound Effects**: Comprehensive sound library for game actions (shoot, hit, explosion, power-up)
- **Music Tracks**: Background music for each game
- **Volume Control**: Adjustable sound and music levels
- **Sound Management**: Centralized audio handling with Web Audio API

## 🛠️ Development & Quality

### 📊 Testing Infrastructure

- **Unit Tests**: 218 passing unit tests covering game logic and shared systems
- **E2E Testing**: Playwright tests for complete game flows
- **Code Coverage**: ~85% test coverage with focus on pure logic
- **CI/CD Pipeline**: Automated testing on every push with GitHub Actions
- **Lighthouse Audits**: Performance and accessibility monitoring

### 🚀 Performance Optimization

- **Object Pooling**: Reusable object pools for particles `[planned]`
- **Spatial Partitioning**: Efficient collision detection using grid-based partitioning
- **60 FPS Target**: Optimized game loops maintaining 60 frames per second
- **LOD System**: Level-of-detail system for distant objects `[planned]`
- **Bundle Optimization**: Code splitting and lazy loading strategies

### ♿ Accessibility

- **Keyboard Navigation**: Full keyboard support for all games
- **ARIA Labels**: Semantic HTML with proper ARIA attributes
- **High Contrast**: Clear visual elements with strong color contrast
- **Screen Reader Support**: Basic screen reader compatibility
- **Lighthouse A11y Score**: 100/100 accessibility score

## 🔧 Technical Stack

### 🌐 Framework & Libraries

- **Next.js 15.3.0**: React framework with App Router and server-side rendering
- **Three.js 0.175.0**: 3D graphics library for WebGL rendering
- **React Three Fiber 9.1.2**: React renderer for Three.js with declarative API
- **React Three Cannon 6.6.0**: Physics engine integration for React Three Fiber
- **Styled Components 6.1.17**: CSS-in-JS styling solution
- **GSAP 3.12.2**: Animation library for smooth transitions and effects

### 🧪 Testing & Quality Tools

- **Jest 30.2.0**: JavaScript testing framework with coverage reporting
- **Playwright 1.56.1**: End-to-end testing framework for browser automation
- **ESLint 9.38.0**: JavaScript linter for code quality enforcement
- **Prettier 3.6.2**: Code formatter for consistent style
- **Husky**: Git hooks for pre-commit validation

## 🚀 Deployment & CI/CD

### ⚙️ Build & Deploy

- **Netlify Hosting**: Automated deployments with preview branches
- **GitHub Actions**: CI/CD pipeline with linting, testing, and E2E checks
- **Lighthouse CI**: Automated performance and accessibility audits
- **Preview Deployments**: Automatic preview URLs for pull requests
- **Production Ready**: Live deployment exists, with current release-path cleanup tracked in TASKS.md and ROADMAP.md
