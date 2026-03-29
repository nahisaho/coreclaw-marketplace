# Documentation - coreclaw-skills-hub

coreclaw-skills-hubマーケットプレースの完全なドキュメンテーション。

## 📚 ドキュメント一覧

### [Skills 作成ガイド](./SKILLS_GUIDE.md) 

スキルを作成・登録するための完全なガイド。

**含まれる内容：**
- ディレクトリ構造とファイル配置
- `SKILL.md` 正式メタデータと任意の `skill.json` 互換スキーマ
- 命名規則とバージョン管理
- スキル作成の手順
- ベストプラクティス

**対象者:** スキル開発者、新しいスキルを追加したい人

---

### [Registry と CI/CD ワークフロー](./REGISTRY_AND_CI_CD.md)

系統の仕組みと自動化ワークフローの詳細。

**含まれる内容：**
- Registry（registry.json）の構造
- PR検証ワークフロー（validation.yml）
- リリースワークフロー（release.yml）
- GitHub Release自動生成
- トラブルシューティング

**対象者:** マーケットプレース管理者、ワークフロー理解のための技術者

---

## 🚀 クイックスタート

### 1. 新しいスキルを作成

```bash
# ディレクトリ作成
mkdir -p coreclaw-skills-hub/skills/<group>/<skill-name>
cd coreclaw-skills-hub/skills/<group>/<skill-name>

# SKILL.md 作成
cat > SKILL.md << 'EOF'
---
name: my-skill
description: |
    Description
---

# My Skill

## 概要
スキルの説明

## 使用方法
使用方法
EOF

# 互換メタデータが必要な場合のみ作成
cat > skill.json << 'EOF'
{
    "name": "my-skill",
    "version": "v0.1.0",
    "description": "Description",
    "entrypoint": "main.py"
}
EOF

cat > main.py << 'EOF'
#!/usr/bin/env python3
def main():
        print("Skill execution")

if __name__ == "__main__":
        main()
EOF

# コミット
git add .
git commit -m "feat: add my-skill"
git push origin main
```

詳細は [Skills 作成ガイド](./SKILLS_GUIDE.md) を参照。

### 2. スキルをリリース

```bash
# 互換メタデータがある場合は skill.json のバージョン更新
# version: "v0.1.0" → "v0.2.0"

git add coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json
git commit -m "bump: version v0.2.0"
git push origin main

# リリースタグ作成
git tag <group>/<skill-name>/v0.2.0
git push origin <group>/<skill-name>/v0.2.0
```

詳細は [Registry と CI/CD ワークフロー](./REGISTRY_AND_CI_CD.md#リリースワークフロー) を参照。

---

## 📋 ファイル構造

```
coreclaw-skills-hub/
├── skills/
│   ├── scientist/
│   │   ├── group.json                                  # グループメタデータ
│   │   ├── scientific-academic-writing/
│   │   │   ├── SKILL.md                               # 正式なスキル定義
│   │   │   ├── skill.json                             # 任意の互換メタデータ
│   │   │   ├── main.py                                # 任意の互換エントリポイント
│   │   │   ├── SKILL.md
│   │   │   ├── README.md
│   │   │   └── [その他のアセット]
│   │   └── [...その他のスキル...]
│   ├── consultant/
│   └── [...その他のグループ...]
├── registry.json                                       # リリース済みスキルのメタデータ
├── .github/
│   ├── scripts/
│   │   ├── generate_registry_preview.py               # PR 用プレビュー生成
│   │   ├── validate_skill.py                          # スキル検証
│   │   └── update_registry.py                         # registry 更新
│   └── workflows/
│       ├── validate.yml                               # PR 検証ワークフロー
│       └── release.yml                                # リリースワークフロー
└── docs/
    ├── README.md                                       # このファイル
    ├── SKILLS_GUIDE.md                                # スキル作成ガイド
    └── REGISTRY_AND_CI_CD.md                          # Registry と CI/CD
```

---

## 🔑 重要な概念

### セマンティック バージョニング

バージョン形式：`v<MAJOR>.<MINOR>.<PATCH>`

```
v0.1.0  初期バージョン
v0.2.0  新機能追加 (minor version up)
v0.2.1  バグ修正 (patch version up)
v1.0.0  安定版リリース (major version up)
```

参考：[semver.org](https://semver.org/)

### タグ命名規則

```bash
# 単一スキル（グループ = スキル）
<group>/v<version>

# ネストされたスキル（グループ内のスキル）
<group>/<skill-name>/v<version>
```

例：
```bash
scientist/scientific-academic-writing/v0.2.0
consultant/v0.1.0
```

### Registry の更新タイミング

- **自動更新**: タグのプッシュ時のみ（GitHub Actionsによる）
- **手動更新**: 不可（自動ワークフロー以外では変更不可）
- **PRでは**: プレビュー生成のみ（registry.json変更なし）

---

## 🛠 技術スタック

- **スクリプト言語**: Python 3.8+
- **バージョン管理**: Git
- **自動化**: GitHub Actions
- **Registry フォーマット**: JSON
- **スキル実装言語**: Python（推奨）

---

## 📞 サポート

### よくある質問（FAQ）

Q: **複数スキルを同時にリリースしたい**
A: 各タグを作成してまとめてプッシュできます。
```bash
git tag group/skill1/v0.1.0 group/skill2/v0.1.0
git push origin --tags
```

Q: **タグを削除したい**
A:
```bash
git tag -d tag-name
git push origin :refs/tags/tag-name
```

Q: **Registry プレビューはどこで見られる？**
A: PRのArtifactsセクションから `registry-preview` をダウンロード。

### 問題報告

問題や質問が発生した場合：
1. GitHub Issuesで報告
2. 詳細なエラーログを含める
3. 関連するファイル（skill.jsonなど）を添付

---

## 📝 ライセンス

MIT License

---

**最終更新**: 2026-03-27  
**作成者**: coreclaw-skills-hub  
**バージョン**: 1.0.0
