# agent-skills-builder

Builds CoreClaw skill packages from requirements using `docs/SKILLS_GUIDE.md`-compliant structures, optional sub-agent scaffolding, and downloadable ZIP outputs.

## Features

- Dialogue-driven requirement discovery with users
- Enforces one-question-at-a-time interviews with users
- Discovers the user's true objective behind the initial request
- Proactive proposal generation to surface hidden needs
- Creates complete skill package structures aligned to `docs/SKILLS_GUIDE.md`
- Optionally scaffolds sub-agents (sub-skills) when complexity requires role separation
- Generates valid `skill.json`, `README.md`, and `SKILL.md`
- Applies naming/versioning conventions
- Performs pre-release validation checks
- Bundles generated deliverables into ZIP for download
- Produces release tag suggestions
- Enforces authoring limits (main skill <= 1500 chars, sub-skills <= 2000 chars)

## Quick Start

```bash
python main.py
```

## ZIP Bundle Example

Create a downloadable zip from generated artifacts:

```bash
python - <<'PY'
from pathlib import Path
from main import run

out = Path("/tmp/agent-skills-builder-demo")
out.mkdir(parents=True, exist_ok=True)
(out / "skill.json").write_text('{"name":"demo","version":"v0.1.0","description":"demo","entrypoint":"main.py"}\n', encoding="utf-8")
(out / "README.md").write_text('# Demo Skill\n', encoding="utf-8")

result = run({"create_zip": True, "output_dir": str(out)})
print(result["zip_bundle"])
PY
```

Expected output includes:

- `created: True`
- `zip_path: .../agent-skills-builder-demo.zip`
- `files_packed: <number>`

## Output

This skill helps generate:

- `skill.json` with required fields
- `main.py` entrypoint template
- `README.md` and `SKILL.md` documentation
- optional `group.json` for top-level groups
- optional sub-agent (sub-skill) directories with required files
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
