# DARKMOON Product Roadmap

**Version:** 2.0  
**Last Updated:** November 23, 2025  
**Status:** Active Development

---

## Vision

Transform Darkmoon from a multiplayer tech demo into a production-ready 3D social gaming platform with exceptional mobile experience, scalable infrastructure, and engaging gameplay loops.

---

## Roadmap Overview

```bash
Q4 2025: Foundation & Mobile Fix (v1.1)
├── Fix critical mobile issues
├── Refactor monolithic components
└── Improve server stability

Q1 2026: Polish & Performance (v1.5)
├── Enhanced mobile UX
├── Optimized bundle size
└── Comprehensive test coverage

Q2 2026: Features & Scale (v2.0)
├── New game modes
├── User accounts & progression
└── Horizontal scaling infrastructure

Q3 2026: Social & Monetization (v2.5)
├── Social features
├── Cosmetic customization
└── Revenue streams

Q4 2026: Platform Expansion (v3.0)
└── Native mobile apps
```

---

## Phase 1: Foundation & Mobile Fix (v1.1)

**Timeline:** 4-6 weeks  
**Goal:** Fix P0 bugs, establish maintainable architecture

### Week 1-2: Critical Mobile Fixes (P0)

#### 🔴 Mobile Touch Controls

**Problem:** Joysticks and two-finger camera rotation not responding on mobile devices  
**Impact:** Game is unplayable on mobile

**Tasks:**

- [ ] Add comprehensive touch event logging to MobileJoystick.tsx
- [ ] Test on physical iOS (Safari) and Android (Chrome) devices
- [ ] Fix touch event preventDefault/stopPropagation issues
- [ ] Add passive event listener optimization
- [ ] Implement touch point tracking across rapid movements
- [ ] Add haptic feedback for touch interactions
- [ ] Create mobile control integration test suite

**Files to modify:**

- `src/components/MobileJoystick.tsx` (137 lines)
- `src/components/MobileButton.tsx` (60 lines)
- `src/components/characters/PlayerCharacter.tsx` (camera rotation handling)

**Acceptance Criteria:**

- ✅ Joystick responds to touch on iOS Safari and Android Chrome
- ✅ Two-finger camera rotation works smoothly
- ✅ No conflict with browser zoom/scroll gestures
- ✅ Test coverage >80% for mobile controls

**Estimated Effort:** 3-5 days

---

#### 🔴 Mobile UI Layout

**Problem:** Home page cards not visible, game UI covers controls in landscape

**Tasks:**

- [ ] Make home page cards responsive with swipe support
- [ ] Move dark mode toggle to bottom-right on mobile
- [ ] Ensure game UI adapts to portrait/landscape
- [ ] Test on various screen sizes (iPhone SE to iPad Pro)

**Files to modify:**

- `src/pages/Home.tsx` (215 lines)
- `src/styles/Home.css`
- `src/components/GameUI.tsx` (287 lines)

**Acceptance Criteria:**

- ✅ Home cards visible and swipeable on all mobile devices
- ✅ All controls accessible in both orientations
- ✅ Dark mode toggle never covered by game UI

**Estimated Effort:** 2-3 days

---

### Week 3-4: Code Architecture Refactoring (P1)

#### 🟡 Decompose Solo.tsx (1,002 lines → 4 files)

**Current structure:**

```bash
Solo.tsx (1,002 lines)
├── State management (20+ useState)
├── Socket connection logic
├── Bot AI coordination
├── Game loop orchestration
└── UI rendering
```

**New structure:**

```bash
pages/Solo/
├── index.tsx (150 lines) - Orchestration only
├── hooks/
│   ├── useSoloGame.ts (120 lines) - Game state
│   ├── useGameBots.ts (80 lines) - Bot management
│   └── useSocketConnection.ts (60 lines) - Socket logic
├── components/
│   ├── SoloScene.tsx (200 lines) - 3D scene
│   └── SoloHUD.tsx (150 lines) - UI overlay
└── config/
    └── botConfigs.ts (50 lines) - Bot configurations
```

**Tasks:**

- [ ] Extract socket connection to `useSocketConnection` hook
- [ ] Extract bot coordination to `useGameBots` hook
- [ ] Extract game state to `useSoloGame` hook
- [ ] Create SoloScene component for 3D rendering
- [ ] Create SoloHUD component for UI overlay
- [ ] Move bot configs to separate file
- [ ] Update tests to reflect new structure
- [ ] Verify no regression in gameplay

**Estimated Effort:** 5-7 days

---

#### 🟡 Decompose PlayerCharacter.tsx (900 lines → 5 hooks)

**Tasks:**

