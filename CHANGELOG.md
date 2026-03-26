# Changelog

All notable changes to this repository are documented in this file.

The format is based on Keep a Changelog and the project uses semantic version tags for skills.

## [Unreleased]

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
