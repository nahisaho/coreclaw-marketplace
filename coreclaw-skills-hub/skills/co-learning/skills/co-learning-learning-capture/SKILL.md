---
name: co-learning-learning-capture
description: |
  Learning capture and knowledge persistence skill. Records instructional design
  insights, edge cases, and design playbook updates from completed tasks.
  Use when FINISHING a learning design task, discovering a design pitfall,
  resolving an alignment error, or updating Gotchas for future sessions.
---

# Learning Capture

Learning design insights, design pitfalls, and Gotchas maintenance.

## Use This Skill When

- Completing a learning design task and recording lessons learned.
- Discovering a design pitfall or alignment edge case.
- Resolving an error that future designers should avoid.
- Updating Gotchas in related co-learning skills.

## Workflow

1. Identify learning event (misalignment, Bloom's mismatch, rubric gap, unexpected outcome).
2. Structure: **WHAT** (situation) → **WHY** (impact) → **HOW** (prevention) → **WHERE** (target skill).
3. Generate 1–2 line Gotcha entry with specific criteria. Avoid generic advice.
4. Update target skill's Gotchas section.
5. Record in `logs/learnings-log.jsonl`.

## Deliverables

- Updated Gotchas in target skill's SKILL.md.
- `logs/learnings-log.jsonl`: timestamped learning record.

## Quality Gates

- [ ] Learning is specific (not generic advice).
- [ ] Gotcha entry is 1–2 lines and actionable.
- [ ] No duplicate with existing Gotchas.
- [ ] Target skill remains under 60 lines after addition.

If any gate fails: identify the issue, fix, and re-validate.

## CI Validation

Run `python coreclaw-skills-hub/.github/scripts/validate_skill.py <skill-dir>` after updates.

## Gotchas

- 学習の記録はタスク完了直後に行うこと。セッション終了後は詳細が失われる
- 汎用的なアドバイス（「もっとテストする」）は価値がない。プロジェクト固有の具体的な知見を記録すること
- 1つのスキルに Gotchas が10項目を超えたらカテゴリ分けまたは分割を検討すること

## Validation Loop

1. Generate Gotcha entry
2. Check: specific and actionable, no duplicates, skill stays under 60 lines
3. If any check fails → revise entry
4. Execute update after validation passes
