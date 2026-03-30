---
name: validator
description: |
  Validate generated Agent Skills outputs before packaging or release recommendations.
  Use when checking frontmatter, naming, file completeness, suite topology, or ZIP readiness.
---

# Validator

## Core Checks

| Gate | Check |
|------|-------|
| G1 | `SKILL.md` has `name` and `description` frontmatter |
| G2 | Directory name matches frontmatter `name` |
| G3 | Required files exist for the selected structure |
| G4 | Generated outputs are saved under the artifact-visible path |
| G5 | Suite manifests and `orchestration.json` exist when suite mode is selected |
| G6 | Harness files exist when harness scaffolding is enabled |
| G7 | ZIP exists and is non-empty when bundling is requested |

## Recovery Rules

1. Regenerate only the failed component when possible.
2. If a required field is missing, fail fast and report the exact missing field.
3. If suite topology is incomplete, do not mark the package release-ready.