---
name: co-growth
description: |
  Harness-optimized product growth intelligence partner with 7 sub-skills.
  Structured growth loops: user segmentation → funnel analysis → experiment design →
  copy variants → learning synthesis. Use when driving product growth, optimizing funnels,
  designing A/B experiments, or managing growth backlogs.
---

# Co-Growth v0.1.0

Product growth intelligence partner with 7 sub-skills. Route work to the narrowest sub-skill, save all outputs as files, and leave a complete execution trace.

## Core Rules

- Write `report.md` in the same language as the user's input.
- Keep all figure, chart, axis, legend, and annotation text in English.
- Save every artifact to files. Do not leave analysis, code, tables, or figures only in chat.
- Prefer the narrowest matching sub-skill instead of loading broad context.
- Final chat output should summarize saved files, not reproduce the full analysis.

## Routing Rules

### WHEN/DO Dispatch

WHEN: User requests user segmentation, cohort definition, or persona creation
DO: → `co-growth-user-segmentation`

WHEN: User requests funnel analysis, conversion analysis, or drop-off diagnostics
DO: → `co-growth-funnel-analysis`

WHEN: User requests A/B test design, experiment planning, or hypothesis formulation
DO: → `co-growth-experiment-design`

WHEN: User requests copy variants, messaging alternatives, or CTA options for experiments
DO: → `co-growth-copy-variants`

WHEN: User requests experiment result interpretation, Scale/Iterate/Kill decisions
DO: → `co-growth-learning-synthesis`

WHEN: User requests deep research on growth benchmarks, competitive analysis, or market data
DO: → `co-growth-deep-research`

WHEN: User records a growth learning, updates Gotchas, or captures experiment takeaways
DO: → `co-growth-learning-capture`

### Task Classification

1. Is user segmentation or cohort work needed?
   - YES → `co-growth-user-segmentation`
   - NO → next
2. Is funnel or conversion analysis needed?
   - YES → `co-growth-funnel-analysis`
   - NO → next
3. Is an experiment being designed?
   - YES → `co-growth-experiment-design`
   - NO → next
4. Are copy/messaging variants needed?
   - YES → `co-growth-copy-variants`
   - NO → next
5. Are experiment results being reviewed?
   - YES → `co-growth-learning-synthesis`
   - NO → next
6. Is external growth research needed?
   - YES → `co-growth-deep-research`
   - NO → `co-growth-learning-capture` for knowledge persistence

### Full Growth Loop Workflow

Phase 0 → `co-growth-user-segmentation`: Define target segments ⏸️ User approval
Phase 1 → `co-growth-funnel-analysis`: Identify conversion bottlenecks ⏸️ User approval
Phase 2 → `co-growth-experiment-design`: Design experiment ⏸️ User approval
Phase 3 → `co-growth-copy-variants`: Generate variant messaging
Phase 4 → `co-growth-learning-synthesis`: Analyze results & decide ⏸️ User approval
Phase 5 → `co-growth-learning-capture`: Record learnings

### Urgency Triage

| Priority | Condition | Action |
|----------|-----------|--------|
| 🔴 P0 | Experiment running with data quality issues | Pause experiment, diagnose immediately |
| 🟡 P1 | Funnel drop exceeds 2× historical baseline | Fast-track funnel-analysis, skip segmentation |
| 🟢 P2 | Routine growth loop iteration | Follow full Phase 0–5 sequence |

## Required Output Layout

```text
workspace/
├── report.md
├── figures/
├── results/
├── data/
└── logs/
    └── process-log.jsonl
```

## Verification Loop

Every execution follows: PLAN → EXECUTE → VERIFY → REPORT → LOG

1. **PLAN**: define objective, constraints, target outputs, candidate sub-skills.
2. **EXECUTE**: run selected pipeline, save intermediate artifacts.
3. **VERIFY**: check outputs against quality gates.
4. **REPORT**: write `report.md` in user's language.
5. **LOG**: finalize `logs/process-log.jsonl`.

## Quality Gates

- [ ] Sub-skill routing matches the user's actual request.
- [ ] Figures saved to `figures/` and referenced from `report.md`.
- [ ] Numeric outputs saved under `results/`.
- [ ] `report.md` includes timestamp, methods, results, discussion, file inventory.
- [ ] `logs/process-log.jsonl` records sub-skill usage, handoff I/O, files written.
- [ ] No essential result remains chat-only.

## Data Handling & Confidentiality

- User analytics data containing PII, revenue figures, or proprietary metrics is confidential.
- Use "[Segment A]", "[Metric X]" placeholders. Do not include real user identifiers.
- Do not store credentials or API keys in generated files.
- Mark draft growth plans as "DRAFT — NOT FOR DISTRIBUTION".
- Do not log raw user-level data; aggregate before saving.

## Cost Efficiency Rules

- Do not enable more than 10 MCP servers simultaneously.
- Default to `web_search` for quick lookups; use deep-research MCP only for comprehensive analysis.
- Prefer the narrowest sub-skill. Do not load broad context.

## Prohibited Operations

- Do not skip phases in the growth loop (Phase 0 → Phase 4 direct jump is forbidden).
- Do not skip approval checkpoints (⏸️).
- Do not launch experiments without a documented hypothesis and success criteria.
- Do not declare experiment winners without statistical significance (α ≤ 0.05).
- Do not include raw user-level data in final reports.

## Gotchas

- `co-growth-funnel-analysis` and `co-growth-user-segmentation` have overlapping triggers. If the user asks "why are users dropping off?" — use funnel-analysis. If "who are our best users?" — use user-segmentation.
- Phase outputs must be saved to files before proceeding. Session compaction will lose chat-only intermediate results.
- Copy variants without a defined experiment hypothesis produce untestable messaging. Always run experiment-design before copy-variants.
- `co-growth-learning-synthesis` requires experiment results data. If no experiment has been run, redirect to experiment-design first.
