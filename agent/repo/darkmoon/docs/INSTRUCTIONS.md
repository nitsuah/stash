# Agent Pickup Instructions

## Context
You are picking up work on the Darkmoon repo (branch: play-modes). The previous agent was focused on stabilizing the solo tag game, ensuring bot-vs-player and player-vs-bot tagging is robust, and enforcing a Docker-first validation workflow for all changes.

## Flow / Order of Operations (Best Practices)

1. **Work in a Feature Branch**
   - Never commit or stage code on main/master. Always use a feature branch (e.g., play-modes or a new one if needed).

2. **Make a Code Change**
   - Implement the next task or bugfix as described in TASKS.md.

3. **Docker Validation**
   - Run `docker compose build` and `docker compose up -d` to ensure the app builds and runs in a containerized environment.
   - Use `docker compose restart app` after any code change to ensure the running container reflects your latest edits.

4. **Visual/Manual Review**
   - Open the app in a browser (http://localhost:4444 or as configured) and visually confirm the change works as intended.
   - For UI/UX or gameplay changes, always visually verify before committing.

5. **Automated Tests**
   - Run all relevant tests in Docker (e.g., `docker compose exec app npm run test`).
   - If you add or change features, add/modify tests as needed.

6. **Commit and Continue**
   - Once the change is validated (Docker build, browser, and tests), commit using a conventional commit message (see copilot-instructions.md).
   - Move to the next task in TASKS.md.

7. **Update Documentation**
   - If your change affects docs, update README.md, FEATURES.md, or other relevant files.

## Where to Resume
- See TASKS.md for unfinished todos. Prioritize P0 tasks first.
- If the tag system regresses, review Bots.tsx, PlayerCharacter.tsx, useBotAI.ts, and GameManager.ts for logic symmetry and cooldown handling.
- Always validate in Docker and visually before marking a task complete.

## Contact
If you encounter blockers, document them in TASKS.md and leave a note here for the next agent.

---
_Last updated: 2026-04-13_
