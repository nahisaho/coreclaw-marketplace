---
name: suite-generation
description: |
  Generate a suite package with explicit orchestrator, execution agent, sub-agent, and harness outputs.
  Use when the request requires multiple specialized roles and reviewable handoff contracts.
---

# Suite Generation

## Build Steps

1. Confirm the group name, title, and suite profile.
2. Identify the orchestrator, execution agent, and specialized sub-agents.
3. Generate the suite README and nested `skills/` directories.
4. Generate `agents/*.md` manifests and `orchestration.json`.
5. Generate harness scaffolds when enabled.
6. Validate topology, contracts, and file completeness.

## Minimum File Set

- `README.md`
- `orchestration.json`
- `skills/orchestrator/SKILL.md`
- one `SKILL.md` per specialized skill directory under `skills/`
- `agents/*.md`