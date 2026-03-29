---
name: learning
description: |
  Learning Design and Assessment skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Learning Design and Assessment

Learning Design and Assessment skill suite for coordinated multi-step workflows. Includes an orchestrator plus specialized sub-skills designed to produce higher-quality outcomes through structured chaining.

## Use This Skill When

- A learning workflow needs objective design, activity generation, curriculum building, rubric design, or feedback analysis.
- Multiple learning sub-skills must contribute to a single instructional recommendation.
- Intermediate outputs require validation before the final learning design is issued.

## Local Resources

- Route through `learning-orchestrator` when multiple learning sub-skills are required.
- Use the specialized learning sub-skills directly for narrow execution tasks.

## Required Inputs

- Learning objective, audience, constraints, and delivery context.
- Available materials, evidence, deadlines, and assessment needs.
- Required deliverables, review expectations, and success criteria.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, method, recommendation, and file inventory.
- `results/`: curriculum outputs, rubrics, activities, analyses, and structured learning artifacts.
- `figures/`: English-only charts or visuals when helpful.
- `data/`: processed source inputs when transformation occurs.

## Quality Gates

- Outputs include explicit assumptions, audience context, and constraints.
- Reasoning is traceable from source inputs to recommendation.
- Final recommendations are actionable and saved as files.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
