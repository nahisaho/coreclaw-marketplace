---
name: scientific-gtex-tissue-expression
description: |
 GTEx tissue expression skill. Tissue-specific gene expression queries from GTEx portal, eQTL analysis, cross-tissue comparison, and gene expression variation analysis.
tu_tools:
 - key: gtex_v2
 name: GTEx v2
 description: GTEx Portal REST API v2 tissueexpressioneQTL
---

# Scientific GTEx Tissue Expression

GTEx (Genotype-Tissue Expression) Portal REST API v2 utilizing
tissuegene expressionanalysiseQTL searchtissuecomparisonpipeline
is provided.

## When to Use

- gene's tissueexpression is investigatedand
- tissuein eQTL (expression levelshapegene) is searchedand
- multipletissuegene expression is comparedand
- TPM (Transcripts Per Million) expressiondata is retrievedand
- gene expression is evaluatedand
- tissue's geneexpression minwhen needed

---

## Quick Start

## 1. tissuegene expressionretrieval

```python
import requests
import pandas as pd

GTEX_BASE = "https://gtexportal.org/api/v2"


def gtex_gene_expression(gene_id, tissue=None):
 """
 GTEx — tissuegene expression (median TPM) retrieval。

 Parameters:
 gene_id: str — gene symbol or Ensembl ID
 (example: "BRCA1", "ENSG00000012048")
 tissue: str — tissue ID (None all tissues)
 (example: "Breast_Mammary_Tissue")
 """
 url = f"{GTEX_BASE}/expression/medianGeneExpression"
 params = {
 "gencodeId": gene_id,
 "datasetId": "gtex_v8",
 }
 if tissue:
 params["tissueSiteDetailId"] = tissue

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "gene_symbol": item.get("geneSymbol", ""),
 "gencode_id": item.get("gencodeId", ""),
 "tissue": item.get("tissueSiteDetailId", ""),
 "tissue_name": item.get("tissueSiteDetail", ""),
 "median_tpm": item.get("median", 0),
 "sample_count": item.get("numSamples", 0),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("median_tpm", ascending=False)

 print(f"GTEx expression: {gene_id} → "
 f"{len(df)} tissues")
 return df


def gtex_top_tissues(gene_id, top_n=10):
 """
 GTEx — expression leveltoptissue。

 Parameters:
 gene_id: str — gene symbol or Ensembl ID
 top_n: int — toptissuenumber/count
 """
 df = gtex_gene_expression(gene_id)
 top = df.head(top_n) if not df.empty else df
 print(f"GTEx top {top_n} tissues for {gene_id}:")
 for _, row in top.iterrows:
 print(f" {row['tissue_name']}: "
 f"{row['median_tpm']:.2f} TPM "
 f"(n={row['sample_count']})")
 return top
```

## 2. eQTL search

```python
def gtex_eqtl_lookup(gene_id, tissue, variant_id=None):
 """
 GTEx — eQTL 。

 Parameters:
 gene_id: str — gene symbol or Ensembl ID
 tissue: str — tissue ID
 (example: "Liver", "Whole_Blood")
 variant_id: str — ID (optional)
 (example: "rs12345")
 """
 url = f"{GTEX_BASE}/association/singleTissueEqtl"
 params = {
 "gencodeId": gene_id,
 "tissueSiteDetailId": tissue,
 "datasetId": "gtex_v8",
 }
 if variant_id:
 params["variantId"] = variant_id

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get("data", []):
 results.append({
 "gene_symbol": item.get("geneSymbol", ""),
 "variant_id": item.get("variantId", ""),
 "tissue": tissue,
 "pvalue": item.get("pValue"),
 "nes": item.get("nes"), # normalized effect size
 "maf": item.get("maf"),
 "ref": item.get("ref", ""),
 "alt": item.get("alt", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("pvalue")

 print(f"GTEx eQTL: {gene_id} in {tissue} → "
 f"{len(df)} associations")
 return df
```

## 3. tissuecomparison

```python
def gtex_multi_gene_comparison(gene_ids, tissues=None):
 """
 GTEx — multiplegenemultipletissue'sexpressioncomparison。

 Parameters:
 gene_ids: list[str] — gene list
 tissues: list[str] — tissue list (None all tissues)
 """
 all_data = []
 for gid in gene_ids:
 try:
 df = gtex_gene_expression(gid)
 if tissues:
 df = df[df["tissue"].isin(tissues)]
 all_data.append(df)
 except Exception as e:
 print(f" Warning: {gid} — {e}")
 continue

 if not all_data:
 return pd.DataFrame

 combined = pd.concat(all_data, ignore_index=True)

 # table: =tissue, =gene, value=TPM
 if not combined.empty:
 pivot = combined.pivot_table(
 index="tissue_name",
 columns="gene_symbol",
 values="median_tpm",
 aggfunc="first",
 )
 print(f"GTEx comparison: {len(gene_ids)} genes × "
 f"{len(pivot)} tissues")
 return pivot

 return combined
```

## 4. GTEx integrationpipeline

```python
def gtex_pipeline(gene_ids, tissues=None,
 output_dir="results"):
 """
 GTEx integrationpipeline。

 Parameters:
 gene_ids: list[str] — gene list
 tissues: list[str] — tissue list (None all tissues)
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) allgene's tissueexpression
 all_expr = []
 for gid in gene_ids:
 try:
 df = gtex_gene_expression(gid)
 df.to_csv(output_dir / f"expression_{gid}.csv",
 index=False)
 all_expr.append(df)
 except Exception:
 continue

 # 2) tissuecomparison
 pivot = gtex_multi_gene_comparison(gene_ids, tissues)
 if isinstance(pivot, pd.DataFrame) and not pivot.empty:
 pivot.to_csv(output_dir / "expression_matrix.csv")

 # 3) eQTL search (toptissue)
 eqtl_results = []
 for gid in gene_ids:
 if all_expr:
 top = all_expr[-1].head(3)
 for _, row in top.iterrows:
 try:
 eqtl = gtex_eqtl_lookup(gid,
 row["tissue"])
 eqtl_results.append(eqtl)
 except Exception:
 continue
 if eqtl_results:
 eqtl_combined = pd.concat(eqtl_results,
 ignore_index=True)
 eqtl_combined.to_csv(output_dir / "eqtl_results.csv",
 index=False)

 print(f"GTEx pipeline: {output_dir}")
 return {"expression": all_expr, "matrix": pivot}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| (direct) | GTEx Portal API v2 | REST API — TU integration |

## Pipeline Integration

```
gene-expression-transcriptomics → gtex-tissue-expression → variant-interpretation
 (DESeq2/edgeR minexpression) (tissue TPM + eQTL) (variant/mutationevaluation)
 │ │ ↓
 arrayexpress-expression ──────────┘ gwas-catalog
 (ArrayExpress data) │ (GWAS analysis)
 ↓
 disease-research
 (diseasegene)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/expression_*.csv` | genetissueexpression | → disease-research |
| `results/expression_matrix.csv` | genecomparison | → pathway-enrichment |
| `results/eqtl_results.csv` | eQTL | → variant-interpretation |

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
