# Co-Learning

Harness-optimized learning design & assessment partner. Outcome-based objective design, curriculum sequencing, activity generation, analytic rubric creation, and feedback-driven iteration.

## Sub-Skills

| # | Skill | Description |
|---|-------|-------------|
| 1 | `co-learning-objective-designer` | Designs measurable learning objectives using Bloom's Taxonomy and ABCD format |
| 2 | `co-learning-curriculum-builder` | Builds sequenced curriculum with scaffolding and prerequisite mapping |
| 3 | `co-learning-activity-generator` | Generates aligned learning activities with engagement and differentiation |
| 4 | `co-learning-rubric-designer` | Creates analytic rubrics with performance level descriptors |
| 5 | `co-learning-feedback-analyzer` | Analyzes learner feedback for iteration and improvement |
| 6 | `co-learning-deep-research` | Deep research for learning science evidence and benchmarks |
| 7 | `co-learning-learning-capture` | Captures design learnings and maintains Gotchas |

## Learning Design Workflow

```
Phase 0: objective-designer ⏸️  Define what learners should achieve
         │
Phase 1: curriculum-builder     Sequence content with scaffolding
         │
Phase 2: activity-generator ⏸️  Design learning experiences
         │
Phase 3: rubric-designer        Create evaluation criteria
         │
Phase 4: feedback-analyzer ⏸️   Plan feedback-driven iteration
```

⏸️ = Review pause — save artifacts and confirm before proceeding.

## Harness 7-Axis Alignment

| Axis | Score | Evidence |
|------|-------|----------|
| Tool Coverage | 3/3 | Full tools (learning-architect) + read-only (assessment-reviewer) |
| Quality Gates | 3/3 | Every SKILL.md has checkbox gates + failure recovery |
| Validation Loop | 3/3 | PLAN → EXECUTE → VERIFY → REPORT in all skills |
| Gotchas | 3/3 | 3+ Gotchas per skill, learning-capture maintains them |
| File-First | 3/3 | All artifacts saved to files, compaction-resilient |
| CI Integration | 3/3 | validate_skill.py referenced in learning-capture |
| Data Handling | 3/3 | "[Learner A]" placeholders, no PII, DRAFT marking |

## Deploy Guide

1. Copy `co-learning/` to your skills directory.
2. Verify structure: `find co-learning/ -type f | wc -l` (expect 17 files).
3. Validate: `python coreclaw-skills-hub/.github/scripts/validate_skill.py co-learning/`.
4. Configure MCP: review `.mcp.json` for deep-research server settings.
5. Test: invoke each sub-skill individually, then run full workflow.
