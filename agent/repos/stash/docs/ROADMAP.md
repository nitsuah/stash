---
up: "[[repos/stash]]"
source: https://github.com/nitsuah/stash/blob/main/docs/ROADMAP.md
kind: repo-doc
repo: stash
---

# Roadmap

> 🧭 [stash](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): 2026 Q1–Q2 (planning integrity, docs baseline, security hygiene, open-source
> sanitization, backend/database/SSO examples, IaC consolidation) and the completed 2026 Q3 items (Jira runbook,
> per-directory README audit) are condensed in [FEATURES](./FEATURES.md) / [CHANGELOG](./CHANGELOG.md). Every open
> 2026 Q3/Q4 item was carried into 2027 Q1 below; the old "2027 Q1+ (Backlog)" list follows it unchanged.

## 2027 Q1 (Status: Planned)

### Carried from 2026 Q3

- [ ] Naming and Consistency Cleanup (In Progress)
	- Objective: normalize anomalous filenames and tighten cross-reference accuracy across docs/scripts.
	- Sequencing Rationale: depends on Q2 architecture/runbook clarity to avoid accidental rename regressions.
	- Exit Criteria: naming standard applied, references updated, and validation checks pass.
	- Progress (2026-09-02): fixed 14 broken cross-references left over from the `IAS/` → `cloud/iac/` and `CLOUD/` → `cloud/aws/` reorganization, across docs/CHANGELOG.md, .github/copilot-instructions.md, agent/repos/stash.md, cloud/README.md, cloud/aws/examples.py, and cloud/iac/*.sh|.ps1. The `CLOUD/` casing was a live bug — it works on Windows but breaks on case-sensitive filesystems. A full filename-normalization pass across the rest of the repo remains open.

- [ ] Lightweight Validation Harness for Critical Scripts (Exploratory)
	- Objective: define repeatable smoke checks for high-impact scripts (dry-run where possible).
	- Sequencing Rationale: exploratory until script inventory and risk tiers are finalized in Q2.
	- Exit Criteria: decision record on feasibility and an initial validation workflow draft.

### Carried from 2026 Q4

- [ ] Cross-Repo Automation Catalog (Exploratory)
	- Objective: publish a discoverable catalog of script capabilities and ownership metadata.
	- Strategic Fit: improves reuse and reduces duplicate tooling across related repositories.
	- Exit Criteria: pilot catalog for one script family, with maintenance owner and update workflow.

- [ ] Operational Metrics Maturity (Exploratory)
	- Objective: define measurable quality metrics grounded in executable checks (not placeholders).
	- Strategic Fit: supports planning confidence and auditability for future PMO cycles.
	- Exit Criteria: proposed metrics list, collection method, and feasibility assessment.

- [ ] **Script dependency graph** (Exploratory)
	- Objective: auto-generate a Mermaid diagram from `imports`, `source`, and `require` calls across scripts; gives operators a visual map of inter-script dependencies before making changes.
	- Exit Criteria: CI emits an updated diagram artifact on each push; at least one script family is fully mapped.

- [ ] **Dry-run audit log** (Exploratory)
	- Objective: when any script runs with `--dry-run`, emit a structured JSON summary of planned changes (files touched, commands skipped, env vars read) as an artifact for review.
	- Exit Criteria: at least two high-impact scripts produce structured dry-run output; format documented in `docs/DRY_RUN.md`.

- [ ] **Python linting CI** (Planned)
	- Objective: add `ruff` (or `flake8`) to a GitHub Actions workflow to lint all Python examples on push.
	- Strategic Fit: catches style inconsistencies and import errors in examples before they reach readers.
	- Exit Criteria: `.github/workflows/lint.yml` runs `ruff check .` on push to `main`; zero violations.

- [ ] **PowerShell linting CI** (Planned)
	- Objective: add PSScriptAnalyzer to CI to validate all `.ps1` scripts on push.
	- Strategic Fit: ensures PowerShell scripts follow best practices; catches common mistakes before distribution.
	- Exit Criteria: CI runs `Invoke-ScriptAnalyzer` on all `.ps1` files with zero warnings at `Error` severity.

### Vault knowledge management (new, prepped 2026-09-24)

- [ ] **Obsidian orphan-detection routine** (Committed)
	- Objective: turn `agent/scripts/find-orphans.py` into a scheduled obn routine (or skill) that reports unconnected notes and proposes links.
	- Baseline: 486 notes / 241 orphans (2026-09-24). Simulated after the 16 upstream `pmo-ff` PRs merge + `sync-repos.ps1 -Prune` + `REPOS-INDEX.md`: 412 / 95, with `repos/` down to 8 known stale files.
	- Exit Criteria: routine runs weekly, trend recorded in `agent/reports/`, remaining `reports/`/`notes/`/`projects/` orphans indexed.

## 2027 Backlog (unscheduled)

- [ ] **Modernize VBA/Access tools** (Aspirational)
	- Objective: document migration paths for Remora, Sampler, and VMT from VBA/Access to web-based equivalents (e.g., Python + PostgreSQL + simple web UI).
	- Strategic Fit: VBA tools are not portable across environments and require specific Microsoft Office licenses; a migration path increases longevity.
	- Exit Criteria: migration feasibility document for at least one tool; prototype scaffolding if warranted.

- [ ] **Add test coverage to Python examples** (Aspirational)
	- Objective: introduce `pytest` unit tests for at least the Atlassian and SAAS example scripts, using `unittest.mock` or `responses` to mock HTTP calls.
	- Strategic Fit: 0% test coverage limits confidence in examples; tests prove they work against expected API shapes.
	- Exit Criteria: `pytest` runs in CI; coverage reaches at least 30% on Python example files.

- [ ] **Frontend examples** (Planned)
	- Priority: P2
	- Candidates: React/Next.js, Svelte/SvelteKit, Vue/Nuxt.js components from the nitsuah.io stack.
	- Exit Criteria: at least one framework with a CRUD page wired to the Flask/Express backend reference.

- [ ] **Cloud cost management examples** (Planned)
	- Priority: P3
	- Candidates: Cloudability, CloudHealth, CloudZero, Kubecost APIs.

- [ ] **SaaS inventory audit examples** (Planned)
	- Priority: P3
	- Candidates: Fortify-on-Demand, ZenGRC, Zylo.
