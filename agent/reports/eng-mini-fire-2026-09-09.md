# eng-mini: fire — 2026-09-09 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 2–3 most recently pushed in-scope repos (last commit 2026-09-07T12:16:20-04:00). First MINI run for this repo.

## Root Audit — fire/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.mcp.json` | Tooling Config | MCP clients (incl. Claude Code) discover this by convention at project root | **KEEP** |
| `.prettierrc` | Config | Editors resolve by walking upward from edited file — explicitly must-stay-root per MINI.md | **KEEP** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Protected until global doc folder standards are established | **KEEP** |
| `README.md` | Documentation | root-only (deploy badges) | **KEEP** |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `coverage_summary.txt` | Generated Artifact | Not a MINI move candidate — see Out-of-Scope Observation | **FLAG (CLEANUP)** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | Zero references found anywhere in the repo — no path updates needed |
| `FEATURES.md` | `docs/FEATURES.md` | **Low** | 3 references across 2 files, all straightforward relative-link updates; overseer already accepts `docs/features.md` |

## References That Would Need Updating

| File | Line | Current Reference |
|------|------|-------------------|
| `README.md` | 220 | `[FEATURES.md](FEATURES.md)` |
| `ROADMAP.md` | 9 | `FEATURES.md` (prose mention) |
| `ROADMAP.md` | 13 | `FEATURES.md` (prose mention) |

No references found to `CHANGELOG.md` anywhere in the repo (checked `.md`, `.json`, `.ts`, `.js`, `.yml`/`.yaml`).

Note: `ROADMAP.md` and `TASKS.md` themselves also reference each other and `docs/prod-plan.md` references both — since those two files are deferred (not moved), no action needed on those cross-references this run.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — may move to `.github/` but requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `.mcp.json` | Tooling discovery convention — MCP clients look for this at project root |
| `.prettierrc` | Explicitly must-stay-root per MINI.md (editor upward-walk resolution) |
| `package.json` / `package-lock.json` | Standard root-required npm files |
| `Dockerfile` / `.dockerignore` / `netlify.toml` | Deploy configs read from repo root by their respective platforms |
| `.env.example` / `.gitignore` | Standard root-required files |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity; same open item flagged for kryptos and darkmoon |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — named explicitly as requiring validation before move |
| `TASKS.md` | Hold at root | Same as above |

## Out-of-Scope Observation (not a root-file move, flagging for CLEANUP)

- `coverage_summary.txt` is listed in `.gitignore` (line 4) but is still tracked in git (`git ls-files` returns it) — an orphaned artifact committed before the ignore rule took effect, same pattern flagged for kryptos's `.playwright-mcp/` and darkmoon's `test-results/`. Recommend CLEANUP `git rm --cached coverage_summary.txt`.
- `.mcp.json` hardcodes an absolute Windows path (`cwd: "C:\\Users\\ajhar\\code\\fire"`) for the `fire-tracker` MCP server. Not a root-placement issue, but worth flagging: this makes the checked-in config non-portable across machines/contributors. Recommend CLEANUP or a follow-up task make the `cwd` relative or derive it at runtime.

## Errors Encountered

None.

## Suggested Follow-up

1. Execute the two low-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/fire/root-hygiene-2026-09-09` branch, updating the 3 references listed above, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted (consider batching this decision once across kryptos, darkmoon, and fire rather than three separate reviews).
3. Flag `coverage_summary.txt` to CLEANUP for untracking.
4. Flag the hardcoded Windows path in `.mcp.json` as a portability follow-up (outside MINI scope).

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/fire`.*
