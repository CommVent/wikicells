# seed/

Initial content for a fresh Wikibase instance. Everything here can be loaded
into a brand-new wiki by `bots/seed_load.py`.

## Contents

- `schema.yaml` — Property and class-item definitions: datatypes, labels,
  descriptions, and any default statements. YAML, not TSV, because the
  schema is hierarchical (properties have aliases, class items have
  statements) and YAML reads well.
- `open-questions.tsv` — The rows of the first wikified table, one per
  architectural question, with columns for label, status, decision,
  decided-by, decided-when, and rationale. Tab-separated because *tabular
  data is natural for TSV*, and the file is itself a demonstration of the
  cell-as-wiki concept once loaded into Wikibase.
- `pages/` — MediaWiki prose pages as text files. `Main_Page.wiki`,
  `About.wiki`, `Roadmap.wiki`, `Architecture.wiki`, `Trust_Model.wiki`.
  These become the canonical wiki content on first load.

The two formats are loaded together by `bots/seed_load.py`: schema first
(records assigned P-IDs and Q-IDs), then the TSV rows referencing schema
entries by their `id_alias`.

## Why this content first

The project eats its own dog food from day one: every architectural decision
made during planning becomes a wikified row, with each cell having its own
revision history. The wiki documents the very infrastructure that hosts it.
