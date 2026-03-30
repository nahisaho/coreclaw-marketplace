# co-compliance

Harness-optimized compliance & audit automation partner with 7 sub-skills, 2 Custom Agents, and full Orchestrator routing.

- **Version**: v0.1.0
- **Sub-skills**: 7
- **Custom Agents**: 2 (compliance-lead, audit-reviewer)
- **Harness Score**: 21/21 (Expert)

## Overview

Co-Compliance automates regulatory compliance workflows from control mapping through audit response. It supports multiple frameworks (SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS, SOX, NIST) with traceable control-to-requirement mapping, evidence collection planning, gap detection, and remediation roadmaps.

## Sub-skills

| Skill | Purpose |
|-------|---------|
| `co-compliance-control-mapping` | Maps regulations/frameworks to internal controls with ownership assignment |
| `co-compliance-evidence-collector` | Defines evidence requirements, collection cadences, and readiness status |
| `co-compliance-gap-analysis` | Detects control/evidence gaps and ranks remediation urgency |
| `co-compliance-remediation-plan` | Creates phased remediation plans with milestones and accountability |
| `co-compliance-audit-response` | Drafts audit-ready responses with traceable evidence references |
| `co-compliance-deep-research` | Regulatory research with web_search, /research, and MCP |
| `co-compliance-learning-capture` | Records compliance insights and methodology lessons |

## Compliance Workflow

```
Phase 0: Control Mapping     → co-compliance-control-mapping
Phase 1: Evidence Collection  → co-compliance-evidence-collector
Phase 2: Gap Analysis         → co-compliance-gap-analysis        ⏸️
Phase 3: Remediation Plan     → co-compliance-remediation-plan    ⏸️
Phase 4: Audit Response       → co-compliance-audit-response
```

## Supported Frameworks

SOC 2 Type II, ISO 27001, GDPR, HIPAA, PCI DSS, SOX (IT controls), NIST CSF, NIST 800-53

## Deploy

```
<project>/.github/
├── AGENTS.md
├── copilot-instructions.md
├── agents/
│   ├── compliance-lead.md
│   └── audit-reviewer.md
└── skills/
    └── co-compliance-*/SKILL.md
```

## Harness 7-Axis

| # | Axis | Score |
|---|------|:-----:|
| 1 | Tool Coverage | 3/3 |
| 2 | Context Efficiency | 3/3 |
| 3 | Quality Gates | 3/3 |
| 4 | Memory Persistence | 3/3 |
| 5 | Eval Coverage | 3/3 |
| 6 | Security Guardrails | 3/3 |
| 7 | Cost Efficiency | 3/3 |
