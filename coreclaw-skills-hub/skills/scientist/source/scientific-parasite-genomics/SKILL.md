---
name: scientific-parasite-genomics
description: |
 skill。PlasmoDB/VectorBase/ToxoDB REST API
 by/viagenomesearchgeneinformationcomparison
 。 REST API integration (TU )。
tu_tools: []
---

# Scientific Parasite Genomics

VEuPathDB (PlasmoDB, VectorBase, ToxoDB, TriTrypDB)
's REST API utilizinganalysispipelineproviding
.

## When to Use

- genome (PlasmoDB) is searchedand
- 'sgenome (VectorBase) is searchedand
- genome (ToxoDB) is searchedand
- /genome (TriTrypDB) is searchedand
- 'swhen needed
- 's comparison is performedand

---

## Quick Start

## 1. VEuPathDB genesearch

```python
import requests
import pandas as pd
import numpy as np

VEUPATHDB_SITES = {
 "plasmo": "https://plasmodb.org/plasmo/service",
 "vector": "https://vectorbase.org/vectorbase/service",
 "toxo": "https://toxodb.org/toxo/service",
 "tritryp": "https://tritrypdb.org/tritrypdb/service",
}


def veupathdb_search_genes(organism, query, db="plasmo",
 limit=100):
 """
 VEuPathDB — genesearch。

 Parameters:
 organism: str — organism/species (example: "Plasmodium falciparum 3D7")
 query: str — searchkeyword (example: "kinase", "transporter")
 db: str — database ("plasmo", "vector", "toxo", "tritryp")
 limit: int — maximum results
 """
 base = VEUPATHDB_SITES.get(db, VEUPATHDB_SITES["plasmo"])
 url = f"{base}/record-types/gene/searches/GenesByTextSearch"

 payload = {
 "searchConfig": {
 "parameters": {
 "text_expression": query,
 "text_fields": "Gene ID,Gene Name or Symbol,"
 "Gene product",
 "organism": [organism],
 }
 },
 "reportConfig": {
 "attributes": ["primary_key", "gene_name",
 "gene_product", "gene_type",
 "chromosome", "start_min",
 "end_max", "strand"],
 "pagination": {"offset": 0, "numRecords": limit},
 },
 }
 headers = {"Content-Type": "application/json"}
 resp = requests.post(url, json=payload, headers=headers,
 timeout=60)
 resp.raise_for_status
 data = resp.json

 results = []
 for rec in data.get("records", []):
 attrs = rec.get("attributes", {})
 results.append({
 "gene_id": attrs.get("primary_key", ""),
 "gene_name": attrs.get("gene_name", ""),
 "product": attrs.get("gene_product", ""),
 "gene_type": attrs.get("gene_type", ""),
 "chromosome": attrs.get("chromosome", ""),
 "start": attrs.get("start_min", None),
 "end": attrs.get("end_max", None),
 "strand": attrs.get("strand", ""),
 })

 df = pd.DataFrame(results)
 print(f"VEuPathDB ({db}) genes: {len(df)} results "
 f"(organism={organism}, query={query})")
 return df
```

## 2. geneannotation

