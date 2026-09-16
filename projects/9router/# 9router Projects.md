# 9router Projects

Each of the following should have a different Issue & PR created to track the work distinctly (if there is an existing PR or draft that is fine to continue using ie: mcp filtering & 3575)

## MCP & Tool Filtering

> [https://github.com/decolua/9router/pull/3575](https://github.com/decolua/9router/pull/3575)

- nit/note - should combine the UI toggle for "Filter MCP" and BM25 config so its a single inline option
- by default leave max tools per turn as empty/0 (if empty, then bm25 disabled)
- besides a static default, maybe there should be an "average" or (high/med/low) setting.
- we should have dynamic sets based upon common operations or keywords. so that way we include what we should but leave out what we dont need when working on certain things. theres always some core system tools, but primarily mcp's like docker and playwright nad others that we can include or exclude based upon the context of what the agent is being asked to do.
- but tl;dr we need to make sure we have enough observability and metrics to accurately detect whether we're making tuning improvements or not. as well as via e2e tests to ensure we are not adversely affecting the processing speed or performance quality of our router.
- WHY: ANOTHER failure due to individual model weights on tool limits  -"Reason: Execution failed: Error: Failed to get response from the AI model; retried 5 times (total retry wait time: 30.60 seconds) Last error: 502 Cannot have more than 128 tools per request." outcome: may need to make the max dynamic even past filtering or higher limits (ie: 150 -> 128 ) so tl;dr this problem needs to be addressed to support all providers provably without regressions.

## Token Saver Visualizer

- create a "bar chart" on the Token saver ui that shows the distribution of token usage across different tools and operations. aggregate and average, but otherwise facet by Output, Input, Context, MCP, Tools, etc.

TL;DR express a good aggregate of everything we currently do or capture or should capture from our events/logs, but highlight and show the true compression impact by other elements and how effective they are (can estimate, but should strive to prove through automated e2e tests with feature flag or toggles for each respective component so that measurements through tests put the proof in the pudding.) So that way we really know how effective our compression or deferred  or cache usage or discard has effectively saved us.

```text
Context window 958.6k / 1M (96%)
Messages 907.8k 90.8%
System tools 27.5k 2.7%
System prompt 10.4k 1.0%
Skills 10k 1.0%
MCP tools 8.3k 0.8%
Custom agents 2.3k 0.2%
Memory files 783 0.1%
Autocompact buffer 33k 3.3%
Free space 0 0.0%
MCP tools (deferred) 141.6k —
System tools (deferred) 14.2k —
MCP tools 149.9k 326 
Memory files 783 2
Custom agents 2.3k 9
```

## Current compression features

- Compress tool output (RTK) - git/grep/ls/tree/logs → 60-90% fewer input tokens
- Compress context (Headroom) - Running - Compress prompts via /v1/compress before - routing to the model
- Compress LLM output (Caveman) - Terse-style system prompt → ~65% fewer output - tokens (up to 87%)
- Telegraphic, max compression - Lazy senior dev (Ponytail) → Bias the model toward minimal code: YAGNI, reuse stdlib, deletion over addition.
- MCP & BM25 filtering - Dynamically filter and rank tools based on relevance and context, improving efficiency and reducing unnecessary token usage (will eventually be merged - i hope so we can prioritize this last tbh)

## Copilot Tool Schema Normalization

[https://github.com/decolua/9router/pull/3665](https://github.com/decolua/9router/pull/3665)

- need e2e tests for all providers to check for OpenAI compatibility so that models work effectively for all supported scenarios (ie: when Copilot Chat is using the OpenAI API to connect to 9router). it only errored on a couple so hopefully is fixed with the one update I made on this branch/pr
- have to verify that all schema changes are correctly applied and that the normalization works across different providers and consumers that support OpenAI custom local endpoints (ie: claude cli, VSC Code/Continue.dev, etc.)

## Improvements

- Providers should be filterable (all sections, active, inactive/no connection, etc)
- Custom Providers (OpenAI/Anthropic Compatible) should have a "scan" option for common localhost/127.0.0.1 and local network addresses or common docker localhost setups (ollama ports, etc.) that run systems on local endpoints on common ports.

## Bugs

- Venice AI - failed: Provider test not supported
- Gemini CLI - currently not functional or all models are stale or tests fail to check properly.
- When a model is not found after 5 retries it should be added to a list of "stale" models and kept in a panel for optional "cleanup" or removal/de-ranking within combos. ex: Client Request Id: "Reason: Execution failed: Error: Failed to get response from the AI model; retried 5 times (total retry wait time: 30.88 seconds) Last error: 502 [gemini-cli/gemini-2.5-pro] [403]: HTTP 403 (reset after 1m 42s)"
- Default resync of quota should be increased to 5min interval default (to decrease strain of call and backend processing on these checks once more providers get fixed -- see quota fix scope below)

## Quotas

- Some of the below connected providers are missing in quota tracker or empty/null
  - Gemini CLI — connected, but quota detection returns 403 (used to show models & allocation available, likely endpoint change or no matching models)
  - Qoder — connected, but usage/quota fetch returns 401
  - Fireworks AI — connected, not tracked
  - Cohere — connected, not tracked
  - Groq — connected, not tracked
  - Mistral — connected, not tracked
  - OpenAI — connected, not tracked
  - SiliconFlow — connected, not tracked
  - Cerebras — connected, not tracked
  - NVIDIA NIM — connected, not tracked
  - Cloudflare — connected, not tracked
  - OpenRouter — connected, not tracked
  - Vercel AI Gateway — connected, but no credit allocation detected/unfunded (should say so not 403/error)

## Regression Protection

One big glaring issue is the lack of test coverage or framework. Constant churn on public PR's due to lack of sufficient controls and unit testing. we should strive to fix that. one of our existing PR's introduces a framework to ensure it doesnt break anything, but we should create a separate PR branch that works to improve the entire codebase test coverage to uncover bugs and catch issues before they get implemented as code in main.