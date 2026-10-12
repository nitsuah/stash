# PROMO

The RSI log for the `/promo` skill (`~/.claude/skills/promo/SKILL.md`, upstream `nitsuah/.github` `skills/promo/SKILL.md`, contract `showcase/STANDARD.md`). Every `/promo` run appends an entry under **Run log**. When the same friction shows up twice, it becomes a checklist rule in the skill. The skill's own RSI section defines the entry format.

**Owner:** whoever runs `/promo`. [[RSI]] reads this log each cycle, like the other routine logs.

## Rules settled so far

- **Feature cull** (2026-10-08, vigil): a FEATURES.md bullet gets a visual only when a user can see it or do it (a screen, a button, a CLI or MCP response). These are `"visual": "none"` in `promo/spots.json`:
  - implementation details,
  - items of a list a parent check covers,
  - tech stack and deployment,
  - cross-category duplicates,
  - process or marketing statements,
  - unshipped or unverifiable claims (grep the code).

  Propose FEATURES.md trims in the PR and let the user confirm. Never delete lines in a promo PR. Report coverage as visuals over *visual* features.
- **One composition, many cuts**: a new spot is a `spot.json` with `"base"` and a scene list, not a copied compose/synth.
- **Narration**: Kokoro (`hyperframes tts`) runs only in an image with Python `kokoro-onnx`. The voice sets scene lengths, and the wavs are committed.
- **Feature spots share no intro or outro** (2026-10-08, vigil, user-reported): each spot shows only its own scenes, with the wordmark from frame 0, an outro of 3 s or less and its natural length (12–21 s). The shared hook, reveal and full outro play once, in a single continuous hero cut, never in spots concatenated end to end. Check it with a same-timestamp frame grid across the spots.

## Run log

