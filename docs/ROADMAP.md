# Roadmap

Last Updated: 2026-09-02

## 2026 Q1–Q2 ✅

> Completed. Planning integrity reset, documentation baseline, security hygiene pass, open-source sanitization, backend/database/SSO examples, and IaC consolidation all shipped.

## 2026 Q3 (Status: Planned)

- [ ] Naming and Consistency Cleanup (In Progress)
	- Objective: normalize anomalous filenames and tighten cross-reference accuracy across docs/scripts.
	- Sequencing Rationale: depends on Q2 architecture/runbook clarity to avoid accidental rename regressions.
	- Exit Criteria: naming standard applied, references updated, and validation checks pass.
	- Progress (2026-09-02): fixed 14 broken cross-references left over from the `IAS/` → `cloud/iac/` and `CLOUD/` → `cloud/aws/` reorganization, across docs/CHANGELOG.md, .github/copilot-instructions.md, agent/repos/stash.md, cloud/README.md, cloud/aws/examples.py, and cloud/iac/*.sh|.ps1. The `CLOUD/` casing was a live bug — it works on Windows but breaks on case-sensitive filesystems. A full filename-normalization pass across the rest of the repo remains open.

- [ ] Lightweight Validation Harness for Critical Scripts (Exploratory)
	- Objective: define repeatable smoke checks for high-impact scripts (dry-run where possible).
	- Sequencing Rationale: exploratory until script inventory and risk tiers are finalized in Q2.
	- Exit Criteria: decision record on feasibility and an initial validation workflow draft.

- [x] Complete the Jira Runbook (Committed)
	- Objective: fill in `atlassian/jira/RUNBOOK.md` with safe execution guidance for all Atlassian scripts.
	- Exit Criteria: runbook covers prerequisites, parameter references, dry-run steps, and known risks.

- [x] Per-Directory READMEs Audit (Committed)
	- Objective: ensure every major subdirectory has a README.md explaining what is in it and how to use it.
	- Exit Criteria: all major directories have a README.md; content is accurate and links are valid.
	- Closed 2026-09-02: all top-level directories and all 7 `projects/*` subdirectories have a README.md; added the one missing index (`projects/README.md`). `docs/` and `flipper/` are intentional exceptions (see Tasks audit notes).

## 2026 Q4 (Status: Planned)

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

## 2027 Q1+ (Backlog)

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
