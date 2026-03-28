---
name: scientific-rcsb-pdb-search
description: |
 RCSB PDB search skill. Protein Data Bank structure search, advanced query construction, structure clustering, and PDB data retrieval/parsing.
tu_tools:
 - key: rcsb_pdb
 name: RCSB PDB Data
 description: PDB entryData Retrievalstructuredata
 - key: rcsb_search
 name: RCSB PDB Search
 description: PDB structuresearch/sequence/structuresearch
---

# Scientific RCSB PDB Search

RCSB PDB Search API and Data API utilizingproteinstructure
searchData Retrievalligandinformationpipeline is provided。

## When to Use

- PDB 's proteinstructuresearchwhen needed
- degreeexperimentmethod filterwhen needed
- ligandbindingstructure is searchedand
- structure'sdata (authorcitationdegree) is retrievedand
- sequencestructure is searchedand
- PDB entryfromligandbindinginformation is retrievedand

---

## Quick Start

## 1. searchstructuredata

```python
import requests
import pandas as pd

RCSB_SEARCH = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_DATA = "https://data.rcsb.org/rest/v1/core"


def rcsb_text_search(query, method=None,
 resolution_max=None, limit=50):
 """
 RCSB PDB — search。

 Parameters:
 query: str — search query (example: "BRCA1", "kinase")
 method: str — experimentmethodfilter
 (example: "X-RAY DIFFRACTION", "ELECTRON MICROSCOPY")
 resolution_max: float — degree (Å)
 limit: int — maximum results
 """
 search_query = {
 "query": {
 "type": "group",
 "logical_operator": "and",
 "nodes": [
 {
 "type": "terminal",
 "service": "full_text",
 "parameters": {"value": query},
 }
 ],
 },
 "return_type": "entry",
 "request_options": {
 "paginate": {"start": 0, "rows": limit},
 "sort": [{"sort_by": "score", "direction": "desc"}],
 },
 }

 if method:
 search_query["query"]["nodes"].append({
 "type": "terminal",
 "service": "text",
 "parameters": {
 "attribute": "exptl.method",
 "operator": "exact_match",
 "value": method,
 },
 })

 if resolution_max:
 search_query["query"]["nodes"].append({
 "type": "terminal",
 "service": "text",
 "parameters": {
 "attribute": "rcsb_entry_info."
 "resolution_combined",
 "operator": "less_or_equal",
 "value": resolution_max,
 },
 })

 resp = requests.post(RCSB_SEARCH, json=search_query,
 timeout=30)
 resp.raise_for_status
 data = resp.json

 pdb_ids = [r["identifier"]
 for r in data.get("result_set", [])]
 total = data.get("total_count", 0)
 print(f"RCSB PDB search: {len(pdb_ids)}/{total} "
 f"(query='{query}')")
 return pdb_ids


def rcsb_get_entry(pdb_id):
 """
 RCSB PDB — entryData Retrieval。

 Parameters:
 pdb_id: str — PDB ID (example: "1BRS", "7S4O")
 """
 url = f"{RCSB_DATA}/entry/{pdb_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 info = data.get("rcsb_entry_info", {})
 citation = (data.get("rcsb_primary_citation") or {})

 result = {
 "pdb_id": pdb_id,
 "title": data.get("struct", {}).get("title", ""),
 "method": info.get("experimental_method", ""),
 "resolution": info.get("resolution_combined", [None])[0],
 "deposition_date": info.get("deposition_date", ""),
 "polymer_count": info.get(
 "deposited_polymer_entity_count", 0),
 "nonpolymer_count": info.get(
 "deposited_nonpolymer_entity_count", 0),
 "citation_title": citation.get("title", ""),
 "citation_doi": citation.get(
 "pdbx_database_id_doi", ""),
 }
 return result
```

## 2. structurebatchretrievalcomparison

```python
def rcsb_batch_metadata(pdb_ids):
 """
 RCSB PDB — batchData Retrieval。

 Parameters:
 pdb_ids: list[str] — PDB ID 
 """
 results = []
 for pid in pdb_ids:
 try:
 meta = rcsb_get_entry(pid)
 results.append(meta)
 except Exception as e:
 print(f" Warning: {pid} — {e}")
 continue

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("resolution")
 print(f"RCSB batch: {len(df)} entries")
 return df
```

## 3. ligandbindinginformation

```python
def rcsb_get_ligands(pdb_id):
 """
 RCSB PDB — ligandinformationretrieval。

 Parameters:
 pdb_id: str — PDB ID
 """
 url = (f"https://data.rcsb.org/rest/v1/core/"
 f"nonpolymer_entity/{pdb_id}")
 # entry's nonpolymerretrieval
 entry = rcsb_get_entry(pdb_id)
 n_ligands = entry.get("nonpolymer_count", 0)

 ligands = []
 for i in range(1, n_ligands + 1):
 try:
 lig_url = (f"https://data.rcsb.org/rest/v1/core/"
 f"nonpolymer_entity/{pdb_id}/{i}")
 r = requests.get(lig_url, timeout=15)
 if r.status_code == 200:
 ld = r.json
 comp_id = ld.get(
 "pdbx_entity_nonpoly", {}).get(
 "comp_id", "")
 ligands.append({
 "pdb_id": pdb_id,
 "entity_id": i,
 "comp_id": comp_id,
 "name": ld.get(
 "rcsb_nonpolymer_entity", {}).get(
 "pdbx_description", ""),
 "formula": ld.get(
 "rcsb_nonpolymer_entity", {}).get(
 "formula_weight", ""),
 })
 except Exception:
 continue

 df = pd.DataFrame(ligands)
 print(f"RCSB ligands: {pdb_id} → {len(df)} ligands")
 return df
```

## 4. RCSB PDB integrationpipeline

```python
def rcsb_pipeline(query, resolution_max=3.0,
 output_dir="results"):
 """
 RCSB PDB integrationpipeline。

 Parameters:
 query: str — search query
 resolution_max: float — degree
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) search
 pdb_ids = rcsb_text_search(
 query, resolution_max=resolution_max)

 # 2) batchdata
 metadata = rcsb_batch_metadata(pdb_ids[:20])
 metadata.to_csv(output_dir / "pdb_entries.csv",
 index=False)

 # 3) structure'sligand
 if not metadata.empty:
 top = metadata.iloc[0]["pdb_id"]
 ligands = rcsb_get_ligands(top)
 ligands.to_csv(output_dir / "ligands.csv",
 index=False)

 print(f"RCSB pipeline: {output_dir}")
 return {"entries": metadata}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `rcsb_pdb` | RCSB PDB Data | entrydatastructuredata |
| `rcsb_search` | RCSB PDB Search | /sequence/structuresearch |

## Pipeline Integration

```
protein-structure-analysis → rcsb-pdb-search → molecular-docking
 (PDB/AlphaFold structure) (RCSB Search API) (Vina/DiffDock)
 │ │ ↓
 uniprot-proteome ──────────────┘ drug-target-profiling
 (UniProtsequence) │ 
 ↓
 alphafold-structures
 (AlphaFold DB)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/pdb_entries.csv` | structuredata | → protein-structure-analysis |
| `results/ligands.csv` | ligandinformation | → molecular-docking |
---

## Harness Optimization (v0.4.0)

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
