---
up: "[[repos/ats-fill]]"
title: "ats-fill · CHROMEWEBSTORE"
source: https://github.com/nitsuah/ats-fill/blob/main/CHROMEWEBSTORE.md
kind: repo-doc
repo: ats-fill
---

# Chrome Web Store Listing — ats-fill

> Last Updated: 2026-10-15

Single source of truth for the Developer Dashboard: listing copy, permission justifications and privacy disclosures. Release mechanics (OAuth, the publish workflow, rollback) live in [docs/release/chrome-web-store.md](docs/release/chrome-web-store.md); listing images in [docs/CHROME_WEB_STORE_ASSETS.md](docs/CHROME_WEB_STORE_ASSETS.md).

## Store Listing

**Extension Name**
ats-fill

**Short Description**
Local-first ATS form-filling assistant. Save your profile once, review answers, and fill forms with your own Gemini key.

**Detailed Description**

ats-fill fills job applications from a profile you save once, and you review every field before you submit.

Fill Greenhouse, Lever, Ashby and LinkedIn Easy Apply forms in place, with partial support for Workday, iCIMS, Jobvite and other application forms. Fill also attaches your saved resume file to the form's resume upload (you can turn this off); like everything you fill in, it reaches the employer's application site only when you submit the form yourself. Preview every answer before it's used. Corrections you make on forms are remembered for next time, and you can review, edit or delete them.
Search 16 job boards from one panel, and save any result to your pipeline with one click.
Track every application on a board from draft to offer, import past applications from a spreadsheet, and see response analytics computed from your own history.
Practice for interviews with questions generated for the specific job.
Optional AI drafting and resume parsing use your own free Google Gemini key. Without a key, filling, tracking, search and analytics all still work.

How to use it: accept the privacy notice, upload your resume and check the parsed details, fill in your preferences, then open an application page and press Fill. Review the form and submit it yourself. ats-fill never submits for you.

Privacy: everything is stored only in your browser on your device. There is no account, no server and no analytics. Data leaves your device only when you start a job search, an AI request with your own key, or an optional profile import. Sensitive demographic fields are off by default and never sent to AI.

Source code and support: https://github.com/nitsuah/ats-fill

**Category**
Productivity

**Single Purpose**
Helps job seekers fill and track job applications from a locally stored profile.

**Primary Language**
English

## Graphics & Assets

Built and validated from each release tag by the release workflow (see [docs/CHROME_WEB_STORE_ASSETS.md](docs/CHROME_WEB_STORE_ASSETS.md)) and uploaded by hand, since the Store API has no listing-image endpoint.

| Asset | Dimensions | Status | Filename |
|-------|-----------|--------|----------|
| Store Icon | 128×128 PNG | ✅ Ready | release `ats-fill-vX.Y.Z-store-assets.zip` |
| Screenshots 1–5 | 1280×800 | ✅ Ready | release `ats-fill-vX.Y.Z-store-assets.zip` |
| Small Promo Tile | 440×280 | ✅ Ready | release `ats-fill-vX.Y.Z-store-assets.zip` |
| Marquee Promo Tile | 1400×560 | ✅ Ready | release `ats-fill-vX.Y.Z-store-assets.zip` |

## Permissions Justification

| Permission | Type | Justification |
|------------|------|---------------|
| `storage` | permissions | Saves the user's profile, resume, saved answers, application tracker and settings on their own device. Nothing is stored anywhere else. |
| `activeTab` | permissions | When the user opens ats-fill on a job page, lets it read that page's job details and fill the application form the user is looking at. |
| `scripting` | permissions | Re-attaches the form-filling script to the current job page when the user presses Fill on a tab opened before the extension was installed or updated, so the fill works without a page reload. |
| `identity` | permissions | Runs the optional "Import profile from LinkedIn/Google" sign-in that the user starts themselves, using their own app credentials. |
| `alarms` | permissions | When the user has turned on AI assistant access, checks about once a minute for tracker changes their AI assistant queued on this computer. Does nothing while that setting is off. |
| `nativeMessaging` | optional permissions | Requested only when the user turns on Settings → "AI assistant access". Lets ats-fill exchange messages with one local helper program the user installs, so an AI assistant on the same computer can add or update tracker entries (never delete). No data goes online, and the helper can't reach any other part of the browser. |
| `cookies` | optional permissions | Requested only if the user turns on LinkedIn job search, so searches can use the LinkedIn session they're already signed in to. Never requested otherwise. |
| `https://*/*`, `http://*/*` | optional host permissions | Requested one site at a time, only when the user adds a custom job feed (for example a state workforce board or a company careers feed), so ats-fill can read that one feed. |
| `https://generativelanguage.googleapis.com/*` | host_permissions | Sends the user's own AI requests (resume parsing, answer drafts, job summaries, interview questions) to Google Gemini with the user's own API key. |
| `https://remotive.com/*`, `https://www.arbeitnow.com/*`, `https://www.themuse.com/*`, `https://remoteok.com/*`, `https://jobicy.com/*`, `https://www.workingnomads.com/*`, `https://hn.algolia.com/*`, `https://weworkremotely.com/*`, `https://remote.co/*` | host_permissions | Job search across these public boards when the user runs a search. Only the search query is sent. |
| `https://api.adzuna.com/*`, `https://data.usajobs.gov/*`, `https://www.reed.co.uk/*`, `https://jooble.org/*` | host_permissions | Job search on these boards with the user's own API keys, entered in Settings, when the user runs a search. |
| `https://hackajob.com/*` | host_permissions | Job search on Hackajob when the user runs a search. |
| `https://api.linkedin.com/*`, `https://www.linkedin.com/*` | host_permissions | Optional LinkedIn profile import and LinkedIn job search that the user starts; also reads job details on LinkedIn job pages. |
| `https://oauth2.googleapis.com/*`, `https://www.googleapis.com/*` | host_permissions | Completes the optional Google profile import sign-in the user starts. |
| `https://*.greenhouse.io/*`, `https://*.ashbyhq.com/*`, `https://*.lever.co/*`, `https://*.workday.com/*`, `https://*.icims.com/*`, `https://*.jobvite.com/*`, `https://*.circle.com/*`, `https://*.phenompeople.com/*` | host_permissions | Applicant tracking systems where ats-fill detects the application form, reads the job details, and fills the fields the user reviews. |

