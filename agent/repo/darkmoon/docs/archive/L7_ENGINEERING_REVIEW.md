# L7 Engineering Review - Darkmoon

**Date:** November 23, 2025  
**Reviewer:** L7 Engineering Analysis  
**Repository:** github.com/nitsuah/darkmoon

---

## Executive Summary

Darkmoon is a well-architected real-time multiplayer 3D tag game with solid fundamentals. The codebase demonstrates:

- ✅ **Strong CI/CD pipeline** with comprehensive pre-commit hooks
- ✅ **Good test coverage** across critical paths
- ✅ **Modern tooling** (Vite, React 19, Three.js, TypeScript strict mode)
- ✅ **Clear separation of concerns** between game logic and UI

However, there are **significant opportunities** for improvement in code organization, mobile experience, and scalability that would benefit from systematic refactoring.

### Critical Issues (P0)

1. **Mobile touch controls non-functional** - Joysticks don't respond to touch input (documented in TODO.md)
2. **Solo.tsx is 1002 lines** - Urgently needs decomposition
3. **PlayerCharacter.tsx is 900+ lines** - Complex game loop logic mixed with rendering

### High Priority Issues (P1)

4. **Commented-out Spline integration** in Home.tsx
5. **Duplicate debug logging utilities** across 3+ files
6. **No mobile-specific test coverage**
7. **Server lacks rate limiting and connection validation**

---

## Detailed Analysis

### 1. File Structure & Code Organization

#### 🔴 Critical: Monolithic Components

**Solo.tsx (1,002 lines)**

- **Issues:**
  - Game state management, bot AI coordination, socket handling, UI rendering all in one file
  - Duplicate debug logger implementation (lines 50-89)
  - Bot configs defined inline (lines 90-116) instead of separate config file
  - 20+ useState hooks indicating state management needs refactoring
- **Recommendation:** Extract to:
  ```
  pages/Solo/
    index.tsx (orchestration only, ~150 lines)
    hooks/
      useSoloGame.ts
      useGameBots.ts
      useSocketConnection.ts
    config/
      botConfigs.ts
    components/
      SoloScene.tsx
      SoloHUD.tsx
  ```

**PlayerCharacter.tsx (900 lines)**

- **Issues:**
  - Movement logic, collision detection, camera controls, tag detection, jetpack physics all intertwined
  - useFrame hook with 300+ lines of game loop logic
  - Difficult to test individual behaviors in isolation
- **Recommendation:** Extract to:
  ```
  characters/PlayerCharacter/
    index.tsx (rendering wrapper)
    hooks/
      usePlayerMovement.ts
      usePlayerCamera.ts
      usePlayerCollision.ts
      usePlayerTagging.ts
      useJetpack.ts
  ```

**SoundManager.ts (621 lines)**

- **Issues:**
  - Procedural music generation, SFX playback, volume management all in one class
  - Web Audio API initialization mixed with game logic
- **Recommendation:** Split into:
  ```
  lib/audio/
    SoundManager.ts (orchestrator, ~150 lines)
    ProceduralMusic.ts
    SoundEffects.ts
    AudioContext.ts
  ```

#### 🟡 Medium Priority Files

| File              | Lines | Issue                          | Recommendation               |
| ----------------- | ----- | ------------------------------ | ---------------------------- |
| SpacemanModel.tsx | 349   | Hardcoded 3D model geometry    | Extract to `lib/models/`     |
| UtilityMenu.tsx   | 288   | Settings UI + state management | Split UI from logic          |
| GameUI.tsx        | 287   | Game HUD with inline styles    | Extract styles to CSS module |
| ChatBox.tsx       | 220   | Chat logic + profanity filter  | Separate filter to utility   |
| Home.tsx          | 215   | Card flip logic + nav          | Extract `useCardFlip` hook   |

---

### 2. Code Duplication & Patterns

#### Debug Logging (4 implementations found)

**Locations:**

- `Solo.tsx` lines 50-89
- `PlayerCharacter.tsx` lines 47-52
- `GameManager.ts` lines 45-62
- `useBotAI.ts` lines 8-14

**Recommendation:** Create unified logger

```typescript
// lib/utils/logger.ts
export const createLogger = (namespace: string) => {
  const isDev = import.meta.env?.DEV || process.env?.NODE_ENV !== "production";
  return {
    debug: (...args: unknown[]) =>
      isDev && console.log(`[${namespace}]`, ...args),
    info: (...args: unknown[]) => console.log(`[${namespace}]`, ...args),
    warn: (...args: unknown[]) => console.warn(`[${namespace}]`, ...args),
    error: (...args: unknown[]) => console.error(`[${namespace}]`, ...args),
  };
};

// Usage
const log = createLogger("GameManager");
log.debug("Game started", gameState);
```

