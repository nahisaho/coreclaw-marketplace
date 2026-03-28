---
name: scientific-monarch-ontology
description: |
 Monarch Initiative disease-tabletypeskill。
 Monarch Initiative API usingdisease-gene-tabletype
 HPO 
 gene-diseasesearch。
 ToolUniverse integration: monarch。
tu_tools:
 - key: monarch
 name: Monarch Initiative
 description: disease-tabletype-geneintegration API
---

# Scientific Monarch Initiative Ontology

Monarch Initiative API utilizingdisease-gene-tabletype
retrievalHPO 
searchpipeline is provided。

## When to Use

- disease's genetabletype (HPO) is searchedand
- genefromdiseasetabletypewhen needed
- HPO forwhen needed
- for's degreecalculationwhen needed
- disease-tabletype-gene'sintegrationwhen needed

---

## Quick Start

## 1. disease-gene-tabletype

```python
import requests
import pandas as pd

MONARCH_API = "https://api.monarchinitiative.org/v3/api"


def monarch_disease_genes(disease_id, limit=50):
 """
 Monarch — disease→generetrieval。

 Parameters:
 disease_id: str — disease ID
 (example: "MONDO:0007254" = breast cancer)
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/association"
 params = {
 "subject": disease_id,
 "category": "biolink:GeneToDiseaseAssociation",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 obj = item.get("object", {})
 rows.append({
 "disease_id": disease_id,
 "gene_id": obj.get("id", ""),
 "gene_label": obj.get("label", ""),
 "relation": item.get("predicate", ""),
 "source": "; ".join(
 item.get("provided_by", [])),
 })

 df = pd.DataFrame(rows)
 print(f"Monarch disease→genes: {disease_id} "
 f"→ {len(df)} genes")
 return df


def monarch_disease_phenotypes(disease_id, limit=100):
 """
 Monarch — disease→tabletype (HPO) retrieval。

 Parameters:
 disease_id: str — disease ID
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/association"
 params = {
 "subject": disease_id,
 "category":
 "biolink:DiseaseToPhenotypicFeatureAssociation",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 obj = item.get("object", {})
 rows.append({
 "disease_id": disease_id,
 "phenotype_id": obj.get("id", ""),
 "phenotype_label": obj.get("label", ""),
 "frequency": item.get("frequency_qualifier",
 ""),
 "onset": item.get("onset_qualifier", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Monarch disease→phenotypes: {disease_id} "
 f"→ {len(df)} HPO terms")
 return df
```

## 2. gene→disease

```python
def monarch_gene_diseases(gene_id, limit=50):
 """
 Monarch — gene→diseaseretrieval。

 Parameters:
 gene_id: str — gene ID
 (example: "HGNC:1100" = BRCA1)
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/association"
 params = {
 "subject": gene_id,
 "category": "biolink:GeneToDiseaseAssociation",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 obj = item.get("object", {})
 rows.append({
 "gene_id": gene_id,
 "disease_id": obj.get("id", ""),
 "disease_label": obj.get("label", ""),
 "relation": item.get("predicate", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Monarch gene→diseases: {gene_id} "
 f"→ {len(df)} diseases")
 return df
```

## 3. searchfor

```python
def monarch_search(query, category=None, limit=25):
 """
 Monarch — search。

 Parameters:
 query: str — search query
 category: str — filter
 (example: "biolink:Disease", "biolink:Gene",
 "biolink:PhenotypicFeature")
 limit: int — maximum results
 """
 url = f"{MONARCH_API}/search"
 params = {"q": query, "limit": limit}
 if category:
 params["category"] = category

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data.get("items", []):
 rows.append({
 "id": item.get("id", ""),
 "label": item.get("name", ""),
 "category": item.get("category", ""),
 "description": (item.get("description", "")
 or "")[:200],
 })

 df = pd.DataFrame(rows)
 print(f"Monarch search: '{query}' → {len(df)}")
 return df
```

## 4. Monarch integrationpipeline

```python
def monarch_pipeline(disease_query,
 output_dir="results"):
 """
 Monarch integrationpipeline。

 Parameters:
 disease_query: str — disease or ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) diseasesearch
 diseases = monarch_search(disease_query,
 category="biolink:Disease")
 diseases.to_csv(output_dir / "monarch_diseases.csv",
 index=False)

 if diseases.empty:
 print(f"Monarch: '{disease_query}' not found")
 return {"diseases": diseases}

 disease_id = diseases.iloc[0]["id"]

 # 2) gene
 genes = monarch_disease_genes(disease_id)
 genes.to_csv(output_dir / "monarch_genes.csv",
 index=False)

 # 3) tabletype (HPO)
 phenotypes = monarch_disease_phenotypes(disease_id)
 phenotypes.to_csv(
 output_dir / "monarch_phenotypes.csv",
 index=False)

 print(f"Monarch pipeline: {disease_query} "
 f"→ {output_dir}")
 return {"genes": genes, "phenotypes": phenotypes}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `monarch` | Monarch Initiative | disease-tabletype-geneintegration |

## Pipeline Integration

```
disease-research → monarch-ontology → rare-disease-genetics
 (GWAS/DisGeNET) (Monarch API) (OMIM/Orphanet)
 │ │ ↓
variant-interpretation ───┘ ontology-enrichment
 (ClinVar/ACMG) (EFO/OLS/Enrichr)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/monarch_diseases.csv` | diseasesearchresults | → disease-research |
| `results/monarch_genes.csv` | gene | → variant-interpretation |
| `results/monarch_phenotypes.csv` | HPO tabletype | → rare-disease-genetics |
