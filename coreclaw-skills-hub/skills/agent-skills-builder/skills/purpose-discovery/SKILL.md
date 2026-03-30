---
name: purpose-discovery
description: |
  Clarify the user's true objective for an Agent Skills package through one-question-at-a-time dialogue.
  Use when the request is still too ambiguous to choose a concrete package topology.
---

# Purpose Discovery

## Goal

Clarify what the user actually needs to ship before any files are generated.

## Dialogue Rules

1. Ask exactly one question at a time.
2. Prefer questions that reduce architecture ambiguity.
3. Confirm the true objective before generation starts.
4. Stop asking questions as soon as the remaining ambiguity no longer changes the package design.

## Required Outputs

- Surface request summary
- True objective in plain language
- Success criteria
- Constraints
- Chosen structure: single skill or suite