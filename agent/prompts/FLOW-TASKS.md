# AGENT FLOW PROMPT: TASK/ROADMAP-DRIVEN DELIVERY

**Instructions for all agents:**

1. **Parse TASKS.md and ROADMAP.md**  
   - Read and summarize all open tasks and roadmap items.
   - Prioritize by urgency, dependencies, and business value.

2. **Select Next Actionable Item(s)**  
   - Choose the highest-priority item(s) that are unblocked and ready for work.
   - If none are actionable, update TASKS.md/ROADMAP.md with blockers or next steps.

3. **Create/Update Handoff Artifact**  
   - Fill out or update the HANDOFF.md template for the selected task/feature.
   - Ensure all context, scope, and acceptance criteria are clear.

4. **Branch/PR Creation**  
   - Create a feature branch for the selected item.
   - All work for this item must be coordinated on this branch/PR.

5. **Run the Agent Delivery Loop**  
   - PMO: Confirm task/roadmap context, update docs, and approve brief.
   - DevOps: Prepare environment, branch, and CI.
   - Software Engineer: Implement code, tests, and docs.
   - QA: Validate against acceptance criteria.
   - Oncall: Triage feedback/incidents if needed.
   - Loop: PMO reviews, updates plans, and closes or cycles to next item.

6. **Repeat**  
   - After closing/completing an item, return to step 1 and repeat for the next highest-priority task.

**Rules:**
- Never skip TASKS.md or ROADMAP.md review.
- Always update handoff artifacts and status in docs.
- Only one agent owns a branch/PR at a time.
- Document blockers and improvement ideas as you go.
