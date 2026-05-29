# Roadmap

> **Note**: This is a bootstrap mirror. Once the wiki is online, the canonical
> version of this content lives at `https://<TBD-domain>/wiki/Roadmap` and
> this file becomes an auto-exported snapshot.

## Hello World phase (current)

Goal: a self-hosted Wikibase running at a real domain, populated with this
project's own architectural decisions as a wikified table, demonstrating
cell-as-wiki and schema-as-wiki on real project content from day one.

| Step | Description                                                  | Status      |
| ---- | ------------------------------------------------------------ | ----------- |
| 1    | Scaffold repo layout + slim bootstrap docs                   | In progress |
| 2    | `infra/docker-compose.yml` (Wikibase Suite)                  | Pending     |
| 3    | `infra/LocalSettings.php` (federation + CC0 + user groups)   | Pending     |
| 4    | `seed/properties.tsv` + `seed/items.tsv` (open-questions table) | Pending  |
| 5    | `seed/pages/` (Main_Page, About, Roadmap, Architecture, ...) | Pending     |
| 6    | `bots/seed_load.py` (idempotent seed loader)                 | Pending     |
| 7    | `infra/nginx/` + Let's Encrypt deployment recipe             | Pending     |
| 8    | User: provision VPS, register domain, first deploy           | Pending     |

## User actions blocking public-URL deployment

- Register a domain.
- Provision a VPS (≥ 4 GB RAM recommended).
- Point DNS at the VPS.
- Set admin credentials on first boot.

Steps 1–7 don't depend on these — they can run locally on Docker Compose.

## Post-Hello-World phases

### Phase A — `CellHistory` extension

Custom MediaWiki extension surfacing per-statement edit history as a
first-class UI. The principal engineering investment of this project, since
it's the gap between Wikibase and our "every cell is a wiki" requirement.

### Phase B — Bots and export

- `bots/wikidata_sync.py` — controlled import/export with Wikidata.
- `bots/export_mirror.py` — scheduled wiki → `docs/*.md` mirror for offline
  / GitHub-search discoverability.

### Phase C — Oversight policy hardening

Document the appeal process for RevisionDelete and suppression; establish
the audit trail. Train initial oversighters.

### Phase D — Federation hardening

RDF dump publishing on a schedule; SPARQL endpoint hardening; QuickStatements
push-to-Wikidata workflow for notable facts.

### Phase E — Maintainers' first deployment

The project maintainers' own wikified-database site, built on this
infrastructure — serving as a real-world stress test and reference deployment.
A [Known Deployments](known-deployments.md) index will grow as others adopt
the stack.

### Phase F — Adoption packaging (Goal i)

Turn `infra/` + `extensions/` + `bots/` + `seed/` into a forkable deployment
template other organizations can adopt with minimal setup.
