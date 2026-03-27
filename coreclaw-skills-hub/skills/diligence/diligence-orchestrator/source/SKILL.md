---
name: diligence-orchestrator
description: Orchestrates due diligence from market scan to investment memo recommendation.
---

# diligence-orchestrator

## Overview
Orchestrates due diligence from market scan to investment memo recommendation.

## Orchestration Flow
1) diligence-market-scan -> 2) diligence-competitive-benchmark -> 3) diligence-financial-redflags -> 4) diligence-risk-matrix -> 5) diligence-investment-memo

## Input Contract
- Target company and investment thesis
- Market and competitor scope
- Data confidence constraints

## Output Contract
- Opportunity and risk synthesis
- Weighted risk matrix
- Investment memo with recommendation

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
