---
name: orchestrator
description: |
  Route education support requests to the most appropriate educationalist sub-skill.
  Use when deciding among lesson planning, materials, assessment, individual support,
  feedback, guidance, or theory lookup.
---

# オーケストレーター

> ユーザーのリクエストを分析し、最適なスキルにルーティングする指揮者です。

## 概要

このスキルは、ユーザーの入力を分析し、educationalistパッケージ内の適切なスキルに振り分けます。複合的なリクエストの場合は、複数スキルの実行順序を管理します。

## キーワードルーティング

| キーワード | スキル | 優先度 |
|-----------|--------|--------|
| 授業計画、指導案、本時の展開 | lesson-plan | 高 |
| ワークシート、スライド、教材、プリント、クイズ | materials | 高 |
| テスト、ルーブリック、評価、採点 | assessment | 高 |
| 個別指導、支援計画、学習スタイル、ZPD | individual | 高 |
| フィードバック、コメント、添削、振り返り | feedback | 高 |
| 生活指導、生徒指導、不登校、いじめ、行動 | guidance | 高 |
| 教育理論、理論、エビデンス | theory-lookup | 中 |

## 実行順序

複合リクエスト時の推奨実行順序：

```
meta-prompt（コンテキスト収集）
  ↓
lesson-plan（授業計画）
  ↓
materials（教材作成）
  ↓
assessment（評価設計）
  ↓
feedback（フィードバック）
```