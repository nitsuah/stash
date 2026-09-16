# eng-mini: skyview — 2026-09-16 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 3 most recently updated in-scope repos (last commit 2026-09-16T04:54:24-04:00: "metrics: refresh skyview coverage (2026-09-11), flag native test failures (#129)"). Note: the top 3 repos by `updated_at` (skyview, fire, darkmoon) all show the same automated `metrics: refresh coverage` bot commit within seconds of each other — this reflects a scheduled metrics job, not necessarily the most recent human development activity. Repo discovery used GitHub code search (`user:nitsuah`, sort=updated) since the unscoped `/users/{user}/repos` REST endpoint is blocked by this session's git proxy for repos outside its attached set.

## Root Audit — skyview/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.pre-commit-config.yaml` | Config | root OR `config/` accepted, but requires editing `.git/hooks/pre-commit` `--config` flag | **KEEP (deferred, low priority)** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `Dockerfile.dev` | Build/Deploy | Must stay root | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Protected until global doc folder standards are established | **KEEP** |
| `README.md` | Documentation | root-only (deploy badges) | **KEEP** |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `SETUP.md` | Documentation | Not in MINI's recognized doc-file list; destination unclear; referenced by 10 files | **UNKNOWN — deferred, keep in place** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `config.js` | App Config | Referenced by 6 files including `index.html`; unclear if tool config or app runtime config | **UNKNOWN — deferred, keep in place** |
| `docker-compose.dev.yml` | Build/Deploy | Compose convention expects file at invocation root; moving requires updating all script references | **KEEP (low-priority candidate, not moved this pass)** |
| `index.html` | App Entry | Site entry point — must stay root | **KEEP** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |
| `playwright.config.ts` | Config | `testDir`/`globalSetup` resolve from config file location — moving requires path updates | **KEEP** |
| `robots.txt` | Static Asset | Must be served at `/robots.txt` — required at site root | **KEEP** |
| `sitemap.xml` | Static Asset | Must be served at `/sitemap.xml` — required at site root | **KEEP** |

Root-level directories (`.claude`, `.github`, `admin`, `assets`, `config`, `db`, `docs`, `netlify`, `pages`, `platform`, `scripts`, `styles`, `tests`) already follow the MINI Folder Strategy (config/src/scripts/docs separation) — no action needed.

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | 0 external references found — safe, low-effort move |
| `FEATURES.md` | `docs/FEATURES.md` | **Medium** | 4 references across `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/archive/README.md` — all need updating; overseer already accepts `docs/features.md` |

## References That Would Need Updating

| File | Reference |
|------|-----------|
| `README.md` | `FEATURES.md` |
| `ROADMAP.md` | `FEATURES.md` |
| `CHANGELOG.md` | `FEATURES.md` (moves with the file — self-referential, no separate update needed once colocated) |
| `docs/archive/README.md` | `FEATURES.md` |

`CHANGELOG.md` has no inbound references from other tracked files, so its move needs no reference updates.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `playwright.config.ts` | Tool-specific path resolution — moving breaks `testDir`/`globalSetup` unless updated |
| `index.html` / `package.json` / `package-lock.json` | Standard root-required build/tooling files |
| `Dockerfile` / `Dockerfile.dev` / `.dockerignore` / `netlify.toml` / `docker-compose.dev.yml` | Deploy configs read from repo root by their respective platforms |
| `robots.txt` / `sitemap.xml` | Static hosting requires these at the site root path |
| `.env.example` / `.gitignore` / `.pre-commit-config.yaml` | Standard root-required or root-convention files |
| `SETUP.md` / `config.js` | Destination unclear per MINI.md rule ("if destination is unclear, keep file in place and mark as deferred for review") |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — named explicitly as requiring validation before move |
| `TASKS.md` | Hold at root | Same as above |
| `SETUP.md` | Human call on whether `docs/` is an appropriate destination | Not in MINI's currently-recognized doc-file table; 10 inbound references make this a non-trivial move to plan |

## Out-of-Scope Observations (not root-file moves, flagging for CLEANUP)

- None found — `test-results/`, `test-results.json`, and `coverage/` are all correctly listed in `.gitignore` and are not tracked in git.

## Errors Encountered

None.

## Suggested Follow-up

1. Execute the two low/medium-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/skyview/root-hygiene-2026-09-16` branch, updating the 3 references listed above, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted.
3. Have a human or the Overseer decide whether `SETUP.md` and `config.js` should have a defined destination folder; both are currently unclassifiable under MINI's existing rules.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/skyview`.*
