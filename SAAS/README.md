# SAAS

Python API examples for SaaS platforms used in enterprise automation and operations.

## Setup

```bash
cp SAAS/.env.example SAAS/.env   # add your credentials
pip install requests python-dotenv
```

Each script auto-loads credentials from (in order):
1. `--env-file` flag
2. `SAAS/<service>/.env`
3. `SAAS/.env`

## Services

| Script | Covers | Auth |
|--------|--------|------|
| [`pagerduty/examples.py`](pagerduty/examples.py) | Incidents, services, on-call, schedules, events | `PAGERDUTY_API_KEY` + `PAGERDUTY_ROUTING_KEY` |
| [`slack/examples.py`](slack/examples.py) | Messages, channels, users, files, reactions, webhooks | `SLACK_BOT_TOKEN` |
| [`github/examples.py`](github/examples.py) | Repos, issues, PRs, Actions, releases, orgs, webhooks | `GITHUB_TOKEN` |
| [`datadog/examples.py`](datadog/examples.py) | Metrics, monitors, dashboards, incidents, logs, downtimes | `DATADOG_API_KEY` + `DATADOG_APP_KEY` |

---

## PagerDuty

**Docs:** https://developer.pagerduty.com/api-reference/

Uses two separate auth mechanisms:
- **REST API** (`api.pagerduty.com`) — account/team API key for resource management
- **Events API v2** (`events.pagerduty.com`) — service integration routing key for alert ingestion

### Quick start

```bash
# Read-only (lists services, on-call, incidents):
python SAAS/pagerduty/examples.py

# Write demo (creates then resolves a test incident + event):
python SAAS/pagerduty/examples.py --demo-write --service-id <SERVICE_ID>
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PAGERDUTY_API_KEY` | Yes | REST API key — Integrations → API Access Keys |
| `PAGERDUTY_ROUTING_KEY` | Write demo | Events API v2 service integration key (32 chars) |
| `PAGERDUTY_SERVICE_ID` | Write demo | Default service ID for incident creation |
| `PAGERDUTY_ESCALATION_POLICY_ID` | No | Default escalation policy for incident creation |

### Function reference

| Function | Method | Description |
|----------|--------|-------------|
| `list_incidents` | `GET /incidents` | Active triggered/acknowledged incidents |
| `get_incident` | `GET /incidents/{id}` | Incident detail |
| `create_incident` | `POST /incidents` | Create a new incident |
| `update_incident_status` | `PUT /incidents/{id}` | Acknowledge or resolve |
| `add_note` | `POST /incidents/{id}/notes` | Add a note to an incident |
| `send_event` | Events API v2 `/v2/enqueue` | Trigger, acknowledge, or resolve an alert |
| `list_services` | `GET /services` | All services |
| `get_service` | `GET /services/{id}` | Service detail |
| `list_escalation_policies` | `GET /escalation_policies` | All escalation policies |
| `list_oncall` | `GET /oncalls` | Current on-call assignments |
| `list_schedules` | `GET /schedules` | All on-call schedules |
| `get_schedule` | `GET /schedules/{id}` | Schedule with rendered entries |
| `list_users` | `GET /users` | All users |
| `list_teams` | `GET /teams` | All teams |

---

## Slack

**Docs:** https://api.slack.com/methods

### Quick start

```bash
# Read-only (lists channels and users, reads recent messages):
python SAAS/slack/examples.py

# Write demo (sends a test message, reacts, updates, then deletes it):
python SAAS/slack/examples.py --demo-write --channel C0123456789
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Bot User OAuth Token (`xoxb-...`) — api.slack.com → Your Apps → OAuth |
| `SLACK_CHANNEL_ID` | Write demo | Default channel for messaging examples |
| `SLACK_WEBHOOK_URL` | No | Incoming Webhook URL for simple posting (no bot token needed) |

**Required bot token scopes:**
`channels:read`, `channels:write`, `chat:write`, `files:write`, `pins:read`, `pins:write`, `reactions:write`, `users:read`, `users:read.email`

### Function reference

| Function | Method | Description |
|----------|--------|-------------|
| `list_channels` | `conversations.list` | Public/private channels |
| `get_channel` | `conversations.info` | Channel detail and topic |
| `list_channel_members` | `conversations.members` | Member user IDs |
| `create_channel` | `conversations.create` | Create a public or private channel |
| `archive_channel` | `conversations.archive` | Archive a channel |
| `join_channel` | `conversations.join` | Bot joins a public channel |
| `send_message` | `chat.postMessage` | Post a message (supports blocks, threads) |
| `update_message` | `chat.update` | Edit a posted message |
| `delete_message` | `chat.delete` | Delete a message |
| `get_permalink` | `chat.getPermalink` | Get a permanent link to a message |
| `list_messages` | `conversations.history` | Recent messages in a channel |
| `post_webhook` | Incoming Webhook | Post via webhook URL (no bot token) |
| `add_reaction` | `reactions.add` | Add emoji reaction to a message |
| `remove_reaction` | `reactions.remove` | Remove emoji reaction |
| `pin_message` | `pins.add` | Pin a message in a channel |
| `list_pins` | `pins.list` | All pinned items in a channel |
| `list_users` | `users.list` | All active non-bot users |
| `get_user` | `users.info` | User profile detail |
| `lookup_user_by_email` | `users.lookupByEmail` | Find user by email address |
| `upload_file` | `files.upload` | Upload text content as a file |

---

## GitHub

**Docs:** https://docs.github.com/en/rest

### Quick start

```bash
# Read-only (lists repos, issues, PRs, workflows):
python SAAS/github/examples.py --repo owner/repo

