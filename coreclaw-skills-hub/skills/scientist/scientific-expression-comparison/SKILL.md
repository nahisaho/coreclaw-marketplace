---
name: scientific-expression-comparison
description: |
 Gene expression comparison skill. Differential expression analysis (DESeq2/edgeR/limma), multi-condition comparison, volcano plots, and enrichment analysis pipelines.
---

# Scientific Expression Comparison

EBI Expression Atlas API as GTEx/HPA dataand integration
gene expressioncomparisonpipeline is provided。expressionexpression
experimentdatacross-cuttingsearchcomparison。

## When to Use

- EBI Expression Atlas gene's expression is investigatedand
- disease vs 'sexpressiondata is searchedand
- multiple'stissue/celltypeexpressioncomparison is performedand
- Expression Atlas 's experimentdata is retrievedand
- GTEx/HPA 's expressiondata and integrationcomparisonminwhen needed

---

## Quick Start

## 1. expressionsearch

```python
import requests
import pandas as pd

ATLAS_API = "https://www.ebi.ac.uk/gxa/json"
ATLAS_REST = "https://www.ebi.ac.uk/gxa"


def get_baseline_expression(gene, species="homo sapiens"):
 """
 Expression Atlas expressionfileretrieval。

 Parameters:
 gene: str — gene symbolor Ensembl ID
 species: str — organism/species

 ToolUniverse:
 ExpressionAtlas_get_baseline(gene=gene, species=species)
 """
 url = f"{ATLAS_REST}/json/baseline_expression"
 params = {"gene": gene, "species": species}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 profiles = data.get("profiles", {}).get("rows", [])
 rows = []
 for profile in profiles:
 gene_name = profile.get("name", gene)
 for exp in profile.get("expressions", []):
 rows.append({
 "gene": gene_name,
 "factor_value": exp.get("factorValue", ""),
 "expression_level": exp.get("value"),
 "unit": "TPM",
 })

 df = pd.DataFrame(rows)
 print(f"Baseline expression for {gene}: {len(df)} tissue/cell profiles")
 return df
```

## 2. expressionsearch

```python
def search_differential_expression(gene, condition=None, species="homo sapiens"):
 """
 expressionexperiment'ssearch。

 Parameters:
 gene: str — gene symbolor Ensembl ID
 condition: str — condition (example: "cancer", "inflammation")
 species: str — organism/species

 ToolUniverse:
 ExpressionAtlas_search_differential(
 gene=gene, condition=condition, species=species
 )
 """
 url = f"{ATLAS_REST}/json/search"
 params = {"geneQuery": gene, "species": species}
 if condition:
 params["conditionQuery"] = condition

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 results = data.get("results", [])
 rows = []
 for r in results:
 rows.append({
 "experiment_accession": r.get("experimentAccession"),
 "experiment_description": r.get("experimentDescription", "")[:200],
 "experiment_type": r.get("experimentType"),
 "species": r.get("species"),
 "contrast": r.get("contrastId", ""),
 "log2_fold_change": r.get("foldChange"),
 "p_value": r.get("pValue"),
 })

 df = pd.DataFrame(rows)
 print(f"Differential expression for {gene}: {len(df)} contrasts found")
 return df
```

## 3. experimentData Retrieval

```python
def get_experiment_details(accession):
 """
 Expression Atlas experimentdetailsretrieval。

 Parameters:
 accession: str — experiment ID (example: "E-MTAB-5214")

 ToolUniverse:
 ExpressionAtlas_get_experiment(accession=accession)
 """
 url = f"{ATLAS_REST}/json/experiments/{accession}"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 experiment = data.get("experiment", {})
 info = {
 "accession": experiment.get("accession"),
 "description": experiment.get("description"),
 "type": experiment.get("type"),
 "species": experiment.get("species", []),
 "pubmed_ids": experiment.get("pubmedIds", []),
 "n_assays": experiment.get("numberOfAssays"),
 "n_contrasts": experiment.get("numberOfContrasts"),
 "last_updated": experiment.get("lastUpdate"),
 }

 print(f"Experiment: {info['accession']} — {info['description'][:100]}")
 return info
```

