# eng-mini: darkmoon — 2026-09-10 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 2–3 most recently pushed in-scope repos (last commit 2026-09-10T13:54:39-04:00, `chore(deps): bump the minor-and-patch group with 11 updates (#444)`).

## Root Audit — darkmoon/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.claude/` | Tooling | Not a root file; agent-local config | **KEEP** |
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.github/` | VCS/CI | Required-root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.husky/` | Tooling | Git hooks dir, path-sensitive | **KEEP** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** (candidate-move) |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** (candidate-move) |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Explicitly protected in MINI.md until global doc folder standards established | **KEEP** (required-root, protected) |
| `README.md` | Documentation | Root-only (deploy badges) | **KEEP** (required-root) |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `index.html` | App Entry | Vite entry point — must stay root | **KEEP** (required-root) |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** (required-root) |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** (required-root) |
| `package.json` | Package Manifest | Must stay root | **KEEP** (required-root) |
| `playwright.config.ts` | Config | `testDir`/`globalSetup` resolve from config file location — move requires path updates | **KEEP** (unknown/deferred — could go to `config/` with edits) |
| `render.yaml` | Build/Deploy | Render reads from repo root | **KEEP** (required-root) |
| `test-results/` | Build Artifact | Tracked in git but not gitignored — looks accidental, not a root-hygiene item | **FLAG (out of scope)** |
| `tsconfig.json` | Config | Must stay root | **KEEP** (required-root) |
| `vite.config.js` | Config | Must stay root | **KEEP** (required-root) |

Note: `config/` already holds `.pre-commit-config.yaml`, `.prettierrc`* (wait — actually `.prettierrc` per MINI.md must stay root, verify below), `docker-compose.yml`, `eslint.config.js`, `lint-staged.config.json`, `tsconfig.json` (build variant), `vitest.config.ts`, `vitest.setup.ts` — this repo has already completed a prior config-file MINI pass. `docs/` already holds `API.md`, `ARCHITECTURE.md`, `CONKER_BFD_BUILD_GUIDE.md`, `INSTRUCTIONS.md`, `MULTIPLAYER_GATE.md`, `MULTIPLAYER_SHOOTER_ROADMAP.md`, `TECH_DEBT.md`, `archive/`.

**Correction check on `.prettierrc`:** repo root does not contain a `.prettierrc` at all (only `config/` has one, pre-existing from an earlier pass) — no root-hygiene action needed there this run.

## Status vs. prior run (2026-09-01)

No change: `CHANGELOG.md` and `FEATURES.md` are still at root — the 2026-09-01 report's proposed moves were not yet executed (consistent with report-mode-only operation; execution requires a separate PR pass per MINI.md governance).

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | 1 reference found (a mention, not a link), easy to update |
| `FEATURES.md` | `docs/FEATURES.md` | **Medium** | 10 references across 7 files (grew from 8/6 on 2026-09-01) — all need updating; overseer already accepts `docs/features.md` |

## References That Would Need Updating

| File | Line | Current Reference |
|------|------|-------------------|
| `.github/copilot-instructions.md` | 87 | `CHANGELOG.md` |
| `CHANGELOG.md` | 47 | `FEATURES.md` (self-referential; moves with the file) |
| `ROADMAP.md` | 16 | `FEATURES.md` |
| `TASKS.md` | 93, 147, 158 | `FEATURES.md` |
| `docs/INSTRUCTIONS.md` | 32 | `FEATURES.md` |
| `docs/MULTIPLAYER_GATE.md` | 7 | `FEATURES.md` |
| `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` | 223, 253 | `FEATURES.md` |
| `src/components/characters/player/PlayerMovement.tsx` | 303 | `FEATURES.md` (code comment — new since 2026-09-01) |

Note: `ROADMAP.md` and `TASKS.md` are deferred (not moved), so no action needed on their own cross-references this run.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — may move to `.github/` but requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `playwright.config.ts` | Tool-specific path resolution — moving breaks `testDir`/`globalSetup` unless updated |
| `index.html` / `vite.config.js` / `tsconfig.json` / `package.json` / `package-lock.json` | Standard root-required build/tooling files |
| `Dockerfile` / `.dockerignore` / `netlify.toml` / `render.yaml` | Deploy configs read from repo root by their respective platforms |
| `.env.example` / `.gitignore` | Standard root-required files |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — heavy internal cross-referencing |
| `TASKS.md` | Hold at root | Same as above |

## Known Risks / Deferred Moves

- `FEATURES.md` move risk ticked up from Medium (8 refs) to Medium (10 refs) since the last run — the reference set is growing, so execution should not be deferred indefinitely.
- `test-results/.last-run.json` remains tracked and ungitignored — unchanged from 2026-09-01, still recommend routing to CLEANUP rather than MINI.

## Errors Encountered

None.

## Suggested Follow-up

1. Execute the two low/medium-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/darkmoon/root-hygiene-2026-09-10` branch, updating the 8 references listed above, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted.
3. Flag `test-results/.last-run.json` to CLEANUP for `.gitignore` correction (repeat flag from 2026-09-01, still unaddressed).

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/darkmoon`.*
