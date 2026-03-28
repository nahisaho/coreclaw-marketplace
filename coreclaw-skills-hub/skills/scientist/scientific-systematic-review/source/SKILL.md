---
name: scientific-systematic-review
description: |
 Systematic review skill. PRISMA-compliant systematic review workflow, literature screening, data extraction, risk of bias assessment, and evidence synthesis.
---

# Scientific Systematic Review

PRISMA 2020 
systematic review's methodpipeline is provided。

## When to Use

- systematic review's search is designedand
- title/'sworkflowwhen needed
- (RoB 2, ROBINS-I, NOS) evaluation is performedand
- PRISMA figure is generatedand
- systematic review's dataextractiontable is createdand

---

## Quick Start

## 1. searchdesign (PICO → )

```python
import pandas as pd
import json


def design_search_strategy(pico, databases=None):
 """
 PICO frameworkfromsearchdesign。

 Parameters:
 pico: dict — {"P": "...", "I": "...", "C": "...", "O": "..."}
 databases: list — ["PubMed", "Embase", "Cochrane", "Web of Science"]
 """
 if databases is None:
 databases = ["PubMed", "Embase", "Cochrane"]

 strategy = {
 "pico": pico,
 "databases": databases,
 "search_blocks": [],
 }

 # P (Population) block
 p_terms = pico.get("P", "").split(",")
 p_block = {
 "concept": "Population",
 "terms": [t.strip for t in p_terms],
 "mesh_terms": [], # manual MeSH addition
 "boolean": "OR",
 }

 # I (Intervention) block
 i_terms = pico.get("I", "").split(",")
 i_block = {
 "concept": "Intervention",
 "terms": [t.strip for t in i_terms],
 "mesh_terms": [],
 "boolean": "OR",
 }

 # C (Comparison) block
 c_terms = pico.get("C", "").split(",")
 c_block = {
 "concept": "Comparison",
 "terms": [t.strip for t in c_terms if t.strip],
 "boolean": "OR",
 }

 # O (Outcome) block
 o_terms = pico.get("O", "").split(",")
 o_block = {
 "concept": "Outcome",
 "terms": [t.strip for t in o_terms],
 "boolean": "OR",
 }

 strategy["search_blocks"] = [p_block, i_block]
 if c_block["terms"]:
 strategy["search_blocks"].append(c_block)
 if o_block["terms"]:
 strategy["search_blocks"].append(o_block)

 # PubMed generation
 pubmed_parts = []
 for block in strategy["search_blocks"]:
 terms = [f'"{t}"' for t in block["terms"]]
 mesh = [f'"{m}"[MeSH]' for m in block.get("mesh_terms", [])]
 all_terms = terms + mesh
 pubmed_parts.append(f"({' OR '.join(all_terms)})")

 strategy["pubmed_query"] = " AND ".join(pubmed_parts)

 print(f"Search strategy: {len(strategy['search_blocks'])} blocks, "
 f"{len(databases)} databases")
 print(f"PubMed query: {strategy['pubmed_query'][:200]}...")
 return strategy
```

## 2. workflow

```python
def screening_workflow(records_df, stage="title_abstract",
 inclusion_criteria=None,
 exclusion_criteria=None):
 """
 workflow。

 Parameters:
 records_df: DataFrame — columns: [id, title, abstract, source]
 stage: "title_abstract" or "fulltext"
 inclusion_criteria: list — criteria
 exclusion_criteria: list — criteria
 """
 if inclusion_criteria is None:
 inclusion_criteria = [
 "Published in English or Japanese",
 "Human subjects",
 "Original research (not review/editorial)",
 ]
 if exclusion_criteria is None:
 exclusion_criteria = [
 "Case reports (n < 5)",
 "Conference abstracts only",
 "Animal studies only",
 ]

 # 
 initial_count = len(records_df)
 records_df = records_df.drop_duplicates(subset=["title"], keep="first")
 duplicates_removed = initial_count - len(records_df)

 # resultstemplate
 records_df["decision"] = "pending"
 records_df["excluded_reason"] = ""
 records_df["screener"] = ""

 result = {
 "stage": stage,
 "total_records": initial_count,
 "duplicates_removed": duplicates_removed,
 "unique_records": len(records_df),
 "inclusion_criteria": inclusion_criteria,
 "exclusion_criteria": exclusion_criteria,
 }

 print(f"Screening ({stage}): {initial_count} records → "
 f"{duplicates_removed} duplicates removed → "
 f"{len(records_df)} to screen")
 return records_df, result
```

## 3. evaluation

