---
name: scientific-supplementary-generator
description: |
 Supplementary materials generator skill. Supplementary data preparation, extended methods writing, supplementary table/figure organization, and SI document formatting.
tu_tools:
 - key: crossref
 name: Crossref
 description: 's citationdatareference
---

# Scientific Supplementary Information Generator

paper's Supplementary Information (SI) analysisresultspapersfromautomatedgeneratesskill。
's SI 、Figure S / Table S / Methods S 's number、
papersfrom'sreferenceconsistency check、citation's is performed。

## When to Use

- paperpapers's 、Supplementary Information is createdand
- papers additionfigures/tablesmethoddatawhen needed
- 's SI necessary and
- papers and SI 's phasereference（Figure S1, Table S1 ）'swhen needed
- fromadditiondata's and

## Quick Start

## 1. SI generationworkflow

```
papers (manuscript.md) + analysisresults (results/, figures/)
 ├─ Phase 1: SI 's
 │ ├─ papersfromreference Figure S / Table S extraction
 │ ├─ figures/ papersfor's figure
 │ ├─ results/ 'sdetailsdata（results）addition
 │ └─ Methods 's detailsprocedure papers also 's
 ├─ Phase 2: SI configuration
 │ ├─ Supplementary Figures 
 │ ├─ Supplementary Tables 
 │ ├─ Supplementary Methods 
 │ └─ Supplementary References 
 ├─ Phase 3: numbersystemreferenceconsistency check
 │ ├─ Figure S1, S2,... 'sverification
 │ ├─ papers's "Figure S1" reference SI verification
 │ └─ SI 'sfigures/tablespapersfromreferenceverification
 └─ Phase 4: filesave
 ├─ manuscript/supplementary.md
 ├─ manuscript/supplementary_figures/ (necessary)
 └─ manuscript/si_crossref_report.json
```

## 2. SI 

```markdown
## SI 

| | SI title | figurenumbershapeformula | tablenumbershapeformula | file |
|---|---|---|---|---|
| Nature system | Supplementary Information | Supplementary Fig. 1 | Supplementary Table 1 | single PDF |
| Science system | Supplementary Materials | fig. S1 | table S1 | single PDF |
| ACS system | Supporting Information | Figure S1 | Table S1 | single PDF |
| IEEE system | Supplementary Material | Fig. S1 | TABLE S-I | file |
| Elsevier system | Appendix A / Supplementary data | Fig. A.1 | Table A.1 | Appendix shapeformula |
```

## 3. SI 's automated

```python
def collect_si_candidates(manuscript_path, figures_dir, results_dir):
 """
 papers and analysisresultsdirectoryfrom SI automated.

 Args:
 manuscript_path: Path — papers (manuscript.md)
 figures_dir: Path — figures/ directory
 results_dir: Path — results/ directory

 Returns:
 dict: SI 's
 """
 import re
 from pathlib import Path

 # papersload
 with open(manuscript_path, "r", encoding="utf-8") as f:
 manuscript_text = f.read

 # papers's Figure reference extraction
 main_figs = set(re.findall(
 r'!\[(?:Fig(?:ure)?\.?\s*\d+)\]\(figures/([^)]+)\)', manuscript_text
 ))

 # papers's SI reference extraction
 si_refs = re.findall(
 r'(?:Figure|Fig\.?|Table|Supplementary\s+(?:Fig|Table))\s*S(\d+)',
 manuscript_text, re.IGNORECASE
 )

 # figures/ 's allfile
 all_figs = set
 if figures_dir.exists:
 all_figs = {
 f.name for f in figures_dir.iterdir
 if f.suffix.lower in ('.png', '.svg', '.pdf', '.jpg', '.jpeg')
 }

 # papersfor'sfigure → SI 
 unused_figs = all_figs - main_figs

 # results/ 'sdetailsdata
 detail_data = []
 if results_dir.exists:
 for f in results_dir.iterdir:
 if f.suffix == '.csv' and f.name not in ('analysis_summary.json',):
 detail_data.append(f.name)

 candidates = {
 "supplementary_figures": sorted(unused_figs),
 "supplementary_tables": detail_data,
 "si_references_in_main": sorted(set(si_refs)),
 "main_figures": sorted(main_figs),
 }

 print(f" SI :")
 print(f" figure: {len(candidates['supplementary_figures'])} items")
 print(f" table: {len(candidates['supplementary_tables'])} items")
 print(f" papers's SI reference: {len(candidates['si_references_in_main'])} items")

 return candidates
```

## 4. SI generation

