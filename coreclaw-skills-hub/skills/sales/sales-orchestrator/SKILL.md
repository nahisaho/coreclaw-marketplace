---
name: sales-orchestrator
description: Orchestrates strategic sales workflows from account intelligence to proposal output.
---

# sales-orchestrator

## Overview
Orchestrates strategic sales workflows from account intelligence to proposal output.

## Orchestration Flow
1) sales-account-research -> 2) sales-stakeholder-mapping -> 3) sales-discovery-questioning -> 4) sales-objection-handling -> 5) sales-proposal-builder

## Input Contract
- Account target and deal context
- Stage, stakeholders, and constraints
- Value proposition hypotheses

## Output Contract
- Account strategy summary
- Discovery and objection playbook
- Stakeholder-aligned proposal draft

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.
