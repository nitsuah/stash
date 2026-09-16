# Custom Endpoint wizard saves the endpoint as the group name and leaves models[].url empty

## Steps to reproduce

1. Open the GitHub Copilot Chat model picker in VS Code.
2. Select **Manage Models** and add a **Custom Endpoint** model using the **Chat Completions** API.
3. Enter `http://localhost:20128/v1` as the local OpenAI-compatible endpoint, choose a model, and save.
4. Select the newly created model and send any chat message.

## Actual result

The model appears in the picker, but the configuration persisted by the wizard leaves the required per-model URL empty. The first request fails before an HTTP request is made to the configured endpoint:

```text
TypeError: Cannot read properties of undefined (reading 'includes')
    at aFi (.../extensions/copilot/dist/extension.js:1598:8522)
    at iFi (.../extensions/copilot/dist/extension.js:1598:8255)
    at ED.createOpenAIEndPoint (.../extensions/copilot/dist/extension.js:1598:9407)
    at ED.provideTokenCount (.../extensions/copilot/dist/extension.js:1594:8256)
```

The wizard writes this malformed configuration:

```json
[
  {
    "name": "http://localhost:20128/v1",
    "vendor": "customendpoint",
    "apiType": "chat-completions",
    "models": [
      {
        "id": "or-free",
        "name": "or-free",
        "url": "",
        "toolCalling": true,
        "vision": true,
        "maxInputTokens": 128000,
        "maxOutputTokens": 16000
      }
    ]
  }
]
```

The Custom Endpoint schema declares `models[].url` as required and requires an `http(s)` URL. `createOpenAIEndPoint()` resolves this missing URL while constructing the endpoint and then calls `.includes()` on it.

## Expected result

The wizard should:

- Save the entered endpoint into `models[].url`.
- Use a human-readable provider label, rather than the URL, for the group `name`.
- Reject a blank model URL before saving.
- Show a clear configuration error for an existing malformed config instead of throwing an unhandled `TypeError`.

The configuration should instead resemble:

```json
[
  {
    "name": "9router",
    "vendor": "customendpoint",
    "apiType": "chat-completions",
    "models": [
      {
        "id": "or-free",
        "name": "or-free",
        "url": "http://localhost:20128/v1/chat/completions",
        "toolCalling": true,
        "vision": false,
        "maxInputTokens": 128000,
        "maxOutputTokens": 16000
      }
    ]
  }
]
```

## Workaround

Manually edit `%APPDATA%\Code\User\chatLanguageModels.json` and set a human-readable provider name plus a non-empty per-model URL:

```json
"name": "9router",
"url": "http://localhost:20128/v1/chat/completions"
```

After reloading VS Code, Copilot Chat successfully reaches the custom endpoint.

## Environment

- OS: Windows
- VS Code: 1.135.0
- GitHub Copilot Chat: 0.63.0
- Endpoint type: local OpenAI-compatible Chat Completions endpoint
- Example router: https://github.com/decolua/9router
- No API keys are included in this report.

## Scope

A separate 9router investigation found free-provider fallback and tool-schema compatibility issues under Copilot Agent's large tool payload. Those are distinct from this issue: the blank `models[].url` causes the initial `.includes()` crash before Copilot sends any request to the configured endpoint.

[Issue](https://github.com/microsoft/vscode/issues/333701)
