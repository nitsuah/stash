# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Roadmap**: New strategic roadmap focusing on Services, Gallery, and Contact features.
- **Tasks**: Specific implementation tasks for Phase 1 and 2.
- **Features**: clearer definition of core site features (Drone services, dynamic gallery).

### Changed
- **Documentation**: Complete overhaul of project documentation (`ROADMAP.md`, `TASKS.md`, `FEATURES.md`) to align with Skyview project goals.
- **Cleanup**: Removed generic boilerplate tasks unrelated to the current static site architecture.

## [0.1.0] - In Progress

### Added
- **Dynamic Gallery**: Implemented `gallery-loader.js` to fetch images from `assets/gallery.json`.
- **E2E Testing**: Added Playwright tests (`tests/site.spec.ts`) covering critical paths.
- **Admin Panel**: Added Decap CMS (`admin/`) for managing gallery assets without code.
- **Documentation**: Added `docs/ASSET_MANAGEMENT.md`.

### Changed
- **Services**: Updated service cards with real-world offerings (Real Estate, Cinematography, Mapping).
- **Contact Form**: Configured for Netlify Forms (`data-netlify="true"`).
- **Structure**: Gallery is now rendered dynamically on page load.
- **Infrastructure**: Replaced incorrect Dockerfile and removed confused linter/test configs. Added `stylelint.config.mjs` and correct valid `Dockerfile` for static serving.
