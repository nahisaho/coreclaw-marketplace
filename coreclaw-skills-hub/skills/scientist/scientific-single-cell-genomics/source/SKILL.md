---
name: scientific-single-cell-genomics
description: |
 Single-cell genomics skill. scRNA-seq analysis (Scanpy/Seurat), cell clustering, trajectory inference, cell type annotation, and gene regulatory network inference.
---

# Scientific Single-Cell Genomics

scRNA-seq / snRNA-seq data、QC → normalization → geneselection →
dimensionality reduction → clustering → DEG → cellannotation'sStandard Pipeline is provided。
CELLxGENE CensusHCA dataand 's integration also。

## When to Use

- scRNA-seq / snRNA-seq data's analysispipelinewhen needed
- cell's clustering andannotation is performedand
- 's expressiongenewhen needed
- RNA velocity by/viacellminanalysiswhen needed
- CellChat / CellPhoneDB by/viacell is performedand

---

## Quick Start

## 1. QCpreprocessingpipeline

```python
import scanpy as sc
import numpy as np
import pandas as pd

def sc_qc_preprocessing(adata, min_genes=200, max_genes=5000,
 max_pct_mito=20, min_cells=3):
 """
 scRNA-seq standard QC pipeline。

 QC metrics:
 - n_genes_by_counts: cellgenenumber/count
 - total_counts: cell UMI 
 - pct_counts_mt: generate（%）

 filtercriteria:
 - min_genes ≤ n_genes ≤ max_genes
 - pct_mito ≤ max_pct_mito
 - gene min_cells above/more's cellexpression
 """
 # gene'sannotation
 adata.var["mt"] = adata.var_names.str.startswith(("MT-", "mt-"))
 sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

 n_before = adata.n_obs
 # cellfilter
 sc.pp.filter_cells(adata, min_genes=min_genes)
 adata = adata[adata.obs["n_genes_by_counts"] <= max_genes].copy
 adata = adata[adata.obs["pct_counts_mt"] <= max_pct_mito].copy
 # genefilter
 sc.pp.filter_genes(adata, min_cells=min_cells)

 n_after = adata.n_obs
 print(f" QC: {n_before} → {n_after} cells ({n_before - n_after} removed)")

 return adata


def sc_normalize(adata, target_sum=1e4, n_top_genes=2000):
 """
 normalizationHVG selectionpipeline。

 procedure:
 1. Library size normalization (target_sum)
 2. Log1p transformation
 3. Highly Variable Gene (HVG) selection (Seurat v3 method)
 """
 adata.layers["counts"] = adata.X.copy
 sc.pp.normalize_total(adata, target_sum=target_sum)
 sc.pp.log1p(adata)
 adata.layers["log_normalized"] = adata.X.copy
 sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, flavor="seurat_v3",
 layer="counts")
 print(f" HVG: {adata.var['highly_variable'].sum} genes selected")
 return adata
```

## 2. dimensionality reductionclustering

```python
def sc_clustering(adata, n_pcs=50, n_neighbors=15, resolution=1.0,
 random_state=42):
 """
 PCA → graph → UMAP → Leiden clustering。

 Parameters:
 n_pcs: PCA minnumber/count
 n_neighbors: k-NN graph's number/count
 resolution: Leiden clustering's degree
 """
 sc.pp.scale(adata, max_value=10)
 sc.tl.pca(adata, n_comps=n_pcs, random_state=random_state)

 # Elbow plot for's variancerate
 variance_ratio = adata.uns["pca"]["variance_ratio"]
 cumvar = np.cumsum(variance_ratio)
 n_pcs_use = int(np.argmax(cumvar >= 0.9)) + 1
 n_pcs_use = max(n_pcs_use, 15)
 print(f" PCA: using {n_pcs_use} PCs (cumulative variance ≥ 90%)")

 sc.pp.neighbors(adata, n_pcs=n_pcs_use, n_neighbors=n_neighbors,
 random_state=random_state)
 sc.tl.umap(adata, random_state=random_state)
 sc.tl.leiden(adata, resolution=resolution, random_state=random_state)

 n_clusters = adata.obs["leiden"].nunique
 print(f" Leiden: {n_clusters} clusters (resolution={resolution})")
 return adata
```

