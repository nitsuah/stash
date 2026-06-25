# Tech Debt Tracker

**Last Updated:** November 25, 2025  
**Status:** Actively tracked

> **Note:** This document tracks actionable tech debt items. See QA issues in [TODO.md](./TODO.md)

---

## 🔴 Critical (P0) - Fix Immediately

### 1. Mobile Touch Controls Non-Functional

**Status:** 🔴 BLOCKING  
**Impact:** Game unplayable on mobile  
**Files:** `src/components/MobileJoystick.tsx`, `src/components/MobileButton.tsx`  
**Details:** Touch events not responding on iOS Safari and Android Chrome. Two-finger camera rotation not working.  
**Owner:** [Assign]  
**Due:** [Sprint 1]

**Action Items:**

- [ ] Add touch event logging
- [ ] Test on physical iOS/Android devices
- [ ] Fix preventDefault/stopPropagation issues
- [ ] Add mobile control integration tests

---

### 2. Solo.tsx Monolithic (1,002 lines)

**Status:** 🔴 URGENT  
**Impact:** Hard to maintain, test, and extend  
**Files:** `src/pages/Solo.tsx`  
**Details:** Game state, socket logic, bot AI, and rendering all in one file with 20+ useState hooks  
**Owner:** [Assign]  
**Due:** [Sprint 2]

**Action Items:**

- [ ] Extract `useSocketConnection` hook
- [ ] Extract `useGameBots` hook
- [ ] Extract `useSoloGame` hook
- [ ] Create `SoloScene` and `SoloHUD` components
- [ ] Move bot configs to separate file

**Target:** Reduce to <200 lines

---

### 3. PlayerCharacter.tsx Game Loop (900+ lines)

**Status:** 🔴 URGENT  
**Impact:** Complex testing, hard to debug  
**Files:** `src/components/characters/PlayerCharacter.tsx`  
**Details:** Movement, camera, collision, tagging, jetpack all in one useFrame hook  
**Owner:** [Assign]  
**Due:** [Sprint 2]

**Action Items:**

- [ ] Extract `usePlayerMovement` hook
- [ ] Extract `usePlayerCamera` hook
- [ ] Extract `usePlayerCollision` hook
- [ ] Extract `usePlayerTagging` hook
- [ ] Extract `useJetpack` hook

**Target:** Reduce to <200 lines

---

## 🟡 High Priority (P1) - Next Sprint

### 4. Server Lacks Input Validation

**Status:** ✅ COMPLETED  
**Impact:** Vulnerable to position spoofing, chat flooding (resolved)  
**Files:** `server.js`, `server/validation.js`  
**Details:** Resolved: Added validation schemas and rate limiting  
**Owner:** [Assign]  
**Completed:** Sprint 1

**Completed:**

- [x] Add validation schemas for socket events
- [x] Implement rate limiting (Map-based tracker)
- [x] Validate position/rotation bounds
- [x] Add per-action rate limits (MOVE: 100/s, CHAT: 10/min, GAME: 5/s)

---

### 5. Duplicate Debug Logger (4 implementations)

**Status:** ✅ COMPLETED  
**Impact:** Inconsistent logging, harder to debug (resolved)  
**Files:** `Solo.tsx`, `PlayerCharacter.tsx`, `GameManager.ts`, `useBotAI.ts`  
**Details:** Resolved: Created `lib/utils/logger.ts` and implemented across all files  
**Owner:** [Assign]  
**Completed:** Sprint 1

**Completed:**

- [x] Create `lib/utils/logger.ts` with namespaced logging
- [x] Replace all debug loggers with unified utility
- [x] Add log levels (debug, info, warn, error)

---

### 6. No Mobile-Specific Test Coverage

**Status:** 🟡 QUALITY ISSUE  
**Impact:** Mobile bugs slip through to production  
**Files:** `src/__tests__/`  
**Details:** Zero tests for touch interactions, orientation changes  
**Owner:** [Assign]  
**Due:** [Sprint 2]

**Action Items:**

- [ ] Create `MobileJoystick.integration.test.tsx`
- [ ] Create `MobileButton.test.tsx`
- [ ] Test portrait/landscape transitions
- [ ] Target 80%+ mobile control coverage

---

### 7. SoundManager.ts Too Large (621 lines)

**Status:** � IN PROGRESS — music layers extracted  
**Impact:** Easier to reason about procedural music and test its parts  
**Files:** `src/components/SoundManager.ts`, `src/components/musicLayers.ts`  
**Details:** Procedural music was extracted into `musicLayers.ts`. `SoundManager` now delegates music-layer creation and manages orchestration. Remaining work: split SFX helpers and further reduce `SoundManager` body to ~150 lines.

