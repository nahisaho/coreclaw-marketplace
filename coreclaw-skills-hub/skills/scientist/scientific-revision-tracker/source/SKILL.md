---
name: scientific-revision-tracker
description: |
 Revision tracker skill. Manuscript revision tracking, diff generation between drafts, change log maintenance, and reviewer comment integration management.
---

# Scientific Revision Tracker

paperprocessinchange's minskill。
peer reviewfrom to 's direction.

## When to Use

- 's 's minvisualizationwhen needed
- peer reviewsupport's changewhen needed
- change（/）when needed
- multiple'swhen needed
- summaryautomatedgenerationwhen needed

## Quick Start

## 1. workflow

```
 (v1) + peer review
 ├─ Phase 1: 
 │ ├─ manuscript/versions/v1.md assave
 │ ├─ data（datetime、number）
 │ └─ 's
 ├─ Phase 2: 's（skill and 'sintegration）
 │ ├─ peer-review-response → support's
 │ ├─ academic-writing → papersfix
 │ └─ critical-review → fix's cell
 ├─ Phase 3: min
 │ ├─ 's minextraction
 │ ├─ 's change
 │ ├─ addition/deletion/change's
 │ └─ change'scalculation
 ├─ Phase 4: verification
 │ ├─ all Major correspondingchange
 │ ├─ change times's and
 │ └─ support's
 └─ Phase 5: fileoutput
 ├─ manuscript/manuscript_tracked.md — change
 ├─ manuscript/revision_summary.json — 
 └─ manuscript/versions/vN.md — 
```

## 2. 

```python
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher, unified_diff


def create_version_snapshot(manuscript_path, round_number=1,
 label="original", filepath=None):
 """
 'ssave.

 Args:
 manuscript_path: Path — 's
 round_number: int — peer review
 label: str — "original", "r1_revised", "r2_revised" 
 filepath: Path — save

 Returns:
 dict: data
 """
 if filepath is None:
 versions_dir = BASE_DIR / "manuscript" / "versions"
 versions_dir.mkdir(parents=True, exist_ok=True)
 filepath = versions_dir / f"v{round_number}_{label}.md"

 with open(manuscript_path, "r", encoding="utf-8") as f:
 content = f.read

 # 's
 sections = _split_into_sections(content)
 section_hashes = {
 name: hashlib.md5(text.encode).hexdigest
 for name, text in sections.items
 }

 # save
 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)

 metadata = {
 "version": f"v{round_number}_{label}",
 "timestamp": datetime.now.isoformat,
 "round": round_number,
 "label": label,
 "path": str(filepath),
 "word_count": len(content.split),
 "section_count": len(sections),
 "section_hashes": section_hashes,
 }

 # datasave
 meta_path = filepath.with_suffix(".json")
 with open(meta_path, "w", encoding="utf-8") as f:
 json.dump(metadata, f, indent=2, ensure_ascii=False)

 print(f" → save: {filepath}")
 print(f" → datasave: {meta_path}")
 return metadata


def _split_into_sections(text):
 """Markdown min."""
 sections = {}
 current_section = "Preamble"
 current_content = []

 for line in text.split('\n'):
 header_match = re.match(r'^#{1,3}\s+(.+)$', line)
 if header_match:
 if current_content:
 sections[current_section] = '\n'.join(current_content)
 current_section = header_match.group(1).strip
 current_content = [line]
 else:
 current_content.append(line)

 if current_content:
 sections[current_section] = '\n'.join(current_content)

 return sections
```

## 3. min

