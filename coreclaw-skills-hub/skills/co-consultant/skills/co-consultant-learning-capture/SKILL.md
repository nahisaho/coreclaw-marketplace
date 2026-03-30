---
name: co-consultant-learning-capture
description: |
  Consulting learning capture and knowledge persistence. Records engagement insights,
  framework pitfalls, and client-specific patterns from completed consulting tasks.
  Use when FINISHING a consulting engagement, discovering a framework limitation,
  resolving an analysis error, or recording lessons for future engagements.
---

# Learning Capture

Record consulting learnings and maintain Gotchas for Memory Persistence.

## Use This Skill When

- Completing a consulting engagement and recording lessons.
- Discovering a framework limitation or edge case.
- Resolving an analysis error that others should avoid.
- Updating Gotchas in related co-consultant skills.

## Workflow

1. Identify learning event:
   - Framework misapplication that was corrected
   - Source that proved unreliable
   - Client feedback that changed the approach
   - MECE gap discovered during review

2. Structure the learning:
   - **WHAT**: Specific situation
   - **WHY**: Impact and frequency
   - **HOW**: Prevention or best practice
   - **WHERE**: Which co-consultant skill to update

3. Generate Gotcha entry (1-2 lines, concrete, actionable).

4. Update target skill's Gotchas section.

5. Record in `logs/learnings-log.jsonl`.

## Deliverables

- Updated Gotchas in target skill's SKILL.md.
- `logs/learnings-log.jsonl`: timestamped learning record.

## Quality Gates

- [ ] Learning is specific (not generic advice).
- [ ] Gotcha entry is 1-2 lines and actionable.
- [ ] No duplicate with existing Gotchas.
- [ ] Target skill remains under 500 lines after addition.

If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- 学びの記録は「ミス発生直後」に行うこと。時間が経つと詳細を忘れる
- 「フレームワークをもっと勉強しよう」のような汎用的な教訓は価値が低い。具体的な失敗と対策を書く
- 同じ学びを複数スキルに重複記載しない。最も関連性の高い1箇所に書く

## Validation Loop

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py` on modified skills after Gotchas update.

1. Gotcha エントリを生成
2. チェック:
   - 具体的な状況・対策が含まれるか
   - 既存 Gotchas と重複していないか
   - 追記後のスキルが 500 行以内か
3. 不合格なら修正
4. 合格後に追記実行
