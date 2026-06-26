# 🌾 Farm RTS: Complete Game Manual & North Star Plan

> _A browser-based isometric real-time strategy game with a farm theme — inspired by Warcraft 3 and StarCraft_

---

## Vision (North Star)

Build a browser-based, isometric real-time strategy (RTS) game inspired by Warcraft 3 and StarCraft, with a farm theme. The MVP should deliver the core gameplay loop: base building, resource gathering, unit management, and combat vs. AI enemies. The experience should be smooth, responsive, and fun — even if simplified and "on rails" at first.

---

## 1. Core Gameplay Systems

### 1.1 Resource System

| Resource | Farm Equivalent      | Gathered By                               | Stored At        |
| -------- | -------------------- | ----------------------------------------- | ---------------- |
| Gold     | Coins / Market Sales | Farmer (Worker) at Market Well            | Barn (Town Hall) |
| Lumber   | Hay / Wood           | Farmer (Worker) at Haystacks / Tree grove | Lumber Shed      |
| Food     | Grain / Feed         | Produced passively by Grain Silos         | N/A (supply cap) |
| Upkeep   | Farm Population      | Consumed by each unit                     | Farmhouses       |

**Resource Rules (Warcraft 3 parity):**

- Workers carry a fixed amount per trip (e.g., 10 gold, 10 lumber) and must return to the Barn to deposit.
- Resources are displayed in the top resource bar: `🪙 Coins: 500 | 🌾 Hay: 200 | 🍞 Food: 12/24`
- **Supply cap**: Each unit costs food. Farmhouses (equivalent of WC3 farms) expand supply cap. Max cap: 100.
- **Upkeep tiers** (optional stretch): 0–40 food = no upkeep penalty; 41–70 = reduced income; 71–100 = heavy penalty.

### 1.2 Resource Gathering (Worker Mechanics)

- Workers auto-gather when ordered to a resource node.
- Workers auto-return to nearest Barn when full.
- Workers auto-resume gathering after depositing unless ordered otherwise.
- Workers can be queued: right-click a node then shift+right-click Barn to set a return loop.
- Multiple workers can harvest the same node simultaneously (diminishing returns after 5 workers per node).
- Resource nodes have finite capacity (e.g., haystacks deplete and disappear).
- **Replanting**: Workers can plant new tree groves if a Seed Shed structure has been built (equivalent to WC3 wisps planting trees).

---

## 2. Map & World

### 2.1 Isometric Grid

- Tile-based isometric grid (e.g., 64x64 map, each tile = 32x32 px base).
- Terrain types: grass, dirt, water (impassable), crops, rocky soil.
- Pathfinding: A* or Theta* on a grid — supports diagonal movement.
- Cliff/height levels: 2 levels (flat field, elevated barn hill) — units on high ground gain a ranged attack bonus.

### 2.2 Camera

- WASD / arrow keys: smooth pan.
- Mouse edge-scroll: optional (toggle in settings).
- Scroll wheel: zoom in/out (2 levels minimum).
- Middle-mouse drag: pan.
- Minimap click: jump camera to location.
- `Spacebar`: snap camera to selected unit or last event.

### 2.3 Fog of War (Stretch)

- Black = unexplored (never seen).
- Dark overlay = explored but not currently visible.
- Full color = currently in a unit/building's vision radius.
- Vision range varies by unit type (e.g., Scarecrow has high range, Piglet has low).

### 2.4 Minimap

- Bottom-right corner.
- Shows terrain color, friendly units (green), enemy units (red), resources (yellow).
- Clickable to move camera. Right-click minimap: move selected units.
- Flashing pings on minimap when units are attacked.

---

## 3. Buildings

### 3.1 Building Placement

