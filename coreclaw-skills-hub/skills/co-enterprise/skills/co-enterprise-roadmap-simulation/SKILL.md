---
name: co-enterprise-roadmap-simulation
description: |
  Phased transformation roadmap with dependency mapping and scenario simulation.
  Use when PLANNING transformation phases, mapping initiative dependencies,
  simulating resource allocation scenarios, or building execution timelines.
---

# Roadmap Simulation

Phased roadmap with dependencies and scenario analysis.

## Use This Skill When

- Building phased transformation execution plans.
- Mapping dependencies between initiatives.
- Simulating optimistic/base/pessimistic scenarios.

## Workflow

1. Sequence initiatives from prioritization (Phase 1/2/3).
2. Map dependencies (what must complete before what).
3. Assign resource requirements per phase.
4. Simulate 3 scenarios (optimistic/base/pessimistic).
5. Identify critical path and bottlenecks.
6. Save to files.

## Deliverables

- `results/roadmap.md`: phased roadmap with scenarios.

## Quality Gates

- [ ] Dependencies explicitly mapped.
- [ ] Resource constraints validated per phase.
- [ ] 3 scenarios include timeline and resource variations.
- [ ] Critical path identified.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 依存関係を見落とすと並行実行できない施策を並行に配置してしまう。必ず依存グラフを作成すること
- 「楽観シナリオ」だけでなく「悲観シナリオ」でも実行可能な計画にすること
- リソース制約は「人」「金」「時間」の3つを全て検証すること

## Validation Loop

1. ロードマップを生成
2. チェック: 依存関係、リソース制約、3シナリオ、クリティカルパス
3. 不合格なら修正
4. 合格後のみ完了
