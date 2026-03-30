---
name: co-consultant-acn-framework-library
description: |
  Accenture-specific framework definitions and selection reference.
  11 frameworks covering organization, cost, transformation, strategy, operations.
  Use when looking up ACN framework definitions, comparing frameworks,
  or selecting the best ACN framework for a business question.
---

# Framework Library (ACN)

11 Accenture-specific framework definitions.

## Use This Skill When

- Looking up a ACN-specific framework definition.
- Comparing ACN frameworks for a business question.
- Selecting the best framework from ACN candidates.

## Framework Index

| Framework | Primary Trigger | Category |
|-----------|----------------|----------|
| DX Strategy Framework | DX | transformation |
| Digital Maturity Assessment | digital maturity | transformation |
| Technology Vision | technology trends | transformation |
| Zero-Based Budgeting (ZBB) | zero-based | cost |
| Cost Excellence | cost optimization | cost |
| Intelligent Operations | automation | operations |
| Process Excellence | process improvement | operations |
| Value Creation Framework | value creation | strategy |
| Growth Strategy | growth | strategy |
| Change Management | change | organization |
| Talent Strategy | talent | organization |

## Recommended Workflow Patterns


### DX Transformation
`Digital Maturity Assessment` → `Technology Vision` → `DX Strategy Framework` → `Intelligent Operations` → `Talent Strategy`

### Cost Transformation
`Cost Excellence` → `Zero-Based Budgeting` → `Process Excellence` → `Value Creation Framework`

### Growth Strategy
`Growth Strategy` → `Value Creation Framework` → `Change Management` → `Talent Strategy`


## Selection Principles

1. Choose the ACN framework that directly answers the core question.
2. Prefer simpler frameworks when data is limited.
3. Maximum 3 frameworks per analysis.
4. ACN frameworks take priority over generic frameworks when applicable.
5. Read detailed definitions in `references/acn-frameworks.md` when applying a specific framework.

## Quality Gates

- [ ] Framework definition is accurate and complete.
- [ ] Selection rationale matches the business objective.
- [ ] Recommended frameworks do not exceed 3.
- [ ] Detailed reference is conditionally referenced (not loaded unconditionally).


If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- ACNフレームワークは「考える道具」であって「答え」ではない。フレームワークを埋めることが目的になってはならない
- 汎用フレームワーク（SWOT, 3C等）とACNフレームワークは併用可能だが、ACN固有の視点を主軸にすること
- フレームワーク間の推奨ワークフロー順序を無視して適用すると、前提となるデータが不足する

## Validation Loop

1. フレームワーク情報を提供
2. チェック: 定義が正確か、選択理由が目的と合致しているか
3. 不合格なら修正
