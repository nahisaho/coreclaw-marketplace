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
    skills: dict[str, dict[str, str]] = {}

    for skill_json_path in sorted(skills_root.rglob("skill.json")):
        skill_dir = skill_json_path.parent
        skill_path = skill_dir.relative_to(skills_root).as_posix()
        data = json.loads(skill_json_path.read_text(encoding="utf-8"))
        skills[skill_path] = {
            "name": data["name"],
            "version": data["version"],
            "entrypoint": data["entrypoint"],
            "description": data["description"],
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