---
name: scientific-gwas-catalog
description: |
 GWAS logskill。NHGRI-EBI GWAS Catalog REST API by/viagenome
 researchdatashapegenesearch。
 ToolUniverse integration: gwas。
tu_tools:
 - key: gwas
 name: GWAS Catalog
 description: GWAS shapegenesearch
---

# Scientific GWAS Catalog

NHGRI-EBI GWAS Catalog REST API utilizing GWAS data
analysisgenepipeline is provided。

## When to Use

- GWAS Catalog fromdisease/shape's is searchedand
- 's Pvalue is retrievedand
- gene's LD blockinformationanalysiswhen needed
- shape PheWAS-like analysis is performedand
- GWAS amount analysiswhen needed
- GWAS datafrom PRS is extractedand

---

## Quick Start

## 1. GWAS search

```python
import requests
import pandas as pd
import numpy as np

GWAS_BASE = "https://www.ebi.ac.uk/gwas/rest/api"


def gwas_search_associations(trait=None, gene=None, variant=None,
 p_upper=5e-8, limit=100):
 """
 GWAS Catalog — search。

 Parameters:
 trait: str — shape/disease EFO ID or name (example: "EFO_0001645")
 gene: str — gene name (example: "BRCA1")
 variant: str — rsID (example: "rs1234567")
 p_upper: float — Pvalue
 limit: int — maximum results
 """
 if trait:
 url = f"{GWAS_BASE}/efoTraits/{trait}/associations"
 elif gene:
 url = f"{GWAS_BASE}/associations/search/findByGene"
 elif variant:
 url = f"{GWAS_BASE}/singleNucleotidePolymorphisms/{variant}/associations"
 else:
 url = f"{GWAS_BASE}/associations"

 params = {"size": limit}
 if gene:
 params["geneName"] = gene

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 associations = data.get("_embedded", {}).get("associations", [])
 results = []
 for assoc in associations:
 p_value = assoc.get("pvalue", 1.0)
 if p_value and float(p_value) > p_upper:
 continue

 loci = assoc.get("loci", [{}])
 genes = []
 for locus in loci:
 for gene_info in locus.get("authorReportedGenes", []):
 genes.append(gene_info.get("geneName", ""))

 snps = []
 for snp_info in assoc.get("snps", []):
 snps.append(snp_info.get("rsId", ""))

 results.append({
 "association_id": assoc.get("associationId", ""),
 "p_value": float(p_value) if p_value else None,
 "p_value_mlog": assoc.get("pvalueMantissa", 0),
 "or_beta": assoc.get("orPerCopyNum", None),
 "beta_num": assoc.get("betaNum", None),
 "beta_direction": assoc.get("betaDirection", ""),
 "ci": assoc.get("range", ""),
 "risk_allele_freq": assoc.get("riskFrequency", ""),
 "snps": "; ".join(snps),
 "genes": "; ".join(genes),
 "trait": assoc.get("efoTraits", [{}])[0].get("trait", "")
 if assoc.get("efoTraits") else "",
 "study_accession": assoc.get("study", {}).get(
 "accessionId", ""),
 })

 df = pd.DataFrame(results)
 print(f"GWAS associations: {len(df)} results "
 f"(trait={trait}, gene={gene}, p<{p_upper})")
 return df.sort_values("p_value") if not df.empty else df
```

## 2. GWAS researchdatasearch

