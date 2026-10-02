---
HEAD: 16e0b1df5a1727c94ee44c3764166c8b9c9c3b85
kind: eng-mini
repo: stash
date: 2026-10-01
---

# eng-mini: stash — 2026-10-01 (REPORT MODE / DRY RUN)

> 🧭 [[repos/stash|stash]] · ← [[reports/eng-mini-stash-2026-09-30|2026-09-30]] <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as the #3 most recently active tracked repo this run (`git log -1 --format=%ci` from this session's own synced checkout: 2026-10-01T21:50:24+00:00, HEAD `16e0b1d` "chore(privacy): remove personal data found in a whole-repo sweep (#179)"). Root audited directly from this session's working checkout at `/home/user/stash` (already synced to `origin/main` at the top of this run — no separate throwaway clone was needed or made, since a fresh clone to `/home/user/stash` would have clobbered this session's own mid-branch working copy).

## Root Audit — stash/

| File/Dir | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.claude/` | Tooling | Claude Code project config — read from repo root | **KEEP** |
| `.git/` | VCS internal | N/A | **N/A (not a content file)** |
| `.gitattributes` | VCS | Must stay root | **KEEP** |
| `.githooks/` | Tooling | `core.hooksPath` set to `.githooks` — relative to repo root | **KEEP** |
| `.github/` | Community health / CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.gitleaks.toml` | Config | Invoked with an explicit `--config` flag in both CI (`.github/workflows/ci.yml:69`) and the pre-commit hook (`.githooks/pre-commit:19`), but both hardcode the root-relative path (`--config .gitleaks.toml` / `--config /repo/.gitleaks.toml`) — a move is low-risk but not free: both call sites would need their flag value updated to the new path | **DEFER** — candidate-move to `config/`, but no `config/` directory exists at root yet; creating one for a single file is a broader reorg than this pass should make unilaterally (unchanged from the 2026-09-30 finding) |
| `.obsidian/` | Tooling | Obsidian vault config — read from vault root, same class as `.git/` | **KEEP** |
| `LICENSE` | Legal | **Decided 2026-09-24: stays at root in every repo** (GitHub only detects a license at root) | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `pyproject.toml` | Tooling manifest | Python manifest; ruff/similar tools resolve it by walking up from cwd, but root is the canonical location | **KEEP** |
| `SAAS/`, `agent/`, `atlassian/`, `backend/`, `cloud/`, `database/`, `docs/`, `git/`, `pages/`, `projects/`, `sso/`, `windows/` | Pre-existing top-level content directories | Already organized per the repo's own Folder Strategy; not loose root files | **NO ACTION — out of MINI's root-file-hygiene scope** |

## Duplicate / Destination Checks

`docs/` already holds `CHANGELOG.md`, `FEATURES.md`, `METRICS.md`, `ROADMAP.md`, `TASKS.md`. None of these exist at root, so there is no root/`docs/` duplicate pair — unchanged from the 2026-09-30 finding. No `CONTRIBUTING.md` found at either location.

## Proposed Moves (Dry Run — Not Executed)

**None.** No low-risk, unambiguous-destination move identified this run. `.gitleaks.toml` remains a plausible candidate but stays deferred (see Root Audit) since it would require creating a new `config/` directory rather than filling an existing one.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md |
| `.gitattributes`, `.gitignore` | Standard root-required files |
| `.claude/`, `.obsidian/` | Tooling reads these from repo/vault root by convention, same class as `.git/` |
| `.githooks/` | `core.hooksPath` points here; moving breaks hook resolution without a config change |
| `LICENSE` | **Root-placement decided 2026-09-24** — GitHub only detects a license at root; excluded from Overseer Decisions per MINI.md |
| `pyproject.toml` | Python tooling manifest, canonical root location |

## Overseer Decisions Required

None. (`LICENSE` is resolved per the 2026-09-24 decision and is intentionally excluded from this table per MINI.md.)

## Out-of-Scope Observations

- The `.playwright-mcp/` directory flagged in the 2026-09-30 report (tracked Playwright MCP page-snapshot YAML files that looked like accidentally-committed runtime output) is no longer present at root as of this HEAD — appears to have been cleaned up since. No further action needed.

## Errors Encountered

None — root read directly from this session's synced `/home/user/stash` checkout (HEAD matches `origin/main` as fetched at the start of this run).

## Suggested Follow-up

1. No moves to schedule this run — root is unchanged since 2026-09-30 aside from the `.playwright-mcp/` cleanup (good) and continued accrual of commits under `agent/`.
2. If a `config/` directory is ever created for another reason, revisit `.gitleaks.toml` as a low-risk move — both call sites use an explicit `--config` flag already, but their hardcoded path values (`ci.yml:69`, `.githooks/pre-commit:19`) would need updating to the new location as part of that move.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/stash`.*
