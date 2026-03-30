---
name: co-growth-experiment-design
description: |
  Experiment design skill. Hypothesis-driven A/B test planning with sample size
  calculation, MDE definition, guardrail metrics, and runtime estimation.
  Use when DESIGNING A/B tests, calculating sample sizes, defining hypotheses,
  setting guardrail metrics, or planning experiment rollout.
---

# Experiment Design

Hypothesis-driven A/B test design with statistical rigor.

## Use This Skill When

- Designing a new A/B test or multivariate experiment.
- Formulating a testable hypothesis with success criteria.
- Calculating required sample size given MDE and baseline.
- Defining guardrail metrics that must not degrade.
- Estimating experiment runtime.

## Workflow

1. Formulate hypothesis: "If [change], then [metric] will [direction] by [MDE]."
2. Define metrics: primary, secondary, and guardrail.
3. Calculate sample size: inputs = baseline rate, MDE, α=0.05, β=0.20.
4. Estimate runtime: sample size ÷ daily traffic × seasonality buffer.
5. Document randomization unit, allocation ratio, and exclusion criteria.
6. Save experiment plan using template.

## Deliverables

- `report.md`: experiment rationale and design summary.
- `results/experiment-plan.md`: full plan using template.
- `results/sample-size-calc.md`: calculation with all inputs.

## Quality Gates

- [ ] Hypothesis is falsifiable with a clear primary metric.
- [ ] MDE is business-justified (not just "detectable").
- [ ] Sample size uses α=0.05, β=0.20 (or justified alternatives).
- [ ] At least one guardrail metric is defined.
- [ ] Runtime accounts for weekly seasonality (≥2 full weeks).

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- An MDE of "any improvement" is not valid. Require a minimum business-meaningful threshold (e.g., +2pp conversion).
- Experiments shorter than 2 weeks miss weekly seasonality cycles and produce biased estimates.
- Guardrail metrics added after launch are post-hoc and invalidate the pre-registered analysis plan.

## Validation Loop

1. Generate experiment design
2. Check: falsifiable hypothesis, sample size calc, guardrails, runtime ≥ 2 weeks
3. If any check fails → revise design
4. User approval before launch ⏸️