## 3. expressiongene（DEG）

```python
def sc_deg_analysis(adata, groupby="leiden", method="wilcoxon",
 n_genes=200, min_logfc=0.25, max_pval=0.05):
 """
 's expressiongene.

 method:
 - "wilcoxon": Wilcoxon rank-sum test（recommended）
 - "t-test_overestim_var": Welch's t-test（high-speed）
 - "logreg": Logistic regression

 Returns:
 DataFrame with top DEGs per cluster
 """
 sc.tl.rank_genes_groups(adata, groupby=groupby, method=method, n_genes=n_genes)

 deg_results = []
 for cluster in adata.obs[groupby].unique:
 df = sc.get.rank_genes_groups_df(adata, group=cluster)
 df["cluster"] = cluster
 df_sig = df[(df["logfoldchanges"].abs >= min_logfc) &
 (df["pvals_adj"] < max_pval)]
 deg_results.append(df_sig)

 deg_df = pd.concat(deg_results, ignore_index=True)
 print(f" DEG: {len(deg_df)} significant genes across {adata.obs[groupby].nunique} clusters")
 return deg_df
```

## 4. cellannotation

```python
def annotate_celltypes_marker(adata, marker_dict, groupby="leiden",
 threshold=0.5):
 """
 gene's cellannotation。

 marker_dict example:
 {
 "T cells": ["CD3D", "CD3E", "CD8A", "CD4"],
 "B cells": ["CD19", "MS4A1", "CD79A"],
 "Monocytes": ["CD14", "LYZ", "FCGR3A"],
 "NK cells": ["NKG7", "GNLY", "KLRD1"],
 "Dendritic": ["FCER1A", "CST3", "CLEC10A"],
 }

 each'sgene expressioncalculation、 also highcorresponding
 cell.
 """
 sc.tl.score_genes(adata, gene_list=[], score_name="_dummy")

 scores = {}
 for cell_type, markers in marker_dict.items:
 valid_markers = [m for m in markers if m in adata.var_names]
 if valid_markers:
 score_name = f"score_{cell_type.replace(' ', '_')}"
 sc.tl.score_genes(adata, gene_list=valid_markers, score_name=score_name)
 scores[cell_type] = score_name

 # and 's cell
 cluster_annotations = {}
 for cluster in adata.obs[groupby].unique:
 mask = adata.obs[groupby] == cluster
 best_type = "Unknown"
 best_score = -np.inf
 for cell_type, score_col in scores.items:
 mean_score = adata.obs.loc[mask, score_col].mean
 if mean_score > best_score and mean_score > threshold:
 best_score = mean_score
 best_type = cell_type
 cluster_annotations[cluster] = best_type

 adata.obs["cell_type"] = adata.obs[groupby].map(cluster_annotations)
 print(f" Annotation: {len(set(cluster_annotations.values))} cell types assigned")
 return adata, cluster_annotations
```

## 5. RNA Velocity

```python
def rna_velocity_analysis(adata_loom_path, adata, basis="umap"):
 """
 scVelo by/via RNA velocity analysis。

 RNA velocity 、status（unspliced/spliced）'s ratefrom
 gene expression's timedirection is estimated。

 Modes:
 - stochastic: rate（recommended、high-speed）
 - dynamical: （degree、）
 """
 import scvelo as scv

 # preprocessing
 scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
 scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

 # Velocity 
 scv.tl.velocity(adata, mode="stochastic")
 scv.tl.velocity_graph(adata)

 # visualization
 scv.pl.velocity_embedding_stream(adata, basis=basis,
 save="figures/velocity_stream.png")

 # Latent time（time）
 scv.tl.latent_time(adata)
 print(f" Velocity: latent time range [{adata.obs['latent_time'].min:.3f}, "
 f"{adata.obs['latent_time'].max:.3f}]")

 return adata
```

