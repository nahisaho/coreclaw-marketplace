---
name: co-compliance-evidence-collector
description: |
  Defines evidence requirements, collection cadences, and readiness tracking.
  Use when PLANNING evidence collection, defining evidence sets per control,
  setting collection schedules, or assessing evidence readiness for audit.
---

# Evidence Collector

Define evidence requirements and collection cadences.

## Use This Skill When

- Defining what evidence is needed for each control.
- Setting collection cadences (daily/weekly/monthly/annual).
- Assessing evidence readiness before an audit.

## Workflow

1. For each control from mapping, define required evidence artifacts.
2. Set collection cadence and retention period.
3. Assess current evidence status (available/missing/expired).
4. Identify evidence gaps.
5. Save evidence inventory to files.

## Deliverables

- `results/evidence-inventory.md`: evidence sets per control.

## Quality Gates

- [ ] Evidence defined for every mapped control.
- [ ] Collection cadence specified for each evidence type.
- [ ] Evidence age assessed (current < 90 days, historical as specified).
- [ ] Missing evidence flagged for gap analysis.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 証拠の「適時性」は監査で最も指摘される項目。90日以上前のスクリーンショットは無効と判定されることが多い
- 自動生成される証拠（ログ、アクセスレビューレポート）と手動証拠を区別すること。自動化できるものは自動化を推奨
- 証拠の保存期間は規制ごとに異なる（GDPR: 処理期間中、SOX: 7年、HIPAA: 6年）

## Validation Loop

1. 証拠インベントリを生成
2. チェック: 全コントロールに証拠定義、頻度指定、適時性評価
3. 不合格なら修正
4. 合格後のみ完了
