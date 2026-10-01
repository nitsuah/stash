---
up: "[[obsidian-vault-guide]]"
kind: routine-backup
---

# Routine backups

Public-safe copies of the routine definitions that live **outside** any repo: the local scheduled tasks in `~/.claude/scheduled-tasks/` and the cloud routines at claude.ai/code/routines. If either is lost (machine rebuild, an accidental delete in the routines UI), restore from here. Most routines are thin wrappers that point at a canonical spec in `agent/prompts/`. That spec is the real behaviour, and it's already versioned.

Personal tone and health context is redacted from these copies. The live prompts keep it. Don't paste a backup back over a live prompt without re-adding that context.

## Local (scheduled tasks on this machine)

Exported by `python agent/scripts/export-routines.py`. Re-run it after editing a task; `--check` exits 1 if a backup is stale. One-shot `catchup-*` tasks and the retired `hub-checkin` are not backed up.

| Routine | Spec it runs |
|---|---|
| [[routine-daily-repo-sync]] | [[prompts/DAILY\|DAILY]] |
| [[routine-week-sotu]] | [[prompts/SOTU\|SOTU]] |
| [[routine-week-fin-sum]] | the fire repo's private check-in prompt (read-only, never commits) |
| [[routine-ops-catchup]] | [[prompts/CATCHUP\|CATCHUP]] |
| [[routine-monthly-tire-kick]] | [[prompts/TIRE\|TIRE]] |
| [[routine-monthly-pmo-audit]] | [[prompts/PMO\|PMO]] |
| [[routine-monthly-usage-report]] | [[prompts/USAGE\|USAGE]] |
| [[routine-monthly-self-improvement]] | [[prompts/RSI\|RSI]] |

## Cloud (claude.ai routines)

Snapshots taken by hand on 2026-09-30, because the prompts can only be read through `RemoteTrigger get`. To refresh one, `get` the trigger ID shown in its note, then replace the prompt block. Keep the redactions and leave out `environment_id`. Disabled routines aren't backed up; their IDs are in the memory note on cloud routine IDs.

| Routine | Schedule (UTC) | Publishes |
|---|---|---|
| [[routine-cloud-daily-brief]] | weekdays 13:00 | `reports/cloud/daily-brief/` (counts only) |
| [[routine-cloud-week-obn-import]] | Wed 10:00 | `reports/cloud/obn-import/` |
| [[routine-cloud-week-eng-mini]] | Wed 18:00 | `reports/eng-mini-*` |
| [[routine-cloud-week-vuln]] | Thu 15:00 | `reports/cloud/week-vuln/` |
| [[routine-cloud-week-eng-loc]] | Thu 17:00 | `reports/eng-loc-*` |
