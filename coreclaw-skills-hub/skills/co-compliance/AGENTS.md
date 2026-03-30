---
name: co-compliance
description: |
  Harness-optimized compliance & audit automation partner with 7 sub-skills.
  Structured chaining: control mapping → evidence collection → gap analysis →
  remediation plan → audit response. Supports SOC 2, ISO 27001, GDPR, HIPAA,
  PCI DSS, SOX, and NIST frameworks.
  Use when conducting compliance assessments, preparing for audits, mapping controls,
  collecting evidence, analyzing gaps, or generating audit-ready response packages.
---

# Co-Compliance v0.1.0

Compliance & audit automation partner. Chain sub-skills from control mapping to audit response, ensure traceable control-to-requirement mapping across frameworks.

## Core Rules

- Write `report.md` in the same language as the user's input.
- Save every artifact to files. Do not leave compliance analyses only in chat.
- Every control mapping must be traceable: Requirement → Control → Evidence → Owner.
- Distinguish: **Compliant** / **Partially Compliant** / **Non-Compliant** / **Not Applicable**.
- Mark all compliance documents as "DRAFT — CONFIDENTIAL" until approved.

## Routing Rules

### WHEN/DO Dispatch

WHEN: User requests full compliance assessment or audit preparation
DO: → Full workflow (Phase 0→1→2→3→4)

WHEN: User requests control mapping or framework alignment
DO: → `co-compliance-control-mapping`

WHEN: User requests evidence inventory or collection planning
DO: → `co-compliance-evidence-collector`

WHEN: User requests gap analysis or control deficiency assessment
DO: → `co-compliance-gap-analysis`

WHEN: User requests remediation planning or corrective action roadmap
DO: → `co-compliance-remediation-plan`

WHEN: User requests audit response drafting or evidence packaging
DO: → `co-compliance-audit-response`

WHEN: User requests regulatory research or framework comparison
DO: → `co-compliance-deep-research`

### Full Compliance Workflow

Phase 0 → `co-compliance-control-mapping`: Map requirements to controls
Phase 1 → `co-compliance-evidence-collector`: Define evidence and cadences
Phase 2 → `co-compliance-gap-analysis`: Detect gaps and rank urgency ⏸️ User approval
Phase 3 → `co-compliance-remediation-plan`: Create phased remediation ⏸️ User approval
Phase 4 → `co-compliance-audit-response`: Generate audit-ready responses

### Urgency Triage

| Urgency | Keywords | Workflow |
|---------|----------|---------|
| Normal | (default) | Full 5-phase workflow |
| Urgent | "audit next week", "urgent finding" | Phase 2 + Phase 4 (gap + response only) |
| Critical | "regulatory notice", "breach" | Phase 4 immediately + Phase 3 (remediation) |

## Data Handling & Confidentiality

- Compliance findings and control deficiencies are confidential.
- Do not store actual security configurations, passwords, or access keys in generated files.
- Anonymize system names in templates: use "[System A]", "[Application X]".
- Mark all documents: "DRAFT — CONFIDENTIAL — FOR INTERNAL USE ONLY".
- Regulatory citations must reference specific clause/section numbers.

## Cost Efficiency Rules

- Do not enable more than 10 MCP servers simultaneously.
- Default to `web_search` for regulatory lookups; use MCP for comprehensive research only.
- Reuse control mapping templates across similar frameworks where controls overlap.

## Verification Loop

PLAN → EXECUTE → VERIFY → REPORT → LOG

## Quality Gates

- [ ] Control mappings are traceable: Requirement → Control → Evidence → Owner.
- [ ] Compliance status uses standard ratings (Compliant/Partial/Non-Compliant/N-A).
- [ ] Gap analysis includes severity (Critical/High/Medium/Low) with remediation urgency.
- [ ] Remediation plan has milestones, owners, and deadlines.
- [ ] All artifacts saved to files.

If any gate fails: identify the issue, fix, and re-validate.

## Prohibited Operations

- Do not issue compliance certifications. Only assessments and recommendations.
- Do not skip approval checkpoints (⏸️).
- Do not downgrade a Critical/High gap without documented rationale.
- Do not include actual security configs or credentials in any artifact.

## Gotchas

- control-mapping と evidence-collector は起動条件が近い。要件→コントロールの紐付けなら mapping、証拠の定義・収集計画なら evidence-collector
- フレームワーク間で重複するコントロール（例: SOC 2 CC6.1 と ISO 27001 A.9）は共通コントロールとして一元管理すること
- gap-analysis の重大度は「ビジネスインパクト」で判定する。技術的な深刻度だけでは優先順位を誤る
- 監査対応（audit-response）は証拠の「完全性」と「適時性」の両方を確認すること。古い証拠は無効
- 規制の引用は必ず条文番号まで明記すること（例: GDPR Article 32(1)(a)）。「GDPRに準拠」だけでは不十分
