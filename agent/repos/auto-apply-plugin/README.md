# 🤖 Apply Workspace — Local-First AI Job Application Chrome Extension

> Save your profile once. Land on any job page. Review tailored answers. Fill faster.
> No Docker. No server. No subscription. Review before submitting.

[![CI](https://github.com/nitsuah/auto-apply-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/auto-apply-plugin/actions/workflows/ci.yml)

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
4. Click the 🤖 icon → paste your [free Gemini API key](https://aistudio.google.com/app/apikey) and leave the model on **Auto**
5. Upload your resume (PDF, DOCX, or paste text)
6. Navigate to a job page → click the icon → **Fill Form**

---

## Project Structure

```
apply-workspace/
├── manifest.json          # Chrome MV3 manifest
├── popup/                 # Extension popup UI
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── screenshots/           # README gallery assets
├── content/               # Runs on job pages
│   └── content.js         # Form detection + injection
├── background/
│   └── service-worker.js  # API calls, storage management
├── lib/
│   ├── gemini.js          # Gemini API wrapper
│   ├── resume-parser.js   # Resume structuring
│   ├── jd-parser.js       # JD extraction
│   ├── form-filler.js     # DOM injection
│   └── tracker.js         # Application tracking
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

> Maintenance note: after any significant popup, tracker, or profile UI update, regenerate these images so the README stays current.
> Last refreshed: 2026-05-21 (manual QA closeout)

### Main dashboard

![Apply Workspace main dashboard](screenshots/main-dashboard.png)

### Tracker workspace

![Apply Workspace tracker workspace](screenshots/tracker-workspace.png)

### Profile + Memory

![Apply Workspace profile and memory](screenshots/profile-memory.png)

---

## Job Search

Click **🔍 Search** in the header to open the job search panel. Results are pulled from up to **14 sources** and deduplicated automatically.

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

### Session-based sources (active when you're signed in)

| Source | How it works |
|--------|-------------|
| LinkedIn | Uses your active LinkedIn tab session via the Voyager API — no separate key needed; shows ⚡ chip when a LinkedIn tab is open |

### Optional keyed sources (add credentials in AI settings)

| Source | Coverage | Key source |
|--------|----------|------------|
| Adzuna | Millions of listings across 16+ countries | [developer.adzuna.com](https://developer.adzuna.com/signup) |
| USAJOBS | All US federal government positions | [developer.usajobs.gov](https://developer.usajobs.gov/apirequest/) |
| Reed | Major UK job board | [reed.co.uk/developers](https://www.reed.co.uk/developers/jobseeker) |
| Jooble | Global aggregator (190+ countries) | [jooble.org/api/about](https://jooble.org/api/about) |

### Filters

- **Sources** — toggle individual boards on/off via chip buttons; locked chips (🔒) open the AI settings panel
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
- External network calls happen **only** for actions you trigger (AI help with your Gemini key; optional job-search sources / LinkedIn profile import with your own credentials).
- No servers, no accounts, no telemetry.

See **[PRIVACY.md](PRIVACY.md)** for the full Terms of Use (EULA), Privacy Policy, Security posture, and your GDPR/CCPA data rights — the same content shown in the app's **Help & privacy** panel.

---

## Development

All checks run via Docker — no local Node.js required.

```bash
# Unit tests (63 tests, no browser needed)
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

## License

MIT — built because filling out the same form 47 times is beneath EVERYONE. 🤙
## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

## Repository Index

### Root Files
- [[repos/auto-apply-plugin/CHANGELOG.md|CHANGELOG.md]]
- [[repos/auto-apply-plugin/FEATURES.md|FEATURES.md]]
- [[repos/auto-apply-plugin/METRICS.md|METRICS.md]]
- [[repos/auto-apply-plugin/ROADMAP.md|ROADMAP.md]]
- [[repos/auto-apply-plugin/TASKS.md|TASKS.md]]

### Documentation
- [[repos/auto-apply-plugin/docs/PRIVACY.md|PRIVACY.md]]