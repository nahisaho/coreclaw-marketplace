---
name: supply
description: |
  Supply Chain Decision skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Supply Chain Decision

Supply Chain Decision skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- A supply-chain workflow needs forecasting, inventory optimization, logistics simulation, supplier risk, or scenario planning.
- Multiple supply sub-skills must be coordinated into a single recommendation.
- Intermediate outputs require validation before the final decision package is issued.

## Local Resources

- Route through `supply-orchestrator` when multiple supply sub-skills are required.
- Use the specialized supply sub-skills directly for focused execution.

## Required Inputs

- Supply objective, network scope, and decision horizon.
- Available data, constraints, assumptions, and deadline.
- Required deliverables, review expectations, and decision criteria.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, findings, recommendation, and file inventory.
- `results/`: forecasts, optimization outputs, simulations, and structured supply artifacts.
- `figures/`: English-only charts or network visuals when needed.
- `data/`: processed source data when transformation occurs.

## Quality Gates

- Outputs include explicit assumptions, supply scope, and constraints.
- Evidence and reasoning are traceable from inputs to recommendation.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
