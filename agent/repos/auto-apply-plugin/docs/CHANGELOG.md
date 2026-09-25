# Changelog

> 🧭 [auto-apply-plugin](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Chrome Web Store listing assets and `.env` placeholders (#96).
- Deterministic fictional ATS product-flow fixture for E2E/screenshot runs (#80).

### Changed

- UI screenshot gallery is now generated in CI from fictional Playwright fixture
  data and published through a single rolling PR, with the README version/date
  metadata refreshed automatically (#77–#79, #82–#95, #97).

### Fixed

- Chrome release workflow is dispatched automatically after a version tag (#73).

### Security

- Hardened the Chrome Web Store permission surface (#74), made LinkedIn cookie
  access optional (#75), and tightened custom-RSS network boundaries (#76).

## [1.0.2] - 2026-09-23

### Changed

- Extension version bumped to 1.0.2 (#72).

### Fixed

- Semantic manifest version validation and release-tag verification before
  dispatching the release workflow (#70, #71).

## [1.0.1] - 2026-09-23

First tagged Chrome Web Store release. Everything below shipped across the 2026
roadmap (Q2–Q4) and was previously listed under Unreleased.

### Added

- Renamed the extension to **ats-fill** (GitHub repo `nitsuah/ats-fill`, #69).
- Chrome Web Store release automation (#67).
- Custom user-configured RSS job sources (state workforce boards, internal careers feeds, etc.), merged into the existing job-source registry with per-origin permission requests (2026-09-02).
- Google OAuth profile import, generalizing the existing LinkedIn BYO-OAuth flow to a second provider (2026-09-02).
- Application analytics panel — response rate by source, salary-band effectiveness, and time-to-first-response distribution, computed entirely from local tracker data (PR #57).
- Interview prep mode — Gemini-backed interview questions and suggested answers generated from a saved tracker card's JD and profile.
- Hackajob job-search source (sitemap + JSON-LD scraping, no public API available).
- Tracker module split into focused files under `popup/tracker/` for state, UI, handlers, metadata, and CSV support.
- CSV import support for tracker history with common header aliases.
- ATS receiver auto-recovery path that retries content-script injection when no receiver is active.
- Memory controls in Profile for edit, ignore, restore, and remove workflows.
- Header nav reorder (Search → Pipeline → Interview Prep → Settings → Profile →
  Help/Privacy) with a hamburger menu collapsing to the 3 primary buttons below a
  700px breakpoint; Settings cards collapse into a "✅ Configured" summary once
  saved; Pipeline stage columns are independently collapsible and default-collapsed
  when empty; Help & Privacy sections collapsed by default (2026-09-17).
- Interview prep job-readiness bubble bar (`#interview-prep-job-bar`) to switch
  which tracked job is being prepped for.

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
- Consent-timestamp bug: any unrelated "Save Profile" click was silently
  overwriting `privacy_consent_at` with the current time; the original consent
  date is now preserved unless this is a genuine first-time accept (2026-09-17).
- Interview prep was effectively non-functional for already-tracked jobs: no
  handler existed for the `GET_APPLICATION` message it sent, and it showed "No
  job detected" even with active pipeline jobs when the current tab had no
  detectable posting. Now reads from the existing `GET_STATE` payload and falls
  back to the most recently updated active pipeline job (2026-09-17).
- Header nav toggle CSS specificity bug that kept the hamburger's `display`
  from responding to the 700px breakpoint media query (2026-09-17).
- Clarified that Google OAuth requires registering a **Web application** client
  type (not Desktop) to match `launchWebAuthFlow`'s `chromiumapp.org` redirect;
  documented in the Settings → Google OAuth card and `lib/oauth.js`.

[Unreleased]: https://github.com/nitsuah/ats-fill/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/nitsuah/ats-fill/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/nitsuah/ats-fill/releases/tag/v1.0.1
