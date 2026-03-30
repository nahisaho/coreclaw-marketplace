---
name: co-compliance-gap-analysis
description: |
  Detects control and evidence gaps with severity ranking and remediation urgency.
  Use when ANALYZING compliance gaps, assessing control deficiencies,
  prioritizing remediation efforts, or preparing gap reports for management.
---

# Gap Analysis

Detect control/evidence gaps and rank remediation urgency.

## Use This Skill When

- Identifying missing or ineffective controls.
- Ranking compliance gaps by business impact.
- Preparing gap reports for management review.

## Workflow

1. Compare control mapping against evidence inventory.
2. Identify: missing controls, ineffective controls, missing evidence, expired evidence.
3. Classify severity: Critical / High / Medium / Low (based on business impact).
4. Calculate compliance coverage percentage.
5. Save gap report to files.

## Deliverables

- `results/gap-analysis.md`: gaps with severity and remediation urgency.
- Reuse `assets/gap-analysis-template.md` when producing standardized gap reports.

## Quality Gates

- [ ] All gaps classified by severity with business impact rationale.
- [ ] No gaps silently downgraded (rationale required for severity changes).
- [ ] Compliance coverage percentage calculated.
- [ ] Root cause identified for Non-Compliant findings.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 重大度は「技術的深刻度」ではなく「ビジネスインパクト」で判定すること。データ漏洩リスクのある Low-tech ギャップは Critical になりうる
- 「Partially Compliant」は最もグレーな判定。具体的に何が不足しているか明記すること
- ギャップの root cause を特定しないと、remediation が表面的な対処になる

## Validation Loop

1. ギャップ分析を生成
2. チェック: 重大度根拠、カバレッジ%、root cause、ダウングレード根拠
3. 不合格なら修正
4. ユーザー承認後のみ remediation に進む ⏸️
