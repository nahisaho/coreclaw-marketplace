---
name: enterprise-orchestrator
description: Orchestrates enterprise transformation from problem framing to executive decision output.
---

# enterprise-orchestrator

## Overview
Orchestrates enterprise transformation from problem framing to executive decision output.

## Orchestration Flow
1) enterprise-problem-structuring -> 2) enterprise-kpi-diagnostics -> 3) enterprise-initiative-prioritization -> 4) enterprise-roadmap-simulation -> 5) enterprise-exec-briefing

## Input Contract
- Strategic objective and business context
- Operating constraints (budget, timeline, ownership)
- Baseline KPIs and target outcomes

## Output Contract
- Prioritized initiative portfolio
- Dependency-aware roadmap
- Executive briefing with decisions, risks, and trade-offs

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.

---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run skill logic
VERIFY  → check outputs against quality gates
REPORT  → structured result for downstream skills
```

### Quality Gates

- [ ] Explicit assumptions and constraints documented
- [ ] Clear decisions and rationale
- [ ] Actionable next steps provided
