---
name: scientific-citation-checker
description: |
 's citationliterature's automatedsearch is performedskill。
 referenceextraction、DOI/titleautomatedsearch、citationmin、
 verification、 is executed。
 「citation」「referenceliteraturesearch」「citation check」 。
---

# Scientific Citation Checker

's referenceliterature and paperscitation's、、
automatedverificationskill。

## When to Use

- 's referenceliterature papers's citation andverificationwhen needed
- for/againstcitationverificationwhen needed
- citation'sverificationwhen needed
- citation andcitation（papers referenceliterature）when needed
- DOI and data referenceliteratureinformation automatedwhen needed

## Quick Start

## 1. verificationworkflow

```
 (manuscript/manuscript.md) + reference
 ├─ Phase 1: citationextraction
 │ ├─ papers's citation [1], (Author, 2024) extraction
 │ ├─ referenceliterature（References ） analysis
 │ └─ citationand referenceliteratureentry'ssupportmapping
 ├─ Phase 2: consistency check
 │ ├─ citation: referenceliterature papers citation
 │ ├─ citation: papers citation referenceliterature
 │ ├─ number: [1], [2], [3]... number
 │ └─ : literature different multipletimes
 ├─ Phase 3: 
 │ ├─ -support: comparisonresearch citation
 │ ├─ citationdegree: Introduction/Discussion especially
 │ └─ citationrate: citation
 ├─ Phase 4: dataverification
 │ ├─ DOI : eachcitation's DOI effective
 │ ├─ data: titleauthoretc.'s automated
 │ └─ : eachcitation's
 └─ Phase 5: reportoutput
 └─ manuscript/citation_report.json
```

## 2. citationextraction

```python
import re
import json
from pathlib import Path


CITATION_PATTERNS = {
 "numeric": r'\[(\d+(?:[-–,\s]\d+)*)\]',
 "author_year": r'\(([A-Z][a-z]+(?:\s(?:et\sal\.|&\s[A-Z][a-z]+))?,\s*\d{4}(?:;\s*[A-Z][a-z]+(?:\s(?:et\sal\.|&\s[A-Z][a-z]+))?,\s*\d{4})*)\)',
 "superscript": r'(?<!\[)\b(\d+(?:[-–,]\d+)*)\b(?=[,.]?\s)',
}


def extract_citations(md_text, citation_style="numeric"):
 """
 fromcitation is extracted。

 Args:
 md_text: str — 
 citation_style: str — "numeric", "author_year", "superscript"

 Returns:
 dict: {
 "markers": [{"text": "[1]", "line": 10, "keys": [1]},...],
 "unique_keys": [1, 2, 3,...],
 "style": "numeric"
 }
 """
 pattern = CITATION_PATTERNS.get(citation_style, CITATION_PATTERNS["numeric"])
 markers = []
 unique_keys = set

 for line_num, line in enumerate(md_text.split('\n'), 1):
 for m in re.finditer(pattern, line):
 raw = m.group(1)
 keys = _parse_citation_keys(raw, citation_style)
 markers.append({
 "text": m.group(0),
 "line": line_num,
 "keys": keys,
 })
 unique_keys.update(keys)

 return {
 "markers": markers,
 "unique_keys": sorted(unique_keys) if citation_style == "numeric" else sorted(unique_keys),
 "style": citation_style,
 }


def _parse_citation_keys(raw, style):
 """citation's from is extracted。"""
 if style == "numeric":
 keys = []
 for part in re.split(r'[,\s]+', raw):
 part = part.strip
 if '–' in part or '-' in part:
 sep = '–' if '–' in part else '-'
 start, end = part.split(sep)
 keys.extend(range(int(start.strip), int(end.strip) + 1))
 elif part.isdigit:
 keys.append(int(part))
 return keys
 elif style == "author_year":
 return [k.strip for k in raw.split(';')]
 return [raw]
```

## 3. referenceliteratureanalysis

