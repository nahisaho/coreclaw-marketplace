---
name: diligence
description: |
  Investment and Due Diligence skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Investment and Due Diligence

Investment and Due Diligence skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- A diligence workflow requires market, risk, financial, and memo outputs to be coordinated.
- Multiple diligence sub-skills must contribute to a single investment recommendation.
- Intermediate outputs need quality checks before the final decision package is issued.

## Local Resources

- Route through `diligence-orchestrator` only when multiple diligence sub-skills are required.
- Use the specialized diligence sub-skills directly for focused execution.

## Required Inputs

- Investment question, target scope, and decision timeline.
- Available diligence materials, constraints, and review thresholds.
- Required deliverables, approval points, and reporting audience.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: scope, findings, investment recommendation, and file inventory.
- `results/`: diligence analyses, memos, matrices, and structured evidence outputs.
- `data/`: processed source inputs when normalization or extraction occurs.

## Quality Gates

- Outputs include explicit assumptions, constraints, and diligence scope.
- Reasoning is traceable from source evidence to recommendation.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
