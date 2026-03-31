---
name: co-sales-deep-research
description: |
  Deep market and competitive research with web_search, /research command, and MCP.
  Industry analysis, competitive intelligence, market sizing, and trend identification.
  Use when CONDUCTING market research, competitive deep dives, industry analysis,
  or gathering evidence for business cases.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research

Market and competitive deep research engine for sales intelligence.

## Use This Skill When

- Conducting market or industry research for account planning.
- Building competitive intelligence or gathering evidence for business cases.

## Research Tools (Priority Order)

1. `web_search` (built-in, always available) — focused queries, market data, news.
2. `/research` command (CLI interactive) — multi-faceted synthesis from many sources.
3. `deep-research` MCP (when configured) — full pipeline: Question → Subquestions → Search → Report.

## Workflow

1. Define research objective and scope.
2. Choose tool: `web_search` for targeted, `/research` for comprehensive, MCP for pipeline.
3. Execute research rounds (Think → Action → Report cycle).
4. Cross-validate key data with 2+ sources. Tag findings with source URLs and trust levels.
5. Save to `results/research-notes.md`.

## Deliverables

- `results/research-notes.md`: Findings with source attribution.

## Quality Gates

- [ ] 3+ trusted sources collected for key claims.
- [ ] Key data points cross-validated with 2+ sources.
- [ ] Single-source claims marked with ⚠️.
- [ ] All findings saved to files (not chat-only).
- [ ] Sources tagged with trust level (High / Medium / Low).

If any gate fails: identify the gap, conduct additional research rounds, and re-validate.

## Gotchas

- `web_search` は常に利用可能。MCP が未設定でも Web 検索は実行できる
- deep-research は市場・業界全体の調査。特定企業の情報は account-research を使うこと
- ソースの信頼度が「低」のデータは単独では使用しない。上位ソースで裏付けを取ること

## Validation Loop

1. リサーチラウンドを実行
2. ソース3件以上・交差検証・ファイル保存をチェック
3. 不合格なら追加ラウンド、全基準を満たしてから完了
