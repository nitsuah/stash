# TASKS

Last Updated: 2026-09-02 (docs audit, MapRenderer Phase 2b componentization, home page redesign)

## Farm RTS — Round 2 (2026 Q3)

### Technical Cleanup

- [x] Extract blacksmith upgrade costs to shared config constants — `BLACKSMITH_STEEL_EDGE_COSTS`/`BLACKSMITH_IRON_HIDE_COSTS` in `constants.ts`; `TechTab`'s disable logic already consumes them, not hardcoded (2026-08-07)
- [ ] Continue SVG component extraction — worker body shapes, enemy unit torsos, and building base rects are next candidates
- [ ] Profile render loop at 30+ units on 25×25 map; investigate canvas/OffscreenCanvas fallback for mobile
- [ ] Add unit tests for core helpers: `tileDist`, `tileToSvg`, A\* pathfinding (damage formulas ✅ covered by towerHelpers/spawnHelpers tests)

### Gameplay Features

- [ ] Named unit formations — move selected group in line/wedge/box formation
- [ ] Enemy hero unit — Warlord (wave 20+, unique abilities, drops loot)
- [ ] Dropped hero items — equippable pickups from slain elite enemies (Speed Boots, War Banner, Healing Totem)
- [x] Save slots — 3 cloud-backed slots (0/1/2) with localStorage fallback via hybrid persistence system (2026-08-07); slot picker UI on New Game screen still TBD
- [ ] Achievement / challenge system — milestone badges for specific run conditions
- [ ] Campaign mode Phase 1 — 3 hand-crafted scenarios with scripted objectives

### Content & Polish

- [ ] Background ambient audio loop with independent volume slider
- [ ] More unit voice lines and enemy audio cues (Warchief stomp, Sapper countdown)
- [ ] Minimap: show dropped items and loot crate positions
- [ ] Ensure farmers always render in front of barn and remain selectable when barn is clicked

---

## Farm RTS MVP (2026 Q2–Q3)

- [ ] Complete all MVP milestones as defined in docs/Farm_RTS_Game_Manual.md and docs/FARM-RTS-TODO.md
  - Progress: Milestone 1 complete; Milestone 3 (resource node depletion/feedback) complete
  - Priority: P0
  - Acceptance Criteria: All core gameplay systems (map, camera, resource, worker, building, win/lose) are playable and validated in Docker.

## Legacy Tycoon Tasks (on hold)

- [ ] Complete Farm Tycoon phase 2 core systems (animal needs, feeding, fence, save/load)
- [ ] Refresh README and deployment notes with actual release path.
- [ ] Build content and discovery surfaces (gallery, blog, SEO, accessibility)
- [ ] Plan and implement ecommerce phase 1.

## Unfinished Todos (RTS Farm Game)

