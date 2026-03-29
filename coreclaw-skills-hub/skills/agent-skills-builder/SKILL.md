---
name: agent-skills-builder
description: |
  Builder skill that designs and generates Agent Skills compliant packages through user dialogue.
  Discovers the true objective behind surface-level requests, then designs,
  generates, validates, and distributes skill configurations for GitHub Copilot CLI and related runtimes.
---

# Agent Skills Builder v0.10.0

A builder that creates Agent Skills compliant packages through dialogue-based requirements discovery.

## Use This Skill When

- A user wants to create a new Agent Skill from an ambiguous or high-level request.
- The work requires structured requirements discovery before file generation.
- A single skill or suite collection must be scaffolded and validated.

## Local Resources

- Generate Agent Skills output only.
- Save generated outputs under `coreclaw-skills-hub/.artifacts/generated-skills/` and bundle a ZIP when requested.

## Required Inputs

- Skill or suite name and the user's surface request.
- Background problem, success criteria, constraints, and agreed true objective.
- Structure choice: single skill or suite collection.
- Optional suite profile and any required frontmatter or tooling constraints.

## Workflow

1. Ask exactly one question at a time until the surface request, background, success criteria, constraints, and true objective are clear.
2. Propose the smallest workable architecture: single skill or suite with orchestrator and specialized roles.
3. Generate Agent Skills compliant `SKILL.md` files, plus suite artifacts when the design requires them.
4. Validate naming, frontmatter, structure, and artifact completeness before packaging outputs.

## Deliverables

- Generated skill or suite files under `coreclaw-skills-hub/.artifacts/generated-skills/`.
- `orchestration.json` plus `agents/*.md` files when suite-style output is selected.
- `hooks/hooks.json`, `scripts/hooks/*.js`, `docs/harness-audit.md`, and `commands/*.md` harness scaffolds for suite-style output.
- Validation summary and generated file inventory.
- True objective summary and chosen architecture rationale.
- ZIP bundle path when bundling is requested.

## Quality Gates

- One-question-at-a-time dialogue is maintained until the true objective is confirmed.
- Every generated `SKILL.md` has valid frontmatter and a directory name matching `name`.
- Generated output remains Agent Skills compliant.
- Generated artifacts are saved to a workspace-visible location and validated before delivery.
- Suite-style output includes one orchestrator manifest, one execution agent manifest, and one sub-agent manifest per specialized role.
- Suite-style output can include hook, audit, and eval scaffolds with selectable harness enforcement profiles.

---

## Harness Optimization (v0.9.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Skill Building)

Before execution, define:
- [ ] **Target skill name**: valid kebab-case identifier
- [ ] **True objective**: confirmed by user (not just surface request)
- [ ] **Structure type**: single skill vs. suite-style with sub-agents
- [ ] **Completeness**: all required files identified

#### Pass Criteria
- `SKILL.md` includes `name` and `description` in YAML frontmatter
- Skill directory name matches the frontmatter `name`
- `SKILL.md` contains: instructions, examples, and edge cases
- Naming follows kebab-case convention
- Generated package saved to `coreclaw-skills-hub/.artifacts/generated-skills/`
- ZIP bundle contains all generated files
- Suite-style generation includes an orchestrator and at least one specialized sub-skill
- Default suite generation applies the selected suite profile when no explicit sub-skills are supplied
- Orchestrator contracts match the selected suite profile
- Suite-style generation emits an `orchestration.json` topology and `agents/*.md` manifests for orchestrator, agent, and sub-agent roles
- Suite-style generation emits hook, audit, and eval scaffolds unless explicitly disabled
- True objective documented and aligned with agent design

### Verification Loop

