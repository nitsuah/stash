# Personal Agent System

Agent prompts for personal operations and a product delivery pipeline.
Each prompt defines a specific role, operating rules, and expected outputs.

---

## Agents

| Agent | File | Purpose | Cadence |
|-------|------|---------|---------|
| 💼 CFO | projects/Finance.md | Track finances, runway, CDs | Weekly or on-demand |
| 🧑‍💻 Career | projects/Career.md | Evaluate jobs, draft outreach | When job-hunting |
| 🔧 Builder | projects/Builder.md | Find leads, close web design clients | When building |

---

## Skills

| Skill | Used By | What It Does |
|-------|---------|-------------|
| `financial-summary` | CFO | Structured financial snapshots + runway calc |
| `job-evaluator` | Career | Scores roles on stress / pay / fit |
| `lead-finder` | Builder | Finds local biz leads with weak web presence |
| `outreach-writer` | Career + Builder | Drafts cold emails, DMs, follow-ups |

---

## Usage

### Option A: Claude.ai (simplest)
1. Open 3 separate Claude chats
2. Paste the contents of each `.md` file as the system prompt
3. Chat normally

### Option B: Run locally with Python
```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-...
AGENT=cfo python run_agent.py
```

### Option C: Docker
```bash
# Build
docker build -t personal-agents .

# Run CFO agent
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=cfo personal-agents

# Run Career agent
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=career personal-agents

# Run Builder agent
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=builder personal-agents
```

### Option D: Docker Compose
```bash
# Create .env file first
echo "ANTHROPIC_API_KEY=sk-..." > .env

# Run any agent
docker compose run cfo
docker compose run career
docker compose run builder
```

### Push to Docker Hub
```bash
docker tag personal-agents yourusername/personal-agents:latest
docker push yourusername/personal-agents:latest
```

---

## File Structure

```
.
├── PMO.md
├── DevOps.md
├── QA.md
├── projects/
│   ├── Finance.md
│   ├── Intake.md
│   ├── Career.md
│   └── Builder.md
├── prompts/
│   ├── HANDOFF.md
│   ├── PM.md
│   ├── TEST.md
│   ├── LOC.md
│   └── MINI.md
├── repos/
│   └── *.md
└── README.md
```

---

## Suggested Routine

| When | Agent | Action |
|------|-------|--------|
| Monday morning | CFO | "Give me my weekly summary" |
| Job opportunity appears | Career | Paste job description, get scored |
| Want to work on clients | Builder | "Find me 5 leads in [city]" |
| Recruiter messages you | Career | "Help me reply to this recruiter" |
| Ready to send outreach | Builder/Career | "Write me a message for [target]" |

---

## Notes

- All agents are in LOW EFFORT / calm mode by default
- No agent will push you to grind or overwhelm you
- Docker containerization is ready but defer to Claude.ai pasting until you have 2–3 paying clients

---

## Product Delivery Pipeline Agents

The repository now also includes a Product Delivery Pipeline agent set for product planning and execution governance.

| Agent | File | Purpose |
|-------|------|---------|
| PMO | PMO.md | Audit products, maintain ROADMAP/TASKS from evidence, enforce branch + PR governance |
| Intake | projects/Intake.md | Convert findings/requests into prioritized, acceptance-ready tasks |
| Delivery/DevOps | DevOps.md | Implement approved tasks, validate infra, CI/CD, and ship via branch + PR |
| Software Engineer | SoftwareEng.md | Implement features, refactor, fix bugs, and maintain code quality |
| QA | QA.md | Verify quality, prevent regressions, and feed improvements back into planning |
| Oncall | Oncall.md | Incident response, user feedback, and support triage |
| Automation | Automation.md | Internal tooling and workflow automation |
| Growth | Growth.md | Monetization, adoption, and growth experiments |


Recommended flow:

1. PMO audit identifies reality gaps and planning updates.
2. Intake shapes those into clear, prioritized implementation briefs.
3. Software Engineer implements features and code changes from briefs.
4. Delivery/DevOps validates infra, CI/CD, and ships via branch + PR.
5. QA validates behavior and routes defects/improvements back to TASKS/ROADMAP.
6. Oncall handles incidents and user feedback, routing actionable items to the team.
7. Automation and Growth agents support efficiency and adoption.
## Workflow Gaps & Improvement Plan

### Current Agents
- PMO: Planning, product management, documentation, and audit
- Software Engineer: Feature implementation, refactoring, bugfixes
- DevOps: Delivery, CI/CD, and infrastructure
- QA: Validation, regression, and compliance
- Oncall: Incident response and user feedback
- Automation: Internal tooling and workflow automation
- Growth: Monetization and adoption

