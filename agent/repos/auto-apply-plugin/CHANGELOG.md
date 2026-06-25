# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Tracker module split into focused files under `popup/tracker/` for state, UI, handlers, metadata, and CSV support.
- CSV import support for tracker history with common header aliases.
- ATS receiver auto-recovery path that retries content-script injection when no receiver is active.
- Memory controls in Profile for edit, ignore, restore, and remove workflows.
### Changed
- Popup workspace UX polished with wider layout behavior, tighter tracker controls, grouped editor sections, and clearer profile actions.
- Naming/copy pass continues toward Apply Workspace across popup surfaces and docs.
- Tracker card editing flow improved for URL, location, pay, verdict, and description ergonomics.
- README gallery screenshots refreshed after popup/tracker/profile UI polish, with manual QA closeout sign-off.
### Fixed
- Status normalization and terminal-stage handling to keep tracker semantics honest.
- Job detail parsing and filtering behaviors for tracker/search reliability.
- Runtime wiring regressions in popup/tracker modules through lint/runtime-guard test coverage.
- Documentation drift in contribution/security/process guides and validation notes.