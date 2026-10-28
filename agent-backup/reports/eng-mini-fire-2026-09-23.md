---
kind: eng-mini
repo: fire
date: 2026-09-23
---

# eng-mini: fire — 2026-09-23 (REPORT MODE / DRY RUN)

> 🧭 [[repos/fire|fire]] · ← [[reports/eng-mini-fire-2026-09-16|2026-09-16]] · [[reports/eng-mini-fire-2026-09-24|2026-09-24]] → <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 3 most recently updated in-scope repos (last commit 2026-09-19T07:44:03Z / 2026-09-19T03:43:57-04:00, PR #111 "Product/UI + reliability pass" — real feature/bugfix work, not an automated metrics-bot commit). Repo discovery used `search_repositories` (`user:nitsuah`, sort=updated) and root-file discovery used `search_code` (`repo:nitsuah/fire path:/`), since this session's git proxy scopes direct repo/content access (`get_file_contents`, `list_commits`) to `nitsuah/stash` only and denies the unscoped `/users/{user}/repos` REST path. `vigil` (updated 2026-09-21, most recent of all nitsuah repos) was excluded — it has no entry under `agent/repos/*.md` and is therefore not yet a tracked repo for this routine.

## Root Audit — fire/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
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
| `coverage_summary.txt` | Generated Artifact | Test coverage output; matched by `.gitignore` pattern yet still tracked in git | **OUT OF SCOPE — flag for CLEANUP, not a root-organization move** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package-lock.json` | Lockfile | Must stay root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | 0 inbound references found — safe, low-effort move |
| `FEATURES.md` | `docs/FEATURES.md` | **Low** | 2 references (`README.md`, `ROADMAP.md`) — easy to update; overseer already accepts `docs/features.md` |

Identical to the 2026-09-16 dry-run findings for this repo — neither move has been executed in the 7 days since, and `coverage_summary.txt` is still tracked despite being `.gitignore`d.

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
| `.env.example` | Standard root-required file |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note — named explicitly as requiring validation before move |
| `TASKS.md` | Hold at root | Same as above |

## Out-of-Scope Observations (not a root-file move, flagging for CLEANUP)

- `coverage_summary.txt` remains tracked in git despite matching the repo's own `.gitignore` pattern (unchanged since the 2026-09-16 report). Recommend CLEANUP evaluate `git rm --cached coverage_summary.txt` (no working-tree deletion) so the existing rule takes effect.

## Errors Encountered

None — `search_code path:/` returned exactly 16 root entries against a repo-reported total_count of 16, so the root listing is believed complete.

## Suggested Follow-up

1. Execute the two low-risk moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/fire/root-hygiene-2026-09-23` branch, updating the 2 references listed above, then open a PR per MINI.md branch/PR governance. These have now been proposed twice (2026-09-16 and today) without execution.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md` to the Overseer for an explicit placement decision before any move is attempted.
3. Flag `coverage_summary.txt` to CLEANUP for untracking — now a repeat finding across two consecutive MINI reports.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/fire`.*
