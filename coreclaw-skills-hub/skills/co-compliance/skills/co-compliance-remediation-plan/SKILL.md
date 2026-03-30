---
name: co-compliance-remediation-plan
description: |
  Creates phased remediation plans with milestones, accountability, and tracking.
  Use when PLANNING corrective actions for compliance gaps, creating remediation roadmaps,
  assigning remediation owners, or building milestone-based compliance improvement plans.
---

# Remediation Plan

Phased remediation with milestones and accountability.

## Use This Skill When

- Creating corrective action plans for identified gaps.
- Building phased remediation roadmaps.
- Assigning remediation owners and deadlines.

## Workflow

1. Prioritize gaps from gap analysis (Critical → High → Medium → Low).
2. Define remediation actions for each gap.
3. Assign owner and deadline per action.
4. Create phased roadmap (Immediate / 30-day / 90-day / Next audit cycle).
5. Define success criteria for each remediation.
6. Save plan to files.

## Deliverables

- `results/remediation-plan.md`: phased plan with milestones.

## Quality Gates

- [ ] Critical/High gaps addressed in first remediation phase.
- [ ] Each action has owner + deadline + success criteria.
- [ ] Milestones are realistic and sequenced.
- [ ] Budget/resource requirements estimated.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- Critical ギャップの remediation 期限を「次回監査まで」にしてはならない。Immediate（即時）または30日以内を指定
- 成功基準は「実装した」ではなく「証拠が収集可能な状態」まで含めること
- remediation オーナーが退職・異動した場合の引き継ぎ手順も定義しておくこと

## Validation Loop

1. 是正計画を生成
2. チェック: 優先順位、オーナー+期限+成功基準、フェーズ妥当性
3. 不合格なら修正
4. ユーザー承認後のみ完了 ⏸️
