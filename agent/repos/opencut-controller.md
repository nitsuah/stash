# opencut-controller — MCP Server for OpenCut Video Editor

**Last Validated:** 2026-06-09 | Initial vault entry
**Repo:** https://github.com/nitsuah/opencut-controller (forked from JXUE0/opencut-controller)
**npm:** https://www.npmjs.com/package/opencut-controller
**Branch convention:** `pmo/opencut-controller/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| MCP server (stdio) | PASS | `bun run src/index.ts` connects to local OpenCut editor |
| MCP server (HTTP) | PASS | `http://localhost:3002/mcp` for n8n / remote clients |
| Playwright browsers | PASS | Auto-installed via `postinstall` script |
| Docs baseline | PASS | README, README.es, PROMPTS present |

---

## Stack

- **Protocol:** Model Context Protocol (MCP) v1.29.0
- **Runtime:** Bun (≥1.3)
- **Browser automation:** Playwright (Chromium)
- **Transport:** stdio (Claude Desktop) or HTTP Streamable (n8n, remote)
- **Tools:** 161 granular MCP tools across 17 categories

---

## Key Features

- Full programmatic control over OpenCut: scenes, timeline, effects, keyframes, media, text, audio, canvas, export
- `opencut://projects`, `opencut://editor/state`, `opencut://timeline/tracks` resources for live LLM context
- Pre-built prompts: `create_intro_video`, `add_background_music`, `apply_transition`
- Requires local OpenCut editor with `patch-editor.ts` applied

---

## PMO Findings

- Requires OpenCut editor running locally with patch applied — production `opencut.app` won't work.
- TypeScript type checking via `bun run build` (`tsc --noEmit`).
- Spanish README (`README.es.md`) included for international contributors.

---

## Priority Focus

1. Keep patch script aligned with OpenCut upstream changes after major releases.
2. Validate all 161 tools against current OpenCut UI after upstream updates.
3. Add integration tests for the 5 most-used tool categories.

---

## Key Commands

```powershell
# Install (Playwright browsers auto-download)
bun install

# Patch local OpenCut editor (required once)
bun run scripts/patch-editor.ts ../opencut

# Start MCP server (stdio — for Claude Desktop)
bun run src/index.ts

# Start MCP server (HTTP — for n8n / remote)
$env:TRANSPORT_TYPE="http"; $env:PORT="3002"; bun run src/index.ts

# Type check
bun run build
```

---

## Active PMO

See ROADMAP.md in linked opencut-controller skill for current priorities. Also see [[projects/Intake]] for active sessions.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/opencut-controller/README|README]] · [[repos/opencut-controller/PROMPTS|PROMPTS]] · [[repos/opencut-controller/README.es|README (Español)]]

## Related
- [[repos/opencut|opencut]] — the editor this controller wraps via Playwright
