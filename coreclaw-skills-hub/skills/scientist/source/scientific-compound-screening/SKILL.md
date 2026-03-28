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
