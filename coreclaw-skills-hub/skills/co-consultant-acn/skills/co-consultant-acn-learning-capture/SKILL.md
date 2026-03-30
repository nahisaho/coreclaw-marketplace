---
name: co-consultant-acn-learning-capture
description: |
  Consulting learning capture for Accenture-style engagements.
  Records framework insights, engagement patterns, and methodology lessons.
  Use when FINISHING a ACN engagement, discovering a framework limitation,
  or recording lessons for future Accenture-style consulting sessions.
---

# Learning Capture (ACN)

Record Accenture-style consulting learnings for Memory Persistence.

## Use This Skill When

- Completing a ACN consulting engagement.
- Discovering a ACN framework limitation or edge case.
- Recording lessons for future Accenture-style engagements.

## Workflow

1. Identify learning event (framework misapplication, unreliable source, client feedback).
2. Structure: WHAT, WHY, HOW, WHERE (which skill to update).
3. Generate Gotcha entry (1-2 lines, concrete, actionable).
4. Update target skill's Gotchas section.

## Deliverables

- Updated Gotchas in target skill's SKILL.md.
- `logs/learnings-log.jsonl`: timestamped learning record.

## Quality Gates

- [ ] Learning is specific (not generic advice).
- [ ] Gotcha entry is 1-2 lines and actionable.
- [ ] No duplicate with existing Gotchas.


If any gate fails: identify the specific failing check, fix the issue, and re-validate before proceeding.

## Gotchas

- 学びの記録は「ミス発生直後」に行うこと。時間が経つと詳細を忘れる
- ACN固有の知見と汎用的な知見を区別すること。ACN固有の知見はこのスイートのスキルに、汎用知見はco-consultantに記録する

## Validation Loop

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py` on modified skills after Gotchas update.

1. Gotcha エントリを生成
2. チェック: 具体的か、重複なしか、500行以内か
3. 合格後に追記実行
