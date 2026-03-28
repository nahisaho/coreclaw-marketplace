---
name: scientific-squidpy-advanced
description: |
 Squidpy advanced skill. Spatial omics analysis with Squidpy: neighborhood enrichment, spatial autocorrelation, ligand-receptor analysis, and image feature extraction.
tu_tools: []
kdense_ref: squidpy-advanced
tu_tools:
 - key: cellxgene
 name: CellxGene
 description: spatial transcriptomics datasearch
---

# Scientific Squidpy Advanced

Squidpy 's advancedanalysis utilizing
analysispipeline is provided。

## When to Use

- correlation (Moran's I, Geary's C) calculationwhen needed
- cell type's minwhen needed
- analysis is performedand
- ligand-receptor'smapping is performedand
- (tissueenvironment) when needed
- graphcalculationwhen needed

---

## Quick Start

## 1. correlationanalysis

```python
import squidpy as sq
import scanpy as sc
import pandas as pd
import numpy as np


def squidpy_spatial_autocorrelation(adata, genes=None,
 mode="moran", n_perms=100,
 n_jobs=4):
 """
 Squidpy — correlationanalysis (Moran's I / Geary's C)。

 Parameters:
 adata: AnnData — spatial transcriptomics data
 genes: list[str] — gene (None=HVG for)
 mode: str — "moran" or "geary"
 n_perms: int — testingtimesnumber/count
 n_jobs: int — jobnumber/count
 """
 # graphconstruction (constructioncase)
 if "spatial_connectivities" not in adata.obsp:
 sq.gr.spatial_neighbors(adata, coord_type="generic",
 n_neighs=6)

 if genes is None:
 sc.pp.highly_variable_genes(adata, n_top_genes=200)
 genes = adata.var_names[adata.var["highly_variable"]].tolist

 sq.gr.spatial_autocorr(adata, mode=mode, genes=genes,
 n_perms=n_perms, n_jobs=n_jobs)

 result_key = f"{mode}I" if mode == "moran" else f"{mode}C"
 result = adata.uns[result_key].copy
 sig = result[result["pval_norm"] < 0.05]

 print(f"Spatial autocorrelation ({mode}): "
 f"{len(sig)}/{len(result)} significant genes")
 return result.sort_values("pval_norm")
```

## 2. analysis

```python
def squidpy_co_occurrence(adata, cluster_key="cell_type",
 interval=50, n_splits=None):
 """
 Squidpy — cell typeanalysis。

 Parameters:
 adata: AnnData — spatial transcriptomics data
 cluster_key: str — cell typeannotationcolumn
 interval: int — number/count
 n_splits: int — minnumber/count (large-scaledatafor, None=automated)
 """
 sq.gr.co_occurrence(adata, cluster_key=cluster_key,
 interval=interval, n_splits=n_splits)

 co_occ = adata.uns[f"{cluster_key}_co_occurrence"]
 occ_scores = co_occ["occ"]
 interval_vals = co_occ["interval"]
 categories = adata.obs[cluster_key].cat.categories.tolist

 # 's
 near_idx = 0
 scores = occ_scores[near_idx]
 co_df = pd.DataFrame(scores, index=categories, columns=categories)

 # significant
 pairs = []
 for i, cat_i in enumerate(categories):
 for j, cat_j in enumerate(categories):
 if i < j:
 pairs.append({
 "cell_type_a": cat_i,
 "cell_type_b": cat_j,
 "co_occurrence_score": scores[i, j],
 })
 pairs_df = pd.DataFrame(pairs).sort_values(
 "co_occurrence_score", ascending=False)

 print(f"Co-occurrence: {len(categories)} cell types, "
 f"top pair: {pairs_df.iloc[0]['cell_type_a']} — "
 f"{pairs_df.iloc[0]['cell_type_b']}")
 return co_df, pairs_df
```

## 3. & 

