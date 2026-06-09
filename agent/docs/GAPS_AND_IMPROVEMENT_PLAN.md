# Agent System: Workflow Gaps & New Agent/Skill Opportunities

## Current Agents
- [[prompts/PMO|PMO]]: Planning, product management, documentation, and audit
- [[prompts/OPS|DevOps]]: Delivery, CI/CD, and implementation
- [[prompts/QA|QA]]: Validation, regression, and compliance
- [[prompts/Oncall|Support]]: Incident response and user feedback
- [[prompts/AUTO|Automation]]: Internal tooling and workflow automation
- [[prompts/Growth|Growth]]: Monetization and adoption

## Workflow Gaps & Opportunities

### 1. User Research & Feedback Loop
- **Gap:** No dedicated agent for structured user research, interviews, or feedback synthesis.
- **Opportunity:** Add a "User Research Agent" to run surveys, analyze feedback, and update product docs.

### 2. Security & Compliance
- **Gap:** Security reviews and compliance checks are not explicitly owned.
- **Opportunity:** Add a "Security Agent" to run threat modeling, dependency audits, and compliance checks.
- **See:** [[docs/SECURITY_CHECKLIST]] for the active security/sanitization pass.

### 3. Data & Analytics
- **Gap:** No agent for tracking, analyzing, and reporting product usage or business metrics.
- **Opportunity:** Add a "Data Analytics Agent" to own METRICS.md, dashboards, and experiment analysis.

### 4. Community & Ecosystem
- **Gap:** No agent for managing open source community, docs, or ecosystem partnerships.
- **Opportunity:** Add a "Community Agent" to handle docs, forums, and ecosystem outreach.

### 5. Internal Knowledge Management
- **Gap:** No agent for maintaining internal wikis, onboarding, or process docs.
- **Opportunity:** Add a "Knowledge Agent" to own onboarding, runbooks, and process improvement.

## Skills/Capabilities to Add
- Automated changelog and release note generation
- Dependency and license scanning
- Automated onboarding and environment setup
- Incident postmortem automation
- Growth experiment tracking
- User feedback analysis

---

# Repo Improvement & Monetization Assessment Plan

1. **Repo Audit:**
   - Review README, ROADMAP, TASKS, FEATURES, METRICS, and CONTRIBUTING for each repo.
   - Identify missing, outdated, or unclear documentation.
   - Assess test coverage, CI/CD health, and Docker support.

2. **Monetization/Portfolio Fit:**
   - For each repo, assess:
     - Product-market fit and unique value
     - Monetization potential (SaaS, open source, consulting, etc.)
     - Portfolio/demo value if not monetizable

3. **Action Plan:**
   - Prioritize improvements by impact and effort.
   - Assign to relevant agent ([[prompts/Growth|Growth]], [[prompts/PMO|PMO]], [[prompts/AUTO|Automation]], etc.)
   - Track as tasks in TASKS.md and update ROADMAP.md

4. **Continuous Review:**
   - After each cycle, update agent descriptions and checklists with lessons learned.
   - Propose new agents or skills as new gaps emerge.
