---
name: consultant-acn
description: |
    Accenture style consulting skill for deep research and analysis.
    Features DX Strategy Framework, Digital Maturity Assessment, Zero-Based Budgeting (ZBB),
    Cost Excellence, Intelligent Operations, and Value Creation Framework.
    4-phase workflow: Purpose Discovery → Deep Research → Framework Analysis → Report Writing.
    Supports Deep Research MCP for enhanced web research capabilities.
---

# Consultant ACN (Accenture-Style Consulting)

Accenture style consulting skill for deep research and analysis. Features DX Strategy Framework, Digital Maturity Assessment, Zero-Based Budgeting (ZBB), Cost Excellence, Intelligent Operations, and Value Creation Framework. 4-phase workflow: Purpose Discovery → Deep Research → Framework Analysis → Report Writing. Supports Deep Research MCP for enhanced web research capabilities.

## Use This Skill When

- A transformation or strategy problem needs Accenture-style framework selection.
- DX, cost transformation, operations, or value creation work must be structured into a staged consulting flow.
- Research and recommendations must be saved as reusable delivery artifacts.

## Local Resources

- `prompts/`: phased consulting flows for discovery, research, analysis, and reporting.
- `skills/`: nested Agent Skills including `orchestrator/SKILL.md` for routing and framework application.
- Use `deep-research` MCP when available for structured external research.

## Required Inputs

- Client objective, target business unit, and decision horizon.
- Available evidence, operating context, assumptions, and delivery deadline.
- Required report format, decision criteria, and review expectations.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: problem definition, method, framework output, recommendation, and file inventory.
- `results/`: structured framework outputs, matrices, assessments, and evidence summaries.
- `figures/`: English-only charts or transformation visuals when needed.
- `data/`: processed source material when transformation or normalization occurs.

## Quality Gates

- The selected ACN-style framework matches the client objective and constraints.
- Evidence, assumptions, and calculations are traceable from source to recommendation.
- Final outputs contain concrete next actions and saved supporting artifacts.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated files.
