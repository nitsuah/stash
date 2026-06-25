# Multiplayer Shooter Roadmap — "Robot Conker's Bad Fur Day"

repo: [[repos/darkmoon|darkmoon]]

**Status:** Phase 1 (tag stabilization) complete. Phase A (pluggable game modes)
complete. Phase B (combat primitives) complete. Phase C (deathmatch) complete end to
end — backend, gameplay wiring, and bot combat AI. Phase D (CTF) is now complete end to
end — backend (`CTFMode`, flags, teams, pickup/capture), gameplay wiring (Solo "Start
CTF", team/flag HUD), bot AI (chase/pickup/capture/defend), and CTF combat
(health/damage/respawn, flag-drop-on-death, bots fire at enemies in range without
abandoning their flag objective). Phase E (polish) is next.

## Context

`docs/CONKER_BFD_BUILD_GUIDE.md` is a generic implementation spec for a Conker's Bad Fur
Day-style game (context-sensitive actions, weapons, deathmatch, CTF, race, etc.). This
document translates that guide's relevant systems (Sections 5 and 9: Combat & Weapons,
Multiplayer Modes) into concrete, Darkmoon-anchored next steps — i.e. what to actually
change in _this_ codebase, in what order, building on the tag-mode foundation that now
lives in `src/components/GameManager.ts` and `src/components/characters/useBotAI.ts`.

Each phase below is a candidate for its own session/PR. Phases are ordered by
dependency: A is a prerequisite for B–D; E can happen incrementally alongside B–D.

---

## Phase A — Pluggable Game Modes (prerequisite for everything else) ✅ done

**Implemented:** `src/components/gameModes/GameModeHandler.ts` defines the
`onStart`/`onTick`/`onAction`/`onPlayerRemoved`/`onEnd` interface;
`src/components/gameModes/TagMode.ts` holds all tag-specific rules
(`TAG_BACK_COOLDOWN_MS`, `TAG_FREEZE_MS`, `lastTaggedById`, IT-transfer scoring).
`GameManager` is now a thin host that owns `players`/`gameState` and delegates to the
active `GameModeHandler` — its public API (`startTagGame`, `tagPlayer`,
`updateGameTimer`, `endGame`, `removePlayer`, ...) is unchanged, so no caller updates
were needed.

**Why first:** `GameManager.tagPlayer`/`startTagGame`/`endGame`/`pickNewItPlayer` currently
hardcode tag-specific rules (`TAG_BACK_COOLDOWN_MS`, `TAG_FREEZE_MS`, `lastTaggedById`,
IT-transfer scoring) directly inside `GameManager`. Adding deathmatch or CTF by extending
this class would tangle unrelated rule sets together, the same way the original tag-back
bug tangled IT-transfer with cooldown state.

**Plan:**

- Define a small `GameModeHandler` interface (new file, e.g.
  `src/components/gameModes/GameModeHandler.ts`):
  ```ts
  interface GameModeHandler {
    onStart(players: Map<string, Player>, gameState: GameState): void;
    onTick(deltaTime: number, gameState: GameState): void;
    onAction(action: GameAction, gameState: GameState): boolean; // returns handled/accepted
    onEnd(gameState: GameState): GameResult[];
  }
  ```
- Extract the current tag rules into `src/components/gameModes/TagMode.ts`, implementing
  `GameModeHandler`. `tagPlayer(taggerId, taggedId)` becomes an `onAction({ type: "tag",
taggerId, taggedId })` call routed through the active mode.
- `GameManager` becomes a thin host: owns `players`/`gameState`, holds the active
  `GameModeHandler`, and delegates `startTagGame`/`tagPlayer`/`updateGameTimer`/`endGame`
  to it. Keep the existing public method names/signatures so `Bots.tsx`,
  `PlayerCharacter.tsx`, and `Solo.tsx` callers don't need to change.
