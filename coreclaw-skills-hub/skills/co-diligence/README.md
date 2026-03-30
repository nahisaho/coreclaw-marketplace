# co-diligence

Harness-optimized investment & due diligence partner with 6 specialized sub-skills, 2 Custom Agents, and full Orchestrator routing.

- **Version**: v0.1.0
- **Sub-skills**: 6
- **Custom Agents**: 2 (deal-lead, diligence-reviewer)
- **Harness Score**: 21/21 (Expert)

## Overview

Co-Diligence is an AI-powered due diligence partner that guides investment teams through structured, evidence-based analysis — from initial market scan to final investment recommendation. Every conclusion traces back to source evidence with explicit confidence levels, ensuring defensible and auditable decision support.

## Sub-skills

| Skill | Purpose |
|-------|---------|
| `co-diligence-market-scan` | TAM/SAM/SOM sizing, demand signals, market trends. Builds the market landscape before target evaluation. |
| `co-diligence-competitive-benchmark` | Benchmarks the target against 3-5 direct and 2-3 adjacent competitors. Evaluates moats and positioning sustainability. |
| `co-diligence-financial-redflags` | Screens financials for red flags (margin decline, cash burn, off-balance-sheet items). Runs base/bull/bear scenario analysis. |
| `co-diligence-risk-matrix` | Aggregates risks from all prior phases. Scores Probability × Impact, identifies deal-breakers, assigns mitigation owners. |
| `co-diligence-investment-memo` | Synthesizes all DD findings into a Go / No-Go / Conditional Go recommendation with SMART conditions and next steps. |
| `co-diligence-learning-capture` | Records deal insights and methodology lessons. Updates Gotchas across the suite for continuous improvement. |

## Custom Agents

| Agent | Role | Access |
|-------|------|--------|
| `deal-lead` | Full-lifecycle DD orchestration. Routes tasks, manages phase gates, ensures evidence completeness. | All tools |
| `diligence-reviewer` | Read-only quality audit. Validates evidence chains, financial accuracy, risk completeness, and recommendation logic. | Read & search only |

## DD Workflow

```
Phase 0: Market Scan        → co-diligence-market-scan
Phase 1: Competitive Bench  → co-diligence-competitive-benchmark
Phase 2: Financial Red Flags → co-diligence-financial-redflags
Phase 3: Risk Matrix        → co-diligence-risk-matrix         ⏸️ Approval
Phase 4: Investment Memo    → co-diligence-investment-memo      ⏸️ Approval
```

Each phase saves outputs to `results/` for traceability. Phase 3 and 4 require user approval before proceeding.

## Key Features

### Evidence Chain
Every data point is labeled: **Fact** (verified, 2+ sources) / **Estimate** (calculated, methodology documented) / **Assumption** (unverified, flagged for validation). This ensures every recommendation is traceable from source to conclusion.

### Red Flag Sensitivity
Financial red flags require cross-validation with 2+ sources. Single-source findings are marked ⚠️ and flagged for further investigation, preventing false alarms from driving decisions.

### Risk Quantification
The risk matrix uses Probability × Impact scoring (optionally with Detectability for FMEA-style analysis). Risks are classified as Critical/High/Medium/Low with specific mitigation strategies and owners.

### Urgency Triage

| Mode | Use Case | Workflow |
|------|----------|---------|
| Normal | Full DD engagement | All 5 phases |
| Preliminary | Quick scan for initial screening | Phase 0 + Phase 4 |
| Go/No-Go | Immediate decision needed | Phase 4 only (summary) |

## Assets (Templates)

| Template | Used By | Purpose |
|----------|---------|---------|
| `market-scan-template.md` | market-scan | Standardized TAM/SAM/SOM and trends format |
| `risk-matrix-template.md` | risk-matrix | Severity classification and deal-breaker table |
| `investment-memo-template.md` | investment-memo | Executive summary, thesis, findings, recommendation |

## Harness 7-Axis Coverage

| # | Axis | Score | Implementation |
|---|------|:-----:|---------------|
| 1 | Tool Coverage | 3/3 | WHEN/DO routing + 6 skills + 2 agents + MCP |
| 2 | Context Efficiency | 3/3 | All SKILL.md <60 lines, 3 assets, conditional refs |
| 3 | Quality Gates | 3/3 | 6/6 skills with failure recovery procedures |
| 4 | Memory Persistence | 3/3 | 8 Gotchas files + learning-capture + compaction resilience |
| 5 | Eval Coverage | 3/3 | 6/6 Validation Loops + CI integration |
| 6 | Security Guardrails | 3/3 | MNPI rules, CONFIDENTIAL marking, read-only agent |
| 7 | Cost Efficiency | 3/3 | MCP limit, default tool preference |

## Deploy

```
<project>/.github/
├── AGENTS.md              ← co-diligence/AGENTS.md
├── copilot-instructions.md
├── agents/
│   ├── deal-lead.md
│   └── diligence-reviewer.md
└── skills/
    ├── co-diligence-market-scan/SKILL.md
    ├── co-diligence-competitive-benchmark/SKILL.md
    ├── co-diligence-financial-redflags/SKILL.md
    ├── co-diligence-risk-matrix/SKILL.md
    ├── co-diligence-investment-memo/SKILL.md
    └── co-diligence-learning-capture/SKILL.md
```
