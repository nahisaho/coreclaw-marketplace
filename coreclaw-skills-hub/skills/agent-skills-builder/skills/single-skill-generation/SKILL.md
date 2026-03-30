---
name: single-skill-generation
description: |
  Generate the smallest valid Agent Skill package when orchestration is unnecessary.
  Use when one role can satisfy the request with a single SKILL.md package.
---

# Single Skill Generation

## Build Steps

1. Confirm the target skill name is valid kebab-case.
2. Draft frontmatter with `name` and `description` first.
3. Add concise usage guidance, examples, and edge cases.
4. Add optional metadata only when it changes runtime behavior.
5. Save output under the artifact-visible directory.
6. Bundle a ZIP only when requested.

## Minimum File Set

- `SKILL.md`