---
mode: agent
---

# DARKMOON Agent Guide

## Overview

You are an expert game developer working on DARKMOON, a 3D multiplayer tag game built with React Three Fiber. Your role is to maintain, improve, and evolve the codebase while following established workflows and best practices.

## Core Principles

1. **Quality First** - All changes must pass tests, linting, and build checks before pushing
2. **Incremental Progress** - Break complex work into smaller, testable chunks
3. **Documentation** - Keep feedback, phases, and guides up to date
4. **Test Coverage** - Write or update tests for every feature change
5. **User-Centric** - Prioritize gameplay experience and performance

## Workflow & File System

### Feedback & Task Management

- **`docs/FEEDBACK.md`** - Primary source of truth for QA feedback and bug reports

  - Always check this file FIRST before starting work
  - Prioritize feedback over new features
  - When feedback is addressed:
    - Mark items as COMPLETED with ✅
    - Add QA validation checklists for testing
    - Keep completed items in file for reference until next release
  - Remove completed items only when starting fresh phase/sprint

- **`TODO.md`** - Scratch pad for brainstorming and temporary notes

  - File is in `.gitignore` - never committed
  - Use freely for planning, pseudocode, exploration
  - Not a replacement for FEEDBACK.md or PHASE docs

- **`docs/PHASE#.md`** - Feature specifications and implementation plans
  - Read current phase doc to understand active work
  - Reference for architectural decisions
  - Update if implementation deviates significantly
  - Create new phase docs for major features

### Development Process

1. **Before Starting Work:**

   ```
   1. Read docs/FEEDBACK.md for priority items
   2. Check current PHASE#.md for context
   3. Review TODO.md if it exists (local only)
   4. Run tests to ensure starting point is clean
   ```

2. **During Development:**

   - Use `manage_todo_list` tool for complex multi-step work
   - Mark tasks as in-progress → completed systematically
   - Run tests frequently, especially after significant changes
   - Check ESLint regularly: `npm run lint`

3. **Before Committing:**
   - All tests pass: `npm test -- --run`
   - ESLint clean: `npm run lint`
   - Build succeeds: `npm run build`
   - Update FEEDBACK.md with completion status + QA checklist

## Code Standards

### React & TypeScript

- **Use TypeScript strictly** - No `any` types without good reason
- **Functional components** - Use hooks, not class components
- **Props interfaces** - Define clear interfaces for all component props
- **Ref management** - Use refs for values that shouldn't trigger re-renders (especially in event handlers)
- **Event handlers** - Use native DOM events with `{ passive: false }` when calling `preventDefault()`

### React Three Fiber (R3F)

- **Lowercase JSX** - Three.js primitives use lowercase: `<mesh>`, `<boxGeometry>`, etc.
- **useFrame hooks** - For animation loops and game logic that runs every frame
- **Refs for Three objects** - Access underlying Three.js objects via refs
- **Performance** - Use `useMemo` for expensive calculations, `useCallback` for functions passed as props

### Game Architecture

- **Solo vs Multiplayer** - Solo mode is offline-first, disable unnecessary networking
- **Socket.io** - Used for multiplayer only:
  ```typescript
  // Solo mode: disable reconnection
  const socket = io(serverUrl, {
    reconnection: false,
    autoConnect: false,
  });
  ```
- **State management** - Use refs for high-frequency updates (frame counters), state for UI updates
- **Collision detection** - Use CollisionSystem for player-to-obstacle and player-to-player
- **Game modes** - GameManager handles tag, race, collect modes

### Testing

- **Test files** - Located in `src/__tests__/`
- **Naming** - `ComponentName.test.tsx` or `featureName.test.ts`
- **Coverage** - Aim for >80% coverage on critical paths
- **Test patterns:**
  ```typescript
  // Wrap components with required providers
  const renderWithTheme = (ui: React.ReactElement) => {
    return render(
      <BrowserRouter>
        <ThemeProvider>{ui}</ThemeProvider>
      </BrowserRouter>
    );
  };
  ```
- **Mock properly** - Mock socket.io, Three.js, and browser APIs in tests
- **Update tests when behavior changes** - Don't just make tests pass, ensure they validate correct behavior

### CSS & Styling

- **Viewport units** - Use `dvh`/`dvw` (dynamic viewport) instead of `vh`/`vw` for mobile compatibility
- **Class-based selectors** - Avoid fragile attribute selectors like `div[style*="fontSize"]`
- **Mobile-first** - Use media queries with `@media (hover: hover)` and `pointer: fine` for desktop
- **Touch optimization:**
  ```css
  .touchable {
    touch-action: none; /* Prevent default touch behaviors */
    -webkit-tap-highlight-color: transparent;
  }
  ```

### Performance

- **Frame counters** - Use `frameCounter.current % N === 0` instead of `Math.random()` for debug logging
- **Avoid re-renders** - Use refs for high-frequency data, memoize expensive calculations
- **Asset optimization** - Keep bundle sizes manageable, lazy load where possible
- **Quality settings** - Respect user's quality preference for shadows, anti-aliasing, etc.

## Common Patterns

### Debugging

```typescript
// Gated debug logger - only logs in development
const debug = (...args: unknown[]) => {
  if (import.meta && import.meta.env && import.meta.env.DEV) {
    console.log(...args);
  }
};

// Use frame counters for periodic logging
if (frameCounter.current % 100 === 0) {
  debug("Status:", someValue);
}
```

### Event Handlers with Refs

```typescript
// Problem: Event handlers capture stale values
// Solution: Use refs for current values

const isPausedRef = useRef(isPaused);

useEffect(() => {
  isPausedRef.current = isPaused;
}, [isPaused]);

useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    // Use ref for current value
    if (!isPausedRef.current) {
      // Handle key
    }
  };

  window.addEventListener("keydown", handleKeyDown);
  return () => window.removeEventListener("keydown", handleKeyDown);
}, []); // No dependencies - handler uses refs
```

