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
