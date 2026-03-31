---
name: co-learning-curriculum-builder
description: |
  Builds sequenced curriculum structures with scaffolding, prerequisite mapping, and pacing.
  Use when STRUCTURING content sequence, creating scope & sequence documents,
  mapping prerequisites, or designing pacing guides for a course or program.
---

# Curriculum Builder

Builds sequenced curriculum with scaffolding, prerequisites, and pacing guides.

## Use This Skill When

- Creating scope & sequence for a course or program.
- Mapping prerequisite dependencies between topics.
- Designing pacing guides with time allocations.
- Structuring content scaffolding from simple to complex.

## Workflow

1. Receive finalized objectives from objective-designer.
2. Map prerequisite dependencies between objectives.
3. Sequence topics using scaffolding (simple → complex).
4. Allocate time and create pacing guide.
5. Save curriculum to `results/curriculum.md`.

## Deliverables

- `results/curriculum.md`: scope & sequence with prerequisite map.
- `results/pacing-guide.md`: time allocations per module/unit.

## Quality Gates

- [ ] Prerequisites mapped with no circular dependencies.
- [ ] Scaffolding progresses from foundational to advanced.
- [ ] Pacing is realistic for target audience and delivery mode.
- [ ] Every objective from Phase 0 is addressed in the sequence.

If any gate fails: re-map prerequisites, adjust pacing, and re-validate.

## Gotchas

- 前提条件の循環依存は検出しにくい。依存グラフを明示的に描いて確認すること
- Scaffolding は「簡単→難しい」だけでなく「具体→抽象」の軸も考慮すること
- ペーシングは理想的な学習時間ではなく、実際の授業時間（休憩・質疑含む）で計算すること

## Validation Loop

1. Map prerequisites and create sequence
2. Check: no circular deps, scaffolding progression, pacing realistic
3. If any check fails → restructure sequence or adjust time
4. Curriculum ready for activity-generator input
