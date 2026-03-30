---
name: co-growth-user-segmentation
description: |
  User segmentation skill. Behavioral, value-based, and lifecycle segmentation
  with RFM analysis, MECE validation, and segment sizing.
  Use when DEFINING user segments, creating cohorts, building personas,
  running RFM analysis, or validating segment coverage.
---

# User Segmentation

Behavioral, value-based, and lifecycle user segmentation.

## Use This Skill When

- Defining target user segments for growth initiatives.
- Building behavioral or value-based cohorts.
- Running RFM (Recency, Frequency, Monetary) analysis.
- Validating that segments are MECE.
- Sizing segments for experiment feasibility.

## Workflow

1. Clarify segmentation objective and available data dimensions.
2. Select segmentation approach (behavioral / value / lifecycle / RFM).
3. Define segment boundaries and criteria.
4. Validate MECE: every user belongs to exactly one segment.
5. Size each segment (count, % of total, revenue share).
6. Save segment definitions and sizing to files.

## Deliverables

- `report.md`: segmentation rationale and summary.
- `results/segments.md`: segment definitions using template.
- `results/segment-sizing.csv`: counts, percentages, revenue share.

## Quality Gates

- [ ] Segments are MECE (Mutually Exclusive, Collectively Exhaustive).
- [ ] Each segment has ≥5% of total users (actionable size).
- [ ] RFM scoring uses consistent thresholds across dimensions.
- [ ] Segment definitions are concrete and reproducible.
- [ ] Sizing data is saved to `results/`.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- Segments below 5% of the user base are rarely actionable for experiments — flag and consider merging.
- RFM quintile boundaries should be recalculated quarterly; stale thresholds misclassify users.
- "Power users" is not a valid segment without concrete behavioral criteria (e.g., ≥10 sessions/week).

## Validation Loop

1. Generate segment definitions
2. Check: MECE compliance, minimum size (≥5%), reproducible criteria
3. If any check fails → revise boundaries
4. User approval before finalizing ⏸️
