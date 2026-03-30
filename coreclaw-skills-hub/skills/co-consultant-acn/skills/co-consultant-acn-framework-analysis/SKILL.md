---
name: co-consultant-acn-framework-analysis
description: |
  Accenture-specific framework application with MECE validation and pyramid structuring.
  11 frameworks including DX Strategy Framework, Digital Maturity Assessment, Technology Vision, Zero-Based Budgeting (ZBB).
  Use when ANALYZING data with ACN frameworks, applying ACN-specific methodologies,
  or structuring findings for Accenture-style deliverables.
---

# Framework Analysis (ACN)

Apply Accenture-specific frameworks with MECE validation and pyramid structuring.

## Use This Skill When

- Applying a ACN-specific framework.
- Structuring research findings into actionable insights.
- Validating analysis completeness with MECE.

## Framework Selection Guide

| Trigger Keyword | Framework |
|----------------|-----------|
| DX | DX Strategy Framework |
| digital maturity | Digital Maturity Assessment |
| technology trends | Technology Vision |
| zero-based | Zero-Based Budgeting (ZBB) |
| cost optimization | Cost Excellence |
| automation | Intelligent Operations |
| process improvement | Process Excellence |
| value creation | Value Creation Framework |
| growth | Growth Strategy |
| change | Change Management |
| talent | Talent Strategy |

Refer to `co-consultant-acn-framework-library` for detailed definitions.

## Workflow

1. Select framework based on objective + keywords.
2. Apply framework to collected data.
3. MECE validation (no overlap, no gaps, consistent granularity).
4. Pyramid structuring (conclusion → 3 arguments → evidence).
5. Derive actionable insights.
6. Recommend concrete next steps.

## Deliverables

- `results/framework-outputs.md`: structured analysis with MECE validation.
- `figures/`: matrices, maps, or strategy canvases.
- Reuse output template in `assets/output-template.md`.

## Quality Gates

- [ ] Framework selection rationale documented.
- [ ] MECE validation passed.
- [ ] Pyramid structure has conclusion → arguments → evidence.
- [ ] Insights are actionable.

## Gotchas

- フレームワークを選ぶ前に「このフレームワークで目的の質問に答えられるか」を確認すること
- 複数フレームワークを適用する場合は3つ以内に絞ること
- ACN固有のフレームワークと汎用フレームワーク（SWOT等）を混在させる場合、ACNフレームワークを主軸にすること

## Validation Loop

1. フレームワーク分析を生成
2. チェック: 選択理由明記、MECE合格、ピラミッド構造あり
3. 不合格なら修正
4. 合格後のみ次Phaseへ
