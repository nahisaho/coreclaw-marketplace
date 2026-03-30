---
name: co-educationalist-lesson-planning
description: |
  Theory-grounded lesson planning with curriculum alignment and Constructive Alignment.
  Supports single-lesson, unit, and course design with differentiation strategies.
  Use when PLANNING lessons, designing units, creating teaching sequences,
  or aligning instruction with curriculum standards and learning objectives.
---

# Lesson Planning

Theory-grounded lesson and unit design with curriculum alignment.

## Use This Skill When

- Designing a single lesson, unit, or course sequence.
- Aligning instruction with curriculum standards.
- Applying Constructive Alignment (objectives ↔ activities ↔ assessment).

## Workflow

1. Confirm: grade, subject, topic, duration, learner context.
2. Look up curriculum standards via `data/curriculum.db` (for K-12).
3. Define learning objectives using Bloom's Taxonomy verbs.
4. Design teaching activities aligned with objectives.
5. Plan assessment aligned with objectives (Constructive Alignment).
6. Apply differentiation (UDL principles).
7. Cite grounding education theories.

## Deliverables

- `results/lesson-plan.md`: structured lesson plan with theory citations.
- Reuse `assets/lesson-plan-template.md` when creating standard lesson plans.

## Quality Gates

- [ ] Learning objectives use Bloom's verbs.
- [ ] Constructive Alignment verified (objectives ↔ activities ↔ assessment).
- [ ] Curriculum standard referenced (K-12).
- [ ] At least 1 education theory cited with application explanation.
- [ ] Differentiation strategies included.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 学習目標は「〜を理解する」ではなく「〜を説明できる」のように観察可能な動詞で書くこと
- Constructive Alignment は3要素（目標・活動・評価）全てが揃って初めて成立する。1つでも欠けると不整合
- 45分/50分の授業時間に収まるか確認すること。活動を詰め込みすぎると消化不良になる

## Validation Loop

1. レッスンプランを生成
2. チェック: Bloom's動詞、Constructive Alignment、カリキュラム参照、理論引用
3. 不合格なら修正
4. 合格後のみ完了