**Action Items:**

- [x] Extract `ProceduralMusic.ts` (implemented as `musicLayers.ts`)
- [ ] Extract `SoundEffects.ts` (split SFX helpers into separate module)
- [ ] Extract `AudioContext.ts` (centralize AudioContext creation/management)
- [ ] Keep SoundManager as orchestrator (~150 lines)

---

## 🟢 Medium Priority (P2) - Backlog

### 8. Commented-Out Spline Integration

**Status:** 🟢 DECISION NEEDED  
**Impact:** Code confusion, dependency bloat  
**Files:** `src/pages/Home.tsx`  
**Details:** Spline imports commented out, unclear if needed  
**Owner:** [Assign]  
**Due:** [Sprint 3]

**Action Items:**

- [ ] Decide: Remove permanently or create feature flag?
- [ ] If removing: uninstall `@splinetool` dependencies
- [ ] If keeping: implement proper lazy loading

---

### 9. Unused Assets

**Status:** 🟢 CLEANUP  
**Impact:** Unnecessary bundle size  
**Files:** `src/assets/emoji.ico`, `src/assets/emoji.png`  
**Details:** No references found in codebase  
**Owner:** [Assign]  
**Due:** [Sprint 4]

**Action Items:**

- [ ] Verify emoji files are truly unused
- [ ] Remove if confirmed unused
- [ ] Optimize twitter-512.png (68KB → WebP ~15KB)

---

### 10. CSS Architecture (Global namespace pollution)

**Status:** 🟢 REFACTOR NEEDED  
**Impact:** Risk of style conflicts, hard to maintain  
**Files:** `src/styles/*.css`, inline styles in components  
**Details:** No CSS modules, duplicate theme variables, inline styles  
**Owner:** [Assign]  
**Due:** [Sprint 5]

**Action Items:**

- [ ] Migrate to CSS Modules
- [ ] Create design token system
- [ ] Extract inline styles from GameUI.tsx
- [ ] Convert to mobile-first responsive design

---

### 11. Outdated Dependencies

**Status:** 🟢 MAINTENANCE  
**Impact:** Missing bug fixes and features  
**Files:** `package.json`  
**Details:** Prettier 2.x (latest 3.x), Husky 8.x (latest 9.x)  
**Owner:** [Assign]  
**Due:** [Sprint 6]

**Action Items:**

- [ ] Update Prettier to 3.x
- [ ] Update Husky to 9.x
- [ ] Test for breaking changes
- [ ] Monitor React 19 + R3F compatibility

---

### 12. Lobby.tsx Deprecated?

**Status:** 🟢 DECISION NEEDED  
**Impact:** Dead code in repo  
**Files:** `src/pages/Lobby.tsx` (119 lines)  
**Details:** Appears unused in favor of Solo.tsx  
**Owner:** [Assign]  
**Due:** [Sprint 7]

**Action Items:**

- [ ] Confirm Lobby.tsx is not used
- [ ] Archive or remove if confirmed
- [ ] Update tests if removed

---

### 13. Duplicate Profanity Filter

**Status:** 🟢 INCONSISTENCY  
**Impact:** Client/server filter mismatch  
**Files:** `src/lib/constants/profanity.ts`, `server/profanity.js`  
**Details:** Server uses env var, client has hardcoded list  
**Owner:** [Assign]  
**Due:** [Sprint 8]

**Action Items:**

- [ ] Share config via JSON file or npm package
- [ ] Ensure client/server parity
- [ ] Add tests for filter consistency

---

## 📊 Tech Debt Metrics

| Category                | Items  | Estimated Effort |
| ----------------------- | ------ | ---------------- |
| 🔴 Critical (P0)        | 3      | 4-6 weeks        |
| 🟡 High Priority (P1)   | 4      | 3-4 weeks        |
| 🟢 Medium Priority (P2) | 6      | 4-6 weeks        |
| **Total**               | **13** | **11-16 weeks**  |

---

## Completed ✅

_(Move items here as they're resolved)_

---

## Notes

- **Review Cycle:** Weekly during sprint planning
- **Prioritization:** Based on user impact, security risk, and development velocity
- **Effort Estimates:** T-shirt sizing (S=1-2d, M=3-5d, L=1-2w, XL=2-4w)

---

**Related Documents:**

- [TODO.md](./TODO.md) - QA checklist and open bugs
- [archive/](./archive/) - Historical analysis and planning docs
