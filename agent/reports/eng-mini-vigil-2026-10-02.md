---
HEAD: e4701d857ae374ed53fa7033f655931711017a31
kind: eng-mini
repo: vigil
date: 2026-10-02
---

# eng-mini: vigil — 2026-10-02 (REPORT MODE / DRY RUN)

> 🧭 [[repos/vigil|vigil]] <!-- nav --> (first eng-mini audit of this repo; the Overseer app itself)

> Report only — no moves executed, no changes made to the target repo. Follow-up batch run at the user's request. HEAD `e4701d8` "docs(pmo): add Done section the TASKS parser expects; fold 4 checked items (refs #261) (#262)", `git log -1 --format=%ci` 2026-10-01T13:09:07-04:00. Root audited from a throwaway `--depth 1` clone at `/home/user/vigil`. This is the busiest root of all 16 repos audited across both 2026-10-01 and 2026-10-02 runs — see Out-of-Scope Observations for the findings a non-destructive pass can't act on directly.

## Root Audit — vigil/

| File/Dir | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.claude/` | Tooling | Claude Code project config — root | **KEEP** |
| `.dockerignore` | Docker | Must stay with `Dockerfile`'s build context | **KEEP** |
| `.env.example` | Config template | Root-required | **KEEP** |
| `.github/` | CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.husky/` | Tooling | `package.json`'s `"prepare": "husky || true"` sets `core.hooksPath` to `.husky` | **KEEP** |
| `.nvmrc` | Tooling | nvm reads this from cwd by convention | **KEEP** |
| `.prettierignore` / `.prettierrc.json` | Config | Prettier resolves by walking upward from the edited file; a `config/` subdir isn't in that path | **KEEP** |
| `.vscode/` | Editor config | Committed intentionally (`tasks.json`, last touched this HEAD's date) — a directory, not a loose root file | **NO ACTION** |
| `AGENTS.md` | Documentation | Open "AGENTS.md" convention, read by non-Claude agent tooling — same root-read class as `CLAUDE.md`, different consumer | **KEEP** |
| `CLAUDE.md` | Tooling | Claude Code project instructions — root | **KEEP** |
| `Dockerfile` | Build | Root-required | **KEEP** |
| `LICENSE` | Legal | Decided 2026-09-24: stays at root in every repo | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `ROADMAP.md`, `TASKS.md`, `FEATURES.md`, `METRICS.md`, `CHANGELOG.md` | Documentation | Root-only valid location per MINI.md's documented table (root OR `docs/`) — none have a `docs/` counterpart, so no duplicate pair | **KEEP** |
| `auth.ts` | Framework entry point | NextAuth.js v5 canonical config file — imported via `@/auth` from `app/api/auth/[...nextauth]/route.ts` and ~10 other route handlers | **KEEP** |
| `proxy.ts` | Framework entry point | Exports `proxy()`, imported as `@/proxy` — root path alias. See Out-of-Scope Observations for a usage caveat this audit can't resolve | **KEEP** |
| `netlify.toml` | Build | Netlify reads from repo root by default | **KEEP** |
| `next.config.ts` | Build | Next.js requires this at project root | **KEEP** |
| `package.json` / `package-lock.json` | Manifest/lockfile | Root-required | **KEEP** |
| `playwright.config.ts`, `playwright.ci.config.ts`, `playwright.smoke.config.ts`, `playwright.visual-docs.config.ts` | Tooling | Multiple intentional Playwright config variants (standard/CI/smoke/visual-docs); each resolves `testDir` relative to its own location | **KEEP** |
| `postcss.config.mjs` | Build | PostCSS/Tailwind tooling resolves from cwd root | **KEEP** |
| `tsconfig.json` | Tooling manifest | TypeScript convention, canonical root location | **KEEP** |
| `app/`, `components/`, `config/`, `database/`, `docs/`, `e2e/`, `hooks/`, `lib/`, `promo/`, `public/`, `scripts/`, `site/`, `skills/`, `templates/`, `tests/`, `types/` | Pre-existing top-level content directories | Already organized; not loose root files | **NO ACTION** |
| `.coverage`, `build.log`, `build-out.log`, `build2.log` | Generated artifacts | See Out-of-Scope Observations | **NO ACTION** |

## Duplicate / Destination Checks

All five planning docs (`ROADMAP.md`, `TASKS.md`, `FEATURES.md`, `METRICS.md`, `CHANGELOG.md`) exist at root only — no `docs/` counterpart for any, so no duplicate pair to report. No `CONTRIBUTING.md` found at either location.

## Proposed Moves (Dry Run — Not Executed)

**None.** Everything at root is either a hard platform/framework requirement (Next.js config, NextAuth entry point, lockfiles) or an intentional multi-location documentation file already valid per MINI.md's own rules.

## Overseer Decisions Required

None.

## Out-of-Scope Observations

- **Three build-log files tracked at root**: `build.log`, `build-out.log`, `build2.log` all contain literal `next build` terminal output (ANSI escape codes included) and are not excluded by `.gitignore` (which only covers `npm-debug.log*`/`yarn-*-debug.log*`/`.pnpm-debug.log*`, not a bare `*.log` or these specific names). These read as accidentally committed local build logs. Recommend adding a `*.log` (or these three names) rule to `.gitignore` and `git rm --cached` the tracked files; out of scope for this non-destructive pass (deletion).
- **`.coverage`** is a tracked SQLite database (pytest-cov or similar coverage-tool output) at root, also not covered by `.gitignore`. Same recommendation as above.
- **`proxy.ts` usage is worth a human look, not a MINI finding**: it's imported only by its own test (`tests/proxy.test.ts`); no `middleware.ts` exists anywhere in the repo, and `next.config.ts` has no reference to a custom proxy/middleware wiring. This audit can't determine from a root-file pass alone whether `proxy.ts` is (a) a newer Next.js 16 convention this repo has correctly adopted, (b) mid-refactor and not yet wired in, or (c) dead code — that's a code-correctness question, outside MINI's root-hygiene scope. Flagging for a human or a CLEANUP-tier pass rather than asserting an answer.

## Errors Encountered

None.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/vigil`.*
