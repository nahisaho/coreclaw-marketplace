# Skills 作成ガイド

このガイドでは、coreclaw-skills-hubマーケットプレースにスキルを登録・公開するための手順とベストプラクティスを説明します。

## 目次

1. [ディレクトリ構造](#ディレクトリ構造)
2. [skill.json スキーマ](#skilljson-スキーマ)
3. [group.json スキーマ](#groupjson-スキーマ)
4. [ファイル要件](#ファイル要件)
5. [命名規則](#命名規則)
6. [スキル作成手順](#スキル作成手順)
7. [リリース手順](#リリース手順)
8. [ベストプラクティス](#ベストプラクティス)
9. [ハーネス最適化](#ハーネス最適化)

---

## ディレクトリ構造

### package-style グループ root（スイート親）

```
coreclaw-skills-hub/skills/
└── <group-name>/
    ├── group.json                    # グループメタデータ
  ├── skill.json                    # root互換メタデータ
  ├── README.md                     # パッケージ説明 / root entrypoint 対象
  ├── orchestration.json            # 任意のルーティング・契約メタデータ
  ├── agents/                       # 任意のagent manifest
  ├── hooks/                        # 任意のhook設定
  ├── commands/                     # 任意のcommand doc
  ├── docs/                         # 任意の監査・補助doc
  └── skills/
    ├── orchestrator/
    │   └── SKILL.md
    └── <specialized-skill>/
      └── SKILL.md
```

例：`agent-skills-builder/`, `dx-agent/`のような生成スイートルート

### インストール可能な単一スキルルート

```
coreclaw-skills-hub/skills/
└── <group-name>/<skill-name>/
  ├── SKILL.md                      # 正式なスキル定義
  ├── README.md                     # マーケットプレース向け説明
  ├── skill.json                    # 任意の互換メタデータ
  ├── main.py                       # entrypoint が main.py の場合だけ必要
  └── [その他のアセット]
```

例：`scientist/scientific-academic-writing/`, `growth/growth-funnel-analysis/`

---

## skill.json スキーマ

### 最小限の例

```json
{
  "name": "my-skill-name",
  "version": "v0.1.0",
  "description": "Brief description of what this skill does",
  "entrypoint": "README.md"
}
```

### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `name` | string | ✅ | スキルの一意な名前。ケバブケース（kebab-case）で記述。EXドメイン内で重複しない必要があります。 |
| `version` | string | ✅ | セマンティック バージョン（Semantic Versioning）形式：`vX.Y.Z`。例：`v0.1.0`, `v1.2.3` |
| `description` | string | ✅ | スキルの簡潔な説明（英語推奨）。1-2 文で概要を説明。 |
| `entrypoint` | string | ✅ | 互換 entrypoint として使う既存ファイル。`SKILL.md`、`README.md`、`main.py` など |
| `author` | string | ❌ | スキル作成者の名前またはメールアドレス |
| `license` | string | ❌ | ライセンスタイプ。例：`MIT`, `Apache-2.0` |
| `keywords` | array | ❌ | スキルを分類するキーワード。例：`["research", "writing", "academic"]` |

### 拡張例

```json
{
  "name": "scientific-academic-writing",
  "version": "v0.2.0",
  "description": "Assists researchers in composing high-quality academic papers with proper structure and citation formatting",
  "entrypoint": "SKILL.md",
  "author": "research-team",
  "license": "MIT",
  "keywords": ["research", "writing", "academic", "paper", "documentation"]
}
```

---

## group.json スキーマ

グループ（スキルカテゴリ）のメタデータを定義します。グループディレクトリの直下に配置。

### 最小限の例

```json
{
  "name": "Scientist",
  "description": "Skills for scientists and researchers",
  "icon": "🔬",
  "count": 196
}
```

### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `name` | string | ✅ | グループの表示名。ユーザーフレンドリーな形式。 |
| `description` | string | ✅ | グループの説明（英語）。このグループに属するスキルの共通の特徴を説明。 |
| `icon` | string | ✅ | グループを表す絵文字またはアイコン。UI での表示用。 |
| `count` | number | ✅ | グループ内のスキル数。Registry 生成時に更新される。 |

### 使用可能なアイコン例

```
🔬  科学者向け (scientist)
💼  コンサルタント向け (consultant)
📚  教育関係者向け (educationalist)
📊  データサイエンティスト向け
🔧  エンジニア向け
💡  イノベーション向け
```

---

## ファイル要件

### SKILL.md（スキルドキュメント）

スキルの詳細なドキュメント。インストール可能な各スキルルートに配置します。

**必須セクション：**

```markdown
# [Skill Name]

## 概要
スキルが何をするか、誰を対象にしているかの概要。

## 主な機能
- 機能 1
- 機能 2
- 機能 3

## 使用方法
スキルの使用方法や実行例。

## 入出力フォーマット
入力と出力の仕様。

## 前提条件
必要な環境、依存関係、アクセス権限など。

## ライセンス
スキルのライセンス情報。
```

### Orchestrator用SKILL.md（スイート構成で必須）

`<group>/skills/orchestrator/` のようなオーケストレーター用サブスキルでは、`SKILL.md` に次のセクションを含めます。

- `## Orchestration Flow`
- `## Input Contract`
- `## Output Contract`
- `## Quality Gates`
- `## Fallback Policy`

サブスキル連携順と検証ルールを明示してください。

### main.py（任意の runtime entrypoint）

互換`entrypoint`が`main.py`を指す場合だけ必要なPythonスクリプトです。

**最小限の例：**

```python
#!/usr/bin/env python3
"""Marketplace entrypoint for [Skill Name]."""

def main():
    """Execute skill logic."""
    print("Skill executed successfully")

if __name__ == "__main__":
    main()
```

### README.md（マーケットプレース向け説明）

レジストリに表示される短い説明。`description` に基づいて作成。

**例：**

```markdown
# Scientific Academic Writing

Assists researchers in composing high-quality academic papers with proper structure 
and citation formatting.

## Features

- Automated abstract generation
- Citation management
- Structure validation
- Language polish

## Quick Start

```bash
python main.py
```

## Requirements

- Python 3.8+
- LaTeX for PDF generation (optional)
```

---

## 命名規則

### グループ名
- 英語、ケバブケース（kebab-case）
- 複数形推奨：`scientists`, `consultants`
- 例： `scientist`, `consultant`, `consultant-acn`, `educationalist`

### スキル名
- 英語、ケバブケース（kebab-case）
- スキルの機能を明確に表現
- 例： `scientific-academic-writing`, `strategic-planning`, `presentation-design`

### バージョン番号
- セマンティック バージョニング（Semantic Versioning）準拠
- 形式：`vMAJOR.MINOR.PATCH`
- 例： `v0.1.0`, `v1.0.0`, `v2.1.3`

**版のガイドライン：**
- `MAJOR`：互換性を失う変更を行った場合
- `MINOR`：後方互換性を保ちながら機能を追加した場合
- `PATCH`：バグ修正などの小さな変更の場合

---

## スキル作成手順

### 1. 構成タイプを選択

- **package-style スイート root（複数スキルのオーケストレーション向け、推奨）**

```bash
mkdir -p coreclaw-skills-hub/skills/<group>
mkdir -p coreclaw-skills-hub/skills/<group>/skills/orchestrator
mkdir -p coreclaw-skills-hub/skills/<group>/skills/<specialized-skill>
```

- **単一のインストール可能スキル**

```bash
mkdir -p coreclaw-skills-hub/skills/<group>/<skill-name>
cd coreclaw-skills-hub/skills/<group>/<skill-name>
```

### 2. スイートルートが必要ならルートメタデータを作成

package-style suite rootでは、次を作成します。

- `group.json`
- `skill.json`
- `README.md`

ルートに実ランタイムがない場合、`entrypoint`は通常`README.md`を使います。

### 3. SKILL.md を作成

正式なメタデータと手順を定義します：

```markdown
---
name: <skill-name>
description: |
  Your skill description here
---

# [Skill Name]

## 概要
説明
```

### 4. README.md を作成

マーケットプレース向けの説明：

```markdown
# [Skill Name]

Brief description and features
```

### 5. 必要な場合だけ互換メタデータを追加

```json
{
  "name": "<skill-name>",
  "version": "v0.1.0",
  "description": "Your skill description here",
  "entrypoint": "SKILL.md"
}
```

### 6. main.py は必要な場合だけ作成

`skill.json` を置く場合だけ必要です。

スキルのロジックを実装：

```python
#!/usr/bin/env python3
"""[Skill Name] implementation."""

def main():
    """Main skill execution."""
    # Your implementation here
    pass

if __name__ == "__main__":
    main()
```

### 7. 変更をコミット

```bash
git add <group>/<skill-name>/
git commit -m "feat: add <skill-name> skill"
git push origin main
```

---

## リリース手順

### 1. リリース対象の更新を確定

`SKILL.md` が正式定義です。互換メタデータがある場合だけ `skill.json` のバージョンも更新します。

```json
{
  "name": "my-skill",
  "version": "v0.2.0",  // <- Update this
  "description": "...",
  "entrypoint": "SKILL.md"
}
```

### 2. 変更をコミット

```bash
git add coreclaw-skills-hub/skills/<group>/<skill-name>/SKILL.md
git add coreclaw-skills-hub/skills/<group>/<skill-name>/README.md
git add coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json
git commit -m "bump: version v0.2.0 for <skill-name>"
git push origin main
```

package-style suite rootでは、ルートメタデータも必要に応じてコミットします。

```bash
git add coreclaw-skills-hub/skills/<group>/group.json
git add coreclaw-skills-hub/skills/<group>/skill.json
git add coreclaw-skills-hub/skills/<group>/README.md
git add coreclaw-skills-hub/skills/<group>/skills/**
```

### 3. リリースタグを作成

```bash
# 単一スキル（グループと同じ名前）
git tag <group>/v0.2.0
git push origin <group>/v0.2.0

# ネストされたスキル（グループ内のスキル）
git tag <group>/<skill-name>/v0.2.0
git push origin <group>/<skill-name>/v0.2.0
```

### 4. GitHub Release を確認

タグ作成後、GitHub Actionsが自動的に以下を実行：
- スキルディレクトリをZIP化
- GitHub Releaseを作成
- registry.jsonを更新
- 変更をmainブランチにプッシュ

---

## ベストプラクティス

### 説明の書き方

✅ **良い例：**
```
"Assists researchers in composing high-quality academic papers with proper structure and citation formatting"
```

❌ **悪い例：**
```
"paper writing"
"tool for writing"
```

### バージョンの進め方

```
v0.1.0  -> v0.2.0  新機能追加時
v0.1.0  -> v0.1.1  バグ修正時
v0.9.0  -> v1.0.0  安定版リリース時
```

### ファイルサイズ

- `SKILL.md`: 簡潔に。複雑な場合は複数ファイルに分割
- `main.py`: 実装が大きい場合はモジュール化
- `source/`: オリジナルペイロード全体を保存
- `agent-skills-builder` は本体1500文字以内、サブスキル2000文字以内を維持

### 依存関係管理

- `requirements.txt` を用意（外部ライブラリが必要な場合）
- 依存関係のバージョンを固定
- Python >= 3.8 を推奨

### 言語の統一

- `skill.json` の `description`: **英語**
- `group.json` の `description`: **英語**
- `SKILL.md`: 日本語 または 英語（一貫性を保つ）
- `README.md`: 英語推奨

### CI/CD との連携

- `skill.json` は必須フィールドをすべて含める
- `entrypoint` で指定したファイルが存在することを確認
- `main` ブランチへのプッシュは自動検証される
- `group.json` の `count` はグループ内実数（本体 + サブスキル）と一致させる

---

## ハーネス最適化

**v0.2.0** より、マーケットプレースの全スキルに **ハーネスパフォーマンス最適化** が導入されています。これは [everything-claude-code](https://github.com/affaan-m/everything-claude-code) の Harness Performance System（v1.8.0）を参考にした構造化品質保証システムです。

### ハーネス最適化とは？

ハーネス最適化は、すべてのスキルの `SKILL.md` に標準化された品質保証ループを追加します。スキルの出力が生成されるだけでなく、**検証・妥当性確認・レポート** を経てから納品されることを保証します。

### 検証ループ（Verification Loop）

ハーネス最適化されたスキルは、`SKILL.md` に追加された以下の4フェーズサイクルに従います：

```
## Verification Loop

| フェーズ   | アクション                                    |
|-----------|---------------------------------------------|
| PLAN      | リクエストを解析し、実行パスを選択              |
| EXECUTE   | コアスキルロジックを実行                        |
| VERIFY    | 品質ゲートに対して出力を検証                    |
| REPORT    | 信頼度付きの構造化結果を返却                    |
```

### 品質ゲート（Quality Gates）

品質ゲートは VERIFY フェーズで評価される合否チェックポイントです。スキルタイプにより異なります：

| スキルタイプ       | 品質ゲートの例                                              |
|-------------------|------------------------------------------------------------|
| スイートルート      | オーケストレーションカバレッジ、サブスキル委任精度              |
| サブスキル         | ドメイン固有の出力検証、フォーマット準拠チェック                |
| スタンドアロンスキル | エンドツーエンドの出力正確性、完全性チェック                   |

### main.py のハーネスメタデータ

各 `main.py` にはランタイム内省用のハーネスメタデータが含まれます：

```python
SKILL_META = {
    "version": "v0.2.0",
    "harness": "coreclaw-v1",
    "capabilities": ["verification-loop", "quality-gates", "eval-checkpoints"],
    "quality_gates": {
        "min_confidence": 0.7,
        "require_verification": True,
        "output_format_check": True
    }
}
```

### 3種類のフッターバリアント

`SKILL.md` の検証ループフッターはスキルの役割により異なります：

1. **スイートルート** — オーケストレーション原則を強調：
   > 「スイートルートがリクエストを受信した場合、オーケストレーター経由で正しいサブスキルに委任しなければならない（MUST）」

2. **スタンドアロンスキル** — 単一スキルの完全性に焦点：
   > 「このスキルはエンドツーエンドで実行される。VERIFY フェーズで REPORT 前に出力の正確性を確認する」

3. **サブスキル** — 下流責任を明確化：
   > 「このサブスキルはスイートパイプライン内で実行される。VERIFY でドメイン固有の品質を確認してからオーケストレーターに返す」

### 新規スキルへのハーネス最適化適用

v0.2.0 以降で新規スキルを作成する場合、以下の手順を含めてください：

1. **SKILL.md** — 適切な検証ループフッターを末尾に追加（上記バリアント参照）
2. **skill.json** — `"version": "v0.2.0"` 以上を設定
3. **main.py** — ハーネス機能と品質ゲートを含む `SKILL_META` 辞書を追加
4. **source/SKILL.md** — ルートの `SKILL.md` の内容をミラーリング

### バッチ変換

既存スキルのアップグレードには `scripts/` 内のバッチ変換スクリプトを使用してください：

- `scripts/convert_scientist_v020.py` — Scientist グループ（195サブスキル）
- `scripts/convert_all_groups_v020.py` — その他全グループ（15グループ、63サブスキル）

これらのスクリプトは以下を処理します：
- フロントマター説明文とセクション見出しの日本語→英語翻訳
- 検証ループフッターの注入（3バリアント）
- `skill.json` のバージョンバンプ
- `main.py` へのハーネスメタデータ挿入
- `source/SKILL.md` の同期

---

## FAQ

### Q. スキルを更新する場合、バージョンを上げずに済む？

A. いいえ。registry に登録されるため、バージョンは必ず更新してください。タグ作成時に GitHub Actions が新しいバージョンを検出し、registry.json を更新します。

### Q. 複数のスキルをまとめてリリースできる？

A. 可能です。各スキルのタグを作成してプッシュすれば、GitHub Actions が順次処理します。

```bash
git tag scientist/scientific-writing/v0.2.0
git tag scientist/data-analysis/v0.1.0
git push origin --tags
```

### Q. ネストされたグループ（3階層以上）をサポートしている？

A. 現在のシステムは最大 2階層（グループ + スキル）をサポートしています。3階層以上が必要な場合は registry の設定を変更する必要があります。

### Q. source/ ディレクトリは必須？

A. いいえ。新規作成スキルは必須ではありません。既存のペイロードをインポートする際に、元のファイル構造を保存するために使用します。

---

## サポート

質問や問題がある場合は、リポジトリの Issues セクションで報告してください。
