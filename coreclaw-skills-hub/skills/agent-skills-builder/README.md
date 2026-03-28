# agent-skills-builder

Builds Agent Skills compliant packages for GitHub Copilot CLI by default, while preserving the previous CoreClaw package layout as an explicit legacy mode.

## Features

- Dialogue-driven requirement discovery with one-question-at-a-time interviews
- True-objective discovery before scaffolding
- Agent Skills compliant single-skill generation with required `SKILL.md`
- Agent Skills compliant suite generation with orchestrator and specialized skill directories
- Profile-based suite presets for `ops`, `research`, and `consulting`
- Profile-specific orchestrator Input Contract, Output Contract, Quality Gates, and Fallback Policy sections
- Workspace-visible artifact output and optional ZIP bundling
- Backward-compatible CoreClaw generation via `target_format: "coreclaw"`

## Default Output Format

If `target_format` is omitted, the builder generates Agent Skills compliant output.

Single-skill output:

- `SKILL.md`

Suite output:

- `README.md` collection summary
- `<group>-orchestrator/SKILL.md`
- one `SKILL.md` per specialized skill directory

The generated `SKILL.md` files include YAML frontmatter with `name` and `description`, and optionally add `license`, `compatibility`, `metadata`, and `allowed-tools` when supplied in the input payload.

## Legacy CoreClaw Mode

Set `target_format` to `coreclaw` to generate the previous repository-specific scaffold:

- `skill.json`
- `main.py`
- `README.md`
- `SKILL.md`
- `source/SKILL.md`
- `group.json` for suite mode

## Artifact Output

Generated skills are saved to a workspace-visible location so they can be surfaced in Artifacts.

- Default directory: `coreclaw-skills-hub/.artifacts/generated-skills/<skill-name>/`
- ZIP bundle: `coreclaw-skills-hub/.artifacts/generated-skills/<skill-name>.zip`
- If `output_dir` points outside the workspace, the builder falls back to the artifact-visible default path

## Quick Start

```bash
python main.py
```

## Example: Default Agent Skills Output

```bash
python - <<'PY'
from main import run

result = run({
	"skill_name": "incident-triage",
	"description": "Triage operational incidents and prepare a concise action plan.",
	"compatibility": "github-copilot-cli",
	"allowed_tools": ["bash", "read_file"],
	"create_zip": True,
})
print(result["template_summary"])
print(result["artifact_output"])
PY
```

Expected generated files:

- `SKILL.md`
- optional ZIP bundle in the artifact directory

## Example: Agent Skills Suite

```bash
python - <<'PY'
from main import run

result = run({
	"structure_type": "suite",
	"suite_profile": "research",
	"group_name": "lab-workflow",
	"group_title": "Lab Workflow",
	"description": "Coordinate intake, evidence synthesis, and report assembly for a research workflow.",
})
print(result["template_summary"])
PY
```

Expected generated directories:

- `lab-workflow-orchestrator/`
- `lab-workflow-intake/`
- `lab-workflow-evidence-synthesis/`
- `lab-workflow-report-assembly/`

## Example: Legacy CoreClaw Output

```bash
python - <<'PY'
from main import run

result = run({
	"target_format": "coreclaw",
	"skill_name": "coreclaw-demo",
	"description": "Generate the previous CoreClaw package layout.",
})
print(result["template_summary"])
PY
```

## Interaction Rule

- Ask users exactly one question at a time
- Wait for the user's answer before asking the next question
- Do not bundle multiple requirement questions into a single turn
- Confirm the true objective in plain language before generating artifacts
