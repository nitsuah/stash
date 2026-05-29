# GitHub Copilot Instructions

Custom instructions for GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Stash
**Description:** Personal technical reference repository — API examples, automation scripts, infrastructure templates, AI agent prompts, and VBA/Access tools accumulated over 15+ years of enterprise engineering work.
**Primary Languages:** Python, PowerShell, Bash, VBA, Groovy, HTML/JS

---

## Code Style & Conventions

- Follow existing patterns and file structure in each subdirectory.
- Write self-documenting code with clear variable and function names.
- Add comments only when intent is non-obvious — never restate what the code does.
- No magic numbers; no hardcoded credentials or secrets.

### Python
- Target Python 3.10+ (`type | None`, `match`, etc.)
- Use `requests` for HTTP; `python-dotenv` for env loading.
- Scripts should be runnable standalone with a `main()` and `if __name__ == "__main__"` guard.
- Prefer explicit `r.raise_for_status()` over manual status checks.

### PowerShell
- Use `$ErrorActionPreference = "Stop"` in bootstrap/infra scripts.
- Quote all paths; use `Write-Log` or `Write-Host` with `-ForegroundColor` for visibility.
- Prefer `param()` blocks over positional args for reusable scripts.

### Bash
- Start with `set -euo pipefail`.
- Use `echo ">>> ..."` for stage headers in bootstrap scripts.

### VBA
- Use `Option Explicit` on all modules.
- Wrap COM object use in `Try...Catch` equivalents (`On Error GoTo`).

---

## Security

- Never commit secrets, API keys, or credentials — use `.env` files (gitignored).
- Validate inputs at system boundaries; trust internal calls.
- Use parameterized queries when interacting with databases.

---

## File Organization

- `atlassian/` — Atlassian Cloud API examples (Python)
- `SAAS/` — SaaS platform API examples (Python)
- `IAS/` — EC2 UserData bootstrap scripts (Bash / PowerShell)
- `agent/` — AI agent role prompts (Markdown)
- `git/` — Git maintenance utilities (PowerShell)
- `windows/` — Windows automation (Batch, PowerShell, VBA)
- `projects/` — Standalone tools (Access/VBA, HTML, circuit design)

---

## Documentation

- Update the relevant `README.md` when adding new scripts or changing behavior.
- Root `README.md` links out to folder-level READMEs — keep it concise.
- Do not create documentation for obvious one-liners.
