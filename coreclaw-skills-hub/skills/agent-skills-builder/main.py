#!/usr/bin/env python3
"""Entrypoint for skill: agent-skills-builder."""

from __future__ import annotations

from pathlib import Path
import zipfile


def _create_zip_bundle(output_dir: str, zip_path: str | None = None) -> dict:
    """Package generated artifacts into a downloadable zip bundle."""
    source_dir = Path(output_dir).expanduser().resolve()
    if not source_dir.exists() or not source_dir.is_dir():
        return {
            "created": False,
            "error": f"output_dir not found: {source_dir}",
        }

    bundle_path = (
        Path(zip_path).expanduser().resolve()
        if zip_path
        else source_dir.parent / f"{source_dir.name}.zip"
    )
    bundle_path.parent.mkdir(parents=True, exist_ok=True)

    packed_files = 0
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in source_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.resolve() == bundle_path:
                continue
            zf.write(file_path, arcname=file_path.relative_to(source_dir))
            packed_files += 1

    return {
        "created": True,
        "zip_path": str(bundle_path),
        "files_packed": packed_files,
    }


def run(input_data: dict | None = None) -> dict:
    request = input_data or {}
    zip_result = None

    if request.get("create_zip"):
        zip_result = _create_zip_bundle(
            output_dir=request.get("output_dir", ""),
            zip_path=request.get("zip_path"),
        )

    return {
        "skill": "agent-skills-builder",
        "skill_path": "agent-skills-builder",
        "status": "ready",
        "structure_reference": "docs/SKILLS_GUIDE.md",
        "supports": {
            "sub_agents": True,
            "zip_bundle": True,
            "interaction_mode": "one-question-one-answer",
        },
        "capabilities": [
            "scaffold-skill-package",
            "scaffold-sub-agents",
            "apply-skills-guide-structure",
            "generate-skill-json",
            "generate-skill-docs",
            "validate-schema",
            "package-zip-bundle",
            "prepare-release-tag",
        ],
        "input": request,
        "zip_bundle": zip_result,
    }


if __name__ == "__main__":
    print(run())
