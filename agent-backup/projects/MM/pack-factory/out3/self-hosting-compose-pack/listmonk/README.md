# listmonk
Newsletter and mailing lists.

    cp .env.example .env   # edit secrets
    docker compose up -d

First run may need `docker compose run --rm app ./listmonk --install` (see listmonk docs). You need an SMTP provider to send mail; follow anti-spam laws.

Images use `latest` tags; pin a version before relying on it. Back up the named volumes.
