# Registry と CI/CD ワークフロー

このドキュメントでは、coreclaw-skills-hubのregistryシステムと自動化ワークフローについて説明します。

## 目次

1. [Registry 構造](#registry-構造)
2. [検証ワークフロー](#検証ワークフロー)
3. [リリースワークフロー](#リリースワークフロー)
4. [トラブルシューティング](#トラブルシューティング)

---

## Registry 構造

### registry.json の形式

`coreclaw-skills-hub/registry.json`は、すべてのリリース済みスキルのメタデータとURLを管理します。

```json
{
  "generated_at": "2026-03-27T12:34:56+00:00",
  "skills": {
    "scientist": {
      "name": "Scientist",
      "description": "Skills for scientists...",
      "icon": "🔬",
      "isGroup": true,
      "skillCount": 196
    },
    "scientist/scientific-academic-writing": {
      "name": "scientific-academic-writing",
      "version": "v0.1.0",
      "entrypoint": "main.py",
      "metadataSource": "skill.json",
      "description": "Assists researchers in composing...",
      "latest": "v0.1.0",
      "versions": [
        {
          "version": "v0.1.0",
          "url": "https://github.com/.../releases/download/scientist/scientific-academic-writing/v0.1.0/skill.zip",
          "released_at": "2026-03-27T10:30:00+00:00"
        }
      ]
    },
    "consultant": {
      "name": "Consultant",
      "description": "General consultant skills...",
      "icon": "💼",
      "isGroup": true,
      "skillCount": 1
    }
  }
}
```

### フィールド説明

#### グループエントリ（`isGroup: true`）

| フィールド | 説明 |
|-----------|------|
| `name` | グループの表示名 |
| `description` | グループの説明 |
| `icon` | グループを表す絵文字 |
| `isGroup` | グループかどうかを示すフラグ |
| `skillCount` | グループ内のスキル数 |

#### スキルエントリ

| フィールド | 説明 |
|-----------|------|
| `name` | スキルの一意な名前 |
| `version` | 現在のバージョン |
| `description` | スキルの説明 |
| `entrypoint` | 互換メタデータがある場合の実行ファイル |
| `metadataSource` | `SKILL.md` または `skill.json` |
| `latest` | 最新バージョン番号 |
| `versions` | バージョン履歴（URL とリリース日時を含む） |

---

## 検証ワークフロー

### 実行タイミング

- **トリガー**: `skills/**`パスへの変更を含むPull Request
- **アクション**: PRのvalidationチェック実行

### ワークフロー処理

```yaml
PR 作成 → 変更検出 → SKILL.md と互換メタデータを検証 → registry プレビュー生成 → artifact upload → レビュー
```

### 検証項目

1. **SKILL.md の存在**: 各スキルディレクトリに正式な `SKILL.md` があるか
2. **frontmatter 整合性**: `name` と `description` があり、`name` がディレクトリ名と一致するか
3. **互換メタデータ**: `skill.json` がある場合だけ `name`, `version`, `description`, `entrypoint` を検証
4. **entrypoint の存在**: `skill.json` がある場合だけ `entrypoint` 先が存在するか

### Registry プレビュー

PRでは`registry.preview.json`が自動生成され、artifactとしてアップロードされます。

**用途:**
- PRレビュー時にスキルメタデータを確認
- registry.jsonの最終形を事前に確認
- branch を汚さずに検証

**確認方法:**
1. PR の「Checks」タブを開く
2. 「Details」から「Artifacts」を選択
3. `registry-preview` をダウンロード

---

## リリースワークフロー

### 実行タイミング

- **トリガー**: タグの作成とプッシュ
- **タグ形式**: `<skill-path>/v<major>.<minor>.<patch>`

### タグ例

```bash
# 単一スキル（グループ = スキル）
git tag consultant/v0.1.0

# ネストされたスキル（グループ内のスキル）
git tag scientist/scientific-academic-writing/v0.2.0
```

### ワークフロー処理

```
タグ作成
  ↓
スキルメタデータ検証
  ↓
スキルディレクトリを ZIP 化
  ↓
GitHub Release を作成
  ↓
registry.json を更新
  ↓
registry.json を main にプッシュ
```

### 出力

#### GitHub Release

リリースページに以下が作成されます：

- **タイトル**: `[<skill-path>] Release v<version>`
- **説明**: `SKILL.md` frontmatter の description
- **アセット**: `skill.zip` （スキル全体をZIP化）

**URL 例：**
```
https://github.com/nahisaho/coreclaw-marketplace/releases/download/scientist/scientific-academic-writing/v0.1.0/skill.zip
```

#### registry.json の更新

```json
{
  "scientist/scientific-academic-writing": {
    "latest": "v0.2.0",
    "versions": [
      {
        "version": "v0.2.0",
        "url": "https://github.com/.../releases/download/scientist/scientific-academic-writing/v0.2.0/skill.zip",
        "released_at": "2026-03-27T15:45:00+00:00"
      },
      {
        "version": "v0.1.0",
        "url": "https://github.com/.../releases/download/scientist/scientific-academic-writing/v0.1.0/skill.zip",
        "released_at": "2026-03-26T10:30:00+00:00"
      }
    ]
  }
}
```

---

## トラブルシューティング

### 検証エラー

#### エラー: `missing SKILL.md`

**原因**: スキルディレクトリに正式なスキル定義がない

**解決方法**:
```bash
# スキルディレクトリを確認
ls coreclaw-skills-hub/skills/<group>/<skill-name>/SKILL.md

# ない場合は作成
cat > coreclaw-skills-hub/skills/<group>/<skill-name>/SKILL.md << 'EOF'
---
name: your-skill
description: |
  Description
---

# Your Skill
EOF
```

#### エラー: `Invalid version format`

**原因**: バージョンが `vX.Y.Z` 形式でない

**解決方法**:
```json
{
  "version": "v0.1.0"  // ✅ 正しい形式
}
```

❌ 間違った形式：
- `0.1.0` （v がない）
- `v1` （マイナー、パッチがない）
- `1.0.0-beta` （プレリリースタグは非サポート）

#### エラー: `entrypoint file not found`

**原因**: `skill.json` の `entrypoint` で指定したファイルが存在しない

**解決方法**:
```bash
# ファイルが存在するか確認
ls coreclaw-skills-hub/skills/<group>/<skill-name>/main.py

# ない場合は作成
cat > coreclaw-skills-hub/skills/<group>/<skill-name>/main.py << 'EOF'
#!/usr/bin/env python3
"""Skill entry point."""

def main():
    print("Skill execution")

if __name__ == "__main__":
    main()
EOF
```

### リリースエラー

#### エラー: `Release creation failed`

**原因**: タグ形式が不正

**解決方法**:
```bash
# 正しいタグ形式確認
git tag -l | grep "scientist/scientific"

# 削除（必要な場合）
git tag -d incorrect-tag
git push origin :refs/tags/incorrect-tag

# 正しいタグを作成
git tag scientist/scientific-academic-writing/v0.2.0
git push origin scientist/scientific-academic-writing/v0.2.0
```

#### エラー: `GitHub Actions failure`

**確認方法**:
1. GitHub の「Actions」タブを開く
2. 失敗したワークフローをクリック
3. ログを確認

**一般的な原因と解決**:

| エラー | 原因 | 解決 |
|------|------|------|
| `Invalid regex` | タグ形式が不正 | タグを再作成 |
| `ZIP creation failed` | ファイルが見つからない | ファイルパスを確認 |
| `API rate limit` | GitHub API の制限に達した | 少し待機してから再試行 |

---

## ベストプラクティス

### リリース前のチェックリスト

- [ ] `skill.json` が正しいフォーマットか確認
- [ ] 必須フィールド（name, version, description, entrypoint）が入っているか
- [ ] バージョン番号がセマンティック バージョニングに従っているか
- [ ] `main.py` が存在し、実行可能か
- [ ] SKILL.md または README.md が存在するか
- [ ] 新しいバージョンが main にマージされているか

### タグ作成コマンド

```bash
# 完全なフロー例
git checkout main
git pull origin main

# バージョン更新（例）
# coreclaw-skills-hub/skills/scientist/scientific-academic-writing/skill.json の version を v0.2.0 に更新

git add coreclaw-skills-hub/skills/scientist/scientific-academic-writing/skill.json
git commit -m "bump: version v0.2.0 for scientific-academic-writing"
git push origin main

# リリースタグ作成
git tag scientist/scientific-academic-writing/v0.2.0
git push origin scientist/scientific-academic-writing/v0.2.0

# ステータス確認
git tag -l scientist/scientific-academic-writing/v0.2.0
```

### 複数スキル同時リリース

```bash
git tag scientist/skill1/v0.2.0
git tag scientist/skill2/v0.1.0
git push origin --tags
```

---

## 参考リンク

- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
