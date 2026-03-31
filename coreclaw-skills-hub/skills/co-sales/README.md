# co-sales

Harness-optimized strategic sales enablement partner suite with 7 specialized sub-skills, 2 Custom Agents, and full Orchestrator routing. Combines SPIN Selling, MEDDIC qualification, and Challenger Sale methodologies in structured deal workflows from account intelligence through proposal delivery.

- **Source path**: `co-sales`
- **Version**: v0.1.0
- **Sub-skills**: 7
- **Custom Agents**: 2 (deal-strategist, pipeline-reviewer)

## Sub-Skills

| # | Skill | Description |
|---|-------|-------------|
| 1 | `co-sales-account-research` | Company intel, financials, triggers, competitive landscape |
| 2 | `co-sales-stakeholder-mapping` | Buying committee, influence mapping, champion identification |
| 3 | `co-sales-discovery-questioning` | SPIN-based discovery question sets, persona-tailored |
| 4 | `co-sales-objection-handling` | Evidence-backed objection responses, reframing techniques |
| 5 | `co-sales-proposal-builder` | Stakeholder-aligned proposals with ROI justification |
| 6 | `co-sales-deep-research` | Market and competitive deep research via web_search and MCP |
| 7 | `co-sales-learning-capture` | Gotcha maintenance and deal learning persistence |

## Sales Workflow

```
Phase 0: Account Research       → co-sales-account-research        ⏸️
Phase 1: Stakeholder Mapping    → co-sales-stakeholder-mapping     ⏸️
Phase 2: Discovery Questioning  → co-sales-discovery-questioning
Phase 3: Objection Handling     → co-sales-objection-handling      ⏸️
Phase 4: Proposal Building      → co-sales-proposal-builder        ⏸️
Cross-cutting: Deep Research    → co-sales-deep-research
Cross-cutting: Learning Capture → co-sales-learning-capture
```

## Harness Optimization

Built on the [Harness 7-axis framework](https://qiita.com/hisaho/items/b3abdbf1df498c4244db):

| Axis | Score | Implementation |
|------|-------|---------------|
| Tool Coverage | 3/3 | WHEN/DO Orchestrator + 7 skills + 2 agents + MCP |
| Context Efficiency | 3/3 | Progressive Disclosure, ≤60 lines per skill |
| Quality Gates | 3/3 | SPIN/MEDDIC validation + evidence quality checks in every skill |
| Memory Persistence | 3/3 | Gotchas sections + learning-capture skill |
| Eval Coverage | 3/3 | Validation loops with failure recovery in every skill |
| Security Guardrails | 3/3 | Deal data confidentiality, no pricing commitments, DRAFT marking |
| Cost Efficiency | 3/3 | Description keyword separation, MCP 10-server limit, web_search default |

## Deploy Structure

```
<project>/.github/
├── AGENTS.md              ← co-sales/AGENTS.md
├── copilot-instructions.md
├── .mcp.json
├── agents/
│   ├── deal-strategist.md
│   └── pipeline-reviewer.md
└── skills/
    ├── co-sales-account-research/
    │   ├── SKILL.md
    │   └── assets/account-brief-template.md
    ├── co-sales-stakeholder-mapping/
    │   ├── SKILL.md
    │   └── assets/stakeholder-map-template.md
    ├── co-sales-discovery-questioning/SKILL.md
    ├── co-sales-objection-handling/SKILL.md
    ├── co-sales-proposal-builder/
    │   ├── SKILL.md
    │   └── assets/proposal-template.md
    ├── co-sales-deep-research/SKILL.md
    └── co-sales-learning-capture/SKILL.md
```

## Differences from `sales`

| Aspect | sales | co-sales |
|--------|-------|----------|
| Custom Agents | None | 2 (deal-strategist, pipeline-reviewer) |
| Gotchas | None | 3+ items per skill |
| Validation loops | None | Full loops with failure recovery |
| Memory Persistence | None | learning-capture skill |
| Sales Methodology | Basic workflow | SPIN + MEDDIC + Challenger Sale |
| MCP integration | None | Configurable via .mcp.json |
| Asset Templates | None | Account brief, stakeholder map, proposal |
| Urgency Triage | None | Normal / Urgent / Critical |
