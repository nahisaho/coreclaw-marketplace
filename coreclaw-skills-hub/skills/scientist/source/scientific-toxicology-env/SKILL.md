---
name: scientific-toxicology-env
description: |
 toxicityenvironmentskill。CTD (Comparative Toxicogenomics Database)
 -gene-diseaseToxCast/Tox21 looptoxicity
 IRIS evaluationT3DB /environmenttoxicityPubChem BioAssay toxicitydata。
tu_tools:
 - key: ctd
 name: CTD
 description: -disease-genedatasearch
---

# Scientific Toxicology & Environmental Health

CTD / Tox21 / ToxCast / T3DB / IRIS utilizingtoxicityenvironment
pipeline is provided。-gene-disease、loop
toxicity、evaluation。

## When to Use

- genedisease is investigatedand (CTD)
- Tox21/ToxCast data toxicityanalysiswhen needed
- IRIS evaluationdata (RfD/RfC/UR) referencewhen needed
- environmenttoxicity'sdetailsdatabase (T3DB) is searchedand
- PubChem BioAssay fromtoxicityloopdata is retrievedand
- ADMET toxicitypredictionand experimenttoxicitydata forwhen needed

---

## Quick Start

## 1. CTD -gene-diseasesearch

```python
import requests
import pandas as pd
import json

CTD_BASE = "https://ctdbase.org/tools"


def ctd_chemical_gene(chemical_name, limit=100):
 """
 CTD — -geneinteraction search。

 Parameters:
 chemical_name: str — chemical name (example: "Bisphenol A")
 limit: int — maximum retrieval count
 """
 url = f"{CTD_BASE}/batchQuery.go"
 params = {
 "inputType": "chem",
 "inputTerms": chemical_name,
 "report": "genes_curated",
 "format": "json",
 }
 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json[:limit]

 results = []
 for entry in data:
 results.append({
 "chemical": entry.get("ChemicalName", ""),
 "gene": entry.get("GeneSymbol", ""),
 "organism": entry.get("Organism", ""),
 "interaction": entry.get("Interaction", ""),
 "pubmed_ids": entry.get("PubMedIDs", ""),
 })

 df = pd.DataFrame(results)
 print(f"CTD: {chemical_name} → {len(df)} gene interactions")
 return df
```

## 2. CTD -diseasesearch

```python
def ctd_chemical_disease(chemical_name, limit=100):
 """
 CTD — -diseasesearch。

 Parameters:
 chemical_name: str — chemical name
 limit: int — maximum retrieval count
 """
 url = f"{CTD_BASE}/batchQuery.go"
 params = {
 "inputType": "chem",
 "inputTerms": chemical_name,
 "report": "diseases_curated",
 "format": "json",
 }
 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json[:limit]

 results = []
 for entry in data:
 results.append({
 "chemical": entry.get("ChemicalName", ""),
 "disease": entry.get("DiseaseName", ""),
 "disease_id": entry.get("DiseaseID", ""),
 "direct_evidence": entry.get("DirectEvidence", ""),
 "inference_score": float(entry.get("InferenceScore", 0)),
 })

 df = pd.DataFrame(results)
 df = df.sort_values("inference_score", ascending=False)
 print(f"CTD: {chemical_name} → {len(df)} disease associations")
 return df
```

## 3. Tox21/ToxCast Data Retrieval

```python
COMPTOX_BASE = "https://comptox.epa.gov/dashboard/api"


def tox21_assay_search(chemical_identifier, assay_source="Tox21"):
 """
 CompTox Dashboard — Tox21/ToxCast resultsretrieval。

 Parameters:
 chemical_identifier: str — DTXSID or CAS
 assay_source: str — "Tox21" or "ToxCast"
 """
 # CompTox Dashboard API 'sData Retrieval
 url = f"{COMPTOX_BASE}/chemical/search"
 params = {"query": chemical_identifier}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 chem_data = resp.json

 dtxsid = chem_data.get("dtxsid", chemical_identifier)

 # endpointretrieval
 url_assay = f"{COMPTOX_BASE}/chemical/{dtxsid}/assays"
 resp_assay = requests.get(url_assay, timeout=30)
 resp_assay.raise_for_status
 assays = resp_assay.json

 results = []
 for assay in assays:
 if assay_source.lower in assay.get("assaySource", "").lower:
 results.append({
 "assay_name": assay.get("assayName", ""),
 "assay_source": assay.get("assaySource", ""),
 "endpoint": assay.get("assayEndpoint", ""),
 "activity": assay.get("activity", ""),
 "ac50_um": assay.get("ac50", None),
 "hit_call": assay.get("hitCall", ""),
 })

 df = pd.DataFrame(results)
 n_active = (df["hit_call"] == "Active").sum if len(df) > 0 else 0
 print(f"Tox21/ToxCast: {dtxsid} → {len(df)} assays, {n_active} active")
 return df
```

