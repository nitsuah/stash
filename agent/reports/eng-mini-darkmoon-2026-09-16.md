# eng-mini: darkmoon — 2026-09-16 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 3 most recently updated in-scope repos (last commit 2026-09-16T04:54:16-04:00: "metrics: refresh darkmoon coverage (2026-09-11) (#447)"). Note: the top 3 repos by `updated_at` (skyview, fire, darkmoon) all show the same automated `metrics: refresh coverage` bot commit within seconds of each other — this reflects a scheduled metrics job, not necessarily the most recent human development activity. Repo discovery used GitHub code search (`user:nitsuah`, sort=updated) since the unscoped `/users/{user}/repos` REST endpoint is blocked by this session's git proxy for repos outside its attached set.
>
> This is a re-audit — darkmoon was also covered by `eng-mini-darkmoon-2026-09-01.md`. That run proposed moving `CHANGELOG.md`/`FEATURES.md` to `docs/` and deferred `LICENSE`/`ROADMAP.md`/`TASKS.md` to the Overseer; none of those were executed (all four still sit at root today), and the deferred items remain deferred here for the same reasons.

## Root Audit — darkmoon/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.husky` | Tooling | Git hooks directory — `core.hooksPath` expects it at root | **KEEP** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Protected until global doc folder standards are established | **KEEP** |
| `README.md` | Documentation | root-only (deploy badges) | **KEEP** |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `index.html` | App Entry | Vite entry point — must stay root | **KEEP** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |
| `playwright.config.ts` | Config | `testDir`/`globalSetup` resolve from config file location — moving requires path updates | **KEEP** |
| `render.yaml` | Build/Deploy | Render reads from repo root | **KEEP** |
| `tsconfig.json` | Config | Must stay root | **KEEP** |
| `vite.config.js` | Config | Must stay root | **KEEP** |

Root-level directories (`.claude`, `.github`, `config`, `docs`, `e2e`, `scripts`, `server`, `src`) already follow the MINI Folder Strategy — no action needed. `test-results/` is a directory, not a root file, and is addressed as an out-of-scope observation below (carried over from the 2026-09-01 run).

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | 1 reference (`.github/copilot-instructions.md`), easy to update |
| `FEATURES.md` | `docs/FEATURES.md` | **Medium** | 6 references across `ROADMAP.md`, `CHANGELOG.md`, `TASKS.md`, `docs/INSTRUCTIONS.md`, `docs/MULTIPLAYER_GATE.md`, `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` — all need updating; overseer already accepts `docs/features.md` |

Unchanged from the 2026-09-01 audit's conclusions (same two candidates, similar risk profile).

## References That Would Need Updating

| File | Reference |
|------|-----------|
| `.github/copilot-instructions.md` | `CHANGELOG.md` |
| `ROADMAP.md` | `FEATURES.md` |
| `CHANGELOG.md` | `FEATURES.md` (moves with the file — self-referential once colocated) |
| `TASKS.md` | `FEATURES.md` |
| `docs/INSTRUCTIONS.md` | `FEATURES.md` |
| `docs/MULTIPLAYER_GATE.md` | `FEATURES.md` |
| `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` | `FEATURES.md` |

Note: `ROADMAP.md` and `TASKS.md` themselves are deferred (not moved), so no action needed on their own cross-references this run.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `playwright.config.ts` | Tool-specific path resolution — moving breaks `testDir`/`globalSetup` unless updated |
| `index.html` / `vite.config.js` / `tsconfig.json` / `package.json` / `package-lock.json` | Standard root-required build/tooling files |
| `Dockerfile` / `.dockerignore` / `netlify.toml` / `render.yaml` | Deploy configs read from repo root by their respective platforms |
| `.env.example` / `.gitignore` / `.husky` | Standard root-required files/tooling directory |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity; unresolved since 2026-09-01 |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note; unresolved since 2026-09-01 |
| `TASKS.md` | Hold at root | Same as above; unresolved since 2026-09-01 |

## Out-of-Scope Observation (not a root-file move, flagging for CLEANUP)

- `test-results/` is still tracked in git despite `test-results/` being present in `.gitignore` — this is the same issue flagged in the 2026-09-01 report and remains unresolved 2.5 months later. Recommend CLEANUP prioritize `git rm -r --cached test-results/` so the existing ignore rule takes effect, since this keeps churning the repo on every Playwright run.

## Errors Encountered

None.

## Suggested Follow-up

1. Execute the two low/medium-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/darkmoon/root-hygiene-2026-09-16` branch, updating the 7 references listed above, then open a PR per MINI.md branch/PR governance.
2. Escalate `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer — these have now been deferred across two consecutive eng-mini runs (2026-09-01 and 2026-09-16) with no decision.
3. Escalate the still-unresolved `test-results/` tracking issue to CLEANUP; it has persisted across the same two runs.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/darkmoon`.*
