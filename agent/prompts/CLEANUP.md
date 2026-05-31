# Repo Cleanup Agent Prompt

> Give this prompt to an AI agent (e.g. Claude Code) to perform a structured cleanup of any software repository. The agent should work through each phase in order, pausing to report findings before making changes in phases that are destructive or hard to reverse.

---

## Context

You are performing a structured cleanup of this repository. Your goals are:

1. Reduce root-level clutter without breaking CI/CD or tooling
2. Organize tests into meaningful tiers
3. Assess all data and documentation — migrate structured/runtime data to a database where appropriate, keep static reference data as files
4. Bring all reference and analysis documentation up to date with the actual codebase
5. Ensure the roadmap, feature list, and task backlog accurately reflect what is done vs. what is not

Work methodically. Before each destructive phase (deletes, moves, schema creation), report what you plan to do and why. Use `git mv` for all file moves so history is preserved. Never delete a file unless you've confirmed it's either migrated elsewhere or genuinely obsolete.

---

## Phase 1 — Root declutter

**Goal:** Move non-essential config files out of the project root into a `config/` directory. Leave only files that tools require at root by convention.

### Steps

1. List all files in the project root (non-directories).
2. For each file, determine: does this tool require the file to be at the repo root, or can it be moved?
3. Apply the following heuristics:

| File type | Rule |
|-----------|------|
| `.gitignore`, `.dockerignore` | Must stay at root — not configurable |
| `LICENSE`, `README.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` | Must stay at root — GitHub renders these |
| `.pre-commit-config.yaml` | Must stay at root — pre-commit only looks here |
| `pyproject.toml` / `package.json` / `Cargo.toml` (build manifests) | Must stay at root — package tooling requires it |
| `Dockerfile`, `docker-compose.yml` | Convention is root; moving requires updating all `docker build` and CI references — flag but do not move unless owner confirms |
| `pytest.ini` / `jest.config.js` / similar test config | Move into `pyproject.toml` / `package.json` `[tool.*]` sections if supported, eliminating the file entirely |
| `requirements.txt`, `requirements-dev.txt`, `.markdownlint.json`, `.pylintrc`, `eslintrc`, etc. | Move to `config/` and update all references (Dockerfile `COPY`, CI `pip install`, etc.) |
| `.env.example` | Optional — can move to `config/` if owner prefers; not consumed by any tool automatically |

4. For each file you move: update every reference to it in `Dockerfile`, CI workflow files (`.github/workflows/*.yml`), `Makefile`, scripts, and documentation.
5. Verify the build still works after moves (run `pytest` / `npm test` / equivalent to confirm nothing broke).

### Report format

Before moving anything, output a table:

| File | Action | Reason | References to update |
|------|--------|--------|----------------------|

---

## Phase 2 — Test suite organization

**Goal:** Organize a flat `tests/` directory into three tiers that reflect test speed and scope.

### Tiers

| Tier | Directory | What belongs here |
|------|-----------|------------------|
| **Smoke** | `tests/smoke/` | Fastest tests — CLI entry points, basic correctness on known inputs, quick sanity checks. Should finish in seconds. Files with "smoke", "basic", "quick", "reliability", "sanity" in name or docstring. Also fast coverage-targeted tests (`test_fast_*`). |
| **Functional** | `tests/functional/` | Unit and module tests — one function, class, or subsystem per file. The bulk of the suite. |
| **E2E** | `tests/e2e/` | End-to-end and integration tests — full pipeline runs, campaign orchestration, multi-process, multi-component. Files with "integration", "pipeline", "campaign", "orchestrat", "coordinator", "autonomous", "full" in name or docstring. |

### Steps

1. Read the test file listing and categorize each file into one of the three tiers using the rules above. When in doubt, prefer functional.
2. Create `tests/smoke/__init__.py`, `tests/functional/__init__.py`, `tests/e2e/__init__.py`.
3. Use `git mv` to move each file to its tier directory.
4. Run the test collector (`pytest --collect-only -q`) and fix any import errors caused by the move:
   - Cross-test imports (`from tests.test_foo import ...`) need their paths updated to reflect the new location
   - Relative file paths in test bodies (e.g., `open("tests/config/...")`) need their `..` depth adjusted
5. Update `pytest.ini` / `pyproject.toml` `testpaths` if needed (pytest recurses by default so `tests` usually still works).
6. Write or update `tests/README.md` documenting the three tiers and how to run each.

---

## Phase 3 — Data directory audit

**Goal:** Assess every file in `data/` (or equivalent static data directory). Determine whether each file should stay as a flat file, move to a database, be deleted, or be reorganized into subfolders.

### Decision framework

For each file, answer these questions:

1. **Is it loaded at module import time into an in-memory structure?** → Keep as flat file. Database adds latency for zero benefit.
2. **Is it runtime-appended or runtime-generated?** → Migrate to database. Append-only logs, discovered results, and decision trails belong in a queryable table.
3. **Is it a stale snapshot / test artifact with no production reader?** → Delete.
4. **Is it referenced by CLI `--flag` arguments?** → Check if the value is also in a config file. If yes, make the flag optional and delete the file. If no, keep the file but organize it into a subfolder.
5. **Does the source code that reads this file use the correct path?** → Verify. Path bugs (wrong number of `..` traversals) are common and silently produce empty data.

