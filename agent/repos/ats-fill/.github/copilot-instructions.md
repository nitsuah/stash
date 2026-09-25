# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** ats-fill
**Description:** A local-first Chrome MV3 extension that stores a candidate's profile locally, reads job descriptions, drafts tailored answers with the user's own Gemini API key, and fills application forms — always leaving submission to the user.
**Tech Stack:** Vanilla JavaScript (ES modules), Chrome MV3 APIs, Gemini 2.5 REST API. No build step, no framework, no bundler for the extension itself.
**Testing:** Node's built-in test runner (`node --test`) for unit tests, Playwright for e2e/a11y. All checks run via Docker — see `Dockerfile` / `config/docker-compose.yml`.

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure — this is a no-build-step extension, so files run as-authored in the browser.
- Maintain consistent naming conventions across the codebase (e.g., `camelCase` for variables and functions).
- Write self-documenting code with clear variable and function names.
- Add comments only when the code's intent is not immediately clear or for complex algorithms (use JSDoc for public functions, especially in `lib/`).
- Adhere to the ESLint rules in `config/eslint.config.mjs` (`npm run lint`, zero warnings allowed).

### Language-Specific Guidelines

- **JavaScript**:
  - Use ESNext features (`const`, `let`, arrow functions, async/await, ES modules).
  - Prefer `const` over `let` when a variable is not reassigned. Avoid `var`.
  - Use JSDoc for documenting functions, parameters, and return types, especially for exported `lib/` functions.
  - Prefer pure functions in `lib/` where possible, minimizing side effects — this is what keeps them unit-testable without a browser.
  - Handle asynchronous operations with `async/await` and proper `try/catch` blocks.

### File Organization

Actual layout (see `README.md` → Project Structure for the full breakdown):

- `manifest.json` — Chrome MV3 manifest.
- `popup/` — extension popup UI (HTML/CSS/JS), organized by feature area (`ai/`, `ats/`, `forms/`, `search/`, `tracker/`, `ux/`, `analytics/`).
- `content/` — content scripts that run on job pages (JD extraction, form filling, ATS detection).
- `background/` — MV3 service worker (`service-worker.js`) plus `modules/handlers/` for per-domain message handlers.
- `lib/` — shared, browser-independent logic (Gemini wrapper, job search source registry, OAuth, tracker storage, resume/JD parsing). This is where most pure-function unit-test coverage lives.
- `data/` — static data (e.g. `field-map.json`).
- `tests/*.test.mjs` — unit tests (Node test runner), mirroring `lib/`. `tests/e2e/*.spec.mjs` — Playwright e2e + a11y specs.
- Keep files focused on a single responsibility; prefer small modules over growing one file indefinitely (see the background service-worker's `modules/handlers/` split for the pattern).

## Architecture Patterns

### Module Structure

- Keep modules small, focused, and reusable.
- Business logic that doesn't need `chrome.*` APIs or the DOM belongs in `lib/` so it can be unit-tested directly with Node's test runner.
- Minimize inter-module dependencies; prefer explicit imports.
- Extensible registries over special-casing: e.g. new job-search sources are added as one entry in `lib/job-search.js`'s `JOB_SOURCES` array, not scattered conditionals.

### State Management & Side Effects

- All persistent state lives in `chrome.storage.local` (local-first — no accounts, no backend, no sync).
- Be explicit about functions that produce side effects (storage writes, network calls, DOM mutation) and keep them separate from pure logic in `lib/`.
- Handle external interactions (DOM manipulation, `fetch`, `chrome.*` APIs) carefully, injecting them (e.g. via a `doFetch`/`ctx` parameter) so the pure logic underneath stays testable.

### Extension API Design

- Message types between popup/content/background are a flat `type` string dispatch table (see `background/service-worker.js`'s `handleMessage` switch) — follow that pattern for new messages rather than introducing a different routing mechanism.
- Validate all inputs to public/exported functions; default to safe empty values (`{}`, `[]`, `''`) rather than throwing on missing optional fields.
- Request only the permissions a feature actually needs. Arbitrary user-supplied URLs (e.g. custom job sources) use `optional_host_permissions` + `chrome.permissions.request()` scoped to that one origin, not a blanket host permission.

## Testing Strategy

- Write unit tests for all new `lib/` functions in `tests/<module>.test.mjs`, following the existing mock-object style (e.g. a `{ querySelector: (sel) => ... }` stub for DOM-shaped inputs, an injected `fetchImpl` for network calls).
- Write/extend Playwright specs in `tests/e2e/` for anything that changes popup/options UI, including an a11y check (`tests/e2e/a11y.spec.mjs`) for new panels.
- Run everything via Docker — `docker compose -f config/docker-compose.yml run --rm test|lint|coverage|e2e` — never assume a local Node/Playwright install.
