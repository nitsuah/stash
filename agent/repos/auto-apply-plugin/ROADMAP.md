---
updated: 2026-06-08
---

# Roadmap

## 2026 Q1 ✅

> Completed. See FEATURES.md for shipped capabilities.

## 2026 Q2 (In Progress)

- [/] Turn the tracker into a real job-workspace view with stored JD metadata, location, employment type, structured pay bands, verdict controls, scorecard fields, search/filter controls, and a wider lower-scroll popup layout.
- [/] Start a lightweight `apply-bot` rebrand pass across popup copy, icons, and docs without over-scoping the MVP.
- [ ] Add picker-style job detail capture from the current page or pasted JD text and keep extending it into a stronger import workflow.

## 2026 Q3 (In Progress)

- [/] Expand job search to additional sources — on-ATS-page parsing depth, tracker-side indexing, and OAuth job source once a partner API is available.

## 2026 Q4 (Exploratory)

- [ ] Begin to implement job search results by scraping and searching multiple job pages, starting with LinkedIn and Indeed, etc. and then expanding to a more general multi-site search and alerting capability.
- [ ] Explore optional identity-provider imports (Google, ID.me, etc.) for bootstrapping profile data without breaking local-first/privacy guarantees. But also for email/etc. auto-fill in the tracker and potential future job-board integrations.
- [ ] Revisit deeper job-fit scoring, verdict assistance, and richer tracker analytics after the storage and review foundations are stable.
- [ ] Run a lightweight `axe` / accessibility audit on popup navigation, labels, contrast, and keyboard flow as the workspace UI settles.
- [ ] **Interview prep mode** — from a saved tracker card, generate a Gemini-backed set of likely behavioral and technical questions tailored to the JD and the user's stored profile, with suggested answer structures pre-filled from memory. Keeps interview prep local-first and zero-upload.
- [ ] **Application analytics panel** — surface aggregate stats from tracker data: response-rate by source, salary-range effectiveness, and time-to-first-response distribution; gives signal on which boards and bid ranges are yielding callbacks without any external telemetry.

## Notes

- Local-first and consent-first remain the product guardrails.
- Scrape from the page or JD before asking the user to type.
- Detailed execution work stays in `TASKS.md`.
