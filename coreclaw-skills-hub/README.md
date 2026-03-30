# coreclaw-skills-hub

Marketplace repository for Core-Claw Agent Skills.

## Structure

- `.github/workflows/release.yml`: package and release a skill from a tag.
- `.github/workflows/validate.yml`: validate changed skills on pull requests.
- `.github/scripts/validate_skill.py`: validates each skill directory using `SKILL.md` as canonical metadata and checks `skill.json` only when present.
- `.github/scripts/update_registry.py`: updates `registry.json` after release.
- `skills/<group>/<skill-name>/`: nested skill packages, e.g. `skills/scientist/scientific-academic-writing/`.
- `registry.json`: generated index for all released skills.

## Imported Skill Layout

This repository does not keep `skills/` identical to `nahisaho/coreclaw`.
The current layout is intentional and is the official marketplace format.

For each imported skill directory such as `skills/scientist/scientific-academic-writing/`, the following files are maintained:

- `SKILL.md`: the canonical installable skill definition at the skill root.
- `README.md`: marketplace-facing description for the imported skill.

For root group packages such as `skills/scientist/` or `skills/consultant/`, the repository can also retain a lightweight `skill.json` so version-aware consumers can discover the latest released package version without requiring a legacy wrapper tree. Package-style roots may omit a root `SKILL.md` if they keep `group.json`, nested `skills/<subskill>/SKILL.md`, and a root `skill.json`.

Compatibility metadata files are otherwise minimized in the repository. The only remaining executable implementation helper is `skills/agent-skills-builder/main.py`, which generates Agent Skills artifacts.

Examples:

- Original file `coreclaw/skills/scientist/scientific-academic-writing/SKILL.md`
   is preserved as `skills/scientist/scientific-academic-writing/SKILL.md`.
- Installable helper assets such as prompts, skills, or assets are kept outside `source/`
   because CoreClaw does not install files from `source/`.

This means:

- skill directory nesting is preserved
- the root `SKILL.md` is the only installable skill definition
- root group packages may include `skill.json` for lightweight compatibility metadata and version discovery
- package-style roots without a root `SKILL.md` are allowed when `group.json` and nested `skills/<subskill>/SKILL.md` files exist
- marketplace-specific executable wrapper files are added only when a real compatibility consumer still exists
- current CI and release workflows validate `SKILL.md` first and do not require `skill.json` / `main.py`

If you compare `coreclaw/skills` and `coreclaw-skills-hub/skills`, they are expected to differ structurally because this repository is organized for marketplace validation and release.

## Release Flow

1. Create a tag with this format:
   - `<skill-path>/v<major>.<minor>.<patch>`
   - Example: `scientist/scientific-academic-writing/v0.1.0`
2. Push the tag.
3. The release workflow will:
   - validate `skills/<skill-path>/`
   - zip that nested skill directory
   - create a GitHub Release and upload the zip
   - update `registry.json` and push to `main`

## PR Validation

Pull requests that touch files under `skills/**` run metadata validation for changed skills.

PR validation does not commit `registry.json` changes.
Instead, CI generates a preview registry artifact so reviewers can inspect the current skill catalog without polluting the pull request branch with bot commits.

## Compatibility skill.json Schema (minimum)

`SKILL.md` frontmatter is canonical when a root `SKILL.md` exists. Add `skill.json` when a consumer needs explicit release metadata such as a version number. Root group packages may use `SKILL.md` as the metadata entrypoint when no executable wrapper is required, or an existing helper such as `main.py` when the package root has no root `SKILL.md`.

```json
{
   "name": "scientific-academic-writing",
   "version": "v0.1.0",
    "description": "Imported from nahisaho/coreclaw",
   "entrypoint": "SKILL.md"
}
```

For package-style roots that intentionally keep only nested sub-skills, the compatibility metadata can point at the retained helper file instead:

```json
{
   "name": "agent-skills-builder",
   "version": "v0.11.0",
   "description": "Builder skill that designs and generates Agent Skills compliant packages through user dialogue.",
   "entrypoint": "main.py"
}
```
