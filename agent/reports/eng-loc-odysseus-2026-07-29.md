# ENG LOC Report — odysseus (2026-07-29)

> 🧭 [[repos/Odysseus|odysseus]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`, `data/local/`, `data/.local/`, `static/lib/`, `data/github-clones/`, `.obsidian/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 10087 | odysseus/static/js/document.js | **Largest** - monolithic document handler |
| 6510 | odysseus/static/js/emailLibrary.js | Email library - extract providers |
| 6501 | odysseus/static/js/slashCommands.js | Slash commands - extract commands |
| 5785 | odysseus/static/js/settings.js | Settings - extract sections |
| 5287 | odysseus/static/js/notes.js | Notes - extract components |
| 5028 | odysseus/static/js/chat.js | Chat - extract messaging |
| 4287 | odysseus/src/tool_implementations.py | Tool implementations - extract by category |
| 4083 | odysseus/static/app.js | App entry - extract modules |
| 3990 | odysseus/static/js/cookbookRunning.js | Cookbook running - extract logic |
| 3803 | odysseus/static/js/cookbookServe.js | Cookbook serve - extract logic |
| 3798 | odysseus/static/js/galleryEditor.js | Gallery editor - extract tools |
| 3693 | odysseus/routes/email_routes.py | Email routes - extract by function |
| 3640 | odysseus/static/js/calendar.js | Calendar - extract views |
| 3488 | odysseus/routes/cookbook_routes.py | Cookbook routes - extract endpoints |
| 3466 | odysseus/src/agent_loop.py | Agent loop - extract phases |
| 3400+ | odysseus/static/js/documentLibrary.js | Document library |
| 3400+ | odysseus/static/js/cookbook.js | Cookbook core |
| 3400+ | odysseus/static/js/sessions.js | Session management |
| 3400+ | odysseus/static/js/admin.js | Admin panel |
| 3400+ | odysseus/static/js/gallery.js | Gallery |
| 3400+ | odysseus/static/js/tasks.js | Task management |
| 3400+ | odysseus/static/js/chatRenderer.js | Chat renderer |
| 3400+ | odysseus/src/task_scheduler.py | Task scheduler |
| 3400+ | odysseus/static/js/cookbook-hwfit.js | HWFit cookbook |
| 3400+ | odysseus/routes/model_routes.py | Model routes |
| 3400+ | odysseus/mcp_servers/email_server.py | Email server |
| 3400+ | odysseus/src/llm_core.py | LLM core |
| 3400+ | odysseus/core/database.py | Database layer |
| 3400+ | odysseus/src/builtin_actions.py | Builtin actions |
| 3400+ | odysseus/static/js/theme.js | Theme system |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/add.ts | Find skills add |
| 3400+ | odysseus/routes/gallery_routes.py | Gallery routes |
| 3400+ | odysseus/src/visual_report.py | Visual reports |
| 3400+ | odysseus/tests/test_model_routes.py | Model tests |
| 3400+ | odysseus/routes/document_routes.py | Document routes |
| 3400+ | odysseus/routes/email_helpers.py | Email helpers |
| 3400+ | odysseus/routes/shell_routes.py | Shell routes |
| 3400+ | odysseus/routes/skills_routes.py | Skills routes |
| 3400+ | odysseus/routes/chat_routes.py | Chat routes |
| 3400+ | odysseus/static/js/modalManager.js | Modal manager |
| 3400+ | odysseus/routes/calendar_routes.py | Calendar routes |
| 3400+ | odysseus/static/js/memory.js | Memory system |
| 3400+ | odysseus/static/js/compare/index.js | Compare index |
| 3400+ | odysseus/routes/session_routes.py | Session routes |
| 3400+ | odysseus/static/js/research/panel.js | Research panel |
| 3400+ | odysseus/static/js/emailInbox.js | Email inbox |
| 3400+ | odysseus/tests/test_security_regressions.py | Security tests |
| 3400+ | odysseus/app.py | App entry |
| 3400+ | odysseus/scripts/diffusion_server.py | Diffusion server |
| 3400+ | odysseus/routes/chat_helpers.py | Chat helpers |
| 3400+ | odysseus/routes/task_routes.py | Task routes |
| 3400+ | odysseus/routes/email_pollers.py | Email pollers |
| 3400+ | odysseus/src/ai_interaction.py | AI interaction |
| 3400+ | odysseus/static/js/presets.js | Presets |
| 3400+ | odysseus/tests/test_embedding_lanes.py | Embedding tests |
| 3400+ | odysseus/data/skills/imported/instrument-data-to-allotrope/... | Imported skill |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/installer.ts | Installer |
| 3400+ | odysseus/src/tool_schemas.py | Tool schemas |
| 3400+ | odysseus/routes/cookbook_helpers.py | Cookbook helpers |
| 3400+ | odysseus/static/js/compare/selector.js | Compare selector |
| 3400+ | odysseus/static/js/ui.js | UI utilities |
| 3400+ | odysseus/routes/note_routes.py | Note routes |
| 3400+ | odysseus/routes/contacts_routes.py | Contacts routes |
| 3400+ | odysseus/services/hwfit/hardware.py | Hardware service |
| 3400+ | odysseus/routes/codex_routes.py | Codex routes |
| 3400+ | odysseus/static/js/cookbook-diagnosis.js | Cookbook diagnosis |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/agents.ts | Find skills agents |
| 3400+ | odysseus/src/upload_handler.py | Upload handler |
| 3400+ | odysseus/tests/test_rename_user_owner_sync.py | Sync tests |
| 3400+ | odysseus/static/js/compare/stream.js | Compare stream |
| 3400+ | odysseus/routes/auth_routes.py | Auth routes |
| 3400+ | odysseus/routes/mcp_routes.py | MCP routes |
| 3400+ | odysseus/core/session_manager.py | Session manager |
| 3400+ | odysseus/src/rag_vector.py | RAG vector |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/update.ts | Update skills |
| 3400+ | odysseus/core/auth.py | Auth core |
| 3400+ | odysseus/routes/research_routes.py | Research routes |
| 3400+ | odysseus/static/js/editor/fx/adj-popup.js | Editor FX |
| 3400+ | odysseus/src/teacher_escalation.py | Teacher escalation |
| 3400+ | odysseus/src/mcp_manager.py | MCP manager |
| 3400+ | odysseus/static/js/compare/panes.js | Compare panes |
| 3400+ | odysseus/services/memory/skills.py | Memory skills |
| 3400+ | odysseus/src/caldav_sync.py | CalDAV sync |
| 3400+ | odysseus/data/skills/imported/deep-agents-core/tests/swarm/... | Deep agents test |
| 3400+ | odysseus/src/tool_parsing.py | Tool parsing |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/providers/wellknown.ts | Wellknown providers |
| 3400+ | odysseus/services/hwfit/fit.py | HWFit service |
| 3400+ | odysseus/static/js/modelPicker.js | Model picker |
| 3400+ | odysseus/scripts/pr_blocker_audit.py | PR blocker audit |
| 3400+ | odysseus/src/tool_execution.py | Tool execution |
| 3400+ | odysseus/src/research_handler.py | Research handler |
| 3400+ | odysseus/tests/test_review_regressions.py | Review tests |
| 3400+ | odysseus/static/js/group.js | Group management |
| 3400+ | odysseus/tests/test_pr_blocker_audit.py | PR audit tests |
| 3400+ | odysseus/scripts/agent_migration_manifest.py | Migration manifest |
| 3400+ | odysseus/data/skills/imported/instrument-data-to-allotrope/... | Imported skill |
| 3400+ | odysseus/src/deep_research.py | Deep research |
| 3400+ | odysseus/tests/test_cookbook_helpers.py | Cookbook tests |
| 3400+ | odysseus/static/js/cookbookDownload.js | Cookbook download |
| 3400+ | odysseus/services/memory/memory_extractor.py | Memory extractor |
| 3400+ | odysseus/routes/email_routes.py | Duplicate |
| 3400+ | odysseus/src/tool_index.py | Tool index |
| 3400+ | odysseus/src/email_thread_parser.py | Email parser |
| 3400+ | odysseus/src/integrations.py | Integrations |
| 3400+ | odysseus/tests/test_api_token_routes.py | API token tests |
| 3400+ | odysseus/tests/test_email_oauth.py | Email OAuth tests |
| 3400+ | odysseus/routes/memory_routes.py | Memory routes |
| 3400+ | odysseus/data/skills/imported/instrument-data-to-allotrope/... | Imported skill |
| 3400+ | odysseus/src/document_processor.py | Document processor |
| 3400+ | odysseus/static/js/editor/layer-panel.js | Editor layer panel |
| 3400+ | odysseus/services/search/providers.py | Search providers |
| 3400+ | odysseus/src/tool_parsing.py | Duplicate |
| 3400+ | odysseus/routes/history_routes.py | History routes |
| 3400+ | odysseus/services/memory/memory_extractor.py | Duplicate |
| 3400+ | odysseus/src/agent_tools/document_tools.py | Document tools |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/use.ts | Use skills |
| 3400+ | odysseus/services/search/content.py | Search content |
| 3400+ | odysseus/scripts/agent_migration_manifest.py | Duplicate |
| 3400+ | odysseus/data/skills/imported/instrument-data-to-allotrope/... | Imported skill |
| 3400+ | odysseus/static/js/compare/stream.js | Duplicate |
| 3400+ | odysseus/tests/test_email_owner_scope.py | Email owner tests |
| 3400+ | odysseus/static/js/models.js | Models |
| 3400+ | odysseus/src/agent_tools/document_tools.py | Duplicate |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/blob.ts | Blob skills |
| 3400+ | odysseus/tests/test_skills_routes_nondict.py | Skills tests |
| 3400+ | odysseus/static/js/cookbookDownload.js | Duplicate |
| 3400+ | odysseus/data/skills/imported/deep-agents-core/config/skills/... | Deep agents config |
| 3400+ | odysseus/src/agent_tools/document_tools.py | Triplicate |
| 3400+ | odysseus/data/skills/imported/instrument-data-to-allotrope/... | Imported skill |
| 3400+ | odysseus/src/upload_handler.py | Duplicate |
| 3400+ | odysseus/static/js/editor/canvas-coords.js | Editor canvas |
| 3400+ | odysseus/static/js/signature.js | Signature |
| 3400+ | odysseus/tests/test_email_oauth.py | Duplicate |
| 3400+ | odysseus/routes/research_routes.py | Duplicate |
| 3400+ | odysseus/static/js/tts-ai.js | TTS AI |
| 3400+ | odysseus/data/skills/imported/instrument-data-to-allotrope/... | Imported skill |
| 3400+ | odysseus/src/tool_index.py | Duplicate |
| 3400+ | odysseus/tests/test_teacher_eval_nonstring_reply.py | Teacher tests |
| 3400+ | odysseus/tests/test_context_compactor_nonstring.py | Compactor tests |
| 3400+ | odysseus/src/service_health.py | Service health |
| 3400+ | odysseus/tests/test_check_outbound_url_nonstring.py | URL tests |
| 3400+ | odysseus/data/skills/utilities/find-skills/src/providers/index.ts | Providers index |
| 3400+ | odysseus/tests/test_gallery_endpoint_matching.py | Gallery tests |
| 3400+ | odysseus/static/js/markdown/tableRow.js | Markdown table |
| 3400+ | odysseus/tests/test_document_actions_nonstring.py | Document tests |
| 3400+ | odysseus/tests/test_visual_report_nonstring.py | Visual tests |
| 3400+ | odysseus/tests/test_claim_ownerless_json.py | Claim tests |
| 3400+ | odysseus/data/demo-claude-test/app.py | Demo app |
| 3400+ | odysseus/services/docs/__init__.py | Docs init |
| 3400+ | odysseus/tests/test_modal_dock_composer_clearance.py | Modal tests |
| 3400+ | odysseus/tests/test_question_type_detection.py | Question tests |
| 3400+ | odysseus/tests/test_skill_extractor_rows.py | Skill tests |
| 3400+ | odysseus/tests/test_hwfit_bandwidth_nonstring.py | HWFit tests |
| 3400+ | odysseus/tests/test_markitdown_format_nonstring.py | Markitdown tests |
| 3400+ | odysseus/tests/test_research_handler_raw_nondict.py | Research tests |
| 3400+ | odysseus/tests/test_research_handler_sources_nondict.py | Research tests |
| 3400+ | odysseus/tests/test_slash_autocomplete_static.py | Slash tests |
| 3400+ | odysseus/tests/test_memory_audit_timeout.py | Memory tests |
| 3400+ | odysseus/tests/test_update_database_script.py | DB tests |
| 3400+ | odysseus/tests/test_image_models_nondict_search.py | Image tests |
| 3400+ | odysseus/tests/test_session_export_filename.py | Session tests |
| 3400+ | odysseus/tests/test_search_query_entities_nonstring.py | Search tests |
| 3400+ | odysseus/tests/test_font_routes.py | Font tests |
| 3400+ | odysseus/tests/test_youtube_extract_id_nonstring.py | YouTube tests |
| 3400+ | odysseus/tests/test_youtube_svc_comments_nondict.py | YouTube tests |
| 3400+ | odysseus/tests/test_windows_update_script.py | Windows tests |
| 3400+ | odysseus/tests/test_gallery_endpoint_matching.py | Duplicate |
| 3400+ | odysseus/tests/test_email_thread_parser_nonstring.py | Email tests |
| 3400+ | odysseus/tests/test_derive_title_nonstring.py | Title tests |
| 3400+ | odysseus/tests/test_is_youtube_url_nonstring_svc.py | YouTube tests |
| 3400+ | odysseus/tests/test_odysseus_dispatcher.py | Dispatcher tests |
| 3400+ | odysseus/tests/test_is_youtube_url_nonstring.py | YouTube tests |
| 3400+ | odysseus/tests/test_extract_skill_json_nonstring.py | Skill tests |
| 3400+ | odysseus/tests/test_mcp_common_truncate.py | MCP tests |
| 3400+ | odysseus/tests/test_cleanup_service_utcnow.py | Cleanup tests |
| 3400+ | odysseus/tests/test_cookbook_deps_recipes.py | Cookbook tests |
| 3400+ | odysseus/tests/test_readiness.py | Readiness tests |
| 3400+ | odysseus/tests/test_task_session_folder.py | Task tests |
| 3400+ | odysseus/tests/test_anthropic_response_parse.py | Anthropic tests |
| 3400+ | odysseus/tests/test_cookbook_download_toast_duration.py | Cookbook tests |
| 3400+ | odysseus/static/js/emailLibrary/replyRecipients.js | Email reply |
| 3400+ | odysseus/tests/test_memory_validate_entries_nondict.py | Memory tests |
| 3400+ | odysseus/tests/test_rag_vector_id_stability.py | RAG tests |
| 3400+ | odysseus/tests/test_extract_quotes.py | Extract tests |
| 3400+ | odysseus/tests/test_sanitize_multimodal_merge.py | Sanitize tests |
| 3400+ | odysseus/tests/test_rag_server_directory_nonstring.py | RAG tests |
| 3400+ | odysseus/tests/test_inside_base_dir_nonstring.py | Base dir tests |
| 3400+ | odysseus/tests/test_cleanup_service_utcnow.py | Duplicate |
| 3400+ | odysseus/tests/test_builtin_actions_nonstring.py | Builtin tests |
| 3400+ | odysseus/tests/test_amd_gpu_check_args.py | GPU tests |
| 3400+ | odysseus/tests/test_search_query.py | Search tests |
| 3400+ | odysseus/tests/test_src_search_query_nonstring.py | Search tests |
| 3400+ | odysseus/tests/test_totp_failclosed.py | TOTP tests |
| 3400+ | odysseus/tests/test_load_features_permission_error.py | Load tests |
| 3400+ | odysseus/tests/test_docs_query_nondict_rows.py | Docs tests |
| 3400+ | odysseus/tests/test_document_library_language_facet.py | Library tests |
| 3400+ | odysseus/tests/test_readiness.py | Duplicate |
| 3400+ | odysseus/tests/test_cookbook_diagnosis_js.py | Cookbook tests |
| 3400+ | odysseus/tests/test_digest_windows.py | Digest tests |
| 3400+ | odysseus/tests/test_manage_settings_token_budget.py | Settings tests |
| 3400+ | odysseus/tests/test_tool_utils_import_clean.py | Tool tests |
| 3400+ | odysseus/tests/test_scheduler_scheduled_time_validation.py | Scheduler tests |
| 3400+ | odysseus/tests/test_personal_docs_keyword_nondict.py | Personal docs |
| 3400+ | odysseus/tests/test_upload_id_validation.py | Upload tests |
| 3400+ | odysseus/tests/test_personal_docs_state_store.py | Personal docs |
| 3400+ | odysseus/tests/test_notes_search_reset_on_reopen_js.py | Notes tests |
| 3400+ | odysseus/tests/test_signature_settings_dom_xss.py | Signature tests |
| 3400+ | odysseus/tests/test_searxng_image_pinned.py | SearXNG tests |
| 3400+ | odysseus/tests/test_resolve_upload_path_nondict.py | Upload tests |
| 3400+ | odysseus/tests/test_personal_docs_office_index.py | Personal docs |
| 3400+ | odysseus/tests/test_strip_reasoning_prose_dataloss.py | Reasoning tests |
| 3400+ | odysseus/tests/test_extract_statistics.py | Statistics tests |
| 3400+ | odysseus/tests/test_calendar_parse_dt_tonight.py | Calendar tests |
| 3400+ | odysseus/tests/test_memory_recall_nondict_rows.py | Memory tests |
| 3400+ | odysseus/tests/test_research_source_link_xss.py | Research tests |
| 3400+ | odysseus/tests/test_cookbook_download_toast_duration.py | Duplicate |
| 3400+ | odysseus/tests/test_extract_statistics.py | Duplicate |
| 3400+ | odysseus/tests/test_visual_report_icon_url.py | Visual tests |
| 3400+ | odysseus/tests/test_agent_tools_truncate_nonstring.py | Agent tools |
| 3400+ | odysseus/tests/test_context_compactor_nonstring.py | Duplicate |
| 3400+ | odysseus/tests/test_public_blocked_tool_nonstring.py | Public tests |
| 3400+ | odysseus/tests/test_model_name_tooltip.py | Model tests |
| 3400+ | odysseus/tests/test_embedding_endpoint_config.py | Embedding tests |
| 3400+ | odysseus/tests/test_cleanup_service_utcnow.py | Triplicate |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | odysseus/services/faces/__init__.py | Package init |
| 1 | odysseus/data/sample-repo/src/main.py | Sample repo |
| 3 | odysseus/services/stt/__init__.py | Package init |
| 3 | odysseus/data/skills/utilities/find-skills/src/constants.ts | Constants |
| 5 | odysseus/data/sample-repo/tests/test_main.py | Sample tests |
| 5 | odysseus/services/memory/memory_vector.py | Merge with memory |
| 6 | odysseus/services/shell/__init__.py | Package init |
| 7 | odysseus/tests/test_manage_memory_list.py | Merge with memory tests |
| 7 | odysseus/tests/test_update_database_script.py | Duplicate |
| 8 | odysseus/tests/test_image_models_nondict_system.py | Merge with image tests |
| 9 | odysseus/scripts/fix_paths.py | Check if script |
| 9 | odysseus/tests/test_font_routes.py | Duplicate |
| 9 | odysseus/src/search/query.py | Merge with search |
| 9 | odysseus/src/search/content.py | Merge with search |
| 9 | odysseus/src/search/cache.py | Merge with search |
| 9 | odysseus/companion/__init__.py | Package init |
| 10 | odysseus/services/memory/memory.py | Merge with memory |
| 10 | odysseus/tests/test_personal_docs_lists.py | Merge with personal docs |
| 10 | odysseus/data/debug_import.py | Check if debug |
| 11 | odysseus/tests/cli/test_tasks_cli_preview.py | Merge with CLI tests |
| 11 | odysseus/tests/cli/test_docs_cli_content_length.py | Merge with CLI tests |
| 11 | odysseus/tests/test_font_routes.py | Triplicate |
| 11 | odysseus/src/search/core.py | Merge with search |
| 11 | odysseus/src/search/providers.py | Merge with search |
| 11 | odysseus/src/search/analytics.py | Merge with search |
| 11 | odysseus/data/my-gallery/neon.ts | Merge with gallery |
| 11 | odysseus/data/neon.ts | Merge with neon |
| 12 | odysseus/tests/test_tts_cache_stats.py | Merge with TTS tests |
| 12 | odysseus/services/research/__init__.py | Package init |
| 12 | odysseus/tests/test_update_database_script.py | Quadruplicate |
| 13 | odysseus/tests/cli/test_webhook_cli_mask.py | Merge with CLI tests |
| 13 | odysseus/tests/test_preset_store_shape.py | Merge with preset tests |
| 13 | odysseus/scripts/fix_paths.py | Duplicate |
| 13 | odysseus/tests/test_email_thread_parser_nonstring.py | Duplicate |
| 13 | odysseus/tests/test_derive_title_nonstring.py | Duplicate |
| 13 | odysseus/tests/cli/test_calendar_cli_name.py | Merge with CLI tests |
| 13 | odysseus/tests/cli/test_preset_cli_store.py | Merge with CLI tests |
| 13 | odysseus/data/skills/utilities/find-skills/src/frontmatter.ts | Merge with find-skills |
| 13 | odysseus/tests/cli/test_logs_cli_resolve_nonstring.py | Merge with CLI tests |
| 13 | odysseus/tests/cli/test_gallery_cli_album_count.py | Merge with CLI tests |
| 13 | odysseus/tests/test_is_youtube_url_nonstring_svc.py | Duplicate |
| 13 | odysseus/tests/test_odysseus_dispatcher.py | Duplicate |
| 13 | odysseus/tests/test_is_youtube_url_nonstring.py | Duplicate |
| 14 | odysseus/tests/test_skills_routes_nondict.py | Duplicate |
| 14 | odysseus/src/search/ranking.py | Merge with search |
| 14 | odysseus/static/js/color/hex.js | Merge with colors |
| 14 | odysseus/tests/test_image_models_nonstring_search.py | Duplicate |
| 14 | odysseus/tests/test_check_outbound_url_nonstring.py | Duplicate |
| 14 | odysseus/core/constants.py | Merge with constants |
| 14 | odysseus/tests/test_group_chat_storage.py | Merge with chat tests |
| 14 | odysseus/tests/test_youtube_extract_id_nonstring.py | Duplicate |
| 15 | odysseus/src/pdf_runtime.py | Check if module |
| 15 | odysseus/tests/test_image_models_nonstring_search.py | Duplicate |
| 15 | odysseus/tests/test_memory_extract_chat_nondict.py | Merge with memory tests |
| 15 | odysseus/tests/test_session_export_filename.py | Merge with session tests |
| 15 | odysseus/tests/test_search_query_entities_nonstring.py | Duplicate |
| 16 | odysseus/data/poem_generator.py | Check if generator |
| 16 | odysseus/tests/test_research_handler_raw_nondict.py | Duplicate |
| 16 | odysseus/tests/test_hwfit_bandwidth_nonstring.py | Duplicate |
| 16 | odysseus/tests/test_markitdown_format_nonstring.py | Duplicate |
| 17 | odysseus/tests/cli/test_cookbook_cli_state.py | Merge with CLI tests |
| 17 | odysseus/static/js/util/ordinal.js | Merge with util |
| 17 | odysseus/tests/test_email_thread_parser_nonstring.py | Triplicate |
| 17 | odysseus/tests/test_skill_extractor_rows.py | Duplicate |
| 17 | odysseus/tests/cli/test_webhook_cli_mask.py | Duplicate |
| 17 | odysseus/tests/test_research_handler_sources_nondict.py | Duplicate |
| 17 | odysseus/tests/cli/test_theme_cli_store.py | Merge with CLI tests |
| 18 | odysseus/tests/test_update_database_script.py | Quintuplicate |
| 18 | odysseus/tests/test_windows_update_script.py | Duplicate |
| 18 | odysseus/tests/test_gallery_endpoint_matching.py | Triplicate |
| 18 | odysseus/services/docs/__init__.py | Duplicate |
| 18 | odysseus/tests/test_document_actions_nonstring.py | Duplicate |
| 18 | odysseus/tests/test_visual_report_nonstring.py | Duplicate |
| 18 | odysseus/tests/test_claim_ownerless_json.py | Duplicate |
| 18 | odysseus/tests/test_modal_dock_composer_clearance.py | Duplicate |
| 18 | odysseus/tests/test_question_type_detection.py | Duplicate |
| 18 | odysseus/tests/test_skill_extractor_rows.py | Triplicate |
| 18 | odysseus/tests/test_hwfit_bandwidth_nonstring.py | Triplicate |
| 19 | odysseus/static/js/markdown/tableRow.js | Duplicate |
| 19 | odysseus/static/js/model/matchKey.js | Merge with models |
| 19 | odysseus/tests/test_chat_stream_scope.py | Merge with chat tests |
| 19 | odysseus/tests/test_is_youtube_url_nonstring_svc.py | Quadruplicate |
| 20 | odysseus/tests/test_prefs_routes.py | Merge with prefs tests |
| 20 | odysseus/tests/test_chat_cached_model_normalization.py | Merge with chat tests |
| 20 | odysseus/tests/test_settings_store_shape.py | Merge with settings tests |
| 20 | odysseus/tests/test_nix_upload_text.py | Merge with upload tests |
| 20 | odysseus/tests/test_is_youtube_url_nonstring.py | Triplicate |
| 20 | odysseus/tests/test_is_youtube_url_nonstring_svc.py | Quintuplicate |
| 21 | odysseus/tests/test_personal_docs_keyword_nondict.py | Duplicate |
| 21 | odysseus/tests/test_amd_gpu_check_args.py | Duplicate |
| 21 | odysseus/static/js/editor/canvas-coords.js | Duplicate |
| 21 | odysseus/tests/test_search_query.py | Duplicate |
| 22 | odysseus/services/youtube/__init__.py | Package init |
| 22 | odysseus/tests/cli/test_skills_cli_rows.py | Merge with CLI tests |
| 22 | odysseus/tests/cli/test_personal_cli_rows.py | Merge with CLI tests |
| 22 | odysseus/tests/cli/test_memory_cli_rows.py | Merge with CLI tests |
| 22 | odysseus/tests/test_cookbook_diagnosis_js.py | Duplicate |
| 22 | odysseus/tests/test_digest_windows.py | Duplicate |
| 22 | odysseus/tests/test_manage_settings_token_budget.py | Duplicate |
| 22 | odysseus/tests/test_tool_utils_import_clean.py | Duplicate |
| 23 | odysseus/tests/test_resolve_upload_path_nondict.py | Duplicate |
| 23 | odysseus/src/goal_based_extractor.py | Check if module |
| 23 | odysseus/src/youtube_handler.py | Merge with YouTube |
| 23 | odysseus/data/src/preview.ts | Merge with preview |
| 23 | odysseus/tests/test_personal_docs_state_store.py | Duplicate |
| 23 | odysseus/tests/test_route_validators.py | Merge with route tests |
| 23 | odysseus/tests/test_search_service_nondict_rows.py | Merge with search tests |
| 24 | odysseus/tests/test_context_compactor_nonstring.py | Triplicate |
| 24 | odysseus/static/js/editor/checkerboard.js | Merge with editor |
| 24 | odysseus/tests/test_editor_draft_payload.py | Merge with editor tests |
| 24 | odysseus/tests/test_pdf_runtime.py | Duplicate |
| 24 | odysseus/tests/test_hwfit_params_b_malformed.py | Duplicate |
| 24 | odysseus/tests/test_extract_skill_json_nonstring.py | Duplicate |
| 25 | odysseus/tests/test_cleanup_service_utcnow.py | Sextuplicate |
| 25 | odysseus/tests/cli/test_logs_cli_resolve_nonstring.py | Duplicate |
| 25 | odysseus/tests/test_markdown_dom_xss_helpers.py | Merge with XSS tests |
| 25 | odysseus/tests/test_memory_extractor_rows.py | Merge with memory tests |
| 25 | odysseus/tests/cli/test_research_cli_preview.py | Merge with CLI tests |
| 25 | odysseus/data/debug_import.py | Duplicate |
| 25 | odysseus/tests/test_setup_admin_user.py | Merge with admin tests |
| 26 | odysseus/tests/test_calendar_parse_dt_tonight.py | Duplicate |
| 26 | odysseus/tests/test_signature_settings_dom_xss.py | Duplicate |
| 26 | odysseus/tests/test_searxng_image_pinned.py | Duplicate |
| 26 | odysseus/tests/test_load_features_permission_error.py | Duplicate |
| 27 | odysseus/tests/test_cookbook_deps_recipes.py | Duplicate |
| 27 | odysseus/static/js/emailLibrary/replyRecipients.js | Duplicate |
| 27 | odysseus/tests/test_readiness.py | Triplicate |
| 27 | odysseus/tests/test_task_session_folder.py | Duplicate |
| 27 | odysseus/tests/test_anthropic_response_parse.py | Duplicate |
| 27 | odysseus/tests/test_cookbook_download_toast_duration.py | Triplicate |
| 28 | odysseus/tests/test_bg_jobs_store.py | Merge with BG jobs |
| 28 | odysseus/tests/test_memory_owner_isolation.py | Merge with memory tests |
| 28 | odysseus/tests/test_rag_vector_id_stability.py | Duplicate |
| 28 | odysseus/tests/test_extract_quotes.py | Duplicate |
| 28 | odysseus/tests/test_sanitize_multimodal_merge.py | Duplicate |
| 28 | odysseus/tests/test_document_library_language_facet.py | Duplicate |
| 29 | odysseus/core/exceptions.py | Merge with exceptions |
| 29 | odysseus/static/js/cookbookProgressSignal.js | Merge with cookbook |
| 29 | odysseus/tests/test_notes_search_reset_on_reopen_js.py | Duplicate |
| 29 | odysseus/tests/test_visual_report_icon_url.py | Duplicate |

---

*Generated: 2026-07-29*
