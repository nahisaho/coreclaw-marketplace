---
name: scientific-cancer-genomics
description: |
 Cancer genomics skill. Somatic mutation analysis, copy number variation, tumor mutational burden, microsatellite instability, driver gene identification, and oncological pathway analysis.
---

# Cancer genomics

Cancer genomics skill. Somatic mutation analysis, copy number variation, tumor mutational burden, microsatellite instability, driver gene identification, and oncological pathway analysis.

## Use This Skill When

- Somatic mutation analysis.
- Copy number variation.
- Tumor mutational burden.
- Microsatellite instability.
- Driver gene identification.

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
