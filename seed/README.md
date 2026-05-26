# seed/

Initial content for a fresh Wikibase instance. Everything here can be loaded
into a brand-new wiki by `bots/seed_load.py`.

## Contents

- `properties.tsv` — Property definitions (label, description, datatype) for
  the open-questions table and any other initial schemas. QuickStatements
  format.
- `items.tsv` — Initial items, one per row, with statements. The first
  wikified table the project hosts is the **open-questions list itself**:
  one item per architectural question, with statements for status, decision,
  decided-by, decided-when, and rationale.
- `pages/` — MediaWiki prose pages as text files. `Main_Page.wiki`,
  `About.wiki`, `Roadmap.wiki`, `Architecture.wiki`, `Trust_Model.wiki`.
  These become the canonical wiki content on first load.

## Why this content first

The project eats its own dog food from day one: every architectural decision
made during planning becomes a wikified row, with each cell having its own
revision history. The wiki documents the very infrastructure that hosts it.
