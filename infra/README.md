# infra/

Docker Compose stack + MediaWiki/Wikibase configuration for standing up the
wiki, locally or on a public VPS.

## Contents

- `docker-compose.yml` — the Wikibase Suite stack (Wikibase + MariaDB +
  Elasticsearch + WDQS/Blazegraph + QuickStatements) behind a **Traefik 3**
  reverse proxy that terminates TLS and issues Let's Encrypt certificates.
- `docker-compose.local.yml` — a **localhost-only** Compose override:
  disables Let's Encrypt and switches every public URL to `http://`. Used
  only for the local dry-run; never used in production.
- `env.example` — template for `infra/.env` (hostnames, admin user, DB
  password). `infra/.env` is gitignored.
- `config/` — MediaWiki/Wikibase overrides (`Extensions.php`), Traefik
  routing (`traefik-dynamic.yml`), and branding assets (`config/branding/`,
  stored via git-lfs).

## Local stand-up (dry-run)

```bash
cp infra/env.example infra/.env   # set wiki.localhost / query.localhost + throwaway secrets
docker compose -f infra/docker-compose.yml -f infra/docker-compose.local.yml up -d
# browse http://wiki.localhost/  (add /etc/hosts entries → 127.0.0.1 if .localhost doesn't resolve)
```

## Production VPS stand-up

The stack is containerized, so the host OS only needs Docker, the Compose
plugin, git, and git-lfs. **Debian (latest stable) or Ubuntu LTS both work**;
the Docker install below auto-detects the distro.

### 0. Prerequisites (decide before provisioning)

- **Domain** — wikicells' own deployment uses **`wikicells.org`**, served as
  `wiki.wikicells.org` (the wiki) and `query.wikicells.org` (the SPARQL UI).
  You must be able to set DNS records for these. *(Deploying your own
  instance? Substitute your domain for `<domain>` throughout.)*
- **VPS size** — **≥ 4 GB RAM / ≥ 40 GB SSD** is the floor; **8 GB is
  recommended** because Elasticsearch + Blazegraph + MariaDB + MediaWiki
  together make 4 GB tight.
- **Admin identity** — a username and a *real* email. The email doubles as
  the Let's Encrypt registration contact.

### 1. Server baseline

Create a non-root sudo user, install your SSH key, disable password SSH, then
open only the ports the stack needs:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp      # ACME HTTP-01 challenge + HTTPS redirect
sudo ufw allow 443/tcp     # TLS
sudo ufw enable
```

### 2. DNS

Create **A records** for `wiki.<domain>` and `query.<domain>` pointing at the
VPS public IP. **Wait for propagation** (`dig +short wiki.<domain>` returns the
VPS IP) before bringing the stack up — otherwise Let's Encrypt's HTTP-01
challenge fails and repeated failures can hit its rate limit.

### 3. Install Docker, Compose, git-lfs

Docker's official repository, distro-agnostic (works on both Debian and
Ubuntu via the `$ID` / `$VERSION_CODENAME` substitution):

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL "https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg" -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin git git-lfs
sudo usermod -aG docker "$USER"   # log out / back in for this to take effect
git lfs install
```

### 4. Clone the repo

```bash
git clone git@github.com:CommVent/wikicells.git
cd wikicells
git lfs pull   # REQUIRED: the logo in config/branding/ is LFS-tracked.
               # Skip this and the container mounts a pointer file, not the PNG.
```

### 5. Fill in `infra/.env` (production values)

> **Generate fresh secrets — never reuse local dry-run passwords.**

```bash
cp infra/env.example infra/.env
openssl rand -base64 24   # → MW_ADMIN_PASS
openssl rand -base64 24   # → DB_PASS
```

Checklist for `infra/.env`:

| Variable | Value |
| -------- | ----- |
| `WIKIBASE_PUBLIC_HOST` | `wiki.<domain>` |
| `WDQS_PUBLIC_HOST` | `query.<domain>` |
| `MW_ADMIN_NAME` | your admin username |
| `MW_ADMIN_EMAIL` | real email (also the Let's Encrypt contact) |
| `MW_ADMIN_PASS` | generated above |
| `DB_NAME` / `DB_USER` | defaults (`my_wiki` / `sqluser`) are fine |
| `DB_PASS` | generated above |
| `METADATA_CALLBACK` | `true` (send anonymous deploy telemetry to wmde) or `false` |

### 6. (Recommended) Validate with Let's Encrypt *staging* first

Production Let's Encrypt has a low rate limit for failed issuance. Before the
real run, point Traefik at the staging CA to confirm DNS + firewall are
correct. In `docker-compose.yml`, **uncomment** this line under the `traefik`
service `command:`:

```yaml
- "--certificatesresolvers.letsencrypt.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"
```

Bring the stack up (step 7). A staging cert will be issued — the browser shows
a "not trusted" warning, which is expected and *proves issuance works*. Then
switch to production certs:

```bash
docker compose down
docker volume rm wikicells_traefik-letsencrypt-data   # discard the staging cert cache
# re-comment the caserver line above
docker compose up -d                                  # now issues a real, trusted cert
```

### 7. Launch

```bash
cd infra
docker compose up -d        # NO override file — production uses the canonical compose
docker compose logs -f traefik     # watch for certificate issuance
docker compose ps                  # all services should reach healthy (first boot 3–5 min)
```

### 8. Seed the wiki

Log in as admin → `Special:BotPasswords` → create a credential pair for the
seed loader, then:

```bash
cd ../bots
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export WIKIBASE_BOT_USER='Admin@<botname>'
export WIKIBASE_BOT_PASS='<generated-bot-password>'
python seed_load.py --host wiki.<domain>     # https is the default; no --http in production
```

### 9. Verify

```bash
curl -I https://wiki.<domain>/        # HTTP/2 200 with a valid (non-staging) cert
```

- `Special:Version` shows Wikibase loaded.
- `Special:RecentChanges` shows the bot's seed edits.
- Properties, the class item, status items, the open-questions rows, and the
  prose pages are all present.
- Assign admin / oversighter roles via `Special:UserRights`.

## Source of truth

This stack is adapted from the upstream
[wmde/wikibase-release-pipeline](https://github.com/wmde/wikibase-release-pipeline)
`deploy/` compose, with pinned versions for reproducibility.
