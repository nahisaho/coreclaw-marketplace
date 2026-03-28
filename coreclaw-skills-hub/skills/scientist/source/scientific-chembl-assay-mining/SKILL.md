---
name: scientific-chembl-assay-mining
description: |
 ChEMBL activitydataskill。ChEMBL REST API by/via
 searchData RetrievalIC50/Ki/EC50 SAR analysis
 -compoundmappingselectionATC classificationsearch
 structurealertpipeline。
tu_tools:
 - key: chembl
 name: ChEMBL
 description: activitydatabase (EBI)
---

# Scientific ChEMBL Assay Mining

ChEMBL REST API (EBI) utilizingdata
pipeline is provided。search、activityvalueanalysis、SAR (structureactivitycorrelation)、
selection、molecular dockingpreprocessing integration。

## When to Use

- ChEMBL fromdata is retrievedand
- IC50/Ki/EC50 bulkretrieval SAR analysiswhen needed
- for/againstcompoundselection is evaluatedand
- moleculestructuresearchstructuresearch is performedand
- ATC classificationfromfile is builtand
- structurealert (PAINS, Dundee) when needed

---

## Quick Start

## 1. search & retrieval

```python
import requests
import pandas as pd

CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"
HEADERS = {"Accept": "application/json"}


def search_target(query, organism="Homo sapiens", limit=10):
 """
 ChEMBL search。

 Parameters:
 query: str — (example: "EGFR", "CDK4")
 organism: str — organism/species
 limit: int — maximum retrieval count

 ToolUniverse:
 ChEMBL_search_targets(pref_name__contains=query, organism=organism)
 ChEMBL_get_target(target_chembl_id=target_id)
 """
 url = f"{CHEMBL_API}/target.json"
 params = {
 "pref_name__icontains": query,
 "organism": organism,
 "limit": limit,
 }
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 targets = resp.json.get("targets", [])

 rows = []
 for t in targets:
 rows.append({
 "target_chembl_id": t.get("target_chembl_id"),
 "pref_name": t.get("pref_name"),
 "target_type": t.get("target_type"),
 "organism": t.get("organism"),
 })

 df = pd.DataFrame(rows)
 print(f"ChEMBL targets matching '{query}': {len(df)}")
 return df
```

## 2. Data Retrieval

```python
def get_target_activities(target_chembl_id, standard_type="IC50",
 max_value=10000, limit=500):
 """
 for/againstData Retrieval。

 Parameters:
 target_chembl_id: str — ChEMBL ID
 standard_type: str — "IC50", "Ki", "EC50", "Kd" etc.
 max_value: float — nM threshold
 limit: int — maximum retrieval count

 ToolUniverse:
 ChEMBL_search_activities(
 target_chembl_id=target_chembl_id,
 standard_type=standard_type,
 standard_value__lte=max_value
 )
 ChEMBL_get_target_activities(target_chembl_id__exact=target_chembl_id)
 """
 url = f"{CHEMBL_API}/activity.json"
 params = {
 "target_chembl_id": target_chembl_id,
 "standard_type": standard_type,
 "standard_value__lte": max_value,
 "standard_units": "nM",
 "limit": limit,
 }
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 activities = resp.json.get("activities", [])

 rows = []
 for act in activities:
 rows.append({
 "molecule_chembl_id": act.get("molecule_chembl_id"),
 "canonical_smiles": act.get("canonical_smiles"),
 "standard_type": act.get("standard_type"),
 "standard_value": act.get("standard_value"),
 "standard_units": act.get("standard_units"),
 "pchembl_value": act.get("pchembl_value"),
 "assay_chembl_id": act.get("assay_chembl_id"),
 "assay_type": act.get("assay_type"),
 "target_chembl_id": act.get("target_chembl_id"),
 })

 df = pd.DataFrame(rows)
 if "standard_value" in df.columns:
 df["standard_value"] = pd.to_numeric(df["standard_value"], errors="coerce")
 print(f"Activities for {target_chembl_id} ({standard_type}): {len(df)}")
 return df
```