```python
def compute_diff(original_path, revised_path):
 """
 2 items's 's mincalculation.

 Args:
 original_path: Path — 's
 revised_path: Path — 's

 Returns:
 dict: {
 "sections_changed": ["Introduction", "Discussion"],
 "sections_added": [],
 "sections_removed": [],
 "changes": [
 {
 "section": "Introduction",
 "type": "modified",
 "original_lines": [...],
 "revised_lines": [...],
 "similarity": 0.85,
 }
 ],
 "stats": {
 "lines_added": 45,
 "lines_removed": 12,
 "lines_modified": 23,
 "word_count_change": +350,
 "sections_modified": 3,
 }
 }
 """
 with open(original_path, "r", encoding="utf-8") as f:
 original = f.read
 with open(revised_path, "r", encoding="utf-8") as f:
 revised = f.read

 orig_sections = _split_into_sections(original)
 rev_sections = _split_into_sections(revised)

 all_sections = set(list(orig_sections.keys) + list(rev_sections.keys))
 sections_changed = []
 sections_added = []
 sections_removed = []
 changes = []

 for section in all_sections:
 if section in orig_sections and section not in rev_sections:
 sections_removed.append(section)
 changes.append({
 "section": section,
 "type": "removed",
 "original_lines": orig_sections[section].split('\n'),
 "revised_lines": [],
 "similarity": 0.0,
 })
 elif section not in orig_sections and section in rev_sections:
 sections_added.append(section)
 changes.append({
 "section": section,
 "type": "added",
 "original_lines": [],
 "revised_lines": rev_sections[section].split('\n'),
 "similarity": 0.0,
 })
 elif orig_sections[section] != rev_sections[section]:
 sections_changed.append(section)
 similarity = SequenceMatcher(
 None, orig_sections[section], rev_sections[section]
 ).ratio
 changes.append({
 "section": section,
 "type": "modified",
 "original_lines": orig_sections[section].split('\n'),
 "revised_lines": rev_sections[section].split('\n'),
 "similarity": round(similarity, 3),
 })

 # 
 orig_lines = original.split('\n')
 rev_lines = revised.split('\n')
 diff_lines = list(unified_diff(orig_lines, rev_lines, lineterm=''))
 lines_added = sum(1 for l in diff_lines if l.startswith('+') and not l.startswith('+++'))
 lines_removed = sum(1 for l in diff_lines if l.startswith('-') and not l.startswith('---'))

 stats = {
 "lines_added": lines_added,
 "lines_removed": lines_removed,
 "lines_modified": min(lines_added, lines_removed),
 "word_count_original": len(original.split),
 "word_count_revised": len(revised.split),
 "word_count_change": len(revised.split) - len(original.split),
 "sections_modified": len(sections_changed),
 "sections_added": len(sections_added),
 "sections_removed": len(sections_removed),
 }

 return {
 "sections_changed": sections_changed,
 "sections_added": sections_added,
 "sections_removed": sections_removed,
 "changes": changes,
 "stats": stats,
 }
```

## 4. changegeneration

```python
MARKUP_STYLES = {
 "latex": {
 "added": r"\textcolor{blue}{%s}",
 "removed": r"\st{\textcolor{red}{%s}}",
 "comment": r"\marginpar{\footnotesize %s}",
 },
 "markdown": {
 "added": '<span style="color:blue">%s</span>',
 "removed": '~~<span style="color:red">%s</span>~~',
 "comment": '<!-- REVISION: %s -->',
 },
 "track_changes": {
 "added": "[++%s++]",
 "removed": "[--%s--]",
 "comment": "[COMMENT: %s]",
 },
}


def generate_tracked_manuscript(original_path, revised_path,
 markup_style="markdown",
 response_mapping=None,
 filepath=None):
 """
 change is generated。

 Args:
 original_path: Path — 's
 revised_path: Path — 's
 markup_style: str — "markdown", "latex", "track_changes"
 response_mapping: dict — -mapping（noteaddition）
 filepath: Path — output destination
 """
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "manuscript_tracked.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 style = MARKUP_STYLES.get(markup_style, MARKUP_STYLES["markdown"])

 with open(original_path, "r", encoding="utf-8") as f:
 orig_lines = f.readlines
 with open(revised_path, "r", encoding="utf-8") as f:
 rev_lines = f.readlines

 matcher = SequenceMatcher(None, orig_lines, rev_lines)
 tracked = []

 for tag, i1, i2, j1, j2 in matcher.get_opcodes:
 if tag == 'equal':
 tracked.extend(orig_lines[i1:i2])
 elif tag == 'replace':
 for line in orig_lines[i1:i2]:
 tracked.append(style["removed"] % line.rstrip + '\n')
 for line in rev_lines[j1:j2]:
 tracked.append(style["added"] % line.rstrip + '\n')
 elif tag == 'delete':
 for line in orig_lines[i1:i2]:
 tracked.append(style["removed"] % line.rstrip + '\n')
 elif tag == 'insert':
 for line in rev_lines[j1:j2]:
 tracked.append(style["added"] % line.rstrip + '\n')

 # peer reviewnumber noteasinsertion
 if response_mapping:
 tracked = _annotate_with_comments(tracked, response_mapping, style)

 with open(filepath, "w", encoding="utf-8") as f:
 f.writelines(tracked)

 print(f" → save: {filepath}")
 return filepath


def _annotate_with_comments(tracked_lines, mapping, style):
 """numbernote addition."""
 # response_mapping from section → number's mappingconstruction
 section_comments = {}
 for reviewer in mapping.get("reviewers", []):
 for comment in reviewer.get("comments", []):
 section = comment.get("section", "General")
 if section not in section_comments:
 section_comments[section] = []
 section_comments[section].append(
 f"{reviewer['id']} #{comment['number']}"
 )

 # 's noteinsertion
 result = []
 for line in tracked_lines:
 result.append(line)
 header = re.match(r'^#{1,3}\s+(.+)', line)
 if header:
 section_name = header.group(1).strip
 if section_name in section_comments:
 comment_refs = ", ".join(section_comments[section_name])
 result.append(style["comment"] % f"Addresses: {comment_refs}" + '\n')

 return result
```

