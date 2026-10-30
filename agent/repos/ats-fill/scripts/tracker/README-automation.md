---
up: "[[repos/ats-fill]]"
title: "ats-fill · README-automation"
source: https://github.com/nitsuah/ats-fill/blob/main/scripts/tracker/README-automation.md
kind: repo-doc
repo: ats-fill
---

# Zero-model tracker automation

Two Node 22 scripts (no npm install, no AI calls) replace the model-driven scheduled tasks:

- `inbox-sync.mjs`: Gmail REST search, `cli sync-email --apply`, `cli summary`, at most 8 lines. Prints `ACTION: open that thread` when an interview or offer shows up.
- `weekly-review.mjs`: read-only review (at most 15 lines) from `cli summary` and `cli list --status submitted`; keeps last week's numbers in `%USERPROFILE%\.ats-fill\weekly-review.json`.

## One-time Google OAuth setup (inbox-sync only)

1. In Google Cloud Console create a project, enable the **Gmail API**, and configure the OAuth consent screen. Set it to **In production**; a "Testing" consent screen expires refresh tokens after 7 days.
2. Credentials, Create credentials, **OAuth client ID**, type **Desktop app** (or Web with `https://developers.google.com/oauthplayground` as a redirect). Note the client ID and secret.
3. Run the consent once with scope `https://www.googleapis.com/auth/gmail.readonly` only. Easiest: OAuth Playground, gear icon, tick "Use your own OAuth credentials", authorize that single scope, then "Exchange authorization code for tokens" and copy the **refresh token**.
4. Store the three values outside the repo, either as user environment variables `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, or in `%USERPROFILE%\.ats-fill\gmail-oauth.json`:
   `{"clientId": "...", "clientSecret": "...", "refreshToken": "..."}`
5. Test: `node scripts\tracker\inbox-sync.mjs`. Without credentials it exits with code 2 and a message; a revoked token exits 1 with Google's reason.

The script only reads mail (`gmail.readonly`); it never sends, labels or deletes.

## Task Scheduler examples

Adjust the repo path. Daily inbox sync at 07:30:

    schtasks /Create /TN "ats-fill inbox sync" /SC DAILY /ST 07:30 /TR "cmd /c node C:\Users\you\code\ats-fill\scripts\tracker\inbox-sync.mjs >> %USERPROFILE%\.ats-fill\inbox-sync.log 2>&1"

Weekly review, Mondays at 08:00:

    schtasks /Create /TN "ats-fill weekly review" /SC WEEKLY /D MON /ST 08:00 /TR "cmd /c node C:\Users\you\code\ats-fill\scripts\tracker\weekly-review.mjs >> %USERPROFILE%\.ats-fill\weekly-review.log 2>&1"

Both read the tracker through `cli.mjs`, which uses `~/.ats-fill/config.json`. Writes need the helper from `cli.mjs setup`.
