---
name: compliance-orchestrator
description: Orchestrates compliance workflows from control mapping to audit-ready response.
---

# compliance-orchestrator

## Overview
Orchestrates compliance workflows from control mapping to audit-ready response.

## Orchestration Flow
1) compliance-control-mapping -> 2) compliance-evidence-collector -> 3) compliance-gap-analysis -> 4) compliance-remediation-plan -> 5) compliance-audit-response

## Input Contract
- Applicable frameworks and regulations
- Current control inventory
- Audit timeline and evidence scope

## Output Contract
- Traceable control-to-requirement map
- Prioritized remediation roadmap
- Audit response package

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.
