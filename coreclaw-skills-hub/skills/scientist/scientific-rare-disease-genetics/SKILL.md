---
name: scientific-rare-disease-genetics
description: |
 Rare disease genetics skill. Rare variant prioritization, exome/genome sequencing analysis, phenotype-driven gene ranking, and diagnostic yield optimization.
tu_tools:
 - key: orphanet
 name: Orphanet
 description: diseaseclassificationgeneratedatabase
---

# Scientific Rare Disease Genetics

OMIM / Orphanet / DisGeNET / IMPC integration
diseasepipeline is provided。

## When to Use

- disease's genewhen needed
- OMIM gene-disease's Mendelian is investigatedand
- Orphanet diseaseclassification and rate is searchedand
- DisGeNET disease-gene (GDA) is retrievedand
- IMPC tabletype andcomparisonwhen needed

---

## Quick Start

## 1. OMIM gene-diseasemapping

```python
import requests
import pandas as pd

OMIM_API = "https://api.omim.org/api"


def search_omim(query, api_key, include="geneMap"):
 """
 OMIM databasesearch。

 Parameters:
 query: str — search term (gene name、disease)
 api_key: str — OMIM API 
 include: str — "geneMap", "clinicalSynopsis", "all"

 ToolUniverse:
 OMIM_search(query=query)
 OMIM_get_entry(mim_number=mim_number)
 OMIM_get_gene_map(gene_symbol=gene_symbol)
 OMIM_get_clinical_synopsis(mim_number=mim_number)
 """
 params = {
 "search": query,
 "include": include,
 "format": "json",
 "apiKey": api_key,
 }
 resp = requests.get(f"{OMIM_API}/entry/search", params=params)
 resp.raise_for_status
 data = resp.json

 entries = data.get("omim", {}).get("searchResponse", {}).get("entryList", [])
 results = []
 for entry in entries:
 e = entry.get("entry", {})
 gene_map = e.get("geneMap", {})
 results.append({
 "mim_number": e.get("mimNumber"),
 "title": e.get("titles", {}).get("preferredTitle", ""),
 "gene_symbols": gene_map.get("geneSymbols", ""),
 "chromosome": gene_map.get("computedCytoLocation", ""),
 "phenotypes": [
 p.get("phenotype", "")
 for p in gene_map.get("phenotypeMapList", [])
 ],
 "inheritance": [
 p.get("phenotypeMappingKey", "")
 for p in gene_map.get("phenotypeMapList", [])
 ],
 })

 df = pd.DataFrame(results)
 print(f"OMIM search '{query}': {len(df)} entries")
 return df
```

## 2. Orphanet diseaseclassification

```python
ORPHANET_API = "https://api.orphadata.com"


def search_orphanet_diseases(query):
 """
 Orphanet diseasesearch。

 ToolUniverse:
 Orphanet_search_diseases(query=query)
 Orphanet_search_by_name(name=query)
 Orphanet_get_disease(orpha_code=code)
 Orphanet_get_genes(orpha_code=code)
 Orphanet_get_classification(orpha_code=code)
 """
 resp = requests.get(
 f"{ORPHANET_API}/rd-cross-referencing",
 params={"query": query}
 )
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data if isinstance(data, list) else [data]:
 results.append({
 "orpha_code": item.get("ORPHAcode", ""),
 "name": item.get("Preferred term", ""),
 "prevalence_class": item.get("Prevalence", {}).get("PrevalenceClass", ""),
 "inheritance": item.get("TypeOfInheritance", []),
 "age_of_onset": item.get("AgeOfOnset", []),
 "genes": item.get("DisorderGeneAssociationList", []),
 })

 df = pd.DataFrame(results)
 print(f"Orphanet search '{query}': {len(df)} diseases")
 return df
```

## 3. DisGeNET disease-gene

```python
DISGENET_API = "https://www.disgenet.org/api"


def get_disease_gene_associations(disease_id, api_key):
 """
 DisGeNET GDA by/viadisease-generetrieval。

 Parameters:
 disease_id: str — UMLS CUI (e.g., "C0023264") or disease name
 api_key: str — DisGeNET API key

 ToolUniverse:
 DisGeNET_search_disease(query=disease_id)
 DisGeNET_get_disease_genes(disease_id=disease_id)
 DisGeNET_search_gene(query=gene)
 DisGeNET_get_gene_diseases(gene_symbol=gene)
 DisGeNET_get_variant_diseases(variant_id=variant)
 """
 headers = {"Authorization": f"Bearer {api_key}"}
 resp = requests.get(
 f"{DISGENET_API}/gda/disease/{disease_id}",
 headers=headers
 )
 resp.raise_for_status
 data = resp.json

 results = []
 for gda in data:
 results.append({
 "gene_symbol": gda.get("gene_symbol", ""),
 "gene_id": gda.get("geneid", ""),
 "gda_score": gda.get("score", 0),
 "ei": gda.get("ei", 0), # Evidence Index
 "el": gda.get("el", ""), # Evidence Level
 "n_pmids": gda.get("pmid_count", 0),
 "source": gda.get("source", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("gda_score", ascending=False)

 print(f"DisGeNET '{disease_id}': {len(df)} gene associations, "
 f"top GDA score={df['gda_score'].max:.3f}" if len(df) > 0 else "")
 return df
```

## 4. IMPC tabletypereference

