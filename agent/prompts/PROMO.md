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

## Waiting on the desktop (render hardware)

Do this the first time `/promo` runs on Austin's primary desktop (Ryzen 7 + RTX 4080). Set 2026-10-15. Tracked in `docs/TASKS.md` under Later.

- **Why:** the laptop (Ryzen 9 5900HX, TDP-locked RTX 3070, 15.4 GB RAM, no `.wslconfig`) gives Docker only 8 GB. Renders run at about 1.5–3 fps (a 20 s spot takes 3–6 min, mostly headless-Chromium frame capture), and every render or Playwright job had to run alone behind `~/code/.docker-lock`. The T1/T2 waves spent hours queued. The desktop also has no thermal or TDP ceiling on long all-core renders.
- **Benchmarks.** Run both before step 1 and after each step, and log the numbers here:
  - **Render:** one spot, the same one each time (stash `journeys-19s`, compose-only and no /brag). Record frames per second and wall time.
  - **Playwright:** one fixed workload, fire's journeys (`npm run test:journeys` in its pinned image, `--repeat-each 3`). Record wall time. Also record how many of these can run at once without failures or OOM. That number replaces the one-at-a-time Docker lock.
- **Steps, in order:**
  1. Create `%USERPROFILE%\.wslconfig` with `[wsl2]`, `memory=` (total RAM minus about 4 GB) and `processors=` (all threads), then run `wsl --shutdown` and restart Docker Desktop. Then let wave briefs run two or three Docker jobs at once and relax the lock.
  2. Raise `RENDER_WORKERS` (default 4) in each repo's `promo/render.js` / `render.cjs` up to the core count. Watch memory.
  3. Use the GPU: run `docker run --gpus all` (Docker Desktop supports it on WSL2), encode with ffmpeg `h264_nvenc`, and try Chromium GPU raster (`--use-gl=egl`). Keep x264 where NVENC quality loses on the contact sheet.
  4. Optionally render compose-only spots (stash, bb-mcp, nitsuah-io, skyview: no /brag in the loop) in GitHub Actions through `workflow_dispatch` on the free public-repo runners, then download the artifact for review. Spots that use /brag stay local.
- **Done when:**
  - a full render wave runs in parallel;
  - Playwright suites run concurrently without failures;
  - both benchmarks (render frames/s and wall time; Playwright wall time and safe concurrency) are logged here before and after.

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

### 2026-10-14 · vhs · fix screenshots,diagrams,journeys,vertical
- Ran: journeys (4 journeys / 13 baselines) → journey-tagged screenshots (11) + `visual-docs.yml`; 3 Mermaid diagrams; `vert brag-20s` → `brag-20s-vert` (1080×1920, 20.0 s, −18.6 LUFS, Kokoro VO, web cut 1.8 MB), published to a new Pages section. One PR, nitsuah/vhs#80. Locked `brag-20s` and `site/brag.*` byte-identical; the spot was read-only (iframe of its `composition.html`, `audio.py` run for the music bed).
- Checklist misses: first poster (18.5 s, inherited from brag-20s) caught the last caption half-lit; moved to 19.6 s. VO line 2 ran 4.3 s into line 3; shortened the line and re-timed from measured `dur`. Nobody listened to the final mix (loudness only).
- Friction: `fix vertical` alone would have turned `videos` 1/1 → 1/2 (unpublished spot), so the Pages slot isn't optional. A vertical over a locked spot can't use `--format vertical` re-renders; the vigil shell (iframe + captions) works but had to be served over http for same-origin. The tts image needed scipy added for `audio.py`/`mix.py`.
- Promote: skill — `vertical` cell = render **and publish** (else `videos` regresses); ship vigil's `promo/tts` + vertical shell as a `nitsuah/.github/showcase/vert/` template that takes a locked base spot. visual_board: the `vertical` cell could require `published`.

