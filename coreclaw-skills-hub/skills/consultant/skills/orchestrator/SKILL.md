---
name: orchestrator
description: |
  Route consultant requests to the most appropriate staged workflow.
  Use when deciding between purpose discovery, deep research, framework analysis,
  report writing, or the full-research workflow.
---

# オーケストレーター

> ユーザーのリクエストを分析し、最適なフェーズにルーティングする指揮者です。

## 概要

ユーザーの入力を分析し、consultantパッケージ内の適切なプロンプトに振り分けます。
複合的なリクエストの場合は、full-researchワークフローを実行します。

## タスク分類

### Phase 0 が必要なタスク（リサーチ・報告タスク）

以下のカテゴリに該当するリクエストは、Purpose Discoveryから開始します。

| カテゴリ | 例 |
|---------|-----|
| リサーチ・分析 | 市場調査、競合分析、技術動向調査 |
| コンテンツ作成 | レポート、提案書、事業計画書 |
| 情報収集 | トレンド調査、ベンチマーク、ベストプラクティス |

### 直接対応可能なタスク

以下はPurpose Discoveryを経ずに直接対応します。

| カテゴリ | 例 |
|---------|-----|
| 質問応答 | 「MECEとは何ですか？」 |
| ファイル操作 | 「このファイルを読んで」 |
| コード関連 | 「この関数を修正して」 |

## キーワードルーティング

| キーワード | プロンプト | 優先度 |
|-----------|----------|--------|
| 調べて、調査、リサーチ、分析して | full-research | 高 |
| 目的、なぜ、真のゴール | purpose-discovery | 高 |
| 検索、情報収集、深掘り | deep-research | 高 |
| SWOT、3C、PEST、フレームワーク | framework-analysis | 高 |
| レポート、報告書、提案書、まとめて | report-writing | 高 |

## 緊急度判定

| キーワード | 緊急度 |
|-----------|--------|
| 急ぎ、今日中、明日まで、ASAP | urgent |
| 今すぐ、至急、概要のみ、すぐに | critical |
| それ以外 | normal |