#### Socket Connection Logic (duplicated across Lobby.tsx and Solo.tsx)

```typescript
// Current: Duplicated in 2 places
const serverUrl =
  import.meta.env.VITE_SOCKET_SERVER_URL || window.location.origin;
const socket = io(serverUrl, { transports: ["websocket"] });

// Recommended: Extract to hook
// hooks/useSocketConnection.ts
export const useSocketConnection = (options?: SocketOptions) => {
  // Centralized connection logic with reconnection, error handling, etc.
};
```

#### Profanity Filter (2 implementations)

- Client: `src/lib/constants/profanity.ts`
- Server: `server/profanity.js`

**Issue:** Server uses dynamic `process.env.CHAT_PROFANITY`, client has hardcoded list. Risk of inconsistency.

**Recommendation:** Share config via npm package or JSON config file

---

### 3. TypeScript & Type Safety

#### 🟢 Strengths

- Strict mode enabled in `tsconfig.json`
- Good use of type guards and interfaces
- Proper Socket.io typings in `types/socket.ts`

#### 🟡 Areas for Improvement

**20+ ESLint disables found**

```typescript
// Solo.tsx
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore - import.meta may not be available

// SoundManager.ts
/* eslint-disable no-undef */
```

**Recommendation:**

- Create proper type declarations for `import.meta.env` in `vite-env.d.ts`
- Add AudioContext types to global.d.ts instead of disabling rules
- Use `satisfies` operator for safer type assertions (TypeScript 4.9+)

**Missing types for ref forwarding:**

```typescript
// PlayerCharacter.tsx uses any in multiple places
const meshRef = useRef<THREE.Group>(null); // Good
const collisionSystem = useRef(new CollisionSystem()); // Missing generic type
```

---

### 4. Testing & Quality Assurance

#### Coverage Analysis

Based on test file examination:

- ✅ **Good:** Component rendering, game manager scoring, profanity filter
- ⚠️ **Partial:** Movement integration, socket communication
- ❌ **Missing:** Mobile controls (joystick/button), collision edge cases, bot AI decision-making

#### Critical Test Gaps

**1. Mobile Controls (HIGHEST PRIORITY)**

```typescript
// Needed: src/__tests__/MobileJoystick.integration.test.tsx
describe("MobileJoystick touch handling", () => {
  it("should respond to touch events on actual device", () => {
    // Test touch start/move/end
    // Verify coordinate translation
    // Test multi-touch scenarios
  });

  it("should handle orientation changes", () => {
    // Test portrait/landscape transitions
  });
});
```

**2. Collision System Edge Cases**

```typescript
// Needed: src/__tests__/CollisionSystem.edge-cases.test.ts
describe("Collision edge cases", () => {
  it("should handle high-velocity impacts", () => {});
  it("should prevent tunneling through walls", () => {});
  it("should handle simultaneous tag attempts", () => {});
});
```

**3. Bot AI Validation**

```typescript
// Needed: src/__tests__/useBotAI.behavior.test.ts
describe("Bot AI decision-making", () => {
  it("should chase player when IT", () => {});
  it("should flee when not IT", () => {});
  it("should avoid collisions with obstacles", () => {});
});
```

---

### 5. Performance & Optimization

#### Bundle Analysis

Current setup uses `rollup-plugin-visualizer` - good!

**Code splitting strategy:**

```javascript
// vite.config.js - Current manual chunks
manualChunks: {
  'react-vendor': ['react', 'react-dom', 'react-router-dom'],
  'three-vendor': ['three', '@react-three/fiber', '@react-three/drei']
}
```

**Recommendations:**

1. **Lazy load game pages:**

   ```typescript
   // App.tsx - Already using Suspense, good!
   const Solo = lazy(() => import("./pages/Solo"));
   const Lobby = lazy(() => import("./pages/Lobby"));
   ```

2. **Defer heavy imports:**

   - Spline (disabled but 150KB when enabled)
   - SpacemanModel.tsx 3D geometry (load on game start, not home page)

3. **Image optimization:**

   ```bash
   # Assets to optimize:
   src/assets/twitter-512.png (68KB - can be WebP)
   src/assets/emoji.png (unused? - see below)
   ```

#### Runtime Performance