- [ ] Extract `usePlayerMovement` hook (150 lines)
  - WASD input handling
  - Velocity calculations
  - Sprint mechanics
- [ ] Extract `usePlayerCamera` hook (120 lines)
  - Mouse/touch camera controls
  - Sky cam toggle
  - Camera offset management
- [ ] Extract `usePlayerCollision` hook (100 lines)
  - Collision detection
  - Position validation
- [ ] Extract `usePlayerTagging` hook (80 lines)
  - Tag distance checks
  - Tag cooldown logic
- [ ] Extract `useJetpack` hook (60 lines)
  - Jump/jetpack physics
  - Double-jump logic
- [ ] Refactor PlayerCharacter.tsx to use extracted hooks (150 lines)

**Estimated Effort:** 6-8 days

---

#### 🟢 Create Unified Logger Utility

**Problem:** 4+ duplicate debug logger implementations

**Tasks:**

- [ ] Create `lib/utils/logger.ts` with namespaced logging
- [ ] Replace debug loggers in:
  - Solo.tsx
  - PlayerCharacter.tsx
  - GameManager.ts
  - useBotAI.ts
- [ ] Add log levels (debug, info, warn, error)
- [ ] Add optional log persistence for debugging
- [ ] Update ESLint rules to enforce logger usage

