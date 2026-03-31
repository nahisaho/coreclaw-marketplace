---
name: co-sales-discovery-questioning
description: |
  SPIN-based discovery question sets for sales meetings. Stage-appropriate,
  persona-tailored questions for pain discovery and needs analysis.
  Use when PREPARING discovery questions, planning sales calls,
  building persona-specific question sets, or structuring needs analysis.
---

# Discovery Questioning

Generate SPIN-based discovery question sets tailored to stakeholder personas.

## Use This Skill When

- Preparing for a discovery call or needs analysis meeting.
- Building stage-appropriate questions for different buying phases.
- Tailoring questions to specific stakeholder personas.
- Deepening pain discovery after initial conversations.

## Workflow

1. Review account brief and stakeholder map from prior phases.
2. Identify target persona(s) for the upcoming conversation.
3. Generate SPIN question sequence per persona:
   - **Situation** (2-3): Current state, processes, tools, metrics.
   - **Problem** (2-3): Difficulties, gaps, frustrations, inefficiencies.
   - **Implication** (2-3): Consequences, cascading effects, cost of inaction.
   - **Need-payoff** (2-3): Value of solving, desired outcomes, success vision.
4. Add follow-up questions for likely responses.
5. Tag questions by deal stage: Early / Mid / Late.
6. Save to `results/discovery-questions.md`.

## Deliverables

- `results/discovery-questions.md`: Persona-tagged SPIN question sets.

## Quality Gates

- [ ] SPIN sequence complete: all 4 categories present per persona.
- [ ] Questions tailored to stakeholder role (not generic).
- [ ] Implication questions link problems to quantifiable business impact.
- [ ] Follow-up questions prepared for top 3 likely responses.
- [ ] Questions tagged by deal stage (Early / Mid / Late).

If any gate fails: identify weak question categories, revise with deeper persona context, and re-validate.

## Gotchas

- SPIN の順序を守ること。Problem から始めると尋問になる。必ず Situation で文脈を作ってから
- Implication が最も重要。問題の「影響」を掘り下げないと、買い手は緊急性を感じない
- 質問は open-ended にすること。Yes/No で答えられる質問は発見の深さを損なう

## Validation Loop

1. SPIN 質問セットを生成
2. 4カテゴリ存在・Implication のビジネスインパクト・フォローアップ有無をチェック
3. 不合格なら修正、全基準を満たしてから完了
