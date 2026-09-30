---
HEAD: 01a9707dc719aa47ce4a97b0c9ee485c0dd00452
kind: eng-mini
repo: stash
date: 2026-09-30
---

# eng-mini: stash — 2026-09-30 (REPORT MODE / DRY RUN)

> 🧭 [[repos/stash|stash]] · ← [[reports/eng-mini-stash-2026-09-24|2026-09-24]] <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as the #1 most recently active tracked repo (`git log -1 --format=%ci` from a fresh `--depth 1` clone: 2026-09-30T14:11:11Z, HEAD `01a9707` "docs(agents): close tracked items in the same PR, before the last push (#168)"). Root audited from a throwaway clone at `/tmp/mini-scan/stash` (kept separate from this session's own `/home/user/stash` working checkout, which is mid-branch for this same report PR).

## Root Audit — stash/

| File/Dir | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.claude/` | Tooling | Claude Code project config — read from repo root | **KEEP** |
| `.git/` | VCS internal | N/A | **N/A (not a content file)** |
| `.gitattributes` | VCS | Must stay root | **KEEP** |
| `.githooks/` | Tooling | `core.hooksPath` set to `.githooks` (see pre-commit header) — relative to repo root | **KEEP** |
| `.github/` | Community health / CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.gitleaks.toml` | Config | Already invoked with an explicit `--config` flag in both CI (`ci.yml:69`) and `.githooks/pre-commit:16,19`, so a move wouldn't break resolution | **DEFER** — candidate-move to `config/`, but no `config/` directory exists at root yet; creating one for a single file is a broader reorg than this pass should make unilaterally |
| `.obsidian/` | Tooling | Obsidian vault config — read from vault root, same class as `.git/` | **KEEP** |
| `.playwright-mcp/` | Generated artifact | Tracked in git (not in `.gitignore`); contains timestamped Playwright MCP page snapshots (`page-2026-09-28T*.yml`) — looks like an accidentally-committed runtime cache, not a misplaced *source* file | **OUT OF SCOPE** — not a move candidate (MINI relocates misplaced files, it doesn't untrack generated output); flagged below for human follow-up |
| `LICENSE` | Legal | **Decided 2026-09-24: stays at root in every repo** (GitHub only detects a license at root) | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `pyproject.toml` | Tooling manifest | Python manifest (`[tool.ruff]`); ruff/similar tools resolve it by walking up from cwd, but root is the canonical location | **KEEP** |
| `SAAS/`, `agent/`, `atlassian/`, `backend/`, `cloud/`, `database/`, `docs/`, `git/`, `projects/`, `sso/`, `windows/` | Pre-existing top-level content directories | Already organized per the repo's own Folder Strategy; not loose root files | **NO ACTION — out of MINI's root-file-hygiene scope** |

## Duplicate / Destination Checks

`docs/` already holds `CHANGELOG.md`, `FEATURES.md`, `METRICS.md`, `ROADMAP.md`, `TASKS.md`. None of these exist at root (confirmed via `ls -A` on the fresh clone), so there is no root/`docs/` duplicate pair to report — unchanged from the 2026-09-24 finding.

## Proposed Moves (Dry Run — Not Executed)

**None.** No low-risk, unambiguous-destination move identified this run. `.gitleaks.toml` is a plausible candidate but deferred (see Root Audit) since it would require creating a new `config/` directory rather than filling an existing one.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md |
| `.gitattributes`, `.gitignore` | Standard root-required files |
| `.claude/`, `.obsidian/` | Tooling reads these from repo/vault root by convention, same class as `.git/` |
| `.githooks/` | `core.hooksPath` points here; moving breaks hook resolution without a config change |
| `LICENSE` | **Root-placement decided 2026-09-24** — GitHub only detects a license at root; no longer an open Overseer item |
| `pyproject.toml` | Python tooling manifest, canonical root location |

## Overseer Decisions Required

None. (`LICENSE` is resolved per the 2026-09-24 decision and is intentionally excluded from this table per MINI.md.)

## Out-of-Scope Observations

- `.playwright-mcp/` is tracked in git and holds nine dated page-snapshot YAML files from a 2026-09-28 browsing session. This looks like tool output that should be gitignored rather than committed; removing already-tracked files is a deletion, which is out of scope for this non-destructive pass. Recommend a human (or a follow-up CLEANUP run) add `.playwright-mcp/` to `.gitignore` and `git rm --cached` the existing snapshots.
- `agent/repos/stash.md`'s open naming-consistency note from the 2026-09-23/24 runs was not re-checked this pass (no change observed at root level); still better suited to CLEANUP or a human decision than to MINI.

## Errors Encountered

None — root read from a clean `--depth 1` clone at `/tmp/mini-scan/stash`.

## Suggested Follow-up

1. No moves to schedule this run — root files are unchanged since 2026-09-24 aside from new tooling additions (`.gitattributes`, `.githooks/`, `.gitleaks.toml`, `pyproject.toml`), all correctly root-required or deferred.
2. Human review: should `.playwright-mcp/` be gitignored and untracked? (deletion, out of MINI's scope)
3. If a `config/` directory is ever created for another reason, revisit `.gitleaks.toml` as a low-risk move (both call sites already use an explicit `--config` flag).

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/stash`.*
