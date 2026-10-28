# nextcloud
Private file sync and sharing.

    cp .env.example .env   # edit secrets
    docker compose up -d

Open http://localhost:8080 and create the admin account. Put it behind HTTPS before exposing it.

Images use `latest` tags; pin a version before relying on it. Back up the named volumes.
