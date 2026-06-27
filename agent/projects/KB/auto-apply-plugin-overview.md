---
name: auto-apply-plugin-overview
description: Central synthesis document for the Auto-Apply Plugin (Apply Workspace).
metadata:
  type: project
---

# Auto-Apply Plugin (Apply Workspace)

The Auto-Apply Plugin is a local-first Chrome extension designed to streamline job applications by automating repetitive form filling and job search aggregation, while keeping data strictly private on the user's local machine.

## Core Pillars

- **Privacy-First**: No servers, accounts, or telemetry. Resumes, API keys, and application history are stored locally in `chrome.storage.local`.
- **Review-First**: AI generates tailored answers based on user profile and job description, but the tool enforces human review *before* injecting data into the form.
- **Job Aggregation**: Searches across 14+ job boards, performs automatic deduplication, and offers advanced filtering (salary, remote status, etc.).

## Key Capabilities

- **Form Automation**: Detects job application forms (Greenhouse, Ashby, Lever, LinkedIn, etc.) and injects profile-tailored data.
- **Job Search**: Integrated search panel supporting multiple job boards, with support for session-based (LinkedIn) and keyed (Adzuna, USAJOBS) data sources.
- **Tracker**: Built-in application tracker with CSV import/export capabilities.

## Related Resources

- **Source Code**: [[repos/auto-apply-plugin/README.md|Auto-Apply Plugin README]]
- **Privacy Policy**: [[repos/auto-apply-plugin/docs/PRIVACY.md|Privacy & Terms]]
- **Roadmap**: [[repos/auto-apply-plugin/ROADMAP.md|Roadmap]]