# Write demo (creates then closes a test issue):
python SAAS/github/examples.py --demo-write --repo owner/repo
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | Personal Access Token — github.com → Settings → Developer settings → PAT |
| `GITHUB_REPO` | Read demo | Default repo in `owner/repo` format |
| `GITHUB_ORG` | Org examples | Default org slug |

**Required token scopes:** `repo`, `read:org`, `workflow` (for Actions triggers)

### Function reference

| Function | Method | Description |
|----------|--------|-------------|
| `get_authenticated_user` | `GET /user` | Current token identity |
| `list_repos` | `GET /user/repos` | Repos sorted by last updated |
| `get_repo` | `GET /repos/{owner}/{repo}` | Repo detail, stars, open issues |
| `list_branches` | `GET /repos/.../branches` | All branches with protected flag |
| `list_commits` | `GET /repos/.../commits` | Recent commits with author and message |
| `list_releases` | `GET /repos/.../releases` | Releases and pre-releases |
| `list_contributors` | `GET /repos/.../contributors` | Sorted by commit count |
| `list_issues` | `GET /repos/.../issues` | Open or closed issues (excludes PRs) |
| `get_issue` | `GET /repos/.../issues/{n}` | Issue detail |
| `create_issue` | `POST /repos/.../issues` | Create issue with labels |
| `update_issue` | `PATCH /repos/.../issues/{n}` | Update state, title, or body |
| `add_issue_comment` | `POST /repos/.../issues/{n}/comments` | Add a comment |
| `list_pull_requests` | `GET /repos/.../pulls` | Open or closed PRs |
| `get_pull_request` | `GET /repos/.../pulls/{n}` | PR detail with diff stats |
| `list_pr_reviews` | `GET /repos/.../pulls/{n}/reviews` | Review states per reviewer |
| `list_workflows` | `GET /repos/.../actions/workflows` | All workflow definitions |
| `list_workflow_runs` | `GET /repos/.../actions/runs` | Recent CI runs with status |
| `get_workflow_run` | `GET /repos/.../actions/runs/{id}` | Run detail |
| `trigger_workflow` | `POST /repos/.../actions/workflows/{id}/dispatches` | Trigger a workflow_dispatch |
| `get_org` | `GET /orgs/{org}` | Org detail |
| `list_org_members` | `GET /orgs/{org}/members` | Org member list |
| `list_org_teams` | `GET /orgs/{org}/teams` | Teams with member counts |
| `list_repo_webhooks` | `GET /repos/.../hooks` | Repo webhook configs |

---

## Datadog

**Docs:** https://docs.datadoghq.com/api/latest/

### Quick start

```bash
# Read-only (lists hosts, monitors, dashboards, logs):
python SAAS/datadog/examples.py

# Write demo (submits metric + event, creates then deletes a monitor):
python SAAS/datadog/examples.py --demo-write
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATADOG_API_KEY` | Yes | API key — Organization Settings → API Keys |
| `DATADOG_APP_KEY` | Yes | App key — Organization Settings → Application Keys |
| `DATADOG_SITE` | No | Default: `datadoghq.com` — use `datadoghq.eu` for EU |

### Function reference

| Function | API | Description |
|----------|-----|-------------|
| `query_metrics` | `GET /query` | Time-series query (DogStatsD syntax) |
| `list_active_metrics` | `GET /metrics` | Metrics seen in last N seconds |
| `submit_metric` | `POST /series` | Submit a custom gauge/count/rate |
| `list_monitors` | `GET /monitor` | All monitors with state |
| `get_monitor` | `GET /monitor/{id}` | Monitor detail and query |
| `create_monitor` | `POST /monitor` | Create a metric alert monitor |
| `mute_monitor` | `POST /monitor/{id}/mute` | Mute with optional end time |
| `delete_monitor` | `DELETE /monitor/{id}` | Delete a monitor |
| `list_dashboards` | `GET /dashboard` | All dashboards |
| `get_dashboard` | `GET /dashboard/{id}` | Dashboard detail and widget count |
| `list_hosts` | `GET /hosts` | Active hosts with integrations |
| `get_host_totals` | `GET /hosts/totals` | Total active / up host counts |
| `list_downtimes` | `GET /downtime` | Current maintenance windows |
| `create_downtime` | `POST /downtime` | Schedule a maintenance window |
| `cancel_downtime` | `DELETE /downtime/{id}` | Cancel a downtime |
| `list_events` | `GET /events` | Events in last N seconds |
| `post_event` | `POST /events` | Post a custom event |
| `search_logs` | `POST /logs/events/search` (v2) | Full-text log search |
| `list_incidents` | `GET /incidents` (v2) | Incidents (requires Incident Management) |
