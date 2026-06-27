# Netlify Cost Optimization & Migration Plan

| Repo | Type | Current | Recommendation | Why? |
| :--- | :--- | :--- | :--- | :--- |
| **darkmoon** | Static | Netlify | Keep (Netlify) | Non-critical, aesthetic, cheap. |
| **nitsuah-arcade**| Web/Next | Netlify | Keep (Netlify) | Low traffic, personal play. |
| **nitsuah.io** | Web/Next | Netlify | Keep (Netlify) | Portfolio/Identity, low complexity. |
| **pgfarms** | Web/Next | Netlify | Vercel (Free) | More robust Next.js perf/features. |
| **ghoverseer** | Web/Next | Netlify | Vercel (Free) | Higher utility, better DX on Vercel. |
| **skyviewd** | Static | Netlify | Vercel or CF Pages | Move for free tier optimization. |
| **agent-board** | Local/Tool| N/A | Keep Local | CLI/Agent focus, no web surface needed. |
| **vhs** | Local/Tool| N/A | Keep Local | Dev/Recording tool, not web-hosted. |

## Strategy
1. **Netlify:** Keep low-criticality, low-traffic sites here if under free tier limits.
2. **Vercel:** Priority migration for performance/feature-heavy projects (Next.js focus).
3. **Local:** Maintain `agent-board` and `vhs` as tool-focused, non-deployed artifacts.
