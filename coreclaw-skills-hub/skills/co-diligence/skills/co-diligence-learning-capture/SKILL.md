---
name: co-diligence-learning-capture
description: |
  DD learning capture and knowledge persistence. Records deal insights, red flag patterns,
  and diligence methodology lessons from completed DD engagements.
  Use when FINISHING a DD engagement, discovering a risk assessment pitfall,
  or recording lessons for future due diligence work.
---

# Learning Capture

Record DD learnings for Memory Persistence.

## Use This Skill When

- Completing a DD engagement and recording lessons.
- Discovering a financial analysis pitfall.
- Updating Gotchas in related co-diligence skills.

## Workflow

1. Identify learning event.
2. Structure: WHAT, WHY, HOW, WHERE.
3. Generate Gotcha entry (1-2 lines, concrete).
4. Update target skill's Gotchas.

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py` on modified skills.

## Deliverables

- Updated Gotchas in target SKILL.md.
- `logs/learnings-log.jsonl`.

## Quality Gates

- [ ] Learning is specific (not generic).
- [ ] Gotcha is 1-2 lines and actionable.
- [ ] No duplicate.
- [ ] Target skill ≤500 lines.

If any gate fails: fix and re-validate.

## Gotchas

- DD固有の知見（財務基準の違い、業界固有のリスク）はこのスイートに記録する
- 学びの記録はエンゲージメント完了直後に行うこと

## Validation Loop

1. Gotcha 生成 → 2. チェック → 3. 合格後に追記
