---
name: co-consultant-mck-deep-research
description: |
  Iterative deep research with Think→Action→Report cycle for McKinsey-style engagements.
  Web search via web_search tool, /research command, and MCP integration.
  Bilingual search, source quality assessment, and cross-validation.
  Use when COLLECTING information, verifying market data, conducting competitive analysis,
  or gathering evidence for MCK framework application.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research (MCK)

Hypothesis-driven iterative research for McKinsey-style consulting.

## Use This Skill When

- Collecting market, competitive, or technology intelligence.
- Verifying business data from multiple sources.
- Gathering evidence before applying MCK frameworks.

## Research Tools (Priority Order)

### 1. `web_search` tool (Built-in — Always Available)
Targeted web queries. Always run bilingual (JP + EN):
```
web_search("Japan digital transformation market size 2025")
web_search("McKinsey MCK framework case study")
```
Best for: focused data points, market statistics, recent news, company data.

### 2. `/research` command (CLI — Interactive Sessions)
Comprehensive multi-source investigation:
```
/research What is the competitive landscape for [target market]?
```
Best for: complex research questions needing automated sub-question decomposition.

### 3. `deep-research` MCP (When Configured)
Full pipeline: elaborate → subquestions → search → analyze → report.

## Workflow

### Think Phase
- Analyze knowledge gaps against the objective.
- Generate hypotheses.
- Choose tool: `web_search` for targeted, `/research` for comprehensive, MCP for pipeline.

### Action Phase
| Action | Tool | When |
|--------|------|------|
| SEARCH | `web_search` (bilingual JP+EN) | Need specific data points |
| RESEARCH | `/research` command | Need comprehensive multi-source investigation |
| VISIT | `web_fetch` | Need full page content from URL |
| VERIFY | `web_search` (2nd query) | Cross-validate key numbers/facts |
| COMPLETE | — | All completion criteria met |

- **Bilingual**: Always search in both Japanese and English.
- **Academic priority**: Prefer `.ac.jp`, `.edu`, `.gov` domains.
- **Cross-validation**: Verify key data with 2+ sources.

### Report Phase
- Update findings after each round.
- Tag each fact with source URL and trust level.
- Mark single-source findings with ⚠️.

## Deliverables

- `results/research-notes.md`: findings with source attribution.
- `results/source-registry.md`: all sources with trust ratings.

## Quality Gates

- [ ] 3+ trusted sources collected.
- [ ] Weighted trust average ≥ 60%.
- [ ] Key hypotheses verified or refuted.
- [ ] Single-source claims marked with ⚠️.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- `web_search` は常に利用可能。MCP が設定されていなくても Web 検索は実行できる
- 検索は日英両方で行うこと。英語のみだと日本市場固有のデータを見落とす
- `/research` コマンドは CLI インタラクティブセッションでのみ使用可能。自動化では `web_search` を使う
- McKinseyのレポート・出版物は信頼度「高」として扱うが、自社バイアスに注意すること
- 収集データは各ラウンド後にファイルに保存。コンパクションで消失する
- Phase間の引き継ぎは必ず `results/research-notes.md` に保存してからハンドオフすること

## Validation Loop

1. リサーチラウンドを実行
2. チェック: 3+ソース、交差検証済み、⚠️タグ付き
3. 不合格なら追加ラウンド
4. 全基準を満たしてからCOMPLETE
