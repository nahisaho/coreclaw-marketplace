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


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def build_preview(skills_root: pathlib.Path) -> dict:
    skills: dict[str, dict[str, str | int | list]] = {}
    groups_seen: set[str] = set()

    # Process individual skills
    for skill_json_path in sorted(skills_root.rglob("skill.json")):
        skill_dir = skill_json_path.parent
        skill_path = skill_dir.relative_to(skills_root).as_posix()
        
        # Skip if this is a group-level metadata file
        if skill_dir.name == "source":
            continue
        
        data = json.loads(skill_json_path.read_text(encoding="utf-8"))
        
        # Track groups
        parts = skill_path.split("/")
        if len(parts) > 1:
            group_name = parts[0]
            if group_name not in groups_seen:
                groups_seen.add(group_name)
        
        skills[skill_path] = {
            "name": data["name"],
            "version": data["version"],
            "entrypoint": data["entrypoint"],
            "description": data["description"],
        }

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