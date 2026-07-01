# Pending LOC Work

## Critical Refactor Targets

- motor-pool/ - 2 files dominate:
  - server.js (2,726 lines) - Express monolith with ALL concerns co-located
  - App.jsx (1,337 lines) - Massive React component

- auto-apply-plugin/ - 2 files:
  - service-worker.js (1,263 lines) - Chrome extension "god worker"
  - content.js (1,202 lines) - Mixed DOM concerns

## Next Priorities

- kryptos - CLI/coordination issues:
  - cli/main.py (663) - Args + business logic mixed
  - autonomous_coordinator.py (608) - Mixed scheduling/dispatch logic
  - Highest ROI: Split cli/main.py into subcommand modules

- darkmoon - Game component bloat:
  - PlayerCharacter.tsx (833) - Input/Physics/UI all-in-one
  - Solo.tsx (763) - Thin coordinator worth extracting hooks
  - Highest ROI: Extract usePlayerInput, usePlayerPhysics hooks

- games - Game loop chaos:
  - Game.jsx (828) - Update/entities/collision all coupled
  - SoundManager.js (808) - Borderline, overlaps with DynamicMusicSystem
  - Highest ROI: Extract game loop + entity management hooks

- overseer - API/component sprawl:
  - github.ts (741) - All GitHub API scattered
  - enrich-template/route.ts (754) - API handler doing too much
  - GuidedTour.tsx (750) - Step definitions inlined JSX
  - Highest ROI: Split github.ts into domain modules, extract tour steps
  
