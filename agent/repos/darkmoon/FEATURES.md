# DARKMOON Features

Status guide: `[shipped]` is live today, `[in-progress]` is partially implemented or awaiting validation, and `[planned]` remains roadmap work.

## Game Modes

### 🤖 Solo Mode with AI Bots `[shipped/live]`

- **Bot AI**: Intelligent bots with pathfinding and tagging behavior
- **Configurable Difficulty**: Adjustable bot speed and reaction time
- **Practice Mode**: Play offline to learn mechanics without pressure
- **Bot Coordination**: Multiple bots with independent AI decision-making
- **Symmetrical Player-Bot Tagging**: Players can tag bots and bots tag players through unified `GameManager.tagPlayer` hit-detection; tag cooldowns and freeze logic enforced for both sides

### 🧩 Pluggable Game Mode Architecture `[shipped]`

- **GameModeHandler Interface**: `onStart`/`onTick`/`onAction`/`onPlayerRemoved`/`onEnd` contract decouples mode logic from the `GameManager` host; adding a new mode requires only a new handler implementation
- **TagMode Implementation**: concrete `GameModeHandler` preserving all current tag-game behavior; serves as the reference implementation for future modes (deathmatch, CTF)

### 🎮 Multiplayer Tag `[planned]`

- **Real-time Multiplayer**: WebSocket-based synchronization with Socket.io; solo-first experience is live; multiplayer planned.
- **Lobby System**: Planned for future release
- **Tag Mechanics**: Planned for future release
- **Player Sync**: Planned for future release

## Player Controls

### 🕹️ Desktop Controls

- **WASD Movement**: Smooth character movement with sprint (Shift) support
- **Mouse Camera**: Free-look camera with two-click rotation
- **Sky Cam Toggle**: Switch between third-person and top-down views
- **Jetpack/Jump**: Spacebar for jump and double-jump mechanics
- **Tag Action**: Click to tag nearby players

### 📱 Mobile Controls `[in-progress]`

- **Virtual Joystick**: Touch-based movement control for mobile devices
- **Two-Finger Camera**: Swipe rotation for camera control
- **Mobile Buttons**: Touch-friendly action buttons for jump and tag
- **Responsive UI**: Adapts to portrait and landscape orientations

## Graphics & Rendering

### 🎨 3D Scene

- **React Three Fiber**: Declarative 3D rendering with Three.js
- **Custom Models**: 3D astronaut character models (SpacemanModel)
- **Lighting System**: Dynamic lighting with shadows
- **Collision Detection**: Physics-based collision system for gameplay
- **Performance Optimization**: LOD and culling for smooth 60 FPS

## User Experience

### 🎭 Theme & UI

- **Dark Mode**: System preference detection with manual toggle
- **Responsive Design**: Mobile-first layout that scales to desktop
- **Game HUD**: Real-time player stats, tag status, and connection indicators
- **Landing Page**: Hero section with game mode cards
- **Toast Notifications**: User feedback for connections, tags, and errors

### 🔊 Audio `[planned]`

- **Sound Effects**: Tag sounds, jump sounds, ambient audio
- **Music**: Background music with volume controls

## Combat & Gameplay

### 🔫 Grenade Hold-to-Throw `[shipped]`

- **Phase BM/BN**: Grenade weapon supports hold-to-charge with parabolic trajectory preview arc; throw distance scales with charge duration.
- **Visual Feedback**: Trajectory arc color shifts from green to red based on charge progress.
- **Projectile System**: Handles parabolic physics and explosion on impact.

### 🔫 Shooting Gallery Mode `[shipped]`

- **Phase BM**: standalone target-practice mode with dedicated crosshair overlay and improved bot tracer rendering

### 🎯 Player Reticle & Mouse-Aimed Firing `[shipped]`

- **Phase BL**: ground-plane raycast maps mouse position to a world-space aim target; CSS crosshair follows cursor; all player shots fire toward the aimed point

