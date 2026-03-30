---
name: educationalist
description: |
  AI assistant skill for educators. Built with reference to the SHIDEN project,
  featuring 10 specialized sub-skills for lesson planning, material creation,
  assessment design, individualized instruction, feedback generation,
  student guidance, and meta-prompt generation. Provides practical educational
  support grounded in 175 education theories and curriculum guidelines.
---

# Teaching Assistant

AI assistant skill for educators. Built with reference to the SHIDEN project, featuring 10 specialized sub-skills for lesson planning, material creation, assessment design, individualized instruction, feedback generation, student guidance, and meta-prompt generation. Provides practical educational support grounded in 175 education theories and curriculum guidelines.

## Use This Skill When

- An education workflow needs lesson planning, materials, assessment, guidance, or feedback support.
- Multiple education sub-skills or theory lookups must be coordinated.
- Outputs must be grounded in curriculum guidance and saved as reusable artifacts.

## Local Resources

- `prompts/`: content-generation flows for meta-prompting, lessons, materials, assessment, individual support, feedback, and guidance.
- `skills/`: nested Agent Skills including `orchestrator/SKILL.md`, `theory-lookup/SKILL.md`, and `context-manager/SKILL.md`.
- `data/`: education reference data including `theories.db`, `theories.json`, `relations.json`, and `curriculum.db`.
- Use `curriculum.db` for curriculum lookup instead of scanning curriculum markdown files.

## Required Inputs

- Educational objective, learner profile, subject, level, and delivery context.
- Available source material, curriculum constraints, and time or format requirements.
- Required outputs, review audience, and evidence expectations.

## Workflow

1. Confirm scope, evidence path, and the artifact set to save.
2. Route through the orchestrator or local helpers only when they materially improve the current task.
3. Save analyses, intermediate outputs, and recommendations to files instead of leaving results in chat.
4. Verify assumptions, traceability, and recommendation quality before finalizing conclusions.
5. Append skill selection, handoff I/O, and file writes to `logs/process-log.jsonl` when the execution harness requires trace logging.

## Deliverables

- `report.md`: objective, learner context, method, outputs, and file inventory.
- `results/`: lesson plans, rubrics, guidance outputs, or structured analysis artifacts.
- `figures/`: English-only charts or visuals when needed for instructional artifacts.
- `data/`: processed source material when transformation occurs.

## Quality Gates

- The selected prompt or helper matches the educational objective and learner context.
- Theory, curriculum assumptions, and constraints are explicit and traceable.
- Final outputs are saved as files and usable without chat context.
- `report.md` and, when used, `logs/process-log.jsonl` reference generated artifacts.