- Click a building from the build menu → cursor shows ghost preview.
- Green ghost = valid placement; Red ghost = blocked (terrain, overlap, out-of-range).
- Buildings must be placed within a "buildable zone" radius of an existing structure (optional; WC3 uses creep constraint).
- Placement snaps to grid tiles.
- Worker walks to location and begins construction animation.
- Multiple workers on the same building speeds up construction.
- Buildings have HP during construction; enemies can attack partially built structures.

### 3.2 Building Types

#### Tier 1 — Foundation

| Building    | Farm Name      | Function                                        | Cost              | Build Time | HP   |
| ----------- | -------------- | ----------------------------------------------- | ----------------- | ---------- | ---- |
| Town Hall   | **Barn**       | Central hub; trains workers; deposits resources | — (starts built)  | —          | 1200 |
| Farm        | **Farmhouse**  | +6 food supply per structure                    | 80 Coins, 20 Hay  | 15s        | 400  |
| Lumber Mill | **Hay Shed**   | Unlocks wood upgrades; required for Tier 2      | 120 Coins, 60 Hay | 20s        | 500  |
| Altar       | **Silo Tower** | Trains hero units                               | 180 Coins, 40 Hay | 30s        | 600  |
| Scout Tower | **Windmill**   | Vision structure; upgradeable to attack tower   | 60 Coins, 30 Hay  | 10s        | 200  |

#### Tier 2 — Expansion

| Building       | Farm Name     | Function                               | Cost               | Requires              |
| -------------- | ------------- | -------------------------------------- | ------------------ | --------------------- |
| Barracks       | **Stable**    | Trains melee/ranged combat units       | 150 Coins, 80 Hay  | Hay Shed              |
| Arcane Sanctum | **Apiary**    | Trains spellcaster units (Beekeeper)   | 200 Coins, 100 Hay | Hay Shed + Silo Tower |
| Workshop       | **Tool Barn** | Trains siege units (Tractor, Haywagon) | 200 Coins, 120 Hay | Hay Shed              |
| Blacksmith     | **Forge**     | Upgrades unit armor and weapons        | 100 Coins, 60 Hay  | Stable                |

#### Tier 3 — Late Game (Stretch)

| Building       | Farm Name           | Function                           |
| -------------- | ------------------- | ---------------------------------- |
| Castle         | **Grand Farmstead** | Upgrades Barn; unlocks elite units |
| Keep           | **Manor**           | Intermediate upgrade of Barn       |
| Gryphon Aviary | **Dove Tower**      | Trains flying units                |

### 3.3 Building Upgrades

- Barn → Keep (Manor) → Castle (Grand Farmstead): two upgrade steps, each unlocking stronger workers and abilities.
- Scout Tower → Guard Tower (Watchtower) → Cannon Tower (Slingshot Tower): attack strength and range upgrades.

### 3.4 Repairing Buildings

- Any Worker ordered to a damaged building will begin repairing it for a lumber/coin cost proportional to HP restored.
- Cannot repair buildings under attack.

---

## 4. Units

### 4.1 Worker Units

**Farmer** (equivalent: WC3 Peasant/Peon)

| Stat       | Value              |
| ---------- | ------------------ |
| HP         | 250                |
| Damage     | 8 (melee, minimal) |
| Armor      | 0                  |
| Speed      | Medium             |
| Carry Cap  | 10 Coins / 10 Hay  |
| Train Cost | 75 Coins           |
| Train Time | 15s                |
| Hotkey     | F                  |

**Abilities:**

- Gather resources (coins/hay)
- Build structures
- Repair structures
- Harvest crops (interact with crop fields for bonus resources)

Multiple Farmers can be queued in the Barn (up to 5 in queue).

### 4.2 Combat Units

#### Melee Units

| Unit           | Farm Name             | HP         | Damage | Armor | Cost              | Requires       |
| -------------- | --------------------- | ---------- | ------ | ----- | ----------------- | -------------- |
| Footman        | **Farmhand**          | 420        | 12-13  | 2     | 135 Coins         | Stable         |
| Knight         | **Draft Horse Rider** | 825        | 21-27  | 5     | 245 Coins, 60 Hay | Stable + Forge |
| Paladin (Hero) | **Harvest Champion**  | 700 (hero) | 25-35  | 5     | Silo Tower        |

