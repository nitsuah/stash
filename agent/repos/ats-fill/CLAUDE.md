---
up: "[[repos/ats-fill]]"
title: "ats-fill · CLAUDE"
source: https://github.com/nitsuah/auto-apply-plugin/blob/main/CLAUDE.md
kind: repo-doc
repo: ats-fill
---

# ats-fill agent notes

- This is a Manifest V3 Chrome extension. Use the `chrome-extensions` skill for extension code and `modern-web-guidance` before any popup/content-script UI, form, or CSS work (it runs `npx -y modern-web-guidance@latest search|retrieve`; use `npx.cmd` on Windows).
- The skills are installed per checkout, pinned to the commit `ref` in `skills-lock.json` (files gitignored). On a fresh clone, install that same commit for Claude Code:
  `npx -y skills@1.7.0 add "https://github.com/GoogleChrome/modern-web-guidance.git#84ae7251ee919239d5ea85aef25897983f26601e" --skill modern-web-guidance --skill chrome-extensions -a claude-code -y`
  (`skills experimental_install` restores the lockfile but only into `.agents/skills/`, which Claude Code doesn't read.)
- Whenever you create or change extension code, create and maintain `CHROMEWEBSTORE.md` (format per the `chrome-extensions` skill), including a justification for every permission and host permission in `manifest.json`. Seed it from `docs/release/chrome-web-store.md` rather than duplicating it by hand.
- To test in a real browser, use the `chrome-devtools` MCP server (`.mcp.json`): it can install, reload, and inspect the extension's popup, side panel, and service worker. It needs remote debugging turned on at `chrome://inspect/#remote-debugging` in each new Chrome session.

## Closing tracked work

week-sotu and vigil read `docs/TASKS.md` from `main`, so an item left unmarked keeps showing as open work. A PR that finishes a tracked item closes it in the same PR, in this order:

1. Finish the code and tests.
2. Before the **last** push, update the docs in the same branch: mark the `docs/TASKS.md` item `- [x]` with a one-line `Done <date>: <what>` note (or record partial progress; to cite the PR number, open the PR as a draft first and add it in this commit). If the `docs/TASKS.md` footer says finished items are removed rather than ticked, remove it and condense it into `docs/CHANGELOG.md` / `docs/FEATURES.md` instead. Tick or condense the matching `docs/ROADMAP.md` line, add a `docs/CHANGELOG.md` Unreleased line, and fix `README.md` / `docs/FEATURES.md` if the change alters what they claim.
3. Commit and push, then open the PR. Say in its description which items it closes (the PR template has a slot for it).
4. **Pre-merge check**, next to CI and review threads: `git diff origin/main...HEAD --stat` must include the tracking docs whenever the PR completes a tracked item. If it doesn't, add the docs commit before merging. Never merge first and "follow up with a docs PR"; that's how stash#158/#159 and avatar#35 left finished work open (2026-09-30).

**A docs-only status PR changes status, nothing else.** When you do have to close items after the fact, touch only the lines for the items you cite (tick, `Done` note, PR link). Don't add, reword, reorder or delete other items, and don't regenerate the file from a template.