- `GameMode` union type (already `"none" | "tag" | "collectible" | "race" | "solo"`)
  becomes the registry key for mode handlers.

**Acceptance:**

- `src/__tests__/gameManager.core.test.ts` and `gameManager.edgeCases.test.ts` pass
  unchanged (or with mechanical updates only — no behavioral rewrites).
- `Bots.test.tsx`'s "blocks an immediate IT ping-pong..." test still passes, proving
  `TagMode` preserves the `lastTaggedById`/cooldown semantics from Phase 1.

---

## Phase B — Combat Primitives

**Goal:** introduce the minimum weapon/damage model needed by Phases C and D.

- ✅ **`WeaponManager`** (`src/components/combat/WeaponManager.ts`): registry of weapon
  configs (`laser`: `damage`, `range`, `cooldownMs`), `equip(weaponId)`/`unequip()`,
  `canFire(shooterId, now)`/`fire(shooterId, now)` with per-shooter cooldown tracking.
  Plain TS, no Three.js scene mutation — that stays in the React layer.
- ✅ **Hit detection**: `CollisionSystem.checkProjectileHit(origin, direction, range,
players, shooterId)` casts a ray and returns the closest hit `{ hitPlayerId, distance }`
  (or `null`), excluding the shooter and anyone outside the cone/range.
- ✅ **`Player` additions** (`GameManager.ts`): `health?: number`, `maxHealth?: number`,
  `respawnAt?: number`. Damage/respawn flow (mutate player, fire callback, mirroring
  `tagPlayer`) is implemented by the mode that needs it (Phase C `DeathmatchMode`).
