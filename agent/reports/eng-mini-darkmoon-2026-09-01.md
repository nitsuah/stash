# eng-mini: darkmoon — 2026-09-01 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 2–3 most recently pushed in-scope repos (last commit 2026-09-01T03:03:41-04:00).

## Root Audit — darkmoon/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
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

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | Only 1 reference found, easy to update |
| `FEATURES.md` | `docs/FEATURES.md` | **Medium** | 8 references across 6 files — all need updating; overseer already accepts `docs/features.md` |

## References That Would Need Updating

| File | Line | Current Reference |
|------|------|-------------------|
| `.github/copilot-instructions.md` | 87 | `CHANGELOG.md` |
| `CHANGELOG.md` | 23 | `FEATURES.md` (self-referential; moves with the file) |
| `ROADMAP.md` | 16 | `FEATURES.md` |
| `TASKS.md` | 93, 147, 158 | `FEATURES.md` |
| `docs/INSTRUCTIONS.md` | 32 | `FEATURES.md` |
| `docs/MULTIPLAYER_GATE.md` | 7 | `FEATURES.md` |
| `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` | 223, 253 | `FEATURES.md` |

Note: `ROADMAP.md` and `TASKS.md` themselves also contain many cross-references to each other and to `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` — since those two files are deferred (not moved), no action needed on those references this run.

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
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — named explicitly as requiring validation before move; also carries heavy internal cross-referencing |
| `TASKS.md` | Hold at root | Same as above |

## Out-of-Scope Observation (not a root-file move, flagging for CLEANUP)

- `test-results/.last-run.json` is tracked in git but `test-results/` is not in `.gitignore` — looks like an accidentally-committed Playwright artifact directory, not root clutter. Recommend the CLEANUP agent evaluate untracking it and adding it to `.gitignore`.

## Errors Encountered

None.

## Suggested Follow-up

1. Execute the two low/medium-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/darkmoon/root-hygiene-2026-09-01` branch, updating the 7 references listed above, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted.
3. Flag `test-results/.last-run.json` to CLEANUP for `.gitignore` correction.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/darkmoon`.*
