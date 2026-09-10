# eng-mini: auto-apply-plugin — 2026-09-10 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 2–3 most recently pushed in-scope repos (last commit 2026-09-10T13:54:30-04:00, `chore(deps): bump the minor-and-patch group with 2 updates (#63)`). First MINI audit for this repo — no prior report on file.

## Root Audit — auto-apply-plugin/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.github/` | VCS/CI | Required-root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** (candidate-move) |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** (candidate-move) |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Explicitly protected in MINI.md until global doc folder standards established | **KEEP** (required-root, protected) |
| `README.md` | Documentation | Root-only (deploy badges/store listing text) | **KEEP** (required-root) |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `manifest.json` | Extension Manifest | Chrome extension manifest — must stay root (extension root is the package root) | **KEEP** (required-root) |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** (required-root) |
| `package.json` | Package Manifest | Must stay root | **KEEP** (required-root) |

`config/` already holds `.pre-commit-config.yaml`, `docker-compose.yml`, `eslint.config.mjs`, `playwright.config.mjs` — a prior config-file MINI pass appears to have happened even though no `agent/reports/eng-mini-auto-apply-plugin-*.md` exists on file (possibly done manually or by CLEANUP). `docs/` currently holds only `PRIVACY.md`. Root also has directories `background/`, `content/`, `data/`, `icons/`, `lib/`, `popup/`, `screenshots/`, `scripts/`, `tests/`, `test-results/` — none are root-file clutter (all are implementation/asset trees, no move classification applies).

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | No cross-file references found; overseer already accepts `docs/changelog.md` |
| `FEATURES.md` | `docs/FEATURES.md` | **Low** | Only 1 reference found (`ROADMAP.md`); overseer already accepts `docs/features.md` |

## References That Would Need Updating

| File | Line | Current Reference |
|------|------|-------------------|
| `ROADMAP.md` | 9 | `FEATURES.md` (`> Completed. See FEATURES.md for shipped capabilities.`) |

Note: `ROADMAP.md` and `TASKS.md` are deferred (not moved) and contain a couple of cross-references to each other (`TASKS.md:40` → `ROADMAP.md`; `ROADMAP.md:34,43` → `TASKS.md`) — since neither file moves this run, no action needed on those.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges / store listing live here) |
| `LICENSE` | Overseer decision — may move to `.github/` but requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `manifest.json` / `package.json` / `package-lock.json` | Standard root-required manifest/tooling files |
| `Dockerfile` / `.dockerignore` | Deploy configs read from repo root |
| `.env.example` / `.gitignore` | Standard root-required files |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — named explicitly as requiring validation before move |
| `TASKS.md` | Hold at root | Same as above |

## Known Risks / Deferred Moves

- Lowest reference-count repo of this run's three (`FEATURES.md` has only 1 external reference vs. darkmoon's 10) — both proposed moves are low-risk and good first candidates for execution.
- No prior eng-mini report exists for this repo; recommend establishing a baseline report cadence going forward given how active it is (dependabot lands frequent dependency PRs here).

## Errors Encountered

None.

## Suggested Follow-up

1. Execute both low-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/auto-apply-plugin/root-hygiene-2026-09-10` branch, updating the single `ROADMAP.md` reference, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted.
3. Add this repo to the regular eng-mini rotation given it has never been audited before this run.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/auto-apply-plugin`.*
