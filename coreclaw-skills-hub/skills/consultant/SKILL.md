---
name: consultant
description: |
    AI consultant skill for deep research and consulting analysis.
    Based on the SHIKIGAMI methodology, featuring 4-phase workflow:
    Purpose Discovery, Deep Research, Framework Analysis, and Report Writing.
    Provides 53 consulting frameworks across 14 categories with MECE validation,
    pyramid structuring, and hypothesis-driven analysis.
---

# Consultant Assistant

AI consultant skill for deep research and consulting analysis. Based on the SHIKIGAMI methodology, featuring 4-phase workflow: Purpose Discovery, Deep Research, Framework Analysis, and Report Writing. Provides 53 consulting frameworks across 14 categories with MECE validation, pyramid structuring, and hypothesis-driven analysis.

## Use This Skill When

- A consulting workflow requires staged discovery, research, analysis, and reporting.
- Structured framework selection is needed to turn ambiguous business questions into decisions.
- The final output must be traceable, file-first, and defensible for a client audience.

## Local Resources

- `prompts/`: purpose discovery, deep research, framework analysis, report writing, and full-research flows.
- `skills/`: orchestrator and framework-library helpers for routing and framework selection.
- Use `deep-research` MCP when available; otherwise keep the built-in staged workflow.

## Required Inputs

- Business objective, decision owner, constraints, and deadline.
- Available evidence, market context, assumptions, and required depth.
- Required deliverables, review gates, and recommendation format.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: executive summary, methods, analysis, recommendation, and file inventory.
- `results/`: research notes, framework outputs, scoring models, and structured decision artifacts.
- `figures/`: English-only charts or matrices when visual outputs improve decision quality.
- `data/`: cleaned market, financial, or operational data when transformation occurs.

## Quality Gates

- The selected phase and framework match the business question and constraints.
- Sources, assumptions, and calculations are traceable from inputs to recommendation.
- The final recommendation includes concrete next actions and saved artifacts.
- `report.md` and, when used, `logs/process-log.jsonl` reference the generated files.
