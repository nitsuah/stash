---
kind: eng-loc
repo: 9router
date: 2026-07-29
---

# ENG LOC Report — 9router (2026-07-29)

> 🧭 ← [[reports/eng-loc-9router-2026-07-04|2026-07-04]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 1502 | 9router/src/lib/oauth/providers.js | Large config - check for unused providers |
| 1307 | 9router/src/app/(dashboard)/dashboard/usage/components/ProviderLimits/index.js | Complex component - extract subcomponents |
| 1295 | 9router/src/app/(dashboard)/dashboard/endpoint/EndpointPageClient.js | Large client component - extract sections |
| 1182 | 9router/src/app/(dashboard)/dashboard/profile/page.js | Page - extract profile sections |
| 1063 | 9router/src/app/(dashboard)/dashboard/proxy-pools/page.js | Page - extract pool management |
| 967 | 9router/src/app/(dashboard)/dashboard/basic-chat/BasicChatPageClient.js | Chat component - extract message handling |
| 966 | 9router/src/app/(dashboard)/dashboard/providers/page.js | Page - extract provider list |
| 904 | 9router/open-sse/utils/cursorProtobuf.js | **Generated code** - likely auto-generated protobuf |
| 877 | 9router/src/mitm/manager.js | MITM manager - extract handlers |
| 859 | 9router/src/lib/tunnel/tailscale/tailscale.js | Tailscale integration - extract config |
| 846 | 9router/cli/src/cli/menus/providers.js | CLI menu - modularize |
| 830 | 9router/cli/cli.js | Main CLI - extract commands |
| 780 | 9router/src/lib/db/repos/usageRepo.js | Repository - split queries |
| 704 | 9router/src/shared/components/OAuthModal.js | Modal - extract form, providers |
| 688 | 9router/open-sse/executors/cursor.js | Executor - extract helpers |
| 654 | 9router/src/app/(dashboard)/dashboard/combos/page.js | Page - extract combo logic |
| 646 | 9router/tests/unit/embeddingsCore.test.js | Test - split by embedding provider |
| 631 | 9router/src/app/api/providers/validate/route.js | API route - extract validation |
| 624 | 9router/open-sse/services/tokenRefresh/providers.js | Token refresh - extract providers |
| 618 | 9router/cli/src/cli/menus/cliTools.js | CLI tools menu - modularize |
| 597 | 9router/src/app/(dashboard)/dashboard/cli-tools/components/CoworkToolCard.js | Component - extract parts |
| 596 | 9router/open-sse/translator/request/openai-to-kiro.js | Translator - extract mapping |
| 568 | 9router/open-sse/executors/kiro.js | Kiro executor - extract logic |
| 566 | 9router/src/app/(dashboard)/dashboard/media-providers/[kind]/[id]/components/TtsExampleCard.js | Component - extract subcomponents |
| 526 | 9router/src/mitm/handlers/kiro.js | MITM handler - extract logic |
| 524 | 9router/tests/unit/embeddings.cloud.test.js | Test - split by cloud provider |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | 9router/src/app/api/v1/route.js | Merge into parent route or remove |
| 1 | 9router/src/shared/utils/clineAuth.js | Merge with auth utilities |
| 2 | 9router/src/lib/qoder/constants.js | Merge with qoder module |
| 2 | 9router/src/lib/qoder/cosy.js | Merge with qoder module |
| 2 | 9router/src/lib/qoder/encoding.js | Merge with qoder module |
| 3 | 9router/src/shared/hooks/index.js | Merge with hooks barrel |
| 4 | 9router/src/lib/disabledModelsDb.js | Merge with DB utilities |
| 4 | 9router/src/app/api/init/route.js | Check if needed |
| 4 | 9router/src/lib/requestDetailsDb.js | Merge with DB utilities |
| 4 | 9router/src/shared/components/layouts/index.js | Merge with layouts barrel |
| 4 | 9router/src/shared/constants/index.js | Merge with constants barrel |
| 4 | 9router/open-sse/handlers/embeddingProviders/_base.js | Check if base class needed |
| 5 | 9router/src/app/(dashboard)/dashboard/basic-chat/page.js | Check if re-export |
| 5 | 9router/src/app/(dashboard)/dashboard/token-saver/page.js | Check if re-export |
| 5 | 9router/src/app/(dashboard)/dashboard/mitm/page.js | Check if re-export |
| 5 | 9router/src/app/page.js | Check if re-export |
| 5 | 9router/src/app/(dashboard)/dashboard/cli-tools/page.js | Check if re-export |
| 5 | 9router/open-sse/translator/concerns/json.js | Merge with translator concerns |
| 5 | 9router/src/app/(dashboard)/dashboard/endpoint/page.js | Check if re-export |
| 6 | 9router/src/store/index.js | Merge with store barrel |
| 6 | 9router/src/shared/utils/machine.js | Merge with machine utilities |
| 6 | 9router/src/app/(dashboard)/layout.js | Check if layout wrapper |
| 6 | 9router/src/shared/utils/connectionStatus.js | Merge with connection utilities |
| 7 | 9router/src/app/(dashboard)/dashboard/page.js | Check if re-export |
| 7 | 9router/src/lib/usageDb.js | Merge with DB utilities |
| 7 | 9router/src/lib/tunnel/tailscale/config.js | Merge with tailscale config |
| 7 | 9router/open-sse/translator/concerns/message.js | Merge with translator concerns |
| 7 | 9router/src/lib/tunnel/cloudflare/config.js | Merge with cloudflare config |
| 7 | 9router/open-sse/translator/schema/defaults.js | Merge with schema defaults |
| 8 | 9router/src/lib/tunnel/shared/watchdogConfig.js | Merge with shared config |
| 8 | 9router/src/proxy.js | Check if proxy config |
| 8 | 9router/src/app/(dashboard)/dashboard/console-log/page.js | Check if re-export |
| 8 | 9router/open-sse/translator/schema/index.js | Merge with schema barrel |
| 9 | 9router/open-sse/translator/concerns/chunk.js | Merge with translator concerns |
| 9 | 9router/src/lib/db/helpers/jsonCol.js | Merge with DB helpers |
| 9 | 9router/open-sse/rtk/ponytail.js | Check if utility |
| 9 | 9router/open-sse/rtk/caveman.js | Check if utility |
| 10 | 9router/src/lib/db/migrations/index.js | Check if migration index |
| 10 | 9router/src/shared/utils/cn.js | Merge with cn utility |
| 10 | 9router/src/lib/localDb.js | Merge with DB utilities |
| 11 | 9router/open-sse/translator/concerns/chunk.js | Duplicate entry |
| 12 | 9router/src/app/api/usage/logs/route.js | Check if needed |
| 12 | 9router/src/app/api/usage/history/route.js | Check if needed |
| 12 | 9router/tests/unit/capabilities.test.js | Merge with capabilities tests |
| 12 | 9router/tests/unit/hf-model-routing.test.js | Merge with routing tests |
| 12 | 9router/src/app/api/tunnel/tailscale-enable/route.js | Merge with tailscale routes |
| 12 | 9router/src/app/api/tunnel/tailscale-disable/route.js | Merge with tailscale routes |
| 12 | 9router/src/app/api/tunnel/disable/route.js | Merge with tunnel routes |
| 13 | 9router/src/app/api/models/test/route.js | Check if test route |
| 13 | 9router/open-sse/translator/schema/roles.js | Merge with schema |
| 13 | 9router/src/app/api/v1/images/generations/route.js | Check if needed |
| 13 | 9router/src/app/api/v1/audio/speech/route.js | Check if needed |
| 13 | 9router/src/app/api/auth/reset-password/route.js | Check if needed |
| 14 | 9router/src/lib/db/migrations/001-initial.js | Check if migration file |
| 14 | 9router/open-sse/utils/sse.js | Merge with SSE utilities |
| 14 | 9router/src/app/api/version/shutdown/route.js | Check if needed |
| 14 | 9router/src/app/api/version/update/route.js | Check if needed |
| 14 | 9router/open-sse/handlers/imageProviders/comfyui.js | Merge with image providers |
| 14 | 9router/open-sse/executors/ollama-local.js | Merge with executors |
| 14 | 9router/open-sse/utils/debugLog.js | Merge with debug utilities |
| 14 | 9router/src/app/api/settings/require-login/route.js | Check if needed |
| 14 | 9router/src/app/api/headroom/stop/route.js | Check if needed |
| 15 | 9router/src/mitm/handlers/cursor.js | Merge with MITM handlers |
| 15 | 9router/src/shared/components/ThemeProvider.js | Check if provider wrapper |
| 15 | 9router/src/app/api/health/route.js | Check if needed |
| 15 | 9router/open-sse/rtk/filters/smartTruncate.js | Merge with RTK filters |
| 15 | 9router/open-sse/rtk/applyFilter.js | Merge with RTK utilities |
| 15 | 9router/tests/unit/provider-thinking-config.test.js | Merge with provider tests |
| 15 | 9router/public/sw.js | Service worker - check if minimal |
| 16 | 9router/src/app/api/v1/embeddings/route.js | Check if needed |
| 16 | 9router/src/app/api/v1/search/route.js | Check if needed |
| 16 | 9router/src/app/api/v1/web/fetch/route.js | Check if needed |
| 16 | 9router/src/lib/db/version.js | Merge with DB utilities |
| 17 | 9router/src/lib/oauth/services/index.js | Check if barrel file |
| 17 | 9router/src/lib/tunnel/shared/dnsResolver.js | Merge with tunnel shared |
| 17 | 9router/src/app/api/v1/audio/transcriptions/route.js | Check if needed |
| 17 | 9router/src/app/api/tunnel/enable/route.js | Merge with tunnel routes |
| 17 | 9router/src/app/api/usage/chart/route.js | Check if needed |

---

*Generated: 2026-07-29*
