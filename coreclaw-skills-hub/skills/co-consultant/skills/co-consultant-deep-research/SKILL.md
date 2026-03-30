---
name: co-consultant-deep-research
description: |
  Iterative deep research with Think→Action→Report cycle. Bilingual search,
  source quality assessment, cross-validation, and hallucination prevention.
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

## MCP Integration

Use `deep-research` MCP when available for structured research:
1. Question Elaboration → refine research scope
2. Subquestion Generation → decompose into 3-5 sub-questions
3. Web Search → collect from authoritative sources
4. Content Analysis → evaluate source quality
5. Report Generation → structured findings with citations

Fall back to the built-in Think→Action→Report cycle when MCP is unavailable.

## Workflow (Built-in)

### Think Phase
- Analyze knowledge gaps against the true objective.
- Generate hypotheses about likely conclusions.
- Determine next action: SEARCH / VISIT / VERIFY / COMPLETE.

### Action Phase
| Action | When | Criteria |
|--------|------|----------|
| SEARCH | Need new information | Large knowledge gap |
| VISIT | Need page details | Promising URL found |
| VERIFY | Need cross-validation | Important numbers/facts |
| COMPLETE | Sufficient evidence | All criteria met |

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

- 検索は日英両方で行うこと。英語のみだと日本市場固有のデータ（官公庁白書、国内調査）を見落とす
- ソースの信頼度が「低」のデータ（ブログ、SNS）は単独では使用しない。必ず上位ソースで裏付けを取る
- 「十分な情報が集まった」の判断を急がないこと。完了基準（3+ソース、信頼度60%+）を満たしてからCOMPLETEにする
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

## Available Tools (MCP)

> Use `deep-research` MCP server for structured research when available.
> Falls back to built-in Think→Action→Report cycle when MCP is unavailable.

| Source | Tool | Description |
|--------|------|-------------|
| Deep Research MCP | `elaborate_question` | Refine research scope |
| Deep Research MCP | `generate_subquestions` | Decompose into sub-questions |
| Deep Research MCP | `web_search` | Search authoritative sources |
| Deep Research MCP | `analyze_content` | Evaluate source quality |
| Deep Research MCP | `generate_report` | Structured findings report |
