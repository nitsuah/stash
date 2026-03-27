# overseer — Meta-Repository Intelligence Layer

**Last Validated:** 2026-03-27 | PMO audit — live site + coverage validation  
**Repo:** [nitsuah/overseer](https://github.com/nitsuah/overseer)  
**Live:** https://ghoverseer.netlify.app  
**Branch convention:** `pmo/overseer/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Live site | ✅ Working | Frontend loads, repo sync in progress |
| GitHub OAuth | ✅ Working | NextAuth v5 configured |
| Netlify deployment | ✅ Working | Auto-deploys from main |
| Test coverage | ✅ 71.51% | Above 70% target (162 tests, 16 suites, 5 E2E) |

---

## Stack

- **Frontend:** Next.js 16 + React 19 + TypeScript + Tailwind CSS 4
- **Backend:** Netlify Functions + Neon Postgres
- **Auth:** NextAuth v5 + GitHub OAuth + rate limit handling
- **AI:** Gemini 2.0 + multi-provider failover (GPT-4, Claude) + auto-discovery & model switching
- **GitHub:** Octokit REST API with retry/throttling, ETag support, rate limit monitoring
- **Testing:** Vitest (71.51% coverage, 162 tests, 16 suites), Playwright E2E (5 tests)
- **CI:** GitHub Actions
- **Deployment:** Netlify with `@netlify/plugin-nextjs`

---

## Key Features

- **Repository Intelligence:** Health scoring (0-100), 4-state doc tracking, LOC parsing, test counting, CI/CD status, vulnerability alerts
- **AI Integration:** Gemini 2.0 + multi-provider failover; auto-discovers when model fails; self-healing
- **Documentation Management:** PR preview modal (diff view), AI template enrichment, one-click auto-fix (8 doc types + 4 best practices + 10 standards)
- **Security Tracking:** SECURITY.md presence, Dependabot, code scanning, secret scanning config
- **User Experience:** Guided tour (16 steps, spotlight, auto-advance), interactive onboarding
- **Rate Limiting:** Smart caching (content-hash + ETag), batch delays, exponential backoff, UI warnings

---

## Gaps (P1–P3)

| Item | Priority | Status |
|---|---|---|
| 2026Q1 Agent Task Queue API | P1 | Planned — foundation for autonomous orchestration |
| [Overseer docs/AUDIT.md refresh](https://github.com/nitsuah/overseer/blob/main/docs/AUDIT.md) | P1 | Stale — last validated Dec 11, 2025 (3.5mo) |
| Conversational UI foundation | P2 | Planned — natural language + handler routing |
| Workflow visualization | P2 | Planned — execution paths for multi-step actions |
| AI doc improvement buttons | P2 | Planned — "Improve" for ROADMAP/TASKS/FEATURES |
| Token density, zombie branches, dark mode | P3 | Open/Exploratory |

---

## Key Commands

```bash
npm run dev                    # Development server
npm run build                  # Production build
npm test                       # Unit tests (71.51% coverage)
npm run test-gemini           # Test Gemini model (auto-discovery)
npm run list-gemini-models    # List available models
npm run setup-db              # Initialize Postgres schema
```

---

## Notable Details

- **Model Auto-Discovery:** When Gemini unavailable, auto-tests and switches to GPT-4/Claude mid-session (15min cache)
- **Rate Limit Safeguards:** Exponential backoff, content-hash caching (5min TTL), ETag support, batch delays (configurable)
- **Health Score:** 0-100 with breakdown (docs 40%, testing 20%, best practices 20%, standards 10%, activity 10%)
- **Doc Health Tracking:** 4-state model (Missing/Dormant/Malformed/Healthy) via content-hash
- **Security Tracking:** 6 GitHub settings monitored (SECURITY.md, advisories, Dependabot, scanning, etc.)

---

## Active PMO

See [TASKS.md](https://github.com/nitsuah/overseer/blob/main/TASKS.md) and [ROADMAP.md](https://github.com/nitsuah/overseer/blob/main/ROADMAP.md) in the Overseer repo for current priorities. Latest PR: `pmo/overseer/planning-alignment-2026-03-27` — [PR #82](https://github.com/nitsuah/overseer/pull/82)
