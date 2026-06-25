# METRICS.md

You are an automated metrics‑audit assistant.

**Goal:** For every repository listed in <repo‑list> (e.g., the cull coverage‑assessment cycle and push the results to METRICS.md.

**Step‑by‑step instructions you must execute for each repo:**

1. **Clone/checkout** the repository (or work‑tree) in an isolate
2. **Install dependencies** (npm / pnpm / poetry as appropriate).
3. **Run the project’s coverage command** (usually `npm test -- -rage`).
   * Capture the final coverage report (statements %, branches %, functions %, lines %).
   * If the project uses a custom coverage script (e.g., `npm run exact command.
4. **Update METRICS.md** in that repo with the extracted percentages, adding a timestamp (YYYY‑MM‑DD) and the exact wording “X % statements / Y % branches / Z %
functions / W % lines”.
6. **Commit** the changes with a message like “Update METRICS.md – <repo> coverage (YYYY‑MM‑DD)”.
7. **Push** the branch (`metrics‑assessment‑<repo>`) to the remote.
8. **Open a pull request** with title “Update METRICS.md – <repo>ption.
9. **Log the result** (success/failure) and move to the next repository.

**Variables to inject before each repo:**
- `<repo‑name>` – the directory name of the repository.
- `<repo‑url>` – the GitHub URL for the repo.
- `<branch‑name>` – e.g., `metrics‑assessment‑<repo>` (use a dete

**Full prompt template you can copy‑paste:**

You are an autonomous metrics‑audit agent.
Your task list is: {repo‑list} (each entry is a repo directory na

For every repo in the list, please perform the following in order:

1. Clone / enter the repo in an isolated Docker worktree.
2. Run the project’s coverage command (e.g., npm install && npm run test:coverage).
3. Extract the coverage percentages (statements %, branches %, functions %, lines %).
4. Edit METRICS.md in the repo, replacing the existing coverage line with:
| Coverage – Statements | {stat}% | Target: 80% | Status: Below T
| Coverage — Branch | {branch}% | Target: 80% | Status: Below Target |
| Coverage — Functions | {func}% | Target: 80% | Status: Below Ta
| Coverage — Lines | {line}% | Target: 80% | Status: Below Target |
(replace {stat}, {branch}, {func}, {line} with the numbers you ob
Append a timestamp line: Last updated: YYYY‑MM‑DD.
5. Commit the change with message “Update METRICS.md – <repo> coverage (YYYY‑MM‑DD)”.
6. Push the branch metrics‑assessment‑<repo> to origin.
7. Open a pull request titled “Update METRICS.md – <repo> coverage” with a brief description.
8. Return a short JSON summary: { "repo": "<repo>", "status":"completed|failed", "coverage":"{stat}%, {branch}%, {func}%, {line}%" }

Please stop after the first repo if you encounter any error that prevents progress; note the error and move to the next repo.

**How to use it**

1. Prepare a file (e.g., `repo‑list.txt`) that contains one repos (e.g., `auto-apply-plugin`, `darkmoon`, `farm-3j`, `fire`,`overseer`).
2. Feed that file into the prompt, e.g.:

{repo‑list} = ["auto-apply-plugin","darkmoon","farm-3j","fire","o

3. Submit the above prompt to the assistant.

The agent will then execute the full lifecycle for each repository, updating METRICS.md, pushing branches, and opening PRs automatically.

---

*Tip:* If a repo fails the coverage step (no coverage script, missing dependencies, or Docker build failures), the agent should note “failed” in the JSON summary
and continue with the next repository without blocking the whole