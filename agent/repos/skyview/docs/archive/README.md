# Archived Documentation

Docs moved here during the 2026-09 documentation audit because they were
superseded by a more current doc, duplicated another doc's content, or
described a one-off past state (a specific dev session, or a project status
snapshot from a specific date) rather than an evergreen reference. Kept for
history — not maintained, and may contain inaccurate/stale instructions
(stale `config.js` examples, dead links, outdated file paths).

| File | Why it moved | Current source of truth |
|------|---------------|--------------------------|
| `PROJECT_STATUS.md` | Dated 2025-12-13; describes a pre-refactor file layout (`client-portal.html` at repo root, no `platform/` SPA) | `FEATURES.md`, `ROADMAP.md` |
| `SESSION_SUMMARY.md` | One-off summary of a past WebP-optimization work session | `docs/WEBP_OPTIMIZATION.md` |
| `QUICK_REFERENCE.md` | Dated 2025-12-13; duplicated setup/testing commands now covered elsewhere | `docs/GETTING_STARTED.md`, root `README.md` |
| `QUICKSTART.md` | Informal duplicate of the onboarding walkthrough | `docs/GETTING_STARTED.md`, `docs/OWNER_GUIDE.md` |
| `MANUAL_SETUP.md` | Dated 2025-12-13; stale `config.js` flag defaults (e.g. showed `contactForm: false` when it's `true`), missing flags added since (`platform`, `analyticsDebugPanel`) | `docs/GETTING_STARTED.md` (setup steps), `docs/CONFIG.md` (flag reference) |
| `CONFIG_README.md` | Stale flag snapshot, redundant with the full config reference | `docs/CONFIG.md` |
| `WEBP_IMPLEMENTATION.md` | Historical "what was built" summary of the WebP feature, not a how-to | `docs/WEBP_OPTIMIZATION.md` |

If you're looking for current setup instructions, start at `docs/GETTING_STARTED.md`
or `docs/OWNER_GUIDE.md`.
