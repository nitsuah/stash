# Game Development Agent Guide

## Overview

You are an expert game developer working on a 3D web-based game. Your role is to maintain, improve, and evolve the codebase while following established workflows and best practices. This guide provides framework-agnostic principles adapted for the specific patterns and conventions used in this project.

## Core Principles

1. **Quality First** - All changes must pass tests, linting, and build checks before committing
2. **Incremental Progress** - Break complex work into smaller, testable chunks with clear milestones
3. **Documentation** - Keep feedback, phase docs, and technical guides synchronized with code
4. **Test-Driven** - Write or update tests for every feature change; tests are living documentation
5. **User-Centric** - Prioritize gameplay experience, performance, and accessibility
6. **Fail Fast** - Catch errors early through automated checks, not in production

## Workflow & File System

### Feedback & Task Management Hierarchy

**1. `docs/FEEDBACK.md` - Primary Source of Truth**

- **ALWAYS check this file FIRST** before starting any work
- Contains QA feedback, bug reports, and user-reported issues
- Priority order: Critical bugs → User feedback → Nice-to-haves → New features
- When addressing feedback:
  - Mark items as COMPLETED with ✅ and timestamp
  - Add detailed QA validation checklists for each fix
  - Document technical implementation summary (files changed, key changes)
  - Keep completed items visible until next major release/phase
  - Remove completed items only when starting fresh sprint cycle

**2. `TODO.md` - Personal Scratch Pad (Git-Ignored)**

- Add to `.gitignore` - this file should NEVER be committed
- Use freely for:
  - Brainstorming and pseudocode
  - Temporary notes during complex debugging
  - Quick calculations or data structures
  - Exploration of multiple approaches
- NOT a replacement for FEEDBACK.md or documentation
- Clean up periodically to avoid clutter

**3. `docs/PHASE#.md` - Feature Specifications**

- Read current phase doc to understand active development context
- Contains architectural decisions, technical requirements, acceptance criteria
- Update if implementation deviates significantly from original plan
- Reference during code reviews and handoffs
- Create new phase docs for major features or architectural changes

### Development Workflow

**Before Starting Work:**

```text
1. Read docs/FEEDBACK.md for priority items (CRITICAL)
2. Check current PHASE#.md for context and requirements
3. Review TODO.md if it exists (local scratch notes)
4. Run tests to ensure clean baseline: npm test -- --run
5. Check for uncommitted changes: git status
```

**During Development:**

- Use `manage_todo_list` tool for multi-step work requiring planning
- Mark tasks: not-started → in-progress → completed (systematically)
- Run tests frequently (after each logical change)
- Commit incrementally with descriptive messages
- Keep feedback loop tight: code → test → commit

**Before Committing:**

```text
1. All tests pass: npm test -- --run
2. Linting clean: npm run lint (or equivalent)
3. Build succeeds: npm run build
4. Update FEEDBACK.md with completion status + QA checklist
5. Review diff to ensure no debug code or unintended changes
```

**After Committing:**

- Push to feature branch (not main)
- Monitor CI/CD pipeline for build failures
- Test deployed preview if available (Netlify, Vercel, etc.)
- Update team/stakeholders on progress

## Code Standards & Best Practices

### General Coding Principles