**Content scripts:** run on the applicant-tracking hosts above and on pages whose path is `/careers`, `/jobs` or `/job/…`. They detect application forms, read job details (title, company, description) for the tracker, keep an in-progress draft of answers on the user's device, and fill fields only when the user presses Fill.

## Privacy & Data Use

### Data Collection

**Does the extension collect user data?** No data is collected by the developer. The extension stores the user's data on their own device, and sends parts of it only to services the user chooses, for requests the user starts.

| Data Type | Handled? | Transmitted Off-Device? | Purpose | Shared with Third Parties? |
|-----------|-----------|------------------------|---------|---------------------------|
| Personally identifiable info | Yes (profile, resume) | Only to Google Gemini when the user runs an AI action with their own key, and to the employer's application site (filled answers and the attached resume file) when the user submits that form themselves | Filling applications, drafting answers | Only that user-initiated request or submission |
| Health info | Disability field, opt-in only | No; never sent to AI | Answering a form question when the user enables it | No |
| Financial info | Desired pay range | Only within a user-run AI draft | Answering salary questions | Only that user-initiated request |
| Authentication info | User's own API keys | Only to the service each key belongs to | Job search, AI | No |
| Personal communications | No | — | — | — |
| Location | City or region from the profile | Only within a user-run AI draft | Answering location questions | Only that user-initiated request |
| Web history | No | — | — | — |
| User activity | Application tracker (jobs the user saved or applied to) | No | Pipeline and analytics on the user's device | No |
| Website content | Job description text from pages the user applies on | Only to Gemini when the user asks for a summary or drafts | Tracker entries, tailored drafts | Only that user-initiated request |

### Data Use Certification
- [x] Data is NOT sold to third parties
- [x] Data is NOT used for purposes unrelated to the extension's core functionality
- [x] Data is NOT used for creditworthiness or lending purposes

## Privacy Policy

**Privacy Policy URL**
https://github.com/nitsuah/ats-fill/blob/main/docs/PRIVACY.md

## Distribution

**Visibility**: Public
**Regions**: All regions

## Developer Info

**Publisher Name**
nitsuah

**Support URL**
https://github.com/nitsuah/ats-fill/issues

**Homepage URL**
https://nitsuah.github.io/ats-fill/

## Version History

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0.4 | 2026-10-16 | Attaches your saved resume to the application's resume upload (can be turned off in Profile; the file only reaches the employer when you press submit). Answers Ashby Yes/No buttons and type-ahead dropdowns (Greenhouse location, country, demographic questions); filled values now stick on React forms. Fill no longer reuses AI non-answers or untouched autofill. Tracker: "Remove duplicates" button, one row per application form embedded in a career page, and cleaner company names. Job search: Remotive results match the query. | Draft |
| 1.0.3 | 2026-10-14 | Optional "AI assistant access" setting: a local AI assistant can add and update tracker entries through a helper program on the user's computer (new `alarms` permission; optional `nativeMessaging`, requested only from that setting). Tracker entries capture the real company name on Ashby, Workday and generic apply pages instead of the page title; "My Application –" prefixes are dropped from job titles. | In review |
| 1.0.2 | 2026-10-05 | See [CHANGELOG](docs/CHANGELOG.md). | Published |

## Review Notes

### Known Issues / Limitations
- Automated publishing is blocked until the Store OAuth refresh token is rotated (tracked in [docs/TASKS.md](docs/TASKS.md)).
- Workday, iCIMS, Jobvite and generic forms fill partially; users are told to review every field.

### Rejection History
None recorded.
