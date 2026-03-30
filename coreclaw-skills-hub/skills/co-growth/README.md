# co-growth

Harness-optimized product growth intelligence partner with 7 sub-skills, 2 Custom Agents, and full Orchestrator routing.

- **Source path**: `co-growth`
- **Version**: v0.1.0
- **Sub-skills**: 7
- **Custom Agents**: 2 (growth-lead, experiment-reviewer)

## Overview

Co-Growth provides structured growth loops for product teams: user segmentation → funnel analysis → experiment design → copy variants → learning synthesis. Every workflow follows the AARRR framework and enforces experiment rigor (α=0.05, β=0.20).

## Sub-Skills

| # | Skill | Focus |
|---|-------|-------|
| 1 | `co-growth-user-segmentation` | Behavioral/value/lifecycle segments, RFM, MECE validation, segment sizing |
| 2 | `co-growth-funnel-analysis` | AARRR stages, conversion bottleneck detection, segment-level drop-off, revenue impact |
| 3 | `co-growth-experiment-design` | Hypothesis-driven A/B, sample size calculation, MDE, guardrail metrics |
| 4 | `co-growth-copy-variants` | Variant messaging for experiment arms, variable isolation, segment-appropriate tone |
| 5 | `co-growth-learning-synthesis` | Scale/Iterate/Kill decisions, effect size review, next hypotheses generation |
| 6 | `co-growth-deep-research` | Web search + deep research MCP for growth benchmarks and competitive analysis |
| 7 | `co-growth-learning-capture` | Gotcha maintenance, learning persistence, CI validation |

## Growth Loop Diagram

```
Phase 0: User Segmentation       → co-growth-user-segmentation       ⏸️
Phase 1: Funnel Analysis          → co-growth-funnel-analysis          ⏸️
Phase 2: Experiment Design        → co-growth-experiment-design        ⏸️
Phase 3: Copy Variants            → co-growth-copy-variants
Phase 4: Learning Synthesis       → co-growth-learning-synthesis       ⏸️
Phase 5: Learning Capture         → co-growth-learning-capture
Cross-cutting: Deep Research      → co-growth-deep-research
```

## Harness Optimization

Built on the [Harness 7-axis framework](https://qiita.com/hisaho/items/b3abdbf1df498c4244db):

| Axis | Score | Implementation |
|------|-------|---------------|
| Tool Coverage | 3/3 | WHEN/DO Orchestrator + 7 skills + 2 agents |
| Context Efficiency | 3/3 | Progressive Disclosure, <60 lines per skill, conditional references |
| Quality Gates | 3/3 | Verification loop (PLAN→EXECUTE→VERIFY→REPORT→LOG) in every skill |
| Memory Persistence | 3/3 | Gotchas sections + learning-capture skill |
| Eval Coverage | 3/3 | Validation loops with failure recovery in every skill |
| Security Guardrails | 3/3 | Data handling rules, prohibited operations, PII protection |
| Cost Efficiency | 3/3 | Description keyword separation, compact skills, MCP limit |

## Directory Structure (Deploy)

```
<project-folder>/.github/
├── AGENTS.md              ← co-growth/AGENTS.md
├── copilot-instructions.md ← co-growth/copilot-instructions.md
├── agents/
│   ├── growth-lead.md
│   └── experiment-reviewer.md
└── skills/
    ├── co-growth-user-segmentation/SKILL.md
    ├── co-growth-funnel-analysis/SKILL.md
    ├── co-growth-experiment-design/SKILL.md
    ├── co-growth-copy-variants/SKILL.md
    ├── co-growth-learning-synthesis/SKILL.md
    ├── co-growth-deep-research/SKILL.md
    └── co-growth-learning-capture/SKILL.md
```

| Aspect | growth (legacy) | co-growth |
|--------|-----------------|-----------|
| Sub-skills | Domain-specific | 7 lifecycle-oriented |
| Orchestrator | Embedded in root SKILL.md | WHEN/DO routing with phase gates |
| Custom Agents | None | 2 (growth-lead, experiment-reviewer) |
| Gotchas | None | 3+ items per skill |
| Validation loops | Basic quality gates | Full loops with failure recovery |
| Memory Persistence | None | learning-capture skill |
| Description quality | Generic templates | Keyword-separated for routing precision |
