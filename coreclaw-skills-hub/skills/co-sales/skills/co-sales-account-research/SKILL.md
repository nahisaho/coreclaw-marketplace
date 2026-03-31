---
name: co-sales-account-research
description: |
  Account intelligence and company research for strategic sales planning.
  Company overview, financial health, industry trends, recent news, competitive landscape,
  and business triggers. Use when STARTING account planning, preparing for a first meeting,
  researching a target company, or updating account intelligence.
---

# Account Research

Build comprehensive account intelligence briefs for strategic sales planning.

## Use This Skill When

- Starting account planning for a new or existing opportunity.
- Preparing for a first meeting or executive briefing.
- Updating account intelligence before a major deal milestone.
- Researching competitive landscape for a specific account.

## Workflow

1. Gather company overview: industry, size, headquarters, key products/services.
2. Assess financial health: revenue trends, profitability, recent earnings (public companies).
3. Identify business triggers: leadership changes, M&A, strategic initiatives, funding rounds.
4. Map competitive landscape: current vendors, competitive threats, differentiation opportunities.
5. Analyze industry trends: market dynamics, regulatory changes, technology shifts.
6. Compile risk factors: financial risks, organizational changes, competitive threats.
7. Save output using `assets/account-brief-template.md`.

## Deliverables

- `account-brief.md`: Comprehensive account intelligence brief.

## Quality Gates

- [ ] Company overview covers industry, size, products, and recent developments.
- [ ] Financial indicators present for public companies (or noted as private).
- [ ] At least 3 business triggers or strategic initiatives identified.
- [ ] Competitive landscape includes current vendors and differentiation points.
- [ ] All data sourced and dated (no unattributed claims).

If any gate fails: identify the gap, conduct targeted research to fill it, and re-validate.

## Gotchas

- 公開企業と非公開企業で収集可能な財務データが異なる。非公開企業は推定値を「推定」と明記すること
- アカウント情報の鮮度が重要。6ヶ月以上前の情報は「要更新」フラグを付けること
- account-research は特定企業の情報収集。市場全体の調査は deep-research を使うこと

## Validation Loop

1. アカウントブリーフを生成
2. チェック:
   - 企業概要が業界・規模・製品を網羅しているか
   - ビジネストリガーが3件以上特定されているか
   - 競合情報に差別化ポイントが含まれているか
3. 不合格なら追加調査を実行
4. 全基準を満たしてから完了
