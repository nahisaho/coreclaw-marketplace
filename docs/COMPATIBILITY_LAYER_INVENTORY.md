# Compatibility Layer Inventory

Inventory of remaining compatibility-oriented files under `coreclaw-skills-hub/skills/` after the CI/release workflow was made `SKILL.md`-native and the compatibility cleanup was applied.

## Summary

- `skill.json`: 1 file
- `main.py`: 1 file
- Skill READMEs that still tell users to run `python main.py`: 0 files

The current workflows are `SKILL.md`-native by default and only require `skill.json` for package-style roots or explicit compatibility metadata.
The repository keeps one root `skill.json` and one implementation file for the builder runtime.

## main.py Categories

### 1. Substantive implementation

- Count: 1
- Status: keep
- Reason: contains real generation and artifact writing logic for Agent Skills output

Files:

- `agent-skills-builder/main.py`

### 2. Imported metadata wrappers

- Count: 0
- Status: removed in Phase 2
- Previous pattern: `def run(...)` returning static metadata with `"status": "imported"`
- Previous purpose: expose a minimal runtime-facing compatibility object for imported skills

### 3. Placeholder entrypoints

- Count: 0
- Status: removed in Phase 1
- Previous pattern: `def main()` printing a small JSON payload with `"status": "ok"`
- Previous purpose: satisfy legacy marketplace entrypoint expectations for suite-local sub-skills

## Group Counts

Compatibility `main.py` counts by top-level group:

| Group | Count |
| --- | ---: |
| `agent-skills-builder` | 1 |

## Current Dependencies

### Hard dependencies still present

Only one runtime-significant implementation file remains:

- `agent-skills-builder/main.py`

This file should not be deleted unless its generation logic is moved elsewhere.

### Soft dependencies still present

These are not CI blockers anymore:

- placeholder sub-skill READMEs were updated to point users at SKILL.md instead of a removed standalone entrypoint
- imported wrappers and their matching `skill.json` files were removed in Phase 2
- `agent-skills-builder/main.py` remains only because it contains real builder implementation logic
- runtime-generated suite roots intentionally emit `group.json` plus root `skill.json` so nested `skills/*/SKILL.md` packages validate as package-style roots

## Removal Priority

### Phase 1: safest removals

Completed.

Removed placeholder entrypoints and matching `skill.json` from:

- `compliance/*`
- `diligence/*`
- `enterprise/*`
- `growth/*`
- `learning/*`
- `sales/*`
- `secops/*`
- `supply/*`

Completed follow-up:

- updated the corresponding 48 skill READMEs that previously said `python main.py`
- rewrote `agent-skills-builder/README.md` quick start to show the supported Python API invocation

### Phase 2: imported wrappers

Completed.

Removed static imported wrappers and matching `skill.json` from:

- top-level suite roots except `agent-skills-builder`
- all nested `scientist/scientific-*`

Follow-up completed:

- removed matching `skill.json`
- reduced the repository compatibility layer to the single substantive legacy generator implementation

### Phase 3: legacy generation mode review

Completed. `agent-skills-builder` no longer emits legacy `coreclaw` scaffolds and now generates Agent Skills output only.

## Recommendation

The repository cleanup is complete.

Remaining implementation note:

1. `agent-skills-builder/main.py` is kept because it is the builder runtime, not a compatibility shim.
2. `agent-skills-builder/skill.json` is kept because the package root intentionally exposes compatibility metadata.
