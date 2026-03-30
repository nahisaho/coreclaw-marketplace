---
name: co-growth-learning-capture
description: |
  Growth learning capture and knowledge persistence skill. Records experiment
  insights, edge cases, and growth playbook updates from completed tasks.
  Use when FINISHING a growth task, discovering a growth pitfall,
  resolving an analysis error, or updating Gotchas for future sessions.
---

# Learning Capture

Growth learnings, experiment insights, and Gotchas maintenance.

## Use This Skill When

- Completing a growth task and recording lessons learned.
- Discovering a growth pitfall or experiment edge case.
- Resolving an analysis error that others should avoid.
- Updating Gotchas in related co-growth skills.

## Workflow

1. Identify learning event (incorrect assumption, adjusted boundary, statistical pitfall, unexpected behavior).
2. Structure: **WHAT** (situation) → **WHY** (impact) → **HOW** (prevention) → **WHERE** (target skill).
3. Generate 1–2 line Gotcha entry with specific thresholds or criteria. Avoid generic advice.
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

- Record learnings immediately after discovery. Details fade quickly after session ends.
- Generic advice ("test more") has no value. Write project-specific, concrete findings.
- Gotchas exceeding 10 items in a single skill should be categorized or split.

## Validation Loop

1. Generate Gotcha entry
2. Check: specific and actionable, no duplicates, skill stays under 60 lines
3. If any check fails → revise entry
4. Execute update after validation passes
