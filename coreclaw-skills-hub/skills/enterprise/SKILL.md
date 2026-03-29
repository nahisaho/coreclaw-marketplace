---
name: enterprise
description: |
  Enterprise Transformation skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Enterprise Transformation

Enterprise Transformation skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- An enterprise transformation workflow needs multiple specialized sub-skills in sequence.
- Briefing, prioritization, diagnostics, or roadmap outputs must be coordinated.
- Intermediate outputs require validation before a final recommendation is issued.

## Local Resources

- Route through `enterprise-orchestrator` when multiple enterprise sub-skills are needed.
- Use the domain-focused enterprise sub-skills directly for narrow execution tasks.

## Required Inputs

- Transformation objective, enterprise scope, and decision horizon.
- Available evidence, constraints, stakeholders, and timeline.
- Required deliverables, review checkpoints, and audience.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, findings, recommendation, and file inventory.
- `results/`: diagnostics, prioritization outputs, briefs, and structured transformation artifacts.
- `data/`: processed inputs when transformation or normalization occurs.

## Quality Gates

- Outputs include explicit assumptions, enterprise scope, and constraints.
- Evidence and reasoning are traceable from source inputs to recommendations.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