## 6. cell

```python
def cell_communication_analysis(adata, groupby="cell_type",
 database="CellChatDB.human"):
 """
 CellChat by/vialigand-interactionanalysis。

 pipeline:
 1. L-R database's
 2. expression's ratecalculation
 3. network
 4. 
 """
 import cellchat

 cc = cellchat.CellChat(adata, groupby=groupby)
 cc.preprocess
 cc.identify_overexpressed_genes
 cc.identify_overexpressed_interactions

 cc.compute_communication_prob(database=database)
 cc.filter_communication(min_cells=10)
 cc.compute_communication_prob_pathway

 # networkvisualization
 cc.aggregate_net
 cc.net_analysis

 # resultsretrieval
 lr_pairs = cc.get_significant_interactions
 print(f" CellChat: {len(lr_pairs)} significant L-R interactions")

 return cc, lr_pairs
```

## 7. visualization

```python
def sc_visualization_panel(adata, deg_df=None, save_dir="figures"):
 """
 single-cellanalysisresults's visualization。

 generationfigure:
 1. QC violin plot (n_genes, total_counts, pct_mito)
 2. UMAP — leiden clusters
 3. UMAP — cell types
 4. DEG dot plot (top markers per cluster)
 5. Marker heatmap
 """
 import matplotlib.pyplot as plt
 import os
 os.makedirs(save_dir, exist_ok=True)

 # 1. QC violin
 sc.pl.violin(adata, ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
 jitter=0.4, multi_panel=True, save="_qc.png")

 # 2. UMAP — clusters
 sc.pl.umap(adata, color="leiden", legend_loc="on data",
 title="Leiden Clusters", save="_leiden.png")

 # 3. UMAP — cell types
 if "cell_type" in adata.obs.columns:
 sc.pl.umap(adata, color="cell_type",
 title="Cell Type Annotation", save="_celltypes.png")

 # 4. DEG dot plot
 if deg_df is not None:
 top_markers = deg_df.groupby("cluster").head(5)["names"].unique.tolist
 sc.pl.dotplot(adata, var_names=top_markers[:30],
 groupby="leiden", save="_markers.png")

 # 5. Stacked violin
 if deg_df is not None:
 top5 = deg_df.groupby("cluster").head(3)["names"].unique.tolist[:20]
 sc.pl.stacked_violin(adata, var_names=top5,
 groupby="leiden", save="_stacked.png")

 print(f" Figures saved to {save_dir}/")
```

## References

### Output Files

| File | Format |
|---|---|
| `results/sc_qc_summary.json` | JSON |
| `results/sc_deg_results.csv` | CSV |
| `results/sc_celltype_annotations.json` | JSON |
| `results/sc_velocity_summary.json` | JSON |
| `results/sc_cellchat_interactions.csv` | CSV |
| `figures/umap_leiden.png` | PNG |
| `figures/umap_celltypes.png` | PNG |
| `figures/velocity_stream.png` | PNG |
| `figures/deg_dotplot.png` | PNG |

## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    """Generic REST API data retrieval with error handling."""
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-bioinformatics](../scientific-bioinformatics/SKILL.md) | geneannotationpathway analysis |
| [scientific-multi-omics](../scientific-multi-omics/SKILL.md) | multi-omics integration |
| [scientific-network-analysis](../scientific-network-analysis/SKILL.md) | genenetwork |
| [scientific-deep-learning](../scientific-deep-learning/SKILL.md) | scVI / scGPT 'sdeep learning |
| [scientific-pca-tsne](../scientific-pca-tsne/SKILL.md) | dimensionality reductionmethod |
| [scientific-gene-expression-transcriptomics](../scientific-gene-expression-transcriptomics/SKILL.md) | bulk RNA-seq expression |
| [scientific-epigenomics-chromatin](../scientific-epigenomics-chromatin/SKILL.md) | epigenome-expressionintegration |

#### Dependencies

- scanpy, anndata, scvelo, cellchat, leidenalg, umap-learn
---

## Harness Optimization (v0.5.0)

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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
