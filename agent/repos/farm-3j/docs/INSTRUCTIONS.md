# Agent Instructions: Farm RTS Handoff

## Where to Pick Up

- See `TASKS.md` under 'Unfinished Todos (RTS Farm Game)' for the current actionable items.
- All code and UI changes should be validated visually in the browser using the mapped Docker port (run `node scripts/print-docker-port.js` or `docker compose -f config/docker-compose.yml port farm-app 3000`, then open `http://localhost:<PORT>/rtsfarm`) after each Docker redeploy.

## Flow / Order of Operations (Best Practices)

1. **Work on one todo at a time** from the top of the unfinished list unless a different order is justified.
2. **Make code changes** as needed for the current todo.
3. **Restart Docker containers** (`docker compose -f config/docker-compose.yml restart`) to ensure the latest code is running.
4. **Visually review the app** in the browser to confirm/validate the change.
5. **Commit the change** if it works as intended (use a descriptive commit message).
6. **Update the todo list** (in code and in TASKS.md) to mark the item complete.
7. **Continue to the next todo**.

## Additional Notes

- Do not commit directly to main/master. Always work on a feature branch.
- Keep the codebase clean and follow project conventions (see .github/copilot-instructions.md).
- If a UI or gameplay change is made, update screenshots in the README if possible.
- If you encounter a blocker, document it in TASKS.md and move to the next actionable item.

---

**For more context, see:**

- `docs/FARM-RTS-TODO.md` (milestones, design notes)
- `TASKS.md` (current progress)
- `.github/copilot-instructions.md` (coding standards)
