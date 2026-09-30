---
up: "[[repos/nitsuah-io]]"
title: "nitsuah-io · API"
source: https://github.com/Nitsuah-Labs/nitsuah-io/blob/main/docs/API.md
kind: repo-doc
repo: nitsuah-io
---

# API Reference

> 🧭 [nitsuah-io](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

**Last Updated:** 2026-09-28

The code-level surface of the site: what the server serves, how pages get their metadata, and the wagmi/chain layer the Labs pages build on. For how the pieces fit together, see [ARCH.md](./ARCH.md).

## Server routes

The site runs as Next.js SSR on Netlify (Node version pinned in `.nvmrc`). There are **no `/api/*` routes yet**; `/api/chat` (bb-mcp) is planned in [ROADMAP.md](./ROADMAP.md).

| Route | Source | Behaviour |
| --- | --- | --- |
| `GET /sw.js` | `src/app/sw.js/route.ts` | Serves a no-op service worker (`skipWaiting` + `clients.claim`) with `Cache-Control: no-cache, no-store, must-revalidate`, so browsers holding an old worker replace it with one that does nothing. |
| `GET /robots.txt` | `src/app/robots.ts` | Allows `/`, `/about`, `/projects`, `/labs`; disallows account and internal paths (`/profile/`, `/logout/`, `/api/`, `/_next/`, …); blocks SEO scrapers (Semrush, Ahrefs, MJ12); points at `/sitemap.xml`. |
| `GET /sitemap.xml` | `src/app/sitemap.ts` | Static pages, the Labs pages, and the blog and client-project indexes, stamped with the build date. |
| Every page | `src/proxy.ts` | Middleware adding `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff` and `Referrer-Policy: strict-origin-when-cross-origin` outside development. It skips `_next/static`, `_next/image` and `favicon.ico`. |

The Content-Security-Policy and long-lived cache headers are set by Netlify (`netlify.toml` `[[headers]]`), not by the app. Any new third-party origin the browser calls (RPCs, wallet SDKs, CDNs) must be added to `connect-src` there, or it's blocked on the deployed site but works locally.

Covered by `src/__tests__/server-runtime.test.ts` (unit) and `tests/runtime.spec.ts` (against `next start`).

## Page metadata

`src/lib/seo.ts` exports `pageMetadata({ title, description, path, noIndex?, absoluteTitle?, image?, openGraph? })`. It returns a Next.js `Metadata` object with:

- `alternates.canonical` and `openGraph.url` set to `path`. **Every page needs its own canonical.** The root layout deliberately sets none, because a root-level canonical is inherited by every route and would mark each page a duplicate of that one URL.
- the title with ` | Austin J. Hardy` appended (as an absolute title, so it survives nested layouts that set their own title), unless `absoluteTitle` is set.
- `openGraph` and `twitter` blocks that always include an image, defaulting to `DEFAULT_OG_IMAGE` (`/og-image.jpg`, 1200×630). Next.js replaces rather than merges these objects when a page sets them.
- `robots: { index: false, follow: true }` when `noIndex` is set (used for `/profile`, `/logout` and the WIP Labs pages).

Most pages are client components, which can't export metadata, so each route directory has a small server `layout.tsx` exporting `metadata = pageMetadata(...)`. The homepage exports it from `src/app/page.tsx`, and blog posts build it in `generateMetadata` in `src/app/projects/blogs/[slug]/page.tsx`. `src/__tests__/seo.test.ts` fails if a route is missing its layout, has the wrong canonical, or duplicates another route's title or description.

## Wagmi config

`getWagmiConfig()` in `src/wagmi.ts` creates the wagmi config once and caches it. `src/app/providers.tsx` passes it to `WagmiProvider`, alongside a shared `QueryClient` (no refetch on window focus, no retries) and `ThemeProvider`.

**Chains and transports:** each chain uses viem's default public HTTP transport (`http()`).

| Chain | ID | Explorer (`EXPLORER_URLS`) |
| --- | --- | --- |
| Ethereum mainnet | 1 | etherscan.io |
| Polygon | 137 | polygonscan.com |
| Sepolia | 11155111 | sepolia.etherscan.io |
| Polygon Amoy (testnet) | 80002 | amoy.polygonscan.com |

`getExplorerLink(address, chainId)` in `src/lib/constants/networks.ts` returns `<explorer>/address/<address>`, or `null` for an unknown chain.

**Connectors:**

| Connector | When |
| --- | --- |
| `injected()` | Always (browser wallets such as MetaMask's extension). |
| `walletConnect({ projectId, showQrModal: true })`, `metaMask({ dapp })`, `safe()` | Browser only, outside test mode. WalletConnect/Reown AppKit calls `*.walletconnect.org`, `*.walletconnect.com` and `*.web3modal.org`, all allowed in the CSP. |
| `mock({ accounts: ["0x1234…5678"] })` | Browser only, in test mode: `NEXT_PUBLIC_TEST_HELPERS=1` at build time, or `?testHelpers=1` in the URL at runtime. Lets connect → account → disconnect flows run without a real wallet. |

No live connectors are created during SSR, which avoids initialising WalletConnect on the server.

## Generated contract hooks

`npm run wagmi` (`scripts/wagmi-generate.js` → `@wagmi/cli` with `config/wagmi.config.ts`) regenerates `src/generated.ts`. It needs `ETHERSCAN_API_KEY` for the Etherscan plugin and skips cleanly without it, so CI and deploy previews build from the committed file.

It exposes the `WagmiMintExample` ERC-721 on Ethereum mainnet (`0xFBA3912Ca04dd458c843e2EE08967fC04f3579c2`) as `wagmiMintExampleAbi`, `wagmiMintExampleAddress`, `wagmiMintExampleConfig` and typed hooks in four families:

- `useReadWagmiMintExample*` (10): `balanceOf`, `ownerOf`, `name`, `symbol`, `tokenURI`, `totalSupply`, `getApproved`, `isApprovedForAll`, `supportsInterface`, plus the generic reader.
- `useWriteWagmiMintExample*` (6) and `useSimulateWagmiMintExample*` (6): `mint`, `approve`, `safeTransferFrom`, `setApprovalForAll`, `transferFrom`, plus the generic writer/simulator.
- `useWatchWagmiMintExample*Event` (4): `Approval`, `ApprovalForAll`, `Transfer`, plus the generic watcher.

`src/app/_components/_web3/MintNFT.tsx` uses the `mint` simulate + write hooks. It `require`s `src/generated.ts` lazily and falls back to no-op hooks when it's unavailable (tests, missing codegen).

## Labs contracts

| Lab | Address | Source |
| --- | --- | --- |
| Register | `0x94b40dDa4ACfDe42c7B334A60f25a0f86CE163d8` | `src/app/labs/register/RegisterContentProduction.tsx` |
| Domains | `0xBbDF8C47BC3FF87aaC2396493C3F98a89C399163` | `src/app/labs/domains/DomainsContentProduction.tsx` |

The UI targets Polygon Amoy, but both contracts were only ever deployed to the now shut-down Mumbai testnet, so these addresses have no contract on Amoy until they're redeployed. See [TASKS.md](./TASKS.md) P1.

## App hooks

Exported from `src/hooks/index.ts`:

| Hook | Returns |
| --- | --- |
| `useBlogFilters(blogs)` | `{ filteredBlogs, selectedCategory, setSelectedCategory, sortBy, setSortBy, categories }`: category filter plus date / upvotes / views sort. |
| `useDelayedVisibility(delay = 1000)` | `boolean` that turns `true` after `delay` ms. |
| `useHoverStyle(base, hover)` | `[style, handlers]`: merged style plus `onMouseEnter` / `onMouseLeave`. |
| `useModal(initial = false)` | `{ isOpen, open, close, toggle }`. |
| `useScrollOpacity(fadeDistance = 300)` | Opacity from 1 → 0 over the first `fadeDistance` px of scroll. |
| `useScrollPosition()` | Current `window.scrollY`. |
