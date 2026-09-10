# Jira Script Operations Runbook

Safe execution guidance for all Atlassian scripts in this directory.

---

## Prerequisites

1. **Python 3.10+** installed and on PATH.
2. **Dependencies installed:**
   ```bash
   pip install requests python-dotenv
   ```
3. **Credentials configured** — copy the env template and fill in your values:
   ```bash
   cp atlassian/.env.example atlassian/.env
   ```

### Required environment variables

| Variable | Where to get it |
|----------|----------------|
| `JIRA_HOST` | Your Jira Cloud base URL — `https://yourorg.atlassian.net` |
| `JIRA_EMAIL` | Atlassian account email |
| `JIRA_TOKEN` | [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) |
| `BITBUCKET_WORKSPACE` | Bitbucket workspace slug |
| `BITBUCKET_USERNAME` | Bitbucket username |
| `BITBUCKET_APP_PASSWORD` | [bitbucket.org → Personal settings → App passwords](https://bitbucket.org/account/settings/app-passwords/) |
| `STATUSPAGE_API_KEY` | Statuspage dashboard → API → API Keys |
| `STATUSPAGE_PAGE_ID` | Statuspage dashboard → API → page ID shown at top |

---

## `atlassian/jira/examples.py`

### Risk level: Low (read-only default) / Medium (--demo-write)

**Read-only (safe):**
```bash
# Lists your projects, issues, service desks, and asset schemas — no writes
python atlassian/jira/examples.py --project MYPROJECT
```

**Write demo:**
```bash
# Creates a Task, adds a comment, updates it, then DELETES it
# All objects created with "[EXAMPLE]" prefix and cleaned up in finally block
python atlassian/jira/examples.py --project MYPROJECT --demo-write
```

**Risk mitigation:**
- Write operations require `--demo-write` opt-in.
- All created issues have `[EXAMPLE]` in the summary and are deleted in a `finally` block even if an error occurs.
- Run read-only first to verify credentials and target project before using `--demo-write`.

---

## `atlassian/jira/validate_project.py`

### Risk level: Medium (creates and deletes Jira issues)

**Usage:**
```bash
# Validates a project's workflows, issue types, custom fields
python atlassian/jira/validate_project.py --project MYPROJECT
```

**Risk mitigation:**
- Creates test issues with `[VALIDATION]` prefix during lifecycle tests.
- Deletes all test issues in `finally` blocks regardless of success or failure.
- Do not interrupt mid-run (Ctrl+C) — test issues may be left behind if the script is killed before cleanup.
- To check for leftover issues: `python atlassian/jira/examples.py --project MYPROJECT` and filter for `[VALIDATION]` in the summary.

**Permissions required:**
- Create issue, Edit issue, Delete issue in the target project.
- If using a read-only token, the script will fail at the first write operation with a 403.

---

## `atlassian/confluence/examples.py`

### Risk level: Low (read-only default) / Low-Medium (--demo-write)

**Read-only:**
```bash
python atlassian/confluence/examples.py
python atlassian/confluence/examples.py --space MYSPACE
```

**Write demo:**
```bash
# Creates a test page in the target space, then deletes it
python atlassian/confluence/examples.py --space MYSPACE --demo-write
```

**Risk mitigation:**
- Creates pages with `[EXAMPLE]` in the title; deletes them in `finally` blocks.
- Uses the same Jira credentials — verify `JIRA_EMAIL` and `JIRA_TOKEN` are set.

---

## `atlassian/bitbucket/examples.py`

### Risk level: Low (read-only default) / Low-Medium (--demo-write)

**Read-only:**
```bash
python atlassian/bitbucket/examples.py
python atlassian/bitbucket/examples.py --repo my-repo-slug
```

**Write demo:**
```bash
# Creates an issue in the target repo, then deletes it
python atlassian/bitbucket/examples.py --repo my-repo-slug --demo-write
```

**Risk mitigation:**
- Requires the Bitbucket App Password to have `Issues: write` permission for `--demo-write`.
- Issue creation is idempotent enough that duplicate runs leave at most one test issue if interrupted.

---

## `atlassian/statuspage/examples.py`

### Risk level: Low (read-only default) / Medium (--demo-write)

**Read-only:**
```bash
# Lists pages, components, incidents — no writes
python atlassian/statuspage/examples.py
```

**Write demo:**
```bash
# Creates an incident, walks through Investigating → Identified → Monitoring → Resolved, then deletes
python atlassian/statuspage/examples.py --demo-write
```

**Risk mitigation:**
- Incident creation is visible to Statuspage subscribers if your page is public — run write demos against a non-production test page where possible.
- The incident is resolved and deleted in a `finally` block, but subscribers may receive email notifications during the demo run.
- Set `STATUSPAGE_PAGE_ID` to a hidden or maintenance page for safe testing.

---

## `atlassian/jira/groovy/users.groovy`

### Risk level: Low (read-only)

Run via the ScriptRunner console in Jira Server/DC:
1. Admin → ScriptRunner → Script Console
2. Paste contents of `users.groovy`
3. Run — outputs a list of all user accounts

No writes performed.

---

## `atlassian/jira/automation/`

These are Jira Automation rule export files (JSON). They are **not scripts** — import them via:

Jira project → Project settings → Automation → Import rule → upload the `.json` file.

| File | What it does |
|------|-------------|
| `reopen-on-reply.json` | Reopens a resolved issue when a comment is added |
| `set-parent-on-resolve.json` | Sets parent issue status when all child issues resolve |

**Review the rule trigger and condition before importing** — automation rules fire on real project events.

---

## Shared Base Client (`atlassian/client.py`)

`client.py` is used by all Atlassian example scripts. It handles:
- Loading credentials from `.env`
- Basic auth construction
- Shared `get`, `post`, `put`, `delete` methods that return raw responses; error handling is performed by the calling layer (e.g., `validate_*` functions)

Do not modify `client.py` for one-off credential overrides — use environment variables instead.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | Wrong token or email | Verify `JIRA_EMAIL` and `JIRA_TOKEN` in `.env` |
| `403 Forbidden` | Missing project permission | Check token account's permissions in Jira project settings |
| `404 Not Found` | Wrong project key or URL | Verify `JIRA_HOST` (no trailing slash) and project key case |
| `429 Too Many Requests` | Rate limited | Wait and retry; Atlassian Cloud rate limits vary by tier |
| Issues not cleaned up | Script killed before `finally` | Search Jira for `[EXAMPLE]` or `[VALIDATION]` in summary; delete manually |
