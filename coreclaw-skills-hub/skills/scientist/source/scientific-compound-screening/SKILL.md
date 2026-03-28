---
name: scientific-compound-screening
description: |
 compoundskill。ZINC databaseutilizingpossiblecompoundsearch、
 SMILES/name'ssearch、logfilter、
 preprocessingpipeline。
tu_tools:
 - key: zinc
 name: ZINC
 description: possiblecompounddatabase
---

# Scientific Compound Screening

ZINC databaseutilizingcompoundlibrarysearch
preprocessingpipeline is provided。

## When to Use

- possiblecompoundlibrary is searchedand
- SMILES structureformulafromcompound and
- compoundfromdatabaserecord is retrievedand
- log's is performedand
- for's compoundwhen needed

---

## Quick Start

## 1. ZINC compoundsearch

```python
import requests
import pandas as pd

ZINC_API = "https://zinc15.docking.org"


def zinc_search_by_name(name, max_results=20):
 """
 ZINC databasecompoundby/viasearch。

 Parameters:
 name: str — compound name (e.g., "aspirin")
 max_results: int — maximum results

 ToolUniverse:
 ZINC_search_by_name(name=name)
 """
 url = f"{ZINC_API}/substances/search"
 params = {"q": name, "count": max_results}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data:
 results.append({
 "zinc_id": item.get("zinc_id", ""),
 "name": item.get("name", ""),
 "smiles": item.get("smiles", ""),
 "mwt": item.get("mwt", ""),
 "logp": item.get("logp", ""),
 "purchasable": item.get("purchasability", ""),
 })

 df = pd.DataFrame(results)
 print(f"ZINC search '{name}': {len(df)} compounds")
 return df
```

## 2. ZINC SMILES search

```python
def zinc_search_by_smiles(smiles, similarity=0.7, max_results=20):
 """
 ZINC SMILES structureformulaby/viasearch。

 Parameters:
 smiles: str — SMILES string
 similarity: float — Tanimoto similarity threshold (0-1)

 ToolUniverse:
 ZINC_search_by_smiles(smiles=smiles)
 """
 url = f"{ZINC_API}/substances/search"
 params = {
 "smiles": smiles,
 "similarity": similarity,
 "count": max_results,
 }
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data:
 results.append({
 "zinc_id": item.get("zinc_id", ""),
 "smiles": item.get("smiles", ""),
 "similarity": item.get("similarity", ""),
 "mwt": item.get("mwt", ""),
 "logp": item.get("logp", ""),
 "purchasable": item.get("purchasability", ""),
 })

 df = pd.DataFrame(results)
 print(f"ZINC SMILES search: {len(df)} similar compounds "
 f"(threshold={similarity})")
 return df
```

## 3. ZINC compounddetailsretrieval

```python
def zinc_get_substance(zinc_id):
 """
 ZINC ID fromcompound's allinformationretrieval。

 Parameters:
 zinc_id: str — ZINC ID (e.g., "ZINC000000000001")

 ToolUniverse:
 ZINC_get_substance(zinc_id=zinc_id)
 """
 url = f"{ZINC_API}/substances/{zinc_id}.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 info = {
 "zinc_id": data.get("zinc_id", ""),
 "name": data.get("name", ""),
 "smiles": data.get("smiles", ""),
 "inchikey": data.get("inchikey", ""),
 "mwt": data.get("mwt", ""),
 "logp": data.get("logp", ""),
 "num_rotatable_bonds": data.get("num_rotatable_bonds", ""),
 "num_hba": data.get("num_hba", ""),
 "num_hbd": data.get("num_hbd", ""),
 "tpsa": data.get("tpsa", ""),
 "purchasable": data.get("purchasability", ""),
 }

 print(f"ZINC {zinc_id}: {info['name']} (MW={info['mwt']})")
 return info, data
```

## 4. ZINC loglist

```python
def zinc_get_catalogs:
 """
 ZINC 's usepossiblelog  list retrieval。

 ToolUniverse:
 ZINC_get_catalogs
 """
 url = f"{ZINC_API}/catalogs.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 results = []
 for cat in data:
 results.append({
 "catalog_name": cat.get("name", ""),
 "short_name": cat.get("short_name", ""),
 "num_substances": cat.get("num_substances", 0),
 "url": cat.get("url", ""),
 })

 df = pd.DataFrame(results)
 print(f"ZINC catalogs: {len(df)} vendors")
 return df
```

## 5. preprocessingpipeline

```python
def virtual_screening_prep(query_smiles, lipinski=True, max_compounds=100):
 """
 for's compound。
 Lipinski's Rule of Five filterincludes。

 ToolUniverse (cross-cutting):
 ZINC_search_by_smiles(smiles=query_smiles) → ZINC_get_substance(zinc_id)
 """
 # Step 1: Similar compound search
 df = zinc_search_by_smiles(query_smiles, similarity=0.6,
 max_results=max_compounds)

 if df.empty:
 print("No similar compounds found")
 return df

 # Step 2: Lipinski filter
 if lipinski:
 df["mwt"] = pd.to_numeric(df["mwt"], errors="coerce")
 df["logp"] = pd.to_numeric(df["logp"], errors="coerce")
 before = len(df)
 df = df[
 (df["mwt"] <= 500)
 & (df["logp"] <= 5)
 ]
 print(f"Lipinski filter: {before} → {len(df)} compounds")

 # Step 3: Sort by similarity
 df["similarity"] = pd.to_numeric(df["similarity"], errors="coerce")
 df = df.sort_values("similarity", ascending=False)

 print(f"VS prep: {len(df)} compounds ready for screening")
 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/zinc_search.csv` | CSV |
| `results/zinc_similar.csv` | CSV |
| `results/zinc_substance.json` | JSON |
| `results/zinc_catalogs.csv` | CSV |
| `results/vs_library.csv` | CSV |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| ZINC | `ZINC_search_by_name` | compoundsearch |
| ZINC | `ZINC_search_by_smiles` | SMILES search |
| ZINC | `ZINC_get_substance` | compounddetails |
| ZINC | `ZINC_get_catalogs` | loglist |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-compound-similarity` | compound similarity |
| `scientific-pharmacology-targets` | |
| `scientific-molecular-docking` | molecular docking |
| `scientific-drug-target-interaction` | DTI analysis |
| `scientific-admet-toxicity` | ADMET toxicity |

### Dependencies

`requests`, `pandas`
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
