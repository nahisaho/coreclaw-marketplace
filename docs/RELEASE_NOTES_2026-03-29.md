# Release Notes 2026-03-29

This document contains copy-ready GitHub Releases body text for the skills updated in the 2026-03-29 cleanup and version bump release.

## agent-skills-builder/v0.10.0

### Highlights

- Simplified the builder to generate Agent Skills artifacts only.
- Removed legacy CoreClaw output behavior and aligned the runtime contract with the current packaging model.
- Updated skill documentation and delivery expectations for generated artifacts.

### Included Changes

- `SKILL.md` frontmatter is now the canonical metadata source across validation and registry workflows.
- Legacy compatibility files and wrapper runtimes removed from imported skills.
- Release documentation updated to reflect the new builder-only Agent Skills path.

## scientist/v0.6.0

### Highlights

- Reworked the root scientist contract around file-first execution and required artifact logging.
- Aligned the suite with compact execution-contract style optimized for harness-driven use.
- Coordinated the cleanup of 195 `scientific-*` skills and their imported version updates.

### Included Changes

- Required output layout standardized around `report.md`, `figures/`, `results/`, `data/`, and `logs/process-log.jsonl`.
- Root suite documentation refreshed to match the new execution contract.
- Updated imported scientific sub-skill markers to `v0.5.1` where affected by this release.

## Imported Suite Releases v0.3.0

Use the following body for each suite tag listed below.

### Shared Body

#### Highlights

- Refreshed the imported suite package to `v0.3.0` after the repository-wide cleanup.
- Removed obsolete compatibility-layer artifacts from the imported skill layout.
- Aligned suite metadata and release tooling with `SKILL.md` frontmatter as the canonical source.

#### Included Changes

- Removed legacy `skill.json`, wrapper `main.py`, and mirrored `source/SKILL.md` compatibility files from imported skills.
- Kept installable skill content in the published layout expected by the marketplace.
- Updated imported version markers in suite documentation to `v0.3.0`.

### compliance/v0.3.0

Use the Shared Body section above.

### consultant/v0.3.0

Use the Shared Body section above.

### consultant-acn/v0.3.0

Use the Shared Body section above.

### consultant-bcg/v0.3.0

Use the Shared Body section above.

### consultant-mck/v0.3.0

Use the Shared Body section above.

### consultant-pwc/v0.3.0

Use the Shared Body section above.

### diligence/v0.3.0

Use the Shared Body section above.

### educationalist/v0.3.0

Use the Shared Body section above.

### enterprise/v0.3.0

Use the Shared Body section above.

### growth/v0.3.0

Use the Shared Body section above.

### learning/v0.3.0

Use the Shared Body section above.

### sales/v0.3.0

Use the Shared Body section above.

### secops/v0.3.0

Use the Shared Body section above.

### supply/v0.3.0

Use the Shared Body section above.

## Scientific Subskill Releases v0.5.1

Use the following body for each `scientific-*` tag added in this release.

### Shared Body

#### Highlights

- Refreshed the imported scientific subskill package to `v0.5.1`.
- Aligned the subskill with the scientist suite cleanup and compact execution-contract format.
- Removed compatibility-layer artifacts from the imported skill layout.

#### Included Changes

- Updated imported version markers in subskill documentation to `v0.5.1`.
- Removed legacy `skill.json`, compatibility wrapper `main.py`, and mirrored `source/SKILL.md` files.
- Kept the published layout compatible with the current `SKILL.md`-native validation and release pipeline.