## 3. detailssearch

```python
def search_assays(target_chembl_id=None, assay_type=None, limit=50):
 """
 ChEMBL search。

 Parameters:
 target_chembl_id: str — ChEMBL ID
 assay_type: str — "B" (Binding), "F" (Functional), "A" (ADME)
 limit: int — maximum retrieval count

 ToolUniverse:
 ChEMBL_search_assays(
 target_chembl_id=target_chembl_id,
 assay_type=assay_type
 )
 ChEMBL_get_assay(assay_chembl_id=assay_id)
 ChEMBL_get_assay_activities(assay_chembl_id__exact=assay_id)
 """
 url = f"{CHEMBL_API}/assay.json"
 params = {"limit": limit}
 if target_chembl_id:
 params["target_chembl_id"] = target_chembl_id
 if assay_type:
 params["assay_type"] = assay_type

 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 assays = resp.json.get("assays", [])

 rows = []
 for a in assays:
 rows.append({
 "assay_chembl_id": a.get("assay_chembl_id"),
 "description": a.get("description", "")[:200],
 "assay_type": a.get("assay_type"),
 "assay_organism": a.get("assay_organism"),
 "confidence_score": a.get("confidence_score"),
 "target_chembl_id": a.get("target_chembl_id"),
 })

 df = pd.DataFrame(rows)
 print(f"Assays found: {len(df)}")
 return df
```

## 4. SAR (structureactivitycorrelation) analysis

```python
import numpy as np


def sar_analysis(activity_df, pchembl_col="pchembl_value"):
 """
 data's SAR analysis。

 Parameters:
 activity_df: DataFrame — get_target_activities 's output
 pchembl_col: str — pChEMBL value column

 Returns:
 dict — SAR 
 """
 df = activity_df.copy
 df[pchembl_col] = pd.to_numeric(df[pchembl_col], errors="coerce")
 df = df.dropna(subset=[pchembl_col])

 summary = {
 "n_compounds": len(df),
 "n_unique_molecules": df["molecule_chembl_id"].nunique,
 "pchembl_mean": round(df[pchembl_col].mean, 2),
 "pchembl_median": round(df[pchembl_col].median, 2),
 "pchembl_std": round(df[pchembl_col].std, 2),
 "pchembl_range": [
 round(df[pchembl_col].min, 2),
 round(df[pchembl_col].max, 2),
 ],
 "most_potent": df.loc[df[pchembl_col].idxmax].to_dict
 if len(df) > 0 else None,
 "potency_bins": {
 "high_potent_lt100nM": int((df[pchembl_col] >= 7.0).sum),
 "moderate_100_1000nM": int(
 ((df[pchembl_col] >= 6.0) & (df[pchembl_col] < 7.0)).sum
 ),
 "weak_gt1000nM": int((df[pchembl_col] < 6.0).sum),
 },
 }

 print(f"SAR summary: {summary['n_unique_molecules']} molecules, "
 f"pChEMBL mean={summary['pchembl_mean']}")
 return summary
```

## 5. selection

```python
def selectivity_profile(molecule_chembl_id, limit=100):
 """
 compound's selectionevaluation。

 Parameters:
 molecule_chembl_id: str — compound ChEMBL ID
 limit: int — maximum retrieval count

 ToolUniverse:
 ChEMBL_get_molecule_targets(
 molecule_chembl_id__exact=molecule_chembl_id
 )
 ChEMBL_search_activities(molecule_chembl_id=molecule_chembl_id)
 """
 url = f"{CHEMBL_API}/activity.json"
 params = {
 "molecule_chembl_id": molecule_chembl_id,
 "limit": limit,
 }
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 activities = resp.json.get("activities", [])

 target_data = {}
 for act in activities:
 tid = act.get("target_chembl_id")
 pchembl = act.get("pchembl_value")
 if tid and pchembl:
 if tid not in target_data:
 target_data[tid] = {
 "target_pref_name": act.get("target_pref_name", ""),
 "pchembl_values": [],
 }
 target_data[tid]["pchembl_values"].append(float(pchembl))

 profile = []
 for tid, info in target_data.items:
 vals = info["pchembl_values"]
 profile.append({
 "target_chembl_id": tid,
 "target_name": info["target_pref_name"],
 "n_measurements": len(vals),
 "best_pchembl": round(max(vals), 2),
 "mean_pchembl": round(np.mean(vals), 2),
 })

 df = pd.DataFrame(profile).sort_values("best_pchembl", ascending=False)
 print(f"Selectivity: {molecule_chembl_id} tested on {len(df)} targets")
 return df
```