- **Readability over cleverness** - Write code that junior developers can understand
- **Single Responsibility** - Functions/components should do ONE thing well
- **DRY (Don't Repeat Yourself)** - Extract common logic into reusable utilities
- **Fail fast** - Validate inputs early, throw meaningful errors
- **Defensive programming** - Handle edge cases, null checks, fallbacks
- **Comment why, not what** - Code shows what it does; comments explain why

### State Management Patterns

**When to use refs vs state:**

- **Refs** - High-frequency updates that don't need UI re-renders:
  - Frame counters, animation loops
  - Values accessed in event handlers (prevents stale closures)
  - Direct DOM manipulation
  - Previous values for comparison

- **State** - Values that trigger UI updates:
  - User-facing data (scores, health, UI visibility)
  - Conditional rendering logic
  - Props passed to child components

**Common pitfall - Stale closures in event handlers:**

```javascript
// Problem: Event handler captures old value
const [isPaused, setIsPaused] = useState(false);

useEffect(() => {
  const handleKeyDown = (e) => {
    if (!isPaused) { // This captures isPaused at mount time!
      // Handle input
    }
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []); // Empty deps = stale closure

// Solution: Use ref for current value
const isPausedRef = useRef(isPaused);
useEffect(() => { isPausedRef.current = isPaused; }, [isPaused]);

useEffect(() => {
  const handleKeyDown = (e) => {
    if (!isPausedRef.current) { // Always current value
      // Handle input
    }
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []); // No stale closure
```

### Testing Philosophy

- **Test files location** - Typically `__tests__/` or `*.test.{js,ts,jsx,tsx}`
- **Naming convention** - `ComponentName.test.tsx` or `featureName.test.ts`
- **Coverage targets** - Aim for >80% on critical paths, 100% on core game logic
- **What to test:**
  - Core game mechanics (scoring, collision, state transitions)
  - Edge cases and error handling
  - User interactions (keyboard, mouse, touch)
  - Integration between systems
- **What NOT to test:**
  - Third-party library internals
  - Trivial getters/setters
  - Static content

**Test patterns:**

```javascript
// Wrap components with required providers
const renderWithProviders = (ui) => {
  return render(
    <GameProvider>
      <AudioProvider>
        {ui}
      </AudioProvider>
    </GameProvider>
  );
};

// Mock high-frequency updates
jest.mock('./hooks/useGameLoop', () => ({
  useGameLoop: jest.fn(),
}));
```

- **Mock appropriately** - Mock network calls, timers, browser APIs, heavy calculations
- **Update tests when behavior changes** - Tests document expected behavior

### Performance Optimization

**Frame-based operations:**

```javascript
// Use frame counters for periodic logging (deterministic)
const frameCounter = useRef(0);
useFrame(() => {
  frameCounter.current++;
  if (frameCounter.current % 100 === 0) { // Every 100 frames
    console.log('Debug info');
  }
});

// Avoid Math.random() for debug toggles (non-deterministic)
```

**Rendering optimization:**

- **Memoization** - Use `useMemo` for expensive calculations, `useCallback` for functions
- **Avoid re-renders** - Keep high-frequency data in refs, not state
- **Lazy loading** - Code-split routes, defer non-critical assets
- **Asset optimization** - Compress textures, use appropriate formats (WebP, AVIF)

**Game-specific:**

- **Object pooling** - Reuse objects (bullets, particles) instead of creating/destroying
- **Level of detail (LOD)** - Reduce complexity for distant objects
- **Quality settings** - Provide low/medium/high presets (shadows, anti-aliasing, effects)

### CSS & Styling

**Modern viewport units (mobile compatibility):**

```css
/* Avoid fixed vh/vw on mobile (doesn't account for browser UI) */
.fullscreen-bad {
  height: 100vh; /* Includes address bar on mobile */
}

/* Use dynamic viewport units */
.fullscreen-good {
  height: 100dvh; /* Excludes browser UI */
  width: 100dvw;
}
```

**Touch optimization:**

```css
.interactive-element {
  touch-action: none; /* Prevent default gestures */
  -webkit-tap-highlight-color: transparent; /* Remove tap highlight */
  user-select: none; /* Prevent text selection */
}
```

**Responsive design:**

```css
/* Mobile-first approach */
.button {
  font-size: 16px;
  padding: 12px;
}

/* Desktop enhancements */
@media (hover: hover) and (pointer: fine) {
  .button:hover {
    transform: scale(1.05);
  }
}
```

### Error Handling & Debugging

**Gated debug logging (production-safe):**

```javascript
const debug = (...args) => {
  if (process.env.NODE_ENV === 'development') {
    console.log('[DEBUG]', ...args);
  }
};

// Or environment-specific
if (import.meta && import.meta.env && import.meta.env.DEV) {
  console.log('Dev-only message');
}
```

**Meaningful error messages:**

```javascript
// Bad
throw new Error('Invalid');

// Good
throw new Error(`Invalid weapon type "${weaponType}". Expected: ${VALID_WEAPONS.join(', ')}`);
```

**Graceful degradation:**

```javascript
// Handle missing features gracefully
try {
  await audioContext.resume();
} catch (err) {
  console.warn('Audio context failed to resume:', err);
  // Continue without audio rather than crashing
}
```

## Common Patterns & Solutions

### Mobile Viewport Handling

Mobile browsers have dynamic UI (address bars, toolbars) that affect viewport height:

```javascript
useEffect(() => {
  const updateViewportHeight = () => {
    // Hide browser UI by scrolling slightly
    window.scrollTo(0, 1);
    
    // Set CSS custom property for true viewport height
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  };

  updateViewportHeight();
  window.addEventListener('resize', updateViewportHeight);
  window.addEventListener('orientationchange', updateViewportHeight);

  return () => {
    window.removeEventListener('resize', updateViewportHeight);
    window.removeEventListener('orientationchange', updateViewportHeight);
  };
}, []);
```

```css
/* Use custom property in CSS */
.fullscreen-container {
  height: calc(var(--vh, 1vh) * 100);
}
```

### Input Sanitization (Profanity Filtering)

For user-generated content in multiplayer games:

```javascript
const filterProfanity = (text) => {
  const badWords = ['word1', 'word2', /* ... */];
  let filtered = text;
  
  badWords.forEach(word => {
    // Escape regex special characters
    const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(escaped, 'gi');
    filtered = filtered.replace(regex, '*'.repeat(word.length));
  });
  
  return filtered;
};

// Usage
const displayName = filterProfanity(userInput);
```

### Event Handler Memory Management

Prevent memory leaks by cleaning up event listeners:

```javascript
useEffect(() => {
  const handleKeyDown = (e) => {
    // Handle key
  };
  
  const handleResize = () => {
    // Handle resize
  };
  
  // Add listeners
  window.addEventListener('keydown', handleKeyDown);
  window.addEventListener('resize', handleResize);
  
  // CRITICAL: Remove on cleanup
  return () => {
    window.removeEventListener('keydown', handleKeyDown);
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

### Preventing Default Touch Behaviors

For game controls that conflict with browser gestures:

```javascript
useEffect(() => {
  const preventDefaults = (e) => {
    e.preventDefault();
  };
  
  // Use { passive: false } to allow preventDefault()
  document.addEventListener('touchmove', preventDefaults, { passive: false });
  document.addEventListener('touchstart', preventDefaults, { passive: false });
  
  return () => {
    document.removeEventListener('touchmove', preventDefaults);
    document.removeEventListener('touchstart', preventDefaults);
  };
}, []);
```

## Git Workflow

### Branch Strategy

- **`main`** - Production-ready code (protected, requires PR)
- **`phase-N`** - Feature branches for major work (e.g., `phase-7`, `phase-8`)
- **`feature/xyz`** - Short-lived branches for specific features
- **`fix/xyz`** - Bug fix branches

**Branching rules:**

- Branch from `main` for new phases
- Branch from current phase for related features
- Never commit directly to `main`
- Delete feature branches after merging

### Commit Messages

Write clear, actionable commit messages in imperative mood:

**Good examples:**

- ✅ `fix: WASD movement by using refs for pause state`
- ✅ `feat: add invincibility power-up with visual effect`
- ✅ `refactor: extract scoring logic to separate module`
- ✅ `test: add coverage for weapon switching behavior`
- ✅ `docs: update FEEDBACK.md with QA validation checklist`

**Bad examples:**

- ❌ `Fixed bug` (not descriptive)
- ❌ `Update Solo.tsx` (what changed?)
- ❌ `WIP` (work-in-progress should be rebased)
- ❌ `Various changes` (not atomic)

**Commit message format:**

```text
<type>: <description>

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `perf`, `chore`

### Pre-Commit Checklist

Before committing, ensure:

1. **Tests pass** - `npm test -- --run` (or equivalent)
2. **Linting clean** - `npm run lint` (or equivalent)
3. **Build succeeds** - `npm run build`
4. **No debug code** - Remove console.logs, breakpoints, test data
5. **FEEDBACK.md updated** - Mark completed items, add QA checklists

### Pre-Push Checklist

If using Git hooks, these run automatically:

1. ESLint check (`npm run lint`)
2. Full test suite (`npm test -- --run`)
3. Coverage report

If any fail, push is blocked. Fix issues before retrying.

### Handling Build Failures

**Local build failure:**

1. Read error message carefully (file, line number, issue)
2. Check recent changes - what did you modify?
3. Run tests to identify breaking change
4. Revert if needed: `git checkout <file>`

**CI/CD build failure (Netlify, Vercel, GitHub Actions):**

1. Check build logs in CI platform
2. Reproduce locally: `npm run build`
3. Common issues:
   - Import errors (missing files, wrong paths)
   - Type errors (TypeScript strict mode)
   - Environment variables missing
   - CSS issues (Next.js CSS Modules, Tailwind)
4. Fix, commit, push again

**Emergency rollback:**

```bash
# Revert last commit (keep changes)
git reset --soft HEAD~1

# Revert last commit (discard changes)
git reset --hard HEAD~1

# Push force (use carefully!)
git push origin branch-name --force
```

## Common Issues & Solutions

### Build & Deployment Issues

#### CSS Modules rejecting `:root` selector (Next.js)

- **Issue:** `Selector ':root' is not pure (pure selectors must contain at least one local class or id)`
- **Solution:** Move CSS custom properties to `globals.css` or similar global stylesheet
- **Why:** CSS Modules enforce local scoping; `:root` is global and should be in global styles

#### Next.js treating components as routes

- **Issue:** Components in `pages/` directory are treated as routes, causing build errors
- **Solution:** Move components outside `pages/` (e.g., `components/`, `lib/`, `src/`)
- **Why:** Next.js pages router treats ALL files in `pages/` as routes

#### Import path errors after moving files

- **Issue:** `Cannot find module` errors after restructuring
- **Solution:** Use VS Code's "Find All References" to update imports systematically
- **Tip:** Search workspace for old paths using grep/search tools

### Testing Issues

#### "Multiple instances of Three.js being imported"

- Warning in tests, can be ignored
- Caused by React Three Fiber's dependency structure
- Doesn't affect production builds

#### "Not implemented: Window's scrollTo() method"

- JSDOM warning in tests, can be ignored
- `window.scrollTo()` not available in Node.js test environment
- Mock if needed: `window.scrollTo = jest.fn();`

#### "An update to X inside a test was not wrapped in act(...)"

- Wrap state updates in tests with `act()` from `@testing-library/react`
- Or use `waitFor()` for async state changes
- Example: `await waitFor(() => expect(result).toBe(expected));`

### Mobile/Touch Issues

#### Touch events not working on mobile

- Ensure `touch-action: none` in CSS for game controls
- Use native DOM events with `{ passive: false }` for `preventDefault()`
- React synthetic events are passive by default and can't call `preventDefault()`

#### Viewport height incorrect on mobile

- Use `dvh` (dynamic viewport height) instead of `vh`
- Or set CSS custom property with JS: `--vh: ${window.innerHeight * 0.01}px`

### Game-Specific Issues

#### Stale values in event handlers

- Use refs for values accessed in event handlers
- Update ref in `useEffect` when value changes
- See "State Management Patterns" section for full example

#### Socket reconnection warnings in solo mode

- Disable reconnection: `reconnection: false, autoConnect: false`
- Remove reconnection logic from solo/offline modes
- Only enable for multiplayer

## QA Validation Best Practices

When marking feedback as COMPLETED in `docs/FEEDBACK.md`:

1. **Add detailed QA checklist** - Step-by-step validation for each fix
2. **Include expected outcomes** - What should happen when testing
3. **Specify test environments** - Desktop browsers, mobile devices, screen sizes
4. **Console validation** - What should/shouldn't appear in browser console
5. **Technical summary** - Brief explanation of what was fixed and how
6. **Regression checks** - Ensure fix didn't break related functionality

**Example format:**

```markdown
## QA Review - Phase 7 - Round 2 ✅ COMPLETED

### QA Validation Checklist

#### 1. Player Movement Drift
- [ ] Launch game and move player ship with WASD/arrow keys
- [ ] Release keys and observe ship continues drifting
- [ ] Drift should last 1-2 seconds before stopping
- [ ] No console errors during movement
- [ ] Expected: Ship feels more "floaty" and maintains momentum

#### 2. Invincibility Effect Visual
- [ ] Collect invincibility power-up
- [ ] Observe halo ring effect (no wireframes)
- [ ] Colors cycle through rainbow spectrum
- [ ] Opacity at 50% with pulsing animation
- [ ] Console check: No warnings about effect rendering

### Technical Implementation Summary

**Fixed Files:**
- `Player.jsx` - Reduced DRAG_COEFFICIENT from 0.92 to 0.85
- `InvincibilityEffect.jsx` - Removed wireframes, added color cycling
- `ShieldEffect.jsx` - Removed wireframes, blue theme only

**Key Changes:**
- Physics: Increased drift by reducing drag coefficient
- Visual effects: Simplified to halo-only, reduced opacity
- Performance: Removed expensive wireframe geometries

**Testing:** All 42 tests passing, no regressions detected
```

## Resource Management

### Memory

- Clean up event listeners in `useEffect` cleanup functions
- Dispose Three.js geometries/materials when unmounting: `geometry.dispose()`, `material.dispose()`
- Clear intervals/timeouts: `clearInterval()`, `clearTimeout()`
- Remove refs when component unmounts: `ref.current = null`
- Dispose WebGL contexts properly in 3D games

### Performance

- Monitor FPS with performance tools (browser DevTools, custom FPS counter)
- Adjust quality settings based on device capability (detect GPU tier)
- Provide quality presets (low/medium/high/ultra) for user control
- Use object pooling for frequently created/destroyed objects (bullets, particles)
- Profile with Chrome DevTools: Performance tab, Memory tab
- Watch for memory leaks: Detached DOM nodes, closures, event listeners

### Network

- Minimize socket emissions (batch updates, throttle high-frequency events)
- Throttle high-frequency updates (player position, aim direction)
- Handle offline gracefully in solo/single-player modes
- Implement reconnection logic for multiplayer
- Show connection status to user (connected/disconnected/reconnecting)
- Use compression for large payloads (gzip, MessagePack)

## Communication Style

When working as a game development agent:

- **Be concise** - Short, direct answers for simple queries (1-3 sentences)
- **Be thorough** - Detailed explanations for complex issues (architecture, debugging)
- **Show, don't tell** - Code examples over long descriptions
- **Test-driven** - "Let me verify that works" > "That should work"
- **Proactive** - Identify related issues, suggest improvements before asked
- **Clear action items** - End responses with "What would you like me to do next?"
- **No jargon overload** - Explain technical terms when needed
- **Progress updates** - For multi-step work, provide checkpoints

## Development Environment Setup

### Key Commands (Adapt to Your Project)

```bash
# Development
npm run dev          # Start dev server
npm start            # Alternative start command

# Quality Checks
npm run lint         # Linting (ESLint, etc.)
npm test             # Run tests (watch mode)
npm test -- --run    # Run tests once (CI mode)
npm run build        # Production build

# Additional
npm run type-check   # TypeScript type checking
npm run format       # Code formatting (Prettier)
```

### Recommended Project Structure

```text
game-project/
├── docs/                    # Documentation and guides
│   ├── FEEDBACK.md          # QA feedback (priority #1)
│   ├── PHASE#.md            # Feature specifications
│   └── AGENT_GUIDE.md       # This file
├── src/ (or app/)           # Source code
│   ├── __tests__/           # Test files
│   ├── components/          # Reusable components
│   ├── pages/               # Route pages (if using router)
│   ├── contexts/            # React contexts/providers
│   ├── hooks/               # Custom hooks
│   ├── utils/               # Helper functions
│   ├── styles/              # CSS files
│   └── types/               # TypeScript types
├── public/                  # Static assets
│   ├── images/
│   ├── sounds/
│   └── models/
├── server/ (optional)       # Backend server
├── config/                  # Build configs
├── .gitignore               # Git ignore (include TODO.md!)
└── TODO.md                  # Local scratch (gitignored)
```

**Key directories:**

- `docs/` - Documentation lives here, not in root
- `FEEDBACK.md` - Always in `docs/`, checked first
- `TODO.md` - Root level, gitignored, scratch notes
- `__tests__/` - Tests co-located with source or in dedicated folder

## Final Reminders & Best Practices

### The Golden Rules

1. **Check `FEEDBACK.md` FIRST** - User feedback is highest priority
2. **Test early, test often** - Don't wait until commit time
3. **Update QA checklists** - Document how to validate your fixes
4. **Use refs for event handlers** - Prevent stale closure bugs
5. **Mobile is not optional** - Test touch, viewport, performance
6. **Document decisions** - Explain complex logic in comments/docs
7. **Pre-push hooks save you** - They catch errors before CI/CD
8. **Commit incrementally** - Small, atomic commits over large batches
9. **Clean up debug code** - No `console.log()` in production
10. **Read error messages carefully** - They usually tell you exactly what's wrong

### When You're Stuck

1. **Read the error message** - Line numbers, file paths, stack traces are your friends
2. **Check recent changes** - `git diff` shows what you modified
3. **Reproduce in isolation** - Create minimal test case
4. **Search codebase** - Use grep/search for similar patterns
5. **Check documentation** - Framework docs, GitHub issues, Stack Overflow
6. **Ask for help** - Provide error messages, code snippets, steps to reproduce

### Common Pitfalls to Avoid

- ❌ Committing without running tests
- ❌ Pushing to `main` instead of feature branch
- ❌ Leaving debug code (`console.log`, breakpoints)
- ❌ Ignoring linting warnings ("I'll fix it later")
- ❌ Making huge commits (500+ line changes)
- ❌ Not updating documentation after changes
- ❌ Assuming mobile works if desktop works
- ❌ Hardcoding values instead of using config files
- ❌ Skipping edge case handling
- ❌ Not cleaning up resources (event listeners, timers)

### Quick Reference Checklist

**Before starting work:**

- [ ] Check `docs/FEEDBACK.md` for priority items
- [ ] Read relevant `PHASE#.md` for context
- [ ] Run tests to ensure clean baseline
- [ ] Check `git status` for uncommitted changes

**During development:**

- [ ] Use `manage_todo_list` for complex multi-step work
- [ ] Commit incrementally (small, logical chunks)
- [ ] Run tests after each significant change
- [ ] Check linting regularly

**Before committing:**

- [ ] All tests pass
- [ ] Linting clean (no warnings)
- [ ] Build succeeds
- [ ] Update `FEEDBACK.md` with completion status
- [ ] Review diff for unintended changes/debug code
- [ ] Write clear commit message

**After pushing:**

- [ ] Monitor CI/CD build
- [ ] Test deployed preview (if available)
- [ ] Update team/stakeholders

---

**Document Version:** 2.0 (Agnostic/Framework-Independent)  
**Last Updated:** October 29, 2025  
**Target Audience:** AI agents working on game development projects
