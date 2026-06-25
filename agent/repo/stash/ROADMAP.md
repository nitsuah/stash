# Roadmap

Last Updated: 2026-06-08

## 2026 Q1–Q2 ✅

> Completed. Planning integrity reset, documentation baseline, security hygiene pass, open-source sanitization, backend/database/SSO examples, and IaC consolidation all shipped.

## 2026 Q3 (Status: Planned)

- [ ] Naming and Consistency Cleanup (Committed)
	- Objective: normalize anomalous filenames and tighten cross-reference accuracy across docs/scripts.
	- Sequencing Rationale: depends on Q2 architecture/runbook clarity to avoid accidental rename regressions.
	- Exit Criteria: naming standard applied, references updated, and validation checks pass.

- [ ] Lightweight Validation Harness for Critical Scripts (Exploratory)
	- Objective: define repeatable smoke checks for high-impact scripts (dry-run where possible).
	- Sequencing Rationale: exploratory until script inventory and risk tiers are finalized in Q2.
	- Exit Criteria: decision record on feasibility and an initial validation workflow draft.

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
