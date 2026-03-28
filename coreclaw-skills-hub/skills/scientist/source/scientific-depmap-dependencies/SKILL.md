---
name: scientific-depmap-dependencies
description: |
 DepMap dependencyskill。Cancer Dependency Map (DepMap) Portal
 API by/viacancercell CRISPR/RNAi dependency
 datageneretrieval。ToolUniverse integration: depmap。
tu_tools:
 - key: depmap
 name: DepMap
 description: cancercelldependency API
---

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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `depmap` | DepMap | cancercelldependency API |

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
