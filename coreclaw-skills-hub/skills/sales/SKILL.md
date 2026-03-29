---
name: sales
description: |
  Strategic Sales Enablement skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Strategic Sales Enablement

Strategic Sales Enablement skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- A sales workflow needs account research, questioning, objection handling, stakeholder mapping, or proposal building.
- Multiple sales sub-skills must contribute to a single enablement recommendation.
- Intermediate outputs require validation before the final sales package is issued.

## Local Resources

- Route through `sales-orchestrator` when multiple sales sub-skills are required.
- Use the specialized sales sub-skills directly for focused execution.

## Required Inputs

- Sales objective, account scope, buyer context, and decision stage.
- Available evidence, constraints, timing, and deal assumptions.
- Required deliverables, review expectations, and success criteria.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, findings, recommendation, and file inventory.
- `results/`: account research, sales messaging, mappings, and structured enablement artifacts.
- `figures/`: English-only charts or decision visuals when needed.
- `data/`: processed source inputs when transformation occurs.

## Quality Gates

- Outputs include explicit assumptions, buyer context, and constraints.
- Reasoning is traceable from source inputs to recommendation.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
