# wikicells

Infrastructure for **community-edited Creative-Commons databases** where every
cell *and* every column definition is itself a wiki — full edit history,
attribution, and Wikipedia-style permissions including redaction.

This repo holds the open-source infrastructure that any organization can use to
stand up a wikified-database site. The canonical, living version of this
project lives on the wiki the infrastructure runs. Once the wiki is online,
this `README.md` and the `docs/` directory become an exported mirror — useful
for offline browsing and GitHub search, but not the source of truth.

## Status

Pre-Hello-World. Stack and key design decisions are committed; initial Docker
Compose stand-up is next.

- **Stack**: Wikibase (the engine behind Wikidata) + MediaWiki.
- **Federation**: Wikidata federation enabled from day one.
- **Data license**: CC0 for structured data (cells); CC-BY-SA for long-form
  prose.
- **Hosting**: Self-hosted on a VPS with a real domain and TLS from day one.

See `docs/architecture.md` for the rationale.

## Goals

1. **Build the infrastructure** so that other organizations can spin up
   similar wikified-database sites with minimal effort.
2. **Use that infrastructure** to host this project's own documentation
   and a particular target site (details forthcoming).

## Layout

| Path           | Purpose                                                         |
| -------------- | --------------------------------------------------------------- |
| `infra/`       | Docker Compose stack + MediaWiki/Wikibase configuration         |
| `extensions/`  | Custom MediaWiki extensions (cell-history, trust — later)       |
| `bots/`        | Python automation: seed loader, Wikidata sync, mirror export    |
| `seed/`        | Initial properties, items, and wiki prose pages                 |
| `docs/`        | Bootstrap markdown; superseded by the live wiki once available  |

## License

- **Code**: see `LICENSE` (TBD; leaning AGPL-3.0 to match MediaWiki/Wikibase).
- **Documentation prose**: CC-BY-SA-4.0.
- **Structured data**: CC0-1.0 (federation requirement with Wikidata).
