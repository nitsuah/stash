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

- **Real-time Multiplayer**: WebSocket-based synchronization with Socket.io (not live)
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
- **Health Checks**: `/health` endpoint for monitoring
- **CORS Configuration**: Environment-based origin allowlist
- **Connection Management**: Graceful disconnect handling
- **Error Recovery**: Automatic reconnection with exponential backoff
