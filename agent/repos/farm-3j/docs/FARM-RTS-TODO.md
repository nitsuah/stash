# Farm RTS: Implementation TODOs (MVP)

_This file is the actionable engineering breakdown for the Farm RTS MVP, directly mapped to the milestones and systems in Farm_RTS_Game_Manual.md._

## Milestone 1: Core Map & Camera

    - [x] Isometric tile grid renders correctly
    - [x] Smooth WASD camera pan
    - [x] Zoom levels (2 minimum)
    - [x] Tile types: grass, dirt, water, trees, rocks
    - [x] Debug overlay: show grid, tile coordinates, FPS

## Milestone 2: Main Building & UI

- [x] Barn renders on map at starting position
- [x] Top resource bar (Coins, Hay, Food)
- [ ] Bottom command card (placeholder buttons)
- [ ] Unit info panel renders (static/mock data)
- [ ] Build menu opens from Barn

## Milestone 3: Resource Nodes

    - [x] Tree groves (Hay nodes) render
    - [x] Coin well (Gold node) renders
    - [x] Resource node depletion logic
    - [x] Visual feedback when node is empty

## Milestone 4: Worker Unit

- [x] Farmer unit renders and animates
- [x] Single click selects, right-click moves
- [ ] Farmer walks to resource node
- [ ] Farmer gathers and returns to Barn
- [ ] Carry capacity + deposit logic
- [ ] Resource bar updates on deposit
- [ ] Multiple Farmers can be selected (box select)
- [ ] Idle worker hotkey (F9)

## Milestone 5: Building Construction

- [ ] Build menu shows available buildings
- [ ] Ghost preview on placement
- [ ] Valid/invalid tile detection (red/green)
- [ ] Worker walks to build site and constructs
- [ ] Building progresses from scaffold to complete
- [ ] Multiple workers speed up construction
- [ ] Farmhouse increases food cap

## Milestone 6: Resource System

- [ ] Food supply cap enforced (can't train units over cap)
- [ ] Insufficient resource error messages
- [ ] Resource refund on building cancel
- [ ] Upkeep warning at 80% food cap

## Milestone 7: Win / Lose Condition

- [ ] Static enemy base on opposite side of map
- [ ] Player can attack enemy Barn
- [ ] Victory screen when enemy Barn destroyed
- [ ] Defeat screen when player Barn destroyed
- [ ] Restart and main menu buttons

## Milestone 8+: See manual for stretch goals (combat, AI, heroes, upgrades, polish)
