---
name: scientific-reactome-pathways
description: |
 Reactome pathwayskill。Reactome Content Service
 REST API by/viapathwaysearchretrievalUniProt mapping
 pathwayfigureData Retrieval。ToolUniverse integration: reactome。
tu_tools:
 - key: reactome
 name: Reactome
 description: pathwaydatabase REST API
---

# Scientific Reactome Pathways

Reactome Content Service REST API utilizingpathwaysearch
structureretrievalUniProt accession→pathway mapping
pathwayfigureData Retrievalpipeline is provided。

## When to Use

- pathway name and keywordsearchwhen needed
- pathway is retrievedand
- UniProt accessionfrompathway mappingwhen needed
- pathway's (protein/compound) when needed
- pathwayfigure's layoutdata is retrievedand

---

## Quick Start

## 1. pathwaysearchdetailsretrieval

```python
import requests
import pandas as pd

REACTOME = "https://reactome.org/ContentService"


def reactome_search(query, species="Homo sapiens",
 limit=25):
 """
 Reactome — pathwaysearch。

 Parameters:
 query: str — search query (example: "apoptosis", "MAPK")
 species: str — species name (example: "Homo sapiens")
 limit: int — maximum results
 """
 url = f"{REACTOME}/search/query"
 params = {
 "query": query,
 "species": species,
 "types": "Pathway",
 "cluster": "true",
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for group in data.get("results", []):
 for entry in group.get("entries", [])[:limit]:
 rows.append({
 "stId": entry.get("stId", ""),
 "name": entry.get("name", ""),
 "species": entry.get("species", ""),
 "exact_type": entry.get(
 "exactType", ""),
 "compartments": "; ".join(
 entry.get("compartmentNames", [])),
 })

 df = pd.DataFrame(rows[:limit])
 print(f"Reactome search: '{query}' → {len(df)} "
 f"pathways")
 return df


def reactome_pathway_detail(pathway_id):
 """
 Reactome — pathwaydetailsretrieval。

 Parameters:
 pathway_id: str — Reactome Stable ID
 (example: "R-HSA-109581")
 """
 url = f"{REACTOME}/data/pathway/{pathway_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 result = {
 "stId": data.get("stId", ""),
 "name": data.get("displayName", ""),
 "species": data.get("speciesName", ""),
 "is_inferred": data.get("isInferred", False),
 "has_diagram": data.get("hasDiagram", False),
 "n_sub_events": len(
 data.get("hasEvent", [])),
 "n_compartments": len(
 data.get("compartment", [])),
 "release_date": data.get("releaseDate", ""),
 }
 return result
```

## 2. UniProt→pathway mapping

```python
def reactome_uniprot_pathways(uniprot_id,
 species="Homo sapiens"):
 """
 Reactome — UniProt → pathway mapping。

 Parameters:
 uniprot_id: str — UniProt accession
 (example: "P38398" = BRCA1)
 species: str — species name
 """
 url = f"{REACTOME}/data/pathways/low/entity/{uniprot_id}"
 params = {"species": species}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for pw in data:
 rows.append({
 "pathway_id": pw.get("stId", ""),
 "pathway_name": pw.get("displayName", ""),
 "species": pw.get("speciesName", ""),
 "has_diagram": pw.get("hasDiagram", False),
 })

 df = pd.DataFrame(rows)
 print(f"Reactome UniProt→pathway: {uniprot_id} "
 f"→ {len(df)} pathways")
 return df
```

## 3. pathwayretrieval

```python
def reactome_participants(pathway_id):
 """
 Reactome — pathwaylist。

 Parameters:
 pathway_id: str — Reactome Stable ID
 """
 url = (f"{REACTOME}/data/participants/"
 f"{pathway_id}")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 rows = []
 for item in data:
 pe_name = item.get("displayName", "")
 for ref in item.get("refEntities", []):
 rows.append({
 "pathway_id": pathway_id,
 "participant": pe_name,
 "db_name": ref.get("databaseName", ""),
 "identifier": ref.get("identifier", ""),
 "name": ref.get("displayName", ""),
 })

 df = pd.DataFrame(rows)
 print(f"Reactome participants: {pathway_id} "
 f"→ {len(df)} entities")
 return df
```

## 4. Reactome integrationpipeline

```python
def reactome_pipeline(query_or_uniprot,
 output_dir="results"):
 """
 Reactome integrationpipeline。

 Parameters:
 query_or_uniprot: str — search query or UniProt ID
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 is_uniprot = (len(query_or_uniprot) == 6
 and query_or_uniprot[0].isalpha)

 if is_uniprot:
 # UniProt → pathway
 pathways = reactome_uniprot_pathways(
 query_or_uniprot)
 else:
 # search
 pathways = reactome_search(query_or_uniprot)

 pathways.to_csv(output_dir / "reactome_pathways.csv",
 index=False)

 # pathway's
 if not pathways.empty:
 top_id = (pathways.iloc[0].get("pathway_id")
 or pathways.iloc[0].get("stId"))
 parts = reactome_participants(top_id)
 parts.to_csv(
 output_dir / "reactome_participants.csv",
 index=False)

 print(f"Reactome pipeline: {output_dir}")
 return {"pathways": pathways}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `reactome` | Reactome | pathwaydatabase REST API |

## Pipeline Integration

```
pathway-enrichment → reactome-pathways → systems-biology
 (GO/pathway) (Reactome API) (networkanalysis)
 │ │ ↓
uniprot-proteome ──────────┘ metabolomics-databases
 (UniProt ID) (MetaCyc metabolism)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/reactome_pathways.csv` | pathwaylist | → pathway-enrichment |
| `results/reactome_participants.csv` | | → protein-interaction-network |