### Workflow Gaps & Opportunities

1. **User Research & Feedback Loop**
	- Gap: No dedicated agent for structured user research, interviews, or feedback synthesis.
	- Opportunity: Add a "User Research Agent" to run surveys, analyze feedback, and update product docs.

2. **Security & Compliance**
	- Gap: Security reviews and compliance checks are not explicitly owned.
	- Opportunity: Add a "Security Agent" to run threat modeling, dependency audits, and compliance checks.

3. **Data & Analytics**
	- Gap: No agent for tracking, analyzing, and reporting product usage or business metrics.
	- Opportunity: Add a "Data Analytics Agent" to own METRICS.md, dashboards, and experiment analysis.

4. **Community & Ecosystem**
	- Gap: No agent for managing open source community, docs, or ecosystem partnerships.
	- Opportunity: Add a "Community Agent" to handle docs, forums, and ecosystem outreach.

5. **Internal Knowledge Management**
	- Gap: No agent for maintaining internal wikis, onboarding, or process docs.
	- Opportunity: Add a "Knowledge Agent" to own onboarding, runbooks, and process improvement.

### Skills/Capabilities to Add
- Automated changelog and release note generation
- Dependency and license scanning
- Automated onboarding and environment setup
- Incident postmortem automation
- Growth experiment tracking
- User feedback analysis

### Repo Improvement & Monetization Assessment Plan

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
	- Assign to relevant agent (Growth, PMO, Automation, etc.)
	- Track as tasks in TASKS.md and update ROADMAP.md

4. **Continuous Review:**
	- After each cycle, update agent descriptions and checklists with lessons learned.
	- Propose new agents or skills as new gaps emerge.

Parallel execution model:

1. PMO and Intake can prepare work in parallel across different repositories.
2. For the same repository, PMO owns planning changes and Delivery owns implementation changes on separate branches.
3. QA can run exploratory read-only checks in parallel, but final QA should happen against the Delivery branch or PR.
4. If multiple agents touch the same repo, use explicit handoff notes and avoid editing the same files concurrently.

Branch and PR conventions:

| Agent | Branch Prefix | Commit Prefix | PR Title Prefix |
|-------|---------------|---------------|-----------------|
| PMO | pmo/<repo>/... | docs(pmo): | PMO: |
| Intake | intake/<repo>/... | docs(intake): | Intake: |
| Delivery/DevOps | delivery/<repo>/... | feat:, fix:, chore:, docs: | Delivery: |
| QA | qa/<repo>/... | test(qa): | QA: |

Handoff contract:

- Use prompts/HANDOFF.md as the shared handoff artifact between PMO, Intake, Delivery, and QA.
- PMO or Intake should create the initial brief.
- Delivery should append implementation and validation details for QA.
- QA should append final findings, release recommendation, and follow-up tasks.

Operational prompt modules:

- prompts/HANDOFF.md: Shared handoff template for pipeline agents.
- prompts/PM.md: Overseer compliance formatting and documentation standards.
- prompts/TEST.md: Incremental testing and coverage strategy.
- prompts/LOC.md: LOC hotspot analysis and refactor planning.
- prompts/MINI.md: Safe repository organization and root hygiene.

## Delivery Pipeline Quick Start

1. PMO audits a repository and records findings.
2. PMO or Intake fills out prompts/HANDOFF.md.
3. Delivery executes from that handoff on a dedicated branch and opens a PR.
4. QA validates the PR using the same handoff artifact and appends findings.
5. PMO folds accepted learnings back into TASKS, ROADMAP, and repos notes.

This model allows parallel work across repositories and controlled handoffs within the same repository.

## Agent Run Order Checklist

Use this when kicking off agents against a repository:

1. Confirm the target repository, default branch, and current priority.
2. Start PMO to audit and shape planning changes.
3. If needed, start Intake to turn PMO findings into a clean implementation brief.
4. Create or update prompts/HANDOFF.md with repo context, evidence, scope, and acceptance criteria.
5. Start Delivery/DevOps on a dedicated branch using that handoff.
6. Start QA after a Delivery branch or PR exists; allow read-only exploratory QA earlier if useful.
7. Feed accepted QA findings back to PMO for TASKS, ROADMAP, and repo note updates.

Recommended launch patterns:

- Single repository, full flow: PMO -> Intake -> Delivery -> QA.
- Multiple repositories: run PMO or Intake in parallel across repos, then stagger Delivery and QA per repo.
- Emergency defect: PMO can create a minimal handoff, Delivery executes immediately, QA validates, then PMO backfills planning updates.
