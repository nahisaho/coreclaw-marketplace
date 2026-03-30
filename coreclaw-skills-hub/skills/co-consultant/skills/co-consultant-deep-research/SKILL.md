---
name: co-consultant-deep-research
description: |
  Iterative deep research with Think→Action→Report cycle. Web search via web_search tool,
  /research command, and MCP. Bilingual search, source quality assessment, and cross-validation.
  Use when COLLECTING information from multiple sources, verifying market data,
  conducting competitive analysis, or gathering evidence for business decisions.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research

Iterative hypothesis-driven research engine with Think→Action→Report cycle.

## Use This Skill When

- Collecting market, competitive, or technology intelligence.
- Verifying business data from multiple sources.
- Conducting web-based investigation for consulting deliverables.

## Research Tools (Priority Order)

Use the following tools in priority order based on availability and task needs:

### 1. `web_search` tool (Built-in — Always Available)
The agent's built-in web search tool. Use for targeted queries:
```
web_search("Japan SaaS market size 2025 CAGR")
web_search("McKinsey digital transformation ROI study")
```
- **Best for**: Focused factual queries, market data, statistics, recent news.
- **Bilingual**: Run each query in both Japanese and English for comprehensive coverage.

### 2. `/research` command (CLI — Interactive Sessions)
GitHub Copilot CLI's deep research command for comprehensive investigations:
```
/research What is the competitive landscape for AI-powered CRM in Japan?
```
- **Best for**: Multi-faceted research questions requiring synthesis from many sources.
- **Combines**: GitHub search + web sources + structured analysis.
- **Use when**: The research question is complex and benefits from automated sub-question decomposition.

### 3. `deep-research` MCP (When Configured)
Structured research via MCP server for full-pipeline research:
1. Question Elaboration → refine scope
2. Subquestion Generation → decompose into 3-5 sub-questions
3. Web Search → collect from authoritative sources
4. Content Analysis → evaluate source quality
5. Report Generation → structured findings with citations

## Workflow

### Think Phase
- Analyze knowledge gaps against the true objective.
- Generate hypotheses about likely conclusions.
- Choose tool: `web_search` for targeted queries, `/research` for comprehensive, MCP for pipeline.
- Determine next action: SEARCH / VISIT / VERIFY / COMPLETE.

### Action Phase
| Action | Tool | When |
|--------|------|------|
| SEARCH | `web_search` (bilingual JP+EN) | Need specific data points |
| RESEARCH | `/research` command | Need comprehensive multi-source investigation |
| VISIT | `web_fetch` | Need full page content from a URL |
| VERIFY | `web_search` (2nd query) | Cross-validate key numbers/facts |
| COMPLETE | — | All completion criteria met |

- **Bilingual search**: Always search in both Japanese and English.
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
- [ ] Key hypotheses are verified or refuted.
- [ ] Single-source claims marked with ⚠️.
- [ ] Results saved to files (not chat-only).

If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- `web_search` は常に利用可能。MCP が設定されていなくても Web 検索は実行できる
- 検索は日英両方で行うこと。英語のみだと日本市場固有のデータ（官公庁白書、国内調査）を見落とす
- `/research` コマンドは CLI インタラクティブセッションでのみ使用可能。自動化パイプラインでは `web_search` を使う
- ソースの信頼度が「低」のデータ（ブログ、SNS）は単独では使用しない。必ず上位ソースで裏付けを取る
- 収集データは各ラウンド後にファイルに保存すること。コンパクションで中間結果が消失する
- Phase間の引き継ぎは必ず `results/research-notes.md` に保存してからハンドオフすること

## Validation Loop

1. リサーチラウンドを実行
2. チェック:
   - 3件以上の信頼できるソースがあるか
   - 重要な数値が交差検証されているか
   - 単一ソースの主張に ⚠️ が付いているか
   - 結果がファイルに保存されているか
3. 不合格なら追加ラウンドを実行
4. 全基準を満たしてからCOMPLETE
