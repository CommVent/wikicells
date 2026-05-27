# 2026-05 creating the wikisomething server

## Input 1 (Session 413f4520-488a-4c21-9a00-5e978e8cb75d)
My initial session ended as follows:

```
[Pasted text #1 +21 lines]
```

I believe the next steps should be getting this to GitHub and then setting up the server.  What do you recommend next and in what order?

## Input 2 (2026-05 creating the wikisomething server)
HEre is that quote that was lost with copy/paste:
```
● Step 6 done — Hello World scaffold is complete on main with 25 commits, none pushed. Final summary:

  What's in the repo now
  - infra/docker-compose.yml — full Wikibase Suite stack (wikibase v7, MariaDB, ES, WDQS, QuickStatements, Traefik 3 + Let's Encrypt).
  - infra/config/Extensions.php — Wikidata federation enabled, CC0 (data) + CC-BY-SA-4.0 (prose) declared, extended-confirmed user group, anonymous read-only.
  - infra/config/traefik-dynamic.yml, infra/env.example — routing + deployment template.
  - seed/schema.yaml — 5 local properties + class item + 3 status items; P31 stays federated from Wikidata.
  - seed/open-questions.tsv — 18 rows (8 decided, 10 open) of the first wikified table — the project's own decision log.
  - seed/pages/{Main_Page,About,Architecture,Roadmap,Trust_Model}.wiki — MediaWiki-syntax bootstrap pages.
  - bots/seed_load.py — 370-line idempotent loader using the action API directly (no pywikibot dependency). Type-hinted, Google-style. bots/requirements.txt pinned.
  - docs/{architecture,trust-model,roadmap,open-questions}.md — slim GitHub mirrors of the canonical wiki content.
  - .pre-commit-config.yaml with gitleaks + 8 hygiene checks, replacing the broken local hook.

  What you own from here
  1. Register a domain; decide on WIKIBASE_PUBLIC_HOST and WDQS_PUBLIC_HOST (e.g. wiki.example + query.example).
  2. Provision the VPS (≥ 4 GB RAM) and point DNS.
  3. cp infra/env.example infra/.env, fill in.
  4. cd infra && docker compose up -d — first boot creates the database and admin user.
  5. Visit the wiki, log in, go to Special:BotPasswords, generate credentials.
  6. cd bots && pip install -r requirements.txt && python seed_load.py --host <your-host> to populate the schema, rows, and prose pages.

  Where would you like to focus next — local dry-run of the Docker stack, a LICENSE + AGPL decision, drafting the CellHistory extension, or something else?
```

## Input 3 (2026-05 creating the wikisomething server)
How hard would it be to spin up a Claude Sonnet instance to go back through every commit one by one and do the find/replace of names in the original commits?  I think I prefer changing all of these retroactively.

## Input 4 (2026-05 creating the wikisomething server)
Yes, please update the plan to use `git filter-repo`, which is already installed at `/home/rsage/.virtualenvs/git-filter-repo/bin/` with a shortcut located on my path at `/home/rsage/bin/git-filter-repo`.  If it is not on your path, you can update paths as needed.