## 6. molecule & structuresearch

```python
def similarity_search(smiles, threshold=70, max_results=25):
 """
 SMILES structureby/viasearch。

 Parameters:
 smiles: str — SMILES
 threshold: int — Tanimoto threshold (%)
 max_results: int — maximum results

 ToolUniverse:
 ChEMBL_search_similar_molecules(
 query=smiles, similarity_threshold=threshold
 )
 ChEMBL_search_substructure(smiles=smiles)
 """
 url = f"{CHEMBL_API}/similarity/{smiles}/{threshold}.json"
 params = {"limit": max_results}
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 molecules = resp.json.get("molecules", [])

 rows = []
 for mol in molecules:
 rows.append({
 "molecule_chembl_id": mol.get("molecule_chembl_id"),
 "pref_name": mol.get("pref_name"),
 "similarity": mol.get("similarity"),
 "canonical_smiles": mol.get("molecule_structures", {}).get(
 "canonical_smiles", ""
 ),
 "max_phase": mol.get("max_phase"),
 })

 df = pd.DataFrame(rows)
 print(f"Similar molecules (>{threshold}%): {len(df)}")
 return df
```

## 7. ATC classification & search

```python
def search_approved_drugs(target_chembl_id, limit=50):
 """
 for/against ATC classificationand and alsosearch。

 ToolUniverse:
 ChEMBL_search_drugs(max_phase=4)
 ChEMBL_search_mechanisms(target_chembl_id=target_chembl_id)
 ChEMBL_search_atc_classification
 """
 url = f"{CHEMBL_API}/mechanism.json"
 params = {
 "target_chembl_id": target_chembl_id,
 "limit": limit,
 }
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 mechanisms = resp.json.get("mechanisms", [])

 rows = []
 for mech in mechanisms:
 drug_id = mech.get("molecule_chembl_id")
 drug_resp = requests.get(
 f"{CHEMBL_API}/molecule/{drug_id}.json", headers=HEADERS
 )
 if drug_resp.ok:
 drug = drug_resp.json
 rows.append({
 "molecule_chembl_id": drug_id,
 "pref_name": drug.get("pref_name"),
 "max_phase": drug.get("max_phase"),
 "mechanism": mech.get("mechanism_of_action"),
 "action_type": mech.get("action_type"),
 "first_approval": drug.get("first_approval"),
 "atc_classifications": drug.get("atc_classifications", []),
 })

 df = pd.DataFrame(rows)
 print(f"Drugs/mechanisms for {target_chembl_id}: {len(df)}")
 return df
```

## 8. structurealert

```python
def check_structural_alerts(molecule_chembl_id):
 """
 compound's structurealert (PAINS, Dundee) 。

 ToolUniverse:
 ChEMBL_search_compound_structural_alerts(
 molecule_chembl_id=molecule_chembl_id
 )
 """
 url = f"{CHEMBL_API}/compound_structural_alert.json"
 params = {"molecule_chembl_id": molecule_chembl_id, "limit": 100}
 resp = requests.get(url, params=params, headers=HEADERS)
 resp.raise_for_status
 alerts = resp.json.get("compound_structural_alerts", [])

 rows = []
 for a in alerts:
 rows.append({
 "alert_set_name": a.get("alert", {}).get("alert_set", {}).get(
 "set_name", ""
 ),
 "smarts": a.get("alert", {}).get("smarts", ""),
 "alert_name": a.get("alert", {}).get("alert_name", ""),
 })

 df = pd.DataFrame(rows)
 if len(df) > 0:
 print(f"⚠ {molecule_chembl_id}: {len(df)} structural alerts found")
 else:
 print(f"✓ {molecule_chembl_id}: No structural alerts")
 return df
```

