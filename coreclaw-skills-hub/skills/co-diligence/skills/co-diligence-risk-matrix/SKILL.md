---
name: co-diligence-risk-matrix
description: |
  Weighted risk matrix with probability, impact, detectability, mitigation strategies, and owners.
  Use when ASSESSING investment risks, building risk matrices, prioritizing risk mitigations,
  or evaluating deal-breaker conditions for investment decisions.
---

# Risk Matrix

Weighted risk assessment with mitigation strategies.

## Use This Skill When

- Building a comprehensive risk matrix for an investment.
- Prioritizing risks by probability × impact.
- Identifying deal-breakers and mitigation strategies.

## Workflow

1. Aggregate risks from prior DD phases (market, competitive, financial).
2. Add additional risk categories (regulatory, technology, team, ESG).
3. Score each risk: Probability (1-5) × Impact (1-5) × Detectability (1-5 optional).
4. Classify: Critical (≥20) / High (15-19) / Medium (8-14) / Low (≤7).
5. Define mitigation strategy and owner for Critical/High risks.
6. Identify deal-breakers (Critical risks without viable mitigation).

## Deliverables

- `results/risk-matrix.md`: weighted risk matrix.
- Reuse `assets/risk-matrix-template.md` when producing standardized risk assessments.

## Quality Gates

- [ ] All risk categories covered (market, competitive, financial, regulatory, technology, team).
- [ ] Probability × Impact scored with rationale.
- [ ] Critical/High risks have mitigation + owner.
- [ ] Deal-breakers explicitly identified.
- [ ] Risks from prior phases (market-scan, financial-redflags) are incorporated.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- リスクを「低」にダウングレードする場合は根拠を明記すること。根拠なしのダウングレードは危険
- 「検出可能性」(Detectability)を加えると FMEA 的なアプローチになり精度が上がる（任意だが推奨）
- Deal-breaker の判定基準を事前に定義しておくこと。後から変えると意思決定がブレる

## Validation Loop

1. リスクマトリクスを生成
2. チェック: 全カテゴリカバー、スコア根拠、緩和策+オーナー、Deal-breaker特定
3. 不合格なら修正
4. ユーザー承認後のみ投資メモに進む ⏸️
