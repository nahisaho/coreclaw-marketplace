---
name: consultant-mck
description: |
  McKinsey style consulting skill for deep research and analysis.
  Features 7S Framework, Hypothesis-Driven Approach, Issue Tree, Pyramid Principle,
  Three Horizons, Granularity of Growth, OVA, Profit Pool Analysis, and SCP Analysis.
  McKinsey-style 5-phase workflow: Problem Definition → Hypothesis → Issue Decomposition →
  Data Collection/Analysis → Integration/Recommendation.
  Supports Deep Research MCP for enhanced web research capabilities.
---

# Consultant McK (McKinsey-Style Consulting)

Deep research and consulting analysis skill using McKinsey methodologies.
Provides hypothesis-driven, MECE, Pyramid Principle, and 7S Framework-centered approaches.

## McKinsey-Style Workflow

```
Phase 1: Problem Definition
    ↓ Identify true client issues, define success
Phase 2: Hypothesis Construction
    ↓ Set Day 1 Answer, organize supporting arguments
Phase 3: Issue Decomposition
    ↓ MECE decomposition via Issue Tree, prioritization
Phase 4: Data Collection & Analysis
    ↓ 80/20 analysis, insight extraction via So What?
Phase 5: Integration & Recommendations
    ↓ Structure via Pyramid Principle, formulate action plan
```

## Prompt List

| Prompt | Phase | Description |
|-----------|---------|------|
| **purpose-discovery** | Phase 1-2 | 問題定義・仮説構築 |
| **deep-research** | Phase 3-4 | イシュー分解・データ収集 |
| **framework-analysis** | Phase 4 | McKフレームワーク分析 |
| **report-writing** | Phase 5 | 統合・提言レポート |
| **full-research** | 全フェーズ | 統合リサーチ |

## Skills

| Skill | Description |
|--------|------|
| **orchestrator** | タスク分類・フェーズルーティング |
| **framework-library** | McK固有フレームワーク定義 |

## マッキンゼー・フレームワーク一覧

### 問題解決・仮説思考

| フレームワーク | 用途 |
|--------------|------|
| **仮説駆動アプローチ** | 仮説を立て、検証し、結論を導く問題解決手法 |
| **イシューツリー** | 問題をMECEに分解し、解決の優先順位を明確化 |
| **ピラミッド原則** | 結論先行で論理的にコミュニケーション（Barbara Minto） |
| **MECE** | 漏れなくダブりなく、分析の基本原則 |

### 組織・戦略

| フレームワーク | 用途 |
|--------------|------|
| **マッキンゼーの7S** | 組織の7要素の整合性分析（ハード3S + ソフト4S） |
| **3つの地平線** | 短期（H1）・中期（H2）・長期（H3）の成長を同時管理 |
| **成長のグラニュラリティ** | 成長を詳細に分解して真の成長源を特定 |

### 業績改善

| フレームワーク | 用途 |
|--------------|------|
| **間接費価値分析（OVA）** | 間接部門のコストと価値を分析し最適化 |
| **プロフィットプール分析** | バリューチェーン全体の利益分布を可視化 |
| **SCP分析** | 産業構造→企業行動→業績の因果関係を分析 |

## Usage

### Examples

- 「新規事業の方向性を検討したい」→ 3つの地平線 + 成長のグラニュラリティ
- 「組織の問題点を分析して」→ マッキンゼーの7S
- 「コスト構造を見直したい」→ OVA + プロフィットプール分析
- 「業界の構造を分析して」→ SCP分析

## 品質検証（マッキンゼー基準）

| チェック | 説明 |
|---------|------|
| MECE性 | イシュー分解の重複なし・漏れなし |
| 仮説検証 | Day 1 Answerとの整合性 |
| ファクトベース | データに基づく定量分析 |
| So What | 経営層への示唆が明確 |
| 80/20 | 最も重要な20%の分析にフォーカス |
| ピラミッド構造 | 結論→根拠の論理的階層 |

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
