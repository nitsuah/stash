# Atlassian Cloud API Examples

Python examples for the Atlassian Cloud product suite. Each script is self-contained and runnable independently. All use a shared base client from [`client.py`](client.py).

## Products Covered

| Script | Product | Auth |
|--------|---------|------|
| [`jira/examples.py`](jira/examples.py) | Jira Software · JSM · Assets · Automation | `JIRA_*` |
| [`confluence/examples.py`](confluence/examples.py) | Confluence Cloud | `JIRA_*` (same account) |
| [`bitbucket/examples.py`](bitbucket/examples.py) | Bitbucket Cloud | `BITBUCKET_*` |
| [`statuspage/examples.py`](statuspage/examples.py) | Atlassian Statuspage | `STATUSPAGE_*` |
| [`jira/groovy/users.groovy`](jira/groovy/users.groovy) | Jira Server — ScriptRunner user listing | Jira Server admin |

> **Not covered:** Bamboo (deprecated cloud), Crowd (replaced by Atlassian Access), Jira Data Center  
> **Requires Jira Premium:** Jira Advanced Roadmaps (Plans), Assets — graceful fallback if unavailable

---

## Setup

```bash
# 1. Copy the env template and fill in your credentials
cp atlassian/.env.example atlassian/.env

# 2. Install dependencies
pip install requests python-dotenv
```

### Getting credentials

