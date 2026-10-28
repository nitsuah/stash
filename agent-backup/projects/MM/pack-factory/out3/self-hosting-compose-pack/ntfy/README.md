# ntfy
Push notifications to your phone.

    cp .env.example .env   # edit secrets
    docker compose up -d

Publish with curl -d 'hello' http://localhost:8090/mytopic and subscribe in the ntfy app.

Images use `latest` tags; pin a version before relying on it. Back up the named volumes.
