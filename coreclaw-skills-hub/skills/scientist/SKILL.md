---
name: scientist
description: |
 Scientific research suite with 195 specialized sub-skills.
 Covers literature review, experimental design, data analysis, modeling,
 bioinformatics, cheminformatics, visualization, and publication-ready reporting.
 Requires file-first outputs, verification gates, and timestamped execution logging.
---

# Scientist v0.7.0

Scientific research suite with 195 sub-skills. Route work to the smallest suitable sub-skill, save all outputs as files, and leave a complete timestamped execution trace.

## Core Rules

- Write `report.md` in the same language as the user's input.
- Keep all figure, chart, axis, legend, and annotation text in English.
- Save every artifact to files. Do not leave analysis, code, tables, or figures only in chat.
- Prefer the narrowest matching sub-skill instead of loading broad context.
- Final chat output should summarize saved files, not reproduce the full analysis.

## Required Output Layout

Use this structure unless the task requires a stricter downstream format.

```text
/workspace/group/
├── report.md
├── figures/
├── results/
├── data/
└── logs/
	└── process-log.jsonl
```

Minimum file expectations:

- `report.md`: title, execution timestamp, objective, methods, results, discussion, generated file inventory.
- `figures/`: saved plots only; never rely on interactive display.
- `results/`: numeric summaries, model outputs, metrics, or structured intermediate results.
- `data/`: processed datasets when data transformation occurs.
- `logs/process-log.jsonl`: append-only execution trace with one JSON object per event.

## Required Execution Logging

For every task, write a timestamped process log to `logs/process-log.jsonl`. The log must capture the full workflow, including:

- the user prompt actually used for the run
- each selected sub-skill or external prompt template
- information passed into each skill or tool handoff
- information received back from each skill or tool handoff
- every file created, updated, or finalized
- any recovery action, retry, or fallback decision

Required event fields:

- `timestamp`
- `phase`
- `event_type`
- `actor`
- `input_prompt`
- `skill_or_tool`
- `handoff_in`
- `handoff_out`
- `files_written`
- `status`

Recommended event order:

1. `run_started`
2. `prompt_received`
3. `skill_selected` for each invoked sub-skill
4. `handoff_started` and `handoff_completed` for each transfer
5. `file_written` whenever a file is created or updated
6. `report_finalized`
7. `run_completed`

Example record:

```json
{"timestamp":"2026-03-29T10:15:00Z","phase":"EXECUTE","event_type":"skill_selected","actor":"scientist","input_prompt":"optimize the assay design","skill_or_tool":"scientific-doe","handoff_in":{"objective":"maximize yield"},"handoff_out":{"design_type":"fractional-factorial"},"files_written":["results/doe_plan.json"],"status":"ok"}
```

## Verification Loop

Every execution follows this loop:

1. `PLAN`: define objective, constraints, target outputs, and candidate sub-skills.
2. `EXECUTE`: run the selected analysis pipeline and save intermediate artifacts.
3. `VERIFY`: check outputs against scientific and formatting quality gates.
4. `REPORT`: write `report.md` in the user's language and embed saved figures.
5. `LOG`: finalize `logs/process-log.jsonl` and confirm the generated file inventory.

## Quality Gates

- [ ] Figures are saved to `figures/` and referenced from `report.md`.
- [ ] Numeric and structured outputs are saved under `results/`.
- [ ] `report.md` includes timestamp, methods, results, discussion, and file inventory.
- [ ] Figure text is English-only.
- [ ] `logs/process-log.jsonl` exists and includes prompt, sub-skill usage, handoff I/O, and files written with timestamps.
- [ ] No essential result remains chat-only.

## Coverage

- Data analysis: Bayesian statistics, time-series, anomaly detection, causal inference.
- Life sciences: genomics, proteomics, ADMET, clinical NLP, structural biology.
- Chemistry and materials: cheminformatics, molecular modeling, docking, simulations.
- Research workflows: systematic review, hypothesis design, DOE, reproducible reporting.
- Visualization and AI: advanced plotting, dashboards, ML, transfer learning, ensemble methods.

## Routing Notes

- Use `scientific-deep-research` when literature discovery and source synthesis dominate.
- Use the most domain-specific sub-skill available for computation-heavy tasks.
- Split work across sub-skills only when it improves correctness, reproducibility, or traceability.


