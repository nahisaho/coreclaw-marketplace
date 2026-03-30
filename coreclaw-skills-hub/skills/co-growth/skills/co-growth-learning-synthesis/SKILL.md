---
name: co-growth-learning-synthesis
description: |
  Learning synthesis skill. Experiment result interpretation with Scale/Iterate/Kill
  decision framework, effect size review, and next hypothesis generation.
  Use when INTERPRETING experiment results, deciding to scale or kill a test,
  reviewing effect sizes, or generating next-iteration hypotheses.
---

# Learning Synthesis

Experiment result interpretation and Scale/Iterate/Kill decisions.

## Use This Skill When

- Interpreting completed experiment results.
- Deciding whether to Scale, Iterate, or Kill an experiment.
- Reviewing effect sizes and confidence intervals.
- Generating next-iteration hypotheses from learnings.

## Workflow

1. Load experiment results (primary, secondary, guardrail metrics).
2. Check statistical significance (α ≤ 0.05) and practical significance.
3. Review effect size and confidence interval width.
4. Check guardrail metrics for degradation.
5. Apply decision framework:
   - **Scale**: significant lift, no guardrail violations → ship to 100%.
   - **Iterate**: directional signal but CI crosses zero → refine hypothesis.
   - **Kill**: no signal or guardrail violation → stop and document.
6. Generate next hypotheses based on learnings.
7. Save decision and rationale to files.

## Deliverables

- `report.md`: result summary, decision, and next steps.
- `results/experiment-results.md`: metrics, CIs, decision rationale.

## Quality Gates

- [ ] Statistical significance checked with correct α threshold.
- [ ] Effect size and 95% CI are reported (not just p-value).
- [ ] Guardrail metrics reviewed for degradation.
- [ ] Decision uses Scale/Iterate/Kill framework explicitly.
- [ ] At least one next hypothesis is generated.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- A p-value of 0.049 with a wide CI is not a strong signal. Always report CI width alongside significance.
- "Iterate" is not "re-run the same test." Each iteration must change at least one variable.
- Novelty effects inflate early results. If runtime was <2 weeks, flag potential novelty bias.

## Validation Loop

1. Generate synthesis and decision
2. Check: significance, effect size + CI, guardrails, Scale/Iterate/Kill applied
3. If any check fails → revise analysis
4. User approval before shipping or killing ⏸️
