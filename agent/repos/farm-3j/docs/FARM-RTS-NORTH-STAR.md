# Farm RTS: North Star & Milestone Plan

## Vision (North Star)

Build a browser-based, isometric real-time strategy (RTS) game inspired by Warcraft 3 and Starcraft, with a farm theme. The MVP should deliver the core gameplay loop: base building, resource gathering, and unit management. The experience should be smooth, responsive, and fun, even if simplified and "on rails" at first.

## MVP Feature Baseline

- **Isometric map** with camera movement (WASD/arrow keys, smooth multi-directional)
- **Main building (Barn/Town Hall)**: central structure, can build workers
- **Resource nodes**: trees (lumber), gold mine (gold)
- **Worker units**: can be selected, move, gather resources, build
- **Basic build menu**: build new structures (e.g., farm, lumber mill)
- **Resource bar/UI**: shows current lumber/gold, selected unit info
- **Simple minimap** (optional for MVP)
- **Basic win/lose condition**: e.g., gather X resources or survive Y minutes

## Stretch/Polish (Post-MVP)

- Enemy/neutral units (AI)
- Multiple building/unit types
- Upgrades/tech tree
- Sound, music, and polish
- Save/load game state

## Simplifications Allowed

- No multiplayer (single player only)
- No advanced pathfinding (basic grid movement is fine)
- No fog of war (optional for polish)
- No advanced AI (scripted or static is fine)
- "On rails": scripted events or limited map size

## Milestone Plan

1. **Core Map & Camera**
   - Isometric grid, smooth camera movement
   - Debug overlays for dev
2. **Main Building & UI**
   - Render barn, resource bar, build menu UI
3. **Resource Nodes**
   - Place trees and gold mine, render on map
4. **Worker Unit**
   - Select, move, gather resources, return to barn
5. **Building Construction**
   - Build new structures from menu
6. **Resource System**
   - Track and display lumber/gold
7. **Win/Lose Condition**
   - Simple victory/defeat logic
8. **Polish & Stretch**
   - Minimap, AI, upgrades, sound, etc.

## Success Criteria

- Playable in browser, no build errors
- Can build, gather, and manage units/resources
- UI is clear and responsive
- Codebase is maintainable and documented
- MVP delivered before adding polish/stretch goals

---

_This doc is the guiding star for the Farm RTS MVP. All todos and features should reference this plan. Update as needed as the project evolves._

## Related

- [[repos/farm-3j/docs/Farm_RTS_Game_Manual|Farm RTS Game Manual]] — full game manual and milestone plan
