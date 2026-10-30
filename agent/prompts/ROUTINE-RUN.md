# ROUTINE-RUN

Run a model-driven routine **locally** through `claude -p` and the 9router proxy (the imps kit's runner) instead of the Claude plan quota. Rule: **deterministic first, model only on changed data.** A zero-model `--pre` step decides whether the model runs at all.

- **Runner:** `agent/scripts/routine-run.mjs` reuses `runClaude` and `cleanEnv` from the imps kit (path in `~/.imps/kit-path.txt`; the kit is not modified). The proxy key stays in the user's own settings; nothing secret lives in this repo.
- **Audit:** `agent/scripts/local-audit.mjs` is the zero-model [[CATCHUP]] "Local jobs audit" (read-only, exit 1 on any RED).

## Flow

1. Lock `<out>/.<routine>.lock` (a lock older than 3 h is stale and replaced).
2. Run `--pre`. Exit equal to `--skip-exit` (default 3) logs `idle` and stops, with no model call. Any other non-zero fails open (logged, model still runs, failure noted in the prompt), like the kit's `precheck.mjs`.
3. Probe 9router; if it is down, log `skip-9router-down` and stop.
4. Invoke with a short inline prompt: `Read <file> and follow it. Pre-step output:` plus the first 8 KB of the pre-step stdout.
5. Write the final text to `<out>/<date>.md` and append `date | routine | outcome | turns | tokens` to `--log`.

Flags: `--prompt` (required) `--model MAX` `--tools "Read,Bash(node *),Write"` `--budget <usd>` `--max-turns 30` `--minutes 15` `--pre "<cmd>"` `--skip-exit 3` `--log <file>` `--cwd <dir>` `--out <dir>`. Output and logs default under `agent/logs/` (gitignored).

## Task Scheduler example (not registered by this repo)

```
schtasks /Create /TN "routine-week-example" /SC WEEKLY /D MON /ST 08:00 /TR "node C:\Users\<you>\code\stash\agent\scripts\routine-run.mjs --cwd C:\Users\<you>\code\stash --prompt agent/prompts/EXAMPLE.md --pre \"node agent/scripts/precheck-example.mjs\" --skip-exit 3 --tools \"Read,Write\" --budget 1"
```

Add the new task to the [[CATCHUP]] audit table and `KNOWN_TASKS` in `local-audit.mjs` in the same PR, or the audit flags it as unknown.

## Limits

- No MCP servers (`--strict-mcp-config`), so no `get_usage`, Gmail, Calendar or vigil tools. Routines that need those stay on the cloud or Claude plan.
- The kit denies PowerShell, WebFetch, WebSearch, Task and Skill.
- Windows caps a command line near 32 KB and there is no stdin path, which is why the prompt is short and the pre-step output is truncated.
- Turn cap is enforced by the kit (the CLI ignores `--max-turns`); a capped run exits 1 with outcome `killed-max-turns`.
- Models are whatever 9router serves; quality varies, so keep prompts narrow and the tool list small.
