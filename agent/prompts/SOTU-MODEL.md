# SOTU-MODEL

You are the model step of the weekly SOTU, run headless through `pipeline-run.mjs sotu`. The deterministic build already ran: `agent/reports/sotu/sotu-<YYYY>-W<ww>.md`, `sotu-data.json` and the sidecar `sotu-verify.json` exist in this checkout. Do only the judgment below. Do not commit, push, publish, or edit anything outside `agent/reports/sotu/`.

1. Read `agent/reports/sotu/sotu-verify.json`. Skip entries with `skip_model: true`. For each entry with `pr_hints`, a `path_checks` result, `changed`, or `lookup_failed`, read the hinted PR with `gh pr view <n> -R <repo> --json title,body,mergedAt` and, only if that does not settle it, the issue the item names with `gh issue view`.
2. Classify each judged item: **done** (a merged PR or closed issue names it), **partly done**, or **unclear**. Do not close items at the source here; list them under "check:" in the note so a human or the Claude-plan run can open the docs PRs.
3. Write the focus note: 2-4 plain sentences. What changed (use the `delta` block in `sotu-data.json`), the one thing that most needs the user, which kickoff item looks most worth starting and why, plus any "check: ..." items.
4. Replace the `<!-- focus -->` line in the `.md` with the note, and set `"focus"` to the same text in `sotu-data.json` (rewrite the file with valid JSON).

Counts and generic content only: stash is public. If a `gh` call fails, say which item you could not check.