```python
IMPC_API = "https://www.ebi.ac.uk/mi/impc/solr"


def get_impc_mouse_phenotypes(gene_symbol):
 """
 IMPC tabletypeData Retrieval。

 ToolUniverse:
 IMPC_search_genes(query=gene_symbol)
 IMPC_get_gene_summary(gene_symbol=gene_symbol)
 IMPC_get_phenotypes_by_gene(gene_symbol=gene_symbol)
 IMPC_get_gene_phenotype_hits(gene_symbol=gene_symbol)
 """
 params = {
 "q": f"marker_symbol:{gene_symbol}",
 "rows": 100,
 "wt": "json",
 }
 resp = requests.get(f"{IMPC_API}/genotype-phenotype/select", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for doc in data.get("response", {}).get("docs", []):
 results.append({
 "gene_symbol": doc.get("marker_symbol", ""),
 "mp_term_id": doc.get("mp_term_id", ""),
 "mp_term_name": doc.get("mp_term_name", ""),
 "top_level_mp": doc.get("top_level_mp_term_name", []),
 "p_value": doc.get("p_value", None),
 "effect_size": doc.get("effect_size", None),
 "zygosity": doc.get("zygosity", ""),
 "procedure_name": doc.get("procedure_name", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty and "p_value" in df.columns:
 df = df.sort_values("p_value")

 print(f"IMPC '{gene_symbol}': {len(df)} phenotype associations")
 return df
```

## 5. gene-tabletypeintegrated analysis

```python
def rare_disease_gene_analysis(gene_symbol, omim_api_key=None,
 disgenet_api_key=None):
 """
 all DB integration's diseasegene。
 """
 profile = {"gene": gene_symbol, "sources": {}}

 # 1. OMIM
 if omim_api_key:
 try:
 omim_df = search_omim(gene_symbol, omim_api_key)
 profile["sources"]["omim"] = {
 "entries": len(omim_df),
 "phenotypes": omim_df["phenotypes"].explode.dropna.unique.tolist
 if not omim_df.empty else [],
 }
 except Exception as e:
 profile["sources"]["omim"] = {"error": str(e)}

 # 2. Orphanet
 try:
 orpha_df = search_orphanet_diseases(gene_symbol)
 profile["sources"]["orphanet"] = {
 "diseases": len(orpha_df),
 "names": orpha_df["name"].tolist if not orpha_df.empty else [],
 }
 except Exception as e:
 profile["sources"]["orphanet"] = {"error": str(e)}

 # 3. DisGeNET
 if disgenet_api_key:
 try:
 dgn_df = get_disease_gene_associations(gene_symbol, disgenet_api_key)
 profile["sources"]["disgenet"] = {
 "associations": len(dgn_df),
 "max_gda_score": float(dgn_df["gda_score"].max)
 if not dgn_df.empty else 0,
 }
 except Exception as e:
 profile["sources"]["disgenet"] = {"error": str(e)}

 # 4. IMPC
 try:
 impc_df = get_impc_mouse_phenotypes(gene_symbol)
 profile["sources"]["impc"] = {
 "phenotypes": len(impc_df),
 "top_phenotypes": impc_df["mp_term_name"].head(5).tolist
 if not impc_df.empty else [],
 }
 except Exception as e:
 profile["sources"]["impc"] = {"error": str(e)}

 n_sources = sum(1 for v in profile["sources"].values if "error" not in v)
 print(f"Rare disease profile '{gene_symbol}': {n_sources}/4 sources OK")
 return profile
```

## References

### Output Files

| File | Format |
|---|---|
| `results/omim_search.csv` | CSV |
| `results/orphanet_diseases.csv` | CSV |
| `results/disgenet_gda.csv` | CSV |
| `results/impc_phenotypes.csv` | CSV |
| `results/rare_disease_profile.json` | JSON |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| OMIM | `OMIM_search` | gene/diseasesearch |
| OMIM | `OMIM_get_entry` | MIM entryretrieval |
| OMIM | `OMIM_get_gene_map` | gene |
| OMIM | `OMIM_get_clinical_synopsis` | overview |
| Orphanet | `Orphanet_search_diseases` | diseasesearch |
| Orphanet | `Orphanet_get_disease` | diseasedetails |
| Orphanet | `Orphanet_get_genes` | gene |
| Orphanet | `Orphanet_get_classification` | classificationinformation |
| Orphanet | `Orphanet_search_by_name` | namesearch |
| DisGeNET | `DisGeNET_search_disease` | diseasesearch |
| DisGeNET | `DisGeNET_get_disease_genes` | diseasegene |
| DisGeNET | `DisGeNET_get_gene_diseases` | genedisease |
| DisGeNET | `DisGeNET_get_variant_diseases` | disease |
| IMPC | `IMPC_search_genes` | genesearch |
| IMPC | `IMPC_get_gene_summary` | genesummary |
| IMPC | `IMPC_get_phenotypes_by_gene` | tabletyperetrieval |
| IMPC | `IMPC_get_gene_phenotype_hits` | number/count |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-disease-research` | GWAS/Orphanet diseaseresearch |
| `scientific-variant-interpretation` | ACMG |
| `scientific-variant-effect-prediction` | prediction |
| `scientific-population-genetics` | population genetics |
| `scientific-human-protein-atlas` | proteinexpression |

### Dependencies

`requests`, `pandas`

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