```python
def generate_supplementary(candidates, journal_format="imrad",
 title="", authors="", filepath=None):
 """
 SI Markdown asgenerationsave.

 Args:
 candidates: dict — collect_si_candidates 's value
 journal_format: str — journal format (nature/science/acs/ieee/elsevier/imrad)
 title: str — papertitle
 authors: str — author
 filepath: Path — output destination（: manuscript/supplementary.md）
 """
 import datetime
 from pathlib import Path

 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "supplementary.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 # settings
 fmt = _get_si_format(journal_format)

 content = f"""# {fmt['title_prefix']}
# {title}

{authors}

> Generated: {datetime.datetime.now.strftime('%Y-%m-%d %H:%M')}

"""

 # Supplementary Figures
 sup_figs = candidates.get("supplementary_figures", [])
 if sup_figs:
 content += f"## {fmt['fig_section_title']}\n\n"
 for i, fig_name in enumerate(sup_figs, 1):
 fig_label = fmt['fig_prefix'].format(n=i)
 content += f"![{fig_label}](figures/{fig_name})\n\n"
 content += f"**{fig_label}.** [: {fig_name} 's]\n\n"

 # Supplementary Tables
 sup_tables = candidates.get("supplementary_tables", [])
 if sup_tables:
 content += f"## {fmt['table_section_title']}\n\n"
 for i, table_name in enumerate(sup_tables, 1):
 table_label = fmt['table_prefix'].format(n=i)
 content += f"**{table_label}.** [: {table_name} 's]\n\n"
 content += f"data: `results/{table_name}`\n\n"

 # Supplementary Methods
 content += f"""## {fmt['methods_section_title']}

### S1. [additionexperimentmethod'sdetails]

[papers Methods detailsprocedure]

### S2. [additionanalysismethod'sdetails]

[parameterssettings、'sdetails、]

"""

 # Supplementary References
 content += f"""## {fmt['refs_section_title']}

[SI 's citationliterature]

"""

 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)

 print(f" → SI save: {filepath}")
 return filepath


def _get_si_format(journal_format):
 """'s SI settings is returned。"""
 formats = {
 "nature": {
 "title_prefix": "Supplementary Information for:",
 "fig_section_title": "Supplementary Figures",
 "table_section_title": "Supplementary Tables",
 "methods_section_title": "Supplementary Methods",
 "refs_section_title": "Supplementary References",
 "fig_prefix": "Supplementary Fig. {n}",
 "table_prefix": "Supplementary Table {n}",
 },
 "science": {
 "title_prefix": "Supplementary Materials for:",
 "fig_section_title": "Supplementary Figures",
 "table_section_title": "Supplementary Tables",
 "methods_section_title": "Materials and Methods",
 "refs_section_title": "References",
 "fig_prefix": "fig. S{n}",
 "table_prefix": "table S{n}",
 },
 "acs": {
 "title_prefix": "Supporting Information for:",
 "fig_section_title": "Supporting Figures",
 "table_section_title": "Supporting Tables",
 "methods_section_title": "Supporting Methods",
 "refs_section_title": "Supporting References",
 "fig_prefix": "Figure S{n}",
 "table_prefix": "Table S{n}",
 },
 "ieee": {
 "title_prefix": "Supplementary Material for:",
 "fig_section_title": "Supplementary Figures",
 "table_section_title": "Supplementary Tables",
 "methods_section_title": "Supplementary Methods",
 "refs_section_title": "Supplementary References",
 "fig_prefix": "Fig. S{n}",
 "table_prefix": "TABLE S-{n}",
 },
 "elsevier": {
 "title_prefix": "Appendix A. Supplementary data for:",
 "fig_section_title": "Supplementary Figures",
 "table_section_title": "Supplementary Tables",
 "methods_section_title": "Supplementary Methods",
 "refs_section_title": "References",
 "fig_prefix": "Fig. A.{n}",
 "table_prefix": "Table A.{n}",
 },
 }
 return formats.get(journal_format, formats.get("acs")) # ACS
```

## 5. papers–SI 's phasereference

