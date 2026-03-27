---
name: growth-assistant
description: |
  Product Growth Intelligence skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Product Growth Intelligence

This suite is a coordinated skill package under `growth`.

## Package Structure

- Root skill: `growth-assistant`
- Orchestrator skill: `growth-orchestrator`
- Specialized sub-skills: domain-focused execution skills

## Orchestration Principle

The orchestrator routes tasks to specialized sub-skills in sequence,
checks intermediate quality gates, and consolidates outputs into a
final actionable result.

## Common Output Requirements

- Explicit assumptions and constraints
- Traceable reasoning between steps
- Final recommendation with next actions
