---
name: scientific-metabolomics-databases
description: |
 Metabolomics databases skill. HMDB/METLIN/MassBank database queries, metabolite annotation, spectral library matching, and cross-database metabolite identification.
tu_tools:
 - key: metacyc
 name: MetaCyc
 description: metabolismpathwayreactioncompounddatabase
---

# Scientific Metabolomics Databases

HMDB / MetaCyc / Metabolomics Workbench 's 3 database integration
metabolitepathway mappingbiomarkerpipeline is provided。

## When to Use

- amount (m/z) frommetabolitewhen needed
- HMDB metabolite's is investigatedand
- MetaCyc metabolismpathway'sdetails is verifiedand
- Metabolomics Workbench 'sdataset is searchedand
- multiple DB cross-cuttingmetaboliteannotationwhen needed

---

## Quick Start

## 1. HMDB metabolite search

```python
import requests
import pandas as pd
import xml.etree.ElementTree as ET


def hmdb_search(query, search_type="name", max_results=50):
 """
 HMDB (Human Metabolome Database) search。

 Parameters:
 query: str — search query (metabolite, HMDB ID, formula)
 search_type: "name", "hmdb_id", "formula", "mass"
 """
 # ToolUniverse : HMDB_search, HMDB_get_metabolite, HMDB_get_diseases

 base_url = "https://hmdb.ca/metabolites"

 if search_type == "hmdb_id":
 url = f"{base_url}/{query}.xml"
 resp = requests.get(url, timeout=30)
 if resp.status_code == 200:
 root = ET.fromstring(resp.text)
 ns = {"hmdb": "http://www.hmdb.ca"}
 result = {
 "hmdb_id": root.findtext("hmdb:accession", "", ns),
 "name": root.findtext("hmdb:name", "", ns),
 "chemical_formula": root.findtext("hmdb:chemical_formula", "", ns),
 "monoisotopic_mass": float(root.findtext(
 "hmdb:monisotopic_molecular_weight", "0", ns) or 0),
 "description": (root.findtext("hmdb:description", "", ns) or "")[:300],
 "status": root.findtext("hmdb:status", "", ns),
 "biological_role": root.findtext(
 "hmdb:ontology/hmdb:root/hmdb:term", "", ns),
 }
 return pd.DataFrame([result])

 # namesearch
 results = []
 params = {"query": query, "search_type": search_type}
 print(f"HMDB search: '{query}' (type={search_type})")
 # 's search ToolUniverse SMCP 
 return pd.DataFrame(results)
```

## 2. MetaCyc metabolismpathwaysearch

```python
def metacyc_pathway_search(query, organism="Homo sapiens"):
 """
 MetaCyc metabolismpathwaysearch。

 Parameters:
 query: str — pathway/metabolite/enzyme
 organism: str — organism/speciesfilter
 """
 # ToolUniverse :
 # MetaCyc_search_pathways, MetaCyc_get_pathway
 # MetaCyc_get_compound, MetaCyc_get_reaction

 results = {
 "query": query,
 "organism": organism,
 "database": "MetaCyc",
 "tools": [
 "MetaCyc_search_pathways — pathwaysearch",
 "MetaCyc_get_pathway — pathwaydetails (reactionenzymemetabolite)",
 "MetaCyc_get_compound — compounddetails (structure)",
 "MetaCyc_get_reaction — reactiondetails (generationenzyme)",
 ],
 }

 print(f"MetaCyc: querying '{query}' for {organism}")
 return results
```

## 3. Metabolomics Workbench Data Retrieval

```python
def metabolomics_workbench_search(query, search_type="compound_name",
 exact_mass=None, mz_tolerance=0.01):
 """
 NIH Metabolomics Workbench REST API search。

 Parameters:
 query: str — search query
 search_type: "compound_name", "refmet", "study", "exact_mass", "mz"
 exact_mass: float — amount (search_type="exact_mass" )
 mz_tolerance: float — m/z (Da)
 """
 base_url = "https://www.metabolomicsworkbench.org/rest"

 # ToolUniverse :
 # MetabolomicsWorkbench_search_compound_by_name
 # MetabolomicsWorkbench_get_refmet_info
 # MetabolomicsWorkbench_get_study
 # MetabolomicsWorkbench_search_by_exact_mass
 # MetabolomicsWorkbench_search_by_mz
 # MetabolomicsWorkbench_get_compound_by_pubchem_cid

 if search_type == "compound_name":
 url = f"{base_url}/compound/name/{query}/all/"
 elif search_type == "refmet":
 url = f"{base_url}/refmet/name/{query}/all/"
 elif search_type == "study":
 url = f"{base_url}/study/study_id/{query}/summary/"
 elif search_type == "exact_mass":
 url = f"{base_url}/compound/exact_mass/{exact_mass}/tolerance/{mz_tolerance}/"
 elif search_type == "mz":
 url = f"{base_url}/compound/mz_value/{query}/tolerance/{mz_tolerance}/"
 else:
 raise ValueError(f"Unknown search_type: {search_type}")

 resp = requests.get(url, timeout=30)
 if resp.status_code == 200:
 try:
 data = resp.json
 if isinstance(data, list):
 df = pd.DataFrame(data)
 elif isinstance(data, dict):
 df = pd.DataFrame([data])
 else:
 df = pd.DataFrame
 except Exception:
 df = pd.DataFrame
 else:
 df = pd.DataFrame

 print(f"Metabolomics Workbench ({search_type}): {len(df)} results")
 return df
```