### 2026-10-14 · T1 wave 1 · fix diagrams,linked (+ stash screenshots) · 6 repos in parallel
- **Ran:** a coordinator (Opus) briefed one cheaper-model agent per repo (sonnet: fire, ats-fill, motor-pool, stash; haiku: vhs + vigil), with no local renders and CI as the check. About 130-150k subagent tokens and 4-7 min per repo. PRs: fire#197, ats-fill#141, motor-pool#95, stash#236, vhs#83, vigil#290.
  - **Diagrams (fire, ats-fill, motor-pool, stash):** 2-3 Mermaid sources each, read from the code. Render step added to the existing visual-docs/screenshot workflow. First SVGs committed.
  - **Linked:**

    | Repo | Before | After |
    |---|---|---|
    | fire | 43/57 | 48/54 |
    | ats-fill | 0/50 | 30/40 |
    | motor-pool | 0/47 | 16/25 |
    | stash | 1/24 | 8/10 |
    | vhs | 6/47 | 14/40 |
    | vigil | 38/59 | 38/58 |

    Every repo now has a "needs capture" list of visible features no capture shows.
  - **stash, the first no-frontend repo:** the vault-graph generator moved into `docs/screenshots` behind a `visual-docs.yml` that opens a bot PR. `"frontend": false`. Two infographic generators proposed (routine timeline, prompt card grid).
- **Checklist misses:**
  - Two of six PRs failed CI on first push, both from copied files. motor-pool: the committed SVGs had no trailing newline, so pre-commit `end-of-file-fixer` failed. fire: vigil's `visual-docs-readme.mjs` didn't match fire's prettier. The coordinator fixed both, plus the motor-pool workflow, so the bot PRs won't repeat it.
  - stash's diagrams were never render-tested locally.
