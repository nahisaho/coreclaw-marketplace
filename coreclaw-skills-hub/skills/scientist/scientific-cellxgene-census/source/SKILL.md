---
name: scientific-cellxgene-census
description: |
 CellxGene Census skill. Single-cell RNA-seq data retrieval from CZ CELLxGENE, cell type annotation, cross-dataset comparison, and gene expression atlas queries.
tu_tools:
 - key: cellxgene_census
 name: CELLxGENE Census
 description: large-scale single-cell atlas data API
---

# Scientific CELLxGENE Census

CZ CELLxGENE Census API utilizinglarge-scalesingle-cell's
datasearchgene expressioncelldistributionanalysis
datasetcross-cuttingintegrationpipeline is provided。

## When to Use

- number/countcell'ssingle-cellfromtissue/disease's data is extractedand
- tissuecross-cuttingcelldistribution is comparedand
- gene's all expression is searchedand
- Census datasetdatabase filterwhen needed
- AnnData/Sparse aslarge-scaledatarateretrievalwhen needed

---

## Quick Start

## 1. Census datasearch

```python
import cellxgene_census
import pandas as pd


def census_datasets(organism="Homo sapiens",
 tissue=None, disease=None):
 """
 CELLxGENE Census — datasetdatasearch。

 Parameters:
 organism: str — organism/species
 tissue: str — tissue filter
 disease: str — diseasefilter
 """
 with cellxgene_census.open_soma as census:
 datasets = census["census_info"]["datasets"].read(
 ).concat.to_pandas

 if tissue:
 datasets = datasets[
 datasets["dataset_title"].str.contains(
 tissue, case=False, na=False)]
 if disease:
 datasets = datasets[
 datasets["dataset_title"].str.contains(
 disease, case=False, na=False)]

 print(f"Census datasets: {len(datasets)} matched")
 return datasets


def census_cell_metadata(organism="Homo sapiens",
 tissue=None,
 cell_type=None,
 max_cells=10000):
 """
 CELLxGENE Census — cellData Retrieval。

 Parameters:
 organism: str — organism/species
 tissue: str — tissue filter
 cell_type: str — cellfilter
 max_cells: int — maximum cell count
 """
 obs_filters = []
 if tissue:
 obs_filters.append(
 f"tissue_general == '{tissue}'")
 if cell_type:
 obs_filters.append(
 f"cell_type == '{cell_type}'")
 value_filter = " and ".join(obs_filters) \
 if obs_filters else None

 with cellxgene_census.open_soma as census:
 obs_df = cellxgene_census.get_obs(
 census, organism,
 value_filter=value_filter,
 column_names=[
 "cell_type", "tissue_general",
 "disease", "sex", "development_stage",
 "dataset_id", "assay"],
 )

 df = obs_df.head(max_cells)
 print(f"Census cells: {len(df)} retrieved "
 f"(filter: {value_filter})")
 return df
```

## 2. gene expression

```python
def census_gene_expression(organism="Homo sapiens",
 gene_symbols=None,
 tissue=None,
 max_cells=5000):
 """
 CELLxGENE Census — gene expressionData Retrieval。

 Parameters:
 organism: str — organism/species
 gene_symbols: list[str] — gene symbol list
 tissue: str — tissue filter
 max_cells: int — maximum cell count
 """
 obs_filter = (f"tissue_general == '{tissue}'"
 if tissue else None)
 var_filter = None
 if gene_symbols:
 genes_str = "', '".join(gene_symbols)
 var_filter = f"feature_name in ['{genes_str}']"

 with cellxgene_census.open_soma as census:
 adata = cellxgene_census.get_anndata(
 census, organism,
 obs_value_filter=obs_filter,
 var_value_filter=var_filter,
 obs_column_names=[
 "cell_type", "tissue_general",
 "disease"],
 )

 if max_cells and len(adata) > max_cells:
 import numpy as np
 idx = np.random.choice(
 len(adata), max_cells, replace=False)
 adata = adata[idx]

 print(f"Census expression: {adata.shape[0]} cells × "
 f"{adata.shape[1]} genes")
 return adata
```

## 3. celldistributionanalysis

```python
def celltype_distribution(organism="Homo sapiens",
 tissue=None):
 """
 tissuecelldistributionanalysis。

 Parameters:
 organism: str — organism/species
 tissue: str — tissue filter
 """
 obs_filter = (f"tissue_general == '{tissue}'"
 if tissue else None)

 with cellxgene_census.open_soma as census:
 obs_df = cellxgene_census.get_obs(
 census, organism,
 value_filter=obs_filter,
 column_names=["cell_type",
 "tissue_general"],
 )

 # cell
 ct_counts = obs_df["cell_type"].value_counts
 ct_df = pd.DataFrame({
 "cell_type": ct_counts.index,
 "count": ct_counts.values,
 "fraction": ct_counts.values / ct_counts.sum,
 })

 print(f"Cell types: {len(ct_df)} types, "
 f"total {ct_counts.sum} cells")
 return ct_df
```

## 4. Census integrationpipeline

```python
def census_pipeline(organism="Homo sapiens",
 tissue=None,
 gene_symbols=None,
 output_dir="results"):
 """
 CELLxGENE Census integrationpipeline。

 Parameters:
 organism: str — organism/species
 tissue: str — tissue
 gene_symbols: list[str] — gene
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) datasetdata
 datasets = census_datasets(organism, tissue)
 datasets.to_csv(output_dir / "census_datasets.csv",
 index=False)

 # 2) celldistribution
 ct_dist = celltype_distribution(organism, tissue)
 ct_dist.to_csv(
 output_dir / "celltype_distribution.csv",
 index=False)

 # 3) gene expression (specification)
 adata = None
 if gene_symbols:
 adata = census_gene_expression(
 organism, gene_symbols, tissue)
 adata.write_h5ad(
 output_dir / "census_expression.h5ad")

 print(f"Census pipeline → {output_dir}")
 return {
 "datasets": datasets,
 "celltype_dist": ct_dist,
 "adata": adata,
 }
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `cellxgene_census` | CELLxGENE Census | large-scalesingle-cell API |

## Pipeline Integration

```
human-cell-atlas → cellxgene-census → single-cell-genomics
 (HCA Portal) (Census large-scale) (Scanpy analysis)
 │ │ ↓
 spatial-multiomics ────┘ scvi-integration
 (integration) (scVI/scANVI)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/census_datasets.csv` | datasetlist | → human-cell-atlas |
| `results/celltype_distribution.csv` | celldistribution | → single-cell-genomics |
| `results/census_expression.h5ad` | expression (AnnData) | → scvi-integration |

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
