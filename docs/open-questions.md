# Open questions

> **Note**: This is a bootstrap mirror. Once the wiki is online, the
> canonical version of this content lives at
> `https://wiki.wikicells.org/wiki/Open_Questions` as a **wikified table** (each
> row is a Wikibase item, each cell has its own revision history). The
> markdown form below is a flat snapshot.

## Decisions made

| # | Question                                | Decision                              | When       |
| - | --------------------------------------- | ------------------------------------- | ---------- |
| 1 | Infrastructure stack                    | Wikibase / MediaWiki                  | 2026-05-24 |
| 2 | Trust mechanic — what does "invest" mean? | Stake-and-slash on earned floor    | 2026-05-24 |
| 3 | Wikidata federation                     | Yes, enabled from day one             | 2026-05-24 |
| 4 | Data license                            | CC0 (structured) / CC-BY-SA (prose)   | 2026-05-24 |
| 5 | Hosting model for Hello World           | Self-hosted VPS + real domain + TLS   | 2026-05-25 |
| 6 | First wikified table                    | The open-questions list itself        | 2026-05-25 |
| 7 | Trust system phasing in Hello World     | Defer entirely; rely on stock MediaWiki | 2026-05-25 |
| 8 | Initial deliverable shape               | Self-documenting Hello World site     | 2026-05-25 |

## Still open

| # | Question                                | Notes                                              |
| - | --------------------------------------- | -------------------------------------------------- |
| A | Domain name                             | **Decided 2026-05-27:** `wikicells.org` (served as `wiki.` / `query.` subdomains). |
| B | VPS provider and sizing                 | ≥ 4 GB RAM recommended. Provider TBD.              |
| C | Code license                            | Leaning AGPL-3.0 (Wikipedia/MediaWiki alignment).  |
| D | Schema mutability                       | Anyone-adds vs. property-creation review process.  |
| E | Internationalization at launch          | English-only at first, or multi-language from day one. |
| F | Initial admin and oversighter set       | Who, criteria, appeal process.                     |
| G | Anonymous editing                       | Wikipedia-style IP edits, or login required.       |
| H | Anti-abuse posture                      | Edit-rate limits, CAPTCHA, AI-content detection.   |
| I | Scale targets                           | Year-1 and Year-2 users / rows / edits-per-day.    |
| J | The user's specific site (Goal ii)      | Topic, schema, initial content. Deliberately deferred. |

## How this document evolves

Once the wiki is online, each row becomes a Wikibase item under the
"Architectural decision" class. Status, decision, decided-by, decided-when,
and rationale-link become statements with their own revision history. This
markdown file is regenerated from the wiki by `bots/export_mirror.py`.
