# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Custom user-configured RSS job sources (state workforce boards, internal careers feeds, etc.), merged into the existing job-source registry with per-origin permission requests (2026-09-02).
- Google OAuth profile import, generalizing the existing LinkedIn BYO-OAuth flow to a second provider (2026-09-02).
- Application analytics panel — response rate by source, salary-band effectiveness, and time-to-first-response distribution, computed entirely from local tracker data (PR #57).
- Interview prep mode — Gemini-backed interview questions and suggested answers generated from a saved tracker card's JD and profile.
- Hackajob job-search source (sitemap + JSON-LD scraping, no public API available).
- Tracker module split into focused files under `popup/tracker/` for state, UI, handlers, metadata, and CSV support.
- CSV import support for tracker history with common header aliases.
- ATS receiver auto-recovery path that retries content-script injection when no receiver is active.
- Memory controls in Profile for edit, ignore, restore, and remove workflows.

### Changed

- Popup workspace UX polished with wider layout behavior, tighter tracker controls, grouped editor sections, and clearer profile actions.
- Naming/copy pass continues toward Apply Workspace across popup surfaces and docs.
- Tracker card editing flow improved for URL, location, pay, verdict, and description ergonomics.
- README gallery screenshots refreshed after popup/tracker/profile UI polish, with manual QA closeout sign-off.
- Dependabot config now assigns reviewers and groups minor/patch and GitHub Actions updates to reduce PR noise.

### Fixed

- Two tracker storage gaps that limited analytics accuracy: `job.source` was silently dropped on save, and no first-response timestamp existed (added a sticky `first_response_at`).
- Resume parse feedback, interview prep fallback, tracker card movement, and Hackajob normalization edge cases (PR #60).
- Status normalization and terminal-stage handling to keep tracker semantics honest.
- Job detail parsing and filtering behaviors for tracker/search reliability.
- Runtime wiring regressions in popup/tracker modules through lint/runtime-guard test coverage.
- Documentation drift in contribution/security/process guides and validation notes.