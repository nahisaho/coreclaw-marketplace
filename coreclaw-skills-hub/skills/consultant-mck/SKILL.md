---
name: consultant-mck
description: |
  McKinsey style consulting skill for deep research and analysis.
  Features 7S Framework, Hypothesis-Driven Approach, Issue Tree, Pyramid Principle,
  Three Horizons, Granularity of Growth, OVA, Profit Pool Analysis, and SCP Analysis.
  McKinsey-style 5-phase workflow: Problem Definition → Hypothesis → Issue Decomposition →
  Data Collection/Analysis → Integration/Recommendation.
  Supports Deep Research MCP for enhanced web research capabilities.
---

# Consultant MCK (McKinsey-Style Consulting)

McKinsey style consulting skill for deep research and analysis. Features 7S Framework, Hypothesis-Driven Approach, Issue Tree, Pyramid Principle, Three Horizons, Granularity of Growth, OVA, Profit Pool Analysis, and SCP Analysis. McKinsey-style 5-phase workflow: Problem Definition → Hypothesis → Issue Decomposition → Data Collection/Analysis → Integration/Recommendation. Supports Deep Research MCP for enhanced web research capabilities.

## Use This Skill When

- A problem needs McKinsey-style hypothesis-driven decomposition and synthesis.
- Strategy, growth, operating model, or market structure work must be framed into a structured consulting flow.
- The final output must be decision-oriented, file-first, and presentation ready.

## Local Resources

- `prompts/`: phased flows for discovery, research, framework analysis, and reporting.
- `skills/`: nested Agent Skills including `orchestrator/SKILL.md` for routing and framework application.

## Required Inputs

- Client objective, decision to support, and operating context.
- Available evidence, hypotheses, assumptions, and delivery timeline.
- Required output format, review gates, and success criteria.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: problem, hypothesis, analysis, recommendation, and file inventory.
- `results/`: issue trees, framework outputs, analyses, and evidence summaries.
- `figures/`: English-only charts or synthesis visuals when helpful.
- `data/`: processed or normalized source material when transformation occurs.

## Quality Gates

- The selected McKinsey-style framework matches the problem and evidence quality.
- Hypotheses, assumptions, and calculations are traceable from inputs to conclusions.
- Final outputs contain actionable recommendations and saved supporting artifacts.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated files.
