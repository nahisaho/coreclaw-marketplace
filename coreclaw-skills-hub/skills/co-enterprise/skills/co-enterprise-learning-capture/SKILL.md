---
name: co-enterprise-learning-capture
description: |
  Enterprise transformation learning capture and knowledge persistence.
  Records transformation insights, initiative pitfalls, and methodology lessons.
  Use when FINISHING a transformation engagement or recording lessons learned.
---

# Learning Capture (Enterprise)

Record transformation learnings for Memory Persistence.

## Workflow

1. Identify learning event.
2. Structure: WHAT, WHY, HOW, WHERE.
3. Generate Gotcha entry.
4. Update target skill's Gotchas.

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py` on modified skills.

## Deliverables

- Updated Gotchas + `logs/learnings-log.jsonl`.

## Quality Gates

- [ ] Specific, actionable, no duplicate, ≤500 lines.

If any gate fails: fix and re-validate.

## Gotchas

- 変革プロジェクト固有の知見はこのスイートに記録する
- 学びの記録はエンゲージメント完了直後に行うこと

## Validation Loop

1. Gotcha 生成 → 2. チェック → 3. 合格後に追記
