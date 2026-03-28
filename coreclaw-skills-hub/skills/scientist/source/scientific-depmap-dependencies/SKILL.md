---
name: scientific-depmap-dependencies
description: |
 DepMap dependencyskill。Cancer Dependency Map (DepMap) Portal
 API by/viacancercell CRISPR/RNAi dependency
 datageneretrieval。---

# Scientific DepMap Dependencies

Cancer Dependency Map (DepMap) Portal API utilizing
cancercell's CRISPR/RNAi genedependencyretrieval
datagenepipeline is provided。

## When to Use

- cancercell's genedependency (CRISPR/RNAi) is investigatedand
- gene's cancerselectionrequired is evaluatedand
- data andgene expression's correlation is investigatedand
- celldata (tissuetypedisease) is retrievedand
- Cell Model Passports data referencewhen needed

---

## Quick Start

## 1. DepMap cellsearchdata

```python
import requests
import pandas as pd

DEPMAP_API = "https://api.cellmodelpassports.sanger.ac.uk/v1"


def depmap_cell_lines(tissue=None, cancer_type=None,
 limit=50):
 """
 DepMap / Cell Model Passports — cellsearch。

 Parameters:
 tissue: str — tissuetypefilter (example: "Breast")
 cancer_type: str — cancertypefilter
 (example: "Breast Carcinoma")
 limit: int — maximum results
 """
 url = f"{DEPMAP_API}/models"
 params = {"page_size": limit}
 if tissue:
 params["tissue"] = tissue
 if cancer_type:
 params["cancer_type"] = cancer_type

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for model in data.get("data", data
 if isinstance(data, list)
 else []):
 if isinstance(model, dict):
 rows.append({
 "model_id": model.get("model_id", ""),
 "model_name": model.get("model_name", ""),
 "tissue": model.get("tissue", ""),
 "cancer_type": model.get(
 "cancer_type", ""),
 "sample_site": model.get(
 "sample_site", ""),
 "gender": model.get("gender", ""),
 })

 df = pd.DataFrame(rows[:limit])
 print(f"DepMap cell lines: {len(df)} models")
 return df
```

## 2. CRISPR genedependency

```python
def depmap_gene_dependency(gene_symbol,
 dataset="Chronos_Combined"):
 """
 DepMap — genedependencyretrieval。

 Parameters:
 gene_symbol: str — gene symbol (example: "KRAS")
 dataset: str — dataset name
 (example: "Chronos_Combined", "RNAi_merged")
 """
 # DepMap Public Portal download URL
 DEPMAP_PORTAL = "https://depmap.org/portal/api"

 url = f"{DEPMAP_PORTAL}/dataset/search"
 params = {"gene": gene_symbol,
 "dataset": dataset}

 try:
 resp = requests.get(url, params=params,
 timeout=30)
 resp.raise_for_status
 data = resp.json
 except Exception:
 # Fallback: alternative DepMap API
 print(f" DepMap portal fallback for "
 f"{gene_symbol}")
 data = []

 rows = []
 if isinstance(data, list):
 for entry in data:
 if isinstance(entry, dict):
 rows.append({
 "gene": gene_symbol,
 "cell_line": entry.get(
 "cell_line_name", ""),
 "depmap_id": entry.get(
 "depmap_id", ""),
 "dependency_score": entry.get(
 "dependency", 0),
 "dataset": dataset,
 })

 df = pd.DataFrame(rows)
 if not df.empty:
 df = df.sort_values("dependency_score")
 print(f"DepMap dependency: {gene_symbol} "
 f"→ {len(df)} cell lines")
 return df
```

## 3. data

```python
def depmap_drug_sensitivity(compound_name=None,
 limit=100):
 """
 DepMap — Data Retrieval。

 Parameters:
 compound_name: str — compoundfilter
 (example: "Paclitaxel")
 limit: int — maximum results
 """
 url = f"{DEPMAP_API}/drugs"
 params = {"page_size": limit}
 if compound_name:
 params["name"] = compound_name

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for drug in data.get("data", data
 if isinstance(data, list)
 else []):
 if isinstance(drug, dict):
 rows.append({
 "drug_id": drug.get("drug_id", ""),
 "drug_name": drug.get("drug_name", ""),
 "target": drug.get("target", ""),
 "pathway": drug.get("pathway", ""),
 "n_cell_lines": drug.get(
 "n_cell_lines_tested", 0),
 })

 df = pd.DataFrame(rows[:limit])
 print(f"DepMap drugs: {len(df)} compounds")
 return df
```

## 4. DepMap integrationpipeline

```python
def depmap_pipeline(gene_symbol,
 output_dir="results"):
 """
 DepMap integrationpipeline。

 Parameters:
 gene_symbol: str — gene symbol
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) genedependency
 deps = depmap_gene_dependency(gene_symbol)
 deps.to_csv(output_dir / "depmap_dependency.csv",
 index=False)

 # 2) 
 drugs = depmap_drug_sensitivity
 drugs.to_csv(output_dir / "depmap_drugs.csv",
 index=False)

 # 3) dependency's highcell
 if not deps.empty:
 top_dependent = deps.head(10)
 top_dependent.to_csv(
 output_dir / "depmap_top_dependent.csv",
 index=False)

 print(f"DepMap pipeline: {gene_symbol} → {output_dir}")
 return {"dependency": deps, "drugs": drugs}
```

---

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

## Pipeline Integration

```
cancer-genomics → depmap-dependencies → precision-oncology
 (cancergenome) (DepMap Portal) (tumor)
 │ │ ↓
expression-analysis ──────┘ drug-target-profiling
 (expression) 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/depmap_dependency.csv` | dependency | → cancer-genomics |
| `results/depmap_drugs.csv` | | → drug-target-profiling |
| `results/depmap_top_dependent.csv` | dependencycell | → precision-oncology |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
