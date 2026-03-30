---
name: context-manager
description: |
  Manage session context and handoffs across educationalist sub-skills.
  Use when outputs from one education workflow need to be reused, summarized, or validated by another.
---

# コンテキスト管理スキル

> セッション内の情報を保持し、スキル間のデータ受け渡しを管理します。

## 概要

このスキルは、educationalistのセッション全体を通じてコンテキスト（文脈情報）を管理します。会話履歴、前回のスキル実行結果、ユーザー設定などを保持し、スキル間の連携を円滑にします。

## 主な機能

### 1. セッションコンテキストの保持

会話セッション中に以下の情報を保持します：

- **会話履歴**: ユーザーとの対話履歴
- **スキル実行結果**: 各スキルが生成したコンテンツ
- **メタプロンプト**: 収集したコンテキスト情報
- **教育理論参照**: 参照した教育理論
- **ユーザー設定**: デフォルトの学年・教科など

### 2. コンテキスト操作

#### remember（記憶）
情報をセッションコンテキストに保存します。

#### recall（想起）
保存された情報を取得します。

#### clear（クリア）
コンテキストをクリアします。

#### summarize（要約）
セッションの要約を生成します。

## 依存関係の解決

| スキル | 依存先 | 依存内容 |
|--------|--------|----------|
| materials | lesson-plan | 授業の流れ、時間配分 |
| assessment | lesson-plan | 学習目標、評価観点 |
| feedback | assessment | 評価基準、観点 |
| individual | assessment | 評価結果、課題 |