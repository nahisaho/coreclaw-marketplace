---
name: growth-orchestrator
description: Orchestrates product growth loops from segmentation to experiment learning synthesis.
---

# growth-orchestrator

## Overview
Orchestrates product growth loops from segmentation to experiment learning synthesis.

## Orchestration Flow
1) growth-user-segmentation -> 2) growth-funnel-analysis -> 3) growth-experiment-design -> 4) growth-copy-variants -> 5) growth-learning-synthesis

## Input Contract
- Product growth objective and target metrics
- Audience and lifecycle context
- Historical experiment constraints

## Output Contract
- Segment-level bottleneck diagnosis
- Experiment plan with variants
- Learning summary and next experiment backlog

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.
