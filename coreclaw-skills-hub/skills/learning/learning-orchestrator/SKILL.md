---
name: learning-orchestrator
description: Orchestrates learning design from measurable objectives to feedback-driven iteration.
---

# learning-orchestrator

## Overview
Orchestrates learning design from measurable objectives to feedback-driven iteration.

## Orchestration Flow
1) learning-objective-designer -> 2) learning-curriculum-builder -> 3) learning-activity-generator -> 4) learning-rubric-designer -> 5) learning-feedback-analyzer

## Input Contract
- Learner profile and target outcomes
- Delivery mode and constraints
- Assessment requirements

## Output Contract
- Outcome-aligned curriculum and activities
- Rubrics and evaluation plan
- Improvement recommendations from feedback

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.
