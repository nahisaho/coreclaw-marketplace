#!/usr/bin/env python3
"""
Remove ToolUniverse references from scientist SKILL.md files.

Changes:
1. Remove `tu_tools:` block from YAML frontmatter
2. Replace "Available Tools" / "ToolUniverse Integration" sections
   with "Data Acquisition" section (Python + requests)
3. Remove inline `# ToolUniverse :` comments
4. Remove docstring `ToolUniverse:` blocks
5. Update version to v0.5.0
"""

import os
import re
import json
import glob

SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "coreclaw-skills-hub", "skills", "scientist"
)

DATA_ACQUISITION_SECTION = """## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    \"\"\"Generic REST API data retrieval with error handling.\"\"\"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` summarizing methods, results, and interpretation
"""


def remove_tu_tools_from_frontmatter(content):
    """Remove tu_tools block from YAML frontmatter."""
    # Match YAML frontmatter
    fm_match = re.match(r'^(---\n)(.*?)(---\n)', content, re.DOTALL)
    if not fm_match:
        return content

    pre = fm_match.group(1)
    fm_body = fm_match.group(2)
    post = fm_match.group(3)
    rest = content[fm_match.end():]

    # Remove tu_tools block (key + all indented sub-items)
    # Pattern: tu_tools:\n followed by lines starting with space(s) or - 
    fm_body = re.sub(
        r'tu_tools:\n(?:[ \t]+.*\n)*',
        '',
        fm_body
    )
    # Also remove empty tu_tools: []
    fm_body = re.sub(
        r'\s*tu_tools:\s*\[\]\s*\n?',
        '\n',
        fm_body
    )

    # Clean up multiple blank lines in frontmatter
    fm_body = re.sub(r'\n{3,}', '\n', fm_body)

    return pre + fm_body + post + rest


def remove_tooluniverse_section(content):
    """Remove Available Tools / ToolUniverse Integration sections and replace with Data Acquisition."""
    lines = content.split('\n')
    new_lines = []
    skip_until_next_section = False
    replaced = False
    section_heading_pattern = re.compile(r'^#{1,3}\s')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect start of ToolUniverse-related sections
        if re.match(r'^#{1,3}\s+(Available Tools|ToolUniverse Integration)', line):
            if not replaced:
                new_lines.append(DATA_ACQUISITION_SECTION.rstrip())
                new_lines.append('')
                replaced = True
            skip_until_next_section = True
            i += 1
            continue

        if skip_until_next_section:
            # Check if this line is a new section heading (not part of the tool table)
            if section_heading_pattern.match(line) and not re.match(
                r'^#{1,3}\s+(Available Tools|ToolUniverse Integration)', line
            ):
                skip_until_next_section = False
                new_lines.append(line)
            # Also stop at --- separator
            elif line.strip() == '---' and i > 0:
                skip_until_next_section = False
                new_lines.append(line)
            # Skip this line (part of removed section)
            i += 1
            continue

        new_lines.append(line)
        i += 1

    # If we were still skipping at end of file and haven't added replacement
    if not replaced:
        # No ToolUniverse section found, nothing to replace
        pass

    return '\n'.join(new_lines)


def remove_inline_tooluniverse_comments(content):
    """Remove inline # ToolUniverse : ... comments."""
    # Pattern 1: Single-line comment: # ToolUniverse : tool1, tool2
    content = re.sub(
        r'[ \t]*# ToolUniverse\s*:.*\n',
        '',
        content
    )
    # Pattern 2: Multi-line block starting with # ToolUniverse :
    # followed by # tool_name lines
    content = re.sub(
        r'[ \t]*# ToolUniverse\s*:\s*\n([ \t]*#[ \t]+\w+.*\n)*',
        '',
        content
    )
    # Pattern 3: # 's ToolUniverse retrieval / search / etc.
    content = re.sub(
        r'[ \t]*#.*ToolUniverse.*\n',
        '',
        content
    )
    # Pattern 4: ToolUniverse (cross-cutting): multi-line in docstrings/comments
    content = re.sub(
        r'[ \t]*ToolUniverse \(cross-cutting\):\s*\n([ \t]+.*\n)*?(?=\n[ \t]*\S)',
        '',
        content
    )
    # Pattern 5: ## heading with (ToolUniverse SMCP)
    content = re.sub(
        r'^#{1,3}\s+.*\(ToolUniverse SMCP\).*\n',
        '',
        content,
        flags=re.MULTILINE
    )
    return content


def remove_docstring_tooluniverse(content):
    """Remove ToolUniverse: blocks from docstrings."""
    # Pattern: ToolUniverse:\n    ToolName(args)\n    ToolName(args)\n
    content = re.sub(
        r'[ \t]*ToolUniverse:\s*\n([ \t]+\w+\(.*?\)\n)*',
        '',
        content
    )
    return content


def remove_tooluniverse_blockquote(content):
    """Remove blockquote lines referencing ToolUniverse."""
    content = re.sub(
        r'^>\s*External tools available via \[ToolUniverse\].*\n\n?',
        '',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'^>\s*PubMed/EuropePMC tool.*ToolUniverse.*\n\n?',
        '',
        content,
        flags=re.MULTILINE
    )
    return content