```python
def gwas_search_studies(query=None, efo_trait=None, limit=50):
 """
 GWAS Catalog — researchdatasearch。

 Parameters:
 query: str — search
 efo_trait: str — EFO shape ID
 limit: int — maximum results
 """
 if efo_trait:
 url = f"{GWAS_BASE}/efoTraits/{efo_trait}/studies"
 else:
 url = f"{GWAS_BASE}/studies/search/findByDiseaseTrait"

 params = {"size": limit}
 if query:
 params["diseaseTrait"] = query

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 studies = data.get("_embedded", {}).get("studies", [])
 results = []
 for s in studies:
 results.append({
 "accession": s.get("accessionId", ""),
 "title": s.get("title", ""),
 "pubmed_id": s.get("publicationInfo", {}).get(
 "pubmedId", ""),
 "author": s.get("publicationInfo", {}).get(
 "author", {}).get("fullname", ""),
 "journal": s.get("publicationInfo", {}).get(
 "publication", ""),
 "date": s.get("publicationInfo", {}).get(
 "publicationDate", ""),
 "initial_sample_size": s.get("initialSampleSize", ""),
 "replication_sample_size": s.get(
 "replicationSampleSize", ""),
 "ancestry": s.get("ancestries", []),
 })

 df = pd.DataFrame(results)
 print(f"GWAS studies: {len(df)} results")
 return df
```

## 3. GWAS shapesearchPheWAS

```python
def gwas_phewas(variant_rsid, p_threshold=5e-8):
 """
 GWAS Catalog — PheWAS (shapecross-cuttingsearch)。

 Parameters:
 variant_rsid: str — rsID (example: "rs7903146")
 p_threshold: float — Pvaluethreshold
 """
 url = (f"{GWAS_BASE}/singleNucleotidePolymorphisms/"
 f"{variant_rsid}/associations")
 resp = requests.get(url, params={"size": 500}, timeout=30)
 resp.raise_for_status
 data = resp.json

 associations = data.get("_embedded", {}).get("associations", [])
 results = []
 for assoc in associations:
 p_val = assoc.get("pvalue", 1.0)
 if p_val and float(p_val) > p_threshold:
 continue
 for trait in assoc.get("efoTraits", []):
 results.append({
 "variant": variant_rsid,
 "trait": trait.get("trait", ""),
 "efo_uri": trait.get("shortForm", ""),
 "p_value": float(p_val) if p_val else None,
 "or_beta": assoc.get("orPerCopyNum", None),
 "study": assoc.get("study", {}).get(
 "accessionId", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("p_value")
 print(f"PheWAS {variant_rsid}: {len(df)} trait associations")
 return df
```

## 4. GWAS integrationpipeline

```python
def gwas_catalog_pipeline(trait_query, output_dir="results"):
 """
 GWAS Catalog integrationpipeline。

 Parameters:
 trait_query: str — shape/disease
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) researchsearch
 studies = gwas_search_studies(query=trait_query)
 studies.to_csv(output_dir / "gwas_studies.csv", index=False)

 # 2) 
 assocs = gwas_search_associations(gene=None, trait=None)
 assocs.to_csv(output_dir / "gwas_associations.csv", index=False)

 # 3) 's PheWAS
 if not assocs.empty:
 top_snps = assocs["snps"].str.split("; ").explode.unique[:5]
 phewas_all = []
 for rsid in top_snps:
 if rsid.startswith("rs"):
 phewas = gwas_phewas(rsid)
 phewas_all.append(phewas)
 if phewas_all:
 phewas_df = pd.concat(phewas_all, ignore_index=True)
 phewas_df.to_csv(output_dir / "phewas.csv", index=False)

 print(f"GWAS pipeline: {output_dir}")
 return {"studies": studies, "associations": assocs}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `gwas` | GWAS Catalog | shaperesearchdatasearch |

## Pipeline Integration

```
disease-research → gwas-catalog → variant-interpretation
 (DisGeNET/OMIM) (GWAS Catalog) (ACMG/AMP)
 │ │ ↓
 population-genetics ──┘ variant-effect-prediction
 (Fst/PCA) │ (CADD/SpliceAI)
 ↓
 precision-oncology
 (significance)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gwas_studies.csv` | GWAS researchdata | → literature-search |
| `results/gwas_associations.csv` | | → variant-interpretation |
| `results/phewas.csv` | PheWAS results | → disease-research |
