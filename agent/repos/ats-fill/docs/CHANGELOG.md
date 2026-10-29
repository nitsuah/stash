---
up: "[[repos/ats-fill]]"
title: "ats-fill · CHANGELOG"
source: https://github.com/nitsuah/ats-fill/blob/main/docs/CHANGELOG.md
kind: repo-doc
repo: ats-fill
---

# Changelog

> 🧭 [ats-fill](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Chrome Web Store detailed description: describe ATS and job-board support generically (no brand names) after Keyword Spam (Yellow Argon) rejection; record the rejection and listing rule in `CHROMEWEBSTORE.md`.
- GitHub Pages landing page: new `site/privacy.html` presents `docs/PRIVACY.md` (terms, privacy policy, security, data rights) on the site, linked from the footer and the Privacy nav link on that page. The Chrome Web Store listing's Privacy Policy URL is now https://nitsuah.github.io/ats-fill/privacy.html; a unit test fails if the page's document version or date drifts from `docs/PRIVACY.md`.
- GitHub Pages landing page Fill bullets: resume attach is on by default (toggle under Profile); the submit button still stays yours. Replaces the pre-1.0.4 “File uploads … stay yours” line.
- GitHub Pages landing page (`site/index.html`): complete Open Graph / Twitter Card tags (including `og:url`, `twitter:title` / `description` / `image`, and canonical), a 1200×630 `og-share.jpg` share image, and ATS copy aligned with the extension (full fill for Greenhouse, Lever, Ashby, LinkedIn Easy Apply; partial for Workday, iCIMS, Jobvite and others).
- Privacy disclosures (Chrome Web Store listing and `docs/PRIVACY.md`) now state that answers and any attached resume reach the employer's site when you submit an application yourself, including opt-in disability, salary and location answers. The in-app Help & privacy panel says the same.

### Fixed

- Long unresolved-question labels in the fill report no longer push the popup into horizontal scrolling: the label truncates with an ellipsis, and the full question is still available as the button's accessible name and tooltip (#169).

## [1.0.4] - 2026-10-16

### Fixed

- Tracker rows no longer keep a "<role> @ <company>" company name ("Staff Software Engineer - DevX @ Amplitude"): adding, editing and CSV import keep only the company.
- An application form embedded in a career page iframe (Greenhouse on databricks.com, for example) is now the frame that answers Detect ATS and job capture, so the readiness card names Greenhouse; filling it logs one tracker entry with the company and title instead of a split pair.
- Fill no longer puts profile values into long questions that merely use a field word: "…solutions to **address** recurring challenges?" got the street address, and "…located within the United **States**?" was treated as a standard field and never answered. Single words (address, state, name, available) now only match whole words in label-sized text.
- Last names no longer include a middle name or initial ("Austin J. Hardy" filled Last Name as "J. Hardy").
- The last-resort label matcher uses whole words, and a one-word saved answer only matches a label-sized prompt. "Did someone refer you? …share their name" was getting the applicant's own name, and "Do you reside in the United States?" was getting the state abbreviation.
- Required-marker labels ("…United States?*") are recognised as questions, so they get drafted answers instead of being skipped.
- A radio or checkbox group that needs review is listed once under its question instead of once per option, and react-select's hidden "required" helper inputs no longer show up as "unlabeled field".
- A type-ahead's search text is kept out of page drafts and learned memory, so a half-typed search ("United St") is never replayed on another form.
- Filled fields now get the focus-in / focus-out events a real click-in and tab-out would send. Ashby only commits a typed value to its form model on blur (React onBlur runs on focusout), so filled fields looked complete but failed "Missing entry for required field" on submit.
- Ashby Yes/No questions are answered by clicking the Yes or No button (only for an explicit yes/no answer; anything else is left for review).
- AI non-answers ("Not specified in the provided information.", "N/A") are no longer filled or remembered; the field is flagged for review instead.
- "Other: please specify" boxes are no longer filled with the group's answer (it put the race answer into the race "Other" box).
- Twitter / X fields are no longer filled with the portfolio URL.
- Job search: Remotive results now match the query. Remotive ignores its `search` parameter and returned the same listings for every search, so the query is applied to its results locally.
- Values typed by ats-fill that the user never changed are kept out of page drafts and learned memory, so one bad fill no longer comes back on reload, gets counted as "kept" by the next fill, or is reused on other applications. Radio groups are learned under their question instead of an option label.

- Standalone home masthead stacks under 640px, so the intro no longer squeezes to one word per line and the stats bar no longer overlaps it; the standalone page no longer overflows sideways by the scrollbar width (#142).
- **AI assistant access** wouldn't turn on from the toolbar popup: Chrome's Allow prompt could close along with the popup, so the permission was never granted and the helper never heard from ats-fill. The background now asks for the permission (the popup only relays the click), so the prompt stays up, and Settings says when the prompt was closed instead of looking switched on.
- **AI assistant access** setup on Windows now registers the helper through Explorer and confirms it. Run from inside a packaged app such as the Claude desktop app, the old `reg add` landed in that app's private copy of the registry, so Chrome kept reporting "Specified native messaging host not found". Settings now shows the real connection error and when ats-fill last tried, instead of a generic setup hint.

### Added

- **Type-ahead dropdowns** (Greenhouse react-select, Ashby autocomplete): Fill opens the menu, searches, and clicks the option containing every word of the answer, with US states and countries spelled out ("Sevierville, TN, US" → "Sevierville, Tennessee, United States"). Short lists also match explicit Yes/No answers, "US Citizen" for work-authorization (Yes) and sponsorship (No) questions, gender wording (Male/Man), and each form's own "prefer not to say" option. Anything else is cleared and left for review.
- **Resume attach on fill**: Fill attaches the saved resume PDF to Resume/CV upload fields (never to cover-letter or "autofill from resume" inputs, never over a file already chosen), and the fill summary says so. A checkbox under Profile → Saved local copy turns it off.
- **Remove duplicates** (Tracker toolbar): merges tracker entries for the same application. Entries match when their URLs point at the same posting (Greenhouse/Ashby/Lever/LinkedIn job IDs, ignoring apply/confirmation steps and tracking parameters), or when company and title both match and they were logged within 7 days; title and company alone are not enough. Each merge keeps the furthest-along status, the earliest date and every detail the others had, and the button lists every merge for confirmation first.
- **Nightly journeys** (`tests/journeys/`, `.github/workflows/journeys.yml`, `npm run test:journeys`): 8 journeys (home on a Greenhouse page, fill a fictional application, pipeline, analytics, interview prep, job search with filters, optional sources in Settings, phone) with 12 visual baselines, driven through the real extension on the demo state and tagged with the feature ids in `promo/spots.json`. Failures become deduplicated `bot:journey` issues through the shared `nitsuah/.github` harness with no AI. Replaces the artifact-only `playwright-nightly.yml`; `ci.yml` still runs the full e2e suite on every PR. The one-time review pass filed #142 (phone home masthead).
- Mermaid architecture and form-fill-flow diagrams in `docs/diagrams/`, embedded in the README. The `screenshot-gallery` CI job renders them (pinned `minlag/mermaid-cli`) and the rolling "docs: refresh UI screenshots" PR now carries the `.svg` renders too.
- `promo/spots.json`: existing gallery screenshots linked to the features they show, and non-visual features marked `"visual": "none"`. No spot, reel or video changed.

### Changed

- Docs: merged the duplicate 1.0.3 rows in CHROMEWEBSTORE.md's version history.

## [1.0.3] - 2026-10-14

### Added

- Tracker CLI (`npx -y github:nitsuah/ats-fill <command>` or `npm run tracker`, `scripts/tracker/`): reads the tracker straight from Chrome's on-disk LevelDB store with no setup, and syncs job emails (Gmail search output) into the tracker with a deterministic classifier. Status only moves forward, and processed emails are remembered. The skill gains `references/automation.md` covering the inbox loop and low-token daily/weekly routines.
- **AI assistant access** (Settings, off by default): a local AI assistant or the CLI can add and update tracker entries (never delete) through Chrome native messaging. `ats-fill setup` installs a per-user helper (no admin rights, no open port); ats-fill checks in about once a minute and applies queued changes through its own handlers. Without it, writes become a Tracker → Import CSV file. Remote debugging is no longer used unless `--live` is passed. Adds the `alarms` permission and an optional `nativeMessaging` permission, requested only from that setting.
- Visual showcase ([standard](https://github.com/nitsuah/.github/blob/main/showcase/STANDARD.md)): `promo/spots.json` lists every shipped FEATURES.md entry and records the existing launch video(s); feature-to-video and screenshot links are still empty and get filled in on the next `/promo` run; the Pages site loads the shared expand kit (click-to-expand images, fullscreen button on videos).
- Feature-tour video renders in native 4K (3840x2160, BT.709-tagged H.264 at YouTube's recommended GOP) so YouTube serves its higher-bitrate VP9/AV1 encodes and UI text stays sharp. Every frame is a browser render at full resolution: product screens are captured at 3x, the old whole-frame ffmpeg push-in (the main source of blur after re-encoding) is replaced by still holds plus eased zooms into each step's focus area, and steps within a chapter now flow inside one window with a cursor clicking through to the next screen, crossfading captions and a "Filled" stamp, as in the launch video. Units are encoded once and joined without re-encoding into the shorts and the combined cut. The tour is now narrated (local Kokoro TTS reading the on-screen copy, holds stretched to fit, loudness-normalised, captions and chapters as WebVTT), and a 1080p web cut plays on the landing page's new **Feature tour** section (`site/assets/feature-tour.mp4`, published with `npm run video:publish`); the workflow can attach the 4K master to a GitHub Release.
- Landing page and README link the Chrome Web Store listing ("Add to Chrome" in the hero, nav, install section and footer); the install section now leads with the store and keeps load-unpacked as the from-source option.
- Release workflow builds the Store listing set (five screenshots, both promo tiles, and a new spec-compliant 128×128 store icon with 16px transparent padding) from the release tag, validates it, and attaches `ats-fill-vX.Y.Z-store-assets.zip` to the GitHub Release with dashboard upload steps; the Store API has no listing-image endpoint, so that upload stays manual.
- Feature-tour video pipeline (`video/`, `tests/e2e/feature-video.spec.mjs`, `scripts/build-feature-video.mjs`, Docker `video` target, manual **Feature Tour Video** workflow): renders a per-feature short for each of 7 chapters plus a ~4-minute combined YouTube cut (per-short CTA slides dropped, one intro and one CTA) with chapter timestamps, upload copy and thumbnail, from the real extension and fictional data.
- Launch video (`site/assets/ats-fill.mp4`) now ends on an "Add to Chrome" Chrome Web Store button (23s, was 21s).
- Expanded the Claude skill (`skills/ats-fill-job-search`) into a router plus focused references (using ats-fill, search strategy, applications, interviews, offers, resources) with verified primary-source links, and added a Skill section with install steps to the landing page and README.
- Chrome Web Store listing assets and `.env` placeholders (#96).
- Deterministic fictional ATS product-flow fixture for E2E/screenshot runs (#80).

### Changed

- Agent instructions (`.github/copilot-instructions.md` and `CLAUDE.md`) now require closing tracked work in the same PR: update `docs/TASKS.md`, `docs/ROADMAP.md` and this changelog before the last push, and confirm `git diff origin/main...HEAD --stat` includes them before merge; added `.github/pull_request_template.md` with a "Closes TASKS item(s)" checklist.
- UI screenshot gallery is now generated in CI from fictional Playwright fixture
  data and published through a single rolling PR, with the README version/date
  metadata refreshed automatically (#77–#79, #82–#95, #97).
- `background/service-worker.js` is now a thin entry point; its message-type
  handlers were moved into `background/modules/handlers/*.js` (routing already
  lived in `background/message-router.js`), with characterization tests added
  in `tests/background-router.test.mjs`.

### Fixed

- Chrome Web Store publishing: `invalid_grant` and `unauthorized_client` failures now print the fix (the refresh token expires after 7 days while the OAuth consent screen is in "Testing"; set it to "In production", then re-mint the token with your own client in OAuth Playground). A weekly **Chrome Web Store token check** workflow (`--check-token`) refreshes a token without publishing, so a dead token shows up before release day. The setup doc covers both.
- Tracker entries capture the real company instead of the browser tab title. Ashby application pages had saved "Staff Software Engineer - DevX @ Amplitude" as the company; the tab title is now only parsed for "Role @ Company" / "Role at Company", after the page's company element and the posting's structured data, with the ATS board slug in the URL as a last resort. Workday on `*.myworkdayjobs.com` is recognised as Workday and its legal-entity code is dropped ("100 Everfox Holdings, LLC" → "Everfox Holdings, LLC"). Titles lose apply-flow prefixes such as "My Application –". Added `CHROMEWEBSTORE.md` with listing copy and a justification for every permission.
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
