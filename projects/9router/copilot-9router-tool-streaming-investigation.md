# 9router: Function Tool Schema Compatibility in Fallback Combos

## Defect

9router accepts OpenAI-compatible chat requests and forwards function tools to each candidate in a fallback combo. For already OpenAI-shaped tools, the OpenAI-to-OpenAI path preserves `tools[].function.parameters` unchanged.

That is unsafe for a heterogeneous provider gateway such as OpenRouter: its downstream providers do not all support the same JSON Schema dialect.

## Observed failure

An OpenAI-compatible agent request was routed through the `or-free` fallback combo to an OpenRouter/Cohere model. The upstream rejected a function definition with HTTP 400:

```text
invalid function at tools[1].function:
invalid 'parameters' provided: pattern must be a valid regex
```

The error proves the schema accepted by the client was not accepted by this OpenRouter backend. The exact rejected pattern was not captured, so this does not yet prove whether it was malformed, used an unsupported regex dialect, or was otherwise disallowed by Cohere.

## Why this belongs in 9router

9router deliberately sends a single logical request through multiple providers and models. It therefore owns the provider-boundary compatibility work:

1. A combo may select a backend with stricter tool-schema validation than the client.
2. The current OpenAI-compatible passthrough does not adapt schema constraints for that backend.
3. A provider rejection triggers another fallback attempt, increasing latency and making an agent turn less reliable.

The defect is not that function tools are unsupported. It is that generic tool capability alone does not guarantee support for every JSON Schema feature in a tool definition.

## Isolated draft fix

- Branch: `fix/copilot-tool-schema-streaming`
- Draft PR: https://github.com/decolua/9router/pull/3665

The draft implements two scoped improvements.

### Function tools affect combo selection

Requests containing OpenAI `type: "function"` tools now require the `tools` capability during combo ordering. Previously, only `web_search` influenced the requirement set, so a function-tool request was treated like a text-only request for routing purposes.

### OpenRouter schema compatibility hook

A reusable provider compatibility hook runs before dispatch. For OpenRouter only, it recursively checks JSON Schema `pattern` values:

- valid JavaScript regex patterns are preserved;
- malformed regex patterns are removed;
- property names called `pattern` are preserved;
- nested schemas are handled;
- non-OpenRouter providers receive the original tools object unchanged.

This is a conservative first guard. It prevents malformed JavaScript regexes from reaching stricter OpenRouter backends. It does not claim to solve every provider-specific regex dialect incompatibility; a rejected real request must be captured to extend the normalizer safely.

## Validation

- Syntax checks passed for all changed source modules.
- Direct assertions passed for valid-pattern preservation, malformed-pattern removal, nested schema handling, immutable input behavior, and no-op behavior outside OpenRouter.
- A Docker production build completed successfully.
- The isolated image `9router:copilot-tool-schema-streaming` is deployed locally and `http://localhost:20128/api/version` returns HTTP 200.

Regression tests are included. The repository's Vitest config could not be executed from a clean checkout because Vitest is not declared in `package.json`; this is a pre-existing test-environment issue.

## Follow-up needed

Capture the rejected tool definition in controlled request-detail logging, with secrets redacted. That will distinguish malformed regexes from regex-dialect or wider JSON Schema compatibility gaps and supports adding provider-specific rules without degrading valid client tool schemas.

## Troubleshooting note

If Copilot Chat fails before 9router receives any request with `Cannot read properties of undefined (reading 'includes')`, check its Custom Endpoint configuration. A separate Copilot wizard defect can save a blank `models[].url`; that client-side configuration error is unrelated to this 9router defect.