```python
def check_si_crossrefs(manuscript_path, si_path, filepath=None):
 """
 papers and SI 's phasereferenceverification.

 content:
 - papers's "Figure S1" reference SI 
 - SI 's Figure S / Table S papersfromreference（）
 - number's (S1, S2, S3... )

 Returns:
 dict: verificationresults
 """
 import re, json, datetime
 from pathlib import Path

 with open(manuscript_path, "r", encoding="utf-8") as f:
 main_text = f.read
 with open(si_path, "r", encoding="utf-8") as f:
 si_text = f.read

 # papers's SI reference extraction
 main_fig_refs = set(re.findall(
 r'(?:Supplementary\s+)?(?:Fig(?:ure)?\.?\s*S|fig\.\s*S)(\d+)',
 main_text, re.IGNORECASE
 ))
 main_table_refs = set(re.findall(
 r'(?:Supplementary\s+)?(?:Table\s*S|table\s*S)[\-]?(\d+)',
 main_text, re.IGNORECASE
 ))

 # SI 's Figure/Table definition extraction
 si_fig_defs = set(re.findall(
 r'\*\*(?:Supplementary\s+)?(?:Fig(?:ure)?\.?\s*S?|fig\.\s*S?)(\d+)',
 si_text, re.IGNORECASE
 ))
 si_table_defs = set(re.findall(
 r'\*\*(?:Supplementary\s+)?(?:Table\s*S?|TABLE\s*S[\-]?)(\d+)',
 si_text, re.IGNORECASE
 ))

 # 
 issues = []

 # papers reference SI definition
 missing_in_si = main_fig_refs - si_fig_defs
 for ref in sorted(missing_in_si):
 issues.append({
 "type": "MISSING_IN_SI",
 "severity": "Critical",
 "message": f"Figure S{ref} papers reference SI definition",
 })

 missing_tables_in_si = main_table_refs - si_table_defs
 for ref in sorted(missing_tables_in_si):
 issues.append({
 "type": "MISSING_IN_SI",
 "severity": "Critical",
 "message": f"Table S{ref} papers reference SI definition",
 })

 # SI definition papersfromreference（）
 orphan_figs = si_fig_defs - main_fig_refs
 for ref in sorted(orphan_figs):
 issues.append({
 "type": "ORPHAN_IN_SI",
 "severity": "Minor",
 "message": f"Figure S{ref} SI definition papersfromreference",
 })

 orphan_tables = si_table_defs - main_table_refs
 for ref in sorted(orphan_tables):
 issues.append({
 "type": "ORPHAN_IN_SI",
 "severity": "Minor",
 "message": f"Table S{ref} SI definition papersfromreference",
 })

 # number's
 for label, nums in [("Figure S", si_fig_defs), ("Table S", si_table_defs)]:
 if nums:
 int_nums = sorted(int(n) for n in nums)
 expected = list(range(1, max(int_nums) + 1))
 gaps = set(expected) - set(int_nums)
 for g in sorted(gaps):
 issues.append({
 "type": "NUMBERING_GAP",
 "severity": "Major",
 "message": f"{label}{g} （{label}1〜{label}{max(int_nums)} 's）",
 })

 result = {
 "timestamp": datetime.datetime.now.isoformat,
 "main_fig_refs": sorted(main_fig_refs),
 "main_table_refs": sorted(main_table_refs),
 "si_fig_defs": sorted(si_fig_defs),
 "si_table_defs": sorted(si_table_defs),
 "issues": issues,
 "status": "PASS" if not any(i["severity"] == "Critical" for i in issues) else "FAIL",
 }

 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "si_crossref_report.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(result, f, indent=2, ensure_ascii=False)

 print(f" → SI phasereference: {result['status']}")
 print(f" papers→SIreference: Figure S × {len(main_fig_refs)}, Table S × {len(main_table_refs)}")
 print(f" problem: {len(issues)} items")
 if issues:
 for issue in issues:
 print(f" [{issue['severity']}] {issue['message']}")

 return result
```

## 6. SI generationPipeline Integration

```python
def run_si_pipeline(manuscript_path, figures_dir=None, results_dir=None,
 journal_format="imrad", title="", authors=""):
 """
 SI generationpipeline is executed。

 1. SI 's
 2. SI 'sgeneration
 3. phasereference
 """
 from pathlib import Path

 if figures_dir is None:
 figures_dir = BASE_DIR / "figures"
 if results_dir is None:
 results_dir = BASE_DIR / "results"

 print("=" * 60)
 print("Supplementary Information Generator")
 print("=" * 60)

 # Phase 1: 
 print("\n[Phase 1] SI 's...")
 candidates = collect_si_candidates(manuscript_path, figures_dir, results_dir)

 # Phase 2: SI generation
 print("\n[Phase 2] SI 'sgeneration...")
 si_path = generate_supplementary(
 candidates, journal_format=journal_format,
 title=title, authors=authors,
 )

 # Phase 3: phasereference
 print("\n[Phase 3] phasereference...")
 crossref = check_si_crossrefs(manuscript_path, si_path)

 print("\n" + "=" * 60)
 print(f"SI generationDone! (: {crossref['status']})")
 print("=" * 60)

 return {"si_path": si_path, "crossref": crossref}
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `crossref` | Crossref | 's citationdatareference |

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `manuscript/supplementary.md` | SI （Markdown） | Phase 2 completion |
| `manuscript/si_crossref_report.json` | phasereferenceresults（JSON） | Phase 3 completion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-academic-writing` | papers (`manuscript/manuscript.md`) inputasfor |
| `scientific-publication-figures` | `figures/` 's forfigure SI asautomated |
| `scientific-pipeline-scaffold` | `results/` 's detailsdata SI Table as |
| `scientific-critical-review` | 's fix additionfigures/tables SI |
| `scientific-latex-formatter` | SI 's LaTeX transformationfor |

```
---

## Harness Optimization (v0.4.0)

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
