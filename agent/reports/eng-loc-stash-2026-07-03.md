# ENG LOC Report: stash

> 🧭 [[repos/stash|stash]] · ← [[reports/eng-loc-stash-2026-06-25|2026-06-25]] · [[reports/eng-loc-stash-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** stash (stash)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 87227 | `.obsidian/plugins/obsidian-local-rest-api/main.js` | Unused function (heuristic): getDunder; Unused function (heuristic): createAlias; Unused function (heuristic): addRoute; Unused function (heuristic): addPublicRoute; Unused function (heuristic): addMcpTool; Unused function (heuristic): unregister; Unused function (heuristic): setKey; Unused function (heuristic): deepPartial; Unused function (heuristic): strictImplement; Unused function (heuristic): removeRequestHandler; Unused function (heuristic): removeNotificationHandler; Unused function (heuristic): getClientCapabilities; Unused function (heuristic): getClientVersion; Unused function (heuristic): createElicitationCompletionNotifier; Unused function (heuristic): registerResource; Unused function (heuristic): registerPrompt; Unused function (heuristic): valueIsSaneTruthy; Unused function (heuristic): onunload; Repeated block (2 occurrences, 10+ lines):       var rval;
      if (count) {
        count = Math.min(this.length(), count... |
| 87227 | `agent/.obsidian/plugins/obsidian-local-rest-api/main.js` | Unused function (heuristic): getDunder; Unused function (heuristic): createAlias; Unused function (heuristic): addRoute; Unused function (heuristic): addPublicRoute; Unused function (heuristic): addMcpTool; Unused function (heuristic): unregister; Unused function (heuristic): setKey; Unused function (heuristic): deepPartial; Unused function (heuristic): strictImplement; Unused function (heuristic): removeRequestHandler; Unused function (heuristic): removeNotificationHandler; Unused function (heuristic): getClientCapabilities; Unused function (heuristic): getClientVersion; Unused function (heuristic): createElicitationCompletionNotifier; Unused function (heuristic): registerResource; Unused function (heuristic): registerPrompt; Unused function (heuristic): valueIsSaneTruthy; Unused function (heuristic): onunload; Repeated block (2 occurrences, 10+ lines):       var rval;
      if (count) {
        count = Math.min(this.length(), count... |
| 30536 | `agent/.obsidian/plugins/smart-connections/main.js` | Unused function (heuristic): add_settings_listeners; Unused function (heuristic): remove_embeddings; Unused function (heuristic): get_block_by_line; Unused function (heuristic): get_unseen_notification_count; Unused function (heuristic): onChooseSuggestion; Unused function (heuristic): remove_by_path; Unused function (heuristic): onChooseItem; Unused function (heuristic): getViewType; Unused function (heuristic): get_connections_list_item_options; Unused function (heuristic): onunload; Repeated block (2 occurrences, 10+ lines):     main.smart_settings = smart_settings;
    Object.defineProperty(main, "setti... |
| 28966 | `agent/.obsidian/plugins/smart-context/main.js` | Unused function (heuristic): add_settings_listeners; Unused function (heuristic): get_rand; Unused function (heuristic): update_many; Unused function (heuristic): refresh_actions; Unused function (heuristic): remove_embeddings; Unused function (heuristic): get_block_by_line; Unused function (heuristic): get_unseen_notification_count; Unused function (heuristic): remove_by_path; Unused function (heuristic): onChooseItem; Unused function (heuristic): getViewType; Unused function (heuristic): register_item_views; Unused function (heuristic): queueMicrotask; Unused function (heuristic): get_relative_path; Unused function (heuristic): showStatsNotice; Repeated block (2 occurrences, 10+ lines):     main.smart_settings = smart_settings;
    Object.defineProperty(main, "setti... |
| 26250 | `agent/.obsidian/plugins/smart-lookup/main.js` | Unused function (heuristic): add_settings_listeners; Unused function (heuristic): get_rand; Unused function (heuristic): update_many; Unused function (heuristic): refresh_actions; Unused function (heuristic): remove_embeddings; Unused function (heuristic): get_block_by_line; Unused function (heuristic): get_unseen_notification_count; Unused function (heuristic): onChooseSuggestion; Unused function (heuristic): remove_by_path; Unused function (heuristic): onChooseItem; Unused function (heuristic): getViewType; Unused function (heuristic): onunload; Repeated block (2 occurrences, 10+ lines):     main.smart_settings = smart_settings;
    Object.defineProperty(main, "setti... |
| 2436 | `.obsidian/plugins/nexus/main.js` | Repeated block (2 occurrences, 10+ lines): 
TWO MODES:
- Discovery (default): Search all memory across a workspace. Best fo... |
| 2436 | `agent/.obsidian/plugins/nexus/main.js` | Repeated block (2 occurrences, 10+ lines): 
TWO MODES:
- Discovery (default): Search all memory across a workspace. Best fo... |
| 1051 | `atlassian/jira/validate_project.py` | Unused function (heuristic): __init__ |
| 562 | `cloud/aws/examples.py` | Unused function (heuristic): list_objects; Unused function (heuristic): invoke_lambda; Unused function (heuristic): list_rds_snapshots; Unused function (heuristic): get_stack_outputs |
| 520 | `.obsidian/plugins/mcp-tools/main.js` | — |
| 520 | `agent/.obsidian/plugins/mcp-tools/main.js` | — |

## Small Files (<= 30 lines) — Merge Candidates

_None_
