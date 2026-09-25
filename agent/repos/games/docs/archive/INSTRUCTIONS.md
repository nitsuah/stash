> **Archived 2026-09-23**: describes a client-side exception and Q2 2026
> platform-reliability items as unfinished; both are long since resolved/shipped
> (see `docs/TASKS.md`, `docs/ROADMAP.md`). Kept for historical reference only.

# INSTRUCTIONS.md

> 🧭 [games](../../README.md) · [Features](../FEATURES.md) · [Roadmap](../ROADMAP.md) · [Tasks](../TASKS.md) · [Changelog](../CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

## Where to Resume

The previous agent was actively debugging a global client-side exception (`ReferenceError: Cannot access 'ev' before initialization`) that prevented all games from loading in Docker. The error is not present in server-side logs or Next.js build traces, indicating a runtime/browser-side issue. The last step was to capture browser console logs from the Dockerized app to obtain the actual client-side error and stack trace.

## Next Steps (Best Practice Flow)

1. **Capture Browser Console Logs**
   - Use the browser automation tools to open the arcade home and a failing game route (e.g., `/asteroid`) in Docker.
   - Retrieve all browser console errors and stack traces.
   - Identify the root cause of the client-side exception.

2. **Diagnose and Fix**
   - Trace the error to the relevant code (likely a shared import, circular dependency, or initialization order issue).
   - Apply a fix in a feature branch (never on main/master).
   - Rebuild and restart the Docker container.

3. **Visually Validate**
   - Use the browser plugin to visually confirm that all games load and are playable in Docker.
   - Only after visual validation, commit the fix.

4. **Continue with Next Task**
   - Repeat the above flow for each new bug or feature: always validate in Docker, visually confirm, then commit.

## Unfinished Todos (from TASKS.md)
- Performance audit and asset optimization
- Mobile responsiveness and touch input
- Accessibility pass
- UX verification pass

## Notes
- Always use Docker for validation and visual review.
- Never commit on main/master; always use a feature branch.
- Document any new errors or friction points in TASKS.md before moving to the next task.
