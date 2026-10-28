---
kind: eng-loc
repo: nitsuah-io
date: 2026-10-08
---

# LOC Report — nitsuah-io

> 🧭 [[repos/nitsuah-io|nitsuah-io]] · ← [[reports/eng-loc-nitsuah-io-2026-07-29|2026-07-29]] <!-- nav -->

HEAD: ad5e92b9370ff31dc50f5ef3e7ee75070770b156

---
kind: eng-loc
repo: nitsuah-io
date: 2026-10-08
---


Mode: `--report` (dry run, no changes made)
Date: 2026-10-08
Source: shallow clone (`--depth 1`) of `Nitsuah-Labs/nitsuah-io` @ `ad5e92b9370ff31dc50f5ef3e7ee75070770b156`
Method: `git ls-files` (Phase 0 spec exclusions applied) + per-file line counts — actual counts, not estimated. Shallow clone has no history beyond HEAD, so churn signals are **assumed unavailable**.

Canaries: 0/0 (no canary file tracked in this repo)

## Inventory Summary
- Tracked source files (post-exclusion): 372
- Note: top-by-size list is a mix of CSS, generated/static blog HTML, data (ABI JSON), and actual TSX/JS code. Per Evidence Rules, CSS-only files and generated static output are noted as low structural risk regardless of size.

## Top LOC Files (all tracked files, unfiltered by type)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `src/app/resume/resume.css` | 1,649 | CSS | Stylesheet |
| 2 | `github-pages-blog/index.html` | 1,143 | HTML | Generated static blog index (build output of `generate-articles.js`) |
| 3 | `generate-articles.js` | 899 | JS | **Code** — blog generation script |
| 4 | `src/app/_components/_styles/labs.css` | 843 | CSS | Stylesheet |
| 5 | `src/app/_components/_styles/global.css` | 820 | CSS | Stylesheet |
| 6 | `github-pages-blog/blog/index.html` | 797 | HTML | Generated static blog page |
| 7 | `src/app/projects/clients/_styles/client.css` | 631 | CSS | Stylesheet |
| 8 | `src/app/_components/_labs/_utils/mintABI.json` | 605 | JSON | Contract ABI (data) |
| 9 | `src/app/_components/_labs/_utils/domainABI.json` | 596 | JSON | Contract ABI (data) |
| 10 | `promo/spots.json` | 588 | JSON | Promo config (data) |

## Top Code Files (the actual refactor-candidate pool)

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `generate-articles.js` | 899 | JS | Blog build script |
| 2 | `src/generated.ts` | 535 | TS | Generated (codegen output) |
| 3 | `src/app/projects/clients/_comp/NFTDemo.tsx` | 509 | TSX | Client demo component |
| 4 | `src/app/crypto/page.tsx` | 508 | TSX | Crypto page — single component |
| 5 | `src/utils/__tests__/validation.test.ts` | 507 | TS | Test file |
| 6 | `src/app/projects/clients/_comp/RealEstateDemo.tsx` | 487 | TSX | Client demo component |

## Risk Rank & Rationale

1. **`src/app/crypto/page.tsx` — High**
   508 lines, but it's effectively **one component function** (`const CryptoPage = () => {...}`, lines 13–508, ~495 lines) with 5 `useState`/`useEffect`/etc. hook calls and deeply nested JSX (`return (` reappearing at three increasing indent levels around lines 62, 289, 445). Confirmed structural signals: a single function far over the ~80-line threshold, mixed concerns (state + handlers + markup all inline), and deep nesting. No test file found for this page (`find . -iname "*crypto*test*"` returned nothing), so coverage is assumed zero, not just low.

2. **`generate-articles.js` — Medium**
   899 lines mixing filesystem/path I/O, markdown-to-HTML conversion (`markdownToHtml`), and page templating (`generateArticlePage`) in one script — at least three distinct concerns. Also contains embedded example-code snippets (a `class Service` with a decorator, an `async function UserProfile`) inside string templates, which is expected for a blog generator but adds to the file's apparent complexity on a naive scan. Churn assumed unavailable (shallow clone).

