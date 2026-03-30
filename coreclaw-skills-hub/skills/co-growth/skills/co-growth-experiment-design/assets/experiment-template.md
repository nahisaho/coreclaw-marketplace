# Experiment Template

## Experiment: [Name]

| Field | Value |
|-------|-------|
| **Hypothesis** | If [change], then [metric] will [direction] by [MDE] |
| **Primary metric** | [metric name, current baseline] |
| **Secondary metrics** | [metric 1, metric 2] |
| **Guardrail metrics** | [metrics that must NOT degrade] |

## Sample Size Calculation

| Parameter | Value |
|-----------|-------|
| Baseline rate | [e.g., 12% conversion] |
| MDE | [e.g., +2pp absolute] |
| Significance level (α) | 0.05 |
| Power (1-β) | 0.80 |
| Required sample size (per arm) | [calculated n] |
| Estimated runtime | [days, accounting for seasonality] |

## Design Details

| Field | Value |
|-------|-------|
| Randomization unit | [user / session / device] |
| Allocation ratio | [50/50, 80/20, etc.] |
| Exclusion criteria | [who is excluded and why] |
| Traffic percentage | [% of eligible traffic] |

## Pre-Registration Checklist

- [ ] Hypothesis documented before launch.
- [ ] Sample size calculated and justified.
- [ ] Guardrail metrics defined before launch.
- [ ] Success criteria agreed with stakeholders.
- [ ] Experiment reviewed by experiment-reviewer agent.
