# coreclaw-skills-hub

Marketplace repository for Core-Claw Agent Skills.

## Structure

- `.github/workflows/release.yml`: package and release a skill from a tag.
- `.github/workflows/validate.yml`: validate changed skills on pull requests.
- `.github/scripts/validate_skill.py`: validates each `skill.json`.
- `.github/scripts/update_registry.py`: updates `registry.json` after release.
- `skills/<group>/<skill-name>/`: nested skill packages, e.g. `skills/scientist/scientific-academic-writing/`.
- `registry.json`: generated index for all released skills.

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
  "name": "web-search",
  "version": "v1.0.0",
  "description": "Searches the web and returns summarized results.",
  "entrypoint": "main.py"
}
```
