# eng-mini: fire — 2026-09-16 (REPORT MODE / DRY RUN)

> 🧭 [[repos/fire|fire]] · [[reports/eng-mini-fire-2026-09-23|2026-09-23]] → <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 3 most recently updated in-scope repos (last commit 2026-09-16T04:54:20-04:00: "metrics: refresh fire coverage (2026-09-11) (#104)"). Note: the top 3 repos by `updated_at` (skyview, fire, darkmoon) all show the same automated `metrics: refresh coverage` bot commit within seconds of each other — this reflects a scheduled metrics job, not necessarily the most recent human development activity. Repo discovery used GitHub code search (`user:nitsuah`, sort=updated) since the unscoped `/users/{user}/repos` REST endpoint is blocked by this session's git proxy for repos outside its attached set.

## Root Audit — fire/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.mcp.json` | Tooling | Claude Code project config — read from repo root | **KEEP** |
| `.prettierrc` | Config | Explicit MINI rule: editors resolve upward from edited file, `config/` not in that path | **KEEP** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Protected until global doc folder standards are established | **KEEP** |
| `README.md` | Documentation | root-only (deploy badges) | **KEEP** |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `coverage_summary.txt` | Generated Artifact | Test coverage output; matched by `.gitignore` pattern `coverage_summary.txt` yet still tracked in git (committed 2026-09-16) | **OUT OF SCOPE — flag for CLEANUP, not a root-organization move** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |

Root-level directories (`.claude`, `.github`, `app`, `config`, `docs`, `scripts`, `tests`) already follow the MINI Folder Strategy — no action needed.

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | 0 external references found — safe, low-effort move |
| `FEATURES.md` | `docs/FEATURES.md` | **Low** | 2 references (`README.md`, `ROADMAP.md`) — easy to update; overseer already accepts `docs/features.md` |

## References That Would Need Updating

| File | Reference |
|------|-----------|
| `README.md` | `FEATURES.md` |
| `ROADMAP.md` | `FEATURES.md` |

`CHANGELOG.md` has no inbound references from other tracked files, so its move needs no reference updates.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `.mcp.json` | Claude Code tooling reads this from repo root; no documented alternate location |
| `.prettierrc` | Explicit MINI.md rule — must stay root |
| `package.json` / `package-lock.json` / `Dockerfile` / `.dockerignore` / `netlify.toml` | Standard root-required build/tooling/deploy files |
| `.env.example` / `.gitignore` | Standard root-required files |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — named explicitly as requiring validation before move |
| `TASKS.md` | Hold at root | Same as above |

## Out-of-Scope Observations (not a root-file move, flagging for CLEANUP)

- `coverage_summary.txt` is listed in `.gitignore` (pattern `coverage_summary.txt`) but is nonetheless tracked in git, with a commit as recent as 2026-09-16 — it looks like a generated test-coverage report that keeps getting force-added or was committed before the ignore rule existed. This will churn on every test run. Recommend CLEANUP evaluate `git rm --cached coverage_summary.txt` (no working-tree deletion) so the existing `.gitignore` rule takes effect.

## Errors Encountered

None.

## Suggested Follow-up

1. Execute the two low-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/fire/root-hygiene-2026-09-16` branch, updating the 2 references listed above, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted.
3. Flag `coverage_summary.txt` to CLEANUP for untracking (it is already `.gitignore`d but was committed anyway).

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/fire`.*
