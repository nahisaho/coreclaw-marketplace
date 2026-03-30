---
name: co-consultant-mck-report-writing
description: |
  McKinsey-style consulting report generation with pyramid principle and quality validation.
  Executive summary, framework outputs, recommendations, and 4-layer quality checks.
  Use when WRITING MCK consulting reports, proposals, executive summaries,
  or client-ready deliverables from MCK framework analysis results.
---

# Report Writing (MCK)

Generate McKinsey-style pyramid-principle reports with quality validation.

## Use This Skill When

- Writing a MCK-style consulting deliverable.
- Creating an executive summary for decision-makers.
- Formatting MCK framework outputs into a client report.

## Workflow

1. Select report template (market-analysis, strategic-proposal, business-case, due-diligence).
2. Structure with pyramid principle (executive summary → analysis → recommendations).
3. Run 4-layer quality check (numerical, citation, content, format).
4. Present for user approval ⏸️.

## Deliverables

- `report.md`: complete MCK-style consulting report.
- `results/executive-summary.md`: standalone executive summary.
- Reuse templates in `assets/` when report type matches: market-analysis.md, strategic-proposal.md, business-case.md, due-diligence.md.

## Quality Gates

- [ ] Report follows MCK methodology and conventions.
- [ ] Executive summary conclusions supported by analysis body.
- [ ] All 4 quality check layers passed.
- [ ] Recommendations are concrete with owners and timeline.


If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- エグゼクティブサマリーは全セクション完成後に書くこと
- 推奨アクションは「〜すべき」だけでは不十分。担当者・期限・次のステップを具体的に記述
- MCKフレームワークの出力は必ずレポートに統合すること。フレームワーク結果だけの羅列は不可

## Validation Loop

1. レポートを生成
2. 4層品質チェック (数値/引用/内容/形式)
3. 全チェック合格後、ユーザーに提示 ⏸️
4. ユーザー承認後のみ完了