```
Phase 1: PLAN
  |-- Confirm true objective via 1-question dialogue
  |-- Determine structure type (single / suite-style)
  |-- List all files to generate
  +-- Estimate character counts against limits

Phase 2: EXECUTE
  |-- Generate SKILL.md with required frontmatter and usage guidance
  |-- Generate suite collection README, orchestration schema, and sub-agent files if suite-style
  |-- Apply selected suite profile roles when no sub-skills are specified
  |-- Generate profile-specific orchestrator contracts
  |-- Generate orchestrator, execution agent, and sub-agent manifests
  |-- Generate hooks, audit, and eval scaffolds for the selected harness profile
  |-- Save generated package to artifact-visible workspace path
  +-- Bundle into ZIP

Phase 3: VERIFY
  |-- Validate SKILL.md frontmatter (name and description)
  |-- Confirm directory name matches frontmatter name
  |-- Verify naming convention compliance
  |-- Confirm orchestrator structure exists for suite-style packages
  |-- Confirm orchestration schema and agent manifests exist for suite-style packages
  |-- Confirm hooks, audit, and eval scaffold files exist when harness scaffolding is enabled
  |-- Confirm generated files live under workspace-visible `.artifacts`
  |-- Cross-check true objective alignment
  +-- Test ZIP integrity

Phase 4: RECOVER (on failure)
  |-- Identify which file or field failed validation
  |-- Regenerate only the failed component
  |-- Re-summarize if character limit exceeded
  |-- Log fix as reusable pattern
  +-- If unrecoverable: deliver partial package with documented gaps

Phase 5: REPORT
  |-- Present generated file list to user
  |-- Show validation results
  |-- Provide artifact-visible save path
  |-- Provide ZIP download path
  |-- Suggest release tag format
  +-- Record true objective summary and proposal comparison
```

### Quality Gates

| Gate | Check | Required |
|------|-------|----------|
| G1 | `SKILL.md` has required frontmatter fields | MUST |
| G2 | Directory name matches frontmatter `name` | MUST |
| G3 | SKILL.md contains instructions, examples, and edge cases | MUST |
| G4 | Naming follows kebab-case convention | MUST |
| G5 | Generated files saved under workspace-visible `.artifacts` | MUST |
| G6 | ZIP bundle generated and non-empty when requested | MUST |
| G7 | True objective documented and user-confirmed | MUST |
| G8 | Suite-style packages include orchestrator sections and specialized sub-skills | MUST for suite-style |
| G9 | Default suite templates honor the selected suite profile when `subskills` are omitted | MUST for default suite mode |
| G10 | Orchestrator contracts match the selected suite profile | MUST for profile-based suite mode |
| G11 | Suite-style packages emit orchestrator/agent/sub-agent manifests plus `orchestration.json` | MUST for suite-style |
| G12 | Harness scaffold files are generated consistently with the selected harness profile | MUST when harness scaffolding is enabled |
| G13 | One-question-at-a-time dialogue maintained | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | File scaffolding, frontmatter generation, suite profile expansion, contract generation, ZIP bundling |
| Implementation | `standard` (sonnet-class) | SKILL.md writing, README generation, agent manifest generation, validation |
| Reasoning | `premium` (opus-class) | True objective discovery, architecture decisions, orchestration design, proposal comparison |

### Sub-Agent Orchestration

For suite-style skill packages, split generation into parallel agents:

```
Orchestrator (this skill)
|-- Agent 1: Requirements discovery and true objective articulation
|-- Agent 2: Skill architecture design and file structure planning
|-- Agent 3: File generation (SKILL.md, README.md, orchestration.json, suite artifacts)
+-- Agent 4: Validation, artifact save, ZIP bundling, and release preparation
```

### Token Optimization

- Use structured JSON for intermediate skill specifications (not prose)
- Generate files from templates rather than free-form writing
- Cache `docs/SKILLS_GUIDE.md` structure requirements (avoid re-reading)
- Compact dialogue history after true objective confirmation
- Prefer frontmatter-driven generation over ad-hoc document formatting

### Error Recovery Protocol

```python
def validate_skill_package(skill_dir):
    """Validate generated skill package against quality gates."""
    errors = []
    
  skill_md = skill_dir / "SKILL.md"
  if not skill_md.exists():
    errors.append("G1: SKILL.md missing")
    return errors

  text = skill_md.read_text()
  if not text.startswith("---\n"):
    errors.append("G1: missing YAML frontmatter")

  name_match = re.search(r'^name:\s+(.+)$', text, re.MULTILINE)
  if not name_match:
    errors.append("G1: frontmatter name missing")
  else:
    name = name_match.group(1).strip()
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
      errors.append("G4: name not kebab-case")
    if skill_dir.name != name:
      errors.append("G2: directory name does not match frontmatter name")
    
  if not re.search(r'^description:\s*', text, re.MULTILINE):
    errors.append("G1: frontmatter description missing")
    
    return errors
```