## 4. T3DB toxicitysearch

```python
T3DB_BASE = "https://t3db.ca/api"


def t3db_search(query, search_type="name"):
 """
 T3DB — /environmenttoxicitydatabasesearch。

 Parameters:
 query: str — search term
 search_type: str — "name", "cas", "category"
 """
 url = f"{T3DB_BASE}/toxins/search"
 params = {"query": query, "search_type": search_type}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for toxin in data.get("toxins", []):
 results.append({
 "name": toxin.get("name", ""),
 "t3db_id": toxin.get("t3db_id", ""),
 "cas_number": toxin.get("cas_number", ""),
 "category": toxin.get("category", ""),
 "toxicity_class": toxin.get("toxicity_class", ""),
 "ld50_oral": toxin.get("ld50_oral", ""),
 "target_organs": toxin.get("target_organs", []),
 })

 df = pd.DataFrame(results)
 print(f"T3DB: '{query}' → {len(df)} toxins")
 return df
```

## 5. EPA IRIS evaluation

```python
def iris_risk_assessment(chemical_name):
 """
 EPA IRIS — evaluationData Retrieval。

 Parameters:
 chemical_name: str — chemical name
 """
 url = "https://iris.epa.gov/AtoZ"
 resp = requests.get(url, timeout=30)

 # IRIS structure API — ordata
 # : CompTox Dashboard API 
 url_comptox = f"{COMPTOX_BASE}/chemical/search"
 params = {"query": chemical_name}
 resp = requests.get(url_comptox, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 risk_data = {
 "chemical": chemical_name,
 "dtxsid": data.get("dtxsid", ""),
 "rfd_oral_mg_kg_day": data.get("rfdOral", None),
 "rfc_inhalation_mg_m3": data.get("rfcInhalation", None),
 "cancer_classification": data.get("cancerClassification", ""),
 "oral_slope_factor": data.get("oralSlopeFactor", None),
 "inhalation_unit_risk": data.get("inhalationUnitRisk", None),
 }

 print(f"IRIS: {chemical_name}")
 for k, v in risk_data.items:
 if v and k != "chemical":
 print(f" {k}: {v}")
 return risk_data
```

## 6. toxicitypathway analysis

```python
def toxicity_pathway_analysis(chemical_name, species="Homo sapiens"):
 """
 CTD + pathwayintegrationtoxicityanalysis。

 Parameters:
 chemical_name: str — chemical name
 species: str — organism/species
 """
 # 1) CTD generetrieval
 gene_df = ctd_chemical_gene(chemical_name, limit=500)
 if species:
 gene_df = gene_df[gene_df["organism"] == species]

 gene_list = gene_df["gene"].unique.tolist

 # 2) CTD diseaseretrieval
 disease_df = ctd_chemical_disease(chemical_name, limit=100)

 # 3) pathway (KEGG enrichment via Enrichr)
 enrichr_url = "https://maayanlab.cloud/Enrichr"
 add_resp = requests.post(
 f"{enrichr_url}/addList",
 files={"list": (None, "\n".join(gene_list))}
 )
 user_list_id = add_resp.json["userListId"]

 enrich_resp = requests.get(
 f"{enrichr_url}/enrich",
 params={"userListId": user_list_id, "backgroundType": "KEGG_2021_Human"}
 )
 pathways = enrich_resp.json.get("KEGG_2021_Human", [])

 pathway_results = []
 for pw in pathways[:20]:
 pathway_results.append({
 "pathway": pw[1],
 "p_value": pw[2],
 "adj_p_value": pw[6],
 "genes": pw[5],
 })

 print(f"Toxicity pathway: {chemical_name}")
 print(f" Target genes: {len(gene_list)}")
 print(f" Diseases: {len(disease_df)}")
 print(f" Pathways: {len(pathway_results)}")
 return {
 "genes": gene_df,
 "diseases": disease_df,
 "pathways": pd.DataFrame(pathway_results),
 }
```

---

## Pipeline Integration

```
admet-pharmacokinetics → toxicology-env → pharmacovigilance
 (ADMET toxicityprediction) (CTD/Tox21/IRIS) (all)
 │ │ ↓
cheminformatics ───────────────┘ disease-research
 (RDKit structurealert) │ (disease-gene)
 ↓
 public-health-data
 (CDC/WHO )
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/ctd_gene_interactions.csv` | CTD -gene | → pathway-enrichment |
| `results/ctd_disease_associations.csv` | CTD -disease | → disease-research |
| `results/tox21_assays.csv` | Tox21/ToxCast results | → admet-pharmacokinetics |
| `results/toxicity_pathways.json` | toxicitypathway analysisresults | → pharmacovigilance |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `ctd` | CTD | -disease-genedatasearch |
