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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
