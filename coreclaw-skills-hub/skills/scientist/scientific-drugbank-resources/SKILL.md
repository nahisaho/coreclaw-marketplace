---
name: scientific-drugbank-resources
description: |
 DrugBank resource skill. Drug information retrieval, drug-target interactions, drug-drug interactions, pharmacological classifications, and clinical indication mapping.
tu_tools:
 - key: drugbank
 name: DrugBank
 description: database API
---

# Scientific DrugBank Resources

DrugBank API utilizinginformation (MOA)protein
searchdruginteraction (DDI) pipeline is provided。

## When to Use

- 's basicinformation (nameclassificationstructure) is searchedand
- (MOA) is investigatedand
- proteinfromsearchwhen needed
- druginteraction (DDI) is verifiedand
- 's ADMET is retrievedand

---

## Quick Start

## 1. searchbasicinformation

```python
import requests
import pandas as pd

DRUGBANK_API = "https://api.drugbank.com/v1"


def drugbank_search(query, limit=25, api_key=None):
 """
 DrugBank — search。

 Parameters:
 query: str — search query (example: "imatinib")
 limit: int — maximum results
 api_key: str — DrugBank API key
 """
 headers = {}
 if api_key:
 headers["Authorization"] = f"Bearer {api_key}"

 url = f"{DRUGBANK_API}/drugs"
 params = {"q": query, "per_page": limit}
 resp = requests.get(url, params=params,
 headers=headers, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for d in data:
 rows.append({
 "drugbank_id": d.get("drugbank_id", ""),
 "name": d.get("name", ""),
 "cas_number": d.get("cas_number", ""),
 "drug_type": d.get("type", ""),
 "state": d.get("state", ""),
 "description": (d.get("description", "")
 [:200]),
 })

 df = pd.DataFrame(rows)
 print(f"DrugBank search: '{query}' → {len(df)} drugs")
 return df


def drugbank_drug_detail(drugbank_id, api_key=None):
 """
 DrugBank — detailsretrieval。

 Parameters:
 drugbank_id: str — DrugBank ID (example: "DB01254")
 api_key: str — DrugBank API key
 """
 headers = {}
 if api_key:
 headers["Authorization"] = f"Bearer {api_key}"

 url = f"{DRUGBANK_API}/drugs/{drugbank_id}"
 resp = requests.get(url, headers=headers, timeout=30)
 resp.raise_for_status
 data = resp.json

 result = {
 "drugbank_id": data.get("drugbank_id", ""),
 "name": data.get("name", ""),
 "description": data.get("description", ""),
 "indication": data.get("indication", ""),
 "pharmacodynamics": data.get(
 "pharmacodynamics", ""),
 "mechanism_of_action": data.get(
 "mechanism_of_action", ""),
 "absorption": data.get("absorption", ""),
 "half_life": data.get("half_life", ""),
 "protein_binding": data.get(
 "protein_binding", ""),
 "molecular_weight": data.get(
 "average_molecular_weight", ""),
 }
 return result
```

## 2. protein search

```python
def drugbank_targets(drugbank_id, api_key=None):
 """
 DrugBank — 'sproteinretrieval。

 Parameters:
 drugbank_id: str — DrugBank ID
 api_key: str — DrugBank API key
 """
 headers = {}
 if api_key:
 headers["Authorization"] = f"Bearer {api_key}"

 url = f"{DRUGBANK_API}/drugs/{drugbank_id}/targets"
 resp = requests.get(url, headers=headers, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for t in data:
 polypeptide = t.get("polypeptide", {}) or {}
 rows.append({
 "drugbank_id": drugbank_id,
 "target_name": t.get("name", ""),
 "organism": t.get("organism", ""),
 "known_action": t.get("known_action", ""),
 "gene_name": polypeptide.get(
 "gene_name", ""),
 "uniprot_id": polypeptide.get(
 "external_identifiers", {}).get(
 "UniProtKB", ""),
 })

 df = pd.DataFrame(rows)
 print(f"DrugBank targets: {drugbank_id} "
 f"→ {len(df)} targets")
 return df
```

## 3. druginteraction (DDI)

```python
def drugbank_interactions(drugbank_id, api_key=None):
 """
 DrugBank — druginteractionretrieval。

 Parameters:
 drugbank_id: str — DrugBank ID
 api_key: str — DrugBank API key
 """
 headers = {}
 if api_key:
 headers["Authorization"] = f"Bearer {api_key}"

 url = (f"{DRUGBANK_API}/drugs/"
 f"{drugbank_id}/drug_interactions")
 resp = requests.get(url, headers=headers, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for inter in data:
 rows.append({
 "drug_a": drugbank_id,
 "drug_b_id": inter.get(
 "drugbank_id", ""),
 "drug_b_name": inter.get("name", ""),
 "description": inter.get(
 "description", "")[:300],
 })

 df = pd.DataFrame(rows)
 print(f"DrugBank DDI: {drugbank_id} "
 f"→ {len(df)} interactions")
 return df
```

## 4. DrugBank integrationpipeline

```python
def drugbank_pipeline(drug_name, api_key=None,
 output_dir="results"):
 """
 DrugBank integrationpipeline。

 Parameters:
 drug_name: str — (example: "imatinib")
 api_key: str — DrugBank API key
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) search
 results = drugbank_search(drug_name,
 api_key=api_key)
 results.to_csv(output_dir / "drugbank_search.csv",
 index=False)

 if results.empty:
 print(f"DrugBank: '{drug_name}' not found")
 return {"search": results}

 db_id = results.iloc[0]["drugbank_id"]

 # 2) details
 detail = drugbank_drug_detail(db_id,
 api_key=api_key)
 pd.DataFrame([detail]).to_csv(
 output_dir / "drugbank_detail.csv",
 index=False)

 # 3) 
 targets = drugbank_targets(db_id,
 api_key=api_key)
 targets.to_csv(output_dir / "drugbank_targets.csv",
 index=False)

 # 4) DDI
 ddi = drugbank_interactions(db_id,
 api_key=api_key)
 ddi.to_csv(output_dir / "drugbank_ddi.csv",
 index=False)

 print(f"DrugBank pipeline: {drug_name} → {output_dir}")
 return {"detail": detail, "targets": targets,
 "ddi": ddi}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `drugbank` | DrugBank | database API |

## Pipeline Integration

```
drug-target-profiling → drugbank-resources → admet-pharmacokinetics
  (DrugBank API) (ADMET prediction)
 │ │ ↓
opentargets-genetics ──────────┘ compound-screening
 (OT ) (ZINC compoundsearch)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/drugbank_search.csv` | searchresults | → drug-target-profiling |
| `results/drugbank_detail.csv` | details | → admet-pharmacokinetics |
| `results/drugbank_targets.csv` | protein | → protein-interaction-network |
| `results/drugbank_ddi.csv` | druginteraction | → pharmacogenomics |

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
