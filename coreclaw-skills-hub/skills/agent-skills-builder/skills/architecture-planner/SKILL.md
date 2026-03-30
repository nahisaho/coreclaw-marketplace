---
name: architecture-planner
description: |
  Convert a confirmed objective into a concrete Agent Skills package topology and file inventory.
  Use when deciding structure type, role boundaries, and required artifacts.
---

# Architecture Planner

## Responsibilities

- Choose single-skill or suite architecture.
- Define the file inventory before generation starts.
- Define role boundaries for orchestrator, execution agent, and sub-agents.
- Keep the design as small as possible while meeting the objective.

## Planning Rules

1. Prefer a single skill unless explicit separation is useful.
2. Add suite roles only when they reduce ambiguity or improve maintainability.
3. Add harness assets only when requested or clearly beneficial.
4. Keep optional metadata out of the core design until the file topology is stable.