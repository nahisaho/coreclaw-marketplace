---
name: compliance-assistant
description: |
  Compliance and Audit Automation skill suite for coordinated multi-step workflows.
  Includes an orchestrator plus specialized sub-skills designed
  to produce higher-quality outcomes through structured chaining.
---

# Compliance and Audit Automation

This suite is a coordinated skill package under `compliance`.

## Package Structure

- Root skill: `compliance-assistant`
- Orchestrator skill: `compliance-orchestrator`
- Specialized sub-skills: domain-focused execution skills

## Orchestration Principle

The orchestrator routes tasks to specialized sub-skills in sequence,
checks intermediate quality gates, and consolidates outputs into a
final actionable result.

## Common Output Requirements

- Explicit assumptions and constraints
- Traceable reasoning between steps
- Final recommendation with next actions

---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run analysis / generation pipeline
VERIFY  → check outputs against quality gates
REPORT  → deliver structured artifacts with traceable reasoning
```

### Quality Gates

- [ ] All outputs include explicit assumptions and constraints
- [ ] Traceable reasoning between steps
- [ ] Final recommendation with clear next actions
- [ ] Artifacts saved as files (not chat-only output)
