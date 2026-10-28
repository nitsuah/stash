# vaultwarden
Password manager server (Bitwarden-compatible).

    cp .env.example .env   # edit secrets
    docker compose up -d

Signups are off by default; enable briefly to create your account, then turn off. Use HTTPS in production and back up /data.

Images use `latest` tags; pin a version before relying on it. Back up the named volumes.
