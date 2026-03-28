---
name: scientific-pharmgkb-pgx
description: |
 PharmGKB skill。PharmGKB REST API by/via
 annotationdruggeneamount
 analysis。ToolUniverse integration: pharmgkb。
tu_tools:
 - key: pharmgkb
 name: PharmGKB
 description: annotationdruggenePGx 
---

# Scientific PharmGKB PGx

PharmGKB (Pharmacogenomics Knowledgebase) REST API utilizing
annotationdruggeneinteractionamount
guideline searchpipeline is provided。

## When to Use

- drug and genevariant/mutation's is investigatedand
- annotation  is searchedand
- amount (CPIC/DPWG) is retrievedand
- and tabletype'ssupport is verifiedand
- drug's informationretrievalwhen needed
- 'sdrugselection is supportedand

---

## Quick Start

## 1. druggenesearch

```python
import requests
import pandas as pd

PGKB_BASE = "https://api.pharmgkb.org/v1/data"


def pharmgkb_search_drugs(query, limit=50):
 """
 PharmGKB — drugsearch。

 Parameters:
 query: str — drug (example: "warfarin", "clopidogrel")
 limit: int — maximum results
 """
 url = f"{PGKB_BASE}/chemical"
 params = {"name": query, "view": "max"}

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "pharmgkb_id": item.get("id", ""),
 "name": item.get("name", ""),
 "generic_names": "; ".join(
 item.get("genericNames", [])),
 "trade_names": "; ".join(
 item.get("tradeNames", [])[:5]),
 "type": item.get("type", ""),
 "cross_references": len(
 item.get("crossReferences", [])),
 })

 df = pd.DataFrame(results)
 print(f"PharmGKB drugs: {len(df)} results "
 f"(query='{query}')")
 return df


def pharmgkb_search_genes(query, limit=50):
 """
 PharmGKB — genesearch。

 Parameters:
 query: str — gene symbol (example: "CYP2D6")
 limit: int — maximum results
 """
 url = f"{PGKB_BASE}/gene"
 params = {"symbol": query, "view": "max"}

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "pharmgkb_id": item.get("id", ""),
 "symbol": item.get("symbol", ""),
 "name": item.get("name", ""),
 "chromosome": item.get("chromosomeFormatted", ""),
 "cpic_gene": item.get("cpicGene", False),
 "has_prescribing_info": item.get(
 "hasPrescribingInfo", False),
 })

 df = pd.DataFrame(results)
 print(f"PharmGKB genes: {len(df)} results "
 f"(query='{query}')")
 return df
```

## 2. annotationretrieval

```python
def pharmgkb_clinical_annotations(gene_or_drug,
 search_type="gene"):
 """
 PharmGKB — annotationsearch。

 Parameters:
 gene_or_drug: str — gene symbol or drug
 search_type: str — "gene" or "drug"
 """
 url = f"{PGKB_BASE}/clinicalAnnotation"
 params = {"view": "max"}

 if search_type == "gene":
 # gene search
 gene_url = f"{PGKB_BASE}/gene"
 g_resp = requests.get(gene_url,
 params={"symbol": gene_or_drug},
 timeout=30)
 g_resp.raise_for_status
 genes = g_resp.json.get("data", [])
 if genes:
 params["relatedGenes.id"] = genes[0].get("id", "")
 else:
 # drug search
 drug_url = f"{PGKB_BASE}/chemical"
 d_resp = requests.get(drug_url,
 params={"name": gene_or_drug},
 timeout=30)
 d_resp.raise_for_status
 drugs = d_resp.json.get("data", [])
 if drugs:
 params["relatedChemicals.id"] = drugs[0].get("id", "")

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 genes = [g.get("symbol", "")
 for g in item.get("relatedGenes", [])]
 drugs = [c.get("name", "")
 for c in item.get("relatedChemicals", [])]
 results.append({
 "annotation_id": item.get("id", ""),
 "level": item.get("level", ""),
 "score": item.get("score", ""),
 "genes": "; ".join(genes),
 "drugs": "; ".join(drugs),
 "phenotype_category": item.get(
 "phenotypeCategory", ""),
 "sentences": (item.get("textHtml") or "")[:300],
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("level")

 print(f"PharmGKB annotations: {len(df)} "
 f"({search_type}={gene_or_drug})")
 return df
```

## 3. amountretrieval

```python
def pharmgkb_dosing_guidelines(drug_name=None, gene=None):
 """
 PharmGKB — amount (CPIC/DPWG) search。

 Parameters:
 drug_name: str — drug
 gene: str — gene symbol
 """
 url = f"{PGKB_BASE}/guideline"
 params = {"view": "max"}

 if drug_name:
 params["relatedChemicals.name"] = drug_name
 if gene:
 params["relatedGenes.symbol"] = gene

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 genes = [g.get("symbol", "")
 for g in item.get("relatedGenes", [])]
 drugs = [c.get("name", "")
 for c in item.get("relatedChemicals", [])]
 results.append({
 "guideline_id": item.get("id", ""),
 "name": item.get("name", ""),
 "source": item.get("source", ""),
 "genes": "; ".join(genes),
 "drugs": "; ".join(drugs),
 "recommendation": (item.get("textHtml") or "")[:500],
 })

 df = pd.DataFrame(results)
 print(f"PharmGKB guidelines: {len(df)} "
 f"(drug={drug_name}, gene={gene})")
 return df
```

## 4. PharmGKB integrationpipeline

```python
def pharmgkb_pipeline(drug_name, genes=None,
 output_dir="results"):
 """
 PharmGKB integrationpipeline。

 Parameters:
 drug_name: str — drug
 genes: list[str] — gene list
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) drugsearch
 drugs = pharmgkb_search_drugs(drug_name)
 drugs.to_csv(output_dir / "drugs.csv", index=False)

 # 2) drug'sannotation
 annotations = pharmgkb_clinical_annotations(
 drug_name, search_type="drug")
 annotations.to_csv(output_dir / "annotations.csv",
 index=False)

 # 3) amount
 guidelines = pharmgkb_dosing_guidelines(
 drug_name=drug_name)
 guidelines.to_csv(output_dir / "guidelines.csv",
 index=False)

 # 4) geneanalysis
 if genes:
 gene_results = []
 for g in genes:
 try:
 g_ann = pharmgkb_clinical_annotations(
 g, search_type="gene")
 g_ann["query_gene"] = g
 gene_results.append(g_ann)
 except Exception:
 continue
 if gene_results:
 gene_df = pd.concat(gene_results,
 ignore_index=True)
 gene_df.to_csv(
 output_dir / "gene_annotations.csv",
 index=False)

 print(f"PharmGKB pipeline: {output_dir}")
 return {
 "drugs": drugs,
 "annotations": annotations,
 "guidelines": guidelines,
 }
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `pharmgkb` | PharmGKB | annotationdruggenePGx |

## Pipeline Integration

```
pharmacogenomics → pharmgkb-pgx → clinical-decision-support
 (PGx analysisall) (PharmGKB API) (clinical decision support)
 │ │ ↓
 drug-discovery ──────┘ precision-oncology
 (drug) │ (tumor)
 ↓
 variant-interpretation
 (variant/mutation)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/drugs.csv` | druginformation | → drug-discovery |
| `results/annotations.csv` | annotation | → variant-interpretation |
| `results/guidelines.csv` | amount | → clinical-decision-support |
| `results/gene_annotations.csv` | geneannotation | → pharmacogenomics |
