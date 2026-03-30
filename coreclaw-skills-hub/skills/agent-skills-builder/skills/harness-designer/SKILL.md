---
name: harness-designer
description: |
  Define hook, audit, eval, and checkpoint assets for suite-style Agent Skills packages.
  Use when a generated suite needs lifecycle guardrails or evaluation scaffolds.
---

# Harness Designer

## Responsibilities

- Select `minimal`, `standard`, or `strict` harness posture.
- Define which hook scripts and command docs are required.
- Keep harness assets aligned with the orchestration topology.

## Profile Rules

| Profile | Use When | Expected Assets |
|---------|----------|-----------------|
| `minimal` | Low-control scaffold | Basic hooks and command docs |
| `standard` | Default suite build | Hooks, audit doc, eval and verify commands |
| `strict` | Strong guardrails required | Standard set plus config-protection hooks |