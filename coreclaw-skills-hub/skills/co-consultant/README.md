# co-consultant

Harness-optimized consulting partner suite with 6 specialized sub-skills, 2 Custom Agents, and full Orchestrator routing.

- **Source path**: `co-consultant`
- **Version**: v0.1.0
- **Sub-skills**: 6
- **Custom Agents**: 2 (engagement-lead, quality-reviewer)

## Harness Optimization

Built on the [Harness 7-axis framework](https://qiita.com/hisaho/items/b3abdbf1df498c4244db):

| Axis | Implementation |
|------|---------------|
| Tool Coverage | WHEN/DO Orchestrator + 6 skills + 2 agents + MCP |
| Context Efficiency | Progressive Disclosure, <100 lines per skill |
| Quality Gates | MECE validation + pyramid structure checks in every skill |
| Memory Persistence | Gotchas sections + learning-capture skill |
| Eval Coverage | Validation loops with failure recovery |
| Security Guardrails | Source quality gates, hallucination prevention |
| Cost Efficiency | Description keyword separation, compact skills |

## Consulting Workflow (SHIKIGAMI Methodology)

```
Phase 0: Purpose Discovery  → co-consultant-purpose-discovery   ⏸️
Phase 1: Deep Research       → co-consultant-deep-research
Phase 2: Framework Analysis  → co-consultant-framework-analysis
Phase 3: Report Writing      → co-consultant-report-writing      ⏸️
Cross-cutting: Framework Library → co-consultant-framework-library
Cross-cutting: Learning Capture  → co-consultant-learning-capture
```

## Deploy Structure

```
<project>/.github/
├── AGENTS.md              ← co-consultant/AGENTS.md
├── copilot-instructions.md
├── agents/
│   ├── engagement-lead.md
│   └── quality-reviewer.md
└── skills/
    ├── co-consultant-purpose-discovery/SKILL.md
    ├── co-consultant-deep-research/SKILL.md
    ├── co-consultant-framework-analysis/SKILL.md
    ├── co-consultant-report-writing/SKILL.md
    ├── co-consultant-framework-library/SKILL.md
    └── co-consultant-learning-capture/SKILL.md
```

## Differences from `consultant`

| Aspect | consultant | co-consultant |
|--------|-----------|--------------|
| Custom Agents | None | 2 (engagement-lead, quality-reviewer) |
| Gotchas | None | 3+ items per skill |
| Validation loops | None | Full loops with failure recovery |
| Memory Persistence | None | learning-capture skill |
| MECE validation | In framework-analysis only | Integrated in quality gates |
| MCP integration | deep-research only | Configurable via .mcp.json |
| Language | Mixed JP/EN | English-first |
