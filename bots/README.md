# bots/

Python automation against the Wikibase instance.

## Planned scripts

- `seed_load.py` — Reads `seed/` and populates a fresh Wikibase instance.
  Uses [pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot) for items
  and statements, and writes prose pages from `seed/pages/`. Idempotent — safe
  to run on an existing instance.
- `wikidata_sync.py` — Pulls a curated set of facts from Wikidata into local
  items (for `sameAs` linkage and seed enrichment). Pushes notable facts back
  to Wikidata via QuickStatements (editorial-gated).
- `export_mirror.py` — Exports key wiki pages to `docs/*.md` as a flat
  GitHub-readable mirror of the canonical content. Runs on a schedule.

## Setup

```bash
cd bots
python3 -m venv .venv
source .venv/bin/activate
pip install pywikibot requests
# configure ~/.pywikibot/user-config.py to point at the local/VPS wiki
```

Credentials are read from environment variables (`WIKIBASE_BOT_USER`,
`WIKIBASE_BOT_PASS`) — never committed.