## 5. verification

```python
def verify_revision_traceability(response_mapping, diff_result):
 """
 allpeer reviewcorrespondingverification.

 Args:
 response_mapping: dict — generate_response_mapping 's results
 diff_result: dict — compute_diff 's results

 Returns:
 dict: {
 "all_addressed": bool,
 "unaddressed_comments": [...],
 "orphan_changes": [...], # change
 "verification_summary": str,
 }
 """
 changed_sections = set(diff_result["sections_changed"] + diff_result["sections_added"])

 unaddressed = []
 addressed = []

 for reviewer in response_mapping.get("reviewers", []):
 for comment in reviewer.get("comments", []):
 section = comment.get("section", "General")
 strategy = comment.get("strategy", "pending")

 if strategy == "rebut":
 # case change
 addressed.append(comment)
 elif section in changed_sections:
 addressed.append(comment)
 elif strategy == "accept" or strategy == "partially_accept":
 unaddressed.append({
 "reviewer": reviewer["id"],
 "comment_number": comment["number"],
 "severity": comment["severity"],
 "expected_section": section,
 "strategy": strategy,
 })

 all_addressed = len(unaddressed) == 0

 # change
 commented_sections = set
 for reviewer in response_mapping.get("reviewers", []):
 for comment in reviewer.get("comments", []):
 commented_sections.add(comment.get("section", "General"))

 orphan_changes = [s for s in changed_sections if s not in commented_sections]

 return {
 "all_addressed": all_addressed,
 "addressed_count": len(addressed),
 "unaddressed_comments": unaddressed,
 "orphan_changes": orphan_changes,
 "verification_summary": (
 f"✅ allsupport ({len(addressed)} items)"
 if all_addressed
 else f"⚠️ support: {len(unaddressed)} items"
 ),
 }
```

## 6. Pipeline Integration

```python
def run_revision_tracker(original_path, revised_path, round_number=1,
 response_mapping_path=None, markup_style="markdown"):
 """
 pipeline is executed。

 output file:
 manuscript/versions/vN_*.md — 
 manuscript/manuscript_tracked.md — change
 manuscript/revision_summary.json — 
 """
 print("=" * 60)
 print(f"Revision Tracker Pipeline (Round {round_number})")
 print("=" * 60)

 # Phase 1: 
 print("\n[Phase 1]...")
 create_version_snapshot(original_path, round_number, "original")
 create_version_snapshot(revised_path, round_number, "revised")

 # Phase 2: mincalculation
 print("\n[Phase 2] min calculation...")
 diff = compute_diff(original_path, revised_path)
 stats = diff["stats"]
 print(f" → change: {diff['sections_changed']}")
 print(f" → addition: +{stats['lines_added']}, deletion: -{stats['lines_removed']}")
 print(f" → number/count: {stats['word_count_change']:+d}")

 # Phase 3: generation
 print("\n[Phase 3] change generation...")
 mapping = None
 if response_mapping_path:
 with open(response_mapping_path, "r", encoding="utf-8") as f:
 mapping = json.load(f)

 generate_tracked_manuscript(
 original_path, revised_path,
 markup_style=markup_style,
 response_mapping=mapping,
 )

 # Phase 4: verification
 traceability = None
 if mapping:
 print("\n[Phase 4] verification...")
 traceability = verify_revision_traceability(mapping, diff)
 print(f" → {traceability['verification_summary']}")
 if traceability["unaddressed_comments"]:
 for ua in traceability["unaddressed_comments"]:
 print(f" ⚠️ {ua['reviewer']} #{ua['comment_number']} "
 f"({ua['severity']}): {ua['expected_section']}")

 # summarysave
 summary = {
 "round": round_number,
 "timestamp": datetime.now.isoformat,
 "diff_stats": stats,
 "sections_changed": diff["sections_changed"],
 "traceability": traceability,
 }
 summary_path = BASE_DIR / "manuscript" / "revision_summary.json"
 with open(summary_path, "w", encoding="utf-8") as f:
 json.dump(summary, f, indent=2, ensure_ascii=False)
 print(f"\n → summarysave: {summary_path}")

 print("\n" + "=" * 60)
 print("Done!")
 print("=" * 60)

 return diff, traceability
```

## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    """Generic REST API data retrieval with error handling."""
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` summarizing methods, results, and interpretation

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `manuscript/versions/vN_original.md` | | Phase 1 |
| `manuscript/versions/vN_revised.md` | | Phase 1 |
| `manuscript/versions/vN_*.json` | data | Phase 1 |
| `manuscript/manuscript_tracked.md` | change | Phase 3 |
| `manuscript/revision_summary.json` | | Phase 4 |

### 

| | addition | deletion | for |
|---|---|---|---|
| `markdown` | `<span style="color:blue">` | `~~<span style="color:red">~~` | Web / for |
| `latex` | `\textcolor{blue}{}` | `\st{\textcolor{red}{}}` | LaTeX for |
| `track_changes` | `[++text++]` | `[--text--]` | |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-peer-review-response` | `response_mapping.json` from-supportreference |
| `scientific-academic-writing` | `manuscript.md` 's |
| `scientific-critical-review` | 's cell |
| `scientific-paper-quality` | 'smetricscomparison |
| `scientific-latex-formatter` | LaTeX |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Writing/Review)

Before execution, define:
- [ ] **Target venue**: journal name, word/page limit, citation style
- [ ] **Document structure**: required sections (IMRaD / custom)
- [ ] **Quality standard**: PRISMA / CONSORT / ARRIVE as applicable
- [ ] **Completeness check**: all required sections present

#### Pass Criteria
- All citations verifiable (DOI or PMID present)
- No placeholder text remaining ([TODO], [CITE], etc.)
- Figure/table references match actual figures/tables
- Word count within target range
### Verification Loop

```
Phase 1: PLAN
  |-- Define eval criteria (above checklist)
  |-- Confirm input data availability and format
  |-- Select analysis methods with justification
  +-- Estimate resource requirements (time, memory, API calls)

Phase 2: EXECUTE
  |-- Run analysis pipeline step-by-step
  |-- Save intermediate results after each major step
  |-- Log execution time per step
  +-- Capture warnings/errors without stopping

Phase 3: VERIFY
  |-- Check all Pass Criteria (above)
  |-- Validate output file existence and non-empty
  |-- Cross-check numeric results for sanity (ranges, signs, units)
  |-- Verify figures are readable and correctly labeled
  +-- Run regression check: did existing outputs break?

Phase 4: RECOVER (on failure)
  |-- Identify failed phase and root cause
  |-- Isolate minimum reproducer
  |-- Apply fix and re-run only failed phase
  |-- Log fix as reusable pattern
  +-- If unrecoverable: document limitation and partial results

Phase 5: REPORT
  |-- Generate report.md with all sections
  |-- Embed all figures with captions
  |-- Save numeric results as JSON/CSV
  |-- List all generated files
  +-- Record execution metadata (duration, versions, seed)
```

### Quality Gates

| Gate | Check | Required |
|------|-------|----------|
| G1 | All figures saved to `figures/` (not `plt.show()`) | MUST |
| G2 | All figures embedded in `report.md` | MUST |
| G3 | Numeric results saved as JSON/CSV in `results/` | MUST |
| G4 | Report includes methods, results, discussion | MUST |
| G5 | All figure/table text is English-only | MUST |
| G6 | No hardcoded paths (use `Path` / config) | MUST |
| G7 | Random seed set and documented | MUST |
| G8 | Execution time logged | RECOMMENDED |
| G9 | Input validation performed | RECOMMENDED |
| G10 | Error messages are actionable | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | Data formatting, file I/O, unit conversion |
| Implementation | `standard` (sonnet-class) | Analysis code, pipeline execution, plotting |
| Reasoning | `premium` (opus-class) | Hypothesis generation, result interpretation, review |

### Sub-Agent Orchestration

When the task is complex, split into parallel sub-agents:

```
Orchestrator (this skill)
|-- Agent 1: Data preparation and validation
|-- Agent 2: Core analysis / computation
|-- Agent 3: Visualization and figure generation
+-- Agent 4: Report writing and quality check
```

Each sub-agent receives:
- Specific scope (what to do)
- Input specification (what data to use)
- Output specification (what files to produce)
- Quality gate subset (which gates to check)

### Token Optimization

- Load only the sub-skill needed for the current task
- Compact context after each major phase (discard intermediate logs)
- Use structured output (JSON) over prose for intermediate results
- Prefer code templates over natural language descriptions
- Cache expensive computations (API calls, model training)

### Error Recovery Protocol

```python
def execute_with_recovery(pipeline_steps, max_retries=2):
    results = {}
    for step in pipeline_steps:
        for attempt in range(max_retries + 1):
            try:
                results[step.name] = step.execute()
                break
            except Exception as e:
                if attempt < max_retries:
                    log(f"Step '{step.name}' failed (attempt {attempt+1}): {e}")
                    step.adjust_params()  # reduce batch size, increase timeout
                else:
                    log(f"Step '{step.name}' unrecoverable: {e}")
                    results[step.name] = {"status": "failed", "error": str(e)}
    return results
```