**Implementation:**

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
```

**Estimated Effort:** 1 day

---

### Week 5-6: Server Hardening (P1)

#### 🔴 Add Input Validation & Rate Limiting

**Tasks:**

- [ ] Install and configure `express-rate-limit`
- [ ] Add Zod schemas for socket events
- [ ] Validate position/rotation bounds
- [ ] Implement per-IP rate limits:
  - Chat: 10 messages/minute
  - Movement: 100 updates/second
  - Game actions: 5/second
- [ ] Add connection queue (max 100 concurrent)
- [ ] Implement backpressure handling

**Files to modify:**

- `server.js`
- Create `server/validation.js`
- Create `server/rateLimits.js`

**Estimated Effort:** 3-4 days

---

#### 🟡 Add Monitoring & Error Handling

**Tasks:**

- [ ] Integrate Sentry for error tracking
- [ ] Add structured logging (Winston or Pino)
- [ ] Create health check dashboard
- [ ] Add connection metrics (active users, messages/sec)
- [ ] Implement graceful shutdown
- [ ] Add socket connection error recovery

**Estimated Effort:** 2-3 days

---

### Deliverables - Phase 1

- ✅ Mobile controls fully functional
- ✅ Solo.tsx reduced from 1000 → 150 lines
- ✅ PlayerCharacter.tsx modularized into hooks
- ✅ Unified logging utility
- ✅ Server input validation
- ✅ Rate limiting implemented
- ✅ Error monitoring active
- ✅ All existing tests passing
- ✅ Mobile-specific tests added (>80% coverage)

---

## Phase 2: Polish & Performance (v1.5)

**Timeline:** 6-8 weeks  
**Goal:** Production-ready quality, optimized performance

### Week 7-9: Bundle Optimization

**Tasks:**

- [ ] Analyze bundle with visualizer
- [ ] Implement route-based code splitting
- [ ] Lazy load SpacemanModel 3D geometry
- [ ] Convert twitter-512.png to WebP (68KB → ~15KB)
- [ ] Remove unused dependencies (@splinetool, vite-plugin-bundle-analyzer)
- [ ] Implement dynamic imports for sound effects
- [ ] Add service worker for offline support
- [ ] Optimize Three.js imports (tree-shaking)

**Goal:** Reduce initial bundle by 25% (target: <500KB)

**Estimated Effort:** 4-5 days

---

### Week 10-12: Test Coverage Enhancement

**Current coverage:** ~60% (estimated)  
**Target coverage:** 85%

**Priority areas:**

- [ ] Mobile touch interactions (0% → 80%)
- [ ] Collision system edge cases (40% → 85%)
- [ ] Bot AI decision-making (20% → 75%)
- [ ] Socket connection resilience (50% → 90%)
- [ ] Game state transitions (60% → 90%)

**New test files needed:**

- `MobileJoystick.integration.test.tsx`
- `CollisionSystem.edge-cases.test.ts`
- `useBotAI.behavior.test.ts`
- `useSocketConnection.test.ts`
- `GameManager.state-machine.test.ts`

**Estimated Effort:** 6-8 days

---

### Week 13-14: CSS Architecture Refactor

**Current issues:**

- Global CSS namespace pollution
- Duplicate theme variables
- Desktop-first responsive design
- Inline styles in components

**Tasks:**

- [ ] Migrate to CSS Modules
- [ ] Create design token system (`lib/design-tokens.ts`)
- [ ] Centralize theme variables
- [ ] Convert to mobile-first media queries
- [ ] Extract inline styles from GameUI.tsx
- [ ] Create reusable UI component library:
  - Button
  - Card
  - Modal
  - Input

**Estimated Effort:** 5-6 days

---

### Week 15-16: Developer Experience

**Tasks:**

- [ ] Add Storybook for component development
- [ ] Create component documentation
- [ ] Add Playwright for E2E testing
- [ ] Improve error messages (user-friendly)
- [ ] Add debug overlay (FPS, network stats, hitboxes)
- [ ] Create developer setup video/guide
- [ ] Add VSCode snippets for common patterns

**Estimated Effort:** 4-5 days

---

### Deliverables - Phase 2

- ✅ Bundle size reduced by 25%
- ✅ Test coverage >85%
- ✅ CSS Modules implemented
- ✅ Design token system
- ✅ Storybook setup
- ✅ E2E tests for critical flows
- ✅ Production performance optimized (Lighthouse >90)

---

## Phase 3: Features & Scale (v2.0)

**Timeline:** 8-10 weeks  
**Goal:** New game modes, user accounts, scalable infrastructure

### New Game Modes

#### 1. Collectibles Mode

**Concept:** Gather floating orbs, player with most points wins

**Tasks:**

- [ ] Create Collectible component (3D model)
- [ ] Implement spawn/respawn logic
- [ ] Add score tracking UI
- [ ] Add power-ups (speed boost, magnet, shield)
- [ ] Create leaderboard

**Estimated Effort:** 2 weeks

---

#### 2. Race Mode

**Concept:** Checkpoint racing, speedrun leaderboards

**Tasks:**

- [ ] Design race track with checkpoints
- [ ] Implement lap timing system
- [ ] Add ghost racers (replay system)
- [ ] Create time trial mode
- [ ] Global leaderboard integration

**Estimated Effort:** 3 weeks

---

#### 3. Team Tag

**Concept:** 2v2 or 3v3 team-based tag

**Tasks:**

- [ ] Implement team assignment
- [ ] Add team-colored indicators
- [ ] Team chat system
- [ ] Team scoring logic
- [ ] Matchmaking system

**Estimated Effort:** 2 weeks

---

### User Accounts & Progression

**Tasks:**

- [ ] Implement authentication (Neon db)
- [ ] Create user profile system
- [ ] Add persistent stats (games played, wins, total tags)
- [ ] Implement XP/leveling system
- [ ] Create daily challenges
- [ ] Add achievement system
- [ ] Username + avatar selection

**Tech Stack:**

- Auth: Supabase Auth
- Database: Supabase PostgreSQL
- Real-time: Supabase Realtime (alternative to Socket.io)

**Estimated Effort:** 4 weeks

---

### Infrastructure Scaling

**Current limitations:**

- Single server instance
- Volatile in-memory state
- No database
- Limited to ~50 concurrent users

**Upgrades:**

#### 1. Redis Integration

- [ ] Session storage
- [ ] Game state persistence
- [ ] Leaderboard caching
- [ ] Rate limiting state

**Estimated Effort:** 1 week

---

#### 2. Database (PostgreSQL via Supabase)

- [ ] User accounts
- [ ] Game history
- [ ] Leaderboards
- [ ] Analytics data

**Estimated Effort:** 1 week

---

#### 3. Horizontal Scaling

- [ ] Implement sticky sessions (socket.io-sticky-session)
- [ ] Redis adapter for Socket.io
- [ ] Load balancer configuration
- [ ] Auto-scaling rules (Render.com or AWS)

**Target:** Support 500+ concurrent users

**Estimated Effort:** 2 weeks

---

### Deliverables - Phase 3

- ✅ 3 new game modes live
- ✅ User authentication & profiles
- ✅ Progression system (XP, levels, achievements)
- ✅ Redis + PostgreSQL integrated
- ✅ Horizontal scaling capable
- ✅ Support 500+ concurrent users

---

## Phase 4: Social & Monetization (v2.5)

**Timeline:** 6-8 weeks  
**Goal:** Community features, revenue streams

### Social Features

**Tasks:**

- [ ] Friends system
- [ ] Private lobbies (invite-only)
- [ ] Spectator mode
- [ ] In-game voice chat (optional, WebRTC)
- [ ] Emote system
- [ ] Player reporting/moderation
- [ ] Replay sharing (Twitter/Discord integration)

**Estimated Effort:** 5 weeks

---

### Customization & Cosmetics

**Tasks:**

- [ ] Character skins (5 free, 20 premium)
- [ ] Jetpack trails
- [ ] Tag effects
- [ ] Victory animations
- [ ] Username flair/badges
- [ ] Seasonal cosmetics

**Estimated Effort:** 3 weeks

---

### Monetization Strategy

#### Free-to-Play Model

**Revenue streams:**

1. **Cosmetic Shop** ($2-$10 items)
2. **Battle Pass** ($10/season, 3 months)
3. **Optional Ads** (watch ad for temporary boost)

**Tasks:**

- [ ] Integrate Stripe for payments
- [ ] Create shop UI
- [ ] Implement inventory system
- [ ] Design battle pass progression
- [ ] Add ad network (Google AdMob)
- [ ] Analytics for conversion tracking

**Estimated Effort:** 4 weeks

---

### Deliverables - Phase 4

- ✅ Friends & private lobbies
- ✅ Cosmetic shop with 25+ items
- ✅ Battle pass system
- ✅ Payment processing live
- ✅ Revenue tracking dashboard

---

## Phase 5: Platform Expansion (v3.0)

**Timeline:** 10-12 weeks  
**Goal:** Native mobile apps, expanded reach

### React Native App

**Why native?**

- Better performance (60 FPS)
- Push notifications
- App store discoverability
- Offline mode support

**Tasks:**

- [ ] Create React Native project (Expo)
- [ ] Port UI components
- [ ] Optimize Three.js for mobile (expo-gl)
- [ ] Implement native touch controls
- [ ] Add push notifications
- [ ] iOS App Store submission
- [ ] Google Play Store submission

**Estimated Effort:** 10-12 weeks

---

### Steam/Desktop Release (Optional)

**Tasks:**

- [ ] Electron wrapper
- [ ] Steam integration (achievements, leaderboards)
- [ ] Enhanced graphics settings
- [ ] Keyboard/mouse optimization
- [ ] Controller support

**Estimated Effort:** 6-8 weeks

---

## Success Metrics

### Phase 1 (v1.1)

- ✅ Mobile bounce rate <30%
- ✅ Average session time >5 min
- ✅ 0 critical bugs

### Phase 2 (v1.5)

- ✅ Page load time <2s
- ✅ Lighthouse score >90
- ✅ 95% uptime

### Phase 3 (v2.0)

- ✅ 10,000+ registered users
- ✅ 500+ concurrent users
- ✅ 50% mode variety (not just tag)

### Phase 4 (v2.5)

- ✅ $10,000 MRR
- ✅ 20% conversion rate (free → paid)
- ✅ 30% retention (D7)

### Phase 5 (v3.0)

- ✅ 100,000+ downloads
- ✅ 4.5+ star rating
- ✅ Featured on App Store

---

## Risk Mitigation

### Technical Risks

| Risk                      | Probability | Impact | Mitigation                                  |
| ------------------------- | ----------- | ------ | ------------------------------------------- |
| React 19 incompatibility  | Medium      | High   | Monitor ecosystem, maintain fallback branch |
| Mobile performance issues | High        | High   | Profile early, optimize progressively       |
| Server scaling challenges | Medium      | High   | Load test at 2x target capacity             |
| WebRTC latency            | Low         | Medium | Implement adaptive netcode                  |

### Business Risks

| Risk                       | Probability | Impact | Mitigation                                  |
| -------------------------- | ----------- | ------ | ------------------------------------------- |
| Low player retention       | Medium      | High   | Focus on core gameplay loop, fast iteration |
| Monetization underperforms | Medium      | High   | A/B test pricing, offer value bundles       |
| Competition                | High        | Medium | Differentiate with unique social features   |

---

## Resource Requirements

### Phase 1-2 (Foundation)

- 1 Full-stack Engineer (you)
- 1 Mobile Tester (contract)
- Budget: $2,000 (testing devices, monitoring tools)

### Phase 3-4 (Growth)

- 1 Full-stack Engineer
- 1 Backend Engineer (scaling)
- 1 UI/UX Designer (cosmetics)
- Budget: $5,000 (infrastructure, payment processing)

### Phase 5 (Expansion)

- 1 Full-stack Engineer
- 1 React Native Developer
- 1 DevOps Engineer
- 1 Community Manager
- Budget: $15,000 (app store fees, marketing)

---

## Conclusion

This roadmap balances **technical debt reduction** with **feature development** to create a sustainable, scalable multiplayer game platform.

**Key Philosophy:**

1. **Fix mobile first** - It's a critical blocker
2. **Refactor before scaling** - Clean code scales better
3. **Test everything** - Quality > speed
4. **Iterate based on data** - Analytics guide decisions

**Next Steps:**

1. Review and approve roadmap
2. Set up project tracking (GitHub Projects or Linear)
3. Begin Phase 1 Sprint Planning
4. Schedule weekly sync meetings

---

**Questions? Feedback?** Open an issue or discussion on GitHub.