```python
def squidpy_niche_identification(adata, cluster_key="cell_type",
 n_neighs=15, n_niches=5,
 seed=42):
 """
 Squidpy — 。

 Parameters:
 adata: AnnData — spatial transcriptomics data
 cluster_key: str — cell type column
 n_neighs: int — number/count
 n_niches: int — number/count
 seed: int — random seed
 """
 # 
 sq.gr.nhood_enrichment(adata, cluster_key=cluster_key)
 nhood = adata.uns[f"{cluster_key}_nhood_enrichment"]
 zscore_matrix = nhood["zscore"]
 categories = adata.obs[cluster_key].cat.categories.tolist
 nhood_df = pd.DataFrame(zscore_matrix, index=categories,
 columns=categories)

 # graph
 sq.gr.spatial_neighbors(adata, coord_type="generic",
 n_neighs=n_neighs)

 # file
 from sklearn.cluster import KMeans
 cell_types = adata.obs[cluster_key]
 type_dummies = pd.get_dummies(cell_types)

 # eachcell's
 conn = adata.obsp["spatial_connectivities"]
 nhood_composition = conn.dot(type_dummies.values)
 nhood_comp_df = pd.DataFrame(
 nhood_composition, columns=type_dummies.columns,
 index=adata.obs_names)

 # clustering
 km = KMeans(n_clusters=n_niches, random_state=seed, n_init=10)
 adata.obs["spatial_niche"] = km.fit_predict(
 nhood_comp_df.values).astype(str)

 niche_summary = adata.obs.groupby("spatial_niche")[cluster_key]\
.value_counts(normalize=True).unstack(fill_value=0)

 print(f"Niche identification: {n_niches} niches, "
 f"{len(categories)} cell types")
 return nhood_df, niche_summary
```

## 4. Squidpy advancedanalysisintegrationpipeline

```python
def squidpy_advanced_pipeline(adata, cluster_key="cell_type",
 output_dir="results"):
 """
 Squidpy advancedanalysisintegrationpipeline。

 Parameters:
 adata: AnnData — spatial transcriptomics data
 cluster_key: str — cell type column
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) correlation
 autocorr = squidpy_spatial_autocorrelation(adata)
 autocorr.to_csv(output_dir / "spatial_autocorrelation.csv")

 # 2) 
 co_df, pairs_df = squidpy_co_occurrence(adata,
 cluster_key=cluster_key)
 co_df.to_csv(output_dir / "co_occurrence_matrix.csv")
 pairs_df.to_csv(output_dir / "co_occurrence_pairs.csv",
 index=False)

 # 3) 
 nhood_df, niche_summary = squidpy_niche_identification(
 adata, cluster_key=cluster_key)
 nhood_df.to_csv(output_dir / "nhood_enrichment.csv")
 niche_summary.to_csv(output_dir / "niche_composition.csv")

 # 4) 
 sq.gr.centrality_scores(adata, cluster_key=cluster_key)
 centrality = adata.uns[f"{cluster_key}_centrality_scores"]
 centrality_df = pd.DataFrame(centrality)
 centrality_df.to_csv(output_dir / "centrality_scores.csv")

 adata.write(output_dir / "adata_spatial.h5ad")

 print(f"Squidpy advanced pipeline: {output_dir}")
 return {
 "autocorrelation": autocorr,
 "co_occurrence": co_df,
 "niches": niche_summary,
 "centrality": centrality_df,
 }
```

---

## K-Dense Integration

| K-Dense Key | Reference |
|-------------|---------|
| `squidpy-advanced` | advancedanalysismethod |

## Pipeline Integration

```
spatial-transcriptomics → squidpy-advanced → single-cell-genomics
 (Visium/MERFISH)  (scRNA-seq)
 │ │ ↓
 image-analysis ─────────────┘ cell-communication
 (H&E/IF ) │ (ligand-receptor)
 ↓
 multi-omics
 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/spatial_autocorrelation.csv` | correlation | → gene-expression |
| `results/co_occurrence_matrix.csv` | | → cell-communication |
| `results/niche_composition.csv` | | → single-cell-genomics |
| `results/centrality_scores.csv` | | → spatial-transcriptomics |
| `results/adata_spatial.h5ad` | AnnData (allresults) | → multi-omics |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `cellxgene` | CellxGene | spatial transcriptomics datasearch |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
