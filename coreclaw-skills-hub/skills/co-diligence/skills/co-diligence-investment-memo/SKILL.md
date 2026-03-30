---
name: co-diligence-investment-memo
description: |
  Investment memo generation with thesis, evidence synthesis, risk summary, and Go/No-Go recommendation.
  Use when WRITING investment memos, synthesizing DD findings into recommendations,
  or generating decision packages for investment committees.
---

# Investment Memo

Investment recommendation with evidence synthesis.

## Use This Skill When

- Writing the final investment memo from DD findings.
- Synthesizing market, competitive, financial, and risk analyses.
- Generating Go / No-Go / Conditional recommendations.

## Workflow

1. Synthesize findings from all prior DD phases.
2. State investment thesis in 1-2 sentences.
3. Summarize key findings (market opportunity, competitive position, financial health, risks).
4. Present recommendation: **Go** / **No-Go** / **Conditional Go** (with specific conditions).
5. Define next steps if Go/Conditional (due dates, responsible parties).
6. Run quality checks.

## Deliverables

- `report.md`: complete investment memo.
- Reuse `assets/investment-memo-template.md` when producing standardized memos.

## Quality Gates

- [ ] Investment thesis stated clearly (1-2 sentences).
- [ ] Recommendation is explicit: Go / No-Go / Conditional (not ambiguous).
- [ ] Conditions for Go are specific, measurable, and time-bound.
- [ ] Critical/High risks from risk matrix are surfaced in executive summary.
- [ ] All prior DD phase outputs are referenced and synthesized.
- [ ] Document marked "DRAFT — CONFIDENTIAL".

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 「Conditional Go」の条件は SMART（Specific, Measurable, Achievable, Relevant, Time-bound）であること
- Risk Matrix で Critical リスクの緩和策が未定義の場合、Go を推奨してはならない
- エグゼクティブサマリーは全セクション完成後に書くこと
- 「投資しない理由がない」は Go の理由にならない。積極的な投資理由（thesis）を明記すること

## Validation Loop

1. 投資メモを生成
2. チェック: Thesis明確性、推奨の明示性、条件のSMART性、リスクサーフェス
3. 不合格なら修正
4. ユーザー承認後のみ完了 ⏸️
