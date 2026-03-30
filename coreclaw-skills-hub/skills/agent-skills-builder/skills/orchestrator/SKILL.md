---
name: orchestrator
description: |
  Route an agent-skills-builder request to the smallest valid sub-skill flow.
  Use when deciding whether work should go to discovery, single-skill generation,
  suite generation, validation, harness design, or release readiness.
---

# Orchestrator

## Use This Skill When

- The request is still ambiguous.
- You need to decide between single-skill and suite generation.
- You need to choose the next specialized sub-skill.

## Routing Table

| Request Pattern | Route |
|-----------------|-------|
| One focused capability, one role | `../single-skill-generation/SKILL.md` |
| Orchestrator, agent, sub-agent, or multiple specialties | `../suite-generation/SKILL.md` |
| Hooks, eval, audit, checkpoint requirements | `../harness-designer/SKILL.md` then `../suite-generation/SKILL.md` |
| Packaging, tagging, or handoff summary | `../release-readiness/SKILL.md` |
| Ambiguous request | `../purpose-discovery/SKILL.md` first |

## Escalation Rules

- Escalate to `../architecture-planner/SKILL.md` when structure choice is not obvious.
- Escalate to `../validator/SKILL.md` before declaring the package complete.