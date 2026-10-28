---
up: "[[repos/ats-fill]]"
title: "ats-fill · automation"
source: https://github.com/nitsuah/ats-fill/blob/main/skills/ats-fill-job-search/references/automation.md
kind: repo-doc
repo: ats-fill
---

# Automating the tracker (CLI, inbox sync, routines)

ats-fill has no server. Its tracker lives in the extension's `chrome.storage.local`, which Chrome keeps as a LevelDB folder on disk:

```
<Chrome User Data>/<Profile>/Local Extension Settings/<extension id>/
```

The Web Store build's ID is `amofaeopfmaicbiijgjaojenedkkadmn`. An unpacked dev build has its own ID (shown on `chrome://extensions`) **and its own, separate store**, so point the CLI at whichever build the candidate actually tracks jobs in.

## The CLI

Needs Node 22+. Run it with `npx -y github:nitsuah/ats-fill <command>` (no checkout needed), or `node scripts/tracker/cli.mjs <command>` from a checkout. Below, `…` stands for either.

| Command | Does |
| --- | --- |
| `… setup` | Once per computer: installs the small helper that lets ats-fill accept tracker changes, then reports whether ats-fill is connected. |
| `… summary` | Counts by stage, response rate, apps with no reply after 14+ days, drafts without a verdict. About 5 lines. |
| `… list [--status interview] [--json]` | One line per application. |
| `… set <company or id prefix> <status>` | Move one application (drafted, filled, submitted, interview, offer, rejected, retired). |
| `… add --company C --title T [--url U] [--status s]` | Track a new application. |
| `… gmail-query` | The Gmail search covering everything since the last sync. |
| `… triage <emails.json>` | Classify emails only (applied, interview, rejected, offer, noise). |
| `… sync-email <emails.json> [--apply]` | Plan tracker changes from emails; `--apply` writes them. Status only ever moves forward, and processed emails are remembered in `~/.ats-fill/email-sync.json`. |
| `… export [--out file.json]` | Back up the tracker. |

**Reads** come straight from disk, so Chrome needs no setup and can stay closed.

**Writes** go through ats-fill itself once two one-time steps are done: run `setup`, and the candidate turns on **Settings → AI assistant access** in ats-fill. After that:
- ats-fill checks in with the helper about once a minute and applies queued changes through its own handlers.
- It accepts add, update and import only, never delete.
- It uses Chrome native messaging, so no port is opened and nothing else in the browser is exposed.

If the switch is off, writes become a CSV (`~/.ats-fill/import-<date>.csv`) for **Tracker → Import CSV**, which matches on URL and only moves status forward.

Never ask the candidate to turn on Chrome remote debugging: it exposes every logged-in site. `--live` exists only for development.

Save per-machine defaults in `~/.ats-fill/config.json`, e.g. `{"extensionId": "<unpacked build id>", "profile": "Profile 1", "staleDays": 14}`. The environment variables `ATS_FILL_EXTENSION_ID`, `ATS_FILL_PROFILE` and `ATS_FILL_STALE_DAYS` override it. Run `setup` again after setting `extensionId`, so the helper also accepts that build.

## Browser and environment rules (for agents)

- **Never enable Chrome remote debugging** on the candidate's profile, and never pass `--live` or set `ATS_FILL_CDP_URL` for them. Remote debugging exposes every logged-in site. The CLI's disk reads and bridge writes need no browser access.
- **Tracker writes only through the CLI.** Don't enqueue bridge messages by hand. The bridge accepts only `LOG_APPLICATION`, `UPDATE_APPLICATION`, `IMPORT_APPLICATIONS_CSV`, `SEARCH_JOBS`, `OPEN_APPLICATION_TAB` and `FILL_APPLICATION_TAB` (see `BRIDGE_ALLOWED_TYPES` in `background/native-bridge.js`). `OPEN_APPLICATION_TAB` only opens an http(s) tab. `FILL_APPLICATION_TAB` fills a tab that is already open on that exact URL, using the popup's fill. It never submits; the candidate reviews and submits. Any other type is refused, and new types need a code change and review.
- **Delete is never automated.** Use the popup, or ask the candidate.
- **Reads work anywhere the candidate's Chrome data is on disk** (Windows: `%LOCALAPPDATA%\Google\Chrome\User Data`). Cloud routines and sandboxes can't read it, so run tracker routines locally.
- **Bridge writes need a fresh check-in** (under 3 minutes old in `~/.ats-fill/bridge/heartbeat.json`). When it's stale, `add`/`set` fall back to a CSV. Tell the candidate to import it, and don't retry in a loop.
- **`setup` writes the Node path it runs under** into the helper launcher. After changing or uninstalling Node, run `setup` again from the Node you want to keep.
- **Don't scrape LinkedIn or other sites for hiring managers.** Ask the candidate for names they find themselves.

## Inbox → tracker loop

Classification is deterministic code, not the model, so a sync costs roughly the size of the email snippets:

1. `… gmail-query` → copy the query.
2. Search Gmail with it (Gmail connector `search_threads`, default minimal view, `pageSize` 50). Save the result as-is to a JSON file; `{id, date, sender, subject, snippet}` per message is enough.
3. `… sync-email <file> --apply` and report its last lines. With AI assistant access on, changes land in the tracker directly; otherwise pass on the CSV import line.

Read individual threads in full only when the output flags something to act on (an interview request needing a reply, an offer). Don't send, label or archive mail unless the candidate asks.

Known limits: truncated snippets sometimes drop the role title, and a company whose emails never spell out its full name may be tracked under its mail domain, so tell the candidate to merge it.

## Routines

Pick the cheapest tool that does the job:

| Cadence | What | Cost |
| --- | --- | --- |
| Daily, early morning | Inbox → tracker loop above, then `summary`. Mention only changes, new interviews and offers. | ~2–5k tokens |
| Weekly (e.g. Monday) | `summary`; for each stale app, suggest one follow-up or retire; for drafts without a verdict, ask for a verdict; compare the response rate with last week. | ~3k tokens |
| On demand | Any CLI command directly; no agent needed. | 0 |
| Before an interview | `list --status interview`, then the prep sheet in [interviews.md](interviews.md). | varies |

Run daily and weekly routines as **local** scheduled tasks (the Claude desktop app's scheduled tasks, or a plain OS scheduler calling a script). They need this machine's Chrome profile, which cloud routines can't reach. A pure-script routine (no model at all) can run `summary` on a schedule and only wake an agent when the output changes.