#### Ranged Units

| Unit     | Farm Name             | HP  | Damage         | Range   | Cost              | Requires       |
| -------- | --------------------- | --- | -------------- | ------- | ----------------- | -------------- |
| Rifleman | **Scarecrow Slinger** | 365 | 16-22          | 5 tiles | 205 Coins, 30 Hay | Stable + Forge |
| Mortar   | **Haywagon**          | 320 | 60-70 (splash) | 8 tiles | 180 Coins, 70 Hay | Tool Barn      |

#### Spellcaster Units

| Unit      | Farm Name     | Abilities                                  | Cost              | Requires |
| --------- | ------------- | ------------------------------------------ | ----------------- | -------- |
| Priest    | **Beekeeper** | Heal, Slow Poison (honey debuff)           | 135 Coins, 30 Hay | Apiary   |
| Sorceress | **Herbalist** | Polymorph (turns enemy into chicken), Slow | 155 Coins, 40 Hay | Apiary   |

### 4.3 Hero Units

Heroes are powerful unique units trained at the Silo Tower. One hero per Silo Tower; max 3 heroes per game (stretch).

**Hero Stats:**

- Have XP and level (1–10).
- Gain XP from killing enemies and completing quests.
- Each level grants +stat bonuses and ability unlocks.
- Heroes drop items on death but revive at the Silo Tower after a delay (and a gold cost).
- Heroes can carry up to 6 items in an inventory.

**Example Hero — Harvest Champion (Paladin equivalent):**

| Level | HP   | Damage | Key Abilities                   |
| ----- | ---- | ------ | ------------------------------- |
| 1     | 700  | 25-35  | Harvest Blessing (heal ally),   |
| 5     | 1200 | 55-70  | + Sunstrike (AoE stun)          |
| 10    | 2000 | 95-120 | + Season's Wrath (ultimate AoE) |

---

## 5. Unit Control (Warcraft 3 Controls)

### 5.1 Selection

| Action                             | Control             |
| ---------------------------------- | ------------------- |
| Select single unit                 | Left-click          |
| Box select                         | Left-click drag     |
| Add to selection                   | Shift + left-click  |
| Select all units of type on screen | Double-click unit   |
| Select all units on map            | Ctrl + A            |
| Select hero                        | F1 / F2 / F3        |
| Select idle worker                 | F9 (cycles through) |

### 5.2 Control Groups

| Action                       | Control            |
| ---------------------------- | ------------------ |
| Assign group                 | Ctrl + 1–9         |
| Select group                 | 1–9                |
| Select group + center camera | Double-tap 1–9     |
| Add to existing group        | Shift + Ctrl + 1–9 |

Up to 12 units per control group. Control groups persist until overwritten.

### 5.3 Movement & Orders

