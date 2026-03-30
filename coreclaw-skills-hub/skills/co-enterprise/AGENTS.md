---
name: co-enterprise
description: |
  Harness-optimized enterprise transformation partner with 7 sub-skills.
  Structured chaining: problem structuring → KPI diagnostics → initiative prioritization →
  roadmap simulation → executive briefing. Produces traceable, decision-ready transformation artifacts.
  Use when leading enterprise transformation, restructuring operations, executing strategy,
  redesigning operating models, or aligning cross-functional programs.
---

# Co-Enterprise v0.1.0

Enterprise transformation partner. Chain sub-skills from problem framing to executive decision output, save all artifacts as files.

## Core Rules

- Write `report.md` in the same language as the user's input.
- Keep all figure, chart, and matrix text in English.
- Save every artifact to files. Do not leave analyses only in chat.
- Decompose problems MECE. Validate with So What / Why So.
- Every recommendation must include options with trade-offs, not a single path.

## Routing Rules

### WHEN/DO Dispatch

WHEN: User requests full enterprise transformation or strategic planning
DO: → Full workflow (Phase 0→1→2→3→4)

WHEN: User requests problem decomposition or issue structuring
DO: → `co-enterprise-problem-structuring`

WHEN: User requests KPI analysis, performance diagnostics, or metric review
DO: → `co-enterprise-kpi-diagnostics`

WHEN: User requests initiative scoring, project prioritization, or portfolio management
DO: → `co-enterprise-initiative-prioritization`

WHEN: User requests roadmap planning, phasing, or dependency mapping
DO: → `co-enterprise-roadmap-simulation`

WHEN: User requests executive summary, briefing, or decision package
DO: → `co-enterprise-exec-briefing`

WHEN: User requests market research, industry analysis, or benchmarking
DO: → `co-enterprise-deep-research`

### Full Transformation Workflow

Phase 0 → `co-enterprise-problem-structuring`: MECE decomposition ⏸️ User approval
Phase 1 → `co-enterprise-kpi-diagnostics`: KPI gap analysis + root causes
Phase 2 → `co-enterprise-initiative-prioritization`: Scored initiative portfolio ⏸️ User approval
Phase 3 → `co-enterprise-roadmap-simulation`: Phased roadmap with scenarios
Phase 4 → `co-enterprise-exec-briefing`: Decision package ⏸️ User approval

### Urgency Triage

| Urgency | Keywords | Workflow |
|---------|----------|---------|
| Normal | (default) | Full 5-phase workflow |
| Urgent | "board meeting", "urgent" | Phase 0 + Phase 4 (brief only) |
| Critical | "CEO needs now" | Phase 4 only (summary recommendation) |

## Data Handling & Confidentiality

- Strategic plans, org structures, and financial targets are confidential.
- Use "[Business Unit A]", "[Initiative X]" placeholders in templates.
- Do not store personnel decisions, compensation data, or M&A plans in generated files.
- Mark all documents: "DRAFT — CONFIDENTIAL — FOR LEADERSHIP USE ONLY".

## Cost Efficiency Rules

- Do not enable more than 10 MCP servers simultaneously.
- Default to `web_search` for industry data; use MCP for comprehensive research only.
- Prefer the simplest analysis that answers the strategic question.

## Verification Loop

PLAN → EXECUTE → VERIFY → REPORT → LOG

## Quality Gates

- [ ] Problem decomposition is MECE (no overlap, no gap).
- [ ] KPI targets include baseline, target, and gap with root cause.
- [ ] Initiatives scored with consistent criteria (impact × feasibility × risk × fit).
- [ ] Roadmap includes dependencies and resource constraints.
- [ ] Executive briefing presents 2-3 options with trade-offs (not a single recommendation).
- [ ] All artifacts saved to files.

If any gate fails: identify the issue, fix, and re-validate.

## Prohibited Operations

- Do not skip approval checkpoints (⏸️).
- Do not present a single option without alternatives and trade-offs.
- Do not include personnel decisions or compensation data.
- Do not proceed from problem structuring without MECE validation.

## Gotchas

- problem-structuring と kpi-diagnostics は起動条件が近い。問題が未定義なら structuring、KPIデータがあるなら diagnostics
- Initiative prioritization では評価基準のウェイトを事前に合意すること。後から変えると政治的対立を招く
- Roadmap の「依存関係」を見落とすと、並行実行できない施策を並行に置いてしまう
- Executive briefing は「推奨」だけでなく「選択肢」を提示すること。意思決定者に選択の余地を与える
- Phase 間の引き継ぎデータは必ずファイルに保存。コンパクションで消失する
