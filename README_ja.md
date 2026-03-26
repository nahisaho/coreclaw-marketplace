# coreclaw-marketplace

Coreclaw Skillsを配布するためのマーケットプレース用リポジトリです。

このリポジトリには以下が含まれます。

- `coreclaw-skills-hub/`: パッケージ化されたSkillsマーケットプレース本体
- `docs/`: スキル作成者向け・運用者向けドキュメント
- `LICENSE`: リポジトリ全体のMITライセンス

## 概要

マーケットプレースのSkillsは `coreclaw-skills-hub/skills/` 配下で管理します。

- グループ単体のSkillは `skills/<group>/`
- グループ内の個別Skillは `skills/<group>/<skill-name>/`
- 各SkillはGitタグでリリースし、GitHub Releaseのassetとして配布
- `registry.json` はリリースタグを契機にGitHub Actionsが更新

## リポジトリ構成

```text
.
├── coreclaw-skills-hub/
│   ├── skills/
│   ├── registry.json
│   └── .github/
├── docs/
│   ├── README.md
│   ├── README_ja.md
│   ├── SKILLS_GUIDE.md
│   ├── SKILLS_GUIDE_ja.md
│   ├── REGISTRY_AND_CI_CD.md
│   └── REGISTRY_AND_CI_CD_ja.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## ドキュメント

英語版:

- [docs/README.md](docs/README.md)
- [docs/SKILLS_GUIDE.md](docs/SKILLS_GUIDE.md)
- [docs/REGISTRY_AND_CI_CD.md](docs/REGISTRY_AND_CI_CD.md)

日本語版:

- [docs/README_ja.md](docs/README_ja.md)
- [docs/SKILLS_GUIDE_ja.md](docs/SKILLS_GUIDE_ja.md)
- [docs/REGISTRY_AND_CI_CD_ja.md](docs/REGISTRY_AND_CI_CD_ja.md)

## クイックスタート

### 新しいSkillを追加する

1. `coreclaw-skills-hub/skills/` 配下にSkillディレクトリを作成
2. `skill.json`、`main.py`、`SKILL.md`、`README.md` を追加
3. 必要に応じてグループ用の `group.json` を追加または更新
4. `main` にコミットしてpush

詳細手順: [docs/SKILLS_GUIDE_ja.md](docs/SKILLS_GUIDE_ja.md)

### Skillをリリースする

1. `skill.json` のversionを更新
2. version更新をコミットしてpush
3. `scientist/scientific-academic-writing/v0.2.0` のようなタグを作成してpush

詳細: [docs/REGISTRY_AND_CI_CD_ja.md](docs/REGISTRY_AND_CI_CD_ja.md)

## 現在の状態

- `nahisaho/coreclaw` からSkillsをインポート済み
- ネストされたSkillパスをCI/CDでサポート
- PR検証ではregistry preview artifactを生成
- リリースタグでasset公開と `registry.json` 更新を実行
- Skillグループ説明は `group.json` で英語管理

## ライセンス

このリポジトリはMIT Licenseで提供されています。詳細は [LICENSE](LICENSE) を参照してください。

## English Version

英語版トップガイドは [README.md](README.md) を参照してください。