def remove_tooluniverse_prose(content):
    """Remove ToolUniverse mentions from prose/description text."""
    # Replace "ToolUniverse integration: xxx。" with empty
    content = re.sub(
        r'ToolUniverse integration:\s*\S+。\s*',
        '',
        content
    )
    # Replace "ToolUniverse integration: xxx, yyy。" 
    content = re.sub(
        r'ToolUniverse integration:\s*[\w, ]+。\s*',
        '',
        content
    )
    # Replace "ToolUniverse 's Protein Therapeutic Design" and similar
    content = re.sub(
        r"ToolUniverse\s*'s\s+[\w\s]+(?=\s)",
        '',
        content
    )
    # Replace "ToolUniverse（mims-harvard）'s" references  
    content = re.sub(
        r"ToolUniverse（mims-harvard）'s\s*",
        '',
        content
    )
    # Replace standalone "(ToolUniverse integration)" or "( ToolUniverse )" patterns
    content = re.sub(
        r'\(ToolUniverse[^)]*\)\s*',
        '',
        content
    )
    # Replace " 's ToolUniverse SMCP tool" and similar
    content = re.sub(
        r"'s ToolUniverse SMCP tool[^。]*。\s*",
        '',
        content
    )
    # Replace "API (ToolUniverse integration)。"
    content = re.sub(
        r'\s*\(ToolUniverse\s+integration\)',
        '',
        content
    )
    # Remove remaining "ToolUniverse" standalone references in prose
    # but NOT in our new Data Acquisition section
    content = re.sub(
        r'ToolUniverse\s+SMCP\s*',
        '',
        content
    )
    return content


def update_version_header(content, new_version="v0.5.0"):
    """Update Verification Loop / Harness Optimization version in headers."""
    content = re.sub(
        r'(## (?:Verification Loop|Harness Optimization)) \(v[\d.]+\)',
        rf'\1 ({new_version})',
        content
    )
    return content


def process_skill_md(filepath):
    """Process a single SKILL.md file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original
    content = remove_tu_tools_from_frontmatter(content)
    content = remove_inline_tooluniverse_comments(content)
    content = remove_docstring_tooluniverse(content)
    content = remove_tooluniverse_blockquote(content)
    content = remove_tooluniverse_prose(content)
    content = remove_tooluniverse_section(content)
    content = update_version_header(content)

    # Clean up excessive blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def update_skill_json_version(filepath, new_version="v0.5.0"):
    """Update skill.json version."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data.get("version") != new_version:
        data["version"] = new_version
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        return True
    return False


def update_main_py_version(filepath, new_version="v0.5.0"):
    """Update main.py SKILL_META version."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'("version"\s*:\s*)"v[\d.]+"',
        rf'\1"{new_version}"',
        content
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    new_version = "v0.5.0"

    # Process all scientist sub-skills
    skill_dirs = sorted(glob.glob(os.path.join(SKILLS_DIR, "scientific-*")))
    print(f"Found {len(skill_dirs)} scientist sub-skill directories")

    skill_md_count = 0
    skill_json_count = 0
    main_py_count = 0

    for skill_dir in skill_dirs:
        # Process SKILL.md (in source/ and root)
        for skill_md in glob.glob(os.path.join(skill_dir, "**", "SKILL.md"), recursive=True):
            if process_skill_md(skill_md):
                skill_md_count += 1

        # Process skill.json
        skill_json = os.path.join(skill_dir, "skill.json")
        if os.path.exists(skill_json):
            if update_skill_json_version(skill_json, new_version):
                skill_json_count += 1

    # Process source/ mirror SKILL.md files
    source_dir = os.path.join(SKILLS_DIR, "source")
    if os.path.isdir(source_dir):
        for source_skill in sorted(glob.glob(os.path.join(source_dir, "scientific-*"))):
            for skill_md in glob.glob(os.path.join(source_skill, "**", "SKILL.md"), recursive=True):
                if process_skill_md(skill_md):
                    skill_md_count += 1
        # Root source SKILL.md
        root_source_md = os.path.join(source_dir, "SKILL.md")
        if os.path.exists(root_source_md):
            if process_skill_md(root_source_md):
                skill_md_count += 1

    # Process root scientist skill
    root_skill_json = os.path.join(SKILLS_DIR, "skill.json")
    if os.path.exists(root_skill_json):
        if update_skill_json_version(root_skill_json, new_version):
            skill_json_count += 1

    root_skill_md = os.path.join(SKILLS_DIR, "SKILL.md")
    if os.path.exists(root_skill_md):
        if process_skill_md(root_skill_md):
            skill_md_count += 1

    # Process main.py
    main_py = os.path.join(SKILLS_DIR, "main.py")
    if os.path.exists(main_py):
        if update_main_py_version(main_py, new_version):
            main_py_count += 1

    print(f"\nResults:")
    print(f"  SKILL.md modified: {skill_md_count}")
    print(f"  skill.json updated: {skill_json_count}")
    print(f"  main.py updated: {main_py_count}")


if __name__ == "__main__":
    main()
