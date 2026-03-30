---
name: co-compliance-audit-response
description: |
  Drafts audit-ready responses with traceable control evidence references.
  Use when PREPARING audit response packages, drafting responses to auditor inquiries,
  assembling evidence packages, or creating audit-ready documentation.
---

# Audit Response

Draft audit-ready responses with traceable evidence references.

## Use This Skill When

- Preparing response packages for external/internal auditors.
- Drafting responses to specific auditor inquiries.
- Assembling evidence packages by control area.

## Workflow

1. Identify audit scope and specific inquiries.
2. Map each inquiry to relevant controls and evidence.
3. Draft response with: control description, evidence reference, compliance status.
4. Verify evidence completeness and currency (< 90 days).
5. Package into audit-ready format.
6. Save to files.

## Deliverables

- `results/audit-response.md`: audit-ready response package.
- Reuse `assets/audit-response-template.md` when producing standardized responses.

## Quality Gates

- [ ] Each response traces to specific control and evidence.
- [ ] Evidence is current (< 90 days for operational controls).
- [ ] Compliance status explicitly stated per inquiry.
- [ ] Document marked "DRAFT — CONFIDENTIAL".

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 監査人への回答は「はい/いいえ」ではなく、コントロール説明+証拠参照+コンプライアンス状態の3点セットで行う
- 証拠の適時性（< 90日）を監査人に提出する前に必ず確認すること。期限切れ証拠の提出は信頼性を損なう
- 「N/A」回答には必ず根拠文書を添付すること。根拠なしのN/Aは監査指摘事項になる

## Validation Loop

1. 監査回答を生成
2. チェック: トレーサビリティ、証拠適時性、ステータス明示、CONFIDENTIAL表記
3. 不合格なら修正
4. 合格後のみ完了