### 2026-10-09 · stash · spot (journeys-19s, additive; first repo with no frontend)
- Ran: `journeys-19s` (19.0 s, −14 LUFS, web cut 1.1 MB) with a new compose-only `promo/build.sh` (Chromium frames from `compose.html`, numpy synth, ffmpeg) in Docker; a new `pages/journeys.html` linked from the existing page (2 added lines in index.html, nothing replaced); spots.json gained a feature, a spot and a reel. Checked at 375 px: no horizontal scroll, all media and local links load.
- Checklist misses: readability. The first 18 s cut showed the terminal summary for ~1.4 s and the "plain code on a cron" line for ~1 s. Fixed by faster terminal ticks and +1 s on the lifecycle scene (now 19 s). The contact sheet caught it; the stills alone did not.
- Friction: with no app to capture, /brag would have rebuilt UI. Composing real artifacts (issue titles, journey names, another repo's docs screenshots) was faster and more honest. `preview_start` picked up a launch.json from the parent folder, so the page was served with a throwaway nginx container instead.
- Promote:
  - Skill (nitsuah/.github skills/promo): a "No frontend?" note: compose real artifacts (issues, terminal output, CLI/MCP responses, screenshots from the repos the tool serves) with stash's `promo/build.sh` as the template; additive pages go in a new file plus nav and card links, never edits to the existing hero.
  - Candidate rule (first sighting): check read time per text block on the contact sheet (≈0.3 s per word, fully settled), not just whether it's on screen.

### 2026-10-09 · fire · refresh (same PR as the journeys pilot, fire#176)
- Ran: vigil audit → `apply` (+3 features), cull 38/95 to `none` (57 visible, 43 with a visual), 13 docs screenshots from the journeys, re-capture + re-render of the 3 published spots via `promo/build.sh` (brag-22s 22.0 s, chaos-24s 24.0 s, tour-85s 83 s), published.
- Checklist misses: the demo seed showed a real person's ENS wallet (`vitalik.eth`, fire#175), and the API seed silently dropped the year of net-worth history (fire#174). Both fixed in the PR. The hero's MCP frame disagreed with its dashboard frame (288,278 vs $287,897.50; 13 vs ~12 yrs): filed fire#178, not edited around.
- Friction: no screenshot CI. Rather than a second Playwright suite, the journeys emit `docs/screenshots/<id>.png` (`step({ docs })`). Six unpublished spots run 55–65 s; splitting them needs vigil's reusable composition ported first (fire TASKS, P2). FEATURES.md over-reports at 40% culled; trims proposed in TASKS.
- Promote: done in nitsuah/.github#19: SKILL.md (journeys as screenshot CI; "numbers agree across scenes" and "seed renders" checks), journeys/STANDARD.md (`docs` option). Copied to `~/.claude/skills/promo/`.

### 2026-10-08 · vigil · refresh (full: cull, screenshots, spots, reel, vert, publish, brand)

- **Ran:**
  - Spots: `health-21s`, `work-21s`, `agents-21s` (21 s each) and `health-21s-vert` (24.5 s, 9:16, narrated). All via vigil's `promo/build.sh` (real app, demo seed, Docker), not /brag: the repo has its own engine, and the skill prefers it.
  - Hero reel: 62.4 s via the new `promo/reel.sh`, published as the Pages hero.
  - Visual-docs: 2 new screenshots (chat, mobile).
  - Brand: synced, no logo change.
  - PRs: nitsuah/vigil#271, nitsuah/.github#17.
- **Usage / time:**
  - About 4 h wall clock. About 1 h 15 m of that was Docker rendering: 4 full renders at ~5–10 min each, one re-render pass, captures, TTS image build.
  - Context: ~306k of 1M tokens at PR time.
  - Plan: 28% of the 5-hour window and 60% weekly (Pro) at the end, starting from an unknown baseline. Next run: read `get_usage` at the start too.
- **Audit before → after:**
  - Audit column: 0/201 → 180/201. That counts 144 exemptions.
  - Visual features covered: 0/57 → **36/57**.
  - `feature-dropped`: 6 → 0. These were the Planned bullets, which the parser now skips.
  - Spots published: 1 → 5. Reels published: 0 → 1.
- **Checklist misses:**
  - "First 2 s say what the product is": failed on the existing brag-30s, which opened with a question hook only. Fixed with a wordmark bug on the hook from frame 0.
  - Two encodes silently dropped frames (583/630). ffmpeg's image2 demuxer hit "Cannot allocate memory" while another render ran, yet exited 0, and the pipeline printed "done". Caught by an ffprobe frame count. `pipeline.sh` now fails on a mismatch. Render one spot at a time.
  - Vertical naming: first used `health-vert`; STANDARD says `<spot>-vert`. Renamed before publishing.
- **Friction:**
  - FEATURES.md listed 201 bullets, but only 57 are user-visible. The skill had no cull step, so the first hour went to classification.
  - Audit in a worktree: `.git` is a pointer file to a Windows path, so the container has no history (`spot-stale-unchecked`) and labels the repo `target`.
  - The audit's coverage column counts `none` exemptions as covered (180/201 looks done; 36/57 is the truth).
  - vigil's brag-30s compose/synth were one absolute 30 s timeline. A 21 s cut needed either copies or a refactor. Did the refactor: scene-relative time mapping via `"base"`.
  - `hyperframes tts` fails in a plain node image (needs Python `kokoro-onnx`). Built `promo/tts/Dockerfile`. The first run downloads ~27 MB of voice data into a named volume.
  - No Python on the Windows host, so all JSON edits went through node and all audio through the promo image. That was fine.
  - A synth refactor bug (`at()` shadowed by a loop variable named `at`) surfaced only at the audio step, after 5 minutes of frames. Run `--audio` on one spot before full renders.
  - The skill's "get an OK before rendering more than one spot" gate conflicts with a pre-approved full run. Posted the plan and proceeded.
  - The hero reel repeats hook/reveal/outro three times (once per spot). Watchable, but a native long cut (one hook, all scenes, one outro) would read better.
  - Reviewing stills one image at a time is token-heavy. A contact sheet (`promo/sheet.sh`) cut that to one image per spot.
  - Found a likely false FEATURES.md claim ("Automated Sync — Netlify scheduled functions": no scheduled function exists). It's listed in the PR for the user.
- **Promote:**
  - Skill (done, nitsuah/.github#17, copied to `~/.claude/skills/promo/`): the cull step, the worktree audit caveat, `base` spots, contact sheets, wordmark rule, reel publishing, and vertical TTS notes.
  - vigil `showcase.ts` (TASKS P3 in vigil#271): coverage as visual/visual-features + exempt count; `--features-changed` or read git from the main checkout; row label from `product`.
  - vigil TASKS P3: visual-docs shots for the 21 uncovered visual features.
  - fire (next run): port `base` spots + `reel.sh` + the frame-count check before cutting spots. Read this entry first.
  - Candidate rule (needs a second sighting): "verify every encode's frame count". The skill checklist has it implicitly via duration ±2 s, but the truncated file's duration (19.4 s) was still within ±2 s of 21 s. Consider tightening to an exact frame count.

### 2026-10-08 (later) · vigil · spot · re-cut after user review

- **Ran:** `health-17s`, `work-16s`, `ai-14s` (new `chat` scene captured from the real app) and `hero-37s` (one cut), all via vigil's `promo/build.sh`, about 20 min of rendering. They replace the three 21 s spots and the 62 s concatenated reel. Kept the vertical, renamed `health-17s-vert`.
- **Checklist misses:** none of the checks caught the actual problem. Every 21 s spot opened on the same 3 s hook and 4 s reveal and closed on the same 3 s outro: 10 of 21 s identical. The page's spots gallery read as the full video three times, and the 62 s reel played the intro and outro three times. The user caught it on the live page. Each spot passed its own checklist; nothing compared the spots with each other.
- **Friction:** fitting 21 s forced a shared preamble onto thin content (6 scenes for 3 spots). The AI spot had only one scene of its own and borrowed `connect` from the work spot. Adding a real scene (the chat panel, seeded thread, no AI call) beat stretching or reusing one.
- **Promote:**
  - Skill + STANDARD (done, nitsuah/.github PR): feature spots share no intro or outro and run their natural length, the hero is one continuous cut, a checklist item for a cross-spot frame grid, and the /brag brief no longer defaults to `--duration 21`.
  - vigil: `extraScenes` lets the base composition carry scenes its own cut doesn't play; `reel.sh` handles a one-spot reel; a corner wordmark for spots that open on a feature.
  - Candidate rule (first sighting): if any feature spot has fewer than two scenes of its own (not shared with another spot), add a scene for it (capture more of the app) before rendering instead of sharing or stretching one.

### 2026-10-10 · skyview · refresh

- **Ran:** audit → visual-docs CI recipe (14 screenshots, 2 diagrams) → spots.json cull and links → Pages rebuild → brand record. No video rendered: the only spot is the 2026-10-01 `launch-21s` one-off. Audit went from 0/24 linked to 22/24 (11 of 13 visible features; 11 `none`). PR nitsuah/skyview#183.
- **Checklist misses (existing `launch-21s`):** the outro URL `skyview.nitsuah.io` no longer resolves, and the Pages site had five links to it. Nothing in the audit resolves `live`, `page` or the links on the page. The spot's source was never committed (`brag-output/` is gitignored), so the fix is a full re-render, logged as a TASK.
- **Friction:**
  - The screenshot suite found two product bugs that unit tests miss: campaign personalization targets a selector the page doesn't have, and the dashboard's export buttons have no CSS. Both are FEATURES.md claims, so writing a capture per feature id doubles as a "does this feature render" check.
  - Plain `page.screenshot` was not byte-stable: glow and text-shadow differ by one colour level between runs, which would churn the bot PR. `toHaveScreenshot` with `snapshotPathTemplate` pointing at `docs/screenshots/{arg}{ext}`, `updateSnapshots: 'changed'` and `maxDiffPixelRatio: 0.002` fixed it (three identical runs).
  - `stray-brag-output` fired although `brag-output/` is gitignored and untracked: the audit checks the folder on disk, and a worktree mount has no git history to check against.
  - Pages only uploads `showcase/`, while screenshots live in `docs/screenshots`. Copying them in `pages.yml` at deploy time (and triggering on `docs/screenshots/**`) avoids committing every PNG twice.
  - A `pre` inside a `1fr` grid column caused horizontal scroll at 375 px; the in-app browser pane reported no overflow because its emulated width was 545. Measured with Playwright at a real 375 px instead.
  - `cd ~/code/vigil && docker compose …` from the skill leaves the shell in vigil; the next relative command ran against the wrong repo.
- **Promote:**
  - vigil `showcase audit`: skip `stray-brag-output` when `.gitignore` covers `brag-output/`; add a `dead-link` check that resolves `live`, `page` and the Pages site's outbound hosts.
  - vigil `docs/VISUAL_DOCS.md` and the workflow template: recommend the `toHaveScreenshot` + `snapshotPathTemplate` pattern, and the deploy-time copy into the Pages folder.
  - Skill: run the audit in a subshell (`(cd ~/code/vigil && …)`); add "check 375 px with a real viewport, not the pane" to the Pages checks.
  - Candidate rule (first sighting): a FEATURES.md entry whose capture can't be made because the feature doesn't render is a product bug: file it and leave the feature as a gap, don't mark it `none`.

### 2026-10-10 (later) · skyview · spot + reel + publish

- **Ran:** `site-14s`, `book-18s`, `portal-12s` and `hero-30s` (one continuous cut) via a new `promo/build.sh`, ported from stash (compose-only) with a `base` spot. About 8 min of rendering for 74 s of video. Published to `showcase/media/`; they replace `launch-21s`. Same PR, nitsuah/skyview#183.
- **Checklist misses:** none on the renders (exact frame counts, frame grid clean, outro URL current). Not done: nobody listened to the audio.
- **Friction:**
  - First render ran at under 1 frame/s: eleven full-size screenshot layers at opacity 0 were still composited every frame. Setting hidden layers to `display: none` in `render(t)` brought it to about 3 frames/s.
  - A background `for spot in …; do build.sh` loop kept going after its container was killed and re-rendered into `promo/out/` while a second render was encoding. The published `hero-30s` came from a mixed frame set; a re-encode from the final frames differed and replaced it. The frame-count check did not catch this.
  - `render.js` with `require` fails in a repo whose package.json has `"type": "module"`; renamed to `.cjs`.
  - Camera and ring positions are hand-read fractions of each screenshot, so a layout change silently misaligns a highlight.
- **Promote:**
  - stash/vigil `promo/` templates: ship `render.cjs` / `spot-config.cjs`, and the `display: none` rule for inactive layers.
  - `build.sh` in all three repos: take a lock (`promo/out/<spot>/.lock`) so two renders of one spot cannot overlap.
  - Skill: "kill the shell loop, not just the container" when aborting a render; add "listen to each spot once" to the double-check list.
  - Candidate rule (first sighting): have the visual-docs suite write element bounding boxes next to each screenshot (`<id>.regions.json`) so compositions read highlight positions instead of hard-coding them.
