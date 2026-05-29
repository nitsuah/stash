# Contributing to stash

This is a personal technical reference repository. Contributions are welcome — bug fixes, additional examples, and improvements to existing scripts.

---

## Getting Started

```bash
git clone https://github.com/nitsuah/stash.git
cd stash
git checkout -b feature/your-feature-name
```

---

## What's in Scope

- **New API examples** — following the pattern in `atlassian/`, `SAAS/`, or `CLOUD/`
- **Bug fixes** — broken scripts, incorrect API calls, outdated endpoints
- **Documentation** — improving READMEs, adding missing descriptions
- **New utilities** — scripts that fit an existing category (`windows/`, `git/`, `IAS/`)

For major additions, open an issue first to discuss.

---

## Development Setup

No single build system — each subdirectory is self-contained.

**Python scripts** (atlassian/, SAAS/, CLOUD/):
```bash
pip install requests python-dotenv boto3
cp <dir>/.env.example <dir>/.env   # fill in credentials
python <script>.py
```

**PowerShell scripts** (windows/pwsh/, git/):
```powershell
# Run directly — no install needed
.\script.ps1 -DryRun
```

**Bash scripts** (IAS/):
```bash
chmod +x IAS/ubuntu-userdata.sh
# Deploy via EC2 UserData — not run locally
```

---

## Pull Request Checklist

Before submitting:

- [ ] No secrets committed — tokens, passwords, API keys, `.pem`, `.key`, credential files
- [ ] No internal hostnames, IPs, or org-specific URLs — use `example.com` / `LDAP_HOST` placeholders
- [ ] No PII or sensitive data in examples or sample files
- [ ] `.gitignore` updated if new credential/config file types are introduced
- [ ] Relevant README updated (root `README.md` if adding a new top-level section)
- [ ] Script includes a usage example (docstring or README)
- [ ] Required permissions documented (IAM policies, API scopes, token scopes)

---

## Coding Standards

### Python
- Python 3.10+ (`type | None` union syntax, match statements)
- `requests` for HTTP, `python-dotenv` for env loading
- Scripts runnable standalone with `main()` + `if __name__ == "__main__"` guard
- No comments that restate what the code does

### PowerShell
- `$ErrorActionPreference = "Stop"` in bootstrap/infra scripts
- `param()` blocks with named parameters for reusable scripts
- `-DryRun` / `-Force` flags where destructive operations are involved

### Bash
- `set -euo pipefail`
- `echo ">>> ..."` for stage headers in bootstrap scripts

### VBA
- `Option Explicit` on all modules

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Splunk API examples
fix: correct PagerDuty Events API dedup_key field
docs: update atlassian README with groovy script entry
chore: remove stale ias/ scratchpad folder
```

---

## Questions

Open an issue or reach out via [nitsuah.io](https://nitsuah.io).
