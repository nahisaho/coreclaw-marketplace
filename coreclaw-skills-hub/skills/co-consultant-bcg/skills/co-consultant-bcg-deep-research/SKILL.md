---
name: co-consultant-bcg-deep-research
description: |
  Iterative deep research with Think→Action→Report cycle for BCG-style engagements.
  Bilingual search, source quality assessment, and cross-validation.
  Use when COLLECTING information, verifying market data, conducting competitive analysis,
  or gathering evidence for BCG framework application.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research (BCG)

Hypothesis-driven iterative research for BCG-style consulting.

## Use This Skill When

- Collecting market, competitive, or technology intelligence.
- Verifying business data from multiple sources.
- Gathering evidence before applying BCG frameworks.

## MCP Integration

Use `deep-research` MCP when available. Fall back to Think→Action→Report cycle.

## Workflow

1. Think: Analyze knowledge gaps, generate hypotheses.
2. Action: SEARCH (bilingual) / VISIT / VERIFY / COMPLETE.
3. Report: Update findings with source URLs and trust levels.
4. Repeat until completion criteria met.

## Deliverables

- `results/research-notes.md`: findings with source attribution.
- `results/source-registry.md`: all sources with trust ratings.

## Quality Gates

- [ ] 3+ trusted sources collected.
- [ ] Weighted trust average ≥ 60%.
- [ ] Key hypotheses verified or refuted.
- [ ] Single-source claims marked with ⚠️.


If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- 検索は日英両方で行うこと。英語のみだと日本市場固有のデータを見落とす
- BCGのレポート・出版物は信頼度「高」として扱うが、自社バイアスに注意すること
- 収集データは各ラウンド後にファイルに保存。コンパクションで消失する
- Phase間の引き継ぎは必ず `results/research-notes.md` に保存してからハンドオフすること

## Validation Loop

1. リサーチラウンドを実行
2. チェック: 3+ソース、交差検証済み、⚠️タグ付き
3. 不合格なら追加ラウンド
4. 全基準を満たしてからCOMPLETE

## Available Tools (MCP)

> Use `deep-research` MCP server when available.

| Source | Tool | Description |
|--------|------|-------------|
| Deep Research MCP | `elaborate_question` | Refine research scope |
| Deep Research MCP | `generate_subquestions` | Decompose into sub-questions |
| Deep Research MCP | `web_search` | Search authoritative sources |
