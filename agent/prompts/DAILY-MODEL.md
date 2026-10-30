# DAILY-MODEL

The model-only part of [[DAILY]]. `agent/scripts/daily-run.mjs` already did everything deterministic (sync, logs, the note skeleton, indexes, commit, PR). You have Read, Write, Edit, Glob and Grep only: no shell, no git, no network. Do not run or reinvent any script.

Read `agent/reports/daily-handoff.json`. Do only what it lists, and edit only the files named here:

1. **Hub synthesis (DAILY step 2).** For each repo in `stale_hubs` first, then `changed_repos`: read that repo's changed files under `agent/repos/<repo>/` (see `mirror_diffs`; read the changed files, not the whole mirror) and refresh `agent/repos/<repo>.md` (`repos/`, plural). Update its `Reviewed:` date to the handoff `date`. Leave the `<!-- vault-links:start/end -->` block alone and add no wikilinks.
2. **Reflections.** If `reflections_due`: in `note_file`, replace the line `_(pending model synthesis)_` under `## Reflections` with 1-3 sentences, each pointing at something concrete in that note. No platitudes.
3. **Monday goals.** If `monday_goals.due`: read `monday_goals.last_week_file`'s `## Week Review` (Next week priorities, then Recurring issues). In `monday_goals.file`, replace the goals placeholder line with at most 3 `- [ ]` goals (keep any other Goals line), and add the review's top win to `## Last Week Review`.
4. **Saturday review.** If `saturday_review.due`: read only the `## Repo Activity` and `## Tasks` sections of `saturday_review.notes` plus `saturday_review.file`, then append (never rewrite earlier sections) a `## Week Review — Saturday <date>` section with the five bold lines: Coverage (N of 5 daily notes, missing dates), Wins (merged PRs or pushed commits with repo and PR number), Recurring issues (items on 2+ days), Goals check, Next week priorities (1-3).

Skip any item that is false or absent. Never touch other files, logs or the handoff. Finish with one line listing the files you changed.
