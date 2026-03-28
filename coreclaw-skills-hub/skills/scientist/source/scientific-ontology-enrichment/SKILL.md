---
name: scientific-ontology-enrichment
description: |
 analysisskill。EFO experiment、
 OLS search、Enrichr geneanalysis、
 UMLS system'sintegrationpipeline。
---

# Scientific Ontology Enrichment

EFO / OLS / Enrichr / UMLS integration
searchanalysispipeline is provided。

## When to Use

- EFO experimentcondition (diseasecelltypetissue) 's ID is retrievedand
- OLS multiplecross-cuttingsearch (HP, MONDO, DOID, GO, CHEBI) when needed
- Enrichr gene list'sanalysis is performedand
- UMLS CUI differentforsystem'smapping is performedand
- GWAS Catalog 's trait EFO forstandardizationwhen needed

---

## Quick Start

## 1. EFO experiment

```python
import requests
import pandas as pd

OLS_API = "https://www.ebi.ac.uk/ols4/api"


def search_efo(query, exact=False):
 """
 EFO (Experimental Factor Ontology) search。

 Parameters:
 query: str — search term (disease、celltype、tissue)
 exact: bool — allsearch

 ToolUniverse:
 EFO_search(query=query, exact=exact)
 """
 params = {
 "q": query,
 "ontology": "efo",
 "exact": str(exact).lower,
 "rows": 30,
 }
 resp = requests.get(f"{OLS_API}/search", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for doc in data.get("response", {}).get("docs", []):
 results.append({
 "efo_id": doc.get("obo_id", ""),
 "label": doc.get("label", ""),
 "description": (doc.get("description") or [""])[0][:200],
 "iri": doc.get("iri", ""),
 "ontology": doc.get("ontology_name", ""),
 "is_defining_ontology": doc.get("is_defining_ontology", False),
 "synonyms": doc.get("synonym", []),
 })

 df = pd.DataFrame(results)
 print(f"EFO search '{query}': {len(df)} terms")
 return df
```

## 2. OLS search

```python
def search_ols(query, ontologies=None, type_filter=None):
 """
 OLS (Ontology Lookup Service) cross-cuttingsearch。

 Parameters:
 query: str — search term
 ontologies: list — ID (e.g., ["hp", "mondo", "go"])
 type_filter: str — "class", "property", "individual"

 ToolUniverse:
 OLS_search(query=query, ontology=ontology)
 OLS_get_term(ontology=ontology, iri=iri)
 OLS_get_ancestors(ontology=ontology, iri=iri)
 """
 params = {"q": query, "rows": 50}
 if ontologies:
 params["ontology"] = ",".join(ontologies)
 if type_filter:
 params["type"] = type_filter

 resp = requests.get(f"{OLS_API}/search", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for doc in data.get("response", {}).get("docs", []):
 results.append({
 "obo_id": doc.get("obo_id", ""),
 "label": doc.get("label", ""),
 "ontology": doc.get("ontology_name", ""),
 "description": (doc.get("description") or [""])[0][:200],
 "iri": doc.get("iri", ""),
 "synonyms": doc.get("synonym", []),
 "has_children": doc.get("has_children", False),
 })

 df = pd.DataFrame(results)
 print(f"OLS search '{query}' "
 f"[{','.join(ontologies) if ontologies else 'all'}]: "
 f"{len(df)} terms")
 return df


def get_ols_term_hierarchy(ontology, term_id):
 """
 OLS for'sstructure (ancestors/descendants) retrieval。

 Parameters:
 ontology: str — ID (e.g., "hp", "go")
 term_id: str — OBO ID (e.g., "HP:0001250")
 """
 iri = f"http://purl.obolibrary.org/obo/{term_id.replace(':', '_')}"
 encoded_iri = requests.utils.quote(requests.utils.quote(iri, safe=""), safe="")

 # Ancestors
 anc_resp = requests.get(
 f"{OLS_API}/ontologies/{ontology}/terms/{encoded_iri}/ancestors"
 )

 # Descendants
 desc_resp = requests.get(
 f"{OLS_API}/ontologies/{ontology}/terms/{encoded_iri}/descendants"
 )

 hierarchy = {"ancestors": [], "descendants": []}

 if anc_resp.status_code == 200:
 for t in anc_resp.json.get("_embedded", {}).get("terms", []):
 hierarchy["ancestors"].append({
 "id": t.get("obo_id", ""),
 "label": t.get("label", ""),
 })

 if desc_resp.status_code == 200:
 for t in desc_resp.json.get("_embedded", {}).get("terms", []):
 hierarchy["descendants"].append({
 "id": t.get("obo_id", ""),
 "label": t.get("label", ""),
 })

 print(f"OLS hierarchy {term_id}: "
 f"{len(hierarchy['ancestors'])} ancestors, "
 f"{len(hierarchy['descendants'])} descendants")
 return hierarchy
```

## 3. Enrichr geneanalysis

