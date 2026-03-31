---
name: co-learning-feedback-analyzer
description: |
  Analyzes learner performance patterns and generates improvement recommendations.
  Use when REVIEWING assessment results, identifying performance gaps,
  generating iteration triggers, or recommending design improvements.
---

# Feedback Analyzer

Analyzes learner feedback and performance data for iterative improvement.

## Use This Skill When

- Reviewing assessment results to identify performance patterns.
- Identifying gaps between intended and actual learning outcomes.
- Generating data-driven improvement recommendations.
- Deciding whether to iterate on objectives, activities, or rubrics.

## Workflow

1. Receive assessment data and rubric results (anonymized).
2. Identify performance patterns (common strengths/weaknesses).
3. Map gaps to specific objectives, activities, or rubric criteria.
4. Generate improvement recommendations with iteration triggers.
5. Save analysis to `results/feedback-analysis.md`.

## Deliverables

- `results/feedback-analysis.md`: patterns, gaps, and recommendations.
- `results/iteration-triggers.md`: specific conditions for redesign.

## Quality Gates

- [ ] All learner data anonymized ("[Learner A]" placeholders).
- [ ] Patterns supported by evidence (not anecdotal impressions).
- [ ] Recommendations map to specific design components (objectives/activities/rubrics).
- [ ] Iteration triggers include clear thresholds (e.g., "<60% proficiency → revise").

If any gate fails: re-anonymize data, add evidence, or specify thresholds.

## Gotchas

- 学習者データは必ず匿名化すること。"[Learner A]" プレースホルダーを使用し、実名を含めない
- 相関関係と因果関係を混同しないこと。「低スコアの学習者は出席率も低い」は因果ではない
- 改善提案は具体的な設計要素（目標・活動・ルーブリック）に紐づけること。「もっと頑張る」は提案ではない

## Validation Loop

1. Analyze anonymized performance data
2. Check: anonymized, evidence-based patterns, specific recommendations
3. If any check fails → re-anonymize or add evidence
4. Analysis ready for design iteration or final report
