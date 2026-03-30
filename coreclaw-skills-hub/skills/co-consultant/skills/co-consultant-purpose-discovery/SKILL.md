---
name: co-consultant-purpose-discovery
description: |
  True objective discovery through structured dialogue. 5 Whys analysis,
  JTBD (Jobs To Be Done), and 6-element structured prompting.
  Use when STARTING a consulting engagement, clarifying ambiguous business questions,
  defining the true objective behind a request, or scoping a research project.
---

# Purpose Discovery

Discover the user's true objective through structured one-question-at-a-time dialogue.

## Use This Skill When

- Starting a new consulting engagement or research project.
- The request is ambiguous or surface-level.
- Defining scope, constraints, and success criteria.

## Workflow

1. Decompose the request into 6 elements and present for approval ⏸️:

| Element | Description |
|---------|-------------|
| PURPOSE | What decision or judgment to make |
| TARGET | What/who to investigate |
| SCOPE | Depth and breadth boundaries |
| TIMELINE | Timeframe and deadlines |
| CONSTRAINTS | Budget, access, regulatory limits |
| DELIVERABLES | Expected outputs and success criteria |

2. One-question-at-a-time dialogue (minimum 3 rounds):
   - WHY: "Why is this investigation needed?"
   - WHO: "Who will use the results?"
   - WHAT-IF: "What action follows ideal results?"
   - CONSTRAINT: "What limits exist on time/budget/scope?"
   - SUCCESS: "What defines success?"

3. 5 Whys analysis for abstract answers (drill to root cause).

4. JTBD analysis (3 jobs):
   - Functional: What concrete task to accomplish
   - Emotional: What feeling to achieve/avoid
   - Social: How to be perceived by others

5. Define true objective and get user approval ⏸️.

6. Generate research plan with search queries (bilingual JP/EN).

## Deliverables

- `results/purpose-definition.md`: 6-element breakdown + true objective.
- `results/research-plan.md`: search queries, recommended frameworks, scope.

## Quality Gates

- [ ] All 6 elements are addressed.
- [ ] Minimum 3 dialogue rounds completed.
- [ ] True objective is specific, actionable, and user-approved.
- [ ] Research plan includes bilingual search queries.

If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- 複数の質問を一度に投げてはならない。必ず1問1答形式で進める。情報過多は回答精度を下げる
- 5 Whys で5回掘り下げる必要がないケースもある。根本原因に到達したら停止する
- ユーザーの最初の依頼が「真の目的」であることは稀。表層的な依頼の裏にある本質を探ること
- 構造化プロンプトの承認なしに次のステップに進んではならない
- 対話ラウンドは最低3ラウンド。3ラウンド未満で「十分」と判断してはならない
- 構造化プロンプトの6要素に空欄がある場合は追加ヒアリングで埋めること

## Validation Loop

1. 6要素分解と真の目的を生成
2. チェック:
   - PURPOSE が意思決定に直結する形で記述されているか
   - SCOPE が検証可能な範囲に絞られているか
   - 真の目的が具体的かつ実行可能か
3. 不合格なら対話を追加して修正
4. ユーザー承認後のみ完了
