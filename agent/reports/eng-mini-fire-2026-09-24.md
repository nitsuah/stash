# eng-mini: fire — 2026-09-24 (REPORT MODE / DRY RUN)

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 3 most recently updated in-scope repos (`updated_at` 2026-09-24T17:36:41Z; PR #119 "fix: restore 70% branch coverage, enforce it in CI, fix Docker coverage perms", merged 2026-09-24T17:35:47Z — real test/coverage work from the same-day PMO audit #118, not an automated bot commit). Repo discovery used `search_repositories` (`user:nitsuah`, sort=updated); root-file discovery used `search_code` (`repo:nitsuah/fire path:/`), since this session's git proxy scopes direct repo/content access (`get_file_contents`) to `nitsuah/stash` only. `vigil` and `ats-fill` were excluded — both rank above `fire` by `updated_at` but neither has an entry under `agent/repos/*.md`.

## Root Audit — fire/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.mcp.json` | Tooling | Claude Code project config — read from repo root | **KEEP** |
| `.prettierrc` | Config | Explicit MINI rule: editors resolve upward from edited file, `config/` not in that path | **KEEP** |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `README.md` | Documentation | root-only (deploy badges) | **KEEP** |
| `coverage_summary.txt` | Generated Artifact | Test coverage output; matched by `.gitignore` pattern yet still tracked in git | **OUT OF SCOPE — flag for CLEANUP, not a root-organization move** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |

## Duplicate / Destination Checks

`CHANGELOG.md`, `FEATURES.md`, `METRICS.md`, `ROADMAP.md`, and `TASKS.md` — all present at root in the 2026-09-16 and 2026-09-23 reports — are now **gone from root** and each resolves to exactly one hit under `docs/` (`docs/CHANGELOG.md`, `docs/FEATURES.md`, `docs/METRICS.md`, `docs/ROADMAP.md`, `docs/TASKS.md`, verified via targeted `filename:` searches). The 2026-09-23 report proposed moving only `CHANGELOG.md` and `FEATURES.md` (low-risk) and deferred `ROADMAP.md`/`TASKS.md` to the Overseer, with `METRICS.md` marked **KEEP**; all five have since moved to `docs/` with no root duplicate left behind. No further action needed — root is clean on planning docs, and there's no stale root/`docs/` pair to flag.

## Proposed Moves (Dry Run — Not Executed)

**None.** All 11 remaining root files are required-root, an existing Overseer-deferred item (`LICENSE`), or an existing out-of-scope CLEANUP item (`coverage_summary.txt`). The two moves proposed on 2026-09-16 and repeated on 2026-09-23 (`CHANGELOG.md`, `FEATURES.md` → `docs/`) have now been executed, along with `METRICS.md`, `ROADMAP.md`, and `TASKS.md` beyond what was proposed.

## References That Would Need Updating

N/A this run — no new moves proposed.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — requires human review |
| `.mcp.json` | Claude Code tooling reads this from repo root; no documented alternate location |
| `.prettierrc` | Explicit MINI.md rule — must stay root |
| `package.json` / `package-lock.json` / `Dockerfile` / `.dockerignore` / `netlify.toml` | Standard root-required build/tooling/deploy files |
| `.env.example` | Standard root-required file |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity; unresolved carryover from 2026-09-16/2026-09-23 |

## Out-of-Scope Observations (not a root-file move, flagging for CLEANUP)

- `coverage_summary.txt` remains tracked in git despite matching the repo's own `.gitignore` pattern — unchanged across three consecutive reports (2026-09-16, 2026-09-23, today). Recommend CLEANUP evaluate `git rm --cached coverage_summary.txt` (no working-tree deletion) so the existing `.gitignore` rule takes effect.

## Errors Encountered

None — `search_code path:/` returned 11 root entries, consistent with 5 fewer than the 2026-09-23 report's 16 (matching exactly the 5 planning docs confirmed moved to `docs/` above).

## Suggested Follow-up

1. No moves to schedule — the previously-proposed low-risk moves are done, and the two remaining root files needing a decision (`LICENSE`) are unchanged Overseer carryovers.
2. Bring `LICENSE` to the Overseer for a placement decision — now a repeat item across three consecutive MINI reports.
3. Flag `coverage_summary.txt` to CLEANUP for untracking — now a repeat finding across three consecutive MINI reports.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/fire`.*
