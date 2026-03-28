# agent-skills-builder

Builds CoreClaw skill packages from requirements using `docs/SKILLS_GUIDE.md`-compliant structures, minimal auto-generated templates, profile-based suite-style group scaffolding, profile-specific orchestrator contracts, and artifact-visible ZIP outputs.

## Features

- Dialogue-driven requirement discovery with users
- Enforces one-question-at-a-time interviews with users
- Discovers the user's true objective behind the initial request
- Proactive proposal generation to surface hidden needs
- Creates complete skill package structures aligned to `docs/SKILLS_GUIDE.md`
- Auto-generates a minimal 5-file skill scaffold when explicit file contents are not provided
- Auto-generates suite-style group packages with `group.json`, a root skill, an orchestrator, and profile-specific specialized sub-skill templates
- Switches orchestrator Input Contract, Output Contract, Quality Gates, and Fallback Policy by suite profile
- Optionally scaffolds sub-agents (sub-skills) when complexity requires role separation
- Generates valid `skill.json`, `README.md`, and `SKILL.md`
- Applies naming/versioning conventions
- Performs pre-release validation checks
- Saves generated deliverables under `coreclaw-skills-hub/.artifacts/generated-skills/`
- Bundles generated deliverables into ZIP for download
- Produces release tag suggestions
- Enforces authoring limits (main skill <= 1500 chars, sub-skills <= 2000 chars)

## Quick Start

```bash
python main.py
```

## Artifact Output

Generated skills are saved to a workspace-visible location so they can be surfaced in Artifacts:

- Default directory: `coreclaw-skills-hub/.artifacts/generated-skills/<skill-name>/`
- ZIP bundle: `coreclaw-skills-hub/.artifacts/generated-skills/<skill-name>.zip`
- If `output_dir` points outside the workspace, the builder falls back to the artifact-visible default path

When `skill_name` and a small set of metadata are provided, the builder auto-generates these files if they are missing:

- `skill.json`
- `main.py`
- `README.md`
- `SKILL.md`
- `source/SKILL.md`

When suite-style input is provided, the builder can also auto-generate:

- `group.json`
- root suite files in the group directory
- `<group>-orchestrator/` with the required orchestrator sections
- specialized sub-skill directories with their own 5-file scaffolds

If no explicit `subskills` are provided, the builder chooses a preset from `suite_profile` and generates role-based sub-skills automatically.

Supported presets:

- `ops`: `intake`, `execution`, `reporting`
- `research`: `intake`, `evidence-synthesis`, `report-assembly`
- `consulting`: `problem-structuring`, `analysis`, `executive-storyline`

Each preset also changes the generated orchestrator sections:

- `Input Contract`
- `Output Contract`
- `Quality Gates`
- `Fallback Policy`

If `suite_profile` is omitted, the default preset is `ops`.

Example default `ops` output:

- `<group>-intake`
- `<group>-execution`
- `<group>-reporting`

## ZIP Bundle Example

Create a downloadable zip from generated artifacts and let the builder scaffold the files:

```bash
python - <<'PY'
from main import run

result = run({
	"skill_name": "agent-skills-builder-demo",
	"description": "Demonstrates artifact-visible scaffold generation.",
	"true_objective": "Provide a reviewable starter skill package in Artifacts.",
	"create_zip": True,
})
print(result["zip_bundle"])
print(result["artifact_output"])
PY
```

Expected output includes:

- `created: True`
- `zip_path: coreclaw-skills-hub/.artifacts/generated-skills/agent-skills-builder-demo.zip`
- `output_dir: coreclaw-skills-hub/.artifacts/generated-skills/agent-skills-builder-demo`
- `generated_template_files: ["skill.json", "main.py", "README.md", "SKILL.md", "source/SKILL.md"]`
- `files_packed: 5`

## Suite Example

Create a suite-style package with a group root, orchestrator, and specialized sub-skills:

```bash
python - <<'PY'
from main import run

result = run({
	"structure_type": "suite",
	"group_name": "research-ops",
	"group_title": "Research Ops",
	"description": "Coordinates intake, evidence synthesis, and report assembly for research teams.",
	"subskills": [
		"research-ops-intake",
		{"name": "research-ops-synthesis", "title": "Research Ops Synthesis"},
	],
	"create_zip": True,
})
print(result["template_summary"])
print(result["artifact_output"])
PY
```

Expected output includes:

- `template_mode: suite`
- `group.json`
- root suite files under `coreclaw-skills-hub/.artifacts/generated-skills/research-ops/`
- `research-ops-orchestrator/`
- specialized sub-skill directories such as `research-ops-intake/`
- a ZIP bundle containing the full suite directory tree

If `subskills` is omitted, the builder still produces a suite with default role coverage for intake, execution, and reporting.

## Profile Example

Create a research-oriented suite without explicitly listing sub-skills:

```bash
python - <<'PY'
from main import run

result = run({
	"structure_type": "suite",
	"suite_profile": "research",
	"group_name": "lab-workflow",
	"group_title": "Lab Workflow",
	"description": "Coordinates intake, evidence synthesis, and report assembly for a research workflow.",
})
print(result["template_summary"])
PY
```

Expected `template_summary.subskills`:

- `lab-workflow-intake`
- `lab-workflow-evidence-synthesis`
- `lab-workflow-report-assembly`

The returned `template_summary.orchestrator_contracts` also reflects the selected suite profile.

## Output

This skill helps generate:

- `skill.json` with required fields
- `main.py` entrypoint template
- `README.md` and `SKILL.md` documentation
- `source/SKILL.md` mirror
- `group.json` for suite-style groups
- orchestrator and specialized sub-skill directories with required files
- profile-based default sub-skill sets for suite templates without explicit sub-skill input
- profile-specific orchestrator contracts in `template_summary` and generated `SKILL.md`
- artifact-visible output directory inside the workspace
- downloadable ZIP bundle including generated artifacts
- release-ready tag format (`<skill-path>/vX.Y.Z`)

## Interaction Rule

- Ask users exactly one question at a time
- Wait for the user's answer before asking the next question
- Do not bundle multiple requirement questions into a single turn
- Confirm the true objective in plain language before generating artifacts

## Goal Discovery Flow

1. Capture the user's stated request.
2. Ask one question to identify the background problem.
3. Ask one question to define success criteria.
4. Ask one question to reveal operational constraints.
5. Summarize the inferred true objective and ask for confirmation.
6. Design the agent structure to achieve the confirmed true objective.
