---
name: consultant-pwc
description: |
  PwC style consulting skill for deep research and analysis.
  Features Fit for Growth, Strategy&, BXT (Business Experience Technology),
  TIMM (Total Impact Measurement & Management), Deal Value Creation,
  and Risk & Regulation frameworks.
  PwC-style integrated workflow combining strategy, technology, and business transformation.
  Supports Deep Research MCP for enhanced web research capabilities.
---

# Consultant PwC (PwC-Style Consulting)

Deep research and consulting analysis skill using PwC methodologies.
Provides Fit for Growth, Strategy&, BXT, and TIMM-centered approaches.

## PwC-Style Workflow

```
Phase 1: Problem Diagnosis
    ↓ Diagnose across Business/Experience/Technology axes
Phase 2: Strategy Formulation (Strategy&)
    ↓ Build capability-driven strategy
Phase 3: Fit for Growth Analysis
    ↓ Right-size cost structure, identify differentiated investments
Phase 4: Total Impact Measurement (TIMM)
    ↓ Impact assessment across economic/social/environmental/tax dimensions
Phase 5: Execution & Transformation
    ↓ Deal value creation, integrated risk management execution
```

## Prompt List

| Prompt | Phase | Description |
|-----------|---------|------|
| **purpose-discovery** | Phase 1 | 課題診断・BXTスコーピング |
| **deep-research** | Phase 2-3 | Strategy& + Fit for Growth |
| **framework-analysis** | Phase 3-4 | PwCフレームワーク分析 |
| **report-writing** | Phase 5 | 統合レポート |
| **full-research** | 全フェーズ | 統合リサーチ |

## Skills

| Skill | Description |
|--------|------|
| **orchestrator** | タスク分類・フェーズルーティング |

## PwC フレームワーク一覧

### 戦略・成長

| フレームワーク | 用途 |
|--------------|------|
| **Strategy&** | ケイパビリティ駆動型の差別化戦略策定 |
| **Fit for Growth** | コスト最適化と成長投資の同時実現 |
| **Deal Value Creation** | M&A/ディールからの価値創出最大化 |

### デジタル・変革

| フレームワーク | 用途 |
|--------------|------|
| **BXT（Business Experience Technology）** | ビジネス・体験・技術の3軸で変革を設計 |
| **Digital Fitness Assessment** | デジタル成熟度の診断と変革ロードマップ |
| **Connected Enterprise** | フロント〜バックの統合デジタル企業モデル |

### インパクト・ガバナンス

| フレームワーク | 用途 |
|--------------|------|
| **TIMM（Total Impact Measurement & Management）** | 経済・社会・環境・税の包括的インパクト |
| **Risk & Regulation** | 規制環境分析とリスクベースの意思決定 |
| **ESG Framework** | ESG統合経営とサステナビリティ戦略 |

## Usage

### Examples

- 「コスト構造を見直して成長投資に回したい」→ Fit for Growth
- 「M&A後の統合計画を作りたい」→ Deal Value Creation
- 「デジタル変革の全体像を設計したい」→ BXT
- 「事業の社会的インパクトを測定したい」→ TIMM
- 「競争優位の戦略を策定したい」→ Strategy&

## 品質検証（PwC基準）

| チェック | 説明 |
|---------|------|
| BXT整合性 | ビジネス・体験・技術の3軸が統合されているか |
| ケイパビリティ駆動 | 「できること」から戦略が構築されているか |
| トータルインパクト | 経済以外（社会・環境・税）を考慮したか |
| 実行可能性 | 規制・リスクを踏まえた実行計画か |
| ステークホルダー | 全ステークホルダーの視点を含むか |
| Right to Win | その市場で勝つ権利（ケイパビリティ）があるか |

## MCP Integration

`deep-research` MCP サーバーが有効な場合、Deep Research フェーズで MCP の構造化リサーチ
フレームワークを活用してください。MCP が利用できない場合は従来の Think→Action→Report
ワークフローを使用します。

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
