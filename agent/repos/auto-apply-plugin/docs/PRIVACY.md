# Apply Workspace — Terms, Privacy & Security

**Document version:** 1.1
**Last updated:** September 2, 2026
**Applies to:** the Apply Workspace browser extension ("the extension") in this repository.

This is the canonical, public statement of the extension's Terms of Use (EULA),
Privacy Policy, Security posture, and your data rights. The same content is
surfaced in-app under **Help & privacy**. If the two ever differ, this file is
authoritative for the corresponding release.

---

## Summary (TL;DR)

- **Local-first.** Your data lives in your browser's local extension storage on
  your device. There is no Apply Workspace account, server, or backend.
- **We never receive your data.** We have no way to see, collect, store, or sell
  it — there is nothing to send to us.
- **Review-first.** The extension drafts and fills fields. It never submits an
  application for you.
- **Bring your own keys (BYOK).** Optional AI and extra job sources use *your*
  own API keys/credentials, stored locally, used only for requests you trigger.
- **No tracking.** No analytics, advertising, telemetry, or third-party tracking
  of any kind.

---

## Terms of Use (EULA)

By accepting consent in the extension, you agree to the following:

1. **Review before you submit.** The extension only drafts and fills form
   fields. It never submits an application on your behalf — you review every
   field and click submit yourself.
2. **You are responsible for accuracy.** Auto-filled and AI-drafted answers are
   suggestions. You are solely responsible for the truthfulness and content of
   anything you submit to an employer.
3. **Bring your own key (BYOK).** Optional AI features run through your own
   Google Gemini API key; optional extra job sources (Adzuna, USAJOBS, Reed,
   Jooble, and any custom RSS source you add) and the optional LinkedIn/Google
   profile import run through your own credentials. Your use of those
   third-party services is governed by their terms, not ours.
4. **No warranty.** The extension is provided "as is", without warranty of any
   kind, express or implied. To the maximum extent permitted by law, the authors
   are not liable for any damages, lost opportunities, or rejected applications
   arising from its use.
5. **Acceptable use.** Do not use the extension to submit fraudulent or
   misleading applications, or to violate the terms of any job board or ATS.
6. **Open source.** The extension is distributed under the license in this
   repository ([`LICENSE`](LICENSE)); that license governs the software itself.

---

## Privacy Policy

### We run no servers
There is no Apply Workspace account and no backend. Your data is never
transmitted to us, and we have no infrastructure capable of receiving it.

### What is stored, and where
The following are stored **only** in your browser's local extension storage
(`chrome.storage.local`) on the current device/browser profile:

- Profile details (name, contact, links, work history fields)
- Resume preview / saved local copy
- Saved answer defaults and learned "memory" (and the ignore list)
- The application tracker (your pipeline)
- Settings, including your Gemini API key and any optional source credentials
- Recorded privacy consent and its timestamp

Nothing syncs to the cloud. Uninstalling the extension or using **Delete all
local data** removes it.

### What leaves your device
Data leaves your device **only** when *you* trigger an optional network action:

| Action | Destination | Sent | Auth |
| --- | --- | --- | --- |
| Resume parsing / answer drafting / summarize | Google Gemini API | the relevant resume/JD/answer text | your Gemini key |
| Job search | Nine keyless boards (Remotive, Arbeitnow, The Muse, Remote OK, Jobicy, Working Nomads, HN Who's Hiring, We Work Remotely, remote.co); Indeed and Hackajob (no key); Adzuna, USAJOBS, Reed, Jooble (your keys); any custom RSS source you add | your search query | your keys where applicable |
| LinkedIn session job search (optional) | LinkedIn Voyager API | your search query, via your active browser session | your existing LinkedIn sign-in |
| LinkedIn / Google profile import (optional) | LinkedIn or Google OAuth/OIDC | OAuth handshake | your own app credentials + your sign-in |
| Custom job source fetch (optional) | whatever URL you add | your search query (appended as a param when the feed doesn't already encode one) | none — a one-time browser permission prompt scoped to that site |

Without a Gemini key, autofill still works fully using deterministic, on-device
logic and sends nothing anywhere. Each request sends only what is needed to
fulfill that request.

### Sensitive / demographic data
Race, gender, veteran, and disability fields are **opt-in**, stored locally
only, and are **never** included in AI requests.

### Third parties
The only third parties that can receive your data are the services listed in the
table above, and only for requests you explicitly initiate with your own
credentials. There is **no analytics, advertising, tracking, or telemetry** of
any kind.

---

## Security

- **Data at rest:** stored in the browser's per-profile extension storage,
  protected by the browser's and operating system's user-account isolation.
- **Data in transit:** all third-party calls are over HTTPS. Built-in job
  boards and integrations use the providers' official API endpoints; a
  custom RSS source is whatever URL you add, and the extension requires it
  to be `https://` — non-HTTPS custom source URLs are rejected before any
  request is made, since the search query is sent as a plaintext GET param.
- **Credentials:** API keys and OAuth client secrets are stored locally and used
  only to authenticate the requests you trigger. They are never sent to us.
- **Permissions:** the extension requests only the host permissions needed to
  read job pages, fill forms, and reach the optional APIs you enable. Adding a
  custom job source asks for a one-time, one-site permission (via the
  browser's own permission prompt) scoped to just that source's domain,
  instead of requesting broad access to all sites up front.
- **No remote code:** the extension does not load or execute remote code.
- **Reporting:** see [`SECURITY.md`](SECURITY.md) for how to report a
  vulnerability.

---

## Your rights (GDPR & CCPA)

Because all data lives locally on your device and we never receive it, you are
the sole controller of your information and can exercise every right directly:

- **Access & portability** — Export your tracker to CSV from the Pipeline
  screen; your profile and memory are visible and editable in the Profile
  screen.
- **Rectification** — Edit any saved field at any time in Profile.
- **Erasure ("right to be forgotten")** — Use **Delete all local data** to wipe
  everything instantly. No request to us is needed because we hold nothing.
- **Withdraw consent** — Re-open privacy settings to review or revoke; deleting
  local data also clears your recorded consent.
- **No sale of data** — We never receive your data, so there is nothing to sell;
  we do not sell personal information.

---

## Data controls — what each action removes

**🧹 Clear temp cache** — removes only short-lived working data: cached page
drafts (in-progress form values), the last generated answer set, the last fill
report, and the "recently filled" pointer. Your profile, resume, saved memory,
tracker, settings, and keys are **kept**.

**🗑 Delete all local data** — wipes **everything** the extension stores on your
device: profile and resume, saved answer defaults & ignore list, the entire
application tracker, all settings (including your Gemini API key and recorded
consent), plus everything the temp cache covers. This cannot be undone.

---

## Changes to this document

Material changes will bump the **Document version** and **Last updated** date
above, and update the in-app Help panel to match. Continued use after a change
constitutes acceptance of the revised terms.

## Contact

This is an open-source, local-first project. Questions and reports go through the
repository's issue tracker / the process described in [`SECURITY.md`](SECURITY.md).
