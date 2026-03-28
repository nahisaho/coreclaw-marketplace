---
name: agent-skills-builder
description: |
  Builder skill that designs and generates Agent Skills compliant packages through user dialogue.
  Discovers the true objective behind surface-level requests, then designs,
  generates, validates, and distributes skill configurations for GitHub Copilot CLI and related runtimes.
---

# Agent Skills Builder v0.9.0

A builder that creates Agent Skills compliant packages through dialogue-based requirements discovery.

## Purpose

- Standardize skill creation for Agent Skills compatible runtimes
- Deep exploration of user needs through structured dialogue
- Identify the true objective behind surface-level requests
- Concretize requirements through proactive proposals
- Auto-generate a minimal Agent Skills template when file contents are not explicitly supplied
- Auto-generate suite-style collections with an orchestrator and profile-based specialized skills
- Generate profile-specific orchestrator contracts for input, output, quality, and fallback handling
- Auto-generate sub-agent configurations when needed
- Ensure required `SKILL.md` frontmatter and kebab-case naming
- Preserve legacy CoreClaw scaffolds only when `target_format` requests them
- Maintain documentation quality standards
- Improve deliverable distribution via ZIP packaging and artifact-visible saves

## Interaction Policy

- Elicit background, purpose, and constraints through user questions
- Always conduct one-question-at-a-time interviews (never bundle multiple questions)
- Confirm the previous answer before proceeding to the next question
- Sequentially confirm: surface request → background problem → success criteria → constraints
- Articulate the true objective in writing and obtain user agreement
- Proactively propose multiple options when requirements are ambiguous
- Show pros, cons, and recommendation rationale concisely for each proposal
- When sub-agents are deemed necessary, present reasoning and architecture for agreement
- Finalize specifications in a form the user can choose from

## Expected Workflow

1. Confirm the surface request (what the user initially wants) via one-question dialogue
2. Sequentially confirm background problem, success criteria, and constraints
3. Articulate the true objective in writing and obtain user agreement
4. Decompose agent responsibilities needed to achieve the true objective; propose single or sub-agent architecture
5. Determine structure type (single skill or suite collection)
6. Generate Agent Skills compliant `SKILL.md` files by default
7. When suite mode is selected, generate the orchestrator skill and specialized sub-skills
8. When `subskills` are omitted, select a suite profile and generate its default role templates
9. Generate the orchestrator's contracts and fallback policy from the selected suite profile
10. Validate naming and required frontmatter consistency
11. Save generated skills under `coreclaw-skills-hub/.artifacts/generated-skills/`
12. Bundle deliverables into a downloadable ZIP when requested
13. Only generate `skill.json`, `main.py`, and `source/SKILL.md` when `target_format` is `coreclaw`

## Input

- Skill name
- User's surface request
- Background problem, success criteria, constraints
- Agreed-upon true objective
- Sub-agent requirement (number of roles and responsibility split when needed)
- Required input/output formats
- Target format (`agent-skills` by default, `coreclaw` for legacy packages)
- Optional frontmatter fields: `license`, `compatibility`, `metadata`, `allowed_tools`
- Optional suite profile (`ops`, `research`, `consulting`)
- Operational conditions (deadline, quality requirements, dependencies)

## Output

- Generated Agent Skill package
- Sub-agent (sub-skill) groups when required
- Suite collection with orchestrator and specialized skill directories when requested
- True objective summary (with diff from surface request)
- Proposal comparison (selected vs. alternatives)
- Validation results
- Artifact-visible save path
- Generated template file list
- Downloadable ZIP deliverable (with path)
- Legacy CoreClaw package when explicitly requested

## Quality Criteria

- `SKILL.md` contains required frontmatter fields
- Skill directory name matches the frontmatter `name`
- Descriptions are clear and concise
- Compliant with Agent Skills conventions (naming, structure)
- Requirements traceable to dialogue log
- One-question-at-a-time dialogue order maintained
- True objective articulated and aligned with designed agent responsibilities
- ZIP deliverable generated with all key files included
- Generated package saved under workspace-visible `.artifacts`
- Legacy CoreClaw files are only generated when explicitly requested

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
- [ ] **Target format**: Agent Skills default or legacy CoreClaw override
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
- True objective documented and aligned with agent design
- Legacy CoreClaw files appear only when `target_format` is `coreclaw`

### Verification Loop

```
Phase 1: PLAN
  |-- Confirm true objective via 1-question dialogue
  |-- Determine structure type (single / suite-style)
  |-- List all files to generate
  +-- Estimate character counts against limits

Phase 2: EXECUTE
  |-- Generate SKILL.md with required frontmatter and usage guidance
  |-- Generate suite collection README and sub-agent files if suite-style
  |-- Apply selected suite profile roles when no sub-skills are specified
  |-- Generate profile-specific orchestrator contracts
  |-- Generate legacy CoreClaw scaffolds only when explicitly requested
  |-- Save generated package to artifact-visible workspace path
  +-- Bundle into ZIP

Phase 3: VERIFY
  |-- Validate SKILL.md frontmatter (name and description)
  |-- Confirm directory name matches frontmatter name
  |-- Verify naming convention compliance
  |-- Confirm orchestrator structure exists for suite-style packages
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
| G11 | Legacy CoreClaw files only appear when explicitly requested | MUST |
| G12 | One-question-at-a-time dialogue maintained | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | File scaffolding, frontmatter generation, suite profile expansion, contract generation, ZIP bundling |
| Implementation | `standard` (sonnet-class) | SKILL.md writing, README generation, validation |
| Reasoning | `premium` (opus-class) | True objective discovery, architecture decisions, proposal comparison |

### Sub-Agent Orchestration

For suite-style skill packages, split generation into parallel agents:

```
Orchestrator (this skill)
|-- Agent 1: Requirements discovery and true objective articulation
|-- Agent 2: Skill architecture design and file structure planning
|-- Agent 3: File generation (SKILL.md, README.md, optional legacy compatibility files)
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
    
    # G1: skill.json schema
    skill_json = skill_dir / "skill.json"
    if not skill_json.exists():
        errors.append("G1: skill.json missing")
    else:
        data = json.loads(skill_json.read_text())
        for field in ["name", "version", "description", "entrypoint"]:
            if field not in data:
                errors.append(f"G1: skill.json missing '{field}'")
    
    # G2: entrypoint exists
    if skill_json.exists():
        ep = data.get("entrypoint", "main.py")
        if not (skill_dir / ep).exists():
            errors.append(f"G2: entrypoint '{ep}' not found")
    
    # G4: naming convention
    if not re.match(r'^[a-z][a-z0-9-]*$', data.get("name", "")):
        errors.append("G4: name not kebab-case")
    
    # G5: semver
    if not re.match(r'^v\d+\.\d+\.\d+$', data.get("version", "")):
        errors.append("G5: version not semver vX.Y.Z")
    
    return errors
```
