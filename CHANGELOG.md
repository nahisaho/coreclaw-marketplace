# Changelog

All notable changes to this repository are documented in this file.

The format is based on Keep a Changelog and the project uses semantic version tags for skills.

## [Unreleased]

## [2026-03-29]

### Changed

- Reorganized installable skill content so published assets no longer depend on nested `source/` directories.
- Converted validation, registry preview, and release metadata flows to use `SKILL.md` frontmatter as the canonical source.
- Optimized the `scientist` suite and 195 `scientific-*` skills into compact execution-contract oriented skill definitions.
- Simplified `agent-skills-builder` to generate Agent Skills artifacts only and updated its runtime contract and documentation.
- Bumped skill versions for the updated release set, including `agent-skills-builder` to `v0.10.0`, `scientist` to `v0.6.0`, updated imported suite markers to `v0.3.0`, and updated changed `scientific-*` imported markers to `v0.2.0`.

### Removed

- Repository-wide compatibility `skill.json` files now that `SKILL.md` frontmatter is the source of truth.
- Placeholder or wrapper `main.py` files under imported skills, retaining only the real runtime for `agent-skills-builder`.
- Mirrored `source/SKILL.md` files that previously interfered with validation.

### Added

- Top-level English and Japanese repository guides.
- Initial repository changelog.

## [2026-03-27]

### Added

- English and Japanese documentation sets under `docs/`.
- Skills development guide and registry/CI documentation.
- Group metadata files for skill groups with English descriptions.
- MIT license at the repository root.

### Changed

- Reorganized documentation so Japanese files use the `_ja.md` suffix.
- Updated skill group descriptions to English in `group.json`.

## [2026-03-26]

### Added

- Registry preview generation for pull requests.
- Documentation for imported skill layout.

### Changed

- Validation workflow now uploads a preview registry artifact instead of mutating repository state on PRs.
- Release and validation workflows now support nested skill paths.
- Registry generation and validation updated for group-level metadata support.

### Fixed

- Added root-level `SKILL.md` files for imported skills.
- Fixed nested skill path handling across workflows and scripts.

## [2026-03-25]

### Added

- Initial import of Coreclaw skills into the marketplace at version `v0.1.0`.
