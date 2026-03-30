---
name: co-consultant-framework-analysis
description: |
  Consulting framework application with MECE validation and pyramid structuring.
  53 frameworks across 14 categories with auto-recommendation by keyword matching.
  Use when ANALYZING collected data with structured frameworks, applying SWOT/3C/PEST,
  validating MECE completeness, or structuring findings into pyramid format.
---

# Framework Analysis

Apply consulting frameworks to collected data with MECE validation and pyramid structuring.

## Use This Skill When

- Applying a specific framework (SWOT, 3C, PEST, 5 Forces, etc.).
- Structuring research findings into actionable insights.
- Validating analysis completeness with MECE.
- Building pyramid-structured arguments.

## Workflow

1. **Framework selection**: Auto-recommend based on objective + keywords.
   - Refer to `co-consultant-framework-library` for definitions.
   - Prefer the simplest framework that addresses the core question.
   - When multiple fit, choose the one with best data availability.

2. **Framework application**: Map collected data to framework structure.

3. **MECE validation**:
   - [ ] Mutually Exclusive: No overlap between categories
   - [ ] Collectively Exhaustive: No gaps in coverage
   - [ ] Consistent granularity: Same abstraction level
   - [ ] Logical consistency: Classification criteria are uniform

4. **Pyramid structuring**:
   ```
   Conclusion (So What?)
   ├── Argument 1 (Why So?) → Data/Evidence
   ├── Argument 2 (Why So?) → Data/Evidence
   └── Argument 3 (Why So?) → Data/Evidence
   ```

5. **Insight derivation**: Extract actionable insights from analysis.

6. **Action recommendations**: Concrete next steps with owners and timeline.

## Framework Selection Guide

| Trigger Keywords | Recommended Frameworks |
|-----------------|----------------------|
| Strategy, strengths, threats | SWOT, PEST, 5 Forces, 3C |
| Customer, user, persona | Persona, STP, Customer Journey |
| Pricing, cost, value | 4P, Value-Based Pricing |
| Market entry, GTM, launch | AARRR, Ansoff Matrix |
| Competition, differentiation | Blue Ocean, Positioning Map |
| Root cause, problem, why | Fishbone, 5 Whys, Issue Tree |
| Business model, revenue | BMC, Lean Canvas, TAM/SAM/SOM |
| Organization, team, roles | 7S, RACI |
| Risk, uncertainty | Risk Matrix, Scenario Planning |
| Decision, priority, evaluation | Decision Matrix, Weighted Scoring |

## Deliverables

- `results/framework-outputs.md`: structured analysis with MECE validation.
- `figures/`: matrices, positioning maps, or strategy canvases.
- Reuse the output template in `assets/output-template.md` for consistent formatting.

## Quality Gates

- [ ] Framework selection rationale is documented.
- [ ] MECE validation passed (no overlaps, no gaps).
- [ ] Pyramid structure has conclusion → 3(±1) arguments → evidence.
- [ ] Insights are actionable (not just descriptive).
- [ ] So What / Why So check passes for all conclusions.

## Gotchas

- フレームワークを選ぶ前に「このフレームワークで目的の質問に答えられるか」を確認すること。見栄えの良いフレームワークでも目的に合わなければ無価値
- MECE検証で「粒度の不統一」を見落としがち。「日本市場」と「価格戦略」は同じ抽象度ではない
- 複数フレームワークを適用する場合は3つ以内に絞ること。それ以上は情報過多で意思決定を阻害する
- So What / Why So チェックは必ず行うこと。「事実の羅列」と「洞察」は別物

## Validation Loop

1. フレームワーク分析を生成
2. チェック:
   - フレームワーク選択理由が明記されているか
   - MECE検証に合格しているか（重複なし、漏れなし）
   - ピラミッド構造で結論→根拠→データの階層があるか
   - インサイトが具体的で実行可能か
3. 不合格なら該当箇所を修正
4. 合格後のみ次のPhaseへ
