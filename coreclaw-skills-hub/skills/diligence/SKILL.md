---
name: diligence-assistant
description: |
  Investment and Due Diligence skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Investment and Due Diligence

This suite is a coordinated skill package under `diligence`.

## Package Structure

- Root skill: `diligence-assistant`
- Orchestrator skill: `diligence-orchestrator`
- Specialized sub-skills: domain-focused execution skills

## Orchestration Principle

The orchestrator routes tasks to specialized sub-skills in sequence,
checks intermediate quality gates, and consolidates outputs into a
final actionable result.

## Common Output Requirements

- Explicit assumptions and constraints
- Traceable reasoning between steps
- Final recommendation with next actions
