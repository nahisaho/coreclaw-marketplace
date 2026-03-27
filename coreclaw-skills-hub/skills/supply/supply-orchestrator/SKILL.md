---
name: supply-orchestrator
description: Orchestrates supply chain decisions from forecasting through scenario planning.
---

# supply-orchestrator

## Overview
Orchestrates supply chain decisions from forecasting through scenario planning.

## Orchestration Flow
1) supply-demand-forecast -> 2) supply-inventory-optimizer -> 3) supply-supplier-risk -> 4) supply-logistics-simulation -> 5) supply-scenario-planner

## Input Contract
- Demand horizon and service targets
- Cost, capacity, and lead-time constraints
- Supplier and logistics context

## Output Contract
- Forecast-backed inventory strategy
- Risk-aware logistics scenarios
- Actionable supply chain decision plan

## Quality Gates
- Upstream outputs are complete and parseable before moving to next skill.
- Each step must include assumptions and confidence levels.
- Final response must include recommended next actions.

## Fallback Policy
- If a sub-skill output is insufficient, request clarification and rerun that step.
- If constraints conflict, present at least two viable alternatives.