## 4. experimentsearch

```python
def search_experiments(gene=None, condition=None, species="homo sapiens"):
 """
 Expression Atlas experimentsearch。

 Parameters:
 gene: str — gene
 condition: str — condition
 species: str — organism/species

 ToolUniverse:
 ExpressionAtlas_search_experiments(
 gene=gene, condition=condition, species=species
 )
 """
 url = f"{ATLAS_REST}/json/search"
 params = {"species": species}
 if gene:
 params["geneQuery"] = gene
 if condition:
 params["conditionQuery"] = condition

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 experiments = data.get("matchingExperiments", [])
 rows = []
 for e in experiments:
 rows.append({
 "accession": e.get("experimentAccession"),
 "description": e.get("experimentDescription", "")[:200],
 "type": e.get("experimentType"),
 "species": e.get("species"),
 "n_assays": e.get("numberOfAssays"),
 })

 df = pd.DataFrame(rows)
 print(f"Experiments found: {len(df)}")
 return df
```

## 5. tissuecross-cuttingexpressioncomparison

```python
def cross_tissue_comparison(genes, species="homo sapiens"):
 """
 multiplegene'stissuecross-cuttingexpressioncomparison。

 Parameters:
 genes: list — gene list
 species: str — organism/species

 Returns:
 DataFrame — genes × tissues expression
 """
 all_data = []
 for gene in genes:
 df = get_baseline_expression(gene, species)
 if not df.empty:
 df["gene_query"] = gene
 all_data.append(df)

 if not all_data:
 print("No expression data found")
 return pd.DataFrame

 combined = pd.concat(all_data, ignore_index=True)

 # table (genes × tissues)
 matrix = combined.pivot_table(
 index="gene",
 columns="factor_value",
 values="expression_level",
 aggfunc="mean",
 )

 print(f"Expression matrix: {matrix.shape[0]} genes × "
 f"{matrix.shape[1]} tissues/conditions")
 return matrix
```

## 6. expressionheatmap

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_expression_heatmap(matrix, title="Gene Expression Comparison",
 figsize=(14, 8), save_path=None):
 """
 expression'sheatmapdrawing/plotting。

 Parameters:
 matrix: DataFrame — cross_tissue_comparison 's output
 title: str — figuretitle
 figsize: tuple — figure
 save_path: str — save
 """
 log_matrix = np.log2(matrix.fillna(0) + 1)

 fig, ax = plt.subplots(figsize=figsize)
 sns.heatmap(
 log_matrix,
 cmap="viridis",
 xticklabels=True,
 yticklabels=True,
 ax=ax,
 )
 ax.set_title(title)
 ax.set_xlabel("Tissue / Condition")
 ax.set_ylabel("Gene")
 plt.tight_layout

 if save_path:
 fig.savefig(save_path, dpi=150, bbox_inches="tight")
 print(f"Saved: {save_path}")
 plt.show
```

---

## Pipeline Integration

```
gene-expression-transcriptomics → expression-comparison → multi-omics
 (GEO/GTEx/DESeq2) (Atlas expressioncomparison) (integrated analysis)
 │ │ ↓
human-protein-atlas ────────────┘ │ pathway-enrichment
 (HPA tissue/cancerexpression) ↓ (KEGG/GO)
 ontology-enrichment
 (EFO shapemapping)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/baseline_expression.csv` | expression | → gene-expression |
| `results/differential_expression.csv` | expression | → pathway-enrichment |
| `results/expression_matrix.csv` | expression | → multi-omics |
| `figures/expression_heatmap.png` | heatmap | → publication-figures |

## Available Tools (ToolUniverse SMCP)

| Tool Name | Usage |
|---------|------|
| `ExpressionAtlas_get_baseline` | expression |
| `ExpressionAtlas_search_differential` | expressionsearch |
| `ExpressionAtlas_search_experiments` | experimentsearch |
| `ExpressionAtlas_get_experiment` | experimentdetails |

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
