---
name: scientific-gdc-portal
description: |
 GDC Portal skill. Genomic Data Commons cancer data retrieval, mutation frequency analysis, clinical-genomic correlation, and multi-project data integration.
---

# GDC Portal

GDC Portal skill. Genomic Data Commons cancer data retrieval, mutation frequency analysis, clinical-genomic correlation, and multi-project data integration.

## Use This Skill When

- Genomic Data Commons cancer data retrieval.
- Mutation frequency analysis.
- Clinical-genomic correlation.
- Multi-project data integration.

## Required Inputs

- Research objective, decision target, or hypothesis.
- Available data, source constraints, and domain assumptions.
- Required outputs, success metrics, and deadline or reproducibility constraints.

## Workflow

1. Confirm scope, assumptions, and the exact artifact set to save.
2. Apply the narrowest domain method that answers the request with defensible evidence.
3. Save code, tables, figures, and intermediate outputs to files instead of chat-only output.
4. State limitations, uncertainty, and any validation or sensitivity checks performed.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl`.

## Deliverables

- `report.md`: concise method, results, interpretation, and file inventory in the user's language.
- `results/`: structured outputs, metrics, model artifacts, or extracted findings.
- `figures/`: English-only charts, diagrams, or panels when visual output is needed.
- `data/`: processed or derived datasets when transformation occurs.

## Quality Gates

- The selected method matches the scientific question and stated assumptions.
- Outputs are reproducible, saved to files, and traceable from inputs to conclusions.
- Missing data, uncertainty, bias, and hard limits are made explicit.
- `report.md` and `logs/process-log.jsonl` reference the generated artifacts.
