# coreclaw-marketplace

Marketplace repository for distributing Coreclaw skills.

This repository contains:

- `coreclaw-skills-hub/`: the packaged skills marketplace
- `docs/`: contributor and operations documentation
- `LICENSE`: MIT license for the repository

## Overview

The marketplace organizes skills under `coreclaw-skills-hub/skills/`.

- Group-level skills live at `skills/<group>/`
- Nested skills live at `skills/<group>/<skill-name>/`
- Each skill is released through a Git tag and published as a GitHub Release asset
- `registry.json` is updated by GitHub Actions on release tags

## Repository Structure

```text
.
├── coreclaw-skills-hub/
│   ├── skills/
│   ├── registry.json
│   └── .github/
├── docs/
│   ├── README.md
│   ├── README_ja.md
│   ├── SKILLS_GUIDE.md
│   ├── SKILLS_GUIDE_ja.md
│   ├── REGISTRY_AND_CI_CD.md
│   └── REGISTRY_AND_CI_CD_ja.md
├── CHANGELOG.md
├── LICENSE
└── README_ja.md
```

## Documentation

English documentation:

- [docs/README.md](docs/README.md)
- [docs/SKILLS_GUIDE.md](docs/SKILLS_GUIDE.md)
- [docs/REGISTRY_AND_CI_CD.md](docs/REGISTRY_AND_CI_CD.md)

Japanese documentation:

- [docs/README_ja.md](docs/README_ja.md)
- [docs/SKILLS_GUIDE_ja.md](docs/SKILLS_GUIDE_ja.md)
- [docs/REGISTRY_AND_CI_CD_ja.md](docs/REGISTRY_AND_CI_CD_ja.md)

## Quick Start

### Add a new skill

1. Create a skill directory under `coreclaw-skills-hub/skills/`
2. Add `skill.json`, `main.py`, `SKILL.md`, and `README.md`
3. If needed, add or update `group.json` for the skill group
4. Commit and push to `main`

Detailed instructions: [docs/SKILLS_GUIDE.md](docs/SKILLS_GUIDE.md)

### Release a skill

1. Update the version in `skill.json`
2. Commit and push the version change
3. Create and push a release tag such as `scientist/scientific-academic-writing/v0.2.0`

Detailed workflow: [docs/REGISTRY_AND_CI_CD.md](docs/REGISTRY_AND_CI_CD.md)

## Status

- Imported skills from `nahisaho/coreclaw`
- Nested skill paths supported in CI/CD
- PR validation generates a registry preview artifact
- Release tags publish assets and update `registry.json`
- Skill groups include English descriptions via `group.json`

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).

## Japanese Version

For the Japanese top-level guide, see [README_ja.md](README_ja.md).