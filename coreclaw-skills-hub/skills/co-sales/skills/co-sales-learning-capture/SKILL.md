---
name: co-sales-learning-capture
description: |
  Sales learning capture and knowledge persistence. Records deal insights,
  methodology pitfalls, and account-specific patterns from completed sales activities.
  Use when FINISHING a deal phase, discovering a methodology limitation,
  resolving a sales process error, or recording lessons for future deals.
---

# Learning Capture

Record sales learnings and maintain Gotchas for Memory Persistence.

## Use This Skill When

- Completing a deal phase and recording lessons.
- Discovering a methodology limitation or edge case.
- Resolving a sales process error that others should avoid.
- Updating Gotchas in related co-sales skills.

## Workflow

1. Identify learning event (methodology misapplication, failed objection response, mapping gap, outdated intel).
2. Structure: **WHAT** (situation) → **WHY** (impact) → **HOW** (prevention) → **WHERE** (target skill).
3. Generate Gotcha entry (1-2 lines, concrete, actionable).
4. Update target skill's Gotchas section.
5. Record in `logs/learnings-log.jsonl`.

## Deliverables

- Updated Gotchas in target skill's SKILL.md.
- `logs/learnings-log.jsonl`: Timestamped learning record.

## Quality Gates

- [ ] Learning is specific (not generic advice).
- [ ] Gotcha entry is 1-2 lines and actionable.
- [ ] No duplicate with existing Gotchas.
- [ ] Target skill remains under 100 lines after addition.

If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- 学びの記録は「失敗直後」に行うこと。時間が経つと詳細を忘れる
- 「もっと準備しよう」のような汎用的な教訓は価値が低い。具体的な失敗と対策を書く
- 同じ学びを複数スキルに重複記載しない。最も関連性の高い1箇所に書く

## Validation Loop

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py` on modified skills after update.

1. Gotcha エントリを生成し、具体性・重複・行数上限をチェック
2. 不合格なら修正、合格後に追記実行
