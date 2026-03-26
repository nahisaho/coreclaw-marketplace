# coreclaw-skills-hub

Marketplace repository for Core-Claw Agent Skills.

## Structure

- `.github/workflows/release.yml`: package and release a skill from a tag.
- `.github/workflows/validate.yml`: validate changed skills on pull requests.
- `.github/scripts/validate_skill.py`: validates each `skill.json`.
- `.github/scripts/update_registry.py`: updates `registry.json` after release.
- `skills/<group>/<skill-name>/`: nested skill packages, e.g. `skills/scientist/scientific-academic-writing/`.
- `registry.json`: generated index for all released skills.

## Imported Skill Layout

This repository does not keep `skills/` identical to `nahisaho/coreclaw`.
The current layout is intentional and is the official marketplace format.

For each imported skill directory such as `skills/scientist/scientific-academic-writing/`, the following files are maintained:

- `SKILL.md`: the original skill definition copied to the skill root for direct consumption.
- `skill.json`: marketplace metadata used by validation and release workflows.
- `main.py`: marketplace entrypoint placeholder.
- `README.md`: marketplace-facing description for the imported skill.
- `source/`: preserved original source payload copied from `nahisaho/coreclaw`.

Examples:

- Original file `coreclaw/skills/scientist/scientific-academic-writing/SKILL.md`
   is preserved as `skills/scientist/scientific-academic-writing/SKILL.md`
   and also as `skills/scientist/scientific-academic-writing/source/SKILL.md`.
- Original directory `coreclaw/skills/scientist/scientific-academic-writing/assets/`
   is preserved under `skills/scientist/scientific-academic-writing/source/assets/`.

This means:

- skill directory nesting is preserved
- original source files are preserved
- marketplace-specific files are added
- helper files from the source repository may live under `source/` rather than at the original top-level position

If you compare `coreclaw/skills` and `coreclaw-skills-hub/skills`, they are expected to differ structurally, but the original source content should still be present.

## Release Flow

1. Create a tag with this format:
   - `<skill-path>/v<major>.<minor>.<patch>`
   - Example: `scientist/scientific-academic-writing/v0.1.0`
2. Push the tag.
3. The release workflow will:
   - validate `skills/<skill-path>/skill.json`
   - zip that nested skill directory
   - create a GitHub Release and upload the zip
   - update `registry.json` and push to `main`

## PR Validation

Pull requests that touch files under `skills/**` run metadata validation for changed skills.

## skill.json Schema (minimum)

```json
{
   "name": "scientific-academic-writing",
   "version": "v0.1.0",
   "description": "Imported from nahisaho/coreclaw",
  "entrypoint": "main.py"
}
```
