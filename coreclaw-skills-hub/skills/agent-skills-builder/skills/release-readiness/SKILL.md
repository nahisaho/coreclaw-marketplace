---
name: release-readiness
description: |
  Summarize whether a generated Agent Skills package is ready for packaging, tagging, and registry publication.
  Use when validation is complete and a release-oriented status report is needed.
---

# Release Readiness

## Output Checklist

- Generated file inventory
- Validation results
- Artifact-visible output path
- ZIP path when requested
- Suggested release tag format
- Registry follow-up note when publication is in scope

## Decision Rules

1. Do not call the package ready if required files are missing.
2. Do not recommend tagging before validation passes.
3. When suite assets exist, confirm manifests and orchestration files are included in the inventory.