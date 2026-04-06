# co-educationalist

Harness-optimized education partner suite with 7 specialized sub-skills, 2 Custom Agents, and full Orchestrator routing.

- **Version**: v0.1.0
- **Sub-skills**: 7
- **Custom Agents**: 2 (curriculum-lead, pedagogy-reviewer)
- **Education Theories**: 175 (via theory-lookup + theories.db)
- **Curriculum Standards**: 2,469 items (小中高 学習指導要領 via curriculum.db)

## Prerequisites

- Node.js >= 20.0.0

## Database Setup

教育理論DB・学習指導要領DBは [SHIDEN](https://github.com/nahisaho/SHIDEN) npm パッケージから取得します。

```bash
cd coreclaw-skills-hub/skills/co-educationalist
bash scripts/setup-databases.sh
```

これにより `data/` ディレクトリに以下がインストールされます:

| ファイル | 内容 | サイズ |
|---------|------|--------|
| `theories.db` | 175件の教育理論 (SQLite FTS5 trigram) | ~2MB |
| `theories.json` | 教育理論データ (JSON) | ~500KB |
| `relations.json` | 理論間の関連グラフ | ~100KB |
| `curriculum.db` | 学習指導要領 小中高 2,469項目 (SQLite FTS5) | ~140MB |

### CLI での利用

```bash
# 教育理論の検索
npx shiden theories search "構成主義"
npx shiden theories categories

# 学習指導要領の検索
npx shiden curriculum search "プログラミング"
npx shiden curriculum subject 算数
npx shiden curriculum grade "第3学年"
npx shiden curriculum stats
```

### シンボリックリンクモード（省スペース）

```bash
bash scripts/setup-databases.sh --link
```

## Deploy Structure

```
<project>/.github/
├── AGENTS.md              ← co-educationalist/AGENTS.md
├── copilot-instructions.md
├── agents/
│   ├── curriculum-lead.md
│   └── pedagogy-reviewer.md
└── skills/
    ├── co-educationalist-lesson-planning/SKILL.md
    ├── co-educationalist-materials/SKILL.md
    ├── co-educationalist-assessment/SKILL.md
    ├── co-educationalist-feedback/SKILL.md
    ├── co-educationalist-guidance/SKILL.md
    ├── co-educationalist-theory-lookup/SKILL.md
    └── co-educationalist-learning-capture/SKILL.md
```
