---
name: secops
description: |
  Security Incident Response skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Security Incident Response

Security Incident Response skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- An incident-response workflow needs alert triage, correlation, root-cause analysis, containment, or postmortem work.
- Multiple secops sub-skills must be coordinated into a single response package.
- Intermediate outputs need validation before the final recommendation or report is issued.

## Local Resources

- Route through `secops-orchestrator` when multiple incident-response sub-skills are required.
- Use the specialized secops sub-skills directly for narrow execution tasks.

## Required Inputs

- Incident objective, affected scope, severity, and decision timeline.
- Available evidence, constraints, systems context, and review thresholds.
- Required deliverables, escalation expectations, and reporting audience.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: incident summary, findings, actions, and file inventory.
- `results/`: triage outputs, correlation analyses, RCA artifacts, and structured response outputs.
- `data/`: normalized evidence when transformation occurs.

## Quality Gates

- Outputs include explicit assumptions, incident scope, and constraints.
- Evidence and reasoning are traceable from source inputs to recommendation.
- Final actions are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
