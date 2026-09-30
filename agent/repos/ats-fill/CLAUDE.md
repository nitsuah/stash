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
