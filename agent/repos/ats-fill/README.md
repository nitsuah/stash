# ats-fill — Local-First AI Job Application Chrome Extension

> 🧭 **auto-apply-plugin** · [Features](./docs/FEATURES.md) · [Roadmap](./docs/ROADMAP.md) · [Tasks](./docs/TASKS.md) · [Changelog](./docs/CHANGELOG.md) · [Metrics](./docs/METRICS.md) <!-- nav -->
>
> Save your profile once. Land on any job page. Review tailored answers. Fill faster.
> No Docker. No server. No subscription. Review before submitting.

[![CI](https://github.com/nitsuah/ats-fill/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/ats-fill/actions/workflows/ci.yml)

---

## The Problem

Job applications are the same 20 questions on 47 different forms.
Nobody has time for that. Nobody should have to.

---

## The Solution

A Chrome extension that:
1. **Stores your profile locally** once (resume, defaults, safe memory)
2. **Detects job application forms** automatically
3. **Reads the JD** from the page or pasted text
4. **Generates tailored answers** per role using your own Gemini API key
5. **Keeps you in review** before filling the form in place

**Local-first. Review-first. Private. Fast.**

---

## Quick Start (< 5 minutes)

1. Clone this repo (or download as ZIP)
2. Open `chrome://extensions` → enable **Developer mode**
3. Click **Load unpacked** → select the repo folder
4. Click the extension icon → paste your [free Gemini API key](https://aistudio.google.com/app/apikey) and leave the model on **Auto**
5. Upload your resume (PDF, DOCX, or paste text)
6. Navigate to a job page → click the icon → **Fill Form**

---

## Project Structure

```
ats-fill/
├── manifest.json          # Chrome MV3 manifest
├── popup/                 # Extension popup UI
│   ├── popup.html
│   ├── popup.js
│   ├── popup.css
│   ├── ai/                # AI settings panel
│   ├── ats/               # ATS-specific popup helpers
│   ├── forms/             # Answer preview, memory, form handling
│   ├── search/            # Job search panel
│   ├── tracker/           # Tracker state, UI, handlers, CSV, metadata
│   └── ux/                # Navigation, profile, consent, a11y, interview prep
├── screenshots/           # README gallery assets
├── content/               # Content scripts — run on job pages
│   ├── content.js         # Entry point: orchestration & messaging
│   ├── ats-detector.js    # ATS platform detection (direct + embedded)
│   ├── form-filler.js     # DOM injection + field mapping
│   ├── job-processor.js   # JD extraction from page
│   ├── message-listener.js# Message handler wiring
│   └── utils.js           # Shared content-script helpers
├── background/
│   ├── service-worker.js  # SW entry point
│   ├── message-router.js  # Dispatch table for SW messages
│   └── modules/handlers/  # Per-domain handler modules (answers, jobs, resume, oauth, …)
├── lib/
│   ├── gemini.js          # Gemini API wrapper + model auto-select
│   ├── resume-parser.js   # Resume structuring
│   ├── jd-parser.js       # JD extraction helpers
│   ├── form-filler.js     # Shared form-fill logic (lib copy)
│   ├── job-search.js      # Multi-source job search registry
│   ├── oauth.js           # LinkedIn + Google OAuth / OIDC flows
│   ├── tracker.js         # Application tracking storage
│   └── utils.js           # Shared lib utilities
├── data/
│   └── field-map.json     # Common field name → answer key mappings
└── icons/                 # Extension icons
```

---

## Supported ATS Platforms

| Platform | Detection | Form Fill | Status |
|----------|-----------|-----------|--------|
| Greenhouse | ✅ | ✅ | Phase 1 |
| Ashby | ✅ | ✅ | Phase 1 |
| Lever | ✅ | ✅ | Phase 1 |
| LinkedIn Easy Apply | ✅ | ✅ | Phase 1 |
| Jobvite | ✅ | 🔄 | Phase 2 |
| Circle Careers / Phenom | ✅ | 🔄 | Phase 2 |
| Workday | ✅ | 🔄 | Phase 2 |
| iCIMS | ✅ | 🔄 | Phase 2 |
| Generic (any form) | ✅ | 🔄 | Phase 2 |

---

## Screenshots

> The gallery is generated from deterministic fictional Playwright fixture data; never use personal resume, API-key, or application data in committed screenshots.
> The UI screenshot workflow refreshes these images and the version/date metadata automatically after UI changes.
> Last refreshed: 2026-09-25 · UI snapshot: v1.0.2 (nav/hamburger overhaul, collapsible Settings + Pipeline columns, Help collapsed-by-default, Interview Prep job-readiness bar)

### Main dashboard

![ats-fill main dashboard](screenshots/main-dashboard.png)

### Tracker workspace (Pipeline)

![ats-fill tracker workspace](screenshots/tracker-workspace.png)

### Profile + Memory

![ats-fill profile and memory](screenshots/profile-memory.png)

### Job Search

![ats-fill job search panel](screenshots/job-search.png)

### Settings

![ats-fill settings panel](screenshots/ai-settings.png)

### Help & Privacy

![ats-fill help and privacy panel](screenshots/help-privacy.png)

### Interview Prep

![ats-fill interview prep](screenshots/interview-prep.png)

---

## Job Search

Click **🔍 Search** in the header to open the job search panel. Results are pulled from up to **16 built-in sources** (plus any custom RSS sources you add) and deduplicated automatically.

### Keyless sources (always on)

| Source | Coverage |
|--------|----------|
| Remotive | Remote tech / knowledge-worker roles worldwide |
| Arbeitnow | Global remote & hybrid listings |
| The Muse | US-centric roles across many industries |
| Remote OK | High-volume remote tech board |
| Jobicy | Remote jobs with structured salary data |
| Working Nomads | Curated remote listings |
| HN: Who's Hiring | Monthly HackerNews hiring thread (tech-heavy, often salary posted) |
| We Work Remotely | Large curated remote jobs board |
| remote.co | Vetted remote positions across categories |

### Always-available sources (no key or session needed)

| Source | Coverage |
|--------|----------|
| Indeed | RSS-based search across Indeed's listings |
| Hackajob | Tech-focused UK/EU roles, scraped from the public sitemap + job-posting metadata |

### Session-based sources (active when you're signed in)

| Source | How it works |
|--------|-------------|
| LinkedIn | Uses your active LinkedIn tab session via the Voyager API — no separate key needed; shows ⚡ chip when a LinkedIn tab is open |

### Optional keyed sources (add credentials in Settings)

| Source | Coverage | Key source |
|--------|----------|------------|
| Adzuna | Millions of listings across 16+ countries | [developer.adzuna.com](https://developer.adzuna.com/signup) |
| USAJOBS | All US federal government positions | [developer.usajobs.gov](https://developer.usajobs.gov/apirequest/) |
| Reed | Major UK job board | [reed.co.uk/developers](https://www.reed.co.uk/developers/jobseeker) |
| Jooble | Global aggregator (190+ countries) | [jooble.org/api/about](https://jooble.org/api/about) |

### Custom job sources (bring your own RSS feed)

Add any RSS-based job board from **Settings → Custom job sources** — a state workforce board (e.g. [JOBS4TN.gov](https://www.jobs4tn.gov/)), an internal careers feed, or any niche board with an RSS endpoint. Your search terms are appended as a `?q=` param when the feed doesn't already encode a query. The extension asks for one-time permission to read that specific site rather than requesting broad site access up front.

### Filters

- **Sources** — toggle individual boards on/off via chip buttons; locked chips (🔒) open the Settings panel
- **Pay** — annual or hourly dual-slider; optional toggle to **hide jobs without a published salary**
- **Remote / Type / Location** — filter by work mode, employment type, and region

---

## CSV Import for Tracker History

Use **Tracker → Import CSV** to bring in past applications from another sheet or export.
Accepted headers are case-insensitive and can include:

- `Company`
- `Role Title` / `Title`
- `Status`
- `Date`
- `Employment Type`
- `Remote`
- `Location`
- `Salary Range`
- `Pay Min`
- `Pay Max`
- `Scorecard`
- `Verdict`
- `URL`
- `Notes`

Example header row:

```csv
Company,Role Title,Status,Date,Employment Type,Remote,Location,Pay Min,Pay Max,Scorecard,Verdict,URL,Notes
```

---

## Tech Stack

- **Chrome MV3** extension
- **Auto-selected Gemini 2.5 models** via REST API (`models.list` + fallback strategy)
- Data is stored locally in `chrome.storage.local`; external requests only go to the Gemini API using your key.  

- Zero dependencies, zero build step — just load and use

---

## Storage Schema

```json
{
  "resume": {
    "structured": { "name": "", "email": "", "skills": [], "experience": [], ... },
    "excerpt": "plain-text excerpt/preview (≤1000 chars, including uploaded file/data-URL resumes)"
  },
  "settings": {
    "gemini_api_key": "...",
    "preferred_salary_min": 150000,
    "preferred_salary_max": 325000,
    "work_authorization": "US Citizen",
    "preferred_remote": true
  },
  "applications": [
    {
      "id": "uuid",
      "company": "Anthropic",
      "title": "IT Systems Engineer",
      "url": "...",
      "status": "submitted",
      "date": "2026-04-04",
      "pay_min": 150000,
      "pay_max": 230000,
      "jd_snippet": "...",
      "answers_generated": true
    }
  ]
}
```

---

## Privacy

- Your resume and API key are stored **only** in your local browser storage.
- External network calls happen **only** for actions you trigger (AI help with your Gemini key; optional job-search sources including any custom RSS source you add / LinkedIn or Google profile import with your own OAuth credentials).
- No servers, no accounts, no telemetry.

See **[docs/PRIVACY.md](docs/PRIVACY.md)** for the full Terms of Use (EULA), Privacy Policy, Security posture, and your GDPR/CCPA data rights — the same content shown in the app's **Help & privacy** panel.

---

## Development

All checks run via Docker — no local Node.js required.

```bash
# Unit tests (106 unit tests + 14 Playwright e2e, no browser needed for unit)
docker compose -f config/docker-compose.yml run --rm test

# Lint
docker compose -f config/docker-compose.yml run --rm lint

# E2E (Playwright, requires headed or CI browser)
docker compose -f config/docker-compose.yml run --rm e2e

# Coverage
docker compose -f config/docker-compose.yml run --rm coverage
```

**Pre-commit hooks** (lint on commit, tests on push):
```bash
pip install pre-commit && pre-commit install && pre-commit install --hook-type pre-push
```

---

<!-- docs-index:start -->

## Docs Index

Every doc at the repo root and under `docs/` (the files mirrored into the Obsidian vault), so none of them is orphaned.

- [Changelog](./docs/CHANGELOG.md) — `docs/CHANGELOG.md`
- [Features](./docs/FEATURES.md) — `docs/FEATURES.md`
- [Metrics](./docs/METRICS.md) — `docs/METRICS.md`
- [ats-fill — Terms, Privacy & Security](./docs/PRIVACY.md) — `docs/PRIVACY.md`
- [Roadmap](./docs/ROADMAP.md) — `docs/ROADMAP.md`
- [Tasks](./docs/TASKS.md) — `docs/TASKS.md`

**`docs/release/`**

- [Chrome Web Store release setup](./docs/release/chrome-web-store.md) — `docs/release/chrome-web-store.md`
- [Release process](./docs/release/release-process.md) — `docs/release/release-process.md`

<!-- docs-index:end -->

## License

MIT — built because filling out the same form 47 times is beneath EVERYONE. 🤙
## Automation & CI

The repository uses GitHub Actions to run the blocking test, lint, coverage, security, and Playwright checks. The same CI pipeline also generates the deterministic screenshot gallery and validates the resulting assets before publishing a documentation PR when the UI snapshot changes.

Screenshot publication is deliberately **rerun-safe** and uses a **single rolling PR**. Every refresh rebuilds the fixed `automation/ui-screenshot-gallery` branch from `main` and updates its open PR instead of opening a new one. Commits that merge a gallery refresh are skipped, so publication can't loop. When `main` already matches the captured gallery, any open refresh PR is closed. Gallery screenshots are generated from fictional fixture data and never contain personal resume, API-key, or application data.

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
