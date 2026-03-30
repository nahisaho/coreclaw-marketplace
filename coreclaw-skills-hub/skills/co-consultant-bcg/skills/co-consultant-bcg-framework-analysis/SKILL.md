---
name: co-consultant-bcg-framework-analysis
description: |
  BCG-specific framework application with MECE validation and pyramid structuring.
  12 frameworks including BCG Growth-Share Matrix, BCG Experience Curve, BCG Strategy Palette, Hypothesis-Driven Approach.
  Use when ANALYZING data with BCG frameworks, applying BCG-specific methodologies,
  or structuring findings for BCG-style deliverables.
---

# Framework Analysis (BCG)

Apply BCG-specific frameworks with MECE validation and pyramid structuring.

## Use This Skill When

- Applying a BCG-specific framework.
- Structuring research findings into actionable insights.
- Validating analysis completeness with MECE.

## Framework Selection Guide

| Trigger Keyword | Framework |
|----------------|-----------|
| portfolio | BCG Growth-Share Matrix |
| cost curve | BCG Experience Curve |
| strategy type | BCG Strategy Palette |
| hypothesis | Hypothesis-Driven Approach |
| TSR | BCG TSR Analysis |
| industry analysis | BCG Advantage Matrix |
| value chain | Deconstruction |
| speed | Time-Based Competition |
| growth horizons | Three Horizons |
| granular growth | Granularity of Growth |
| profit pool | Profit Pool Analysis |
| digital acceleration | Digital Acceleration Index |

Refer to `co-consultant-bcg-framework-library` for detailed definitions.

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
- Reuse `assets/output-template.md` when producing standardized framework analysis output.

## Quality Gates

- [ ] Framework selection rationale documented.
- [ ] MECE validation passed.
- [ ] Pyramid structure has conclusion → arguments → evidence.
- [ ] Insights are actionable.


If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- フレームワークを選ぶ前に「このフレームワークで目的の質問に答えられるか」を確認すること
- 複数フレームワークを適用する場合は3つ以内に絞ること
- BCG固有のフレームワークと汎用フレームワーク（SWOT等）を混在させる場合、BCGフレームワークを主軸にすること

## Validation Loop

1. フレームワーク分析を生成
2. チェック: 選択理由明記、MECE合格、ピラミッド構造あり
3. 不合格なら修正
4. 合格後のみ次Phaseへ
