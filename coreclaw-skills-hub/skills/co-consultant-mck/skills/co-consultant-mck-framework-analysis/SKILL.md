---
name: co-consultant-mck-framework-analysis
description: |
  McKinsey-specific framework application with MECE validation and pyramid structuring.
  9 frameworks including McKinsey 7S, Hypothesis-Driven Approach, Issue Tree, Pyramid Principle (Minto).
  Use when ANALYZING data with MCK frameworks, applying MCK-specific methodologies,
  or structuring findings for McKinsey-style deliverables.
---

# Framework Analysis (MCK)

Apply McKinsey-specific frameworks with MECE validation and pyramid structuring.

## Use This Skill When

- Applying a MCK-specific framework.
- Structuring research findings into actionable insights.
- Validating analysis completeness with MECE.

## Framework Selection Guide

| Trigger Keyword | Framework |
|----------------|-----------|
| 7S | McKinsey 7S |
| hypothesis | Hypothesis-Driven Approach |
| issue decomposition | Issue Tree |
| pyramid | Pyramid Principle (Minto) |
| growth horizons | Three Horizons |
| granular | Granularity of Growth |
| overhead | OVA (Overhead Value Analysis) |
| profit pool | Profit Pool Analysis |
| SCP | SCP Analysis |

Refer to `co-consultant-mck-framework-library` for detailed definitions.

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
- MCK固有のフレームワークと汎用フレームワーク（SWOT等）を混在させる場合、MCKフレームワークを主軸にすること

## Validation Loop

1. フレームワーク分析を生成
2. チェック: 選択理由明記、MECE合格、ピラミッド構造あり
3. 不合格なら修正
4. 合格後のみ次Phaseへ