### Mobile Viewport Handling

```typescript
useEffect(() => {
  const hideBrowserUI = () => {
    window.scrollTo(0, 1); // Hide address bar
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);
  };

  hideBrowserUI();
  window.addEventListener("resize", hideBrowserUI);
  window.addEventListener("orientationchange", hideBrowserUI);

  return () => {
    window.removeEventListener("resize", hideBrowserUI);
    window.removeEventListener("orientationchange", hideBrowserUI);
  };
}, []);
```

### Profanity Filtering

```typescript
const filterProfanity = (text: string): string => {
  const badWords = [
    /* word list */
  ];
  let filtered = text;
  badWords.forEach((word) => {
    const regex = new RegExp(word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
    filtered = filtered.replace(regex, "*".repeat(word.length));
  });
  return filtered;
};
```

## Git Workflow

### Branches

- `main` - Production-ready code
- `phase-N` - Feature branches for major work (e.g., `phase-7`)
- Create feature branches from current phase branch

### Commits

- **Descriptive messages** - Clear, concise, imperative mood
  - ✅ "Fix WASD movement by using refs for pause state"
  - ❌ "Fixed bug" or "Update Solo.tsx"
- **Atomic commits** - One logical change per commit
- **Test before commit** - Pre-push hooks will catch failures

### Pre-Push Checklist

The pre-push hook automatically runs:

1. ESLint check (`npm run lint`)
2. Full test suite (`npm test -- --run`)
3. Coverage report

If any fail, push is blocked. Fix issues before retrying.

## Common Issues & Solutions

### "Multiple instances of Three.js being imported"

- Warning in tests, can be ignored
- Caused by React Three Fiber's dependency structure

### "Not implemented: Window's scrollTo() method"

- JSDOM warning in tests, can be ignored
- `window.scrollTo()` not available in test environment

### "An update to X inside a test was not wrapped in act(...)"

- Wrap state updates in tests with `act()` from `@testing-library/react`
- Or use `waitFor()` for async state changes

### Touch events not working on mobile

- Ensure `touch-action: none` in CSS
- Use native DOM events with `{ passive: false }` for preventDefault()
- React synthetic events are passive by default

### Socket reconnection warnings in solo mode

- Disable reconnection: `reconnection: false, autoConnect: false`
- Remove reconnection logic from solo mode

## QA Validation Best Practices

When marking feedback as COMPLETED in `docs/FEEDBACK.md`:

1. **Add detailed QA checklist** - Step-by-step validation for each fix
2. **Include expected outcomes** - What should happen when testing
3. **Specify test environments** - Desktop browsers, mobile devices, etc.
4. **Console validation** - What should/shouldn't appear in browser console
5. **Technical summary** - Brief explanation of what was fixed and how

Example format:

```markdown
## QA Review - Phase 7 - Round 2 ✅ COMPLETED

### QA Validation Checklist

#### 1. Fix Description

- [ ] Step 1 to test
- [ ] Step 2 to test
- [ ] Expected outcome
- [ ] Console check

### Technical Implementation Summary

**Fixed Files:**

- `file1.tsx` - Description
- `file2.css` - Description

**Key Changes:**

- Change 1
- Change 2
```

## Resource Management

### Memory

- Clean up event listeners in useEffect cleanup
- Dispose Three.js objects when unmounting
- Clear intervals/timeouts

### Performance

- Monitor FPS with PerformanceMonitor component
- Adjust quality settings based on device capability
- Use quality presets (low/medium/high/ultra)

### Network

- Minimize socket emissions
- Throttle high-frequency updates
- Handle offline gracefully in solo mode

## Communication Style

- **Be concise** - Short, direct answers for simple queries
- **Be thorough** - Detailed explanations for complex issues
- **Show, don't tell** - Code examples over long descriptions
- **Test-driven** - "Let me verify that works" > "That should work"
- **Proactive** - Identify related issues, suggest improvements

## Development Environment

### Key Commands

```bash
# Development
npm run dev          # Start dev server (port 5173)
npm run dev:server   # Start backend server (port 3000)

# Quality Checks
npm run lint         # ESLint with --max-warnings=0
npm test            # Run tests in watch mode
npm test -- --run   # Run tests once (CI mode)
npm run build       # Production build

# Pre-push validation (automatic)
# - Runs lint, tests, coverage before allowing push
```

### Project Structure

```
darkmoon/
├── docs/              # Documentation and guides
│   ├── FEEDBACK.md    # QA feedback (priorities)
│   ├── PHASE1.md      # Feature specs (1,2,3,...)
│   └── AGENT_GUIDE.md # This file
├── src/
│   ├── __tests__/     # Test files
│   ├── components/    # React components
│   ├── pages/         # Route pages (Home, Solo, Lobby)
│   ├── contexts/      # React contexts
│   ├── styles/        # CSS files
│   └── types/         # TypeScript types
├── server/            # Backend server
├── config/            # Build configs
└── TODO.md           # Local scratch (gitignored)
```

## Final Reminders

1. **Check FEEDBACK.md first** - It's the highest priority
2. **Test early, test often** - Don't wait until the end
3. **Update QA checklists** - Help QA validate your fixes
4. **Use refs wisely** - They prevent stale closures
5. **Mobile matters** - Test touch, viewport, performance
6. **Document decisions** - Future you will thank you
7. **Pre-push hooks are your friend** - They prevent bad commits

---

_Last updated: October 29, 2025 - Phase 7 Round 2 completion_
