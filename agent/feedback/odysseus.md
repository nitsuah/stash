# TASKS to automate

- cleaning up stale worktrees/branches/etc.
- copying all MD files into stash/agent/repo/ daily
- reviewing all /stash/agent/repo/.md files like README, ROADMAP, TASKS, etc. to find what we should work on next for our projects and goals and add these as "notes" to odysseus. (!-3 have "claude do x" in the title, and we can use these to track what we want to do next)
- running stash/agent/prompts/MINI.md weekly/monthly to ensure we minimize our codebase root folders as much as possible. consider output reports of what was moved, what references were updated, and any issues encountered. these reports can be stored in stash/agent/reports/ for later review. they should also include any opportunities like moving docs to docs/ provided we go and update how other apps like overseer might look or reference these docs in different locations. (features, tasks, roadmap, changelog etc.) but some cant/shouldnt move like LICENSE but might be better located in .github so they are global for all tl;dr this is an overseer decision we should make too.
- reviewing the ghoverseer.app.api to find any stale PR's or new security alerts we may need to create "notes" (todos) for.
