# DARKMOON Development Guide

DARKMOON is a 3D multiplayer tag game built with React Three Fiber, Socket.io, and Vite. This guide covers project-specific patterns that differ from typical React/Three.js projects.

## Priority System

1. **Check `docs/FEEDBACK.md` FIRST** - Active QA feedback takes priority over new features
2. Mark completed items with ✅ and add QA validation checklists
3. Use `docs/PHASE#.md` for feature context and architectural decisions
4. `TODO.md` is gitignored - use freely for scratch work

## Architecture Patterns

### Refs Over State for High-Frequency Data

React state causes re-renders. Use refs for values accessed in event handlers or `useFrame` loops:

```typescript
// ❌ Wrong - captures stale state in closure
const [isPaused, setIsPaused] = useState(false);
useEffect(() => {
  const handleKey = (e: KeyboardEvent) => {
    if (!isPaused) {
      /* stale value */
    }
  };
  window.addEventListener("keydown", handleKey);
}, []); // isPaused not in deps = stale closure

// ✅ Correct - use ref for current value
const isPausedRef = useRef(isPaused);
useEffect(() => {
  isPausedRef.current = isPaused;
}, [isPaused]);
useEffect(() => {
  const handleKey = (e: KeyboardEvent) => {
    if (!isPausedRef.current) {
      /* always current */
    }
  };
  window.addEventListener("keydown", handleKey);
}, []); // No deps needed - handler uses refs
```

See `src/pages/Solo.tsx` lines 517-522 and keyboard handlers for the canonical implementation.

### Solo vs Multiplayer Socket Configuration

Solo mode is offline-first. Disable Socket.io reconnection to avoid console spam:

```typescript
const socket = io(serverUrl, {
  reconnection: false, // No reconnection in solo mode
  autoConnect: false, // Manual connection control
});
```

Server runs on port 4444. Dev client on port 5173 (Vite). Check `server.js` for CORS and WebSocket setup.

### Mobile Touch Events

React synthetic events are passive by default and cannot call `preventDefault()`. Use native DOM events:

```typescript
// ❌ Wrong - React synthetic event is passive
<div onTouchStart={(e) => e.preventDefault()}>

// ✅ Correct - native DOM event with passive: false
useEffect(() => {
  const element = ref.current;
  const handler = (e: TouchEvent) => e.preventDefault();
  element?.addEventListener("touchstart", handler, { passive: false });
  return () => element?.removeEventListener("touchstart", handler);
}, []);
```

See `src/components/MobileJoystick.tsx` lines 101-104.

### Dynamic Viewport Units for Mobile

Use `dvh`/`dvw` instead of `vh`/`vw` to handle mobile browser chrome:

```css
/* ❌ Wrong - ignores mobile address bar */
height: 100vh;

/* ✅ Correct - adapts to viewport changes */
height: 100dvh;
```

All CSS files should use dynamic viewport units. Check `src/styles/App.css`.

### Frame-Based Debug Logging

Use frame counters instead of `Math.random()` for periodic logs in `useFrame`:

```typescript
// ❌ ESLint violation - Math.random() in game loop
if (Math.random() < 0.01) console.log("debug");

// ✅ Deterministic - logs every 100 frames
const frameCounter = useRef(0);
useFrame(() => {
  frameCounter.current++;
  if (frameCounter.current % 100 === 0) {
    debug("Status:", value);
  }
});
```

### Gated Development Logging

Use environment-aware debug functions to prevent console spam in production:

```typescript
const debug = (...args: unknown[]) => {
  if (import.meta && import.meta.env && import.meta.env.DEV) {
    console.log(...args);
  }
};
```

This pattern is used throughout `Solo.tsx` and `GameManager.ts`.

## Testing Requirements

### Pre-Push Hook

All commits must pass automated checks before push (`.husky/pre-push`):

- TypeScript type check (`npm run typecheck`)
- ESLint with `--max-warnings=0` (`npm run lint`)
- Full test suite with coverage (`npm run test:ci`)

Run manually: `.\ci-check.ps1` (Windows) or `./ci-check.sh` (Unix)

### Test Patterns

Tests live in `src/__tests__/`. Mock React Three Fiber and Socket.io:

```typescript
// Wrap components with providers
const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <ThemeProvider>{ui}</ThemeProvider>
    </BrowserRouter>
  );
};
```

Config: `config/vitest.config.ts` with jsdom environment and singleThread mode.

## Code Quality Standards

### TypeScript

- Strict mode enabled (`tsconfig.json`)
- No `any` types without justification
- Explicit interfaces for all component props

### React Three Fiber

- Lowercase JSX for Three.js primitives: `<mesh>`, `<boxGeometry>`
- Use `useFrame` for animation loops (NOT `requestAnimationFrame`)
- Access Three objects via refs: `meshRef.current.position.set(...)`

### CSS Selectors

- Use semantic classes, not fragile attribute selectors
- ❌ `div[style*="fontSize"]` (breaks if styles change)
- ✅ `.moon-background` (stable class selector)

### ESLint Configuration

Custom config in `config/eslint.config.js`. Must pass with zero warnings.

## Key Files & Responsibilities

- `src/pages/Solo.tsx` - Offline game mode with character controls, collision, profanity filter
- `src/pages/Lobby.tsx` - Multiplayer lobby with Socket.io room management
- `src/components/GameManager.ts` - Game state (tag/race/collect modes), scoring, player tracking
- `src/components/CollisionSystem.ts` - Player-obstacle and player-player collision detection
- `src/components/MobileJoystick.tsx` - Touch controls with native event handling
- `server.js` - Express + Socket.io backend (port 4444)

## Common Commands

```bash
npm run dev           # Start dev server (port 5173) + backend (port 4444)
npm run lint          # ESLint with --max-warnings=0
npm test              # Vitest in watch mode
npm run test:ci       # Run tests once with coverage
npm run build         # Production build
.\ci-check.ps1        # Run full CI validation locally
```

## Known Test Warnings (Ignorable)

- "Multiple instances of Three.js being imported" - R3F dependency structure
- "Not implemented: Window's scrollTo() method" - JSDOM limitation in tests

## Profanity Filtering

Client-side filter in `Solo.tsx`. Uses regex replacement with asterisks. Server-side filter in `server/profanity.js`.

---

For architectural context, see `docs/PHASE7.md`. For detailed patterns and workflows, see `.github/prompts/AGENT.prompt.md`.
