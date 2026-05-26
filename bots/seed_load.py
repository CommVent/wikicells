#!/usr/bin/env python3
"""Populate a fresh Wikibase instance with the contents of seed/.

The script is idempotent: it looks up existing entities and pages by label or
title and reuses them rather than creating duplicates. Safe to re-run on an
already-populated instance — newly added schema rows or pages will be created;
existing ones will be updated to match the seed sources.

Usage:
    export WIKIBASE_BOT_USER='user@botname'
    export WIKIBASE_BOT_PASS='generated-bot-password'
    python seed_load.py --host wiki.example.com --seed-dir ../seed

Bot password is obtained from Special:BotPasswords on the target wiki. The
bot account needs edit, createpage, and (for property creation) property-create
rights.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
import yaml


# ------------------------------------------------------------------------------
# Wikibase API client
# ------------------------------------------------------------------------------


@dataclass
class WikibaseClient:
    """Thin wrapper around the MediaWiki + Wikibase action API."""

    host: str
    session: requests.Session
    csrf_token: str = ""

    @classmethod
    def login(cls, host: str, user: str, password: str) -> "WikibaseClient":
        """Log in and obtain a CSRF token."""
        session = requests.Session()
        client = cls(host=host, session=session)

        # Step 1: fetch a login token.
        login_token = client._get_token("login")

        # Step 2: log in using the bot password.
        client._api(
            action="login",
            method="POST",
            lgname=user,
            lgpassword=password,
            lgtoken=login_token,
        )

        # Step 3: fetch the CSRF token for subsequent edits.
        client.csrf_token = client._get_token("csrf")
        return client

    def _api_url(self) -> str:
        return f"https://{self.host}/w/api.php"

    def _api(self, action: str, method: str = "GET", **params: Any) -> dict:
        """Issue an API request, return parsed JSON, raise on API-level errors."""
        params["action"] = action
        params["format"] = "json"
        if method == "GET":
            response = self.session.get(self._api_url(), params=params, timeout=60)
        else:
            response = self.session.post(self._api_url(), data=params, timeout=60)
        response.raise_for_status()
        payload = response.json()
        if "error" in payload:
            raise RuntimeError(f"API error: {payload['error']}")
        return payload

    def _get_token(self, kind: str) -> str:
        payload = self._api(action="query", meta="tokens", type=kind)
        return payload["query"]["tokens"][f"{kind}token"]

    # --- Entity lookup -------------------------------------------------------

    def find_entity_by_label(
        self, label: str, entity_type: str, language: str = "en"
    ) -> str | None:
        """Return the entity ID (Q### or P###) for an exact label match, or None."""
        payload = self._api(
            action="wbsearchentities",
            search=label,
            language=language,
            type=entity_type,
            limit=20,
        )
        for hit in payload.get("search", []):
            if hit.get("label") == label or hit.get("match", {}).get("text") == label:
                return hit["id"]
        return None

    # --- Entity create / update ----------------------------------------------

    def upsert_entity(
        self,
        entity_type: str,
        labels: dict[str, str],
        descriptions: dict[str, str] | None = None,
        aliases: dict[str, list[str]] | None = None,
        datatype: str | None = None,
        claims: list[dict] | None = None,
    ) -> str:
        """Create or update an entity. Returns its ID."""
        primary_label = labels.get("en") or next(iter(labels.values()))
        existing_id = self.find_entity_by_label(primary_label, entity_type)

        data: dict[str, Any] = {}
        if labels:
            data["labels"] = {
                lang: {"language": lang, "value": value}
                for lang, value in labels.items()
            }
        if descriptions:
            data["descriptions"] = {
                lang: {"language": lang, "value": value}
                for lang, value in descriptions.items()
            }
        if aliases:
            data["aliases"] = {
                lang: [{"language": lang, "value": v} for v in values]
                for lang, values in aliases.items()
            }
        if claims:
            data["claims"] = claims

        kwargs: dict[str, Any] = {
            "action": "wbeditentity",
            "method": "POST",
            "data": _json_dumps(data),
            "token": self.csrf_token,
            "bot": 1,
        }
        if existing_id:
            kwargs["id"] = existing_id
        else:
            kwargs["new"] = entity_type
            if entity_type == "property":
                if not datatype:
                    raise ValueError("datatype required when creating a property")
                kwargs["datatype"] = datatype

        result = self._api(**kwargs)
        return result["entity"]["id"]

    # --- Wiki pages ----------------------------------------------------------

    def upsert_page(self, title: str, wikitext: str) -> None:
        """Create or replace the content of a wiki page."""
        self._api(
            action="edit",
            method="POST",
            title=title,
            text=wikitext,
            token=self.csrf_token,
            bot=1,
            summary="Seed load",
        )


def _json_dumps(value: Any) -> str:
    """Compact JSON for the wbeditentity data parameter."""
    import json
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


# ------------------------------------------------------------------------------
# Datavalue construction (datatype-aware)
# ------------------------------------------------------------------------------


def build_snak(
    property_id: str, datatype: str, raw_value: str, id_map: dict[str, str]
) -> dict:
    """Build a Wikibase mainsnak dict for a typed value."""
    value: Any
    if datatype == "wikibase-item":
        target_id = id_map.get(raw_value, raw_value)
        if not target_id.startswith("Q"):
            raise ValueError(f"expected Q-ID for {property_id}, got {raw_value!r}")
        value = {"entity-type": "item", "numeric-id": int(target_id[1:])}
        value_type = "wikibase-entityid"
    elif datatype == "monolingualtext":
        value = {"text": raw_value, "language": "en"}
        value_type = "monolingualtext"
    elif datatype == "time":
        # Expected input: "+YYYY-MM-DD" (day precision). Convert to full Wikibase form.
        value = {
            "time": f"{raw_value}T00:00:00Z",
            "timezone": 0,
            "before": 0,
            "after": 0,
            "precision": 11,  # day
            "calendarmodel": "http://www.wikidata.org/entity/Q1985727",  # Gregorian
        }
        value_type = "time"
    elif datatype in ("string", "external-id"):
        value = raw_value
        value_type = "string"
    elif datatype == "url":
        value = raw_value
        value_type = "string"
    else:
        raise ValueError(f"unsupported datatype: {datatype}")

    return {
        "mainsnak": {
            "snaktype": "value",
            "property": property_id,
            "datavalue": {"value": value, "type": value_type},
        },
        "type": "statement",
        "rank": "normal",
    }


# ------------------------------------------------------------------------------
# Seed loading
# ------------------------------------------------------------------------------


def load_schema(client: WikibaseClient, schema: dict, id_map: dict[str, str]) -> None:
    """Create local properties and class/status items, recording assigned IDs."""
    for prop_def in schema.get("properties", []):
        pid = client.upsert_entity(
            entity_type="property",
            datatype=prop_def["datatype"],
            labels=prop_def.get("labels", {}),
            descriptions=prop_def.get("descriptions", {}),
            aliases=prop_def.get("aliases", {}),
        )
        id_map[prop_def["id_alias"]] = pid
        print(f"  property  {prop_def['id_alias']:30s} → {pid}")

    for item_def in schema.get("class_items", []) + schema.get("status_items", []):
        qid = client.upsert_entity(
            entity_type="item",
            labels=item_def.get("labels", {}),
            descriptions=item_def.get("descriptions", {}),
            aliases=item_def.get("aliases", {}),
        )
        id_map[item_def["id_alias"]] = qid
        print(f"  item      {item_def['id_alias']:30s} → {qid}")


# Maps TSV column → (property id_alias, datatype). Order is the column order
# we emit statements in.
ROW_COLUMNS = [
    ("status", "P_status", "wikibase-item"),
    ("decision", "P_decision", "monolingualtext"),
    ("decided_by", "P_decided_by", "string"),
    ("decided_when", "P_decided_when", "time"),
    ("rationale_link", "P_rationale_link", "url"),
]


def load_open_questions(
    client: WikibaseClient,
    tsv_path: Path,
    id_map: dict[str, str],
    class_alias: str = "Q_class_decision",
) -> None:
    """Create one item per row in open-questions.tsv with statements."""
    class_qid = id_map[class_alias]

    with tsv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            label = row["label"].strip()
            description = row.get("description", "").strip()

            claims: list[dict] = []
            # P31 — "instance of" — uses Wikidata's federated property.
            claims.append(
                build_snak("P31", "wikibase-item", class_qid, id_map)
            )

            for col, alias, datatype in ROW_COLUMNS:
                raw = row.get(col, "").strip()
                if not raw:
                    continue
                property_id = id_map[alias]
                # Strip leading "+" from time values per Wikibase format.
                claims.append(build_snak(property_id, datatype, raw, id_map))

            qid = client.upsert_entity(
                entity_type="item",
                labels={"en": label},
                descriptions={"en": description} if description else None,
                claims=claims,
            )
            print(f"  question  {label[:40]:40s} → {qid}")


def load_pages(client: WikibaseClient, pages_dir: Path) -> None:
    """Upload all .wiki files in pages_dir as MediaWiki pages."""
    for page_file in sorted(pages_dir.glob("*.wiki")):
        title = page_file.stem.replace("_", " ")
        wikitext = page_file.read_text(encoding="utf-8")
        client.upsert_page(title, wikitext)
        print(f"  page      {title}")


# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, help="wiki hostname (no scheme)")
    parser.add_argument(
        "--seed-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "seed",
        help="directory containing schema.yaml, open-questions.tsv, pages/",
    )
    args = parser.parse_args()

    user = os.environ.get("WIKIBASE_BOT_USER")
    password = os.environ.get("WIKIBASE_BOT_PASS")
    if not (user and password):
        print(
            "error: set WIKIBASE_BOT_USER and WIKIBASE_BOT_PASS env vars",
            file=sys.stderr,
        )
        return 2

    seed_dir: Path = args.seed_dir
    schema_path = seed_dir / "schema.yaml"
    tsv_path = seed_dir / "open-questions.tsv"
    pages_dir = seed_dir / "pages"

    schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))

    print(f"==> Logging into {args.host} as {user}")
    client = WikibaseClient.login(args.host, user, password)

    id_map: dict[str, str] = {}

    print("==> Loading schema (properties + class/status items)")
    load_schema(client, schema, id_map)

    if tsv_path.exists():
        print("==> Loading open-questions rows")
        load_open_questions(client, tsv_path, id_map)

    if pages_dir.is_dir():
        print("==> Uploading prose pages")
        load_pages(client, pages_dir)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