| Credential | Where to get it |
|------------|----------------|
| `JIRA_TOKEN` | [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) |
| `BITBUCKET_APP_PASSWORD` | [bitbucket.org → Personal settings → App passwords](https://bitbucket.org/account/settings/app-passwords/) |
| `STATUSPAGE_API_KEY` | Statuspage dashboard → API → API Keys |
| `STATUSPAGE_PAGE_ID` | Statuspage dashboard → API → page ID shown at top |

---

## Usage

All scripts default to **read-only** operations. Pass `--demo-write` to also run create/update/delete examples (they clean up after themselves).

### Jira

```bash
# Read-only: lists projects, issues, service desks, asset schemas
python atlassian/jira/examples.py --project MYPROJECT

# Write demo: creates a Task, adds a comment, updates it, deletes it
python atlassian/jira/examples.py --project MYPROJECT --demo-write
```

### Confluence

```bash
# Read-only: lists spaces, pages, runs a search
python atlassian/confluence/examples.py

# Target a specific space; write demo creates then deletes a test page
python atlassian/confluence/examples.py --space MYSPACE --demo-write
```

### Bitbucket

```bash
# Read-only: lists repos, branches, commits, PRs, pipelines
python atlassian/bitbucket/examples.py

# Target a specific repo
python atlassian/bitbucket/examples.py --repo my-repo-slug

# Write demo: creates then deletes a test issue
python atlassian/bitbucket/examples.py --repo my-repo-slug --demo-write
```

### Statuspage

```bash
# Read-only: lists pages, components, incidents
python atlassian/statuspage/examples.py

# Write demo: creates an incident, walks through statuses, deletes it
python atlassian/statuspage/examples.py --demo-write
```

---

## Function Reference

### Jira (`jira/examples.py`)

| Function | Method | Endpoint |
|----------|--------|----------|
| `get_myself` | GET | `/rest/api/3/myself` |
| `list_projects` | GET | `/rest/api/3/project/search` |
| `get_project` | GET | `/rest/api/3/project/{key}` |
| `create_issue` | POST | `/rest/api/3/issue` |
| `get_issue` | GET | `/rest/api/3/issue/{key}` |
| `update_issue` | PUT | `/rest/api/3/issue/{key}` |
| `delete_issue` | DELETE | `/rest/api/3/issue/{key}` |
| `add_comment` | POST | `/rest/api/3/issue/{key}/comment` |
| `search_issues` | GET | `/rest/api/3/search` (JQL) |
| `get_transitions` | GET | `/rest/api/3/issue/{key}/transitions` |
| `transition_issue` | POST | `/rest/api/3/issue/{key}/transitions` |
| `list_custom_fields` | GET | `/rest/api/3/field` |
| `list_service_desks` | GET | `/rest/servicedeskapi/servicedesk` |
| `list_request_types` | GET | `/rest/servicedeskapi/servicedesk/{id}/requesttype` |
| `list_jsm_queues` | GET | `/rest/servicedeskapi/servicedesk/{id}/queue` |
| `create_customer_request` | POST | `/rest/servicedeskapi/request` |
| `list_asset_schemas` | GET | `/rest/assets/1.0/objectschema/list` |
| `list_asset_object_types` | GET | `/rest/assets/1.0/objectschema/{id}/objecttypes/flat` |
| `search_assets` | POST | `/rest/assets/1.0/object/navlist/aql` |
| `list_automation_rules` | GET | `/rest/cb-automation/latest/project/{key}/rule/export` |

### Confluence (`confluence/examples.py`)

| Function | Method | Endpoint |
|----------|--------|----------|
| `list_spaces` | GET | `/wiki/rest/api/space` |
| `get_space` | GET | `/wiki/rest/api/space/{key}` |
| `list_pages_in_space` | GET | `/wiki/rest/api/space/{key}/content/page` |
| `get_page` | GET | `/wiki/rest/api/content/{id}` |
| `create_page` | POST | `/wiki/rest/api/content` |
| `update_page` | PUT | `/wiki/rest/api/content/{id}` |
| `delete_page` | DELETE | `/wiki/rest/api/content/{id}` |
| `search_content` | GET | `/wiki/rest/api/search` (CQL) |
| `get_page_labels` | GET | `/wiki/rest/api/content/{id}/label` |
| `add_label` | POST | `/wiki/rest/api/content/{id}/label` |

### Bitbucket (`bitbucket/examples.py`)

| Function | Method | Endpoint |
|----------|--------|----------|
| `list_repos` | GET | `/2.0/repositories/{workspace}` |
| `get_repo` | GET | `/2.0/repositories/{workspace}/{slug}` |
| `create_repo` | POST | `/2.0/repositories/{workspace}/{slug}` |
| `delete_repo` | DELETE | `/2.0/repositories/{workspace}/{slug}` |
| `list_branches` | GET | `/2.0/repositories/{workspace}/{slug}/refs/branches` |
| `list_commits` | GET | `/2.0/repositories/{workspace}/{slug}/commits/{branch}` |
| `list_pull_requests` | GET | `/2.0/repositories/{workspace}/{slug}/pullrequests` |
| `get_pull_request` | GET | `/2.0/repositories/{workspace}/{slug}/pullrequests/{id}` |
| `create_pull_request` | POST | `/2.0/repositories/{workspace}/{slug}/pullrequests` |
| `list_pipelines` | GET | `/2.0/repositories/{workspace}/{slug}/pipelines` |
| `trigger_pipeline` | POST | `/2.0/repositories/{workspace}/{slug}/pipelines` |
| `list_issues` | GET | `/2.0/repositories/{workspace}/{slug}/issues` |
| `create_issue` | POST | `/2.0/repositories/{workspace}/{slug}/issues` |
| `list_webhooks` | GET | `/2.0/repositories/{workspace}/{slug}/hooks` |

### Statuspage (`statuspage/examples.py`)

| Function | Method | Endpoint |
|----------|--------|----------|
| `list_pages` | GET | `/v1/pages` |
| `get_page` | GET | `/v1/pages/{page_id}` |
| `list_components` | GET | `/v1/pages/{page_id}/components` |
| `create_component` | POST | `/v1/pages/{page_id}/components` |
| `update_component_status` | PATCH | `/v1/pages/{page_id}/components/{id}` |
| `delete_component` | DELETE | `/v1/pages/{page_id}/components/{id}` |
| `list_incidents` | GET | `/v1/pages/{page_id}/incidents` |
| `get_incident` | GET | `/v1/pages/{page_id}/incidents/{id}` |
| `create_incident` | POST | `/v1/pages/{page_id}/incidents` |
| `update_incident` | PATCH | `/v1/pages/{page_id}/incidents/{id}` |
| `delete_incident` | DELETE | `/v1/pages/{page_id}/incidents/{id}` |
| `list_scheduled_maintenances` | GET | `/v1/pages/{page_id}/incidents/scheduled` |

---

## Also in this directory

- [`jira/validate_project.py`](jira/validate_project.py) — validates a Jira project's full configuration (workflows, issue types, custom fields, lifecycle suites)
