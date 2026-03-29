---
name: compliance
description: |
  Compliance and Audit Automation skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Compliance and Audit Automation

Compliance and Audit Automation skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- A compliance workflow requires multiple specialized checks in sequence.
- Evidence collection, gap analysis, remediation planning, or control mapping must be coordinated.
- Intermediate outputs must be validated before a final recommendation is issued.

## Local Resources

- Route through `compliance-orchestrator` when multiple compliance sub-skills are needed.
- Use the domain-focused sub-skills for execution once the objective and evidence path are clear.

## Required Inputs

- Compliance objective, framework, regulation, or audit scope.
- Available evidence, constraints, deadlines, and decision thresholds.
- Required deliverables, approval points, and reporting audience.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: scope, findings, recommendations, and file inventory.
- `results/`: mappings, evidence summaries, remediation plans, or structured assessment outputs.
- `data/`: normalized inputs or processed evidence when transformation occurs.

## Quality Gates

- Outputs include explicit assumptions, constraints, and compliance scope.
- Evidence and reasoning are traceable from source inputs to recommendations.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference the generated artifacts.
