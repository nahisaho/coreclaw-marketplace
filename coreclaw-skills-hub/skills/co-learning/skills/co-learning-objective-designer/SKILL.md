---
name: co-learning-objective-designer
description: |
  Designs measurable learning objectives using Bloom's Taxonomy verbs and ABCD format.
  Use when DEFINING what learners should achieve, writing outcome statements,
  or creating competency targets for a course, module, or lesson.
---

# Objective Designer

Designs measurable learning objectives with Bloom's annotation and ABCD format.

## Use This Skill When

- Defining learning outcomes for a course, module, or lesson.
- Writing measurable objective statements with observable behaviors.
- Aligning objectives to Bloom's cognitive levels.
- Creating competency targets for accreditation or assessment.

## Workflow

1. Identify audience, context, and desired outcomes.
2. Select Bloom's cognitive level (Remember → Create).
3. Draft objectives in ABCD format (Audience/Behavior/Condition/Degree).
4. Validate measurability: can the behavior be observed and assessed?
5. Save objectives to `results/objectives.md` using asset template.

## Deliverables

- `results/objectives.md`: objectives in ABCD format with Bloom's annotation.
- `report.md`: summary with objective inventory and alignment notes.

## Quality Gates

- [ ] Each objective uses a Bloom's Taxonomy action verb.
- [ ] ABCD components (Audience/Behavior/Condition/Degree) are explicit.
- [ ] Objectives are measurable (observable, assessable behavior).
- [ ] No vague verbs ("understand", "know", "learn") without qualifiers.

If any gate fails: revise the objective, re-annotate Bloom's level, and re-validate.

## Gotchas

- "Understand" is not measurable. Replace with "explain", "compare", or "classify"
- ABCD の Degree（達成基準）を省略しがち。「80%の正答率で」等の基準を必ず含めること
- 1つの目標に複数の Bloom's レベルを混在させないこと。目標ごとに1つの認知レベルを指定する

## Validation Loop

1. Draft objectives in ABCD format
2. Check: Bloom's verb present, all ABCD components, measurable
3. If any check fails → revise verb or add missing component
4. Objectives ready for curriculum-builder input
