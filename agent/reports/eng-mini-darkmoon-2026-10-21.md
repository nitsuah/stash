---
HEAD: a44d2091a80899d873c5162d4c5cb61a517075de
kind: eng-mini
repo: darkmoon
date: 2026-10-21
---

# eng-mini: darkmoon — 2026-10-21 (REPORT MODE / DRY RUN)

> 🧭 [[repos/darkmoon|darkmoon]] · ← [[reports/eng-mini-darkmoon-2026-10-02|2026-10-02]] <!-- nav -->

>
> Report only — no moves executed, no changes made to the target repo. Selected as the #2 most recently active tracked repo this run (`git log -1 --format=%ci` from a fresh `--depth 1` clone: 2026-10-21T02:15:51-04:00, HEAD `a44d209` "fix(combat): block hitscan shots through obstacles and improve test diagnostics (#483)"). Root audited from a throwaway clone at `/home/user/darkmoon`.

## Root Audit — darkmoon/

| File/Dir | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.claude/` | Tooling | Claude Code project config — read from repo root | **KEEP** |
| `.git/` | VCS internal | N/A | **N/A (not a content file)** |
| `.github/` | Community health / CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.dockerignore` | Docker | Docker reads from build context root; moving without moving `Dockerfile` breaks the build | **KEEP** |
| `.env.example` | Config template | Root-required (`.env*` class); referenced from `docs/projects/multi/MULTIPLAYER_GATE.md` as a root path | **KEEP** |
| `.husky/` | Git hooks | Husky-managed `.git/hooks`; hook scripts live here by Husky convention | **KEEP** |
| `Dockerfile` | Build | Root-required for default `docker build` context | **KEEP** |
| `LICENSE` | Legal | **Decided 2026-09-24: stays at root in every repo** | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `index.html` | Build entry | Vite resolves this from project root by default | **KEEP** |
| `netlify.toml` | Build | Netlify reads build config from repo root by default | **KEEP** |
| `package.json` / `package-lock.json` | Manifest/lockfile | Root-required | **KEEP** |
| `render.yaml` | Deploy | Render reads its deploy spec from repo root by default | **KEEP** |
| `playwright.config.ts` | Config | `testDir: "./e2e"` resolves from config file location; movable per MINI.md's tool-path table (`./e2e` → `../e2e`), but no current script/CI breakage to fix — low urgency | **CANDIDATE-MOVE (deferred)** |
| `vite.config.js` | Config | Root-required in practice: `scripts/develop.js` imports it directly via `../vite.config.js`; moving would require updating that import plus any bare `vite build`/`vite dev` CLI invocation | **KEEP (deferred — see risk below)** |
| `tsconfig.json` | Config | **Duplicate** — see Duplicate/Destination Checks below | **KEEP (flagged)** |
| `config/`, `docs/`, `e2e/`, `scripts/`, `server/`, `src/` | Pre-existing top-level content directories | Already organized per the repo's own Folder Strategy (eslint, vitest, lint-staged, pre-commit, prettier and docker-compose configs already live under `config/`; `package.json` scripts already pass `--config ./config/...` to each tool) | **NO ACTION — out of MINI's root-file-hygiene scope** |

Root is already mostly migrated to the `config/` convention from a prior pass (ESLint, Vitest, lint-staged, pre-commit, docker-compose, `.prettierrc` all present under `config/` with explicit `--config` flags in `package.json`). The two remaining stragglers — `playwright.config.ts` and `vite.config.js` — are flagged below as deferred, not moved.

## Duplicate / Destination Checks

