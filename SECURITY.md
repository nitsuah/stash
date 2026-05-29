# Security Policy

## Supported Versions

Only the latest state of `main` is actively maintained.

| Version | Supported |
|---------|-----------|
| `main` (latest) | ✅ |
| Older commits | ❌ |

---

## Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub issues.**

Email: **nitsuahlabs@gmail.com**

You can expect:
- **Acknowledgment** within 48 hours
- **Status update** within 7 days
- **Credit** in the changelog unless you prefer to remain anonymous

### What to include

- Type of issue (credential exposure, injection, path traversal, etc.)
- File path(s) and line numbers
- Steps to reproduce or proof-of-concept
- Impact assessment

---

## Security Practices for Contributors

### Credentials & secrets
- Never commit API keys, tokens, passwords, or session cookies
- Never commit `.pem`, `.p12`, `.key`, `.pfx`, or any credential file
- Use `.env` files (gitignored) — see `.env.example` in each subdirectory
- Use placeholder values in examples: `YOUR_API_KEY`, `LDAP_HOST`, `example.com`

### Scripts & automation
- **Python** — use `os.environ` or `python-dotenv`; never hardcode credentials
- **PowerShell** — use environment variables or Windows Credential Manager; never `-w PASSWORD` literals
- **Bash/UserData** — use SSM Parameter Store for secrets at runtime; see commented examples in `IAS/`
- **VBA/Access** — sanitize connection strings; use sample databases, never production DSNs

### Data in examples
- No PII, internal hostnames, or org-specific URLs in committed files
- Replace real resource IDs with generic placeholders (`PARENT-1`, `MYPROJECT`, `owner/repo`)
- Audit any CSVs or JSON sample data for sensitive fields before committing

---

## Disclosure Policy

1. Confirm the issue and determine affected files
2. Audit for similar patterns elsewhere in the repo
3. Push a fix to `main` with a clear commit message
4. Note it in `CHANGELOG.md` under Security
