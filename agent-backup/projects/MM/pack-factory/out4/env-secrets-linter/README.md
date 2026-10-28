# Env and Secrets Linter
    python envlint.py .
Walks a folder and flags likely secrets (AWS key ids, private key blocks, Slack and GitHub tokens, generic `password=...` style assignments)
and `.env` files that should be git-ignored. Offline and dependency-free; exits 1 when it finds something, so it works in CI or a pre-commit hook.
Pattern-based: it will miss some secrets and flag some harmless strings. If a real secret leaks, rotate it; deleting the line is not enough.

Personal and commercial use. Do not resell or redistribute the files themselves.
