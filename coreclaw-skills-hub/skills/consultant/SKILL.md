---
name: consultant-assistant
description: |
  AI consultant skill for deep research and consulting analysis.
  Based on the SHIKIGAMI methodology, featuring 4-phase workflow:
  Purpose Discovery, Deep Research, Framework Analysis, and Report Writing.
  Provides 53 consulting frameworks across 14 categories with MECE validation,
  pyramid structuring, and hypothesis-driven analysis.
---

# Consultant Assistant

AI assistant skill package for deep research and consulting analysis.

## Workflow

Provides a consulting workflow composed of 4 phases.

```
Phase 1: Purpose Discovery
    ↓ Discover true objective via 5 Whys / JTBD
Phase 2: Deep Research
    ↓ Gather information via Think→Action→Report cycle
Phase 3: Framework Analysis
    ↓ Structured analysis with 53 frameworks
Phase 4: Report Writing
    ↓ Report writing based on Pyramid Principle
```

## Prompt List

| Prompt | Phase | Description |
|-----------|---------|------|
| **purpose-discovery** | Phase 1 | Start interactive purpose discovery |
| **deep-research** | Phase 2 | Execute iterative deep research |
| **framework-analysis** | Phase 3 | Execute framework analysis |
| **report-writing** | Phase 4 | Generate report |
| **full-research** | All Phases | Execute integrated research |

## Skills

| Skill | Description |
|--------|------|
| **orchestrator** | Request classification and phase routing |
| **framework-library** | 53 framework definitions and selection support |

## Usage

The orchestrator automatically selects the appropriate phase based on user requests.

### Examples

- "Competitive analysis" → purpose-discovery → discover true objective
- "Research AI market" → full-research → integrated research
- "SWOT analysis of collected data" → framework-analysis
- "Compile findings into report" → report-writing
- "Create new business proposal" → full-research (all phases)

## Frameworks（53定義）

| Category | Count | Examples |
|---------|------|--------|
| Strategy Analysis | 10 | SWOT, 3C, PEST, 5Forces, BCG, VRIO |
| Problem Solving | 7 | MECE, Logic Tree, Issue Tree, 5 Whys, Fishbone |
| Thought Organization | 3 | Pyramid Structure, So What/Why So, PREP |
| Decision Making | 4 | Decision Matrix, Pros/Cons, Risk Matrix, Cost-Benefit |
| Marketing | 7 | 4P, 4C, STP, Customer Journey, Persona, AIDMA/AISAS |
| Innovation | 7 | BMC, Lean Canvas, TAM/SAM/SOM, Design Thinking, SCAMPER |
| Process Improvement | 3 | PDCA, OODA, ECRS |
| Organizational Analysis | 2 | 7S, RACI |
| Customer Analysis | 2 | RFM, NPS |
| General Tools | 5 | 5W1H, SMART, OKR, KPT, JTBD |
| Financial Analysis | 3 | DuPont, CVP, DCF |

## Quality Gates

Quality gates between phases ensure analysis quality.

## MCP Integration

`deep-research` MCP サーバーが Settings > MCP Servers で有効な場合、Phase 2（Deep Research）で
構造化リサーチフレームワーク（課題精緻化→サブ質問分解→Web検索→ソース評価→レポート生成）を
活用してください。MCP が利用できない場合は従来の Think→Action→Report ワークフローを使用します。

| ゲート | 条件 | ユーザー承認 |
|--------|------|-------------|
| 1→2 | 真の目的が定義済、リサーチ計画作成済、最低3回の対話 | **必要** |
| 2→3 | 3件以上のソース、信頼度60%以上 | 不要 |
| 3→4 | 1件以上のフレームワーク適用、数値検証済 | 不要 |
| 4→完了 | レポート存在、品質チェック通過、引用完備 | **必要** |

## 緊急度トリアージ

| レベル | キーワード | ワークフロー |
|--------|----------|-------------|
| 通常 | − | 全フェーズ実行 |
| 急ぎ | 急ぎ、今日中、明日まで | Phase 1→2簡略→3→4簡略 |
| 緊急 | 今すぐ、至急、概要のみ | Phase 1→2概要→4サマリー |

---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY  → check outputs against quality gates
REPORT  → save all artifacts, generate report
```

### Quality Gates

- [ ] All outputs include explicit assumptions and constraints
- [ ] Traceable reasoning between steps
- [ ] Final recommendation with clear next actions
- [ ] Artifacts saved as files (not chat-only output)
