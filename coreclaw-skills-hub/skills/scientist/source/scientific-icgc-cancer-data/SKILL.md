---
name: scientific-icgc-cancer-data
description: |
 ICGC cancergenomedataskill。ICGC ARGO DCC API and
 API by/viacancergenomedatasearch/
 /variant/mutationanalysis。 API (ToolUniverse integration)。
tu_tools: []
---

# Scientific ICGC Cancer Data

ICGC (International Cancer Genome Consortium) ARGO DCC API 
utilizingcancergenomedatasearchvariant/mutationcancertypecross-cuttinganalysis
pipeline.

## When to Use

- cancergenome'sdata is searchedand
- cancertype and 'scellvariant/mutationfile is investigatedand
- variant/mutation's information is retrievedand
- cancergenome's variant/mutationminwhen needed
- PCAWG (Pan-Cancer Analysis of Whole Genomes) data utilizingwhen needed
- cancergenevariant/mutation'scomparisondatawhen needed

---

## Quick Start

## 1. ICGC search

```python
import requests
import pandas as pd

ICGC_BASE = "https://dcc.icgc.org/api/v1"


def icgc_search_projects(query=None, limit=50):
 """
 ICGC — cancergenomesearch。

 Parameters:
 query: str — searchkeyword (example: "lung", "BRCA")
 limit: int — maximum results
 """
 url = f"{ICGC_BASE}/projects"
 params = {"size": limit, "from": 1}
 if query:
 params["filters"] = (
 f'{{"project":{{"primarySite":'
 f'{{"is":["{query}"]}}}}}}'
 )

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 results.append({
 "project_id": hit.get("id", ""),
 "project_name": hit.get("name", ""),
 "primary_site": hit.get("primarySite", ""),
 "tumour_type": hit.get("tumourType", ""),
 "tumour_subtype": hit.get("tumourSubtype", ""),
 "primary_country": "; ".join(
 hit.get("primaryCountries", [])),
 "total_donors": hit.get("totalDonorCount", 0),
 "ssm_count": hit.get("ssmCount", 0),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("total_donors", ascending=False)

 total = data.get("pagination", {}).get("total", 0)
 print(f"ICGC projects: {len(df)}/{total} "
 f"(query='{query}')")
 return df


def icgc_search_donors(project_id, limit=100):
 """
 ICGC — search。

 Parameters:
 project_id: str — project ID (example: "BRCA-US")
 limit: int — maximum results
 """
 url = f"{ICGC_BASE}/donors"
 params = {
 "size": limit,
 "filters": (
 f'{{"donor":{{"projectId":'
 f'{{"is":["{project_id}"]}}}}}}'
 ),
 }

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 results.append({
 "donor_id": hit.get("id", ""),
 "project_id": project_id,
 "primary_site": hit.get("primarySite", ""),
 "gender": hit.get("gender", ""),
 "vital_status": hit.get("vitalStatus", ""),
 "age_at_diagnosis": hit.get("ageAtDiagnosis"),
 "disease_status": hit.get(
 "diseaseStatusLastFollowup", ""),
 "ssm_count": hit.get("ssmCount", 0),
 })

 df = pd.DataFrame(results)
 total = data.get("pagination", {}).get("total", 0)
 print(f"ICGC donors: {len(df)}/{total} "
 f"(project={project_id})")
 return df
```

## 2. cellvariant/mutation (SSM) search

```python
def icgc_search_mutations(gene_symbol=None,
 project_id=None,
 consequence_type=None,
 limit=100):
 """
 ICGC — cellvariant/mutation (Simple Somatic Mutation) search。

 Parameters:
 gene_symbol: str — gene symbol (example: "TP53")
 project_id: str — project ID
 consequence_type: str — variant/mutation
 (example: "missense_variant")
 limit: int — maximum results
 """
 url = f"{ICGC_BASE}/mutations"
 filters = {}

 if gene_symbol:
 filters["gene"] = {"symbol": {"is": [gene_symbol]}}
 if project_id:
 filters["donor"] = {"projectId": {"is": [project_id]}}
 if consequence_type:
 filters["mutation"] = {
 "consequenceType": {"is": [consequence_type]}
 }

 import json
 params = {
 "size": limit,
 "filters": json.dumps(filters) if filters else "{}",
 }

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("hits", []):
 # key consequence retrieval
 consequences = hit.get("consequences", [])
 top_cons = consequences[0] if consequences else {}

 results.append({
 "mutation_id": hit.get("id", ""),
 "chromosome": hit.get("chromosome", ""),
 "start": hit.get("start"),
 "end": hit.get("end"),
 "mutation": hit.get("mutation", ""),
 "type": hit.get("type", ""),
 "gene_symbol": top_cons.get("geneSymbol", ""),
 "consequence_type": top_cons.get("type", ""),
 "aa_mutation": top_cons.get("aaMutation", ""),
 "affected_donors": hit.get(
 "affectedDonorCountTotal", 0),
 "affected_projects": hit.get(
 "affectedProjectCount", 0),
 "functional_impact": hit.get(
 "functionalImpact", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("affected_donors",
 ascending=False)

 total = data.get("pagination", {}).get("total", 0)
 print(f"ICGC mutations: {len(df)}/{total} "
 f"(gene={gene_symbol}, project={project_id})")
 return df
```