```python
def veupathdb_gene_annotation(gene_id, db="plasmo"):
 """
 VEuPathDB — geneannotationretrieval。

 Parameters:
 gene_id: str — gene ID (example: "PF3D7_1133400")
 db: str — database
 """
 base = VEUPATHDB_SITES.get(db, VEUPATHDB_SITES["plasmo"])
 url = f"{base}/record-types/gene/records/{gene_id}"

 params = {
 "attributes": "all",
 "tables": "GoTerms,InterPro,MetabolicPathways,"
 "PubMed,EcNumber",
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 attrs = data.get("attributes", {})
 tables = data.get("tables", {})

 annotation = {
 "gene_id": gene_id,
 "gene_name": attrs.get("gene_name", ""),
 "product": attrs.get("gene_product", ""),
 "molecular_weight": attrs.get("molecular_weight", ""),
 "isoelectric_point": attrs.get("isoelectric_point", ""),
 "signal_peptide": attrs.get("signal_peptide", ""),
 "transmembrane_domains": attrs.get("transmembrane_domains", ""),
 }

 # GO Term retrieval
 go_terms = []
 for go_rec in tables.get("GoTerms", []):
 go_terms.append({
 "go_id": go_rec.get("go_id", ""),
 "go_term": go_rec.get("go_term_name", ""),
 "ontology": go_rec.get("ontology", ""),
 "evidence": go_rec.get("evidence_code", ""),
 })
 annotation["go_terms"] = go_terms

 # InterPro 
 domains = []
 for d in tables.get("InterPro", []):
 domains.append({
 "interpro_id": d.get("interpro_primary_id", ""),
 "name": d.get("interpro_name", ""),
 "description": d.get("interpro_description", ""),
 })
 annotation["domains"] = domains

 print(f"VEuPathDB annotation: {gene_id}, "
 f"{len(go_terms)} GO terms, {len(domains)} domains")
 return annotation
```

## 3. 

```python
def parasite_drug_target_screen(organism, db="plasmo",
 essentiality_threshold=0.5):
 """
 genome — 。

 Parameters:
 organism: str — organism/species
 db: str — database
 essentiality_threshold: float — requiredthreshold
 """
 # search
 kinases = veupathdb_search_genes(organism, "kinase", db=db)
 # search
 proteases = veupathdb_search_genes(organism, "protease", db=db)
 # search
 transporters = veupathdb_search_genes(
 organism, "transporter", db=db)

 all_targets = pd.concat([kinases, proteases, transporters],
 ignore_index=True)
 all_targets = all_targets.drop_duplicates(subset=["gene_id"])

 # 
 all_targets["target_class"] = "unknown"
 all_targets.loc[
 all_targets["gene_id"].isin(kinases["gene_id"]),
 "target_class"] = "kinase"
 all_targets.loc[
 all_targets["gene_id"].isin(proteases["gene_id"]),
 "target_class"] = "protease"
 all_targets.loc[
 all_targets["gene_id"].isin(transporters["gene_id"]),
 "target_class"] = "transporter"

 print(f"Drug target screen: {len(all_targets)} candidates "
 f"(kinases={len(kinases)}, proteases={len(proteases)}, "
 f"transporters={len(transporters)})")
 return all_targets
```

## 4. integrationpipeline

```python
def parasite_genomics_pipeline(organism, query,
 db="plasmo",
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 organism: str — organism/species (example: "Plasmodium falciparum 3D7")
 query: str — search query
 db: str — database
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) genesearch
 genes = veupathdb_search_genes(organism, query, db=db)
 genes.to_csv(output_dir / "genes.csv", index=False)

 # 2) gene'sannotation
 annotations = []
 for gene_id in genes["gene_id"].head(10):
 try:
 ann = veupathdb_gene_annotation(gene_id, db=db)
 annotations.append(ann)
 except Exception:
 continue
 ann_df = pd.DataFrame([{
 k: v for k, v in a.items
 if not isinstance(v, list)
 } for a in annotations])
 ann_df.to_csv(output_dir / "annotations.csv", index=False)

 # 3) 
 targets = parasite_drug_target_screen(organism, db=db)
 targets.to_csv(output_dir / "drug_targets.csv", index=False)

 print(f"Parasite genomics pipeline: {output_dir}")
 return {
 "genes": genes,
 "annotations": annotations,
 "drug_targets": targets,
 }
```

---

## ToolUniverse Integration

 REST API for (VEuPathDB ToolUniverse )。

## Pipeline Integration

```
infectious-disease → parasite-genomics → phylogenetics
 (information) (genome) (phylogenyanalysis)
 │ │ ↓
 drug-discovery ─────────┘ comparative-genomics
 (search/exploration) │ (comparison)
 ↓
 pathway-enrichment
 (pathway analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/genes.csv` | genelist | → phylogenetics |
| `results/annotations.csv` | annotation | → pathway-enrichment |
| `results/drug_targets.csv` | | → drug-discovery |
