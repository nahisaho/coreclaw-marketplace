#!/usr/bin/env python3
"""Update registry.json with a released skill artifact."""

import datetime as dt
import json
import pathlib
import sys
from typing import Any

REGISTRY_FILE = pathlib.Path("registry.json")


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_registry() -> dict[str, Any]:
    if not REGISTRY_FILE.exists():
        return {"generated_at": utc_now_iso(), "skills": {}}

    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("registry.json root must be an object")

    data.setdefault("generated_at", utc_now_iso())
    data.setdefault("skills", {})
    if not isinstance(data["skills"], dict):
        raise ValueError("registry.json 'skills' must be an object")
    return data


def main() -> None:
    if len(sys.argv) != 4:
        print(
            "usage: update_registry.py <skill> <version> <zip_url>",
            file=sys.stderr,
        )
        raise SystemExit(1)

    skill, version, zip_url = sys.argv[1], sys.argv[2], sys.argv[3]

    registry = load_registry()
    skills = registry["skills"]
    released_at = utc_now_iso()

    item = skills.get(skill, {"latest": version, "versions": []})
    versions = item.get("versions", [])
    if not isinstance(versions, list):
        versions = []

    existing = next((v for v in versions if v.get("version") == version), None)
    if existing:
        existing["url"] = zip_url
        existing["released_at"] = released_at
    else:
        versions.append(
            {
                "version": version,
                "url": zip_url,
                "released_at": released_at,
            }
        )

    versions.sort(key=lambda x: x.get("version", ""))
    item["latest"] = version
    item["versions"] = versions
    skills[skill] = item

    registry["generated_at"] = released_at

    REGISTRY_FILE.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Updated {REGISTRY_FILE} for {skill} {version}")


if __name__ == "__main__":
    main()
