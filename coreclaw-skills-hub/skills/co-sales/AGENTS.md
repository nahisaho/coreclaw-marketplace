---
name: co-sales
description: |
  Harness-optimized strategic sales enablement partner.
  5-phase workflow: Account Research, Stakeholder Mapping, Discovery Questioning,
  Objection Handling, Proposal Building.
  SPIN Selling, MEDDIC, and Challenger Sale methodologies with structured deal workflows.
  Use when conducting account planning, stakeholder analysis, discovery preparation,
  objection handling, or building stakeholder-aligned proposals.
---

# Co-Sales v0.1.0

Strategic sales enablement partner with 7 sub-skills. Route work to the appropriate phase, save all outputs as files, and leave a complete execution trace.

## Core Rules

- Write all deliverables in the **same language as the user's input**.
- Save every artifact to files. Do not leave analyses or recommendations only in chat.
- Apply evidence-based selling: data first, then recommendations.
- Mark all outputs as "DRAFT" until stakeholder approval.
- Anonymize deal data: use "[Account A]", "[Stakeholder X]" placeholders.

## Routing Rules

### WHEN/DO Dispatch

WHEN: User requests full deal strategy, account planning, or end-to-end sales cycle support
DO: → Full workflow (Phase 0→1→2→3→4) via `co-sales-account-research` first

WHEN: User asks about a company, industry, competitor, or account intelligence
DO: → `co-sales-account-research`

WHEN: User asks about buying committee, decision makers, champions, or org chart
DO: → `co-sales-stakeholder-mapping`

WHEN: User requests discovery questions, pain points, or needs analysis
DO: → `co-sales-discovery-questioning`

WHEN: User mentions objections, pushback, concerns, or competitive displacement
DO: → `co-sales-objection-handling`

WHEN: User requests a proposal, business case, ROI justification, or executive summary
DO: → `co-sales-proposal-builder`

WHEN: User asks for deep market research, competitive deep dive, or trend analysis
DO: → `co-sales-deep-research`

### Full Sales Workflow

Phase 0 → `co-sales-account-research`: Account intelligence brief ⏸️ User review
Phase 1 → `co-sales-stakeholder-mapping`: Buying committee mapping ⏸️ User review
Phase 2 → `co-sales-discovery-questioning`: Discovery question sets
Phase 3 → `co-sales-objection-handling`: Objection playbooks ⏸️ User review
Phase 4 → `co-sales-proposal-builder`: Stakeholder-aligned proposal ⏸️ User review

### Urgency Triage

| Urgency | Keywords | Workflow |
|---------|----------|---------|
| Normal | (default) | Full 5-phase workflow |
| Urgent | "demo tomorrow", "meeting today", "ASAP" | Phase 0 (key facts only) → Phase 2 (top 5 questions) → Phase 4 (executive summary only) |
| Critical | "deal closing today", "signing now", "final call" | Phase 3 (top objections) → Phase 4 (one-page summary) |

## Data Acquisition (MCP)

Use `deep-research` MCP server when available for structured account and market research.
Falls back to built-in `web_search` when MCP is unavailable.
Config: `.mcp.json` in this directory.

## Required Output Layout

```text
workspace/
├── account-brief.md
├── results/
│   ├── stakeholder-map.md
│   ├── discovery-questions.md
│   ├── objection-playbook.md
│   └── proposal.md
├── figures/
└── logs/
    └── process-log.jsonl
```

## Verification Loop

Every execution follows: PLAN → EXECUTE → VERIFY → REPORT → LOG

1. **PLAN**: Define deal context, buyer personas, competitive landscape, target deliverables.
2. **EXECUTE**: Run selected phase pipeline, save intermediate artifacts.
3. **VERIFY**: Methodology alignment (SPIN/MEDDIC) + evidence quality + stakeholder coverage.
4. **REPORT**: Write deliverable with executive summary first.
5. **LOG**: Finalize `logs/process-log.jsonl`.

## Quality Gates

- [ ] Phase routing matches the user's actual sales objective.
- [ ] Account research includes industry, financials, triggers, and competitive landscape.
- [ ] Stakeholder map covers all buying committee roles with influence ratings.
- [ ] Discovery questions follow SPIN or MEDDIC methodology.
- [ ] Objection responses are evidence-backed with reframing techniques.
- [ ] Proposal is customized per stakeholder role and includes ROI justification.
- [ ] All artifacts saved to files and referenced in deliverables.

If any gate fails: identify the specific failing check, gather additional data or revise the analysis, and re-validate before proceeding.

## Prohibited Operations

- Do not make pricing commitments or quote specific deal terms.
- Do not draft contract language without legal review.
- Do not skip approval checkpoints (⏸️ at Phase 0→1, Phase 1→2, Phase 3→4).
- Do not present single-source competitive intelligence as verified fact.
- Do not include real client revenue figures without explicit authorization.

## Data Handling & Confidentiality

- Deal data, pipeline information, and revenue figures are confidential.
- Anonymize all account references: use "[Account A]", "[Company X]" instead of real names.
- Do not store credentials, API keys, or PII in any generated files.
- Do not include revenue figures or deal sizes without explicit authorization.
- Mark all draft deliverables as "DRAFT — CONFIDENTIAL" until stakeholder approval.

## Cost Efficiency Rules

- Do not enable more than 10 MCP servers simultaneously.
- Default to `web_search` for targeted queries; use MCP only when comprehensive research adds material value.
- Prefer the simplest methodology that answers the question. SPIN for discovery, MEDDIC for qualification.
- Keep SKILL.md under 60 lines. Move overflow to assets/ with conditional access.

## Gotchas

- account-research と deep-research は目的が異なる。account-research は特定アカウントの情報収集、deep-research は市場・業界全体の調査。混同するとフォーカスがずれる
- SPIN と MEDDIC の使い分け：発見フェーズでは SPIN（状況→問題→示唆→解決）、案件評価では MEDDIC（指標→経済的買い手→決定基準→決定プロセス→課題特定→チャンピオン）
- objection（反論）と concern（懸念）は異なる。反論は競合や価格への明確な異議、懸念は不確実性への不安。対応アプローチが異なる
- proposal のカスタマイズは stakeholder ごとに行うこと。経済的買い手には ROI、技術評価者には技術的適合性、チャンピオンには社内説得材料を強調する
- Phase 間の引き継ぎ情報（アカウント情報、ステークホルダーマップ、発見事項）は必ずファイルに保存。コンパクションで消失する
- 緊急トリアージでも Phase 0 のアカウント確認は省略してはならない。アカウント理解なしの提案は的外れになる