- ✅ **Good:** Uses `useCallback` and `useMemo` appropriately
- ✅ **Good:** PerformanceMonitor component for FPS tracking
- ⚠️ **Concern:** `useFrame` in PlayerCharacter runs every frame with 300+ lines of logic

**Recommendation:** Profile with React DevTools Profiler and optimize hot paths

---

### 6. Unused Code & Dead Assets

#### Commented Code

**Home.tsx (lines 3, 5):**

```typescript
// import Spline from '@splinetool/react-spline';
// import LoadingSpinner from '../components/LoadingSpinner';
// const SPLINE_SCENE = `https://prod.spline.design/lwFGUGO5nCfnnDQU/scene.splinecode`;
```

**Decision needed:** Remove permanently or create feature flag?

**Lobby.tsx:**

```typescript
// Solo.tsx comment (line 79 in test file):
// OrbitControls is now commented out in Solo.tsx
```

**Status:** Appears Lobby.tsx is deprecated in favor of Solo.tsx?

#### Unused Assets

**`emoji.ico` and `emoji.png`** - No references found in codebase

```bash
# Search results: 0 matches for emoji.(ico|png) in src/
```

**Recommendation:** Remove or document purpose

**`twitter-512.png`** - Used only in Footer.tsx

- Consider CDN hosting for social icons
- Or convert to inline SVG for faster load

#### Unused Dependencies?

Need to audit:

```json
"@splinetool/react-spline": "^2.2.6",  // Used? See Home.tsx
"@splinetool/runtime": "^0.9.82",      // Used?
"vite-plugin-bundle-analyzer": "^0.0.1" // Overlaps with visualizer?
```

---

### 7. Mobile Experience (Critical Gap)

#### Documented Issues (from TODO.md)

- ❌ Joystick touch input not responding
- ❌ Two-finger camera rotation not working
- ❌ Dark mode icon covered by game UI in landscape
- ⚠️ Home page cards not visible/responsive on mobile

#### Code Review Findings

**MobileJoystick.tsx (137 lines):**

```typescript
const handleTouchStart = useCallback((event: React.TouchEvent) => {
  // ... implementation
}, []);
```

**Issue:** Touch event handling may not account for:

- Browser touch event quirks (Safari vs Chrome)
- Passive event listener optimization
- Touch point tracking across rapid movements

**Recommendation:**

1. Add comprehensive touch event logging
2. Test on physical devices (iOS Safari, Android Chrome)
3. Consider using battle-tested library like `react-use-gesture`
4. Add haptic feedback for better mobile UX

**MobileButton.tsx (60 lines):**

```typescript
// eslint-disable-next-line no-undef
let touchTimeout: ReturnType<typeof setTimeout>;
```

**Issue:** Double-tap for jetpack may conflict with browser zoom gestures

---

### 8. Server Architecture

#### Current Implementation (server.js - 260 lines)

**Strengths:**

- ✅ Clean Express + Socket.io setup
- ✅ CORS configuration with wildcard support
- ✅ Health check endpoint
- ✅ Profanity filter integration

**Critical Gaps:**

**1. No Rate Limiting**

```javascript
// Missing: Rate limit per IP/socket
client.on("chat-message", async (message) => {
  // No check for spam/flooding
  ioServer.sockets.emit("chat-message", filteredMessage);
});
```

**2. No Input Validation**

```javascript
client.on("move", ({ rotation, position }) => {
  // No validation of position bounds
  // No check for impossible movements
  clients[client.id].position = position; // Trusts client!
});
```

**3. No Connection Limits**

```javascript
// Missing: Max connections per IP
// Missing: Connection pooling
// Missing: Graceful degradation under load
```

**4. State Management is Volatile**

```javascript
let clients = {}; // Lost on server restart
let gameState = {}; // No persistence
```

#### Recommendations

**Immediate (P0):**

```javascript
// Add express-rate-limit
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});

app.use("/health", limiter);

