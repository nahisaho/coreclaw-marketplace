---
name: consultant-pwc
description: |
  PwC style consulting skill for deep research and analysis.
  Features Fit for Growth, Strategy&, BXT (Business Experience Technology),
  TIMM (Total Impact Measurement & Management), Deal Value Creation,
  and Risk & Regulation frameworks.
  PwC-style integrated workflow combining strategy, technology, and business transformation.
  Supports Deep Research MCP for enhanced web research capabilities.
---

# Consultant PWC (PwC-Style Consulting)

PwC style consulting skill for deep research and analysis. Features Fit for Growth, Strategy&, BXT (Business Experience Technology), TIMM (Total Impact Measurement & Management), Deal Value Creation, and Risk & Regulation frameworks. PwC-style integrated workflow combining strategy, technology, and business transformation. Supports Deep Research MCP for enhanced web research capabilities.

## Use This Skill When

- A strategy, transformation, deal, or risk question needs PwC-style framing.
- Business, technology, and experience layers must be evaluated together.
- The engagement requires saved artifacts and explicit linkage from evidence to recommendation.

## Local Resources

- `prompts/`: phased flows for discovery, research, framework analysis, and reporting.
- `skills/`: nested Agent Skills including `orchestrator/SKILL.md` for routing and framework application.

## Required Inputs

- Client objective, target transformation or transaction scope, and decision horizon.
- Available evidence, technology context, assumptions, and time constraints.
- Required reporting format, approval expectations, and success criteria.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, method, framework output, recommendation, and file inventory.
- `results/`: structured framework outputs, risk assessments, and evidence summaries.
- `figures/`: English-only diagrams or charts when visual outputs improve clarity.
- `data/`: transformed source material when normalization or enrichment occurs.

## Quality Gates

- The selected PwC-style framework matches the client objective and constraints.
- Assumptions, calculations, and recommendation logic are traceable.
- Final outputs include concrete next actions and saved supporting artifacts.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated files.
