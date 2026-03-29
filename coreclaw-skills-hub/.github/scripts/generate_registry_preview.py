#!/usr/bin/env python3
"""Generate a preview registry from the current skills tree.

This script is intended for CI validation on pull requests.
It does not mutate the canonical registry.json used for releases.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib

from skill_metadata import SkillMetadataError, resolve_skill_metadata


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def build_preview(skills_root: pathlib.Path) -> dict:
    skills: dict[str, dict[str, str | int | list]] = {}

    for skill_md_path in sorted(skills_root.rglob("SKILL.md")):
        skill_dir = skill_md_path.parent
        if skill_dir.name == "source":
            continue

        skill_path = skill_dir.relative_to(skills_root).as_posix()
        try:
            metadata = resolve_skill_metadata(skill_dir)
        except SkillMetadataError as exc:
            raise ValueError(f"failed to resolve metadata for {skill_dir}: {exc}") from exc

        entry: dict[str, str | int | list | None] = {
            "name": metadata.name,
            "description": metadata.description,
            "metadataSource": metadata.metadata_source,
        }
        if metadata.version:
            entry["version"] = metadata.version
        if metadata.entrypoint:
            entry["entrypoint"] = metadata.entrypoint

        skills[skill_path] = entry

    # Process group-level metadata
    for group_dir in sorted(skills_root.iterdir()):
        if not group_dir.is_dir():
            continue
        
        group_json = group_dir / "group.json"
        if group_json.exists():
            group_data = json.loads(group_json.read_text(encoding="utf-8"))
            group_name = group_dir.name
            skills[group_name] = {
                "name": group_data["name"],
                "description": group_data["description"],
                "icon": group_data.get("icon", ""),
                "isGroup": True,
                "skillCount": group_data.get("count", 0),
            }

    return {
        "generated_at": utc_now_iso(),
        "skills": skills,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_root", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    args = parser.parse_args()

    preview = build_preview(args.skills_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(preview, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote preview registry to {args.output}")


if __name__ == "__main__":
    main()