---
name: co-educationalist-learning-capture
description: |
  Education learning capture and pedagogy knowledge persistence.
  Records instructional insights, theory application lessons, and curriculum pitfalls.
  Use when FINISHING an education task, discovering a pedagogy limitation,
  or recording lessons for future instructional design sessions.
---

# Learning Capture

Record education learnings for Memory Persistence.

## Use This Skill When

- Completing an education task and recording lessons.
- Discovering a theory application pitfall.
- Updating Gotchas in related co-educationalist skills.

## Workflow

1. Identify learning event.
2. Structure: WHAT, WHY, HOW, WHERE (which skill to update).
3. Generate Gotcha entry (1-2 lines, concrete, actionable).
4. Update target skill's Gotchas section.

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py` on modified skills after Gotchas update.

## Deliverables

- Updated Gotchas in target skill's SKILL.md.
- `logs/learnings-log.jsonl`: timestamped learning record.

## Quality Gates

- [ ] Learning is specific (not generic advice).
- [ ] Gotcha entry is 1-2 lines and actionable.
- [ ] No duplicate with existing Gotchas.
- [ ] Target skill remains under 500 lines.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 学びの記録は「ミス発生直後」に行うこと
- 教育固有の知見はこのスイートに、汎用知見は別スイートに記録する

## Validation Loop

1. Gotcha エントリを生成
2. チェック: 具体的か、重複なしか、500行以内か
3. 合格後に追記実行