## 4. m/z metabolite ( DB)

```python
def identify_metabolites_by_mass(mz_values, adducts=None,
 tolerance_ppm=10,
 databases=None):
 """
 m/z valuefrommultiple DB cross-cuttingmetabolite。

 Parameters:
 mz_values: list[float] — m/z value
 adducts: list — (e.g., ["[M+H]+", "[M+Na]+", "[M-H]-"])
 tolerance_ppm: float — amount (ppm)
 databases: list — search DB ("hmdb", "metacyc", "mwb")
 """
 import numpy as np

 if adducts is None:
 adducts = [
 {"name": "[M+H]+", "mass_diff": 1.007276, "mode": "positive"},
 {"name": "[M+Na]+", "mass_diff": 22.989218, "mode": "positive"},
 {"name": "[M-H]-", "mass_diff": -1.007276, "mode": "negative"},
 {"name": "[M+NH4]+", "mass_diff": 18.034164, "mode": "positive"},
 ]

 if databases is None:
 databases = ["hmdb", "mwb"]

 all_results = []

 for mz in mz_values:
 for adduct in adducts:
 neutral_mass = mz - adduct["mass_diff"]
 tolerance_da = neutral_mass * tolerance_ppm / 1e6

 result = {
 "query_mz": mz,
 "adduct": adduct["name"],
 "neutral_mass": round(neutral_mass, 6),
 "tolerance_da": round(tolerance_da, 6),
 "databases_queried": databases,
 }
 all_results.append(result)

 df = pd.DataFrame(all_results)
 print(f"Mass-based ID: {len(mz_values)} m/z values × "
 f"{len(adducts)} adducts = {len(df)} queries "
 f"across {databases}")
 return df
```

## 5. RefMet standardization

```python
def refmet_standardize(metabolite_names):
 """
 RefMet (Reference Metabolomics) standardization。

 Parameters:
 metabolite_names: list — metabolite (standardization)
 """
 results = []

 for name in metabolite_names:
 # ToolUniverse : MetabolomicsWorkbench_get_refmet_info
 result = {
 "input_name": name,
 "refmet_name": None,
 "super_class": None,
 "main_class": None,
 "sub_class": None,
 "formula": None,
 "exact_mass": None,
 }
 results.append(result)

 df = pd.DataFrame(results)
 print(f"RefMet standardization: {len(df)} metabolites queried")
 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/hmdb_metabolites.csv` | CSV |
| `results/metacyc_pathways.json` | JSON |
| `results/mwb_compounds.csv` | CSV |
| `results/mass_id_results.csv` | CSV |
| `results/refmet_standardized.csv` | CSV |
| `figures/metabolite_class_distribution.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| HMDB | `HMDB_get_metabolite` | metabolite detail retrieval |
| HMDB | `HMDB_search` | metabolite search |
| HMDB | `HMDB_get_diseases` | diseasemetabolite |
| MetaCyc | `MetaCyc_search_pathways` | metabolismpathwaysearch |
| MetaCyc | `MetaCyc_get_pathway` | pathwaydetails |
| MetaCyc | `MetaCyc_get_compound` | compounddetails |
| MetaCyc | `MetaCyc_get_reaction` | reactiondetails |
| MWB | `MetabolomicsWorkbench_search_compound_by_name` | compoundsearch |
| MWB | `MetabolomicsWorkbench_get_refmet_info` | RefMet standardizationinformation |
| MWB | `MetabolomicsWorkbench_get_study` | researchData Retrieval |
| MWB | `MetabolomicsWorkbench_search_by_exact_mass` | amountsearch |
| MWB | `MetabolomicsWorkbench_search_by_mz` | m/z valuesearch |
| MWB | `MetabolomicsWorkbench_get_compound_by_pubchem_cid` | PubChem CID search |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-metabolomics` | PLS-DA/VIP analysis |
| `scientific-pathway-enrichment` | metabolite → pathway |
| `scientific-cheminformatics` | molecular descriptors and structural analysis |
| `scientific-systems-biology` | FBA metabolism |
| `scientific-multi-omics` | ↔ omicsintegration |

### Dependencies

`requests`, `pandas`, `numpy`, `xml.etree.ElementTree` (stdlib)

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