### Report format

Before taking any action, output a table:

| File | Size | Read by | Category | Verdict | Rationale |
|------|------|---------|----------|---------|-----------|
| `data/foo.tsv` | 1.2 KB | `src/scoring.py:80` | Static lookup | Keep in `data/ngrams/` | Loaded at import into memory dict |
| `data/decisions.jsonl` | 4 KB | `src/agents/ops.py:455` | Runtime append | Migrate to DB | Append-only log; better queryable |
| `data/stale_snapshot.json` | 800 B | Nothing | Orphan | Delete | No reader; superseded by `artifacts/` |

After owner approves, execute: moves with `git mv`, DB migrations with a script, deletes with `git rm`.

---

## Phase 4 — Documentation audit and cleanup

**Goal:** Assess every file in `docs/`. Bring live reference docs up to date. Fix stale links. Migrate structured data to DB where appropriate. Archive outdated snapshots properly.

### Step 1 — Inventory and classify

For every file, assign a classification:

| Class | Definition |
|-------|-----------|
| **Active** | Current, accurate, user-facing or AI-facing reference |
| **Living** | Intentionally updated as work progresses (research state, attack queue) |
| **Archive** | Historical snapshot — do not update content; add a header note if links are stale |
| **Speculative** | Theory or hypothesis — may change; clearly labelled |
| **Stale** | Outdated and superseded; candidate for archiving or deletion |

### Step 2 — DB migration candidates

Migrate to a database table when a doc is:
- **Too large for context** (> ~500 lines of prose): chunk into a `source_chunks` table with `(document, chunk_idx, heading, body)` schema
- **Structured tabular data** that an AI or pipeline would query (confirmed facts, ruled-out hypotheses, crib candidates with provenance, timeline entries): extract rows into dedicated tables
- **Runtime-accumulated** (discovered cribs, decision logs): already handled in Phase 3

Keep as flat files when:
- The document is narrative and meant to be loaded whole as context
- It is short enough to fit in a single LLM context window
- It is a design spec, architecture doc, or analysis report

### Step 3 — Fix stale links

Grep all `.md` and `.html` files for links to files that no longer exist:
```
grep -rn "\[.*\](" docs/ | grep -oP '(?<=\()([^)]+)' | sort -u
```
For each broken link, either update it to the correct current path, remove it, or add an inline note explaining where the content moved.

### Step 4 — Update reference docs

Reference docs (`docs/reference/`) should accurately reflect the current codebase. For each reference doc:

1. List every module, class, function, and CLI command it claims exists
2. Grep the source tree to verify each one still exists at the stated path
3. Add anything that is in the source but missing from the doc
4. Remove or correct anything that has been renamed, moved, or deleted
5. Update the `Last updated:` date

### Step 5 — Update living analysis docs

For documents that track research state (what's been tried, what worked, what's ruled out):
1. Cross-reference each "status: missing" or "needs implementation" item against the actual source tree
2. Update status to ✅ Complete, ❌ Not implemented, or NULL RESULT as appropriate
3. For any attack or hypothesis listed as pending: verify whether the code exists and whether it has been run
4. Add a dated update note at the top of the document

---

## Phase 5 — Roadmap, features, and task backlog

**Goal:** Ensure ROADMAP.md, FEATURES.md (or equivalent), and TASKS.md are internally consistent and accurately reflect project state.

### Steps

1. **ROADMAP.md**
   - Read every item. For each: is it actually done? Check `git log`, source code, and test coverage.
   - Move completed items to a "Completed" section or remove them entirely (they belong in CHANGELOG or the audit doc, not the roadmap).
   - Add any actionable improvements identified during Phases 1–4 that are not yet tracked.
   - Keep only forward-looking work.

2. **FEATURES.md** (or equivalent capability doc)
   - For each feature listed: verify it still exists in the source tree.
   - Add features that exist in the code but are missing from the doc (common after rapid development sprints).
   - Update test counts, success rates, and status notes to match current reality.
   - Add a "Planned" section that mirrors the active roadmap items.

3. **TASKS.md** (or equivalent backlog)
   - Verify every TODO item is still relevant.
   - Mark or remove items that were completed during Phases 1–4 of this cleanup.
   - Ensure items identified as gaps during the audit are added.

---

## Phase 6 — Final verification

Run the full test suite and confirm:
- [ ] All tests collect without import errors
- [ ] No tests that previously passed are now failing
- [ ] CI workflow files reference correct paths for any files that were moved
- [ ] Docker build succeeds if a Dockerfile is present
- [ ] `git status` shows only intentional staged changes — no accidental deletes or unstaged modifications

---

## General rules for this agent

- **Use `git mv`** for all file moves — never copy-and-delete
- **Use `git rm`** for all deletions — never `rm`
- **Read before editing** — always read a file before writing or editing it
- **Verify imports after moves** — run the test collector after every batch of moves
- **Never skip CI config** — always update `.github/workflows/`, `Dockerfile`, `Makefile`, and any scripts that reference moved files
- **Preserve history** — do not squash or amend commits; create new commits for each logical phase
- **Ask before DB schema changes** — propose the schema, wait for approval, then create tables
- **Document null results** — if an attack, migration, or refactor produces no change (e.g. a feature already worked correctly), note that explicitly rather than claiming it was fixed
