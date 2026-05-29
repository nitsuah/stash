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
