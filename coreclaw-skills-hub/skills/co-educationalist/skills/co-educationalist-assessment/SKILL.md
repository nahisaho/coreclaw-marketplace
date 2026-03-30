---
name: co-educationalist-assessment
description: |
  Assessment design with Bloom's Taxonomy annotation and Constructive Alignment.
  Rubrics, tests, formative assessment tools with cognitive level distribution.
  Use when DESIGNING tests, rubrics, quizzes, formative assessments,
  or evaluation criteria aligned with learning objectives and Bloom's levels.
---

# Assessment Design

Bloom's-annotated assessment with Constructive Alignment verification.

## Use This Skill When

- Designing rubrics for performance or portfolio assessment.
- Creating test items with Bloom's level annotation.
- Building formative assessment tools (exit tickets, checklists).

## Workflow

1. Confirm: learning objectives, assessment type (rubric/test/formative), grade, subject.
2. Look up curriculum standards via `data/curriculum.db` (for K-12).
3. Design items with Bloom's level annotation on each.
4. Verify Constructive Alignment (objectives ↔ assessment).
5. Create scoring guide/rubric.
6. Cite grounding theory (Bloom's, Constructive Alignment, Formative Assessment).

## Deliverables

- `results/assessment.md`: assessment tool with Bloom's annotations.
- Reuse `assets/rubric-template.md` when creating rubric assessments.
- Reuse `assets/test-template.md` when creating test assessments.

## Quality Gates

- [ ] Every item annotated with Bloom's level.
- [ ] Cognitive level distribution documented.
- [ ] Constructive Alignment verified.
- [ ] Scoring criteria are explicit and sharable with students.
- [ ] Curriculum standard referenced (K-12).

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 「記憶」レベルの問題ばかりにならないよう、認知レベルの分布を意識すること
- ルーブリックの基準は「生徒にも共有可能」なレベルの明確さが必要。教師だけが分かる基準は不適切
- 形成的評価は「成績をつけるため」ではなく「指導改善のため」に使うこと

## Validation Loop

1. 評価ツールを生成
2. チェック: Bloom's注釈、分布バランス、Constructive Alignment、カリキュラム参照
3. 不合格なら修正
4. 合格後のみ完了
