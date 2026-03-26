# Registry and CI/CD Workflow

This document explains the registry system and automated workflows in coreclaw-skills-hub.

## Table of Contents

1. [Registry Structure](#registry-structure)
2. [Validation Workflow](#validation-workflow)
3. [Release Workflow](#release-workflow)
4. [Troubleshooting](#troubleshooting)

---

## Registry Structure

### registry.json Format

`coreclaw-skills-hub/registry.json` manages metadata and URLs for all released skills.

```json
{
  "generated_at": "2026-03-27T12:34:56+00:00",
  "skills": {
    "scientist": {
      "name": "Scientist",
      "description": "Skills for scientists...",
      "icon": "🔬",
      "isGroup": true,
      "skillCount": 196
    },
    "scientist/scientific-academic-writing": {
      "name": "scientific-academic-writing",
      "version": "v0.1.0",
      "entrypoint": "main.py",
      "description": "Assists researchers in composing...",
      "latest": "v0.1.0",
      "versions": [
        {
          "version": "v0.1.0",
          "url": "https://github.com/.../releases/download/scientist/scientific-academic-writing/v0.1.0/skill.zip",
          "released_at": "2026-03-27T10:30:00+00:00"
        }
      ]
    },
    "consultant": {
      "name": "Consultant",
      "description": "General consultant skills...",
      "icon": "💼",
      "isGroup": true,
      "skillCount": 1
    }
  }
}
```

### Field Description

#### Group Entry (`isGroup: true`)

| Field | Description |
|-------|-------------|
| `name` | Group display name |
| `description` | Group description |
| `icon` | Emoji representing group |
| `isGroup` | Flag indicating group type |
| `skillCount` | Number of skills in group |

#### Skill Entry

| Field | Description |
|-------|-------------|
| `name` | Unique skill name |
| `version` | Current version |
| `description` | Skill description |
| `entrypoint` | Execution file (usually `main.py`) |
| `latest` | Latest version number |
| `versions` | Version history (includes URL and release date) |

---

## Validation Workflow

### Trigger Timing

- **Trigger**: Pull Request with changes to `skills/**` paths
- **Action**: Runs PR validation checks

### Workflow Process

```
Create PR → Detect changes → Validate skill.json → Generate registry preview → Upload artifact → Review
```

### Validation Items

1. **skill.json Existence**: Check if each skill directory has `skill.json`
2. **Required Fields**: Verify `name`, `version`, `description`, `entrypoint` exist
3. **Version Format**: Confirm `vX.Y.Z` format (Semantic Versioning)
4. **Entrypoint Existence**: Verify file specified in entrypoint exists

### Registry Preview

PR automatically generates `registry.preview.json` and uploads as artifact.

**Usage:**
- Review skill metadata during PR review
- Verify final registry.json form before release
- Validation without branch pollution

**How to Check:**
1. Open PR "Checks" tab
2. Select "Details"
3. Choose "Artifacts"
4. Download `registry-preview`

---

## Release Workflow

### Trigger Timing

- **Trigger**: Tag creation and push
- **Tag Format**: `<skill-path>/v<major>.<minor>.<patch>`

### Tag Examples

```bash
# Single skill (group = skill)
git tag consultant/v0.1.0

# Nested skill (skill within group)
git tag scientist/scientific-academic-writing/v0.2.0
```

### Workflow Process

```
Create tag
  ↓
Validate skill.json
  ↓
Zip skill directory
  ↓
Create GitHub Release
  ↓
Update registry.json
  ↓
Push registry.json to main
```

### Output

#### GitHub Release

Created on release page:

- **Title**: `[<skill-path>] Release v<version>`
- **Description**: From skill.json `description`
- **Asset**: `skill.zip` (entire skill zipped)

**URL Example:**
```
https://github.com/nahisaho/coreclaw-marketplace/releases/download/scientist/scientific-academic-writing/v0.1.0/skill.zip
```

#### registry.json Update

```json
{
  "scientist/scientific-academic-writing": {
    "latest": "v0.2.0",
    "versions": [
      {
        "version": "v0.2.0",
        "url": "https://github.com/.../releases/download/scientist/scientific-academic-writing/v0.2.0/skill.zip",
        "released_at": "2026-03-27T15:45:00+00:00"
      },
      {
        "version": "v0.1.0",
        "url": "https://github.com/.../releases/download/scientist/scientific-academic-writing/v0.1.0/skill.zip",
        "released_at": "2026-03-26T10:30:00+00:00"
      }
    ]
  }
}
```

---

## Troubleshooting

### Validation Errors

#### Error: `skill.json not found`

**Cause**: skill.json missing from skill directory

**Solution**:
```bash
# Verify skill directory
ls coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json

# Create if missing
cat > coreclaw-skills-hub/skills/<group>/<skill-name>/skill.json << 'EOF'
{
  "name": "your-skill",
  "version": "v0.1.0",
  "description": "Description",
  "entrypoint": "main.py"
}
EOF
```

#### Error: `Invalid version format`

**Cause**: Version not in `vX.Y.Z` format

**Solution**:
```json
{
  "version": "v0.1.0"  // ✅ Correct format
}
```

❌ Incorrect formats:
- `0.1.0` (missing v)
- `v1` (missing minor, patch)
- `1.0.0-beta` (pre-release tag not supported)

#### Error: `entrypoint file not found`

**Cause**: File specified in skill.json entrypoint doesn't exist

**Solution**:
```bash
# Verify file exists
ls coreclaw-skills-hub/skills/<group>/<skill-name>/main.py

# Create if missing
cat > coreclaw-skills-hub/skills/<group>/<skill-name>/main.py << 'EOF'
#!/usr/bin/env python3
"""Skill entry point."""

def main():
    print("Skill execution")

if __name__ == "__main__":
    main()
EOF
```

### Release Errors

#### Error: `Release creation failed`

**Cause**: Invalid tag format

**Solution**:
```bash
# Check correct tag format
git tag -l | grep "scientist/scientific"

# Delete if needed
git tag -d incorrect-tag
git push origin :refs/tags/incorrect-tag

# Create correct tag
git tag scientist/scientific-academic-writing/v0.2.0
git push origin scientist/scientific-academic-writing/v0.2.0
```

#### Error: `GitHub Actions failure`

**How to Check:**
1. Open GitHub "Actions" tab
2. Click failed workflow
3. Review logs

**Common Causes and Solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid regex` | Invalid tag format | Recreate tag |
| `ZIP creation failed` | File not found | Verify file paths |
| `API rate limit` | GitHub API limit reached | Wait and retry |

---

## Best Practices

### Pre-Release Checklist

- [ ] Verify skill.json has correct format
- [ ] Check all required fields (name, version, description, entrypoint) present
- [ ] Confirm version follows Semantic Versioning
- [ ] Ensure main.py exists and is executable
- [ ] Verify SKILL.md or README.md exists
- [ ] Confirm new version merged to main

### Tag Creation Commands

```bash
# Complete flow example
git checkout main
git pull origin main

# Update version (example)
# Update version in coreclaw-skills-hub/skills/scientist/scientific-academic-writing/skill.json to v0.2.0

git add coreclaw-skills-hub/skills/scientist/scientific-academic-writing/skill.json
git commit -m "bump: version v0.2.0 for scientific-academic-writing"
git push origin main

# Create release tag
git tag scientist/scientific-academic-writing/v0.2.0
git push origin scientist/scientific-academic-writing/v0.2.0

# Verify status
git tag -l scientist/scientific-academic-writing/v0.2.0
```

### Release Multiple Skills

```bash
git tag scientist/skill1/v0.2.0
git tag scientist/skill2/v0.1.0
git push origin --tags
```

---

## Reference Links

- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Language Versions:**
- **English** (this file)
- **日本語** (Japanese) - See [REGISTRY_AND_CI_CD_ja.md](./REGISTRY_AND_CI_CD_ja.md)