## 9. integration SAR pipeline

```python
def chembl_sar_pipeline(target_query, organism="Homo sapiens",
 standard_type="IC50", max_nm=10000):
 """
 ChEMBL SAR integrationpipeline。

 Pipeline:
 search_target → get_target_activities → sar_analysis →
 selectivity_profile (top hits) → check_structural_alerts

 Parameters:
 target_query: str — 
 organism: str — organism/species
 standard_type: str — activityvalue
 max_nm: float — nM threshold
 """
 # Step 1: search
 targets = search_target(target_query, organism)
 if targets.empty:
 print(f"No targets found for '{target_query}'")
 return None

 target_id = targets.iloc[0]["target_chembl_id"]
 print(f"\nSelected target: {target_id}")

 # Step 2: retrieval
 activities = get_target_activities(target_id, standard_type, max_nm)
 if activities.empty:
 print("No activities found")
 return None

 # Step 3: SAR analysis
 sar = sar_analysis(activities)

 # Step 4: compound's selection
 top = activities.nlargest(3, "pchembl_value")
 selectivity_results = []
 for _, row in top.iterrows:
 mol_id = row["molecule_chembl_id"]
 sel = selectivity_profile(mol_id)
 selectivity_results.append({"molecule": mol_id, "profile": sel})

 # Step 5: structurealert
 alert_results = {}
 for _, row in top.iterrows:
 mol_id = row["molecule_chembl_id"]
 alerts = check_structural_alerts(mol_id)
 alert_results[mol_id] = len(alerts)

 result = {
 "target": target_id,
 "sar_summary": sar,
 "top_compounds": top.to_dict("records"),
 "structural_alerts": alert_results,
 }

 print(f"\n=== ChEMBL SAR Pipeline Complete ===")
 print(f"Target: {target_id}")
 print(f"Compounds: {sar['n_unique_molecules']}")
 print(f"Top hit pChEMBL: {sar['pchembl_range'][1]}")

 return result
```

---

## Pipeline Integration

```
drug-target-profiling → chembl-assay-mining → admet-pharmacokinetics
  (SAR data) (ADMET/PK evaluation)
 │ │ ↓
compound-screening selectivity_profile molecular-docking
 (ZINC library)  (Vina/DiffDock)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/chembl_activities.csv` | data | → admet-pharmacokinetics |
| `results/sar_summary.json` | SAR | → drug-target-profiling |
| `results/selectivity_profile.csv` | selectionfile | → compound-screening |
| `results/structural_alerts.json` | structurealertresults | → molecular-docking |

## usepossibletool (ToolUniverse SMCP)

| Tool Name | Usage |
|---------|------|
| `ChEMBL_search_targets` | search |
| `ChEMBL_get_target` | details |
| `ChEMBL_search_assays` | search |
| `ChEMBL_get_assay` | details |
| `ChEMBL_get_assay_activities` | activitydata |
| `ChEMBL_search_activities` | activitysearch (filter) |
| `ChEMBL_get_activity` | activitydatadetails |
| `ChEMBL_get_molecule` | compounddetails |
| `ChEMBL_get_molecule_targets` | compound- |
| `ChEMBL_search_similar_molecules` | search |
| `ChEMBL_search_substructure` | structuresearch |
| `ChEMBL_search_drugs` | search |
| `ChEMBL_search_mechanisms` | forsearch |
| `ChEMBL_search_atc_classification` | ATC classification |
| `ChEMBL_search_compound_structural_alerts` | structurealert |
| `ChEMBL_search_cell_lines` | cellsearch |
| `ChEMBL_search_binding_sites` | binding |
| `ChEMBL_get_drug` | information |
| `ChEMBL_get_drug_mechanisms` | for |
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
