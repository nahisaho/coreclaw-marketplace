---
name: co-consultant-report-writing
description: |
  Pyramid-principle consulting report generation with quality validation.
  Template selection, executive summary, numerical/citation/content/format checks.
  Use when WRITING consulting reports, proposals, executive summaries,
  business cases, or client-ready deliverables from analysis results.
---

# Report Writing

Generate pyramid-principle consulting reports with multi-layer quality validation.

## Use This Skill When

- Writing a final consulting deliverable from analysis results.
- Creating an executive summary for decision-makers.
- Formatting findings into a client-ready report.

## Workflow

1. **Template selection** by objective keywords:

| Category | Templates |
|----------|----------|
| Approval/Decision | budget-approval, immediate-approval |
| Research/Analysis | market-analysis, tech-evaluation, risk-assessment, due-diligence |
| Strategy/Planning | business-case, strategic-proposal, gtm-strategy, dx-strategy |
| Comparison | comparative-analysis, ab-test |
| Project Mgmt | project-status, post-mortem, product-roadmap, qbr |
| Sales/Customer | sales-playbook, customer-success |

2. **Report structure** (Pyramid Principle):
   1. Executive Summary (conclusion first, top 3 findings, recommended actions)
   2. Research Overview (scope, methodology, source registry)
   3. Analysis Results (framework outputs, data, insights)
   4. Recommendations (short-term, mid/long-term, risks & mitigations)
   5. Appendix (detailed data, references)

3. **Quality checks** (4-layer validation):

### Layer 1: Numerical Consistency
- Same numbers match across sections.
- Calculations are verified.
- Units are consistent.

### Layer 2: Citation Completeness
- All data has source URLs.
- Links are valid format.
- Citations match source content.

### Layer 3: Content Coherence
- Executive summary matches body.
- MECE completeness verified.
- No logical leaps (So What / Why So).

### Layer 4: Format/Structure
- Required sections present.
- Heading hierarchy (H1→H2→H3).
- Tables properly formatted.

## Deliverables

- `report.md`: complete consulting report.
- `results/executive-summary.md`: standalone executive summary.
- Reuse local templates in `assets/` when they match the report type: market-analysis.md, strategic-proposal.md, business-case.md, due-diligence.md.

## Quality Gates

- [ ] Template matches the business objective.
- [ ] Executive summary conclusions supported by analysis body.
- [ ] All 4 quality check layers passed.
- [ ] Recommendations are concrete with owners and timeline.
- [ ] No unsourced data in the report.

If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- エグゼクティブサマリーは全セクション完成後に書くこと。先に書くと内容との乖離が生じる
- 「推奨アクション」は「〜すべき」だけでは不十分。担当者・期限・次のステップを具体的に記述すること
- Deep Research で確認できないデータをレポートに含めてはならない。推測は「分析に基づく推測」と明記
- 数値データは本文中で一貫していること。「市場規模100億」がサマリーで「90億」になっていたらリジェクト

## Validation Loop

1. レポートを生成
2. 4層品質チェック:
   - 数値整合性 → 不一致なら修正
   - 引用完全性 → ソースなしデータは削除または出典追加
   - 内容整合性 → サマリーと本文の乖離を修正
   - 形式構造 → セクション欠落を補完
3. 全チェック合格後、ユーザーに提示 ⏸️
4. ユーザー承認後のみ完了
