---
name: co-enterprise-problem-structuring
description: |
  MECE decomposition of ambiguous business problems into decision-ready workstreams.
  Issue trees, hypothesis generation, and workstream definition.
  Use when STRUCTURING strategic problems, decomposing transformation challenges,
  defining workstreams, or framing ambiguous business questions.
---

# Problem Structuring

MECE decomposition into decision-ready workstreams.

## Use This Skill When

- Decomposing ambiguous strategic challenges.
- Building issue trees for transformation programs.
- Defining workstreams with clear ownership.

## Workflow

1. Clarify the strategic question (one sentence).
2. Build issue tree (MECE, max 3 levels).
3. Generate hypotheses for each terminal node.
4. Define workstreams with scope, owner, and deliverables.
5. Validate MECE + So What / Why So.
6. Save to files.

## Deliverables

- `results/problem-structure.md`: issue tree + workstreams.
- Reuse `assets/issue-tree-template.md` when producing standardized decompositions.

## Quality Gates

- [ ] Issue tree is MECE at every level.
- [ ] So What / Why So passes for all nodes.
- [ ] Workstreams have clear scope, owner, and deliverables.
- [ ] Strategic question stated in one sentence.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- Issue tree は最大3レベル。深すぎると実行不能になる
- 「MECE」の検証は各レベルで独立して行うこと。Level 1 が MECE でも Level 2 が重複していることがある
- 仮説は「検証可能」であること。検証不能な仮説はイシューツリーに含めない

## Validation Loop

1. Issue tree + workstreams を生成
2. チェック: MECE、So What/Why So、ワークストリーム定義
3. 不合格なら修正
4. ユーザー承認後のみ完了 ⏸️
