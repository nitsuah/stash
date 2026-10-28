# photoprism
Private photo library.

    cp .env.example .env   # edit secrets
    docker compose up -d

Put photos in ./originals. Admin password must be at least 8 characters.

Images use `latest` tags; pin a version before relying on it. Back up the named volumes.