- ✅ **Vertical slice + combat feel (Phases BG–BL)** — full in-game combat wiring plus a
  polish pass:
  - **BG** — bot shot tracer effects: every bot shot emits `"bot-shot-fired"` rendered as a coloured streak in `BotTracers.tsx`.
  - **BH** — per-weapon ammo + reload: `WeaponManager` gained `startReload`/`isReloading`/`getReloadProgress`; laser auto-reloads; R key manual reload; reload bar in `GameUI`.
  - **BI** — bot LOS wall check: `CollisionSystem.hasLineOfSight` raycasts against all boundary `Box3` objects; bots skip fire when a wall is in the way.
  - **BJ** — bot angular spread: 2D rotation-matrix deviation so bot misses fly to a visible off-target point.
  - **BK** — smooth player movement: `currentSpeedRef` scalar lerps at 10×/s on input and 15×/s to zero on release.
  - **BL** — player reticle + mouse-aimed firing: mouse NDC raycasted to ground plane for fire direction; CSS `+` crosshair at screen centre during active gameplay (PR #321).

**Acceptance:**

- ✅ `src/components/combat/__tests__/WeaponManager.test.ts` covers equip/cooldown/
  per-shooter tracking/unequip.
- ✅ `src/components/__tests__/CollisionSystem.test.ts` covers `checkProjectileHit`
  (direct hit, out-of-range, off-axis miss, behind-shooter, closest-of-multiple).

---

## Phase BM — Grenade Hold-to-Throw + Trajectory Arc

**Goal:** replace the grenade's instant laser-style fire with a hold-to-charge mechanic
and a dotted parabolic arc preview.

- Hold LMB with grenade equipped → render a dotted arc (small spheres along the
  parabolic trajectory) from the player's shoulder to the predicted landing zone; updates
  live as hold time / aim changes.
- Release LMB → fires the grenade along that arc; distance scales with hold duration,
  capped at max range.
- Existing `WeaponManager` grenade config (`damage`, `splashRadius`, `cooldownMs`,
  `maxAmmo: 3`) and `"weapon-explosion"` VFX unchanged.
- Mobile degrades gracefully: no arc preview; tap fires at max range.

**Files to change:** `PlayerCharacter.tsx` (hold/release detection replacing continuous
leftClick fire for grenade weapon), new `GrenadeArc.tsx` R3F component (dotted arc
mesh via parabola), `GameUI.tsx` (suppress ammo hint while arc is visible).

---

## Phase C — Deathmatch (maps to the build guide's `BeachMode`) ✅ done

- ✅ **`DeathmatchMode`** implements `GameModeHandler`: tracks kills via
  `gameState.scores`, a `killLimit`, and a respawn timer (`respawnAt` from Phase B).
- ✅ `onAction({ type: "hit", attackerId, targetId, damage })`: apply damage; on
  `health <= 0`, increment the attacker's kill score, set `respawnAt`, and the target
  sits out until the respawn delay elapses.
- ✅ **Gameplay wiring**: Solo mode's "Start Deathmatch" lobby button, live health/kill
  scoreboard in `GameUI.tsx`, and per-frame position sync (`GameManager.updatePlayerPosition`)
  so projectile hits land on moving targets.
- ✅ **Bot combat AI**: `useBotAI` gained a deathmatch branch — bots chase to
  `FIRE_RANGE`, fire lasers via a shared `WeaponManager` (authoritative cooldown), and
  sit out (pulsing) while downed awaiting respawn.

**Acceptance:** regression tests for kill tracking, respawn timing, end-of-game
results, gameplay wiring, and bot fire behavior all pass (`gameManager.deathmatch.test.ts`,
`usePlayerWeapon.test.ts`, `GameUI.test.tsx`, `useBotAI.unit.test.tsx`, `Bots.test.tsx`).

---

## Phase D — Capture the Flag (maps to the build guide's `HeistMode`)

- ✅ **Teams**: `Player.team?: "a" | "b"`. `CTFMode.onStart` assigns teams by
  alternating join order.
- ✅ **Flag entities**: `CTFFlag { team, position, basePosition, carrierId? }`, stored
  on `gameState.flags` (not on `Player`), one per team, spawned at `TEAM_A_BASE`/
  `TEAM_B_BASE`.
- ✅ **Pickup/capture**: `onAction({ type: "pickupFlag" | "captureFlag", playerId })` —
  pickup only succeeds for the _enemy_ team's unguarded flag within `PICKUP_RADIUS`;
  capture only succeeds while carrying the enemy flag and standing within
  `CAPTURE_RADIUS` of your own team's base, and increments `gameState.scores[team]`.
- ✅ **Carried-flag tracking**: `onTick` syncs a carried flag's position to its
  carrier; `onPlayerRemoved` returns a dropped flag to its base.
- ✅ **Gameplay wiring**: Solo mode's "Start CTF" lobby button (gated on 2+ players,
  mirroring "Start Deathmatch"), a team-colored HUD showing team assignment and
  team scores (`gameState.scores["a"]`/`["b"]`), a "carrying flag" indicator, and
  proximity-based pickup/capture (`GameManager.pickupFlag`/`captureFlag` called from
  `Solo.tsx`'s per-frame position sync).
- ✅ **Bot AI**: `useBotAI` gained a CTF branch — bots on a team head to the enemy
  flag while it's unguarded, carry it home (`captureFlag`) once picked up, and
  otherwise hold/return to their own base to defend it. `Bots.tsx` threads
  `team`/`isCarryingFlag` from `gameManager.getPlayers()`/`gameState.flags` down to
  `BotCharacter`, and `Solo.tsx`'s per-frame bot position handlers call
  `pickupFlag`/`captureFlag` for bots the same way they do for the player.
- ✅ **CTF combat ("bots with guns")**: `CTFMode` now initializes
  `health`/`maxHealth`/`respawnAt` on start (mirroring `DeathmatchMode`) and handles
  `onAction({ type: "hit", ... })` — damage reduces health, a lethal hit starts a
  respawn timer and drops any flag the target was carrying back to its base, and
  `onTick` restores health/clears `respawnAt` once the respawn delay elapses. No
  kill-score is tracked for CTF (capture remains the only scoring mechanism).
  `GameManager.hitPlayer` and `usePlayerWeapon.processFiring` now allow `mode ===
"ctf"`. `useBotAI`'s CTF branch gained a `targetTeam` prop — bots fire at enemies
  (never allies) within `FIRE_RANGE` opportunistically, without abandoning their
  flag-objective movement, and sit out (pulsing) while downed like in deathmatch.
  `GameUI`'s CTF HUD gained a health indicator alongside the team/score display.

**Acceptance:** ✅ `gameManager.ctf.test.ts` covers team assignment, flag spawning,
pickup (including the "can't capture your own team's flag" edge case via the
pickup-rejection check), range gating, flag-follows-carrier, capture/score/return,
carrier-disconnect, end-of-game team-score results, and combat (health init, damage,
lethal hit → respawn + flag drop, respawn restoration, rejecting hits on downed/inactive
players). ✅ `GameUI.test.tsx` covers the "Start CTF" lobby button and the
team/score/health/carrying-flag HUD. ✅ `useBotAI.unit.test.tsx` and `Bots.test.tsx`
cover CTF bot movement (chase unguarded flag, return when carrying, defend base when
enemy flag is guarded, hold at destination), combat (fire at enemy in range, no
friendly fire, range gating, sit out while downed), and prop wiring
(`team`/`isCarryingFlag`/`targetTeam`).

---

## Phase E — Polish

Incremental, can run alongside B–D:

- **Camera**: `PlayerCharacter.tsx` already manages a follow camera; add an "aiming" mode
  (over-the-shoulder offset, per build guide Section 10) when a weapon is equipped.
- **Audio**: extend `musicLayers.ts`/`soundEffects.ts` with a combat music layer that
  cross-fades in when `WeaponManager` reports recent fire/hit events, following the
  existing layered-music approach in `SoundManager.startBackgroundMusic`.
- **HUD**: `GameUI.tsx` gains health/ammo/kill/flag-status displays, gated by
  `gameState.mode` so tag mode's HUD is unaffected.

---

## Server-side tag parity (must-fix before Multiplayer Tag ships)

`FEATURES.md` lists Multiplayer Tag as `[planned]` (not live), so this is **not** a
current blocker — but it must be resolved before that feature ships, since it would
otherwise reintroduce the exact class of bug Phase 1 just fixed.

**Found in `server/index.js`:**

- The `player-tagged` handler (~lines 362–379) only checks
  `data.taggerId === gameState.itPlayerId` and that both clients exist — it has **no**
  equivalent of `TAG_BACK_COOLDOWN_MS` or `TAG_FREEZE_MS`, and trusts `data.taggedId` from
  the client with no server-side distance/eligibility check.
- The `disconnect` handler (~lines 393–409) deletes the disconnecting client from
  `clients` but never checks whether `gameState.itPlayerId === client.id`. If the IT
  player disconnects, `itPlayerId` keeps pointing at a non-existent client — no one can be
  tagged again until `game-end`/`game-start` resets it.

**Fix direction:** once Phase A lands, the server should hold a server-side
`GameManager`/`TagMode` instance as the source of truth (mirrors the client-authoritative
→ server-authoritative shift most multiplayer tag implementations need anyway), so the
same cooldown/freeze/IT-reassignment logic runs in one place. At minimum, before shipping:
port the `lastTaggedById`/cooldown/freeze checks into the `player-tagged` handler, and
reassign or clear `itPlayerId` (mirroring `GameManager.pickNewItPlayer`'s zero-players
branch) in the `disconnect` handler.

---

## Suggested sequencing

`A → B → C → D`, with `E` woven in incrementally. Server-side tag parity should be
addressed either as part of Phase A (if `TagMode` becomes shared client/server code) or
as a standalone fix immediately before Multiplayer Tag moves from `[planned]` to
`[in-progress]` in `FEATURES.md`.
