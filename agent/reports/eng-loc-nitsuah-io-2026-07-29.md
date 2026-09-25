---
kind: eng-loc
repo: nitsuah-io
date: 2026-07-29
---

# ENG LOC Report — nitsuah-io (2026-07-29)

> 🧭 [[repos/nitsuah-io|nitsuah-io]] · ← [[reports/eng-loc-nitsuah-io-2026-07-04|2026-07-04]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 535 | nitsuah-io/src/generated.ts | Generated file - check if auto-generated |
| 509 | nitsuah-io/src/app/projects/clients/_comp/NFTDemo.tsx | NFT demo - extract components |
| 508 | nitsuah-io/src/app/crypto/page.tsx | Crypto page - extract sections |
| 507 | nitsuah-io/src/utils/__tests__/validation.test.ts | Validation tests - split by validator |
| 487 | nitsuah-io/src/app/projects/clients/_comp/RealEstateDemo.tsx | Real estate demo - extract components |
| 437 | nitsuah-io/src/app/projects/clients/_comp/PortfolioDemo.tsx | Portfolio demo - extract components |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | nitsuah-io/src/components/ui/ScrollIndicator/index.ts | Merge with ScrollIndicator |
| 2 | nitsuah-io/src/components/ui/Card/index.ts | Merge with Card barrel |
| 2 | nitsuah-io/src/components/ui/Badge/index.ts | Merge with Badge barrel |
| 2 | nitsuah-io/src/app/about/_components/index.ts | Merge with about barrel |
| 2 | nitsuah-io/src/components/ui/Modal/index.ts | Merge with Modal barrel |
| 2 | nitsuah-io/src/components/ui/Button/index.ts | Merge with Button barrel |
| 3 | nitsuah-io/src/lib/constants/wallets.ts | Merge with constants |
| 3 | nitsuah-io/src/__tests__/sanity.test.ts | Merge with tests |
| 4 | nitsuah-io/src/types/styles.d.ts | Merge with types |
| 4 | nitsuah-io/src/app/projects/clients/_comp/clients/ClientsProjectList.tsx | Merge with clients |
| 4 | nitsuah-io/src/app/_components/_site/_comp/homebar/Brand.tsx | Merge with homebar |
| 5 | nitsuah-io/src/components/demos/index.ts | Merge with demos barrel |
| 5 | nitsuah-io/src/app/clients/page.tsx | Check if page |
| 5 | nitsuah-io/src/app/blogs/page.tsx | Check if page |
| 5 | nitsuah-io/src/hooks/index.ts | Merge with hooks barrel |
| 6 | nitsuah-io/src/app/resume/_components/index.ts | Merge with resume barrel |
| 6 | nitsuah-io/src/app/head.tsx | Check if head |
| 6 | nitsuah-io/src/app/resume/_components/index.ts | Duplicate |
| 7 | nitsuah-io/src/utils/index.ts | Merge with utils barrel |
| 8 | nitsuah-io/src/app/_components/_site/_comp/homebar/Brand.tsx | Duplicate |
| 9 | nitsuah-io/src/types/next-types.d.ts | Merge with types |
| 10 | nitsuah-io/src/app/projects/clients/_comp/resume/__tests__/SkillsSection.test.tsx | Merge with resume tests |
| 11 | nitsuah-io/src/app/_components/SSRFooter.tsx | Merge with SSR components |
| 11 | nitsuah-io/src/app/projects/clients/_comp/resume/__tests__/ExperienceSection.test.tsx | Merge with resume tests |
| 11 | nitsuah-io/src/app/_components/_web3/Connected.tsx | Merge with web3 |
| 12 | nitsuah-io/__mocks__/generated.js | Merge with mocks |
| 12 | nitsuah-io/src/app/projects/clients/_comp/resume/__tests__/ContactForm.test.tsx | Merge with resume tests |
| 13 | nitsuah-io/scripts/debug-resume.js | Check if debug script |
| 14 | nitsuah-io/src/app/_components/_labs/_utils/networks.js | Merge with labs utils |
| 14 | nitsuah-io/src/app/projects/clients/_comp/SaaSDemo.tsx | Check if demo |
| 14 | nitsuah-io/src/app/projects/clients/_comp/resume/__tests__/ContactForm.test.tsx | Duplicate |
| 15 | nitsuah-io/src/app/_components/_web3/Account.tsx | Merge with web3 |
| 15 | nitsuah-io/src/hooks/useDelayedVisibility.ts | Merge with hooks |
| 16 | nitsuah-io/src/lib/constants/networks.ts | Merge with constants |
| 16 | nitsuah-io/src/hooks/useModal.ts | Merge with hooks |
| 16 | nitsuah-io/src/app/_components/_site/_comp/homebar/ExportPDF.tsx | Merge with homebar |
| 16 | nitsuah-io/src/hooks/useScrollPosition.ts | Merge with hooks |
| 17 | nitsuah-io/src/lib/data/project-filters.ts | Merge with data |
| 18 | nitsuah-io/src/app/_components/_labs/DomainsNotConnected.tsx | Merge with labs |
| 18 | nitsuah-io/src/app/resume/_components/LanguagesSection.tsx | Merge with resume |
| 18 | nitsuah-io/src/app/projects/blogs/_api/fetchBlogs.js | Merge with blogs API |
| 18 | nitsuah-io/src/app/projects/clients/_comp/resume/__tests__/ExperienceSection.test.tsx | Duplicate |
| 19 | nitsuah-io/src/app/_components/SSRHeader.tsx | Merge with SSR |
| 20 | nitsuah-io/src/lib/constants/projectCategories.ts | Merge with constants |
| 21 | nitsuah-io/src/lib/data/blogs.ts | Merge with data |
| 21 | nitsuah-io/src/app/sw.js/route.ts | Check if service worker |
| 23 | nitsuah-io/scripts/debug-resume.js | Duplicate |
| 23 | nitsuah-io/src/app/labs/register/page.tsx | Check if page |
| 24 | nitsuah-io/src/components/ui/ScrollIndicator/ScrollIndicator.tsx | Merge with ScrollIndicator |
| 24 | nitsuah-io/src/types/images.d.ts | Merge with types |
| 24 | nitsuah-io/__mocks__/wagmi-codegen.js | Merge with mocks |
| 25 | nitsuah-io/scripts/debug-resume-html.js | Check if debug |
| 26 | nitsuah-io/src/app/resume/_components/LanguagesSection.tsx | Duplicate |
| 26 | nitsuah-io/src/app/_components/_web3/Account.tsx | Duplicate |
| 27 | nitsuah-io/src/components/ui/Badge/Badge.tsx | Merge with Badge |
| 27 | nitsuah-io/src/app/page.tsx | Check if page entry |
| 27 | nitsuah-io/src/hooks/useHoverStyle.ts | Merge with hooks |
| 27 | nitsuah-io/src/app/_components/_labs/DomainsNotConnected.tsx | Duplicate |
| 28 | nitsuah-io/src/app/_components/_site/Search.tsx | Merge with site |
| 28 | nitsuah-io/src/hooks/useScrollOpacity.ts | Merge with hooks |
| 29 | nitsuah-io/src/proxy.ts | Check if proxy |
| 29 | nitsuah-io/src/app/projects/clients/_comp/resume/__tests__/ContactForm.test.tsx | Triplicate |
| 29 | nitsuah-io/tests/global-setup.ts | Check if global setup |

---

*Generated: 2026-07-29*
