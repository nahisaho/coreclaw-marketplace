---
name: skill-scaffolder
description: >
  Generate Harness-optimized Agent Skill packages with full suite support.
  Creates AGENTS.md orchestrators, SKILL.md sub-skills, Custom Agents,
  copilot-instructions.md, .mcp.json, and assets/references/scripts directories.
  Use when creating a new skill suite from scratch, bootstrapping a skill folder,
  or generating any component of a Harness-optimized skill package.
metadata:
  author: coreclaw
  version: "2.0"
---

# Skill Scaffolder

Generate Harness-optimized Agent Skill packages — from single skills to full suites.

## Use This Skill When

- Creating a new Agent Skill suite from scratch.
- Bootstrapping a single skill with Harness patterns.
- Generating suite infrastructure (AGENTS.md, agents/, .mcp.json).

## Workflow

1. Determine package type:
   - **Single skill**: SKILL.md only
   - **Suite**: AGENTS.md + multiple SKILL.md + agents/ + copilot-instructions.md

2. For suites, generate in order:
   a. `group.json`, `skill.json`, `README.md`
   b. `AGENTS.md` (Orchestrator with WHEN/DO routing)
   c. `copilot-instructions.md` (suite-specific conventions)
   d. `agents/*.md` (Custom Agents with tool restrictions)
   e. `skills/<skill-name>/SKILL.md` (each sub-skill)
   f. `.mcp.json` (if external tools needed)

3. For each SKILL.md, include:
   - Frontmatter: `name`, `description` (+ `tu_tools` if MCP)
   - Body: Use This Skill When, Workflow, Deliverables, Quality Gates, Gotchas (3+), Validation Loop

4. Determine if sub-skills need supplementary directories:
   - `assets/` — when the skill produces templated outputs (reports, analyses)
   - `references/` — when detailed definitions exceed SKILL.md's 500-line budget
   - `scripts/` — when validation or transformation scripts are needed
   - Reuse templates from this skill's `assets/` directory

5. Add conditional references in SKILL.md:
   - ✅ `Read references/api-errors.md when API returns non-200 status`
   - ❌ `See references/ for details`

6. Self-validation (see Validation Loop)

## Supplementary Directory Decision Guide

| Condition | Action |
|-----------|--------|
| Skill produces reports with fixed structure | Create `assets/` with report templates |
| Reference content exceeds 100 lines | Move to `references/` with conditional refs |
| Validation needs executable checks | Create `scripts/` with validation code |
| Skill is self-contained and compact | No supplementary dirs needed |

## Output Templates

Reuse templates in this skill's `assets/` directory:
- `assets/agents-md-template.md` — AGENTS.md orchestrator template
- `assets/skill-md-template.md` — SKILL.md sub-skill template
- `assets/copilot-instructions-template.md` — copilot-instructions.md template
- Refer to `references/suite-checklist.md` when validating completeness

## Gotchas

- `description` に「Use when」を含めないと、エージェントがスキルを発見できない死蔵スキルになる
- フォルダ名と `name` フィールドが不一致だと CI バリデーションに失敗する
- SKILL.md が500行を超えるとコンテキストウィンドウを圧迫する。超える場合は references/ に分離する
- references/ を無条件参照にすると Context Efficiency が劣化する。必ず条件付き参照にする
- スイート構成のルート Orchestrator は AGENTS.md にすること（SKILL.md ではない）。デプロイ先は `.github/AGENTS.md`
- assets/ のテンプレートは「構造」を提供するもの。具体的なデータは含めない

## Validation Loop

1. 生成したパッケージを確認
2. **構造チェック**:
   - [ ] `name` フィールドが命名規則に従い、フォルダ名と一致
   - [ ] `description` が「何をするか」+「Use when」の2部構成
   - [ ] スイート構成なら AGENTS.md が存在する
   - [ ] 本文500行以内（超過分は references/ に分離済み）
   - [ ] Gotchas セクションが3項目以上
   - [ ] 検証ループまたはチェックリストが含まれる
   - [ ] references/ への参照は全て条件付き
   - [ ] assets/ のテンプレートが SKILL.md から参照されている
3. 不合格項目がある場合: 修正して再チェック
4. 構造チェック合格後、**Harness 7軸チェック**を実施:

### Post-Generation Harness Check（必須）

生成完了後、以下の 7軸チェックを全スキルに対して実行する。
`harness-auditor` スキルの基準に従い、各軸を 0–3 でスコアリング。

| # | 軸 | 合格基準 | チェック内容 |
|---|-----|---------|------------|
| 1 | Tool Coverage | ≥1 | description に起動条件あり、スキル間キーワード重複なし |
| 2 | Context Efficiency | ≥1 | SKILL.md ≤500行、条件付き参照のみ、assets活用 |
| 3 | Quality Gates | ≥1 | 検証ループ + チェックリスト + 失敗時リカバリ |
| 4 | Memory Persistence | ≥1 | Gotchas 3項目以上（具体的）、learning-capture考慮 |
| 5 | Eval Coverage | ≥1 | 出力検証基準が明示、CI統合ポイントあり |
| 6 | Security Guardrails | ≥1 | 禁止事項明示、データ取り扱いルール |
| 7 | Cost Efficiency | ≥1 | 冗長説明なし、デフォルト明示、選択肢最小化 |

**合格条件**: 全7軸でスコア1以上（総合 7/21 以上）
**推奨水準**: 総合 14/21 以上（Intermediate）

5. いずれかの軸がスコア0の場合:
   - 該当軸の改善を実施（description → `description-optimizer`、Gotchas → `gotchas-curator`）
   - 改善後に再スコアリング
6. 全軸スコア1以上を確認してから完了とする
