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

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
### Verification Loop

```
Phase 1: PLAN
  |-- Define eval criteria (above checklist)
  |-- Confirm input data availability and format
  |-- Select analysis methods with justification
  +-- Estimate resource requirements (time, memory, API calls)

Phase 2: EXECUTE
  |-- Run analysis pipeline step-by-step
  |-- Save intermediate results after each major step
  |-- Log execution time per step
  +-- Capture warnings/errors without stopping

Phase 3: VERIFY
  |-- Check all Pass Criteria (above)
  |-- Validate output file existence and non-empty
  |-- Cross-check numeric results for sanity (ranges, signs, units)
  |-- Verify figures are readable and correctly labeled
  +-- Run regression check: did existing outputs break?

Phase 4: RECOVER (on failure)
  |-- Identify failed phase and root cause
  |-- Isolate minimum reproducer
  |-- Apply fix and re-run only failed phase
  |-- Log fix as reusable pattern
  +-- If unrecoverable: document limitation and partial results

Phase 5: REPORT
  |-- Generate report.md with all sections
  |-- Embed all figures with captions
  |-- Save numeric results as JSON/CSV
  |-- List all generated files
  +-- Record execution metadata (duration, versions, seed)
```

### Quality Gates

| Gate | Check | Required |
|------|-------|----------|
| G1 | All figures saved to `figures/` (not `plt.show()`) | MUST |
| G2 | All figures embedded in `report.md` | MUST |
| G3 | Numeric results saved as JSON/CSV in `results/` | MUST |
| G4 | Report includes methods, results, discussion | MUST |
| G5 | All figure/table text is English-only | MUST |
| G6 | No hardcoded paths (use `Path` / config) | MUST |
| G7 | Random seed set and documented | MUST |
| G8 | Execution time logged | RECOMMENDED |
| G9 | Input validation performed | RECOMMENDED |
| G10 | Error messages are actionable | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | Data formatting, file I/O, unit conversion |
| Implementation | `standard` (sonnet-class) | Analysis code, pipeline execution, plotting |
| Reasoning | `premium` (opus-class) | Hypothesis generation, result interpretation, review |

### Sub-Agent Orchestration

When the task is complex, split into parallel sub-agents:

```
Orchestrator (this skill)
|-- Agent 1: Data preparation and validation
|-- Agent 2: Core analysis / computation
|-- Agent 3: Visualization and figure generation
+-- Agent 4: Report writing and quality check
```

Each sub-agent receives:
- Specific scope (what to do)
- Input specification (what data to use)
- Output specification (what files to produce)
- Quality gate subset (which gates to check)

### Token Optimization

- Load only the sub-skill needed for the current task
- Compact context after each major phase (discard intermediate logs)
- Use structured output (JSON) over prose for intermediate results
- Prefer code templates over natural language descriptions
- Cache expensive computations (API calls, model training)

### Error Recovery Protocol

```python
def execute_with_recovery(pipeline_steps, max_retries=2):
    results = {}
    for step in pipeline_steps:
        for attempt in range(max_retries + 1):
            try:
                results[step.name] = step.execute()
                break
            except Exception as e:
                if attempt < max_retries:
                    log(f"Step '{step.name}' failed (attempt {attempt+1}): {e}")
                    step.adjust_params()  # reduce batch size, increase timeout
                else:
                    log(f"Step '{step.name}' unrecoverable: {e}")
                    results[step.name] = {"status": "failed", "error": str(e)}
    return results
```
