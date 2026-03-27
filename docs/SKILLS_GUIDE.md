# Skills Development Guide

This guide explains the procedures and best practices for creating and registering skills in the coreclaw-skills-hub marketplace.

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [skill.json Schema](#skilljson-schema)
3. [group.json Schema](#groupjson-schema)
4. [File Requirements](#file-requirements)
5. [Naming Conventions](#naming-conventions)
6. [Skill Creation Steps](#skill-creation-steps)
7. [Release Procedures](#release-procedures)
8. [Best Practices](#best-practices)

---

## Directory Structure

### Group-level Root Skill (Suite Parent)

```
coreclaw-skills-hub/skills/
└── <group-name>/
    ├── group.json                    # Group metadata
    ├── SKILL.md                      # Skill documentation (root)
    ├── skill.json                    # Skill metadata
    ├── main.py                       # Entrypoint (marketplace)
    ├── README.md                     # Skill description (marketplace)
  ├── source/                       # Original payload
        ├── SKILL.md                  # Original skill document
  │   └── [other original files]
  ├── <group-orchestrator>/         # Orchestrator sub-skill
  │   ├── SKILL.md
  │   ├── skill.json
  │   ├── main.py
  │   ├── README.md
  │   └── source/
  │       └── SKILL.md
  └── <group-specialized-skill>/    # Specialized sub-skill(s)
    ├── SKILL.md
    ├── skill.json
    ├── main.py
    ├── README.md
    └── source/
      └── SKILL.md
```

Examples: `scientist/`, `enterprise/`, `growth/`, `secops/`

### Nested Skills (Multiple Skills in Group)

```
coreclaw-skills-hub/skills/
└── <group-name>/
    ├── group.json                    # Group metadata
    ├── <skill-name-1>/
    │   ├── SKILL.md
    │   ├── skill.json
    │   ├── main.py
    │   ├── README.md
    │   └── source/
    │       ├── SKILL.md
    │       └── [other files]
    └── <skill-name-2>/
        ├── SKILL.md
        ├── skill.json
        ├── main.py
        ├── README.md
        └── source/
            ├── SKILL.md
            └── [other files]
```

Examples: `scientist/scientific-academic-writing/`, `enterprise/enterprise-orchestrator/`, `growth/growth-funnel-analysis/`

---

## skill.json Schema

### Minimal Example

```json
{
  "name": "my-skill-name",
  "version": "v0.1.0",
  "description": "Brief description of what this skill does",
  "entrypoint": "main.py"
}
```

### Field Description

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Unique skill name. Use kebab-case. Must not duplicate within the domain. |
| `version` | string | ✅ | Semantic Versioning format: `vX.Y.Z`. Ex: `v0.1.0`, `v1.2.3` |
| `description` | string | ✅ | Brief skill description (English recommended). Summarize in 1-2 sentences. |
| `entrypoint` | string | ✅ | Main file executed from marketplace. Usually `main.py` |
| `author` | string | ❌ | Skill creator name or email address |
| `license` | string | ❌ | License type. Ex: `MIT`, `Apache-2.0` |
| `keywords` | array | ❌ | Keywords for skill classification. Ex: `["research", "writing", "academic"]` |

### Extended Example

```json
{
  "name": "scientific-academic-writing",
  "version": "v0.2.0",
  "description": "Assists researchers in composing high-quality academic papers with proper structure and citation formatting",
  "entrypoint": "main.py",
  "author": "research-team",
  "license": "MIT",
  "keywords": ["research", "writing", "academic", "paper", "documentation"]
}
```

---

## group.json Schema

Defines metadata for groups (skill categories). Place directly in group directory.

### Minimal Example

```json
{
  "name": "Scientist",
  "description": "Skills for scientists and researchers",
  "icon": "🔬",
  "count": 196
}
```

### Field Description

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Group display name. User-friendly format. |
| `description` | string | ✅ | Group description (English). Explain common features of skills. |
| `icon` | string | ✅ | Emoji or icon representing group. For UI display. |
| `count` | number | ✅ | Number of skills in group. Updated during registry generation. |

### Suggested Icons

```
🔬  Scientists (scientist)
💼  Consultants (consultant)
📚  Educators (educationalist)
📊  Data Scientists
🔧  Engineers
💡  Innovation
```

---

## File Requirements

### SKILL.md (Skill Documentation)

Detailed skill documentation. Place in both root and `source/` directories.

**Required Sections:**

```markdown
# [Skill Name]

## Overview
What the skill does and who it targets.

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Usage
How to use the skill with examples.

## Input/Output Format
Specification of input and output formats.

## Prerequisites
Required environment, dependencies, access permissions.

## License
Skill license information.
```

### Orchestrator SKILL.md (Required for Suite-style Groups)

For orchestrator sub-skills (for example, `<group>/<group>-orchestrator/`), include these sections in `SKILL.md`:

- `## Orchestration Flow`
- `## Input Contract`
- `## Output Contract`
- `## Quality Gates`
- `## Fallback Policy`

The orchestrator file should explicitly define how sub-skills are chained and validated.

### main.py (Entrypoint)

Python script executed from the marketplace.

**Minimal Example:**

```python
#!/usr/bin/env python3
"""Marketplace entrypoint for [Skill Name]."""

def main():
    """Execute skill logic."""
    print("Skill executed successfully")

if __name__ == "__main__":
    main()
```

### README.md (Marketplace Description)

Short description displayed in registry. Based on `skill.json` `description`.

**Example:**

```markdown
# Scientific Academic Writing

Assists researchers in composing high-quality academic papers with proper 
structure and citation formatting.

## Features

- Automated abstract generation
- Citation management
- Structure validation
- Language enhancement

## Quick Start

```bash
python main.py
```

## Requirements

- Python 3.8+
- LaTeX for PDF generation (optional)
```

---

## Naming Conventions

### Group Names
- English, kebab-case
- Plural recommended: `scientists`, `consultants`
- Examples: `scientist`, `consultant`, `consultant-acn`, `educationalist`

### Skill Names
- English, kebab-case
- Clearly express skill functionality
- Examples: `scientific-academic-writing`, `strategic-planning`, `presentation-design`

### Version Numbers
- Follow Semantic Versioning (Semantic Versioning)
- Format: `vMAJOR.MINOR.PATCH`
- Examples: `v0.1.0`, `v1.0.0`, `v2.1.3`

**Versioning Guidelines:**
- `MAJOR`: Made breaking changes
- `MINOR`: Added features with backward compatibility
- `PATCH`: Bug fixes and minor changes

---

## Skill Creation Steps

### 1. Choose Structure Type

- **Suite-style group** (recommended for advanced workflows):

```bash
mkdir -p coreclaw-skills-hub/skills/<group>
mkdir -p coreclaw-skills-hub/skills/<group>/source
mkdir -p coreclaw-skills-hub/skills/<group>/<group>-orchestrator/source
```

- **Single sub-skill only**:

```bash
mkdir -p coreclaw-skills-hub/skills/<group>/<skill-name>
cd coreclaw-skills-hub/skills/<group>/<skill-name>
```

### 2. Create skill.json

```json
{
  "name": "<skill-name>",
  "version": "v0.1.0",
  "description": "Your skill description here",
  "entrypoint": "main.py"
}
```

### 3. Create main.py

Implement skill logic:

```python
#!/usr/bin/env python3
"""[Skill Name] implementation."""

def main():
    """Main skill execution."""
    # Your implementation here
    pass

if __name__ == "__main__":
    main()
```

### 4. Create SKILL.md

Create skill documentation:

```markdown
# [Skill Name]

## Overview
Description

## Usage
Usage instructions

...
```

### 5. Create README.md

Create marketplace-facing description:

```markdown
# [Skill Name]

Brief description and features
```

### 6. Create source/ Directory (Optional)

Store original payload:

```bash
mkdir source
cp SKILL.md source/
# Copy other original files
```

### 7. Commit Changes

```bash
git add <group>/<skill-name>/
git commit -m "feat: add <skill-name> skill"
git push origin main
```

---

## Release Procedures

### 1. Update Version in skill.json

```json
{
  "name": "my-skill",
  "version": "v0.2.0",  // <- Update this
  "description": "...",
  "entrypoint": "main.py"
}
```

### 2. Commit Changes

```bash
git add coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json
git commit -m "bump: version v0.2.0 for <skill-name>"
git push origin main
```

### 3. Create Release Tag

```bash
# Single skill (group = skill name)
git tag <group>/v0.2.0
git push origin <group>/v0.2.0

# Nested skill (skill within group)
git tag <group>/<skill-name>/v0.2.0
git push origin <group>/<skill-name>/v0.2.0
```

### 4. Verify GitHub Release

After tag creation, GitHub Actions automatically:
- Zips skill directory
- Creates GitHub Release
- Updates registry.json
- Pushes changes to main branch

---

## Best Practices

### Writing Descriptions

✅ **Good Example:**
```
"Assists researchers in composing high-quality academic papers with proper structure and citation formatting"
```

❌ **Bad Example:**
```
"paper writing"
"tool for writing"
```

### Version Progression

```
v0.1.0  -> v0.2.0  When adding features
v0.1.0  -> v0.1.1  When fixing bugs
v0.9.0  -> v1.0.0  When releasing stable version
```

### File Size

- `SKILL.md`: Keep concise. Split into multiple files if complex.
- `main.py`: Modularize if implementation is large.
- `source/`: Store entire original payload.
- For `agent-skills-builder`: keep main skill content within 1500 characters and sub-skill content within 2000 characters.

### Dependency Management

- Provide `requirements.txt` if external libraries needed
- Pin dependency versions
- Recommend Python >= 3.8

### Language Consistency

- `skill.json` `description`: **English**
- `group.json` `description`: **English**
- `SKILL.md`: Japanese or English (maintain consistency)
- `README.md`: English recommended

### CI/CD Integration

- Include all required fields in `skill.json`
- Verify entrypoint file exists
- Validate automatically on push to main branch
- Keep `group.json` `count` aligned with actual number of skills in the group (including root skill).

---

## FAQ

### Q. Can I update a skill without changing the version?

A. No. Since registry tracks versions, always update the version number. GitHub Actions will detect the new version when creating the tag and update registry.json.

### Q. Can I release multiple skills at once?

A. Yes. Create tags for each skill and push them together; GitHub Actions processes each one.

```bash
git tag scientist/scientific-writing/v0.2.0
git tag scientist/data-analysis/v0.1.0
git push origin --tags
```

### Q. Does the system support nested groups (3+ levels)?

A. Current system supports up to 2 levels (group + skill). For 3+ levels, registry configuration needs modification.

### Q. Is the source/ directory required?

A. No. It's optional for new skills. Use it when importing existing payloads to preserve original file structure.

---

## Support

For questions or issues, report in the repository's Issues section.

---

**Language Versions:**
- **English** (this file)
- **日本語** (Japanese) - See [SKILLS_GUIDE_ja.md](./SKILLS_GUIDE_ja.md)
