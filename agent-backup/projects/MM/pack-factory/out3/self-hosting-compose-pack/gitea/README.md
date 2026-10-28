# gitea
Self-hosted Git service.

    cp .env.example .env   # edit secrets
    docker compose up -d

Open http://localhost:3002 and finish the install page. SSH is on port 2222.

Images use `latest` tags; pin a version before relying on it. Back up the named volumes.
