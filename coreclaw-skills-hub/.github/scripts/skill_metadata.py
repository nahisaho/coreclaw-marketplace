#!/usr/bin/env python3
"""Shared helpers for skill metadata resolution.

The canonical metadata source is SKILL.md frontmatter when a root SKILL.md exists.
For package-style group roots that only expose nested skills/<subskill>/SKILL.md,
compatibility metadata from skill.json can be used together with group.json.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import pathlib
import re

SEMVER_TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
NAME_RE = re.compile(r"^name:\s*(.+)$", re.M)
DESCRIPTION_BLOCK_RE = re.compile(r"^description:\s*\|\n((?:^[ \t].*\n?)*)", re.M)
DESCRIPTION_INLINE_RE = re.compile(r"^description:\s*(.+)$", re.M)


class SkillMetadataError(ValueError):
    """Raised when skill metadata is missing or malformed."""


@dataclass(frozen=True)
class SkillMetadata:
    skill_dir: pathlib.Path
    name: str
    description: str
    skill_md: pathlib.Path
    skill_json: pathlib.Path | None
    version: str | None
    entrypoint: str | None
    metadata_source: str


def _normalize_description(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return " ".join(line for line in lines if line).strip()


def parse_skill_frontmatter(skill_md: pathlib.Path) -> tuple[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise SkillMetadataError(f"missing frontmatter in {skill_md}")

    frontmatter = match.group(1)
    name_match = NAME_RE.search(frontmatter)
    if not name_match or not name_match.group(1).strip():
        raise SkillMetadataError(f"missing non-empty frontmatter name in {skill_md}")

    description_match = DESCRIPTION_BLOCK_RE.search(frontmatter)
    if description_match:
        description = _normalize_description(description_match.group(1))
    else:
        inline_match = DESCRIPTION_INLINE_RE.search(frontmatter)
        if not inline_match or not inline_match.group(1).strip():
            raise SkillMetadataError(f"missing non-empty frontmatter description in {skill_md}")
        description = inline_match.group(1).strip()

    return name_match.group(1).strip(), description


def load_compat_metadata(skill_dir: pathlib.Path) -> dict | None:
    skill_json = skill_dir / "skill.json"
    if not skill_json.exists():
        return None

    try:
        data = json.loads(skill_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SkillMetadataError(f"invalid JSON in {skill_json}: {exc}") from exc

    if not isinstance(data, dict):
        raise SkillMetadataError(f"skill.json root must be an object: {skill_json}")

    return data


def list_nested_skill_definitions(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    skills_root = skill_dir / "skills"
    if not skills_root.is_dir():
        return []

    return sorted(
        path
        for path in skills_root.glob("*/SKILL.md")
        if path.is_file()
    )


def is_package_style_group_root(skill_dir: pathlib.Path) -> bool:
    return (skill_dir / "group.json").exists() and bool(list_nested_skill_definitions(skill_dir))


def resolve_skill_dir(target: pathlib.Path) -> pathlib.Path:
    path = target.resolve()
    if path.is_dir():
        return path
    if path.name in {"SKILL.md", "skill.json", "main.py", "README.md"}:
        return path.parent
    raise SkillMetadataError(f"unsupported validation target: {target}")


def resolve_skill_metadata(target: str | pathlib.Path) -> SkillMetadata:
    skill_dir = resolve_skill_dir(pathlib.Path(target))
    skill_md = skill_dir / "SKILL.md"
    compat = load_compat_metadata(skill_dir)

    if skill_md.exists():
        name, description = parse_skill_frontmatter(skill_md)
        if name != skill_dir.name:
            raise SkillMetadataError(
                f"frontmatter name '{name}' must match directory name '{skill_dir.name}' in {skill_md}"
            )

        if compat is None:
            return SkillMetadata(
                skill_dir=skill_dir,
                name=name,
                description=description,
                skill_md=skill_md,
                skill_json=None,
                version=None,
                entrypoint=None,
                metadata_source="SKILL.md",
            )
    else:
        if compat is None:
            raise SkillMetadataError(f"missing SKILL.md in {skill_dir}")
        if not is_package_style_group_root(skill_dir):
            raise SkillMetadataError(
                f"missing SKILL.md in {skill_dir}; package-style roots require group.json and nested skills/*/SKILL.md"
            )
        name = skill_dir.name
        description = compat.get("description", "") if isinstance(compat, dict) else ""

    required = ["name", "version", "description", "entrypoint"]
    for key in required:
        value = compat.get(key)
        if not isinstance(value, str) or not value.strip():
            raise SkillMetadataError(f"key '{key}' must be a non-empty string in {skill_dir / 'skill.json'}")

    if compat["name"] != name:
        raise SkillMetadataError(
            f"skill.json name '{compat['name']}' must match canonical name '{name}' in {skill_dir}"
        )

    if not SEMVER_TAG_PATTERN.match(compat["version"]):
        raise SkillMetadataError(
            f"version must match v<major>.<minor>.<patch> in {skill_dir / 'skill.json'}"
        )

    entrypoint_path = skill_dir / compat["entrypoint"]
    if not entrypoint_path.exists():
        raise SkillMetadataError(f"entrypoint not found: {entrypoint_path}")

    return SkillMetadata(
        skill_dir=skill_dir,
        name=name,
        description=compat["description"].strip() or description,
        skill_md=skill_md if skill_md.exists() else entrypoint_path,
        skill_json=skill_dir / "skill.json",
        version=compat["version"],
        entrypoint=compat["entrypoint"],
        metadata_source="skill.json",
    )