```python
def parse_reference_list(md_text):
 """
 's References fromreferenceliteratureanalysis.

 Returns:
 list[dict]: [
 {"index": 1, "raw": "Author A. Title...", "doi": "10.xxx",
 "authors": "Author A", "title": "Title", "year": "2024",
 "journal": "Journal Name"},
...
 ]
 """
 # References extraction
 ref_section = re.search(
 r'(?:^#{1,2}\s*References\s*$)(.*)',
 md_text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
 )
 if not ref_section:
 return []

 ref_text = ref_section.group(1)
 references = []

 # numbershapeformula: 1. Author A. Title...
 numbered = re.findall(r'^\s*(\d+)[.\)]\s*(.+)$', ref_text, re.MULTILINE)
 if numbered:
 for idx, raw in numbered:
 ref = _parse_single_reference(raw, int(idx))
 references.append(ref)
 return references

 # shapeformula: - Author A. Title...
 bullets = re.findall(r'^\s*[-*]\s*(.+)$', ref_text, re.MULTILINE)
 if bullets:
 for i, raw in enumerate(bullets, 1):
 ref = _parse_single_reference(raw, i)
 references.append(ref)
 return references

 return references


def _parse_single_reference(raw, index):
 """single's referenceliteratureentry structure."""
 ref = {
 "index": index,
 "raw": raw.strip,
 "doi": None,
 "authors": None,
 "title": None,
 "year": None,
 "journal": None,
 }

 # DOI extraction
 doi_match = re.search(r'(?:doi:\s*|https?://doi\.org/)?(10\.\d{4,}/[^\s,]+)', raw, re.IGNORECASE)
 if doi_match:
 ref["doi"] = doi_match.group(1).rstrip('.')

 # 'sextraction
 year_match = re.search(r'\b((?:19|20)\d{2})\b', raw)
 if year_match:
 ref["year"] = year_match.group(1)

 return ref
```

## 4. consistency check

```python
def check_citation_consistency(citations, references):
 """
 papers's citation and referenceliterature'sverification.

 Args:
 citations: dict — extract_citations 's results
 references: list[dict] — parse_reference_list 's results

 Returns:
 dict: {
 "orphan_refs": [...], # referenceliterature paperscitation
 "unresolved_cites": [...], # papers citation
 "duplicates": [...], # entry
 "numbering_gaps": [...], # number's
 "total_refs": int,
 "total_citations": int,
 "passed": bool
 }
 """
 cited_keys = set(citations["unique_keys"])
 ref_keys = set(r["index"] for r in references)

 # referenceliterature（paperscitation）
 orphan_refs = sorted(ref_keys - cited_keys)

 # citation（papers citation）
 unresolved = sorted(cited_keys - ref_keys)

 # number's
 if citations["style"] == "numeric" and ref_keys:
 expected = set(range(1, max(ref_keys) + 1))
 gaps = sorted(expected - ref_keys)
 else:
 gaps = []

 # （DOI ）
 duplicates = _find_duplicate_references(references)

 passed = (len(orphan_refs) == 0 and len(unresolved) == 0
 and len(gaps) == 0 and len(duplicates) == 0)

 return {
 "orphan_refs": orphan_refs,
 "unresolved_cites": unresolved,
 "duplicates": duplicates,
 "numbering_gaps": gaps,
 "total_refs": len(references),
 "total_citations": len(cited_keys),
 "passed": passed,
 }


def _find_duplicate_references(references):
 """DOI ortitledegree referenceliterature."""
 duplicates = []
 doi_map = {}

 for ref in references:
 if ref.get("doi"):
 doi = ref["doi"].lower.strip
 if doi in doi_map:
 duplicates.append({
 "ref_a": doi_map[doi]["index"],
 "ref_b": ref["index"],
 "reason": f" DOI: {doi}",
 })
 else:
 doi_map[doi] = ref

 return duplicates
```

## 5. 

