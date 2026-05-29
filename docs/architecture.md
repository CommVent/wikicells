# Architecture

> **Note**: This is a bootstrap mirror. Once the wiki is online, the canonical
> version of this content lives at `https://<TBD-domain>/wiki/Architecture`
> and this file becomes an auto-exported snapshot.

## Stack

**Wikibase** (the engine behind Wikidata) on top of **MediaWiki**, deployed
via the Wikibase Suite Docker Compose stack.

| Layer                     | Component                          |
| ------------------------- | ---------------------------------- |
| Wiki + structured data    | MediaWiki + Wikibase extension     |
| Database                  | MariaDB                            |
| Search                    | Elasticsearch                      |
| Query service             | Blazegraph (Wikibase Query Service)|
| TLS termination           | nginx + Let's Encrypt              |
| Container orchestration   | Docker Compose                     |

## Why Wikibase

Wikibase is the only mature open-source stack that natively provides all of:

1. **Structured data with cell-level granularity** — items with statements;
   each statement has property + value + qualifiers + references.
2. **Schema-as-wiki** — properties are themselves wiki entities with
   labels, descriptions, and revision history.
3. **Full revision history per entity** — every change is a revision.
4. **Battle-tested permission model** — autoconfirmed → reviewer → admin →
   oversighter, with RevisionDelete and suppression for redaction.
5. **Wikidata federation** — first-class. Federated Properties, `sameAs`
   linkage, federated SPARQL queries.

The alternatives surveyed (Semantic MediaWiki, Cargo, Wiki.js, Dolt + custom
frontend) each lacked at least one of these properties, with the closest
alternative (Dolt) requiring months of build work to reach parity.

## Data model

A row in a wikified database is a Wikibase **item** (Q-ID).
A column is a Wikibase **property** (P-ID), defined globally and reused
across tables.
A cell is a **statement** on an item using a property — and statements
carry their own revision history through the item's revision log.

A "table" is then a set of items that share a common schema (a set of
properties). Tables can be declared explicitly via item-class membership
(`instance of` statements) or via the QueryService.

## Federation with Wikidata

Federated Properties is enabled in `LocalSettings.php`, allowing local items
to use Wikidata's `P31`, `P279`, etc. directly. Local items can reference
Wikidata Q-IDs as values. Federated SPARQL queries can join local data
against Wikidata in a single query.

Structured data is licensed **CC0** so it can flow back to Wikidata
frictionlessly. Long-form prose is **CC-BY-SA**.

## Cell-level history UX gap

Wikibase stores statement-level history (it's reconstructable from item
revisions) but doesn't ship a UI for "show me the history of just this one
cell." Closing this gap is the principal engineering investment of the
post-Hello-World phase, planned as the `CellHistory` MediaWiki extension.