| Action              | Control                                                      |
| ------------------- | ------------------------------------------------------------ |
| Move to location    | Right-click ground                                           |
| Attack-move         | A + left-click (attacks enemies encountered en route)        |
| Hold position       | H (unit won't chase fleeing enemies)                         |
| Stop                | S                                                            |
| Patrol              | P + left-click (cycles between two points, attacks on sight) |
| Force attack ground | A + left-click on ground (for splash damage)                 |
| Follow unit         | Right-click on friendly unit                                 |
| Queue orders        | Shift + right-click (multiple waypoints)                     |

### 5.4 Formation Movement

- Units in a selection move in formation by default.
- Formation types (stretch): Tight cluster, spread line, staggered (set in settings or via hotkey).

### 5.5 Unit Stances

- **Aggressive**: Auto-chases and attacks enemies in vision range.
- **Defensive**: Attacks enemies in range but doesn't pursue far.
- **Hold**: No pursuit — stands firm.
- **Passive**: Never auto-attacks (useful for workers).

---

## 6. Combat System

### 6.1 Attack Types & Armor Types

| Attack Type        | Strong vs.                | Weak vs.             |
| ------------------ | ------------------------- | -------------------- |
| Normal (Farmhand)  | Medium armor              | Heavy armor          |
| Piercing (Slinger) | Light armor, unarmored    | Heavy, fortified     |
| Siege (Haywagon)   | Fortified (buildings)     | Medium, light        |
| Magic (Herbalist)  | Heavy armor               | Not vs. magic immune |
| Hero               | All types (reduced bonus) | —                    |

| Armor Type | Units                |
| ---------- | -------------------- |
| Unarmored  | Workers, critters    |
| Light      | Scout units, casters |
| Medium     | Standard melee       |
| Heavy      | Knights              |
| Fortified  | Buildings            |
| Hero       | Hero units           |

### 6.2 Combat Resolution

- Attack speed: measured in attacks/second (e.g., 0.67 = every 1.5s).
- Damage = base damage + dice roll (e.g., 12-16 = base 12, +0–4 random).
- Armor reduces damage by a percentage per armor point.
- Units auto-attack nearest enemy in range unless given explicit orders.

### 6.3 Abilities & Spells

- Active abilities: click ability icon (or press hotkey) then click target.
- Passive abilities: always active, no input needed.
- Cooldown shown as a timer overlay on the ability icon.
- Mana bar displayed under HP bar when unit is selected (for spellcasters and heroes).

### 6.4 Creep Camps (Neutral Enemies)

Neutral enemy camps are scattered across the map. Clearing them grants:

- XP for heroes.
- Dropped items (equipment pickups).
- Sometimes control of a neutral building (e.g., a Goblin Shop → Farm Supply Store).

Creep camps respawn after a delay (optional; WC3 standard behavior).

---

## 7. AI Enemy (Bot Opponent)

### 7.1 AI Behavior States

| State       | Trigger            | Behavior                             |
| ----------- | ------------------ | ------------------------------------ |
| Build Phase | 0–5 min            | Expands base, gathers resources      |
| Harass      | 5–10 min           | Sends small squads to attack workers |
| Push        | 10+ min            | Sends full army to player base       |
| Defend      | When base HP < 50% | Pulls units back, fortifies          |

### 7.2 AI Difficulty Levels

| Difficulty            | Worker Efficiency | Attack Timing      | Army Size |
| --------------------- | ----------------- | ------------------ | --------- |
| Easy (Seedling)       | 70%               | 8 min first attack | Small     |
| Normal (Farmer)       | 100%              | 5 min first attack | Medium    |
| Hard (Harvest Master) | 130%              | 3 min first attack | Large     |

### 7.3 AI Build Path (Example)

1. Trains 5 Farmers immediately.
2. Builds Farmhouses until 24 food.
3. Builds Hay Shed.
4. Builds Stable at 4 min.
5. Trains 6 Farmhands.
6. Sends attack at 6 min.
7. Builds Forge at 8 min; upgrades armor.

---

## 8. Tech Tree & Upgrades

### 8.1 Weapon & Armor Upgrades (Forge)

| Upgrade           | Effect               | Cost              | Time |
| ----------------- | -------------------- | ----------------- | ---- |
| Iron Pitchfork I  | +1 damage, all melee | 100 Coins, 50 Hay | 60s  |
| Iron Pitchfork II | +2 damage, all melee | 175 Coins, 75 Hay | 75s  |
| Harvest Armor I   | +1 armor, all ground | 100 Coins, 50 Hay | 60s  |
| Harvest Armor II  | +2 armor, all ground | 175 Coins, 75 Hay | 75s  |

### 8.2 Structural Upgrades (Hay Shed / Apiary)

| Upgrade            | Effect                       | Cost              |
| ------------------ | ---------------------------- | ----------------- |
| Improved Gathering | Workers carry +5 resources   | 100 Coins         |
| Faster Hands       | Construction speed +20%      | 80 Coins, 40 Hay  |
| Bee Synergy        | Beekeeper heals for 25% more | 125 Coins         |
| Mechanical Plow    | Tractor siege damage +15%    | 150 Coins, 80 Hay |

---

## 9. Items & Shops

### 9.1 Hero Inventory

- Heroes have 6 item slots.
- Items are picked up by moving the hero over them or clicking.
- Items can be dropped (right-click → drop), given to allies, or sold at a shop.
- Consumables (e.g., Healing Salve → Chicken Soup): single use; restore HP over time.

### 9.2 Farm Supply Store (Goblin Shop equivalent)

A neutral building on the map (captured or visited without needing ownership):

| Item               | Farm Name         | Effect                        | Cost      |
| ------------------ | ----------------- | ----------------------------- | --------- |
| Healing Salve      | Chicken Soup      | +200 HP regen over 15s        | 100 Coins |
| Mana Potion        | Honeycomb         | +150 Mana                     | 50 Coins  |
| Cloak of Shadows   | Scarecrow Cloak   | Grants temporary invisibility | 200 Coins |
| Boots of Speed     | Horseshoes        | +60 movement speed            | 150 Coins |
| Tome of Experience | Seed of Knowledge | +100 XP to hero               | 150 Coins |

### 9.3 Item Combining (Stretch)

Combine two basic items to create a more powerful item (WC3 recipe system):

- Chicken Soup + Horseshoes = Swift Recovery Bandana (HP regen + move speed)
- Seed of Knowledge + Honeycomb = Scholar's Hive (+5 to all stats)

---

## 10. Win / Lose Conditions

### 10.1 Standard Victory

- Destroy the enemy's Barn (Town Hall equivalent).
- If the enemy has a Keep/Manor/Grandstead, all must be destroyed.

### 10.2 Defeat

- Your Barn is destroyed (and no Keep/Manor exists).

### 10.3 Alternative Scenarios (Stretch)

| Mode             | Win Condition                                    |
| ---------------- | ------------------------------------------------ |
| Survival         | Survive X waves of enemy attacks                 |
| Resource Race    | First to gather 5000 total resources             |
| Escort           | Get a Wagon from A to B before time runs out     |
| King of the Hill | Hold the center pasture for 3 cumulative minutes |

---

## 11. UI & HUD

### 11.1 Resource Bar (Top)

```
[🪙 Coins: 345]  [🌾 Hay: 120]  [🍞 Food: 18/30]  [⏱ 12:34]
```

### 11.2 Unit Info Panel (Bottom Left)

When a single unit is selected:

- Unit portrait
- Unit name, level (if hero)
- HP bar (green → red)
- Mana bar (blue, if applicable)
- Current order/state icon
- Stats summary (damage, armor, speed)

When multiple units are selected:

- Grid of unit portraits (up to 12)
- Click portrait to sub-select and focus camera

### 11.3 Command Card (Bottom Right)

- 3×3 or 4×3 grid of ability/action icons.
- Hovering shows tooltip: name, hotkey, description, mana cost, cooldown.
- Grayed-out = insufficient resources or wrong target.
- Glowing = ready to use / recommended.

### 11.4 Building Queue Panel

When a building is selected:

- Shows current training queue (up to 5 slots).
- Click a queued unit to cancel and refund 75% cost.
- Progress bar on currently training unit.

### 11.5 Minimap (Bottom Right or Bottom Left)

- 200×200 px map overview.
- Click to move camera. Right-click to order selected units.
- Toggle fog of war overlay (stretch).
- Alert pings visible for 10 seconds.

### 11.6 Alert System

- Flashing icon + minimap ping when:
  - A unit is under attack.
  - A building is under attack.
  - A unit finishes training.
  - A research completes.
- Player can configure alert sounds and visual priority.

---

## 12. Game Settings & Accessibility

| Setting            | Options                                          |
| ------------------ | ------------------------------------------------ |
| Game Speed         | Slow / Normal / Fast                             |
| AI Difficulty      | Seedling / Farmer / Harvest Master               |
| Map Size           | Small (32×32) / Medium (64×64) / Large (128×128) |
| Fog of War         | Off / On                                         |
| Auto-queue Workers | On / Off (auto-queues workers when Barn is idle) |
| Edge Scrolling     | On / Off                                         |
| Camera Zoom        | 2 / 3 levels                                     |
| Sound Volume       | 0–100% (separate music/SFX)                      |

---

## 13. Milestone Roadmap

### Milestone 1 — Core Map & Camera ✅ (MVP)

- [ ] Isometric tile grid renders correctly
- [ ] Smooth WASD + mouse-edge camera pan
- [ ] Zoom levels (2 minimum)
- [ ] Tile types: grass, dirt, water, trees, rocks
- [ ] Debug overlay: show grid, tile coordinates, FPS

### Milestone 2 — Main Building & UI (MVP)

- [ ] Barn renders on map at starting position
- [ ] Top resource bar (Coins, Hay, Food)
- [ ] Bottom command card (placeholder buttons)
- [ ] Unit info panel renders (static/mock data)
- [ ] Build menu opens from Barn

### Milestone 3 — Resource Nodes (MVP)

- [ ] Tree groves (Hay nodes) render and are finite
- [ ] Coin well (Gold node) renders and is finite
- [ ] Resource node depletion logic
- [ ] Visual feedback when node is empty

### Milestone 4 — Worker Unit (MVP)

- [ ] Farmer unit renders and animates
- [ ] Single click selects, right-click moves
- [ ] Farmer walks to resource node
- [ ] Farmer gathers and returns to Barn
- [ ] Carry capacity + deposit logic
- [ ] Resource bar updates on deposit
- [ ] Multiple Farmers can be selected (box select)
- [ ] Idle worker hotkey (F9)

### Milestone 5 — Building Construction (MVP)

- [ ] Build menu shows available buildings
- [ ] Ghost preview on placement
- [ ] Valid/invalid tile detection (red/green)
- [ ] Worker walks to build site and constructs
- [ ] Building progresses from scaffold to complete
- [ ] Multiple workers speed up construction
- [ ] Farmhouse increases food cap

### Milestone 6 — Resource System (MVP)

- [ ] Food supply cap enforced (can't train units over cap)
- [ ] Insufficient resource error messages
- [ ] Resource refund on building cancel
- [ ] Upkeep warning at 80% food cap

### Milestone 7 — Win / Lose Condition (MVP)

- [ ] Static enemy base on opposite side of map
- [ ] Player can attack enemy Barn
- [ ] Victory screen when enemy Barn destroyed
- [ ] Defeat screen when player Barn destroyed
- [ ] Restart and main menu buttons

### Milestone 8 — Combat & Units

- [ ] Stable building + Farmhand unit
- [ ] Attack-move command (A + click)
- [ ] Basic combat resolution (HP, damage, armor)
- [ ] Unit death animation + removal
- [ ] Attack type vs. armor type system
- [ ] Hold / Stop / Patrol stances

### Milestone 9 — AI Enemy

- [ ] AI gathers resources
- [ ] AI builds base over time
- [ ] AI sends attack wave on timer
- [ ] AI difficulty presets (Easy, Normal, Hard)
- [ ] AI attacks player workers as harassment

### Milestone 10 — Hero System (Stretch)

- [ ] Silo Tower trains Hero
- [ ] Hero has XP, levels, abilities
- [ ] Hero inventory (6 slots)
- [ ] Hero revival on death (cost + timer)
- [ ] Creep camps with XP reward

### Milestone 11 — Upgrades & Tech Tree (Stretch)

- [ ] Forge building
- [ ] Weapon/armor upgrades with effect applied
- [ ] Hay Shed unlocks required for Tier 2
- [ ] Upgrade queue UI

### Milestone 12 — Polish & Stretch (Stretch)

- [ ] Minimap with fog of war
- [ ] Sound effects + background music
- [ ] Particle effects (combat hits, resource pickup)
- [ ] Screen shake on large explosions
- [ ] Save / load game state
- [ ] Additional map scenarios (Survival, Race)
- [ ] Replay system (very stretch)

---

## 14. Technical Architecture Notes

### Recommended Stack

| Layer            | Technology                                          |
| ---------------- | --------------------------------------------------- |
| Renderer         | HTML5 Canvas or PixiJS (WebGL)                      |
| Language         | TypeScript                                          |
| Pathfinding      | A\* on tile grid (heapq priority queue)             |
| Game Loop        | `requestAnimationFrame`, fixed timestep             |
| State Management | Plain objects / event bus (no React needed for MVP) |
| Audio            | Howler.js                                           |
| Build Tool       | Vite                                                |

### Entity-Component Pattern (Recommended)

Each game object (unit, building, resource node) is an entity with components:

- `PositionComponent` — tile x/y
- `RenderComponent` — sprite reference, animation state
- `SelectableComponent` — can be clicked/boxed
- `MovementComponent` — speed, pathfinding state
- `GatherComponent` — (workers only) carry cap, target node
- `CombatComponent` — HP, damage, armor, attack speed
- `BuildingComponent` — (buildings only) queue, HP, footprint

### Performance Targets

- 60 FPS with 80 units on screen
- Map size: up to 128×128 tiles without lag
- Unit pathfinding: <5ms per recalculation
- No visible stutter during resource deposit loops

---

## 15. Art & Audio Direction

### Art Style

- Colorful, slightly cartoonish isometric tiles.
- Units: chunky, readable silhouettes (farmhands in overalls, horses, beekeepers).
- Buildings: recognizable farm architecture (red barn, wooden shed, stone windmill).
- Palette: warm yellows, greens, browns — friendly and pastoral.

### Audio

- Background: ambient farm sounds (birds, wind, distant rooster).
- Music: upbeat acoustic folk during building phase; tense fiddle/drum during combat.
- SFX: unit acknowledgment voices (e.g., "Yes, farmer!", "Right away!"), building sounds, resource pings.

---

## 16. Glossary

| Term             | Definition                                              |
| ---------------- | ------------------------------------------------------- |
| Barn             | Town Hall equivalent; central base building             |
| Farmer           | Worker unit; gathers resources and constructs buildings |
| Hay              | Lumber equivalent resource                              |
| Coins            | Gold equivalent resource                                |
| Farmhouse        | Farm/Supply Depot equivalent; increases food cap        |
| Silo Tower       | Altar of Kings equivalent; trains heroes                |
| Harvest Champion | Paladin-class hero unit                                 |
| Creep Camp       | Neutral enemy group guarding items and XP               |
| Upkeep           | Gold income penalty when near food cap (stretch)        |
| Control Group    | A numbered group of units assigned to keys 1–9          |
| Attack-Move      | A+click command: move and attack any enemy in path      |
| Ghost Preview    | Semi-transparent building preview during placement      |

---

_Last updated: Project inception. Update this document with each milestone completion. All feature implementations and todos should reference a milestone number from Section 13._

## Related

- [[repos/farm-3j/docs/farm.png|farm.png]] — RTS map/asset reference image
- [[repos/farm-3j/docs/FARM-RTS-NORTH-STAR|FARM-RTS-NORTH-STAR]] — project north star and MVP goals
- [[repos/farm-3j/docs/FARM-RTS-TODO|FARM-RTS-TODO]] — active implementation checklist

## Assets

- ![[farm.png]] — RTS map reference image
