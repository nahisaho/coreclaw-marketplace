---
name: co-diligence-financial-redflags
description: |
  Financial health screening and red flag detection with scenario analysis.
  Use when SCREENING financial statements for red flags, analyzing profitability trends,
  evaluating cash flow health, or identifying scenario-sensitive assumptions in financials.
---

# Financial Red Flags

Financial health screening with red flag detection.

## Use This Skill When

- Screening financial statements for warning signs.
- Analyzing profitability, liquidity, and solvency trends.
- Identifying scenario-sensitive assumptions.

## Workflow

1. Analyze key financial metrics (revenue growth, margins, FCF, debt ratios).
2. Identify red flags (declining margins, cash burn, off-balance-sheet items, related-party transactions).
3. Cross-validate each red flag with 2+ sources.
4. Run scenario analysis (base/bull/bear) on key assumptions.
5. Document findings with severity ratings.

## Deliverables

- `results/financial-redflags.md`: red flag analysis with severity ratings.

## Quality Gates

- [ ] Key financial metrics calculated correctly (margins, ratios).
- [ ] Red flags cross-validated with 2+ sources.
- [ ] Single-source red flags marked ⚠️.
- [ ] Scenario analysis includes base/bull/bear cases.
- [ ] Currency and accounting standard (GAAP/IFRS) documented.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- GAAP と IFRS の違い（収益認識、リース会計等）に注意。比較時は基準を統一すること
- 「赤字=レッドフラグ」ではない。成長投資による計画的赤字とキャッシュフロー悪化は区別すること
- オフバランス項目（リース、変動持分事業体）を見落とさないこと。BS に載らないリスクがある

## Validation Loop

1. 財務分析を生成
2. チェック: 計算正確性、クロスバリデーション、シナリオ分析、会計基準明記
3. 不合格なら修正
4. 合格後のみ完了
