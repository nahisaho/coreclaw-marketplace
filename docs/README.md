# Documentation - coreclaw-skills-hub

Complete documentation for the coreclaw-skills-hub skills marketplace.

## 📚 Documentation Index

### [Skills Development Guide](./SKILLS_GUIDE.md)

Complete guide for creating and registering skills in the marketplace.

**Contents:**
- Directory structure and file placement
- `SKILL.md` canonical metadata and optional `skill.json` compatibility schema
- Naming conventions and version management
- Step-by-step skill creation process
- Release procedures and best practices

**Target audience:** Skill developers, those adding new skills

---

### [Registry and CI/CD Workflow](./REGISTRY_AND_CI_CD.md)

Detailed information about the registry system and automated workflows.

**Contents:**
- Registry (registry.json) structure
- PR validation workflow (validation.yml)
- Release workflow (release.yml)
- Automatic GitHub Release generation
- Troubleshooting guide

**Target audience:** Marketplace administrators, developers understanding workflows

---

## 🚀 Quick Start

### 1. Create a New Skill

```bash
# Create directory
mkdir -p coreclaw-skills-hub/skills/<group>/<skill-name>
cd coreclaw-skills-hub/skills/<group>/<skill-name>

# Create SKILL.md
cat > SKILL.md << 'EOF'
---
name: my-skill
description: |
    Description
---

# My Skill

## Overview
Skill description

## Usage
Usage instructions
EOF

# Optional compatibility metadata
cat > skill.json << 'EOF'
{
    "name": "my-skill",
    "version": "v0.1.0",
    "description": "Description",
    "entrypoint": "main.py"
}
EOF

cat > main.py << 'EOF'
#!/usr/bin/env python3
def main():
        print("Skill execution")

if __name__ == "__main__":
        main()
EOF

# Commit
git add .
git commit -m "feat: add my-skill"
git push origin main
```

For detailed instructions, see [Skills Development Guide](./SKILLS_GUIDE.md).

### 2. Release a Skill

```bash
# If compatibility metadata exists, update version in skill.json
# version: "v0.1.0" → "v0.2.0"

git add coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json
git commit -m "bump: version v0.2.0"
git push origin main

# Create release tag
git tag <group>/<skill-name>/v0.2.0
git push origin <group>/<skill-name>/v0.2.0
```

For detailed instructions, see [Registry and CI/CD Workflow - Release Workflow](./REGISTRY_AND_CI_CD.md#release-workflow).

---

## 📋 File Structure

```
coreclaw-skills-hub/
├── skills/
│   ├── scientist/
│   │   ├── group.json                                  # Group metadata
│   │   ├── skill.json                                  # Optional package-style root metadata
│   │   ├── scientific-academic-writing/
│   │   │   ├── SKILL.md                               # Canonical skill definition
│   │   │   ├── skill.json                             # Optional compatibility metadata
│   │   │   ├── README.md
│   │   │   └── [other assets]
│   │   ├── skills/                                    # Optional nested sub-skills for package-style roots
│   │   │   ├── orchestrator/
│   │   │   │   └── SKILL.md
│   │   │   └── [specialized-skill]/
│   │   │       └── SKILL.md
│   │   └── [...other skills...]
│   ├── consultant/
│   └── [...other groups...]
├── registry.json                                       # Released skills metadata
├── .github/
│   ├── scripts/
│   │   ├── generate_registry_preview.py               # PR preview generation
│   │   ├── validate_skill.py                          # Skill validation
│   │   └── update_registry.py                         # Registry update
│   └── workflows/
│       ├── validate.yml                               # PR validation workflow
│       └── release.yml                                # Release workflow
└── docs/
    ├── README.md                                       # This file
    ├── README_ja.md                                    # Japanese version
    ├── SKILLS_GUIDE.md                                # Skills development guide
    ├── SKILLS_GUIDE_ja.md                             # Japanese version
    ├── REGISTRY_AND_CI_CD.md                          # Registry and CI/CD guide
    └── REGISTRY_AND_CI_CD_ja.md                       # Japanese version
```

Package-style roots may omit a root `SKILL.md` when they keep `group.json`, a root `skill.json`, and nested `skills/<subskill>/SKILL.md` files.

---

## 🔑 Key Concepts

### Semantic Versioning

Version format: `v<MAJOR>.<MINOR>.<PATCH>`

```
v0.1.0  Initial version
v0.2.0  New features added (minor version bump)
v0.2.1  Bug fix (patch version bump)
v1.0.0  Stable release (major version bump)
```

Reference: [semver.org](https://semver.org/)

### Tag Naming Convention

```bash
# Single skill (group = skill)
<group>/v<version>

# Nested skill (skill within group)
<group>/<skill-name>/v<version>
```

Examples:
```bash
scientist/scientific-academic-writing/v0.2.0
consultant/v0.1.0
```

### Registry Update Timing

- **Automatic update**: Only when tags are pushed (GitHub Actions)
- **Manual update**: Not allowed (changes only via automated workflow)
- **On PR**: Preview generation only (no registry.json changes)

---

## 🛠 Technology Stack

- **Scripting language**: Python 3.8+
- **Version control**: Git
- **Automation**: GitHub Actions
- **Registry format**: JSON
- **Skill implementation language**: Python (recommended)

---

## 📞 Support

### Frequently Asked Questions (FAQ)

**Q: I want to release multiple skills at once**

A: Create multiple tags and push them together:
```bash
git tag group/skill1/v0.1.0 group/skill2/v0.1.0
git push origin --tags
```

**Q: How do I delete a tag?**

A:
```bash
git tag -d tag-name
git push origin :refs/tags/tag-name
```

**Q: Where can I see the registry preview?**

A: Download `registry-preview` from the Artifacts section of the PR.

### Reporting Issues

If you encounter issues or have questions:
1. Report via GitHub Issues
2. Include detailed error logs
3. Attach related files (skill.json, etc.)

---

## 📚 Additional Resources

- [Semantic Versioning - semver.org](https://semver.org/)
- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### Language Versions

- **English** (this file)
- **日本語** (Japanese) - See [README_ja.md](./README_ja.md)

---

**Last updated**: 2026-03-27  
**Author**: coreclaw-skills-hub  
**Version**: 1.0.0
