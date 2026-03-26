# Skills 作成ガイド

このガイドでは、coreclaw-skills-hub マーケットプレースにスキルを登録・公開するための手順とベストプラクティスを説明します。

## 目次

1. [ディレクトリ構造](#ディレクトリ構造)
2. [skill.json スキーマ](#skilljson-スキーマ)
3. [group.json スキーマ](#groupjson-スキーマ)
4. [ファイル要件](#ファイル要件)
5. [命名規則](#命名規則)
6. [スキル作成手順](#スキル作成手順)
7. [リリース手順](#リリース手順)
8. [ベストプラクティス](#ベストプラクティス)

---

## ディレクトリ構造

### グループレベルのスキル（単一スキル）

```
coreclaw-skills-hub/skills/
└── <group-name>/
    ├── group.json                    # グループメタデータ
    ├── SKILL.md                      # スキルドキュメント（根ルート）
    ├── skill.json                    # スキルメタデータ
    ├── main.py                       # エントリポイント（マーケットプレース用）
    ├── README.md                     # スキル説明（マーケットプレース用）
    └── source/                       # 元のペイロード
        ├── SKILL.md                  # 元のスキルドキュメント
        └── [その他のオリジナルファイル]
```

例：`consultant/`, `educationalist/`, `general-assistant/`

### ネストされたグループ内のスキル（複数スキル）

```
coreclaw-skills-hub/skills/
└── <group-name>/
    ├── group.json                    # グループメタデータ
    ├── <skill-name-1>/
    │   ├── SKILL.md
    │   ├── skill.json
    │   ├── main.py
    │   ├── README.md
    │   └── source/
    │       ├── SKILL.md
    │       └── [その他のファイル]
    └── <skill-name-2>/
        ├── SKILL.md
        ├── skill.json
        ├── main.py
        ├── README.md
        └── source/
            ├── SKILL.md
            └── [その他のファイル]
```

例：`scientist/scientific-academic-writing/`, `scientist/scientific-active-learning/`

---

## skill.json スキーマ

### 最小限の例

```json
{
  "name": "my-skill-name",
  "version": "v0.1.0",
  "description": "Brief description of what this skill does",
  "entrypoint": "main.py"
}
```

### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `name` | string | ✅ | スキルの一意な名前。ケバブケース（kebab-case）で記述。EXドメイン内で重複しない必要があります。 |
| `version` | string | ✅ | セマンティック バージョン（Semantic Versioning）形式：`vX.Y.Z`。例：`v0.1.0`, `v1.2.3` |
| `description` | string | ✅ | スキルの簡潔な説明（英語推奨）。1-2 文で概要を説明。 |
| `entrypoint` | string | ✅ | マーケットプレースから実行されるメインファイル。通常は `main.py` |
| `author` | string | ❌ | スキル作成者の名前またはメールアドレス |
| `license` | string | ❌ | ライセンスタイプ。例：`MIT`, `Apache-2.0` |
| `keywords` | array | ❌ | スキルを分類するキーワード。例：`["research", "writing", "academic"]` |

### 拡張例

```json
{
  "name": "scientific-academic-writing",
  "version": "v0.2.0",
  "description": "Assists researchers in composing high-quality academic papers with proper structure and citation formatting",
  "entrypoint": "main.py",
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
🤖  一般アシスタント (general-assistant)
📊  データサイエンティスト向け
🔧  エンジニア向け
💡  イノベーション向け
```

---

## ファイル要件

### SKILL.md（スキルドキュメント）

スキルの詳細なドキュメント。根ルートと `source/` の両方に配置。

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

### main.py（エントリポイント）

マーケットプレースから実行される Python スクリプト。

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

### 1. ディレクトリを作成

```bash
mkdir -p coreclaw-skills-hub/skills/<group>/<skill-name>
cd coreclaw-skills-hub/skills/<group>/<skill-name>
```

### 2. skill.json を作成

```json
{
  "name": "<skill-name>",
  "version": "v0.1.0",
  "description": "Your skill description here",
  "entrypoint": "main.py"
}
```

### 3. main.py を作成

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

### 4. SKILL.md を作成

スキルのドキュメントを作成：

```markdown
# [Skill Name]

## 概要
説明

## 使用方法
使用方法

...
```

### 5. README.md を作成

マーケットプレース向けの説明：

```markdown
# [Skill Name]

Brief description and features
```

### 6. source/ ディレクトリを作成（オプション）

元のペイロードを保存：

```bash
mkdir source
cp SKILL.md source/
# 他のオリジナルファイルをコピー
```

### 7. 変更をコミット

```bash
git add <group>/<skill-name>/
git commit -m "feat: add <skill-name> skill"
git push origin main
```

---

## リリース手順

### 1. skill.json のバージョンを更新

```json
{
  "name": "my-skill",
  "version": "v0.2.0",  // <- Update this
  "description": "...",
  "entrypoint": "main.py"
}
```

### 2. 変更をコミット

```bash
git add coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json
git commit -m "bump: version v0.2.0 for <skill-name>"
git push origin main
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

タグ作成後、GitHub Actions が自動的に以下を実行：
- スキルディレクトリをZIP化
- GitHub Release を作成
- registry.json を更新
- 変更を main ブランチにプッシュ

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
