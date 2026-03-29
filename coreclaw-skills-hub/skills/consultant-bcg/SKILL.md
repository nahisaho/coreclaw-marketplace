---
name: consultant-bcg
description: |
    BCG (Boston Consulting Group) style consulting skill for deep research and analysis.
    Features Growth-Share Matrix, Experience Curve, Strategy Palette, Hypothesis-Driven Approach,
    TSR Analysis, Advantage Matrix, and Bionic Company Framework.
    4-phase workflow: Purpose Discovery → Deep Research → Framework Analysis → Report Writing.
    Supports Deep Research MCP for enhanced web research capabilities.
---

# Consultant BCG (Boston Consulting Group-Style Consulting)

BCG (Boston Consulting Group) style consulting skill for deep research and analysis. Features Growth-Share Matrix, Experience Curve, Strategy Palette, Hypothesis-Driven Approach, TSR Analysis, Advantage Matrix, and Bionic Company Framework. 4-phase workflow: Purpose Discovery → Deep Research → Framework Analysis → Report Writing. Supports Deep Research MCP for enhanced web research capabilities.

## Use This Skill When

- A strategy, portfolio, or transformation problem needs BCG-style framing.
- Growth, competitive advantage, TSR, or bionic transformation analysis must be structured into a staged workflow.
- The engagement requires saved, reusable artifacts rather than chat-only analysis.

## Local Resources

- `prompts/`: phased flows for discovery, research, framework analysis, and reporting.
- `skills/`: orchestrator support for routing and framework application.
- Use `deep-research` MCP when available for structured external research.

## Required Inputs

- Client objective, portfolio scope, and strategic decision to support.
- Available evidence, assumptions, timing, and review constraints.
- Required report format, metrics, and decision criteria.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: strategic question, method, framework output, recommendation, and file inventory.
- `results/`: matrices, scorecards, portfolio classifications, and structured evidence summaries.
- `figures/`: English-only strategy visuals, portfolio charts, or comparison plots when needed.
- `data/`: normalized source material when transformation occurs.

## Quality Gates

- The chosen BCG-style framework matches the client objective and evidence quality.
- Assumptions, calculations, and recommendation logic are traceable.
- Final outputs contain actionable next steps and saved supporting artifacts.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated files.
