---
name: co-enterprise-kpi-diagnostics
description: |
  KPI gap analysis with root cause identification and leading indicator definition.
  Use when DIAGNOSING performance gaps, analyzing KPI trends, identifying root causes,
  or defining leading indicators for enterprise transformation tracking.
---

# KPI Diagnostics

KPI gap analysis with root causes and leading indicators.

## Use This Skill When

- Analyzing gaps between baseline and target KPIs.
- Identifying root causes of performance shortfalls.
- Defining leading indicators for early warning.

## Workflow

1. List KPIs with baseline, target, and current values.
2. Calculate gaps (absolute and %).
3. Root cause analysis (5 Whys or Fishbone) for significant gaps.
4. Define leading indicators that predict lagging KPI movement.
5. Save to files.

## Deliverables

- `results/kpi-diagnostics.md`: gap analysis with root causes.

## Quality Gates

- [ ] Each KPI has baseline, target, current, and gap.
- [ ] Root causes identified for gaps > threshold.
- [ ] Leading indicators defined for key lagging KPIs.
- [ ] Data sources documented.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 「目標未設定」のKPIが見つかった場合は、診断の前に目標設定を推奨すること
- Leading indicator は Lagging KPI の「先行シグナル」。相関だけでなく因果関係を検証すること
- KPI の定義（計算式、データソース、頻度）が部門間で異なる場合がある。定義を統一してから比較

## Validation Loop

1. KPI診断を生成
2. チェック: ベースライン/ターゲット/ギャップ、root cause、leading indicators
3. 不合格なら修正
4. 合格後のみ完了
