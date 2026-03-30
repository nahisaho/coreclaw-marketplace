---
name: agent-skills-builder
description: |
  Builder skill that designs and generates Agent Skills compliant packages through user dialogue.
  Discovers the true objective behind surface-level requests, then designs,
  generates, validates, and distributes skill configurations for GitHub Copilot CLI and related runtimes.
---

# Agent Skills Builder v0.10.0

A builder that creates Agent Skills compliant packages through dialogue-based requirements discovery.

## Use This Skill When

- A user wants to create a new Agent Skill from an ambiguous or high-level request.
- The work requires structured requirements discovery before file generation.
- A single skill or suite collection must be scaffolded and validated.

## Local Resources

- `skills/`: orchestrator, discovery, planning, generation, validation, harness, and release sub-skills.
- Generate Agent Skills output only.
- Save generated outputs under `coreclaw-skills-hub/.artifacts/generated-skills/` and bundle a ZIP when requested.

## Required Inputs

- Skill or suite name and the user's surface request.
- Background problem, success criteria, constraints, and agreed true objective.
- Structure choice: single skill or suite collection.
- Optional suite profile and any required frontmatter or tooling constraints.

## Workflow

1. Use `skills/orchestrator/SKILL.md` to classify the request and pick the smallest valid build path.
2. Use `skills/purpose-discovery/SKILL.md` when requirements are still ambiguous.
3. Use `skills/architecture-planner/SKILL.md` and, when needed, `skills/harness-designer/SKILL.md` to design the output package.
4. Generate files with `skills/single-skill-generation/SKILL.md` or `skills/suite-generation/SKILL.md` and validate them with `skills/validator/SKILL.md` before packaging outputs.

## Deliverables

- Generated skill or suite files under `coreclaw-skills-hub/.artifacts/generated-skills/`.
- `orchestration.json` plus `agents/*.md` files when suite-style output is selected.
- `hooks/hooks.json`, `scripts/hooks/*.js`, `docs/harness-audit.md`, and `commands/*.md` harness scaffolds for suite-style output.
- Validation summary and generated file inventory.
- True objective summary and chosen architecture rationale.
- ZIP bundle path when bundling is requested.

## Quality Gates

- One-question-at-a-time dialogue is maintained until the true objective is confirmed.
- Every generated `SKILL.md` has valid frontmatter and a directory name matching `name`.
- Generated output remains Agent Skills compliant.
- Generated artifacts are saved to a workspace-visible location and validated before delivery.
- Suite-style output includes one orchestrator manifest, one execution agent manifest, and one sub-agent manifest per specialized role.
- Suite-style output can include hook, audit, and eval scaffolds with selectable harness enforcement profiles.

## Sub-Skills

- `skills/orchestrator/SKILL.md`: route the request to single-skill, suite, or release-check workflows.
- `skills/purpose-discovery/SKILL.md`: collect the true objective through one-question dialogue.
- `skills/architecture-planner/SKILL.md`: decide structure, files, contracts, and role boundaries.
- `skills/single-skill-generation/SKILL.md`: generate a compact single-skill package.
- `skills/suite-generation/SKILL.md`: generate orchestrator, agent, sub-agent, and harness assets.
- `skills/harness-designer/SKILL.md`: define hook, audit, eval, and checkpoint scaffolds.
- `skills/validator/SKILL.md`: validate frontmatter, naming, file completeness, and packaging.
- `skills/release-readiness/SKILL.md`: summarize artifacts, ZIP status, release tag, and registry follow-up.

## Operating Rule

- Keep the parent `SKILL.md` as the entry point only.
- Push specialized execution logic into nested `skills/<name>/SKILL.md` files.
- Reuse the smallest number of sub-skills needed for the current request.
