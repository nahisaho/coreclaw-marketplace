---
name: learning-assistant
description: |
  Learning Design and Assessment skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Learning Design and Assessment

This suite is a coordinated skill package under `learning`.

## Package Structure

- Root skill: `learning-assistant`
- Orchestrator skill: `learning-orchestrator`
- Specialized sub-skills: domain-focused execution skills

## Orchestration Principle

The orchestrator routes tasks to specialized sub-skills in sequence,
checks intermediate quality gates, and consolidates outputs into a
final actionable result.

## Common Output Requirements

- Explicit assumptions and constraints
- Traceable reasoning between steps
- Final recommendation with next actions
