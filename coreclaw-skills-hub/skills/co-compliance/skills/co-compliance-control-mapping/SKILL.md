---
name: co-compliance-control-mapping
description: |
  Maps regulatory requirements to internal controls with ownership assignment.
  Supports SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS, SOX, NIST frameworks.
  Use when MAPPING regulations to controls, assigning control ownership,
  or building a control-to-requirement traceability matrix.
---

# Control Mapping

Map regulatory requirements to internal controls with ownership.

## Use This Skill When

- Mapping a new framework's requirements to existing controls.
- Building a control-to-requirement traceability matrix.
- Assigning control ownership.

## Workflow

1. Identify applicable framework and scope.
2. List all requirements (use `web_search` for current framework versions).
3. Map each requirement to internal controls.
4. Assign owner for each control.
5. Identify shared controls across multiple frameworks.
6. Save mapping to files.

## Deliverables

- `results/control-mapping.md`: requirement-to-control matrix.
- Reuse `assets/control-mapping-template.md` when producing standardized mappings.

## Quality Gates

- [ ] Every requirement maps to ≥1 control.
- [ ] Every control has an assigned owner.
- [ ] Shared controls identified with cross-framework references.
- [ ] Framework version and date documented.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- フレームワークのバージョンを必ず明記（例: ISO 27001:2022 vs 2013）。バージョン違いでコントロール番号が変わる
- 1つのコントロールで複数要件をカバーする「共通コントロール」を特定すると、効率が大幅に向上する
- コントロールオーナーは「チーム」ではなく「個人名+役職」で指定すること。曖昧なオーナーシップは監査で問題になる

## Validation Loop

1. マッピングを生成
2. チェック: 全要件にコントロール紐付け、オーナー指定、共通コントロール特定
3. 不合格なら修正
4. 合格後のみ完了
