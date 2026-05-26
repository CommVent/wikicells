# infra/

Docker Compose stack + MediaWiki/Wikibase configuration for standing up the
wiki, locally or on a public VPS.

## Contents (planned)

- `docker-compose.yml` — Wikibase Suite stack (Wikibase + MariaDB +
  Elasticsearch + Query Service / Blazegraph).
- `LocalSettings.php` — MediaWiki configuration: Federated Properties enabled,
  CC0 declared for structured data, Wikipedia-style user groups.
- `nginx/` — TLS-terminating reverse proxy config for VPS deployment with
  Let's Encrypt.
- `env.example` — environment variables (admin user, DB password, secret key).

## Local stand-up (planned procedure — not yet implemented)

```bash
cd infra
cp env.example .env   # fill in secrets
docker compose up -d
# wait for the stack to boot, then visit http://localhost:8080
```

## VPS stand-up (planned)

1. Provision a small VPS (≥ 4 GB RAM recommended for the Query Service).
2. Point a domain at it.
3. Edit `nginx/site.conf` with the domain, run the included `letsencrypt.sh`.
4. `docker compose up -d` — the `nginx` service handles TLS termination.

## Source of truth

This stack is based on the upstream
[wmde/wikibase-release-pipeline](https://github.com/wmde/wikibase-release-pipeline)
with pinned versions for reproducibility.
