---
name: enterprise-assistant
description: |
  Enterprise Transformation skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Enterprise Transformation

This suite is a coordinated skill package under `enterprise`.

## Package Structure

- Root skill: `enterprise-assistant`
- Orchestrator skill: `enterprise-orchestrator`
- Specialized sub-skills: domain-focused execution skills

## Orchestration Principle

The orchestrator routes tasks to specialized sub-skills in sequence,
checks intermediate quality gates, and consolidates outputs into a
final actionable result.

## Common Output Requirements

- Explicit assumptions and constraints
- Traceable reasoning between steps
- Final recommendation with next actions
