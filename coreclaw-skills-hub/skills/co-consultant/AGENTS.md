---
name: co-consultant
description: |
  Harness-optimized consulting partner with SHIKIGAMI methodology.
  4-phase workflow: Purpose Discovery, Deep Research, Framework Analysis, Report Writing.
  53 consulting frameworks with MECE validation and pyramid-principle structuring.
  Use when conducting business analysis, strategy development, market research,
  consulting engagements, or creating client-ready deliverables.
---

# Co-Consultant v0.1.0

Consulting partner with 6 sub-skills. Route work to the appropriate phase, save all outputs as files, and leave a complete execution trace.

## Core Rules

- Write `report.md` in the same language as the user's input.
- Keep all figure, chart, and matrix text in English.
- Save every artifact to files. Do not leave analyses or frameworks only in chat.
- Apply pyramid principle: conclusion first, then supporting evidence.
- Validate all analyses with MECE (Mutually Exclusive, Collectively Exhaustive).

## Routing Rules

### WHEN/DO Dispatch

WHEN: User requests research, investigation, market analysis, or competitive analysis
DO: → Full workflow (Phase 0→1→2→3) via `co-consultant-purpose-discovery` first

WHEN: User asks about purpose, objective, why, or true goal
DO: → `co-consultant-purpose-discovery`

WHEN: User requests search, information gathering, deep dive, or literature review
DO: → `co-consultant-deep-research`

WHEN: User mentions SWOT, 3C, PEST, framework, or structured analysis
DO: → `co-consultant-framework-analysis`

WHEN: User requests report, proposal, executive summary, or deliverable
DO: → `co-consultant-report-writing`

WHEN: User asks about a framework definition, comparison, or selection
DO: → `co-consultant-framework-library`

### Task Classification

1. Does the request need external information gathering?
   - YES → Full workflow starting with `co-consultant-purpose-discovery`
   - NO → next
2. Does the request need structured analysis of existing data?
   - YES → `co-consultant-framework-analysis`
   - NO → next
3. Does the request need a written deliverable?
   - YES → `co-consultant-report-writing`
   - NO → next
4. Is it a framework question or definition lookup?
   - YES → `co-consultant-framework-library`
   - NO → Answer directly

### Full Workflow (SHIKIGAMI)

Phase 0 → `co-consultant-purpose-discovery`: True objective discovery ⏸️ User approval
Phase 1 → `co-consultant-deep-research`: Iterative research (Think→Action→Report)
Phase 2 → `co-consultant-framework-analysis`: Framework application + MECE
Phase 3 → `co-consultant-report-writing`: Pyramid-principle report ⏸️ User approval

### Urgency Triage

| Urgency | Keywords | Workflow |
|---------|----------|---------|
| Normal | (default) | Full 4-phase workflow |
| Urgent | "urgent", "today", "ASAP" | Phase 0 (3 questions max) → Phase 1 (3 rounds max) → Phase 3 |
| Critical | "immediately", "now", "summary only" | Phase 0 (1 question) → Phase 3 (summary only) |

## Data Acquisition (MCP)

Use `deep-research` MCP server when available for structured research.
Falls back to built-in Think→Action→Report cycle when MCP is unavailable.
Config: `.mcp.json` in this directory.

## Required Output Layout

```text
workspace/
├── report.md
├── results/
│   ├── purpose-definition.md
│   ├── research-notes.md
│   ├── framework-outputs.md
│   └── scoring-models/
├── figures/
└── logs/
    └── process-log.jsonl
```

## Verification Loop

Every execution follows: PLAN → EXECUTE → VERIFY → REPORT → LOG

1. **PLAN**: Define business question, constraints, target deliverables, candidate frameworks.
2. **EXECUTE**: Run selected phase pipeline, save intermediate artifacts.
3. **VERIFY**: MECE validation + pyramid structure check + source quality audit.
4. **REPORT**: Write `report.md` with executive summary first (pyramid principle).
5. **LOG**: Finalize `logs/process-log.jsonl`.

## Quality Gates

- [ ] Phase routing matches the user's actual business question.
- [ ] MECE validation passed for all framework analyses.
- [ ] Sources meet quality threshold (3+ sources, weighted trust ≥ 60%).
- [ ] Executive summary conclusions are supported by analysis body.
- [ ] All artifacts saved to files and referenced in `report.md`.
- [ ] No essential result remains chat-only.

## Prohibited Operations

- Do not skip approval checkpoints (⏸️ at Phase 0→1 and Phase 3 end).
- Do not present single-source findings as definitive conclusions.
- Do not include data without source attribution.
- Do not use a framework without justifying its selection rationale.
- Do not proceed from Phase 0 without user-approved true objective.

## Data Handling & Confidentiality

- Client names, financial figures, and strategic plans are confidential. Do not include real client data in templates or examples.
- Anonymize all case references: use "[Client A]", "[Company X]" instead of real names.
- Do not store credentials, API keys, or PII in any generated files.
- When handling competitive intelligence, cite public sources only.
- Mark all draft deliverables as "DRAFT — CONFIDENTIAL" until client approval.

## Cost Efficiency Rules

- Do not enable more than 10 MCP servers simultaneously.
- Default to built-in Think→Action→Report cycle; use MCP only when structured research adds material value.
- Prefer the simplest framework that answers the question. Complex multi-framework analyses cost more context.
- Keep SKILL.md under 100 lines. Move overflow to references/ with conditional access.

## Gotchas

- Purpose Discovery と Deep Research は起動条件が近い。目的が未定ならPurpose Discovery、目的確定済みで情報収集ならDeep Research
- フレームワーク選択では「最もシンプルで目的に合致するもの」を優先する。複雑なフレームワークを適用してもデータが不足なら価値がない
- Phase 間の引き継ぎ情報（真の目的、検索クエリ、収集データ）は必ずファイルに保存。コンパクションで消失する
- 緊急トリアージでもPhase 0の目的確認は省略してはならない。目的を間違えると全工程が無駄になる
