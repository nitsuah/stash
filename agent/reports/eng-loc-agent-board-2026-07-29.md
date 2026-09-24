# ENG LOC Report — agent-board (2026-07-29)

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 1819 | agent-board/tools/opencut/apps/web/src/stickers/providers/countries-data.ts | Large data file - consider externalizing data |
| 1508 | agent-board/tools/content-gen/modules/MoneyPrinterTurbo/app/services/voice.py | Voice service - extract TTS providers |
| 1451 | agent-board/tools/content-gen/modules/MoneyPrinterTurbo/webui/Main.py | Main UI - split into modules |
| 1361 | agent-board/tools/opencut/apps/web/src/animation/keyframes.ts | Animation keyframes - consider splitting |
| 1298 | agent-board/tools/opencut/apps/web/src/timeline/components/timeline-element.tsx | Timeline element - extract subcomponents |
| 1087 | agent-board/tools/content-gen/modules/MoneyPrinterTurbo/app/services/video.py | Video service - extract encoding logic |
| 1039 | agent-board/tools/content-gen/modules/MoneyPrinterTurbo/app/services/llm.py | LLM service - extract providers |
| 1022 | agent-board/tools/opencut/apps/web/src/app/projects/page.tsx | Projects page - extract sections |
| 988 | agent-board/dashboard/src/App.jsx | Main App - extract routes/providers |
| 953 | agent-board/tools/opencut/apps/web/src/timeline/components/index.tsx | Timeline index - check if barrel |
| 935 | agent-board/tools/opencut/apps/web/src/core/managers/timeline-manager.ts | Timeline manager - extract helpers |
| 923 | agent-board/tools/opencut/apps/web/src/gradients/canvas.ts | Gradient canvas - extract utilities |
| 921 | agent-board/dashboard/src/components/LiminalDashboard.jsx | Dashboard - extract widgets |
| 870 | agent-board/tools/opencut/rust/crates/compositor/src/compositor.rs | Rust compositor - consider modularizing |
| 867 | agent-board/tools/opencut/apps/web/src/media/audio.ts | Audio module - extract submodules |
| 863 | agent-board/tools/content-gen/modules/MoneyPrinterTurbo/test/services/test_llm.py | Test file - split by provider |
| 852 | agent-board/tools/opencut/apps/web/src/masks/components/masks-tab.tsx | Masks tab - extract components |
| 835 | agent-board/tools/opencut/apps/web/src/masks/freeform/path.ts | Path utilities - extract helpers |
| 820 | agent-board/dashboard/src/components/WorkspaceView.jsx | Workspace view - extract panels |
| 788 | agent-board/tools/opencut/apps/web/src/preview/controllers/transform-handle-controller.ts | Transform controller - extract logic |
| 774 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/transformers/v1-to-v2.ts | Migration transformer |
| 731 | agent-board/tools/opencut/apps/web/src/timeline/controllers/element-interaction-controller.ts | Interaction controller |
| 694 | agent-board/tools/opencut/apps/web/src/preview/components/preview-viewport.tsx | Preview viewport |
| 687 | agent-board/tools/opencut/apps/web/src/sounds/components/assets-view.tsx | Assets view |
| 652 | agent-board/tools/opencut/apps/web/src/gradients/parser.ts | Gradient parser |
| 589 | agent-board/tools/opencut/apps/web/src/core/managers/project-manager.ts | Project manager |
| 584 | agent-board/tools/opencut/apps/web/src/services/storage/service.ts | Storage service |
| 575 | agent-board/tools/opencut/apps/web/src/timeline/controllers/drag-drop-controller.ts | Drag-drop controller |
| 572 | agent-board/tools/opencut/apps/web/src/preview/controllers/preview-interaction-controller.ts | Preview interaction |
| 566 | agent-board/tools/content-gen/modules/MoneyPrinterTurbo/test/services/test_video.py | Video tests |
| 566 | agent-board/tools/opencut/apps/web/src/services/renderer/compositor/frame-descriptor.ts | Frame descriptor |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | agent-board/tools/opencut/apps/web/src/background/color.ts | Merge with background module |
| 1 | agent-board/tools/opencut/apps/web/src/selection/attributes.ts | Merge with selection |
| 1 | agent-board/tools/opencut/apps/web/src/animation/transform.ts | Merge with animation |
| 1 | agent-board/tools/opencut/apps/web/src/commands/project/index.ts | Merge with commands |
| 1 | agent-board/tools/opencut/apps/web/src/wasm/index.ts | Merge with wasm barrel |
| 1 | agent-board/tools/opencut/apps/web/src/stickers/intrinsic-size.ts | Merge with stickers |
| 1 | agent-board/tools/opencut/apps/web/src/transcription/supported-languages.ts | Merge with transcription |
| 2 | agent-board/tools/opencut/apps/web/src/commands/media/index.ts | Merge with commands |
| 2 | agent-board/tools/opencut/apps/web/src/clipboard/index.ts | Merge with clipboard |
| 2 | agent-board/tools/opencut/apps/web/src/transcription/caption-defaults.ts | Merge with transcription |
| 2 | agent-board/tools/opencut/apps/web/src/timeline/audio-constants.ts | Merge with timeline constants |
| 2 | agent-board/tools/opencut/apps/web/src/components/icons/index.tsx | Merge with icons barrel |
| 2 | agent-board/tools/opencut/apps/web/src/commands/timeline/clipboard/index.ts | Merge with timeline commands |
| 2 | agent-board/tools/opencut/apps/web/src/masks/dimensions.ts | Merge with masks |
| 2 | agent-board/tools/opencut/apps/web/src/gradients/index.ts | Merge with gradients barrel |
| 2 | agent-board/tools/opencut/apps/web/src/masks/feather.ts | Merge with masks |
| 2 | agent-board/tools/opencut/apps/web/src/fps/defaults.ts | Merge with fps |
| 3 | agent-board/tools/opencut/apps/web/src/actions/index.ts | Merge with actions barrel |
| 3 | agent-board/tools/opencut/apps/web/src/feedback/index.ts | Merge with feedback barrel |
| 3 | agent-board/tools/opencut/apps/web/src/app/api/health/route.ts | Check if needed |
| 3 | agent-board/tools/opencut/apps/web/open-next.config.ts | Check if config |
| 3 | agent-board/tools/opencut/apps/web/src/timeline/scale.ts | Merge with timeline |
| 4 | agent-board/tools/opencut/apps/web/src/guides/grid.ts | Merge with guides |
| 4 | agent-board/tools/opencut/apps/web/src/ripple/index.ts | Merge with ripple |
| 4 | agent-board/tools/opencut/apps/web/src/selection/index.ts | Merge with selection barrel |
| 4 | agent-board/tools/opencut/apps/web/src/commands/timeline/track/index.ts | Merge with track commands |
| 4 | agent-board/tools/opencut/apps/web/src/commands/timeline/element/masks/index.ts | Merge with element commands |
| 4 | agent-board/tools/opencut/apps/web/src/export/mime-types.ts | Merge with export |
| 4 | agent-board/tools/opencut/apps/web/src/transcription/audio.ts | Merge with transcription |
| 5 | agent-board/tools/opencut/apps/web/src/components/icons/types.ts | Merge with icons |
| 5 | agent-board/tools/opencut/apps/web/src/site/social.ts | Merge with site |
| 5 | agent-board/tools/opencut/rust/crates/effects/src/effects.rs | Check if Rust module |
| 5 | agent-board/tools/opencut/rust/crates/masks/src/masks.rs | Check if Rust module |
| 5 | agent-board/tools/opencut/apps/web/src/retime/index.ts | Merge with retime |
| 5 | agent-board/tools/opencut/apps/web/src/commands/timeline/index.ts | Merge with timeline commands |
| 5 | agent-board/tools/opencut/apps/web/src/commands/timeline/element/effects/index.ts | Merge with element commands |
| 6 | agent-board/tools/opencut/apps/web/src/utils/ui.ts | Merge with utils |
| 6 | agent-board/tools/opencut/apps/web/src/commands/timeline/element/keyframes/index.ts | Merge with keyframes |
| 6 | agent-board/tools/opencut/apps/web/src/auth/client.ts | Merge with auth |
| 6 | agent-board/tools/opencut/apps/web/src/timeline/components/layers.ts | Merge with timeline components |
| 7 | agent-board/tools/opencut/apps/web/src/export/defaults.ts | Merge with export |
| 7 | agent-board/tools/opencut/apps/web/src/fps/presets.ts | Merge with fps |
| 7 | agent-board/tools/opencut/apps/web/src/commands/scene/index.ts | Merge with scene commands |
| 7 | agent-board/tools/opencut/apps/web/src/preview/zoom.ts | Merge with preview |
| 7 | agent-board/tools/opencut/apps/web/src/stickers/categories.ts | Merge with stickers |
| 7 | agent-board/tools/opencut/apps/web/src/utils/date.ts | Merge with utils |
| 7 | agent-board/tools/opencut/apps/web/src/utils/string.ts | Merge with utils |
| 7 | agent-board/tools/opencut/apps/web/src/services/renderer/nodes/color-node.ts | Merge with renderer nodes |
| 8 | agent-board/tools/opencut/apps/web/src/commands/index.ts | Merge with commands barrel |
| 8 | agent-board/tools/opencut/apps/web/src/panels/layout.ts | Merge with panels |
| 8 | agent-board/tools/opencut/apps/web/src/text/typography.ts | Merge with text |
| 8 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/transformers/index.ts | Merge with transformers |
| 9 | agent-board/tools/opencut/apps/web/src/media/types.ts | Merge with media |
| 9 | agent-board/tools/opencut/apps/web/src/timeline/tracks.ts | Merge with timeline |
| 9 | agent-board/tools/opencut/apps/web/src/retime/presets.ts | Merge with retime |
| 10 | agent-board/tools/opencut/apps/web/src/timeline/playhead-snap-source.ts | Merge with timeline |
| 10 | agent-board/tools/opencut/apps/web/src/params/__tests__/channel-layout.test.ts | Check if test needed |
| 10 | agent-board/tools/opencut/apps/web/src/graphics/registry.ts | Merge with graphics |
| 10 | agent-board/tools/opencut/apps/web/src/effects/registry.ts | Merge with effects |
| 10 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/__tests__/fixtures/index.ts | Check if fixtures |
| 10 | agent-board/tools/opencut/apps/web/src/stickers/registry.ts | Merge with stickers |
| 10 | agent-board/tools/opencut/apps/web/src/canvas/sizes.ts | Merge with canvas |
| 10 | agent-board/tools/opencut/apps/web/src/background/blur.ts | Merge with background |
| 11 | agent-board/tools/opencut/apps/web/src/utils/platform.ts | Merge with utils |
| 11 | agent-board/tools/opencut/apps/web/src/feedback/types.ts | Merge with feedback |
| 11 | agent-board/tools/opencut/apps/web/src/fonts/system-fonts.ts | Merge with fonts |
| 11 | agent-board/tools/opencut/apps/web/src/components/ui/collapsible.tsx | Merge with UI components |
| 11 | agent-board/tools/opencut/apps/web/src/commands/timeline/element/index.ts | Merge with timeline element |
| 11 | agent-board/tools/opencut/apps/web/src/hooks/use-committed-ref.ts | Merge with hooks |
| 12 | agent-board/tools/opencut/rust/crates/compositor/src/lib.rs | Check if Rust lib |
| 12 | agent-board/tools/opencut/apps/web/src/timeline/placement/index.ts | Merge with placement |
| 12 | agent-board/tools/opencut/apps/web/src/timeline/group-move/index.ts | Merge with group-move |
| 12 | agent-board/tools/opencut/apps/web/src/text/background.ts | Merge with text |
| 13 | agent-board/tools/opencut/apps/web/src/site/brand.ts | Merge with site |
| 13 | agent-board/tools/opencut/apps/web/src/actions/keybindings/migrations/v4-to-v5.ts | Check if migration |
| 13 | agent-board/tools/opencut/apps/web/src/app/robots.ts | Check if robots.txt |
| 13 | agent-board/tools/opencut/apps/web/src/types/eyedropper.d.ts | Merge with types |
| 13 | agent-board/tools/opencut/rust/crates/effects/src/types.rs | Check if Rust types |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v2-to-v3.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v20-to-v21.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v7-to-v8.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v9-to-v10.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v19-to-v20.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v18-to-v19.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v17-to-v18.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v14-to-v15.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v26-to-v27.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v8-to-v9.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v11-to-v12.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v14-to-v15.ts | Duplicate |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v27-to-v28.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v15-to-v16.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v21-to-v22.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v13-to-v14.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v3-to-v4.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v22-to-v23.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v30-to-v31.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v0-to-v1.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v12-to-v13.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v28-to-v29.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v4-to-v5.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v5-to-v6.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v23-to-v24.ts | Check if migration |
| 14 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v10-to-v11.ts | Check if migration |
| 15 | agent-board/tools/opencut/apps/web/src/components/ui/skeleton.tsx | Merge with UI components |
| 15 | agent-board/tools/opencut/apps/web/src/retime/presets.ts | Duplicate |
| 15 | agent-board/tools/opencut/apps/web/src/timeline/snapping/threshold.ts | Merge with snapping |
| 15 | agent-board/tools/opencut/apps/web/src/components/ui/spinner.tsx | Merge with UI components |
| 15 | agent-board/tools/opencut/apps/web/src/services/renderer/canvas-utils.ts | Merge with renderer |
| 15 | agent-board/tools/opencut/apps/web/src/ripple/shift.ts | Merge with ripple |
| 15 | agent-board/tools/opencut/apps/web/src/timeline/creation.ts | Merge with timeline |
| 15 | agent-board/tools/opencut/apps/web/src/actions/keybindings/migrations/v6-to-v7.ts | Check if migration |
| 16 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/transformers/v9-to-v10.ts | Check if transformer |
| 16 | agent-board/tools/opencut/apps/web/src/app/page.tsx | Check if page entry |
| 16 | agent-board/tools/opencut/apps/web/src/auth/rate-limit.ts | Merge with auth |
| 16 | agent-board/tools/opencut/apps/web/src/preview/components/cursors.ts | Merge with preview |
| 16 | agent-board/tools/opencut/apps/web/src/services/renderer/nodes/video-node.ts | Merge with renderer nodes |
| 16 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/base.ts | Merge with migrations base |
| 17 | agent-board/tools/opencut/apps/web/src/timeline/bookmarks/snap-source.ts | Merge with bookmarks |
| 17 | agent-board/tools/opencut/apps/web/src/timeline/snapping/index.ts | Merge with snapping |
| 17 | agent-board/tools/opencut/apps/web/src/timeline/group-resize/index.ts | Merge with group-resize |
| 17 | agent-board/tools/opencut/apps/web/src/timeline/tracks.ts | Duplicate |
| 18 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v29-to-v30.ts | Check if migration |
| 18 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v16-to-v17.ts | Check if migration |
| 18 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v7-to-v8.ts | Duplicate |
| 18 | agent-board/tools/opencut/apps/web/src/guides/index.ts | Merge with guides |
| 18 | agent-board/tools/opencut/apps/web/src/transcription/languages.ts | Merge with transcription |
| 18 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v25-to-v26.ts | Check if migration |
| 18 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/v8-to-v9.ts | Duplicate |
| 19 | agent-board/tools/opencut/apps/web/src/db/index.ts | Merge with db barrel |
| 19 | agent-board/tools/opencut/apps/web/src/components/editor/panels/properties/stores/properties-store.ts | Merge with properties |
| 19 | agent-board/tools/opencut/apps/web/src/hooks/use-container-size.ts | Merge with hooks |
| 19 | agent-board/tools/opencut/apps/web/src/hooks/use-mobile.ts | Merge with hooks |
| 19 | agent-board/tools/opencut/apps/web/src/services/renderer/nodes/effect-layer-node.ts | Merge with renderer nodes |
| 19 | agent-board/tools/opencut/rust/crates/time/src/time.rs | Check if Rust time module |
| 20 | agent-board/tools/opencut/apps/web/src/timeline/components/layout.ts | Merge with timeline |
| 20 | agent-board/tools/opencut/apps/web/src/timeline/track-capabilities.ts | Merge with timeline |
| 20 | agent-board/tools/opencut/apps/web/src/guides/types.ts | Merge with guides |
| 20 | agent-board/tools/opencut/apps/web/src/components/editor/panels/properties/empty-view.tsx | Merge with properties |
| 20 | agent-board/tools/opencut/apps/web/src/hooks/use-raf-loop.ts | Merge with hooks |
| 20 | agent-board/tools/opencut/apps/web/src/services/renderer/mask-feather.ts | Merge with renderer |
| 20 | agent-board/tools/opencut/apps/web/src/stickers/resolver.ts | Merge with stickers |
| 20 | agent-board/tools/opencut/apps/web/src/actions/keybindings/migrations/v3-to-v4.ts | Check if migration |
| 21 | agent-board/tools/opencut/apps/web/src/components/ui/progress.tsx | Merge with UI components |
| 21 | agent-board/tools/opencut/apps/web/src/components/ui/textarea.tsx | Merge with UI components |
| 21 | agent-board/tools/opencut/apps/web/src/editor/cancel-interaction.ts | Merge with editor |
| 21 | agent-board/tools/opencut/apps/web/src/fonts/types.ts | Merge with fonts |
| 21 | agent-board/tools/opencut/apps/web/src/components/ui/scroll-area.tsx | Merge with UI components |
| 22 | agent-board/tools/opencut/apps/web/src/components/editor/panels/properties/hooks/use-element-playhead.ts | Merge with properties hooks |
| 22 | agent-board/tools/opencut/apps/web/src/selection/selection-box.tsx | Merge with selection |
| 22 | agent-board/tools/opencut/apps/web/src/timeline/snapping/types.ts | Merge with snapping |
| 22 | agent-board/tools/opencut/rust/wasm/src/wasm.rs | Check if wasm module |
| 23 | agent-board/tools/opencut/apps/web/src/selection/editor-selection.ts | Merge with selection |
| 23 | agent-board/tools/opencut/apps/web/src/commands/preview-tracker.ts | Merge with commands |
| 23 | agent-board/tools/opencut/apps/web/src/graphics/types.ts | Merge with graphics |
| 23 | agent-board/tools/opencut/apps/web/src/timeline/components/drag-line.tsx | Merge with timeline |
| 24 | agent-board/tools/opencut/apps/web/src/guides/definitions/custom.tsx | Merge with guides |
| 24 | agent-board/tools/opencut/apps/web/src/timeline/snapping/resolve.ts | Merge with snapping |
| 24 | agent-board/tools/opencut/apps/web/src/timeline/bookmarks/index.ts | Merge with bookmarks |
| 24 | agent-board/tools/opencut/apps/web/src/timeline/components/graph-editor/easing-presets.ts | Merge with graph-editor |
| 25 | agent-board/tools/opencut/apps/web/src/subtitles/parse.ts | Merge with subtitles |
| 25 | agent-board/tools/opencut/apps/web/src/components/ui/switch.tsx | Merge with UI components |
| 25 | agent-board/tools/opencut/apps/web/src/timeline/components/graph-editor/session.ts | Merge with graph-editor |
| 25 | agent-board/tools/opencut/apps/web/src/editor/editor-store.ts | Merge with editor |
| 26 | agent-board/tools/opencut/apps/web/drizzle.config.ts | Check if config |
| 26 | agent-board/tools/opencut/apps/web/src/utils/id.ts | Merge with utils |
| 26 | agent-board/tools/opencut/apps/web/src/guides/registry.tsx | Merge with guides |
| 26 | agent-board/tools/opencut/apps/web/src/animation/path.ts | Merge with animation |
| 26 | agent-board/tools/opencut/apps/web/src/actions/keybindings/migrations/v2-to-v3.ts | Check if migration |
| 26 | agent-board/tools/opencut/apps/web/src/hooks/use-resize-observer.ts | Merge with hooks |
| 26 | agent-board/tools/opencut/apps/web/src/components/ui/label.tsx | Merge with UI components |
| 26 | agent-board/tools/opencut/apps/web/src/editor/use-menu-preview.ts | Merge with editor |
| 26 | agent-board/tools/opencut/apps/web/src/masks/param-update.ts | Merge with masks |
| 27 | agent-board/tools/opencut/apps/web/src/timeline/snapping/threshold.ts | Duplicate |
| 27 | agent-board/tools/opencut/apps/web/src/timeline/bookmarks/snap-source.ts | Duplicate |
| 27 | agent-board/tools/opencut/apps/web/src/components/ui/hover-card.tsx | Merge with UI components |
| 27 | agent-board/tools/opencut/apps/web/src/commands/timeline/tracks-snapshot.ts | Merge with timeline |
| 28 | agent-board/tools/opencut/apps/web/src/components/editor/panels/properties/stores/properties-store.ts | Duplicate |
| 28 | agent-board/tools/opencut/apps/web/src/services/storage/migrations/transformers/utils.ts | Merge with transformers |
| 28 | agent-board/tools/opencut/apps/web/src/timeline/components/graph-editor/easing-presets.ts | Duplicate |
| 29 | agent-board/tools/opencut/apps/web/src/timeline/components/graph-editor/ |
| 29 | agent-board/tools/opencut/apps/web/src/timeline/snapping/resolve.ts | Duplicate |
| 29 | agent-board/tools/opencut/apps/web/src/commands/timeline/tracks-snapshot.ts | Duplicate |

---

*Generated: 2026-07-29*