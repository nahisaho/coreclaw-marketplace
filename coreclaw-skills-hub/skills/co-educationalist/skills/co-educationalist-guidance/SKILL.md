---
name: co-educationalist-guidance
description: |
  Developmental stage-aware student guidance with Erikson, Kohlberg, and Piaget frameworks.
  Preventive, responsive, and crisis intervention plans with multi-tier support.
  Use when PLANNING student guidance, behavioral interventions, crisis responses,
  or counseling support grounded in developmental psychology.
---

# Student Guidance

Developmental stage-aware guidance with crisis escalation protocols.

## Use This Skill When

- Creating guidance plans for student behavioral issues.
- Planning preventive interventions (classroom-level).
- Responding to crisis situations (with mandatory escalation).

## ⚠️ Critical Safety Notice

> **AI output is reference information only. It does NOT replace professional judgment.**
>
> For crisis situations (self-harm, abuse, bullying, illegal activity, mental health),
> **immediately consult professionals** (school counselor, administration, medical, child services).

## Workflow

1. Assess situation: preventive / responsive / crisis.
2. If crisis → include mandatory escalation notice and stop.
3. Identify developmental stage (Erikson, Kohlberg, Piaget).
4. Design intervention aligned with developmental stage.
5. Plan multi-tier support (PBIS: Tier 1/2/3).
6. Document parent communication plan.
7. Mark as "CONFIDENTIAL — FOR EDUCATOR USE ONLY".

## Deliverables

- `results/guidance-plan.md`: structured guidance plan.

## Quality Gates

- [ ] Developmental stage explicitly identified (Erikson/Kohlberg/Piaget).
- [ ] Intervention aligns with developmental stage.
- [ ] Crisis situations include mandatory professional referral notice.
- [ ] Document marked CONFIDENTIAL.
- [ ] No student PII in generated files.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 危機対応では必ず「専門家への相談を推奨する」免責文を含めること。省略は許されない
- 発達段階の判定は年齢だけでなく個人差を考慮すること。同学年でも発達段階は異なる
- 保護者連携の文例では、批判的な表現を避け事実ベースで伝えること
- PBIS の Tier 3（個別集中支援）は専門家と連携して実施すること。教師単独での実施は不適切

## Validation Loop

1. 指導案を生成
2. チェック: 発達段階特定、介入整合性、危機時免責文、CONFIDENTIAL表記、PII排除
3. 不合格なら修正
4. 合格後のみ完了