Checked ROADMAP, TASKS, FEATURES, METRICS, CHANGELOG, CONTRIBUTING at both root and `docs/`. `docs/` holds `API.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `FEATURES.md`, `INSTRUCTIONS.md`, `METRICS.md`, `ROADMAP.md`, `TASKS.md`, plus `archive/` and `projects/`; none of these exist at root, so there is **no** root/`docs/` duplicate for the tracked planning docs. No `CONTRIBUTING.md` found at either location (absent, not a duplicate).

**Found instead: `tsconfig.json` exists at both root and `config/tsconfig.json`**, which is outside the planning-doc set MINI.md names but the same class of problem (two copies of one config, risk of silent drift):

| Path | Last commit affecting path (shallow clone, single commit visible) | Notes |
|------|------|------|
| `tsconfig.json` (root) | 2026-10-21 (`a44d209`) | `include` lists `src/**/*` and `config/vitest.setup.ts`; `paths` alias `@/* → src/*`. This is the one `tsc --noEmit` (the `typecheck` npm script) resolves by default since it passes no `--project` flag. |
| `config/tsconfig.json` | 2026-10-21 (`a44d209`) | `include` is `../src/**/*` (relative to `config/`); otherwise near-identical compiler options, formatted with different indentation. No script, CI workflow, or `tsconfig`-aware tool (`vite-tsconfig-paths`, editor settings) references this path explicitly. |

Both files were touched in the same commit in this shallow clone, so commit recency can't disambiguate which is the "real" one — a `--depth 1` clone only shows the one commit present. Nothing in `package.json`, `vite.config.js`, or either Vitest/ESLint config references `config/tsconfig.json` by path, so it's unclear whether it's a leftover from an earlier config-migration attempt or intentionally used by an IDE/tool not visible in scripts. Per MINI.md's non-destructive rule, this is a **conflict, not a move target**: don't move the root copy into `config/` (destination occupied) and don't delete either copy (deletion is out of scope for a non-destructive pass). Flagged below for the Overseer.

## Proposed Moves (Dry Run — Not Executed)

**None executed.** Two deferred candidates noted above (`playwright.config.ts`, `vite.config.js`) — both load-bearing enough (direct relative import in `vite.config.js`'s case; CI/script wiring unverified for `playwright.config.ts`) that a move should land with its own validation pass, not bundled into this audit.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md`, `LICENSE` | Root-only per MINI.md |
| `.gitignore`, `.dockerignore`, `.env.example` | Standard root-required files |
| `.husky/` | Husky-managed git hooks, root-sensitive |
| `Dockerfile`, `index.html` | Build entry points resolved from repo root by default |
| `netlify.toml`, `render.yaml` | Deploy platforms resolve these from repo root by default |
| `package.json`, `package-lock.json` | Node manifest/lockfile, canonical root location |
| `vite.config.js` | `scripts/develop.js` imports it directly via relative path; moving needs a coordinated import update |

## Overseer Decisions Required

- **`tsconfig.json` duplicate (root vs. `config/`)**: decide which copy is canonical and remove the stale one in a follow-up (destructive) pass. This repo isn't one vigil tracks for config-file multi-location support (that table covers `.pre-commit-config.yaml`, ESLint/Vitest/Playwright/`.pylintrc`/`.lighthouserc*` configs, not `tsconfig.json`), so there's no existing "root OR config/ accepted" precedent to fall back on here — this needs a human call, not an automated resolution.

## Out-of-Scope Observations

- `playwright.config.ts` and `vite.config.js` are the only two tool configs left at root while every sibling tool config (ESLint, Vitest, lint-staged, pre-commit, Prettier, docker-compose) already lives under `config/` with explicit `--config` wiring in `package.json`. Worth a dedicated follow-up to finish that migration consistently, rather than leaving two exceptions indefinitely.

## Errors Encountered

None — root read from a clean `--depth 1` clone at `/home/user/darkmoon`.

## Suggested Follow-up

1. Overseer: resolve the `tsconfig.json` root/`config/` duplicate (pick canonical copy, delete the other).
2. Optional, low priority: finish the config-consolidation pass for `playwright.config.ts` and `vite.config.js` into `config/`, updating `scripts/develop.js`'s import and any CI/script invocations accordingly, with its own validation run (`npm run build`, `npm run test:ci`, `npx playwright test`).

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/darkmoon`.*
