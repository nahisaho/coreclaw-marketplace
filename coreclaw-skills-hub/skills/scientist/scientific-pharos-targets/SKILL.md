---
name: scientific-pharos-targets
description: |
 Pharos targets skill. Target Development Level (TDL) classification, understudied protein identification, Illuminating the Druggable Genome (IDG) resource queries.
---

# Scientific Pharos Targets

IDG (Illuminating the Druggable Genome) Pharos GraphQL API
utilizing TDL classificationdisease-
ligandsearchexistingpipeline is provided。

## When to Use

- protein's (Tclin/Tchem/Tbio/Tdark) is verifiedand
- IDG 'sinvestigationwhen needed
- diseaseligandPPI is searchedand
- Tchem/Tbio from is exploredand
- 'sdruggabilitycomparison is performedand

---

## Quick Start

## 1. TDL classificationsearch

```python
import requests
import pandas as pd

PHAROS_API = "https://pharos-api.ncats.io/graphql"


def pharos_target(gene_symbol):
 """
 Pharos — detailsinformationretrieval。

 Parameters:
 gene_symbol: str — gene symbol (example: "ACE2")
 """
 query = """
 query targetDetails($sym: String!) {
 target(q: {sym: $sym}) {
 name
 sym
 tdl
 fam
 novelty
 description
 uniprotId: accession
 diseaseCount
 ligandCount
 ppiCount
 }
 }
 """
 resp = requests.post(
 PHAROS_API,
 json={"query": query,
 "variables": {"sym": gene_symbol}},
 timeout=30)
 resp.raise_for_status
 data = resp.json.get("data", {}).get("target", {})

 if not data:
 print(f"Pharos: {gene_symbol} not found")
 return {}

 print(f"Pharos: {gene_symbol} → TDL={data['tdl']}, "
 f"fam={data.get('fam', 'N/A')}, "
 f"diseases={data.get('diseaseCount', 0)}, "
 f"ligands={data.get('ligandCount', 0)}")
 return data


def pharos_target_list(gene_symbols):
 """
 Pharos — multiple TDL batchretrieval。

 Parameters:
 gene_symbols: list[str] — gene symbol list
 """
 results = []
 for sym in gene_symbols:
 data = pharos_target(sym)
 if data:
 results.append(data)

 df = pd.DataFrame(results)
 if not df.empty:
 tdl_counts = df["tdl"].value_counts
 print(f"TDL distribution: "
 f"{tdl_counts.to_dict}")
 return df
```

## 2. disease-

```python
def pharos_target_diseases(gene_symbol, top_n=20):
 """
 Pharos — 'sdiseaseretrieval。

 Parameters:
 gene_symbol: str — gene symbol
 top_n: int — top count
 """
 query = """
 query targetDiseases($sym: String!, $top: Int!) {
 target(q: {sym: $sym}) {
 sym
 diseases(top: $top) {
 name
 associationCount
 datasource_count
 }
 }
 }
 """
 resp = requests.post(
 PHAROS_API,
 json={"query": query,
 "variables": {"sym": gene_symbol,
 "top": top_n}},
 timeout=30)
 resp.raise_for_status
 target = resp.json.get("data", {}).get(
 "target", {})
 diseases = target.get("diseases", [])

 df = pd.DataFrame(diseases)
 print(f"Pharos diseases: {gene_symbol} → "
 f"{len(df)} associations")
 return df
```

## 3. ligandsearch

```python
def pharos_target_ligands(gene_symbol, top_n=20):
 """
 Pharos — 'sligand/activationretrieval。

 Parameters:
 gene_symbol: str — gene symbol
 top_n: int — top count
 """
 query = """
 query targetLigands($sym: String!, $top: Int!) {
 target(q: {sym: $sym}) {
 sym
 ligands(top: $top) {
 name
 smiles
 isdrug
 actcnt
 activities {
 type
 value
 moa
 }
 }
 }
 }
 """
 resp = requests.post(
 PHAROS_API,
 json={"query": query,
 "variables": {"sym": gene_symbol,
 "top": top_n}},
 timeout=30)
 resp.raise_for_status
 target = resp.json.get("data", {}).get(
 "target", {})
 ligands = target.get("ligands", [])

 rows = []
 for lig in ligands:
 rows.append({
 "name": lig.get("name", ""),
 "smiles": lig.get("smiles", ""),
 "is_drug": lig.get("isdrug", False),
 "activity_count": lig.get("actcnt", 0),
 })

 df = pd.DataFrame(rows)
 n_drugs = df["is_drug"].sum if not df.empty else 0
 print(f"Pharos ligands: {gene_symbol} → "
 f"{len(df)} compounds ({n_drugs} drugs)")
 return df
```

## 4. Pharos integrationpipeline

```python
def pharos_pipeline(gene_symbols,
 output_dir="results"):
 """
 Pharos integrationpipeline。

 Parameters:
 gene_symbols: list[str] — gene symbol list
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) TDL classification
 targets = pharos_target_list(gene_symbols)
 targets.to_csv(output_dir / "pharos_targets.csv",
 index=False)

 # 2) disease (top)
 all_diseases = []
 for sym in gene_symbols[:10]:
 diseases = pharos_target_diseases(sym)
 diseases["target"] = sym
 all_diseases.append(diseases)
 if all_diseases:
 disease_df = pd.concat(all_diseases,
 ignore_index=True)
 disease_df.to_csv(
 output_dir / "pharos_diseases.csv",
 index=False)

 # 3) ligand
 all_ligands = []
 for sym in gene_symbols[:10]:
 ligands = pharos_target_ligands(sym)
 ligands["target"] = sym
 all_ligands.append(ligands)
 if all_ligands:
 ligand_df = pd.concat(all_ligands,
 ignore_index=True)
 ligand_df.to_csv(
 output_dir / "pharos_ligands.csv",
 index=False)

 print(f"Pharos pipeline → {output_dir}")
 return {"targets": targets}
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
drug-target-profiling → pharos-targets → drug-repurposing
 (DGIdb/) (TDL/IDG) 
 │ │ ↓
 pharmacology-targets ─────┘ compound-screening
 (BindingDB/GtoPdb) (ZINC library)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/pharos_targets.csv` | TDL classificationresults | → drug-target-profiling |
| `results/pharos_diseases.csv` | disease | → disease-research |
| `results/pharos_ligands.csv` | ligand/ | → drug-repurposing |
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