- **Friction:**
  - All three diagram agents spent 2+ tries validating Mermaid locally. The answer was `MSYS_NO_PATHCONV=1` plus `pwd -W` with `minlag/mermaid-cli:11.4.2`; no puppeteer JSON is needed.
  - vigil's template hard-codes `main`, and its README script duplicates an existing hand-written gallery.
  - The brief gave no `unlinked` list, so every agent re-derived it.
  - The brief also left out the CHANGELOG path, the CRLF warning (no Python or jq on the host), and the motor-pool folder (the coordinator's memory still said agent-board).
  - No rule covered partial image matches, linking unpublished spots, mirroring a spot's `features[]` into `spots[]`, or culling tests, a11y claims or agent config.
  - The 80% target can't be reached in a links-only pass on any repo with few screenshots. That is expected, and it means the next step is captures.
  - stash: a push trigger on `agent/**/*.md` would have opened a render PR for every routine note. The agent narrowed it and added a weekly cron.
- **Promote:**
  - Done, skill + STANDARD (nitsuah/.github PR):
    - `"frontend": false` and a generated-visuals table for repos without a UI.
    - A board-detector table, so agents can predict the after state.
    - An ordered linking rule with a Needs capture list and a TASKS.md capture-backlog line.
    - The Mermaid one-liner, the SVG newline rule, and the copied-script formatter rule.
    - Cull-list additions (tests, a11y, agent config).
    - Wave rules: what the brief must name, and RSI entries returned to the coordinator.
  - Done, `visual_board.py` (this PR):
    - Generated visuals in `pagesDir` count as screenshots for `frontend: false` repos.
    - Each row carries `unlinked`.
    - The diagram and screenshot hints point at real recipes.
  - vigil TASK: a branch placeholder in `templates/.github/workflows/visual-docs.yml`; a `--diagrams-only` / `SCREENSHOT_EXTS` option in `visual-docs-readme.mjs`; a trailing newline after `mmdc`; the Windows one-liner in `VISUAL_DOCS.md`; and an audit check that a spot's `features[]` and each feature's `spots[]` agree.
  - Next wave: `fix screenshots` per repo, working through the `Capture for promo:` TASKS lines, is what moves `linked` to ok.

### 2026-10-14/15 · T1 waves 2–3 · journeys + render (videos, vertical)
- **Ran:**
  - Wave 2 (journeys) is logged in JOURNEYS.md.
  - Wave 3: one Sonnet agent rendered serially until it hit the session limit just before committing stash. The coordinator reviewed every render and finished stash.
  - skyview#192: site-14s, portal-12s and hero-30s published, plus hero-30s-vert.
  - vigil#291: visual-17s rendered, and brag-30s dropped as superseded.
  - fire#199: brag-22s-vert. The six 55–65 s tour spots were left unrendered by design (TASKS: split them first).
  - stash#239: journeys-19s-vert, with Kokoro narration through `promo/tts`.
  - Board: portfolio 41% → 49%. skyview and stash are at 100%, fire and vhs at 95%, vigil 91% → 95%, and ats-fill and motor-pool 64% → 86%.
- **Checklist misses:** every render passed the checklist, but review still found two real defects.
  - vigil `visual-17s` told viewers Visual Docs was "not scored". It is scored. Its captured card even showed "(not scored)", because the promo capture fixture still set `informational` on `visual_docs`. Fixed copy, share copy and fixture, then recaptured and re-rendered. The e2e fixture is vigil#292.
  - fire `brag-22s-vert` clipped the dashboard at 1080 px, cutting off the spend rate and the legend. Refit the crop and re-rendered.
  - Neither vertical was mirrored onto its features' `spots[]`.
- **Friction:**
  - `build.sh --recapture` rewrote six Pages screenshots as a side effect.
  - `--publish` has no target for `-vert` spots.
  - skyview's vertical leaves the bottom third empty.
  - CodeRabbit's free tier rate-limited several PRs. Self-review per Austin's rule covered them.
- **Promote:**
  - Done in .github#26: check claims against the code (copy, share copy and captured UI); run `git status` after a render; vertical frame checks (no clipping, no dead third); the manual publish path including `spots[]`.
  - Next: T2 (nitsuah-io, bb-mcp, darkmoon). `fix screenshots` per T1 repo, working through the "Capture for promo" TASKS lines, is what turns the remaining `linked` cells green.

### 2026-10-15 · T2 · nitsuah-io + bb-mcp · fix (only the board's missing cells)
- **Ran:** two waves of Sonnet agents, each calling `/promo <repo> fix <cells>` through the Skill tool with only the missing cells. darkmoon and T3 were skipped by the owner's choice.
  - Wave A:
    - nitsuah-io#570: 33 full-page screenshots (19 pages, 9 phone, 5 states), 2 diagrams, and 8 journeys replacing `playwright-nightly`. Linked 1/77 → 17/21, with 56 culled as `none`.
    - bb-mcp#148: generated visuals drawn with resvg (no browser), 2 diagrams. Linked 0/39 → 38/39.
  - Wave B, serial:
    - bb-mcp#153: API-only journeys (`request` fixture plus `webServer`) and a Pages journey, plus `bb-mcp-21s-vert` (23 s, narrated, claims re-derived from the code).
    - nitsuah-io#573: `site-tour-vert` (29 s, stacked on #570).
  - Board: bb-mcp went 50% → 73% after #148; journeys and vertical turn green when #153 merges.
- **Checklist misses that review caught:**
  - nitsuah-io's first screenshots had the fixed footer painted over content, and the home page was cut at 900 px by a `100vh` grid with overflow hidden. Fixed in the capture fixture.
  - The real-site version of that home-page cut is nitsuah-io#572.
  - CodeRabbit raised 5 findings on bb-mcp#153: overlapping captions, sheet.sh dropping stills, external links on PRs, path containment, and range handling. All fixed.
  - CodeRabbit raised 3 on bb-mcp#148: concurrency, persisted credentials, and a CI guard for resvg. All fixed.
- **Bugs found and filed:** nitsuah-io #565–#569 and #572; bb-mcp #149–#152. The old bb-mcp landscape spot claims 34 tools, invents CLI verbs, and ends on an `npm i -g` that installs someone else's package.
- **Friction:**
  - Copilot's quota ran out, and the org's required Copilot review blocks merging nitsuah-io#570. That needs the owner (admin merge or the quota reset).
  - A stacked PR gets no CI, because the workflows only trigger on PRs to main.
  - nitsuah-io's husky hook runs `git add -A`, which breaks per-cell commits.
  - Two usage-limit interruptions mid-agent; both resumed with `SendMessage`.
- **Promote:** done in nitsuah/.github#28.
  - Full-page captures.
  - resvg visuals.
  - Inherited claims and `npm view`.
  - Vertical bounds script and phone-size text.
  - API-only journeys.
  - Caller image flavour (noble vs jammy) and the source paths in the PR trigger.
