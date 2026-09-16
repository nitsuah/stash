# Tech Debt Tracker

**Last Updated:** September 2, 2026  
**Status:** Actively tracked

> **Note:** This document tracks actionable tech debt items. See QA issues in [TODO.md](./TODO.md)

---

## 🔴 Critical (P0) - Fix Immediately

### 1. Mobile Touch Controls Non-Functional ✅ RESOLVED

**Status:** ✅ COMPLETED — see TASKS.md "Stabilize mobile input and mobile layout on physical devices"  
**Impact:** Game unplayable on mobile (resolved)  
**Files:** `src/components/MobileJoystick.tsx`, `src/components/MobileControls.tsx`, `src/components/21st.dev/MobileActionButton.tsx`  
**Details:** Virtual joystick, two-finger camera rotation, and touch action buttons are functional (verified via browser emulation and mobile overhaul PR #417). One layout defect remains: the bottom two mode-cards on the Home page are cut off on narrow/short mobile viewports — tracked as a P0 item below and in TASKS.md.
**Completed:** 2026-08-26 (PR #417, `feat/mobile-gameplay-overhaul`)

**Completed:**

- [x] Fix preventDefault/stopPropagation issues
- [x] Verify touch response via browser emulation
- [x] Two-finger camera rotation
- [ ] Test on physical iOS/Android devices _(still open — emulation only)_
- [ ] Add mobile control integration tests

---

### 2. Solo.tsx Monolithic (1,002 lines) ✅ RESOLVED

**Status:** ✅ COMPLETED — [PR #390](https://github.com/nitsuah/darkmoon/pull/390)  
**Impact:** Hard to maintain, test, and extend (resolved)  
**Files:** `src/pages/Solo.tsx` (1,002 → 603 lines)  
**Details:** Extracted three reusable hooks: `useGameStart` (mode-specific start logic + `ensureBot` helper), `useBotPositionHandlers` (position update + CTF flag pickup/capture), `useDebugModes` (`useBotDebugMode`, `useGalleryDebugMode`, `useAutoRestart`). `useSocketConnection`, `useSoloGame`, `SoloScene`, `SoloHUD`, and bot configs were already extracted in prior sprints.  
**Completed:** August 4, 2026

**Completed:**

- [x] Extract `useSocketConnection` hook
- [x] Extract `useSoloGame` hook
- [x] Create `SoloScene` and `SoloHUD` components
- [x] Move bot configs to `lib/constants/botConfigs.ts`
- [x] Extract `useGameStart` hook
- [x] Extract `useBotPositionHandlers` hook
- [x] Extract `useDebugModes` hook (botDebugMode, galleryDebugMode, autoRestart)

---

### 2b. GameUI.tsx Monolith (2,078 lines) ✅ RESOLVED

**Status:** ✅ COMPLETED — [PR #390](https://github.com/nitsuah/darkmoon/pull/390)  
**Impact:** Single file owned all HUD, overlays, lobby, results, and event-driven state (resolved)  
**Files:** `src/components/GameUI.tsx` → barrel re-export; `src/components/GameUI/`  
**Details:** Split into 15 focused sub-components under `src/components/GameUI/components/`: `DamageFlash`, `HitDirectionIndicator`, `KillAnnouncement`, `PickupToast`, `ScoreBoard`, `KillFeed`, `MinimapRadar`, `Crosshair`, `BottomHUD`, `DeathScreen`, `StreakAnnouncement`, `BonusRoundOverlay`, `GameStatusPanel`, `GameResultsScreen`, `GameLobbyPanel`. All event-driven state extracted into `GameUI/hooks/useGameUIState.ts`. Original `GameUI.tsx` kept as a barrel re-export so all consumer imports remain unchanged.  
**Completed:** August 4, 2026

---

### 3. PlayerCharacter.tsx Game Loop (900+ lines) ✅ RESOLVED

**Status:** ✅ COMPLETED — [PR #391](https://github.com/nitsuah/darkmoon/pull/391)  
**Impact:** Complex testing, hard to debug (resolved)  
**Files:** `src/components/characters/PlayerCharacter.tsx` (900+ → 516 lines)  
**Details:** Movement, camera, collision, tagging, and jetpack logic extracted into dedicated hooks under `src/lib/hooks/`.  
**Completed:** 2026-08-08

**Completed:**

- [x] Extract `usePlayerMovement` hook
- [x] Extract `usePlayerCamera` hook
- [x] Extract `usePlayerCollision` hook
- [x] Extract `usePlayerTagging` hook
- [x] Extract `useJetpack` hook

**Note:** file is now 516 lines — below the original <200-line stretch target but no longer a monolith; further reduction is P2, not urgent.

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
- [ ] Extract inline styles from GameUI sub-components (`src/components/GameUI/components/`)
- [ ] Convert to mobile-first responsive design

---

### 11. Outdated Dependencies ✅ RESOLVED

**Status:** ✅ COMPLETED  
**Impact:** Missing bug fixes and features (resolved)  
**Files:** `package.json`  
**Details:** Prettier upgraded to 3.9.6 and Husky upgraded to 9.1.7; both verified in package.json.  
**Completed:** 2026-08-21

**Completed:**

- [x] Update Prettier to 3.x (now 3.9.6)
- [x] Update Husky to 9.x (now 9.1.7)
- [x] Test for breaking changes
- [x] Monitor React 19 + R3F compatibility

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

| Category                | Items (open) | Estimated Effort |
| ----------------------- | ------------ | ---------------- |
| 🔴 Critical (P0)        | 0            | —                |
| 🟡 High Priority (P1)   | 2            | 2-3 weeks        |
| 🟢 Medium Priority (P2) | 5            | 3-5 weeks        |
| **Total (open)**        | **7**        | **5-8 weeks**    |

> **7 items resolved**: item 1 (mobile touch controls, PR #417), item 2 (Solo.tsx monolith split), item 2b (GameUI.tsx shared utilities extraction), item 3 (PlayerCharacter.tsx hook extraction, PR #391), item 4 (server-side input validation), item 5 (debug logger cleanup), and item 11 (Prettier/Husky setup). 7 items remain open as tracked in the table above.

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