- [x] Add stone resource nodes (2026-06-26)
- [x] Add box selection for multiple units (2026-06-26)
- [x] Wire up Stop command in command card (2026-06-26)
- [x] Real unit info panel (state, carrying, multi-select count) (2026-06-26)
- [x] Population/food cap system (2026-06-26)
- [x] Add animal units (chickens) with grazing AI — 5 chickens spawn near barn, wander to adjacent tiles every 2s, stay within 5 tiles of barn, respect water/tree tiles, only render in fog-clear tiles; SVG bird with body/head/beak/comb/legs (2026-07-02)
- [x] Difficulty selection screen — Easy/Normal/Hard picker before game starts
- [x] Additional sound effects — unit ready (training complete), hero ability, garrison, swordsman charge sounds added; FEATURES.md updated to document iter84-96 features (2026-07-02)
- [x] Resource depletion alerts + more sounds — 🌲 Depleted! / 🪙 Mine Depleted! / 🪨 Quarry Depleted! floating text when node hits zero; cavalry sprint + hero Battle Shout sounds wired (2026-07-02)
- [x] Tower range rings — faint dashed ellipses show attack radius for all built defensive towers (watchtower grey, frost blue, ballista gold, poison green); range ellipse also shown during build-mode ghost placement (2026-07-02)
- [x] Ctrl+click add/remove from selection — holding Ctrl while clicking a unit toggles it in/out of the current selection; standard WC3/AoE micro mechanic; hint added to HUD tooltip bar (2026-07-02)
- [x] Barn attack sound — Snd.hit() plays when grunts deal damage to player barn (2026-07-02)
- [x] Unit voice acknowledgements (iter100) — WC3-style text on move/attack commands; per-unit-type lines; random pick from pool
- [x] Ghost-shot fix (iter101) — troll archer and demolisher setTimeout callbacks check alive status before dealing damage; eliminates barn damage from dead units
- [x] Combat damage log (iter102) — 📋 panel logs every hit to player barn with source + timestamp; last 20 entries; clear button
- [x] Game starts paused (iter103) — speed starts at 0; ⏸ PAUSED overlay; ▶ Start / ⏸ Pause / ▶▶ 2× button label cycle
- [x] Wave timer pause/resume (iter103) — remaining time saved on pause; timer restarted from remaining ms on unpause
- [x] Spacebar pause toggle (iter108) — Space key toggles pause/unpause
- [x] Enemy spawn distance (iter104) — grunts spawn at far map edges (x=24/y=24); flanking grunts spawn from east/south edges
- [x] Passive barn regen (iter105) — +1 HP/5s when no grunts on map
- [x] Enemy last-stand enrage (iter105) — grunts enraged at ≤50% enemy barn HP; 💢 LAST STAND! banner
- [x] Destructible archer tower (iter101) — purple Archer Tower converted to EnemyTower (id=-1, 120 HP); 40🪙 loot on death
- [x] Enemy AI auto-build (iter106) — tower every 90s + wall every 60s from wave 5 onward
- [x] Enemy flanking (iter107) — wave 8+, every 4th wave: 2 grunts from east+south edges; ⚠ FLANKING! text
- [x] Barn damage visual states (iter108) — smoke at <50% HP, fire at <25% HP on both barns; ☠ COLLAPSING! on enemy barn; per-unit-type lines (farmer/swordsman/cavalry/hero/siege); random pick from pool; shown as gold floating text above speaker unit; README updated to reflect 25×25 map, audio, all new features (2026-07-02) (watchtower grey, frost blue, ballista gold, poison green); range ellipse also shown during build-mode ghost placement so players can preview coverage before committing (2026-07-02); Easy: 300g/160l/60s + 70% grunt HP/dmg + 40% longer wave intervals; Hard: 80g/40l/15s + 150% HP, 140% dmg, 20% faster speed, 30% faster waves; difficulty badge shown in HUD; DifficultyConfig type shared between RTSGameRoot and RTSMap (2026-07-02)
- [ ] Implement grazing logic and food meter
- [x] Enable building placement on valid tiles — ghost preview + valid/invalid tile detection (2026-06-26)
- [ ] Ensure farmers render in front of barn and are always selectable
- [x] Lay groundwork for control groups (Ctrl+1-9) (2026-06-26)
- [ ] Add buttons to train animal units from Barn
- [x] Fog of war — tile visibility driven by unit/building vision radius; dark/dim/clear states (2026-06-26)
- [x] Enemy base + win/lose condition (Milestone 7) — enemy barn at (10,10) with HP bar, attack on right-click, victory overlay (2026-06-26)
- [x] A\* pathfinding — workers and grunts avoid water; 8-directional grid search (2026-06-26)
- [x] Enemy grunts — spawn every 25s, pathfind to player barn, reduce barn HP, defeat overlay on 0 HP (2026-06-26)
- [x] Functional minimap — real-time SVG minimap showing all units and buildings (2026-06-26)
- [x] Worker vs grunt combat — right-click grunt to attack; workers chase and deal ATTACK_DAMAGE per tick (2026-06-26)
- [x] Grunt proximity aggro — grunts within 2 tiles of a worker attack it instead of marching to barn (2026-06-26)
- [x] Rally point — right-click tile with barn selected; new workers auto-walk there on train (2026-06-26)
- [x] Formation movement — multi-unit move spreads workers to offset tiles around target (2026-06-26)
- [x] Tech research upgrades — Sharper Tools / Swift Harvest / Iron Will, 2 levels each, gated on farmhouse (2026-06-26)
- [x] Floating damage numbers — animated SVG text on all damage/heal events, color-coded, rises and fades (2026-06-26)
- [x] Auto-repair — idle workers near barn regen 2 HP/2s with green +2 float (2026-06-26)
- [x] Wave escalation — grunts stronger/faster each wave; double-assault every 3rd; HUD wave counter + banner (2026-06-26)
- [x] Game speed toggle — 1×/2× button multiplies animation dt (2026-06-26)
- [x] Kill counter + score — live ☠ HUD counter; end-screen Battle Report with 6 stats (2026-06-26)
- [x] Enemy archer tower — static tower near enemy barn fires arrows at workers in range; 10 dmg/2.5s; disappears with barn (2026-06-26)
- [x] Worker patrol — P key / Patrol button; workers cycle between two waypoints; dashed route line shown on selection; Stop cancels (2026-06-26)
- [x] Palisade wall building — blocks enemy grunt pathfinding; workers can build them anywhere; creates tactical chokepoints (2026-06-26)
- [x] Windmill building — passive +2 gold every 5s per windmill; floating gold text on each tick (2026-06-26)
- [x] Barracks building + Swordsman unit — Barracks (80g/60l/40s) enables training ⚔️ Swordsmen (50g, 80HP, +10 dmg bonus, can't harvest); distinct dark-red visual; damage bonus stacks with Sharper Tools upgrade (2026-06-26)
- [x] Save/load game state — full localStorage persistence; auto-save every 30s + on tab close; 💾 Save and 🗑 New Game buttons in resource bar; Play Again clears save (2026-06-26)
- [x] Day/night cycle — 60s day / 45s night loop; night darkens map with SVG overlay; grunts move 30% faster at night; resource bar and border tint to indigo at night; phase announcement banners; progress bar shows time remaining (2026-06-26)
- [x] Garrisoning — right-click barn or click 🏰 Garrison button to send selected units inside (cap 5); units heal 5 HP/s; each garrisoned unit reduces grunt barn damage by 2 (max 8); barn border turns cyan when occupied; 🚪 Deploy button releases all units (2026-06-26)
- [x] Hero unit (Barnabas) — unique 🦸 hero recruitable from Barracks (150g, 150HP, +20 dmg); crown SVG + gold border; ⚡ Rallying Cry ability deals 30 AoE damage to all grunts within 3.5 tiles; 25s cooldown shown in command card (2026-06-26)
- [x] Siege Workshop + Catapult unit — Siege Workshop (100🪙 80🌲 60🪨) enables training 🪨 Catapults (150g/80l, 60HP); catapults auto-fire AoE splash at grunts within 6 tiles (22 direct / 11 splash, 3.5s cooldown); slow movement; distinct SVG (wooden frame, wheels, throwing arm, boulder); can't harvest or garrison (2026-06-26)
- [x] Player watchtowers fire defensive arrows — watchtowers shoot 8 dmg at nearest grunt within 5 tiles every 2s; floating 🏹 hit text; creates AoE/Warcraft-style defensive tower lines (2026-06-26)
- [x] Grunt gold drops — each grunt killed drops 5🪙 with floating text; Warcraft-style loot incentive for engaging enemies (2026-06-26)
- [x] Market building — Market (80🪙 60🌲 20🪨) enables trading: sell 50🌲 for 30🪙 or 30🪨 for 20🪙 via command card buttons; AoE-style economy layer for converting surplus resources (2026-06-26)
- [x] Stable building + Cavalry unit — Stable (80🪙 60🌲 30🪨) enables 🐴 Cavalry (60🪙, 65HP, 3× speed, +8 dmg); horse+rider SVG; cannot harvest; shares vet/blacksmith upgrades (2026-07-01)
- [x] Lumber Shed passive bonus — each Lumber Shed reduces lumber gather interval by 200ms (stacks with Swift Harvest, min 400ms); AoE-style economic building that actually rewards building drop sites near forests (2026-07-01)
- [x] Enhanced minimap — minimap now renders tree/gold/stone resource nodes, all placed buildings, and uncleaned creep camp markers; legend below map; taller map panel for readability (2026-07-01)
- [x] Player barn defense fire — barn auto-fires 🏰-6 dmg at nearest grunt within 4 tiles every 3s (Town Center mechanic); dashed ring around barn when under siege; defense stat shown in barn command card (2026-07-01)
- [x] Hero second ability: Harvest Boon — 🌾 all farmers gather 2× faster for 10s; 40s cooldown; active state shown on button; boon applies to gold/lumber/stone; WC3-style hero economic support ability (2026-07-01)
- [x] Enemy fortress escalation — enemy base spawns destroyable 🏹 archer towers at waves 5/10/15 (60 HP, 9 dmg, 4.5-tile range); right-click to attack; tower HP bars displayed; red dots on minimap; wave announcement "ENEMY TOWER BUILT!"; makes late-game sieging feel like AoE/WC3 fortress assault (2026-07-01)
- [x] Guard Tower research — 120🪙 80🪨 one-time research upgrades all watchtowers to Guard Towers (+7 dmg: 8→15, +1 range: 5→6); 🏰 emoji on shots; button in farmhouse card when watchtower is built; AoE-style tower upgrade tech (2026-07-01)
- [x] Hero Morale Aura — hero alive within 3 tiles speeds up all unit attacks by 30% (1200ms→840ms); dashed golden ring on affected units; getMoraleMs() helper used at all 4 attack timeout sites; WC3-style passive hero aura (2026-07-01)
- [x] Idle worker alert — yellow ! badge above idle farmers; orange ! above idle combat units; keeps player aware of unassigned units like AoE's worker alert (2026-07-01)
- [x] Enemy Boss Grunt (War Bull) — spawns on every 10th wave alongside regular grunts; 3× HP, 25 barn dmg (vs 12), 80 XP reward, 20🪙 gold drop; distinct bull SVG with horns, red eyes, and WAR BULL label; 💀 wave banner; WC3/AoE-style boss difficulty spike (2026-07-01)
- [x] Neutral creep camps — 3 camps of 2 purple boar creeps; aggro 3.5 tile range, leash; +60🪙 loot on clear; grant XP to killing unit; right-click to attack (2026-07-01)
- [x] Granary building — Granary (50🪙 80🌲 20🪨) adds +8 food cap on placement; stackable silo SVG; AoE-style dedicated pop-cap building cheaper than Farmhouse (2026-07-01)
- [x] Unit veterancy — combat units earn XP per kill; level 1 at 40 XP (+10 HP +5 atk), level 2 at 120 XP (+10 HP +5 atk); ⭐ badges on SVG; XP bar in command panel; stacks with all other bonuses (2026-07-01)
- [x] Blacksmith building — Blacksmith (100🪙 60🌲 80🪨) enables ⚔️ Steel Edge (2 levels, +5 atk per level all units) and 🛡️ Iron Hide (2 levels, -2 dmg taken per level from grunts); stone forge SVG with chimney; AoE/Warcraft-style dedicated upgrade building (2026-07-01)
- [x] Spike Trap building — Spike Trap (30🪙 20🌲 10🪨) deals 20 dmg to any grunt stepping within 0.8 tiles; 30s rearm cooldown per trap; shows armed (yellow spikes) vs recharging (gray spikes) state; build button in farmhouse command card; stackable in chokepoints for layered ground defense; WC3/AoE-style terrain trap (2026-07-01)
- [x] Unit Training Queue — Swordsman and Cavalry training now takes 8s instead of being instant; up to 5 units can be queued per click; progress bar and unit-icon queue shown in command card; "⚔️ Ready!" / "🐴 Ready!" floating text on spawn; AoE/WC3-style queued training that rewards forward planning (2026-07-01)
- [x] Auto-gather on resource depletion — when a farmer's tree/stone node runs dry after returning resources, it automatically pathfinds to the nearest non-empty node of the same type instead of going idle; AoE-style villager auto-reassignment that keeps economy flowing without micromanagement (2026-07-01)
- [x] Command hotkeys — F=train farmer, Q=train swordsman, R=train cavalry, Del=stop selected units, G=garrison; hotkey hints shown in buttons and HUD tooltip bar; AoE/WC3-style keyboard shortcuts for experienced players (2026-07-01)
- [x] Resource shortage alerts — gold <30, lumber <20, stone <10 flash red in HUD with pulse animation; food at cap shows ⚠ warning in red; AoE-style visual alert that surfaces economy bottlenecks without interrupting gameplay (2026-07-01)
- [x] Fog of war on enemy units — enemy grunts and enemy fortress towers only render when their tile is within player vision radius (fogVisible check); adds WC3/AoE tension where threats approach unseen through the fog (2026-07-01)
- [x] Next wave countdown timer — live ⏱ Xs countdown in HUD showing seconds until next grunt wave; pulses red when ≤5s; 1s tick interval drives re-render; AoE/WC3-style wave warning that lets players prepare defenses in time (2026-07-01)
- [x] Minimap click-to-pan — clicking anywhere on the minimap pans the main camera to center on that tile position; cursor:crosshair on minimap SVG; coordinates mapped from minimap SVG space to tile space to camera translate; AoE/WC3 standard navigation feature (2026-07-01)
- [x] Ctrl+A select all units — Ctrl+A selects all living player units; added to HUD hint bar; AoE/WC3 all-select hotkey for rapid army assembly (2026-07-01)
- [x] Cavalry Sprint [S] + Trample — Sprint ability [S key] gives cavalry 2× speed for 5s (20s cooldown); sprinting cavalry show amber glow + ⚡ lightning bolt; passive Trample deals 6 dmg/s to any grunt within 0.8 tiles while cavalry are moving; sprint button in command card shows cooldown; WC3/AoE mounted cavalry mechanics adding micro skill ceiling (2026-07-01)
- [x] Swordsman Charge ability [C] — press C with swordsman(s) selected to instantly deal 2× damage to the nearest grunt; 12s per-unit cooldown tracked individually; charge button in command card shows cooldown countdown; C hotkey added to HUD tooltip; stacks with Sharper Tools + Blacksmith upgrades; WC3/AoE unit active ability adding micro skill ceiling to swordsmen (2026-07-01)
- [x] Enemy AI target priority — grunts prioritize attacking military buildings (barracks/siege workshop/stable rank 5-4, watchtower 3, blacksmith 2, farmhouse 1) over general buildings when adjacent; also re-path toward highest-priority building when idle; WC3/AoE-style smart AI that makes players actively defend their army production (2026-07-01)
- [x] Shared XP on kill — when a unit kills a grunt, allied units within 3 tiles receive 25% of the kill XP (10 per grunt, 20 per boss); encourages grouping and army cohesion; stacks with attacker XP for faster leveling of support units; WC3-style shared experience mechanic (2026-07-01)
- [x] Watchtower garrison — right-click a watchtower with units selected to garrison up to 3 units inside; each garrisoned unit adds +4 tower damage and +0.5 tile range; cyan border + 👥×N label on occupied towers; Deploy button in farmhouse command card per tower; units restore food on deploy; AoE2-style garrisoned tower mechanic rewarding defensive investment (2026-07-01)
- [x] Attack-Move command [A] — press A with combat units selected then right-click a destination; units march but auto-engage any enemy grunt or creep within 2.5 tiles; resume march after kill until reaching destination; red ⚔️ Attack-Move mode banner in HUD; Esc cancels; A hotkey hint added to tooltip bar; SC2/AoE/WC3 staple micro mechanic (2026-07-01)
- [x] Building repair by workers — right-click any damaged building with units selected to send them to repair it; workers enter 🔧 Repairing state; +5 HP every 2s with green float; damaged buildings show orange border + "🔧 REPAIR" hint; fully repaired buildings return workers to idle; WC3/AoE-style villager repair mechanic (2026-07-01)
- [x] Building damage from grunts — placed buildings now have HP (farmhouse 200, watchtower 180, barracks 250, etc.); grunts within 1.2 tiles attack buildings for 8 dmg/1.5s; destroyed buildings removed from map; HP bars shown on damaged buildings (green→yellow→red); old saves migrated to add HP; WC3/AoE strategic depth where players must defend entire base not just barn (2026-07-01)
- [x] Building fire & burn damage — buildings below 25% HP show animated fire+smoke SVG overlay; additionally take 1 HP/s passive burn damage unless actively repaired by a worker; encourages players to prioritize repairs during sieges; AoE2/WC3-style building destruction tension (2026-07-01)
- [x] Loot Crates — resource caches (30🪙 or 25🌲 or 20🪨 etc.) appear at 6 random map positions every 45s; send farmers to right-click/collect; floating resource text on pickup; golden chest SVG with glowing border; AoE2/SC2 relic-style active map resource that rewards map control and exploration (2026-07-01)
- [x] Hold Position command [H] — press H or click 🛡️ Hold button; combat units stand still and auto-attack any enemy within 1.8 tiles without chasing; 🛡️ shield icon above unit; movement orders cancel hold; Stop/Del clears it; H hotkey added to tooltip bar; WC3/AoE/SC2 defensive micro mechanic essential for holding chokepoints and tower lines (2026-07-01)
- [x] Enemy War Ram siege unit — slow battering ram spawns wave 6+ every 3rd wave; 200 HP, deals 40 dmg/3s to nearest building or barn; right-click to attack; XP+gold reward on kill; dark wooden ram SVG with wheels; red rectangle on minimap; attack-move auto-engages; 🪵 wave announcement; AoE2/WC3-style siege unit forcing players to deal with priority threats or lose buildings (2026-07-01)
- [x] Shift+right-click waypoint queuing — hold Shift and right-click to queue multiple movement destinations for selected units; units execute each waypoint in order, A\*-pathing to each in sequence; Stop/Delete clears queue; idle units start immediately on first Shift+click; AoE2/WC3-style waypoint chaining for pre-planned patrol routes and multi-point maneuvers (2026-07-01)
- [x] Goblin Sapper suicide bomber — sprints toward nearest wall/building, explodes on contact for 80 AoE damage in 1.5-tile radius (workers, buildings, barn all take damage); 25 HP / 1.3× speed — fastest enemy in game; right-click to intercept; attack-move and hold-position auto-target; 20🪙 + 45 XP on defuse; red X on minimap; red urgency pulse ring when within 3 tiles of target; 💥 wave 12 banner "Kill it before it reaches your walls!"; WC3/AoE2-style suicide unit that forces immediate response or suffers catastrophic base damage (2026-07-01)
- [x] Enemy Troll Archer ranged unit — green troll with bow spawns wave 10+ every 5th wave; fires 🏹 arrows at nearest worker for 8 dmg/2.5s from 4 tile range; kites backwards when melee units close within 3 tiles; attacks barn when no workers in range; right-click to attack; 12🪙 + 30 XP on kill; orange triangle on minimap; attack-move/hold-position auto-target; wave 10 banner "TROLL ARCHER! Flank with cavalry!"; WC3/AoE2-style ranged enemy forcing players to use cavalry flanks or catapult splash (2026-07-01)
- [x] Enemy Shaman healer unit — green-robed shaman spawns wave 8+ every 4th wave; marches to player barn but heals nearby injured grunts within 2.5 tiles for 5 HP every 2s; green pulse ring when healing; right-click to attack; 15🪙 gold + 35 XP on kill; attack-move and hold-position auto-target shamans; SHAMAN minimap dot (bright green); wave banner warns "SHAMAN SPAWNS! Kill the healer!"; WC3-style priority kill target that punishes players who ignore support units (2026-07-01)
- [x] Frost Tower defensive building — ❄️ Frost Tower (80🪙 40🌲 60🪨, 160 HP) fires every 2.5s at nearest grunt in 4.5-tile range; deals 5 dmg and applies 50% slow for 3s (frozenUntil timestamp on grunt); blue ❄️-5 floating text; AoE2/WC3-style slow-tower adding crowd-control depth to base defense (2026-07-01)
- [x] Expanded 17×17 map — GRID_SIZE expanded from 13→17; player barn moved to (2,2), enemy barn to (14,14) for wider strategic distance; 14 lumber/gold/stone resource nodes scattered in 5 clusters across the map; 4 creep camps; 8 loot crate spawns; redesigned makeTiles() with player-side and enemy-side lakes; more room for base-building and flanking routes (2026-07-01)
- [x] More starting resources — players start with 150🪙 80🌲 30🪨 instead of 0/0/0; reduces early frustration while keeping strategic decisions meaningful (2026-07-01)
- [x] RTSUI code-quality pass — fixed mixed-selection label (heterogeneous unit groups now show ⚔️/🌾 Mixed); fixed attack label (shows actual target type not always "enemy barn"); gated Harvest and Build commands on anyFarmers; added type="button" to all non-submit buttons; derived Granary/Stable/building tooltips from buildingCosts; fixed Cavalry tooltip (2×, not 2.5×); fixed farmhouse level cap from prop length; minimap constants (MINIMAP_GRID, MINIMAP_BARN, MINIMAP_ENEMY_BARN) replacing hardcoded literals; LUMBER_SHED_BONUS_MS shared constant (2026-07-01)
- [x] Blacksmith: extract upgrade costs to shared config constants — done, see Technical Cleanup section above (2026-08-07)
- [x] New Game resets cleanly — module-level INITIAL_SAVE replaced with per-mount loadSave() + RTSGameRoot key pattern; no page reload needed (2026-07-01)
- [x] Start with 5 farmers + 1 swordsman and food:6 for stronger early game (2026-07-01)
- [x] Slower wave progression — 25s→40s base interval, escalation reduced from -1.5s/wave to -0.8s/wave, floor raised to 20s (2026-07-01)
- [x] Starting resource cluster near barn — 3 trees at (4,2)(5,2)(4,3) and gold mine at (4,5) for immediate economy (2026-07-01)
- [x] Auto-retaliation — units attacked by a grunt auto-engage the attacker if idle; works for all unit types except siege (2026-07-01)
- [x] Aggressive/Passive stance toggle — Aggressive (default): idle combat units auto-engage enemies within 3 tiles; Passive: only retaliate when hit; button in command card (2026-07-01)
- [x] Barn defense scales — 10 base dmg (+1/3 waves, +3/garrisoned unit), range 4→5 tiles, fires every 2.5s; garrison now meaningfully buffs barn defense (2026-07-01)
- [x] Market: add stone→lumber trading option — sell 40🪨 for 25🌲 via new Market button (2026-07-01)
- [x] Siege Workshop: Trebuchet unit — 200🪙 80🌲 60🪨, 45HP, auto-fires 40 dmg at enemy barn and towers from 9-tile range, 6s cooldown, 2.5-tile minimum range; AoE2-style long-range siege that rewards positioning (2026-07-01)
- [x] Ballista Tower — 🏹 Ballista (100🪙 60🌲 80🪨, 150HP) piercing bolt: 18 dmg primary + 9 dmg splash to enemies within 1.5 tiles, 6.5-tile range, 4s cooldown; distinct SVG with bow arms and bolt; AoE2/WC3-style piercing tower adding anti-group defense (2026-07-01)
- [x] Under-attack alert banner — red pulsing "⚠ UNDER ATTACK ⚠" overlay below HUD bar when player barn or units take damage; auto-clears after 4s; helps players notice threats off-screen (2026-07-01)
- [x] Income rate display — HUD shows +N/m (per-minute) next to each resource in green after first 30s; income accumulates in incomeAccRef, published every 30s × 2 for per-minute rate; helps players gauge economic efficiency (2026-07-01)
- [x] Auto-repair burning buildings — idle farmers within 3 tiles of a burning building (<25% HP) automatically pathfind and start repairing it; AoE-style worker auto-assignment without micromanagement (2026-07-01)
- [x] Last Stand mechanic — when barn HP drops below 25%, barn fires 2× faster and deals 2× damage; red pulsing ring + "⚔ LAST STAND!" label + red border on barn SVG; barn red stroke replaces normal; WC3-style desperate last defense boost (2026-07-01)
- [x] Enemy Necromancer — 💀 spawns wave 16+ every 5th wave; marches toward dead grunt corpses within 3-tile radius and channels 4s to raise them as purple Skeleton grunts (half HP); distinct skull-headed dark robe SVG with purple channeling ring; right-click to attack; auto-targeted by aggressive stance + attack-move + hold-position; 20🪙 + 45 XP on kill; "Kill it before it raises the dead!" wave banner; WC3-style unit recycling that punishes players who leave corpses on the field (2026-07-01)
- [x] Stone Wall upgrade — right-click any wooden Palisade wall to upgrade it to Stone Wall for 50🪙+20🪨; HP increases from 120→350; distinct grey stone brick SVG with mortar lines; upgrade hint shown on hover when resources available; WC3/AoE2-style defensive building upgrade rewarding mid-game investment (2026-07-01)
- [x] Rally point flag — visible 🔵 flag SVG rendered at the rally point tile in the main map; pole + pennant visible in fog-clear tiles; helps players see where new units will march on spawn (2026-07-01)
- [x] Garrison barn HP regen — each unit garrisoned in the barn regenerates +2 HP/s for the barn (stacks per unit); green floating +N🏰 text; barn becomes a viable repair station when under siege (2026-07-01)
- [x] Fog of War on all enemy special units — Shamans, Necromancers, Trolls, Sappers, War Rams, Demolishers now all check fogVisible before rendering, matching grunts/towers; enemy units are hidden until revealed by player vision (2026-07-01)
- [x] Building destruction loot drop — when an enemy destroys a player building, a loot crate spawns at that tile with 30% resource refund (gold/lumber/stone); workers can right-click to collect; floating "💥 DESTROYED!" text; AoE2-style partial resource recovery that rewards quick response (2026-07-01)
- [x] Wave preview banner — 6s before each wave, a yellow banner shows the incoming composition (grunt count + all special units for that wave number); helps players prepare defenses without removing surprise; auto-clears when wave spawns (2026-07-01)
- [x] Tab key → find idle workers — pressing Tab cycles through idle farmers/units, selects the next one, and pans camera to it; AoE/WC3 standard idle-worker hotkey; hint shown in HUD tooltip bar (2026-07-01)
- [x] Enemy Witch Doctor — 🔮 spawns wave 12+ every 3rd wave; marches with grunt wave and casts Berserk on all grunts within 3 tiles (every 7s, 6s duration, +8 bonus damage); enraged grunts glow red with BERSERK! label; distinct purple-robe + voodoo skull staff SVG; casting ring shown; 18🪙 + 40 XP on kill; priority-targeted by attack-move, hold-position, aggressive stance; magenta diamond on minimap; "Kill it or grunts go berserk!" wave banner; WC3 Witch Doctor-style support enemy that makes grunts exponentially more dangerous (2026-07-01)
- [x] Neutral Map Shrines — 2 capturable objective points: Shrine of War (4,8) and Shrine of Plenty (12,8); right-click with any unit selected to send a worker to channel for 6s; Shrine of War grants permanent +5 ATK to all friendly combat units; Shrine of Plenty grants permanent +15% gather speed to all workers; channel progress bar shown; shrine SVG with pillar + flame icon (⚔️/🌾) changes color on capture; buff indicators in top-right HUD corner; AoE2/WC3-style neutral objectives rewarding map control and risk-taking (2026-07-01)
- [x] Hero level 2 ability: Battle Shout — unlocks at hero level 2 (120 XP); activates 8s burst where all friendly units within 4 tiles attack 40% faster (stacks with Morale Aura for 58% faster); orange dashed ring around affected units; 30s cooldown; command card shows locked state until level 2, then active 📯 button; WC3-style second hero ability rewarding early investment in the hero unit (2026-07-01)
- [x] Barracks Research system — two one-time upgrades available in the Barracks command card: Veteran Training (100🪙 60🌲): all current and future combat units gain +20 max HP; War Drums (120🪙 40🌲): all friendly combat units permanently deal +8 damage; buttons show ✓ when complete; AoE2/WC3-style building-based tech research adding strategic depth to Barracks investment (2026-07-01)
- [x] Grunt corpse rendering — dead grunts leave a faded 💀 gray corpse for 8s (opacity fades with age); only visible in fog-clear tiles; Necromancer's raise-target marker now visually meaningful; WC3-style battlefield debris adding atmosphere and telegraphing Necromancer activity (2026-07-01)
- [x] FEATURES.md + README major update — documented all 20+ features shipped since last update (iter59-73): Building Fire, Loot Crates, Hold Position, War Ram, Waypoints, Demolisher, Necromancer, Building Repair, Stone Wall, Last Stand, Ballista, Trebuchet, Income Rate, Under-Attack Alert, Witch Doctor, Wave Preview, Tab idle, Fog for all units, Building Destruction Loot, Shrines, Battle Shout, Barracks Research; README rewritten to reflect current RTS game scope with feature table (2026-07-01)
- [x] Building construction time — all placed buildings now take 6s to construct; shown as scaffold SVG (wooden frame, cross-poles, planks, faint icon, progress bar); buildings are invulnerable and non-functional while constructing; foodCapBonus applied on completion not placement; "✅ Built!" float on complete; WC3/AoE2-style construction time adding strategic depth to base-building timing (2026-07-01)
- [x] Poison Arrow Tower — ☠️ Poison Tower (70🪙 40🌲 50🪨, 130 HP) fires every 3s at nearest grunt in 5-tile range; deals 8 direct dmg + 3 dmg/s DoT for 4s; poisoned grunts show green dashed ring; custom green vat SVG with bubbles, pipe, and spout; build button in farmhouse panel; stacks with Frost Tower for combo crowd control; WC3/AoE2-style damage-over-time tower adding sustained damage to choke-point defense (2026-07-01)
- [x] Enemy Warchief hero unit — 👑 spawns wave 18+ every 8th wave; 300 HP / 30 barn dmg; War Stomp ability stuns all player units within 3 tiles for 2.5s every 12s (💫STUNNED! float); armored grunt SVG with crown, gems, battle axe; 50🪙 + 120 XP on kill; gold ★ on minimap; auto-targeted by aggressive stance, hold-position, attack-move; wave banner warning; wave preview lists WARCHIEF; WC3-style enemy hero climax encounter for late-game (2026-07-01)
- [x] Multi-worker construction assist — right-click a constructing building with selected farmers to assign them as assistants; each farmer adds 40% construction speed (1 helper=1.4×≈4.3s, 2=1.8×≈3.3s, 3=2.2×≈2.7s); scaffold progress bar turns yellow while assisted; label shows worker count (🔨 Building… ×2); workers released and set idle on completion; WC3-style worker assist mechanic (2026-07-01)
- [x] Construction cancel — right-click scaffold with no units selected to cancel; 50% resource refund (gold/lumber/stone); assisting workers released; ❌ Cancelled float text; hint text on scaffold "RMB: cancel (50% refund)" / "RMB: assist"; AoE2/WC3-style cancel mechanic (2026-07-01)
- [x] Upkeep system (WC3-style) — 0–40 food: no upkeep (100% gold rate); 41–80 food: 70% gold income; 81+ food: 40% gold income; applies to farmer deposits AND windmill passive income; top resource bar shows 📉70% / 📉40% badge on gold; minimap panel shows "✓ No upkeep" / "📉 Upkeep (70%)" / "📉 Heavy upkeep (40%)"; adds WC3-style economic penalty for large armies (2026-07-01)
- [x] Big map expansion (25×25) + 2-3× resources — GRID_SIZE 17→25; ENEMY_BARN_POS (14,14)→(22,22); new 25×25 terrain with 3 lakes, 7 tree clusters, 6 rock clusters, diagonal dirt path; DEFAULT_TREES ×2.5 (45 nodes), gold mines ×2.5 (10 mines), stone nodes ×2.5 (17 nodes); creep camps ×1.75 (7 camps); shrines doubled (4 total); enemy tower positions updated to mid-map; save key bumped to v2 to clear stale saves; fog validated on GRID_SIZE (2026-07-01)
- [x] Projectile visuals — flying 🪨 rock for catapult/trebuchet (arc parabola); ❄ ice bolt for frost tower; 🏹 arrow for watchtower/ballista; ☠ poison bolt for poison tower; SVG SMIL-style interpolation via Date.now() elapsed; projectiles prune every 200ms; adds SC/WC3-style visible attack feedback for all siege and tower attacks (2026-07-01)
- [x] Pause in speed cycle — speed button cycles ⏸ Pause (0×) → ▶ 1× → ▶▶ 2× → Pause; red background when paused (2026-07-01)
- [x] Fix tower useEffect bugs — all tower effects (watchtower, frost, ballista, poison) now always return cleanup; added dead-tower guard (hp>0 check) inside callbacks so destroyed towers stop firing; fixed frost/ballista/poison early-return without cleanup causing stale timer leaks (2026-07-01)
- [x] Fix guard tower research persistence — guardTowerResearched, barracksTech, blacksmithUpgrades now saved to localStorage and restored on reload; save deps array updated (2026-07-01)
- [x] Minimap fix for 25×25 map — MINIMAP_GRID 17→25, MINIMAP_ENEMY_BARN (14,14)→(22,22), minimap SVG height h-16→h-24 so the bigger map renders at correct coordinates; resource dots/enemy/building markers all correctly positioned (2026-07-02)
- [x] Wave scaling for bigger map — grunt count now scales with wave: 1-6 base grunts (floor(wave/5)+1), doubled on every 3rd wave; spread across 3 columns so large waves fan out instead of stacking; wave 20+ sends 6-8 grunts per wave (2026-07-02)
- [x] Loot crates expanded — positions expanded from 8 to 18 spread across 25×25 map; spawn count scales with wave (1 crate early, 2 from wave 5+, 3 from wave 10+); resource pool enriched with 2 new loot types (mixed gold+lumber+stone); uses ref snapshot instead of stale state for occupied check (2026-07-02)
- [x] Smooth WASD/Arrow camera pan — replaced step-per-keypress with held-key + RAF loop at 480 px/s; Set<string> tracks all held keys; onBlur clears held set; camera bounds expanded to GRID_SIZE×TILE_SIZE for full 25×25 map traversal; AoE/WC3-style fluid keyboard navigation (2026-07-02)
- [x] Mouse edge-scroll — cursor within 48px of viewport edge pans camera at 400 px/s via RAF loop; independent of WASD; classic RTS edge-of-screen scrolling for the bigger 25×25 map (2026-07-02)
- [x] Move-target ring — right-click move command flashes an expanding green circle at the destination (WC3-style click confirmation); fades out over 600ms; rendered in SVG coordinate space above terrain (2026-07-02)
- [x] Cursor-anchored zoom — scroll-wheel zoom now keeps the world point under the cursor fixed (AoE/SC2 zoom behavior); range expanded 0.4×–2.5×; +/- keys zoom to viewport center; HUD shows live % with clickable +/− buttons (2026-07-02)
- [x] Hero respawn / revive — when Barnabas dies his XP+level are preserved; auto-revives after 20s+2s×wave (max 60s); barn command card shows countdown bar; instant revive costs 80–200🪙 scaling with wave; hero spawns at barn on revive; WC3-style hero death mechanic adding tension and resource decisions (2026-07-02)
- [x] Projectile visuals for all missing attackers — original archer tower, enemy fortress towers, Demolisher siege (rock arc), and Troll archers now all fire visible projectiles; fixes user-reported issue where these units showed damage numbers but no visual attack (2026-07-02)
- [x] High-score leaderboard — top 5 runs saved to localStorage; shown on game-over screen with wave, kills, gold, result, date; sorted by wave then kills; gold medal color for #1 entry; AoE/WC3-style personal best tracking (2026-07-02)
- [x] Battle report improvements — added stone mined🪨, buildings built, survivors count; now 8 stats total on game-over screen (2026-07-02)
- [x] Hit-flash on damage — workers flash red, grunts flash white for 200ms when hit; uses lightweight per-unit timestamp refs (no state); covers grunt melee, archer tower, enemy fortress towers, and watchtower shots; classic action game damage feedback (2026-07-02)
- [x] Procedural sound effects — Web Audio API synthesized sounds (no audio files); unit select, move, hit, death, build complete, gold deposit, wave warning, victory/defeat tones; lazy AudioContext init; Snd helper module at module scope (2026-07-02)
- [x] Control group double-tap camera center + HUD bar — double-tapping 1-9 within 500ms centers camera on group centroid; compact group indicator bar at top-center shows group number + alive unit count for all assigned groups (2026-07-02)
- [x] Sound mute toggle + gold deposit throttle — 🔊/🔇 button in HUD persists mute state to localStorage; gold deposit sound throttled to once per 2s so it doesn't spam with multiple harvesters; all playTone calls check mute flag (2026-07-02)
- [x] Shared SVG component refactor (iter109) — extracted `HpBar`, `StructureDamageSmoke`, and `StructureFireEffect` into `components/rts/map/`; replaced duplicated inline two-rect HP bars across EnemyBaseLayer, EnemySiegeCastersLayer, EnemyGruntsLayer, EnemyEliteLayer, PlayerBarnLayer, BuildingsLayer, WorkersLayer (17 call sites); replaced near-identical smoke-circle and flame-ellipse blocks in PlayerBarnLayer, EnemyBaseLayer, and BuildingsLayer; components parameterized by center coordinates, colors, opacities, and optional label; type-check and lint clean; visual verified in running dev server (2026-07-04)
- [x] Componentize large files — Phase 1 (2026-08-04) — `RTSUI` (2110 lines) fully split into `ui/BuildMenu`, `ui/WaveTimer`, `ui/HeroPanel`; `HeaderCropRow` background extracted to `animations/AnimatedBackground`; pure helpers in `spawnHelpers.ts`, `towerHelpers.ts`, `game/mapSelectors.ts`; domain hook shells (`useEnemyAI`, `useResourceTick`, `useCombatResolution`, `usePathfinding`) + `MapRenderer` shell scaffolded as migration targets; +55 unit tests (264 total); WaveTimer NaN fix; BuildMenu disabled-state fix; TypeScript clean
- [x] Componentize large files — Phase 2a — migrate logic from `useGameLoop.tsx` into the domain hooks (PR #295, merged). `useGameLoop.tsx` down to 72 lines, decomposed into `useEnemyAI`/`useResourceTick`/`useCombatResolution`/`usePathfinding`/`useBotController` plus a dozen domain tick modules under `hooks/ai/`. Vitest coverage scope expanded to include RTS game logic (see the `thresholds` block in `config/vitest.config.ts` — source of truth — for current lines/statements/functions/branches percentages).
- [x] Componentize large files — Phase 2b (2026-09-02) — `RTSMap.tsx`'s `<svg>` render tree (viewport, pan/zoom transform, mouse handlers, and the 12-layer stack: Terrain/OverlayRings/ResourceNodes/Buildings/EnemyBase/PlayerBarn/Neutral/EnemyGrunts/EnemySiegeCasters/EnemyElite/Workers/Effects) now lives in `MapRenderer` (`components/rts/map/MapRenderer.tsx`), typed via `React.ComponentProps<typeof Layer>` per layer so prop types can't drift from the layer components themselves. `RTSMap.tsx` wires per-layer prop bags into `<MapRenderer>` instead of rendering the SVG tree inline. Also replaced 6 duplicated `placedBuildings.some(b => b.type === X && !b.constructing)` inline checks with `hasBuildingType()` from `mapSelectors`. Type-check and lint clean; all 440 tests still pass.
