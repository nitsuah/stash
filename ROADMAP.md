# Roadmap

Last Updated: 2026-04-03 (pmo/q2-2026-planning)

## 2026 Q2 (Status: In Progress)

- [ ] Planning Integrity Reset (Committed)
	- Objective: bring `TASKS.md` and `ROADMAP.md` into parser-safe, evidence-backed alignment with current repository behavior.
	- Why Now: current planning artifacts were stale and referenced work outside observed repository scope.
	- Exit Criteria: PMO-compliant structure in place, priorities mapped to verified gaps, and clear sequencing established.

- [ ] Documentation Baseline for Script Operations (Committed)
	- Objective: document safe execution guidance for script families in `atlassian/`, `git/`, `ias/`, `projects/`, and `windows/`.
	- Why Now: scripts can affect infrastructure, branches, and local files; safe usage must be explicit.
	- Exit Criteria: architecture map and runbook include prerequisites, parameters, dry-run paths, and risk notes.

- [ ] Repository Security Hygiene Pass (Committed)
	- Objective: run and record a sensitive-data and hardcoded-hostname scan with remediation tasks.
	- Why Now: repository contains operational automation and should prove absence of exposed secrets.
	- Exit Criteria: scan results captured, findings remediated or tracked, and `.gitignore` hardened if gaps are found.

- [ ] Open-Source Safety Sanitization Pass (Committed)
	- Objective: scrub documents and examples for overly specific/proprietary organizational details so the repo is safe for broader sharing.
	- Why Now: planning includes possible public/open-source exposure; docs should avoid confidential context.
	- Exit Criteria: sensitive references are removed or generalized and a sanitization checklist result is recorded.

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

## Completed Milestones

- [x] Initial repository bootstrap and governance baseline (`LICENSE`, `SECURITY.md`, `.github` templates present).