3. **`NFTDemo.tsx` / `RealEstateDemo.tsx` — Low/Medium (tentative)**
   ~500 lines each, single default-exported component each (`export const NFTDemo: React.FC<...>`, `export const RealEstateDemo: React.FC = () => {...}`). Plausibly large single-function components like the crypto page, but not confirmed by a full line-level read this cycle — marked "assumed: large function body, not confirmed" per Evidence Rules. Recommend a closer read next cycle before committing to a phase plan.

4. **CSS files (`resume.css`, `labs.css`, `global.css`, `client.css`) — Low**
   Per Evidence Rules, CSS-only large files are a style/maintainability smell, not a complexity risk — deferred to a design-system pass, not this one.

5. **`github-pages-blog/index.html` / `blog/index.html` — Low, informational**
   Generated static output of `generate-articles.js`, not hand-maintained source. Not a refactor target in its own right; any improvement here flows from fixing the generator.

6. **ABI JSON / `promo/spots.json` / `src/generated.ts` — Low**
   Data/config/codegen output, not hand-authored logic. Deferred.

## Refactor Opportunities by Phase

**`src/app/crypto/page.tsx`**:
- Phase 1: extract data-fetching/state logic (the 5 hooks and their handlers) into a `useCryptoPageData()` hook, leaving `CryptoPage` as a thinner render function.
- Phase 2: split the JSX into sub-components along the three nested `return (` blocks identified (likely a list/table section and a detail/modal section) — exact boundaries need a full read to confirm.
- Phase 3: re-export `CryptoPage` unchanged from `page.tsx` so the route contract doesn't change.

**`generate-articles.js`**:
- Phase 1: extract `markdownToHtml` and `generateArticlePage` into a `lib/markdown-to-html.js` / `lib/article-template.js` pair.
- Phase 2: leave the top-level script as I/O orchestration (read posts → call markdown lib → write `github-pages-blog/`).

## Validation Plan (for eventual `--refactor`)
- No `Dockerfile`/`docker-compose.yml`/devcontainer found at repo root; this is a Next.js app — validate with the existing `__tests__` suites (one exists per component family, e.g. `src/components/demos/__tests__/`) plus `npm run build` / dev server smoke test.
- `crypto/page.tsx` has **no existing test** — add a smoke test (render + one interaction path) before extracting, per Evidence Rules guidance on low-coverage files.
- Flag `crypto/page.tsx` as a UX surface needing manual QC before merge — it's a user-facing page with nested interactive JSX, not just internal logic.

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| nitsuah-io | `src/app/crypto/page.tsx` (single ~495-line component, no tests) | High | Real hotspots are TSX/JS; CSS and generated blog HTML are large but low-risk by Evidence Rules |

## Ordered Next-Cycle Targets (this repo)
1. `src/app/crypto/page.tsx` — extract state hook + split JSX (High)
2. `generate-articles.js` — extract markdown/templating libs (Medium)
3. `NFTDemo.tsx` / `RealEstateDemo.tsx` — structural read to confirm/deny single-giant-function risk (Low/Medium, tentative)

## Deferred / Not Flagged
- `resume.css`, `labs.css`, `global.css`, `client.css` — CSS-only, style/maintainability smell not complexity risk.
- `github-pages-blog/index.html`, `github-pages-blog/blog/index.html` — generated static output.
- `mintABI.json`, `domainABI.json`, `promo/spots.json`, `src/generated.ts` — data/config/codegen, not hand-authored.

## Assumptions / Unconfirmed
- Churn/author-frequency signals for all files: **assumed unavailable** — shallow clone has no history beyond HEAD.
- `NFTDemo.tsx`/`RealEstateDemo.tsx` single-giant-function claim: plausible from file size and single top-level export, not confirmed by a full read this cycle.
