<?php
// ##############################################################################
// wikicells — Wikibase customization
//
// This file is mounted into the Wikibase container at
//   /var/www/html/LocalSettings.d/90_UserDefinedExtensions.php
// and runs *after* MediaWiki's LocalSettings.php and the default Wikibase
// configuration. It is the right place for override-style configuration.
//
// Sections:
//   1. Extensions             — wfLoadExtension() calls (none yet)
//   2. Federation             — Federated Properties from Wikidata
//   3. Licensing              — CC0 for structured data; CC-BY-SA for prose
//   4. Permissions            — Wikipedia-style user-group ladder
//   5. Misc / branding        — sitename, default language, etc.
// ##############################################################################


// ------------------------------------------------------------------------------
// 1. EXTENSIONS
// ------------------------------------------------------------------------------
//
// The wikibase image v7 already loads Wikibase Repo, Wikibase Client,
// WikibaseQualityConstraints, OAuth, etc. by default. Anything we want to
// load on top goes here.
//
// Custom extensions developed in this project belong in
//   /var/www/html/extensions/extensions/<ExtensionName>/
// (mounted from infra/config/extensions/ in docker-compose.yml) and are
// loaded with the "extensions/" prefix:
//
//   wfLoadExtension( 'extensions/CellHistory' );  // planned, not yet built
//   wfLoadExtension( 'extensions/TrustGraph' );   // planned, not yet built
//
// Hello World loads no custom extensions.


// ------------------------------------------------------------------------------
// 2. WIKIDATA FEDERATION
// ------------------------------------------------------------------------------
//
// Enables Federated Properties: properties defined on wikidata.org are usable
// directly on local items as if they were local. Without this, every project
// would need to re-define common properties like "instance of" (P31).
//
// Reference: https://www.mediawiki.org/wiki/Wikibase/Federation
//
// NOTE on Hello World caveat: Federated Properties is incompatible with
// running the local Wikibase Repo *as a property source for other wikis*.
// We accept this trade-off — we want to be a consumer of Wikidata, not a
// property publisher (at least at first).

$wgWBRepoSettings['federatedPropertiesEnabled'] = true;
$wgWBRepoSettings['federatedPropertiesSourceScriptUrl'] = 'https://www.wikidata.org/w/';


// ------------------------------------------------------------------------------
// 3. LICENSING
// ------------------------------------------------------------------------------
//
// Structured data (items, statements) is licensed CC0 to allow frictionless
// flow with Wikidata. Long-form prose on wiki pages (Main_Page, About, etc.)
// is licensed CC-BY-SA-4.0 to align with Wikipedia and to provide attribution
// requirements for substantial editorial work.
//
// $wgRightsUrl / $wgRightsText apply to pages generally;
// $wgWBRepoSettings['dataRightsUrl'] applies to the structured data layer.

$wgRightsUrl = 'https://creativecommons.org/licenses/by-sa/4.0/';
$wgRightsText = 'Creative Commons Attribution-ShareAlike 4.0';
$wgRightsIcon = 'https://creativecommons.org/images/public/somerights20.png';

$wgWBRepoSettings['dataRightsUrl'] = 'https://creativecommons.org/publicdomain/zero/1.0/';
$wgWBRepoSettings['dataRightsText'] = 'Creative Commons CC0 (Public Domain)';


// ------------------------------------------------------------------------------
// 4. PERMISSIONS — Wikipedia-style user-group ladder
// ------------------------------------------------------------------------------
//
// MediaWiki ships with: anonymous, user, autoconfirmed, sysop, bureaucrat.
// Wikibase adds: oversight (via RevisionDelete + suppressrevision).
//
// We add: extendedconfirmed (30 days, 500 edits) — matches en.wikipedia.org.
// Higher tiers (rollbacker, reviewer) are admin-granted via the standard
// Special:UserRights interface and don't need a config change here.

// Autopromotion: extendedconfirmed at 30 days of age AND 500 edits.
$wgAutopromote['extendedconfirmed'] = [
	'&',
	[ APCOND_EDITCOUNT, 500 ],
	[ APCOND_AGE, 30 * 86400 ],
];

// Make the group visible in user-rights logs and Special:ListGroupRights.
$wgGroupPermissions['extendedconfirmed']['editsemiprotected'] = true;
$wgGroupPermissions['extendedconfirmed']['skipcaptcha'] = true;

// Anonymous users may read but not edit. Account creation is open.
// Adjust per project policy (see docs/open-questions.md item G).
$wgGroupPermissions['*']['edit'] = false;
$wgGroupPermissions['*']['createaccount'] = true;
$wgGroupPermissions['user']['edit'] = true;


// ------------------------------------------------------------------------------
// 5. MISC / BRANDING
// ------------------------------------------------------------------------------

$wgSitename = 'wikicells';
$wgMetaNamespace = 'Wikicells';

// English at launch (see docs/open-questions.md item E for i18n decision).
$wgLanguageCode = 'en';

// Allow uploads — needed for icons, screenshots, etc. used in prose pages.
$wgEnableUploads = true;
$wgFileExtensions = array_merge( $wgFileExtensions ?? [], [ 'svg', 'webp' ] );