```python
EVIDENCE_INDICATORS = [
 r'(?:has been|have been)\s+(?:shown|demonstrated|reported|observed)',
 r'(?:previous|prior|earlier|recent)\s+(?:studies?|work|research|findings?)',
 r'(?:according to|as reported by|as shown by)',
 r'(?:it is (?:well )?known|it has been established)',
 r'(?:compared (?:to|with)|in contrast (?:to|with)|consistent with)',
 r'(?:following|based on)\s+(?:the )?(?:method|approach|protocol)',
 r'\b(?:typically|generally|commonly|often|usually)\b.*\b(?:used|observed|found)\b',
]


def check_citation_coverage(md_text, citations):
 """
 papers's research citationverifies。

 Returns:
 dict: {
 "uncited_claims": [{"line": 10, "text": "...", "indicator": "..."}],
 "section_density": {"Introduction": 5.2, "Methods": 1.1,...},
 "self_citation_rate": 0.15,
 }
 """
 uncited_claims = []

 for line_num, line in enumerate(md_text.split('\n'), 1):
 for pattern in EVIDENCE_INDICATORS:
 if re.search(pattern, line, re.IGNORECASE):
 # 's citationverification
 has_citation = any(
 m["line"] == line_num for m in citations["markers"]
 )
 if not has_citation:
 uncited_claims.append({
 "line": line_num,
 "text": line.strip[:100],
 "indicator": pattern,
 })
 break # 1 items 1 items'swarning

 # citationdegree
 section_density = _calculate_section_density(md_text, citations)

 return {
 "uncited_claims": uncited_claims,
 "section_density": section_density,
 "total_uncited": len(uncited_claims),
 }


def _calculate_section_density(md_text, citations):
 """and 's citationdegree（citationnumber/count / number/count） calculation."""
 sections = re.split(r'^#{1,2}\s+', md_text, flags=re.MULTILINE)
 density = {}

 current_line = 0
 for section in sections:
 lines = section.split('\n')
 header = lines[0].strip if lines else "Unknown"
 n_paragraphs = max(1, len([l for l in lines if l.strip]))
 n_citations = sum(
 1 for m in citations["markers"]
 if current_line < m["line"] <= current_line + len(lines)
 )
 density[header[:30]] = round(n_citations / n_paragraphs, 2)
 current_line += len(lines)

 return density
```

## 6. reportgenerationpipeline

```python
def run_citation_check(manuscript_path, citation_style="numeric", filepath=None):
 """
 citationpipeline is executed。

 Args:
 manuscript_path: Path — manuscript file path
 citation_style: str — citation
 filepath: Path — report output path

 Returns:
 dict: allresultsincluding
 """
 from pathlib import Path

 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "citation_report.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 print("=" * 60)
 print("Citation Checker Pipeline")
 print("=" * 60)

 with open(manuscript_path, "r", encoding="utf-8") as f:
 md_text = f.read

 # Phase 1: citationextraction
 print("\n[Phase 1] citationextraction...")
 citations = extract_citations(md_text, citation_style)
 print(f" → {len(citations['markers'])} units's citation、{len(citations['unique_keys'])} units's")

 # Phase 2: referenceliteratureanalysis
 print("\n[Phase 2] referenceliterature analysis...")
 references = parse_reference_list(md_text)
 print(f" → {len(references)} items's referenceliteratureentry")

 # Phase 3: consistency check
 print("\n[Phase 3] citation-referenceliterature's verification...")
 consistency = check_citation_consistency(citations, references)
 status = "✅ PASS" if consistency["passed"] else "⚠️ ISSUES FOUND"
 print(f" → {status}")
 if consistency["orphan_refs"]:
 print(f" → referenceliterature: {consistency['orphan_refs']}")
 if consistency["unresolved_cites"]:
 print(f" → citation: {consistency['unresolved_cites']}")

 # Phase 4: 
 print("\n[Phase 4] citationverification...")
 coverage = check_citation_coverage(md_text, citations)
 print(f" → citation's possible: {coverage['total_uncited']} ")

 # reportintegration
 report = {
 "manuscript": str(manuscript_path),
 "citation_style": citation_style,
 "summary": {
 "total_citations": consistency["total_citations"],
 "total_references": consistency["total_refs"],
 "consistency_passed": consistency["passed"],
 "uncited_claims": coverage["total_uncited"],
 },
 "consistency": consistency,
 "coverage": coverage,
 }

 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(report, f, indent=2, ensure_ascii=False)

 print(f"\n → report save: {filepath}")
 print("=" * 60)

 return report
```

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `manuscript/citation_report.json` | JSON report | completion |

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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

### itemlist

| item | | importantdegree |
|---|---|---|
| referenceliterature | referenceliterature paperscitation | Warning |
| citation | papers's citationnumber | Error |
| number | [1], [3] 's | Warning |
| referenceliterature | DOI 'sentry | Warning |
| citation's | citation | Info |
| citationdegree | Introduction/Discussion 's citation few | Info |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-academic-writing` | input: `manuscript/manuscript.md` 's citationverification |
| `scientific-latex-formatter` | verification's citation BibTeX transformation |
| `scientific-critical-review` | citation'sevaluation |
| `scientific-hypothesis-pipeline` | hypothesisand citation's supportverification |

```
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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
