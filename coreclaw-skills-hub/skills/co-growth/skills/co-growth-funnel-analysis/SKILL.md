---
name: co-growth-funnel-analysis
description: |
  Funnel analysis skill. AARRR-stage mapping, conversion bottleneck detection,
  segment-level drop-off analysis, and revenue impact quantification.
  Use when ANALYZING conversion funnels, diagnosing drop-off points,
  comparing segment performance, or estimating revenue impact of funnel improvements.
---

# Funnel Analysis

AARRR funnel analysis with bottleneck detection and revenue impact.

## Use This Skill When

- Analyzing conversion funnels across AARRR stages.
- Diagnosing where and why users drop off.
- Comparing funnel performance across segments.
- Estimating revenue impact of fixing a specific bottleneck.

## Workflow

1. Map user journey to AARRR stages (Acquisition → Referral).
2. Calculate stage-to-stage conversion rates.
3. Identify bottleneck: stage with largest absolute drop-off.
4. Break down drop-off by segment (from user-segmentation output).
5. Quantify revenue impact: (recovered users) × ARPU.
6. Save funnel data, charts, and impact estimates to files.

## Deliverables

- `report.md`: funnel narrative with bottleneck diagnosis.
- `results/funnel-metrics.csv`: stage, users, conversion rate, drop-off.
- `figures/funnel-chart.svg`: visual funnel with conversion rates.

## Quality Gates

- [ ] All 5 AARRR stages are mapped (or gaps explicitly noted).
- [ ] Conversion rates are calculated stage-to-stage, not end-to-end only.
- [ ] Bottleneck is identified with supporting data.
- [ ] Revenue impact estimate includes assumptions.
- [ ] Segment-level breakdown is included when segments exist.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- End-to-end conversion hides mid-funnel bottlenecks. Always compute stage-to-stage rates.
- Comparing funnels across time periods without controlling for seasonality produces misleading trends.
- "Activation" definition varies by product. Confirm the "aha moment" criteria with the user before analysis.

## Validation Loop

1. Generate funnel analysis with metrics
2. Check: all AARRR stages covered, stage-to-stage rates, bottleneck identified
3. If any check fails → revise analysis
4. User approval before prioritizing fixes ⏸️
