# ENG LOC Report: nitsuah-io

> 🧭 [[repos/nitsuah-io|nitsuah-io]] · ← [[reports/eng-loc-nitsuah-io-2026-06-25|2026-06-25]] · [[reports/eng-loc-nitsuah-io-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** nitsuah-io (nitsuah-io)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 535 | `src/generated.ts` | Repeated block (2 occurrences, 10+ lines):   {
    type: 'event',
    anonymous: false,
    inputs: [
      {
        name:... |
| 509 | `src/app/projects/clients/_comp/NFTDemo.tsx` | Unused function (heuristic): if; Repeated block (2 occurrences, 10+ lines):               </p>
              <button
                onClick={() => setWalle... |
| 508 | `src/app/crypto/page.tsx` | — |
| 507 | `src/utils/__tests__/validation.test.ts` | — |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 1 | `src/app/about/_components/index.ts` | — |
| 1 | `src/components/ui/ScrollIndicator/index.ts` | src/components/ui/ScrollIndicator/ScrollIndicator.tsx |
| 2 | `src/components/ui/Badge/index.ts` | — |
| 2 | `src/components/ui/Button/index.ts` | — |
| 2 | `src/components/ui/Card/index.ts` | — |
| 2 | `src/components/ui/Modal/index.ts` | — |
| 2 | `__mocks__/viem.js` | __mocks__/generated.js |
| 3 | `src/lib/constants/wallets.ts` | src/lib/constants/networks.ts |
| 3 | `tests/_utils/playwright-helpers.d.ts` | — |
| 4 | `src/types/styles.d.ts` | src/types/jest-dom.d.ts |
| 5 | `src/components/demos/index.ts` | — |
| 5 | `src/__tests__/sanity.test.ts` | — |
| 6 | `next-env.d.ts` | — |
| 6 | `src/app/blogs/page.tsx` | — |
| 6 | `src/app/clients/page.tsx` | — |
| 6 | `src/hooks/index.ts` | src/hooks/useDelayedVisibility.ts |
| 7 | `src/types/jest-dom.d.ts` | src/types/styles.d.ts |
| 7 | `src/utils/index.ts` | — |
| 8 | `src/app/head.tsx` | src/app/page.tsx |
| 8 | `src/app/resume/_components/index.ts` | src/app/resume/_components/LanguagesSection.tsx |
| 9 | `src/types/next-types.d.ts` | src/types/styles.d.ts |
| 11 | `src/app/projects/clients/_comp/resume/__tests__/SkillsSection.test.tsx` | src/app/projects/clients/_comp/resume/__tests__/ExperienceSection.test.tsx |
| 11 | `src/app/_components/SSRFooter.tsx` | src/app/_components/SSRHeader.tsx |
| 11 | `src/app/_components/_web3/Connected.tsx` | src/app/_components/_web3/Account.tsx |
| 12 | `src/app/projects/clients/_comp/resume/__tests__/ExperienceSection.test.tsx` | src/app/projects/clients/_comp/resume/__tests__/SkillsSection.test.tsx |
| 12 | `__mocks__/generated.js` | __mocks__/viem.js |
| 14 | `src/app/_components/_labs/_utils/networks.js` | — |
| 15 | `src/app/_components/_site/Search.tsx` | — |
| 15 | `src/app/_components/_web3/Account.tsx` | src/app/_components/_web3/Connected.tsx |
| 15 | `src/hooks/useDelayedVisibility.ts` | src/hooks/index.ts |
| 16 | `src/app/_components/_labs/DomainsNotConnected.tsx` | — |
| 16 | `src/app/_components/_site/_comp/homebar/__tests__/Brand.test.tsx` | — |
| 16 | `src/hooks/useModal.ts` | src/hooks/index.ts |
| 16 | `src/hooks/useScrollPosition.ts` | src/hooks/index.ts |
| 16 | `src/lib/constants/networks.ts` | src/lib/constants/wallets.ts |
| 17 | `src/hooks/useHoverStyle.ts` | src/hooks/index.ts |
| 17 | `src/lib/data/project-filters.ts` | src/lib/data/blogs.ts |
| 18 | `src/app/projects/blogs/_api/fetchBlogs.js` | — |
| 18 | `src/app/projects/clients/_comp/SaaSDemo.tsx` | — |
| 18 | `src/app/_components/SSRHeader.tsx` | src/app/_components/SSRFooter.tsx |
| 18 | `src/app/_components/_site/_comp/homebar/ExportPDF.tsx` | — |
| 18 | `src/hooks/useScrollOpacity.ts` | src/hooks/index.ts |
| 20 | `src/lib/constants/projectCategories.ts` | src/lib/constants/wallets.ts |
| 21 | `src/lib/data/blogs.ts` | src/lib/data/project-filters.ts |
| 23 | `src/app/sw.js/route.ts` | — |
| 23 | `src/app/_components/__tests__/HeroSection.test.tsx` | — |
| 24 | `src/components/ui/ScrollIndicator/ScrollIndicator.tsx` | src/components/ui/ScrollIndicator/index.ts |
| 24 | `src/types/images.d.ts` | src/types/styles.d.ts |
| 24 | `__mocks__/wagmi-codegen.js` | __mocks__/viem.js |
| 26 | `scripts/debug-resume.js` | scripts/debug-resume-html.js |
| 26 | `src/app/labs/register/page.tsx` | — |
| 26 | `src/app/resume/_components/LanguagesSection.tsx` | src/app/resume/_components/index.ts |
| 27 | `src/app/page.tsx` | src/app/head.tsx |
| 29 | `scripts/debug-resume-html.js` | scripts/debug-resume.js |
| 29 | `src/proxy.ts` | — |
| 29 | `src/app/projects/clients/_comp/resume/__tests__/ContactForm.test.tsx` | src/app/projects/clients/_comp/resume/__tests__/SkillsSection.test.tsx |
| 29 | `tests/global-setup.ts` | — |