## 3. cancertypevariant/mutationsummary

```python
def icgc_cancer_stats(project_id=None):
 """
 ICGC — cancertypesummary。

 Parameters:
 project_id: str — project ID (None all)
 """
 if project_id:
 url = f"{ICGC_BASE}/projects/{project_id}"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 stats = {
 "project_id": project_id,
 "project_name": data.get("name", ""),
 "primary_site": data.get("primarySite", ""),
 "total_donors": data.get("totalDonorCount", 0),
 "total_specimens": data.get(
 "totalSpecimenCount", 0),
 "ssm_count": data.get("ssmCount", 0),
 "repository": "; ".join(
 data.get("repository", [])),
 }
 print(f"ICGC stats: {project_id} — "
 f"{stats['total_donors']} donors, "
 f"{stats['ssm_count']} mutations")
 return stats
 else:
 # alloverview
 projects = icgc_search_projects(limit=200)
 summary = {
 "total_projects": len(projects),
 "total_donors": projects[
 "total_donors"].sum,
 "total_ssm": projects["ssm_count"].sum,
 "top_sites": projects.groupby(
 "primary_site")["total_donors"].sum(
 ).sort_values(ascending=False).head(10
 ).to_dict,
 }
 print(f"ICGC summary: {summary['total_projects']} "
 f"projects, {summary['total_donors']} donors")
 return summary


def icgc_gene_mutation_frequency(gene_symbol, top_n=20):
 """
 ICGC — genecancertypevariant/mutationfrequency。

 Parameters:
 gene_symbol: str — gene symbol
 top_n: int — topcancertypenumber/count
 """
 mutations = icgc_search_mutations(
 gene_symbol=gene_symbol, limit=500)

 if mutations.empty:
 return pd.DataFrame

 # 
 freq = mutations.groupby("gene_symbol").agg(
 total_mutations=("mutation_id", "count"),
 total_affected_donors=("affected_donors", "sum"),
 mutation_types=("consequence_type",
 lambda x: "; ".join(x.unique[:5])),
 ).reset_index

 print(f"ICGC gene frequency: {gene_symbol} — "
 f"{len(freq)} entries")
 return freq
```

## 4. ICGC integrationpipeline

```python
def icgc_pipeline(gene_symbols, cancer_site=None,
 output_dir="results"):
 """
 ICGC integrationpipeline。

 Parameters:
 gene_symbols: list[str] — gene list
 cancer_site: str — cancerfilter
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) search
 projects = icgc_search_projects(query=cancer_site)
 projects.to_csv(output_dir / "projects.csv", index=False)

 # 2) genevariant/mutationsearch
 all_mutations = []
 for gene in gene_symbols:
 try:
 muts = icgc_search_mutations(
 gene_symbol=gene, limit=200)
 muts["query_gene"] = gene
 all_mutations.append(muts)
 except Exception as e:
 print(f" Warning: {gene} — {e}")
 continue

 if all_mutations:
 combined = pd.concat(all_mutations,
 ignore_index=True)
 combined.to_csv(output_dir / "mutations.csv",
 index=False)

 # 3) cancertype
 if not projects.empty:
 top_project = projects.iloc[0]["project_id"]
 stats = icgc_cancer_stats(project_id=top_project)
 pd.DataFrame([stats]).to_csv(
 output_dir / "cancer_stats.csv", index=False)

 print(f"ICGC pipeline: {output_dir}")
 return {"projects": projects}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| (direct) | ICGC DCC API | REST API — TU integration |

## Pipeline Integration

```
cancer-genomics → icgc-cancer-data → precision-oncology
 (cancergenomeall) (ICGC DCC API) (tumor)
 │ │ ↓
 tcga-data ────────────┘ clinical-decision-support
 (TCGA data) │ (clinical decision support)
 ↓
 variant-interpretation
 (variant/mutation)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/projects.csv` | list | → cancer-genomics |
| `results/mutations.csv` | cellvariant/mutation | → variant-interpretation |
| `results/cancer_stats.csv` | cancertype | → precision-oncology |
