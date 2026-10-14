---
HEAD: 8f9c3966541fc7e38a514e27a0946726019030c5
kind: eng-mini
repo: vigil
date: 2026-10-14
---

# eng-mini: vigil — 2026-10-14 (REPORT MODE / DRY RUN)

> 🧭 [[repos/vigil|vigil]] · ← [[reports/eng-mini-vigil-2026-10-02|2026-10-02]] <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as the #3 most recently active tracked repo this run (`git log -1 --format=%ci` from a fresh `--depth 1` clone: 2026-10-14T04:56:06-04:00, HEAD `8f9c396` "build(deps): bump the minor-and-patch group across 1 directory with 14 updates (#280)"). Root audited from a throwaway clone at `/home/user/vigil`.

## Root Audit — vigil/

| File/Dir | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.claude/` | Tooling | Claude Code project config — root | **KEEP** |
| `.coverage`, `build.log`, `build-out.log`, `build2.log` | Generated artifacts | See Out-of-Scope Observations | **NO ACTION** |
| `.dockerignore` | Docker | Must stay with `Dockerfile`'s build context | **KEEP** |
| `.env.example` | Config template | Root-required | **KEEP** |
| `.github/` | CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.husky/` | Tooling | `package.json`'s `"prepare": "husky || true"` sets `core.hooksPath` to `.husky` | **KEEP** |
| `.nvmrc` | Tooling | nvm reads this from cwd by convention | **KEEP** |
| `.prettierignore` / `.prettierrc.json` | Config | Prettier resolves by walking upward from the edited file; a `config/` subdir isn't in that path | **KEEP** |
| `.vscode/` | Editor config | Committed intentionally — a directory, not a loose root file | **NO ACTION** |
| `AGENTS.md` | Documentation | Open "AGENTS.md" convention, read by non-Claude agent tooling — same root-read class as `CLAUDE.md`, different consumer | **KEEP** |
| `CLAUDE.md` | Tooling | Claude Code project instructions — root | **KEEP** |
| `Dockerfile` | Build | Root-required | **KEEP** |
| `LICENSE` | Legal | Decided 2026-09-24: stays at root in every repo | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `ROADMAP.md`, `TASKS.md`, `FEATURES.md`, `METRICS.md`, `CHANGELOG.md` | Documentation | Root-only valid location per MINI.md's documented table (root OR `docs/`) — none have a `docs/` counterpart, so no duplicate pair | **KEEP** |
| `auth.ts` | Framework entry point | NextAuth.js v5 canonical config file — imported via `@/auth` from `app/api/auth/[...nextauth]/route.ts` and ~10 other route handlers | **KEEP** |
| `proxy.ts` | Framework entry point | Exports `proxy()`, imported as `@/proxy` — root path alias | **KEEP** |
| `netlify.toml` | Build | Netlify reads from repo root by default | **KEEP** |
| `next.config.ts` | Build | Next.js requires this at project root | **KEEP** |
| `package.json` / `package-lock.json` | Manifest/lockfile | Root-required | **KEEP** |
| `playwright.config.ts`, `playwright.ci.config.ts`, `playwright.journeys.config.ts`, `playwright.smoke.config.ts`, `playwright.visual-docs.config.ts` | Tooling | Multiple intentional Playwright config variants (standard/CI/journeys/smoke/visual-docs); each resolves `testDir` relative to its own location, and each is already wired into its own `package.json` script / CI workflow — moving would require touching 5 configs, `package.json`, and 4 workflow files for no functional gain | **KEEP** |
| `postcss.config.mjs` | Build | PostCSS/Tailwind tooling resolves from cwd root | **KEEP** |
| `tsconfig.json` | Tooling manifest | TypeScript convention, canonical root location | **KEEP** |
| `app/`, `components/`, `config/`, `database/`, `docs/`, `e2e/`, `hooks/`, `lib/`, `promo/`, `public/`, `scripts/`, `site/`, `skills/`, `templates/`, `tests/`, `types/` | Pre-existing top-level content directories | Already organized; not loose root files | **NO ACTION** |

Root listing is unchanged from the 2026-10-02 audit (same files and directories present, including the three tracked build logs and `.coverage`).

## Duplicate / Destination Checks

All five planning docs (`ROADMAP.md`, `TASKS.md`, `FEATURES.md`, `METRICS.md`, `CHANGELOG.md`) exist at root only — no `docs/` counterpart for any, so no duplicate pair to report. `docs/` holds a different, non-overlapping set (`AGENT_TASK_QUEUE_API.md`, `AUDIT.md`, `MCP.md`, `TESTING_STRATEGY_PROMPT.md`, `VISUAL_DOCS.md`, `db-scaling-assessment.md`). No `CONTRIBUTING.md` found at either location.

## Proposed Moves (Dry Run — Not Executed)

**None.** Everything at root is either a hard platform/framework requirement (Next.js config, NextAuth entry point, lockfiles) or an intentional multi-location documentation file already valid per MINI.md's own rules.

## Overseer Decisions Required

None.

## Out-of-Scope Observations

- **Three build-log files still tracked at root**: `build.log`, `build-out.log`, `build2.log` all contain literal `next build` terminal output and are not excluded by `.gitignore` (which only covers `npm-debug.log*`/`yarn-*-debug.log*`/`.pnpm-debug.log*`, not a bare `*.log` or these specific names). Unchanged since the 2026-10-02 audit. Recommend adding a `*.log` (or these three names) rule to `.gitignore` and `git rm --cached` the tracked files; out of scope for this non-destructive pass (deletion).
- **`.coverage`** remains a tracked coverage-tool output file at root, also not covered by `.gitignore`. Same recommendation as above, also unchanged since 2026-10-02.

## Errors Encountered

None.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/vigil`.*
