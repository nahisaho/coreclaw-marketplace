#!/usr/bin/env python3
"""Validate a skill metadata file."""

import json
import pathlib
import re
import sys

REQUIRED_KEYS = ["name", "version", "description", "entrypoint"]
SEMVER_TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")


def fail(message: str) -> None:
    print(f"Validation error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_skill.py <path/to/skill.json>")

    path = pathlib.Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")

    if not isinstance(data, dict):
        fail("skill.json root must be an object")

    for key in REQUIRED_KEYS:
        if key not in data:
            fail(f"missing required key: {key}")

    for key in REQUIRED_KEYS:
        if not isinstance(data.get(key), str) or not data[key].strip():
            fail(f"key '{key}' must be a non-empty string")

    if not SEMVER_TAG_PATTERN.match(data["version"]):
        fail("version must match v<major>.<minor>.<patch>, e.g. v1.0.0")

    entrypoint = path.parent / data["entrypoint"]
    if not entrypoint.exists():
        fail(f"entrypoint not found: {entrypoint}")

    print(f"OK: {path}")


if __name__ == "__main__":
    main()
