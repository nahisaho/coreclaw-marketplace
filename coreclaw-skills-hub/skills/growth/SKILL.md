---
name: growth
description: |
  Product Growth Intelligence skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Product Growth Intelligence

Product Growth Intelligence skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- A growth workflow needs segmentation, funnel analysis, experiments, copy, or synthesis to be coordinated.
- Multiple growth sub-skills must contribute to a single optimization recommendation.
- Intermediate outputs require validation before a final decision is issued.

## Local Resources

- Route through `growth-orchestrator` when multiple growth sub-skills are needed.
- Use the specialized growth sub-skills directly for focused execution.

## Required Inputs

- Growth objective, target segment, and business metric to improve.
- Available evidence, constraints, data quality, and delivery timeline.
- Required deliverables, decision criteria, and audience.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, analysis, recommendation, and file inventory.
- `results/`: funnel outputs, experiment plans, segment analyses, and structured growth artifacts.
- `figures/`: English-only charts or growth visuals when needed.
- `data/`: processed source data when transformation occurs.

## Quality Gates

- Outputs include explicit assumptions, target metrics, and constraints.
- Evidence and reasoning are traceable from inputs to recommendation.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
