---
name: co-growth-copy-variants
description: |
  Copy variant generation skill. Creates messaging alternatives for experiment arms
  with variable isolation, segment-appropriate tone, and A/B-ready formatting.
  Use when GENERATING copy variants, writing CTA alternatives, creating messaging
  for experiment arms, or adapting tone for different user segments.
---

# Copy Variants

Variant messaging for experiment arms with controlled variable isolation.

## Use This Skill When

- Generating copy variants for A/B test arms.
- Writing CTA alternatives for landing pages or onboarding.
- Adapting messaging tone for different user segments.
- Ensuring only one variable changes between variants.

## Workflow

1. Confirm the experiment hypothesis and primary metric.
2. Identify the single variable to isolate (headline / CTA / value prop).
3. Generate control + treatment copy (minimum 2 variants).
4. Tag each variant with target segment and AARRR stage.
5. Validate variable isolation: only one element differs per pair.
6. Save variants to files.

## Deliverables

- `report.md`: variant rationale and isolation analysis.
- `results/copy-variants.md`: all variants with tags.

## Quality Gates

- [ ] Each variant pair differs by exactly one variable.
- [ ] Variants are tagged with target segment and AARRR stage.
- [ ] Tone matches the target segment's profile.
- [ ] An experiment hypothesis exists before variant creation.
- [ ] Variants are formatted for direct implementation.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- Changing both headline and CTA simultaneously violates variable isolation — test results become unattributable.
- "Professional tone" is not specific enough. Define tone with examples (e.g., "formal, no contractions, data-driven").
- Copy variants without a linked experiment hypothesis are untestable. Require experiment-design output first.

## Validation Loop

1. Generate copy variants
2. Check: single variable isolation, segment tags, linked hypothesis
3. If any check fails → revise variants
4. Proceed to experiment launch after approval