### 🏃 Smooth Velocity-Based Player Movement `[shipped]`

- **Phase BK**: velocity scalar lerp (10×/s acceleration, 15×/s deceleration) replaces instant movement; gives movement weight and responsiveness

### 🌀 Bot Angular Spread / Miss Physics `[shipped]`

- **Phase BJ**: 2D rotation-matrix deviation applied to bot shots so misses fly to a visible off-target point rather than vanishing silently

### 👁️ Bot Line-of-Sight Wall Checks `[shipped]`

- **Phase BI**: `CollisionSystem.hasLineOfSight` raycast prevents bots from firing through obstacles; bots wait until a clear sight-line exists

### 🔁 Weapon Reload System `[shipped]`

- **Phase BH**: per-weapon ammo limits; laser auto-reloads, all weapons support R-key manual reload; reload progress bar rendered in HUD via `WeaponManager.startReload/isReloading/getReloadProgress`

### ✨ Bot Shot Tracer Beams `[shipped]`

- **Phase BG**: visual streak rendered for every bot projectile, giving players clear feedback on incoming fire direction

### ⚠️ Score Tension Warning `[shipped]`

- **Phase BF**: pulsing alert triggers when the score leader is 1–2 kills from winning, raising match tension in the final moments

### 🦘 Bot Jumping in Deathmatch `[shipped]`

- **Phase BE**: bots execute jumps during combat, making them harder to track and improving AI believability

### 🔴 Hit Direction Indicator `[shipped]`

- **Phase BD**: red arrow rendered at the screen edge in the direction of incoming damage, giving the player spatial awareness of attackers

### 🔄 Auto-Restart After Results Screen `[shipped]`

- **Phase BC**: combat modes (Deathmatch, CTF) automatically restart after a 7-second results screen, keeping sessions flowing without manual input

## Technical Features

### 🔧 Development Tools

- **Hot Module Replacement**: Vite for instant updates during development
- **TypeScript**: Full type safety with strict mode enabled
- **ESLint & Prettier**: Automated code quality and formatting
- **Pre-commit Hooks**: Husky + lint-staged for quality gates
- **Component Testing**: Vitest + React Testing Library
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

### 🚀 Performance

- **Bundle Optimization**: Code splitting and tree-shaking
- **Lazy Loading**: Dynamic imports for routes and assets
- **Compression**: Gzip compression for production builds
- **CDN Delivery**: Netlify edge network for global distribution

### 🔐 Server & Networking

- **WebSocket Server**: Express + Socket.io for real-time communication
- **Health Checks**: `/health` endpoint for monitoring — pure-function payload (`server/health.js`) reports status/uptime/active players/games and degrades to `degraded` (still HTTP 200) at capacity rather than failing
- **CORS Configuration**: Environment-based origin allowlist shared identically between the HTTP app and the Socket.io handshake (`server/cors.js`); wildcard entries are scoped to a single DNS label (rejects cross-label spoofing) and a bare `ALLOWED_ORIGINS=*` is dropped rather than combined with `credentials: true`
- **Structured JSON Logging**: Every server log line is one JSON object (`server/logger.js`) with a stable `event` key; child loggers carry permanent bound fields that a call-site context key cannot silently overwrite
- **Graceful Shutdown**: `SIGTERM` drains connections and exits `0` within 10s, verified against a `server.shutdown` log record — required for zero-downtime deploys on platforms that send `SIGTERM` on scale-down
- **player-tagged Authorization**: the tag-mode socket event binds the acting player to the authenticated socket connection (`client.id`) rather than trusting a client-supplied ID, and rejects self-tags — prevents a connected client from impersonating the current IT player
- **Multiplayer Readiness Gate**: four criteria (deployment, CORS, logging, observability) each with a runnable acceptance check documented in `docs/MULTIPLAYER_GATE.md`; all four pass
- **Connection Management**: Graceful disconnect handling
- **Error Recovery**: Automatic reconnection with exponential backoff
