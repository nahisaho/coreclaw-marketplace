---
name: secops-orchestrator
description: Orchestrates security incident response from triage to post-incident improvement.
---

# secops-orchestrator

## Overview
Orchestrates security incident response from triage to post-incident improvement.

## Orchestration Flow
1) secops-alert-triage -> 2) secops-log-correlation -> 3) secops-root-cause-analysis -> 4) secops-containment-plan -> 5) secops-postmortem-writer

## Input Contract
- Alert metadata and environment scope
- Available logs and detection evidence
- Incident response constraints

## Output Contract
- Incident timeline and root-cause hypothesis
- Containment and recovery actions
- Postmortem with corrective/preventive actions

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.
