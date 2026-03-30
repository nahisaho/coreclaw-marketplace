---
name: co-diligence-market-scan
description: |
  Market landscape analysis with TAM/SAM/SOM sizing, demand signals, and trend identification.
  Use when SCANNING market conditions, sizing addressable markets,
  identifying demand trends, or building market landscape summaries for due diligence.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Market Scan

Market landscape analysis with TAM/SAM/SOM and trend signals.

## Use This Skill When

- Sizing TAM/SAM/SOM for a target market.
- Identifying demand trends and growth drivers.
- Building market landscape summaries.

## Workflow

1. Define market boundaries (geography, segment, time period).
2. Size TAM (top-down from industry reports) and SAM/SOM (bottom-up from target capability).
3. Identify key trends (macro, technology, regulatory, consumer).
4. Document sources with trust levels.
5. Save to files.

## Deliverables

- `results/market-scan.md`: market landscape with TAM/SAM/SOM.
- Reuse `assets/market-scan-template.md` when producing standardized market analyses.

## Quality Gates

- [ ] TAM/SAM/SOM documented with sources and methodology (top-down/bottom-up).
- [ ] Key trends identified with supporting evidence.
- [ ] All data labeled: Fact / Estimate / Assumption.
- [ ] Confidence levels on estimates.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- TAM と SAM を混同しないこと。TAM=全市場、SAM=自社がアクセス可能な市場
- 市場規模の推定方法（Top-down vs Bottom-up）を必ず明記すること。方法が異なると数値が大きく変わる
- 成長率(CAGR)は期間を明示すること。「高成長」だけでは判断材料にならない

## Validation Loop

1. マーケットスキャンを生成
2. チェック: TAM/SAM/SOM出典、トレンド根拠、Fact/Estimate/Assumptionラベル
3. 不合格なら修正
4. 合格後のみ完了
