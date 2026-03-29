#!/usr/bin/env python3
"""Validate a skill directory or compatibility metadata file."""

import sys

from skill_metadata import SkillMetadataError, resolve_skill_metadata


def fail(message: str) -> None:
    print(f"Validation error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_skill.py <path/to/skill-dir|SKILL.md|skill.json>")

    try:
        metadata = resolve_skill_metadata(sys.argv[1])
    except SkillMetadataError as exc:
        fail(str(exc))

    print(f"OK: {metadata.skill_dir} (metadata source: {metadata.metadata_source})")


if __name__ == "__main__":
    main()
