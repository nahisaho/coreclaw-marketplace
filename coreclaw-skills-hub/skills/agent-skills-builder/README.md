# agent-skills-builder

Builds production-ready CoreClaw skill packages from requirements with schema validation and release-ready outputs.

## Features

- Dialogue-driven requirement discovery with users
- Proactive proposal generation to surface hidden needs
- Creates complete skill package structures
- Generates valid `skill.json`, `README.md`, and `SKILL.md`
- Applies naming/versioning conventions
- Performs pre-release validation checks
- Produces release tag suggestions
- Enforces authoring limits (main skill <= 1500 chars, sub-skills <= 2000 chars)

## Quick Start

```bash
python main.py
```

## Output

This skill helps generate:

- `skill.json` with required fields
- `main.py` entrypoint template
- `README.md` and `SKILL.md` documentation
- optional `group.json` for top-level groups
- release-ready tag format (`<skill-path>/vX.Y.Z`)