```python
def risk_of_bias_assessment(studies_df, tool="RoB2"):
 """
 evaluation。

 Parameters:
 studies_df: DataFrame — columns: [study_id, study_type,...]
 tool: "RoB2" (RCT), "ROBINS-I" (randomization), "NOS" (observationresearch)
 """
 if tool == "RoB2":
 # Cochrane RoB 2 — 5 
 domains = [
 "D1: Randomization process",
 "D2: Deviations from interventions",
 "D3: Missing outcome data",
 "D4: Measurement of the outcome",
 "D5: Selection of the reported result",
 ]
 levels = ["Low", "Some concerns", "High"]
 elif tool == "ROBINS-I":
 domains = [
 "D1: Confounding",
 "D2: Selection of participants",
 "D3: Classification of interventions",
 "D4: Deviations from intended interventions",
 "D5: Missing data",
 "D6: Measurement of outcomes",
 "D7: Selection of the reported result",
 ]
 levels = ["Low", "Moderate", "Serious", "Critical", "NI"]
 elif tool == "NOS":
 domains = [
 "Selection (0-4 stars)",
 "Comparability (0-2 stars)",
 "Outcome/Exposure (0-3 stars)",
 ]
 levels = ["0-3 (low quality)", "4-6 (moderate)", "7-9 (high quality)"]
 else:
 raise ValueError(f"Unknown tool: {tool}")

 # evaluationtemplategeneration
 assessments = []
 for _, study in studies_df.iterrows:
 assessment = {
 "study_id": study.get("study_id", ""),
 "tool": tool,
 }
 for domain in domains:
 assessment[domain] = "pending"
 assessment["overall"] = "pending"
 assessments.append(assessment)

 df = pd.DataFrame(assessments)
 print(f"RoB assessment ({tool}): {len(df)} studies, "
 f"{len(domains)} domains")
 return df
```

## 4. PRISMA figuregeneration

```python
def generate_prisma_flowchart(counts, output="figures/prisma_flow.svg"):
 """
 PRISMA 2020 figure'sautomatedgeneration。

 Parameters:
 counts: dict — {
 "databases": {"PubMed": 500, "Embase": 300, "Cochrane": 100},
 "other_sources": 20,
 "duplicates_removed": 150,
 "title_abstract_screened": 770,
 "title_abstract_excluded": 650,
 "fulltext_assessed": 120,
 "fulltext_excluded": {"not_relevant": 30, "wrong_design": 20,...},
 "included_qualitative": 70,
 "included_quantitative": 50,
 }
 """
 import os
 os.makedirs(os.path.dirname(output), exist_ok=True)

 # Mermaid shapeformula PRISMA generation
 db_counts = counts.get("databases", {})
 total_db = sum(db_counts.values)
 other = counts.get("other_sources", 0)
 total = total_db + other
 dedup = counts.get("duplicates_removed", 0)
 screened = counts.get("title_abstract_screened", total - dedup)
 ta_excluded = counts.get("title_abstract_excluded", 0)
 ft_assessed = counts.get("fulltext_assessed", screened - ta_excluded)
 ft_excluded = counts.get("fulltext_excluded", {})
 ft_excluded_total = sum(ft_excluded.values) if isinstance(ft_excluded, dict) else ft_excluded
 qualitative = counts.get("included_qualitative", ft_assessed - ft_excluded_total)
 quantitative = counts.get("included_quantitative", qualitative)

 mermaid = f"""flowchart TD
 A[Databasesearch<br>n={total_db}] --> C[<br>n={total - dedup}]
 B['s<br>n={other}] --> C
 C --> D[title/<br>n={screened}]
 D --> E[<br>n={ta_excluded}]
 D --> F[allevaluation<br>n={ft_assessed}]
 F --> G[<br>n={ft_excluded_total}]
 F --> H[integration<br>n={qualitative}]
 H --> I[amountintegration <br>n={quantitative}]
"""

 # SVG assave (Mermaid CLI or fallback to text)
 mermaid_file = output.replace(".svg", ".mmd")
 with open(mermaid_file, "w") as f:
 f.write(mermaid)

 print(f"PRISMA flow: {total} identified → {qualitative} included")
 print(f" Mermaid source: {mermaid_file}")
 return mermaid_file, counts
```

## 5. dataextractiontemplate

```python
def create_extraction_template(study_type="RCT",
 custom_fields=None):
 """
 systematic reviewfordataextractiontemplate。

 Parameters:
 study_type: "RCT", "cohort", "cross-sectional", "case-control"
 custom_fields: list — additionfield
 """
 base_fields = [
 "study_id", "first_author", "year", "country",
 "study_design", "sample_size", "population",
 "setting",
 ]

 if study_type == "RCT":
 type_fields = [
 "intervention", "comparator", "randomization_method",
 "blinding", "follow_up_duration",
 "primary_outcome", "primary_result",
 "secondary_outcomes", "adverse_events",
 "attrition_rate", "itt_analysis",
 ]
 elif study_type == "cohort":
 type_fields = [
 "exposure", "comparator", "follow_up_duration",
 "primary_outcome", "adjustment_variables",
 "effect_measure", "effect_estimate", "ci_95",
 "p_value", "loss_to_follow_up",
 ]
 else:
 type_fields = [
 "exposure", "outcome", "adjustment_variables",
 "effect_measure", "effect_estimate", "ci_95",
 ]

 all_fields = base_fields + type_fields
 if custom_fields:
 all_fields.extend(custom_fields)

 template = pd.DataFrame(columns=all_fields)
 print(f"Extraction template ({study_type}): {len(all_fields)} fields")
 return template
```

## References

### Output Files

| File | Format |
|---|---|
| `results/search_strategy.json` | JSON |
| `results/screening_records.csv` | CSV |
| `results/risk_of_bias.csv` | CSV |
| `results/data_extraction.csv` | CSV |
| `figures/prisma_flow.mmd` | Mermaid |
| `figures/prisma_flow.svg` | SVG |

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

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-literature-search` | DB search |
| `scientific-meta-analysis` | amountintegration (Forest/Funnel plot) |
| `scientific-critical-review` | evaluation |
| `scientific-academic-writing` | paperwriting |
| `scientific-scientific-schematics` | PRISMA figure |

### Dependencies

`pandas`, `json` (stdlib)
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
