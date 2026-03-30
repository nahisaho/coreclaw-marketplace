---
name: co-compliance-learning-capture
description: |
  Compliance learning capture and knowledge persistence. Records audit insights,
  control mapping patterns, and regulatory interpretation lessons.
  Use when FINISHING a compliance engagement, discovering a control mapping pitfall,
  or recording lessons for future compliance work.
---

# Learning Capture (Compliance)

Record compliance learnings for Memory Persistence.

## Use This Skill When

- Completing a compliance assessment.
- Discovering a framework interpretation issue.
- Updating Gotchas in related co-compliance skills.

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

- [ ] Learning is specific.
- [ ] Gotcha is 1-2 lines and actionable.
- [ ] No duplicate.
- [ ] Target skill ≤ 500 lines.

If any gate fails: fix and re-validate.

## Gotchas

- コンプライアンス固有の知見（フレームワーク解釈、監査指摘パターン）はこのスイートに記録する
- 学びの記録は監査完了直後に行うこと

## Validation Loop

1. Gotcha 生成 → 2. チェック → 3. 合格後に追記
