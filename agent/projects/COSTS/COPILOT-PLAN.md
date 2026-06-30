# Repository Copilot Audit (Ruthless Optimization)

| Repository | Last Activity | Is Fork | Role | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **9router** | 2026-06-27 | true | Core/Tool | **THROTTLE** |
| **fire** | 2026-06-26 | false | Utility | **THROTTLE** |
| **kryptos** | 2026-06-26 | false | Research | **KILL** |
| **farm-3j** | 2026-06-26 | false | Marketing | **KILL** |
| **overseer** | 2026-06-25 | false | Tool | **KEEP** |
| **games** | 2026-06-25 | false | Project | **THROTTLE** |
| **darkmoon** | 2026-06-25 | false | Project | **THROTTLE** |
| **vhs** | 2026-06-25 | false | Project | **KILL** |
| **stash** | 2026-06-26 | false | Legacy | **KILL** |
| **motor-pool** | 2026-06-25 | false | Tool | **KEEP** |
| **auto-apply-plugin** | 2026-06-25 | false | Tool | **THROTTLE** |
| **odysseus** | 2026-06-25 | true | Project | **KILL** |
| **skyview** | 2026-06-22 | false | Marketing | **KILL** |
| **osrs** | 2026-06-22 | false | Automation | **KILL** |
| **avatar** | 2026-06-22 | false | Project | **KILL** |
| **bb-mcp** | 2026-06-22 | false | Tool | **KILL** |
| **opencut-classic** | 2026-06-09 | true | Legacy | **KILL** |
| **gcp** | 2026-06-17 | false | Tool | **KILL** |
| **.github** | 2026-06-17 | false | Config | **KILL** |
| **initiative-opensource-release**| 2025-11-24 | true | Archive | **KILL** |

---

### Logic
- **KILL (14 Repos)**: Forks, old legacy, marketing, or research that doesn't need active AI coding assistance. Disabling completely will save the bulk of your tokens.
- **THROTTLE (4 Repos)**: Active, but can be manually triggered. Use only when human interaction is required. Disable auto-PR bot reviewers.
- **KEEP (2 Repos)**: Your "high-bus-factor" tools (`overseer`, `motor-pool`) that require full AI support.

### Action Steps (Run these commands)
1. **To Disable for a repo:**
   `gh api -X PATCH /repos/nitsuah/<REPO> -f "has_github_copilot_seat=false"`
2. **Action plan:** Run this for all `KILL` repos. Keep `KEEP`. For `THROTTLE`, check if you can disable "GitHub Actions / Reviewer Bots" in the repository settings UI.
