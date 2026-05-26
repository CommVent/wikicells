# extensions/

Custom MediaWiki extensions developed for this project.

## Planned extensions

### `CellHistory/` (post Hello World)

Surfaces statement-level edit history as a first-class UI. Wikibase stores
the necessary data — every statement change is part of an item revision —
but doesn't currently render a "history of this single cell / statement"
view. This extension fills that gap.

### `TrustGraph/` (later phase)

Implements the stake-and-slash trust system: vouches as a custom data type,
reputation accounting, transitive propagation (EigenTrust-flavored), and
slashing on sanction. Deferred from Hello World — the prototype will use
MediaWiki's stock access-level ladder only.

## Development

Each extension lives in its own directory and follows the MediaWiki extension
layout: `extension.json`, autoloader-friendly PHP, optional ResourceLoader
modules. Extensions are loaded by `infra/LocalSettings.php` via
`wfLoadExtension('CellHistory')`.

See <https://www.mediawiki.org/wiki/Manual:Developing_extensions>.