// Add socket-io-sticky-session for horizontal scaling
```

**Short-term (P1):**

- Implement Redis for shared state across instances
- Add input validation library (Zod or Joi)
- Implement connection queue and backpressure
- Add monitoring/alerting (Sentry, DataDog, or similar)

**Long-term (P2):**

- Consider dedicated game server framework (Colyseus, Geckos.io)
- Implement authoritative server model for anti-cheat
- Add game replay/recording system

---

### 9. CSS & Styling

#### Current Approach

Mixed approach with both inline styles and separate CSS files:

- `src/styles/` folder with component-specific CSS
- Inline styles in React components (especially GameUI.tsx)

#### Issues

**1. No CSS Modules**

```css
/* App.css has global classes that could conflict */
.container {
  /* Generic name */
}
.button {
  /* Generic name */
}
```

**2. Duplicate Theme Logic**

- ThemeContext.tsx manages dark/light theme
- CSS variables defined in multiple files
- No centralized design tokens

**3. No Mobile-First Approach**

```css
/* Current: Desktop-first */
.card {
  width: 300px;
}
@media (max-width: 768px) {
  .card {
    width: 200px;
  }
}

/* Better: Mobile-first */
.card {
  width: 200px;
}
@media (min-width: 768px) {
  .card {
    width: 300px;
  }
}
```

#### Recommendations

**Option A: CSS Modules (low effort)**

```typescript
// Home.module.css
import styles from './Home.module.css';
<div className={styles.heroSection}>
```

**Option B: Styled Components (medium effort)**

```typescript
import styled from "styled-components";
const HeroSection = styled.div`
  /* Styles with theme support */
`;
```

**Option C: Tailwind CSS (high effort, best DX)**

```typescript
<div className="flex flex-col items-center p-4 bg-gray-900 dark:bg-black">
```

**My Recommendation:** Start with CSS Modules, migrate to Tailwind in next major version

---

### 10. Dependency Management

#### Audit Results

**Outdated (check for updates):**

```json
"prettier": "^2.4.1",  // Latest is 3.x
"husky": "^8.0.0",     // Latest is 9.x
"socket.io": "^4.8.1", // Check for 4.9.x patches
```

**Potential Conflicts:**

```json
"react": "^19.2.0",           // Very new!
"@react-three/fiber": "^9.4.0" // May have compat issues with React 19
"@react-three/drei": "^10.7.6"
```

**Action:** Monitor for React 19 compatibility issues in Three.js ecosystem

**Duplicate Functionality:**

```json
"rollup-plugin-visualizer": "^6.0.5",
"vite-plugin-bundle-analyzer": "^0.0.1"
```

**Recommendation:** Keep visualizer (more maintained), remove bundle-analyzer

#### Security

Run regular audits:

```bash
npm audit
npm audit fix
```

---

## Technology Stack Assessment

### Current Stack ✅

- **Frontend:** React 19 + TypeScript + Vite ⭐⭐⭐⭐⭐
- **3D Engine:** Three.js + R3F ⭐⭐⭐⭐⭐
- **Networking:** Socket.io ⭐⭐⭐⭐☆ (good, could be better)
- **Testing:** Vitest + Testing Library ⭐⭐⭐⭐⭐
- **CI/CD:** GitHub Actions + Husky ⭐⭐⭐⭐⭐
- **Hosting:** Netlify (frontend) + custom (backend) ⭐⭐⭐⭐☆

### Recommendations for Stack Evolution

#### Consider Adding:

1. **State Management:** Zustand or Jotai (if useState becomes unwieldy)
2. **Form Validation:** React Hook Form + Zod (for settings, chat)
3. **Monitoring:** Sentry (error tracking), PostHog (analytics)
4. **E2E Testing:** Playwright (for critical user flows)

#### Consider Replacing:

1. **Socket.io → WebRTC Data Channels** (for lower latency P2P)
2. **Express → Fastify** (2x faster, better TypeScript support)
3. **Custom server → Colyseus** (purpose-built game server framework)

---

## Conclusion

Darkmoon has a **solid foundation** but needs **systematic refactoring** to scale. The codebase is maintainable by skilled developers but would benefit from decomposition and better separation of concerns.

### Immediate Action Items (Next Sprint)

1. ✅ Fix mobile touch controls (P0 blocker)
2. ✅ Decompose Solo.tsx into smaller modules
3. ✅ Create unified logger utility
4. ✅ Add input validation to server
5. ✅ Remove commented code and unused assets

### Success Metrics

- Reduce largest file from 1000→300 lines
- Increase mobile test coverage 0%→70%
- Reduce bundle size by 15%
- Fix all P0 mobile UX issues

---

**Next Steps:** See `ROADMAP.md` for prioritized implementation plan.

## Related
- [[repos/darkmoon/docs/archive/ARCHITECTURE_IMPROVEMENTS|Architecture Improvements]] — actionable improvements derived from this review
- [[repos/darkmoon/docs/ARCHITECTURE|Architecture]] — current active architecture document
- [[repos/darkmoon|darkmoon runbook]] — repo context