```python
ENRICHR_API = "https://maayanlab.cloud/Enrichr"


def run_enrichr(gene_list, description="", gene_set_libraries=None):
 """
 Enrichr gene listanalysis。

 Parameters:
 gene_list: list — gene symbol list (e.g., ["TP53", "BRCA1", "EGFR"])
 description: str — analysis's
 gene_set_libraries: list — forgenelibrary

 ToolUniverse:
 Enrichr_submit_gene_list(genes=gene_list)
 Enrichr_get_enrichment(user_list_id=id, library=library)
 """
 if gene_set_libraries is None:
 gene_set_libraries = [
 "GO_Biological_Process_2023",
 "GO_Molecular_Function_2023",
 "KEGG_2021_Human",
 "Reactome_2022",
 "WikiPathway_2023_Human",
 "DisGeNET",
 ]

 # Submit gene list
 genes_str = "\n".join(gene_list)
 submit_resp = requests.post(
 f"{ENRICHR_API}/addList",
 files={"list": (None, genes_str), "description": (None, description)},
 )
 submit_resp.raise_for_status
 user_list_id = submit_resp.json.get("userListId")
 print(f"Enrichr: submitted {len(gene_list)} genes (ID={user_list_id})")

 # Get enrichment results per library
 all_results = {}
 for library in gene_set_libraries:
 enrich_resp = requests.get(
 f"{ENRICHR_API}/enrich",
 params={"userListId": user_list_id, "backgroundType": library},
 )
 enrich_resp.raise_for_status
 data = enrich_resp.json

 results = []
 for term_data in data.get(library, []):
 results.append({
 "rank": term_data[0],
 "term": term_data[1],
 "p_value": term_data[2],
 "z_score": term_data[3],
 "combined_score": term_data[4],
 "overlap_genes": term_data[5],
 "adjusted_p": term_data[6],
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("adjusted_p")
 all_results[library] = df
 sig_count = (df["adjusted_p"] < 0.05).sum if not df.empty else 0
 print(f" {library}: {sig_count} significant terms (FDR < 0.05)")

 return all_results
```

## 4. UMLS mapping

```python
UMLS_API = "https://uts-ws.nlm.nih.gov/rest"


def search_umls(query, api_key, search_type="words"):
 """
 UMLS search。

 Parameters:
 query: str — search term (disease、、)
 api_key: str — UMLS API key
 search_type: str — "words", "exact", "leftTruncation"

 ToolUniverse:
 UMLS_search(query=query, search_type=search_type)
 UMLS_get_concept(cui=cui)
 """
 params = {
 "string": query,
 "searchType": search_type,
 "apiKey": api_key,
 "pageSize": 25,
 }
 resp = requests.get(f"{UMLS_API}/search/current", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("result", {}).get("results", []):
 results.append({
 "cui": item.get("ui", ""),
 "name": item.get("name", ""),
 "root_source": item.get("rootSource", ""),
 "uri": item.get("uri", ""),
 })

 df = pd.DataFrame(results)
 print(f"UMLS search '{query}': {len(df)} concepts")
 return df


def get_umls_crosswalk(cui, api_key, target_source=None):
 """
 UMLS CUI from's forsystemmapping。

 Parameters:
 cui: str — UMLS CUI (e.g., "C0023264")
 api_key: str — UMLS API key
 target_source: str — forsystem (e.g., "SNOMEDCT_US", "ICD10CM", "MeSH")
 """
 params = {"apiKey": api_key, "pageSize": 100}
 if target_source:
 params["sabs"] = target_source

 resp = requests.get(f"{UMLS_API}/content/current/CUI/{cui}/atoms", params=params)
 resp.raise_for_status
 data = resp.json

 mappings = []
 for atom in data.get("result", []):
 mappings.append({
 "source": atom.get("rootSource", ""),
 "code": atom.get("sourceConcept", ""),
 "name": atom.get("name", ""),
 "term_type": atom.get("termType", ""),
 })

 df = pd.DataFrame(mappings)
 if target_source:
 df = df[df["source"] == target_source]

 print(f"UMLS crosswalk {cui}: {len(df)} mappings "
 f"({target_source or 'all sources'})")
 return df
```

---

## Available Tools

| ToolUniverse Category | Key Tools |
|---|---|
| `efo` | `EFO_search` |
| `ols` | `OLS_search`, `OLS_get_term`, `OLS_get_ancestors` |
| `enrichr` | `Enrichr_submit_gene_list`, `Enrichr_get_enrichment` |
| `umls` | `UMLS_search`, `UMLS_get_concept` |

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/efo_terms.csv` | EFO standardizationfor | → disease-research, gene-expression |
| `results/enrichr_results/` | generesults | → pathway-enrichment, multi-omics |
| `results/umls_mapping.json` | UMLS formapping | → clinical-decision-support, public-health-data |
| `results/ontology_hierarchy.json` | | → text-mining-nlp, knowledge-graph |

## Pipeline Integration

```
disease-research ──→ ontology-enrichment ──→ pathway-enrichment
 (GWAS/DisGeNET) (EFO/OLS/UMLS/Enrichr) (KEGG/Reactome/GO)
 │
 ├──→ biothings-idmapping (CUI→Gene→Protein)
 ├──→ public-health-data (UMLS→RxNorm)
 └──→ clinical-reporting (SNOMED/ICD mapping)
```
