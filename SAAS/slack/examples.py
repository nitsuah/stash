"""
Slack API Examples
Covers: messages, channels, users, files, reactions, webhooks, pins

Auth:  SLACK_BOT_TOKEN   (xoxb-... Bot User OAuth Token)
       SLACK_WEBHOOK_URL (optional — Incoming Webhook for simple posting)
Docs:  https://api.slack.com/methods

Usage:
    # Read-only demo:
    python SAAS/slack/examples.py

    # Include write operations (sends a test message then deletes it):
    python SAAS/slack/examples.py --demo-write --channel CHANNEL_ID
"""

import argparse
import os
import sys
import time

import requests

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SAAS_DIR   = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, os.path.dirname(_SAAS_DIR))


# ---------------------------------------------------------------------------
# Env + client
# ---------------------------------------------------------------------------

def _load_env(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path, override=False)
        return
    except ImportError:
        pass
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def _require(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        print(f"ERROR: env var '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return val


def load_env(env_file: str | None = None) -> None:
    for p in [env_file,
              os.path.join(_SCRIPT_DIR, ".env"),
              os.path.join(_SAAS_DIR, ".env")]:
        if p and os.path.exists(p):
            _load_env(p)
            return


BASE = "https://slack.com/api"


class SlackClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def get(self, method: str, params: dict | None = None) -> dict:
        r = requests.get(f"{BASE}/{method}", headers=self.headers, params=params)
        r.raise_for_status()
        data = r.json()
        if not data.get("ok"):
            raise RuntimeError(f"Slack error [{method}]: {data.get('error')}")
        return data

    def post(self, method: str, body: dict) -> dict:
        r = requests.post(f"{BASE}/{method}", headers=self.headers, json=body)
        r.raise_for_status()
        data = r.json()
        if not data.get("ok"):
            raise RuntimeError(f"Slack error [{method}]: {data.get('error')}")
        return data

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "SlackClient":
        load_env(env_file)
        return cls(token=_require("SLACK_BOT_TOKEN"))


# ---------------------------------------------------------------------------
# Channels
# ---------------------------------------------------------------------------

def list_channels(client: SlackClient, max_results: int = 20,
                  types: str = "public_channel") -> list[dict]:
    """conversations.list"""
    data = client.get("conversations.list", params={
        "limit": max_results, "types": types, "exclude_archived": True
    })
    channels = data.get("channels", [])
    print(f"\n[Channels ({types})] {len(channels)} returned:")
    for c in channels:
        members = c.get("num_members", "?")
        print(f"  {c['id']}  [{members:>5} members]  #{c['name']}")
    return channels


def get_channel(client: SlackClient, channel_id: str) -> dict:
    """conversations.info"""
    data = client.get("conversations.info", params={"channel": channel_id})
    c = data["channel"]
    print(f"\n[Channel] #{c['name']}  ({c['id']})")
    print(f"  Members: {c.get('num_members','?')}  Archived: {c.get('is_archived')}")
    print(f"  Topic:   {c.get('topic',{}).get('value','') or '(none)'}")
    return c


def list_channel_members(client: SlackClient, channel_id: str,
                          max_results: int = 20) -> list[str]:
    """conversations.members"""
    data = client.get("conversations.members", params={
        "channel": channel_id, "limit": max_results
    })
    members = data.get("members", [])
    print(f"\n[Channel Members] {len(members)} IDs:")
    print(f"  {', '.join(members[:10])}{'...' if len(members) > 10 else ''}")
    return members


def create_channel(client: SlackClient, name: str,
                   is_private: bool = False) -> dict:
    """conversations.create"""
    data = client.post("conversations.create", {"name": name, "is_private": is_private})
    c = data["channel"]
    print(f"\n[Created Channel] #{c['name']}  ({c['id']})")
    return c


def archive_channel(client: SlackClient, channel_id: str) -> None:
    """conversations.archive"""
    client.post("conversations.archive", {"channel": channel_id})
    print(f"\n[Archived Channel] {channel_id}")


def join_channel(client: SlackClient, channel_id: str) -> dict:
    """conversations.join — bot joins a public channel"""
    data = client.post("conversations.join", {"channel": channel_id})
    print(f"\n[Joined Channel] {channel_id}")
    return data.get("channel", {})


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

def send_message(client: SlackClient, channel: str, text: str,
                 blocks: list | None = None, thread_ts: str | None = None) -> dict:
    """chat.postMessage"""
    body: dict = {"channel": channel, "text": text}
    if blocks:
        body["blocks"] = blocks
    if thread_ts:
        body["thread_ts"] = thread_ts
    data = client.post("chat.postMessage", body)
    msg = data["message"]
    print(f"\n[Message sent] ts={msg['ts']}  channel={channel}")
    print(f"  {text[:80]}")
    return msg


def update_message(client: SlackClient, channel: str, ts: str, text: str) -> dict:
    """chat.update"""
    data = client.post("chat.update", {"channel": channel, "ts": ts, "text": text})
    print(f"\n[Message updated] ts={ts}")
    return data["message"]


def delete_message(client: SlackClient, channel: str, ts: str) -> None:
    """chat.delete"""
    client.post("chat.delete", {"channel": channel, "ts": ts})
    print(f"\n[Message deleted] ts={ts}")


def get_permalink(client: SlackClient, channel: str, ts: str) -> str:
    """chat.getPermalink"""
    data = client.get("chat.getPermalink", params={"channel": channel, "message_ts": ts})
    link = data["permalink"]
    print(f"\n[Permalink] {link}")
    return link


def list_messages(client: SlackClient, channel: str, max_results: int = 10) -> list[dict]:
    """conversations.history"""
    data = client.get("conversations.history", params={
        "channel": channel, "limit": max_results
    })
    messages = data.get("messages", [])
    print(f"\n[Messages in {channel}] {len(messages)} returned:")
    for m in messages:
        user = m.get("user", m.get("bot_id", "?"))
        text = (m.get("text") or "")[:60]
        print(f"  {m['ts']}  [{user}]  {text}")
    return messages


def post_webhook(webhook_url: str, text: str,
                 blocks: list | None = None) -> None:
    """POST to an Incoming Webhook URL — no bot token required"""
    body: dict = {"text": text}
    if blocks:
        body["blocks"] = blocks
    r = requests.post(webhook_url, json=body,
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    print(f"\n[Webhook posted] status={r.status_code}  {text[:60]}")


# ---------------------------------------------------------------------------
# Reactions
# ---------------------------------------------------------------------------

def add_reaction(client: SlackClient, channel: str, ts: str,
                 emoji: str = "white_check_mark") -> None:
    """reactions.add"""
    client.post("reactions.add", {"channel": channel, "timestamp": ts, "name": emoji})
    print(f"\n[Reaction added] :{emoji}: → ts={ts}")


def remove_reaction(client: SlackClient, channel: str, ts: str,
                    emoji: str = "white_check_mark") -> None:
    """reactions.remove"""
    client.post("reactions.remove", {"channel": channel, "timestamp": ts, "name": emoji})
    print(f"\n[Reaction removed] :{emoji}: → ts={ts}")


# ---------------------------------------------------------------------------
# Pins
# ---------------------------------------------------------------------------

def pin_message(client: SlackClient, channel: str, ts: str) -> None:
    """pins.add"""
    client.post("pins.add", {"channel": channel, "timestamp": ts})
    print(f"\n[Pinned] ts={ts} in {channel}")


def list_pins(client: SlackClient, channel: str) -> list[dict]:
    """pins.list"""
    data = client.get("pins.list", params={"channel": channel})
    items = data.get("items", [])
    print(f"\n[Pins in {channel}] {len(items)} pinned:")
    for item in items:
        msg = item.get("message", {})
        print(f"  {msg.get('ts','?')}  {(msg.get('text') or '')[:60]}")
    return items


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def list_users(client: SlackClient, max_results: int = 20) -> list[dict]:
    """users.list"""
    data = client.get("users.list", params={"limit": max_results})
    members = [u for u in data.get("members", []) if not u.get("deleted") and not u.get("is_bot")]
    print(f"\n[Users] {len(members)} active humans returned:")
    for u in members[:max_results]:
        print(f"  {u['id']}  {u.get('real_name','?'):30s}  @{u.get('name','?')}")
    return members


def get_user(client: SlackClient, user_id: str) -> dict:
    """users.info"""
    data = client.get("users.info", params={"user": user_id})
    u = data["user"]
    print(f"\n[User] {u['id']}  @{u.get('name')}  ({u.get('real_name')})")
    print(f"  Email: {u.get('profile',{}).get('email','?')}")
    return u


def lookup_user_by_email(client: SlackClient, email: str) -> dict:
    """users.lookupByEmail"""
    data = client.get("users.lookupByEmail", params={"email": email})
    u = data["user"]
    print(f"\n[User by email] {email} → {u['id']}  @{u.get('name')}")
    return u


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

def upload_file(client: SlackClient, channel: str, content: str,
                filename: str = "upload.txt", title: str = "") -> dict:
    """files.getUploadURLExternal + files.completeUploadExternal (v2 API)
    Falls back to files.upload for older token scopes.
    """
    token = client.headers["Authorization"].split()[-1]
    r = requests.post(
        f"{BASE}/files.upload",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "channels": channel,
            "filename": filename,
            "title": title or filename,
            "content": content,
        },
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack error [files.upload]: {data.get('error')}")
    f = data["file"]
    print(f"\n[File uploaded] {f['id']}  {f['name']}")
    return f


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Slack API examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--channel", default=None,
                        help="Channel ID for write demo (overrides SLACK_CHANNEL_ID env var)")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (sends + deletes a test message)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = SlackClient.from_env()

    print(f"\n{'='*60}")
    print("Slack Examples")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    channels = list_channels(client)
    list_users(client)

    if channels:
        first_id = channels[0]["id"]
        get_channel(client, first_id)
        list_messages(client, first_id, max_results=5)
        list_pins(client, first_id)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        channel = args.channel or os.environ.get("SLACK_CHANNEL_ID", "")
        webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")

        if not channel:
            print("\n[Write] Set SLACK_CHANNEL_ID or pass --channel to test messaging")
        else:
            msg = send_message(client, channel,
                               text="[EXAMPLE] API test from SAAS/slack/examples.py — safe to ignore")
            ts = msg["ts"]
            get_permalink(client, channel, ts)
            time.sleep(1)
            add_reaction(client, channel, ts, emoji="robot_face")
            time.sleep(1)
            update_message(client, channel, ts,
                           text="[EXAMPLE] Updated message — safe to ignore")
            time.sleep(1)
            delete_message(client, channel, ts)

        if webhook_url:
            post_webhook(webhook_url,
                         text="[EXAMPLE] Webhook test from SAAS/slack/examples.py — safe to ignore")
        else:
            print("\n[Write] Set SLACK_WEBHOOK_URL to test Incoming Webhooks")


if __name__ == "__main__":
    main()
