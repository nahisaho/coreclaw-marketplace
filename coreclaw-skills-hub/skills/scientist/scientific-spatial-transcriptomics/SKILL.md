---
name: scientific-spatial-transcriptomics
description: |
 Spatial transcriptomics skill. Visium/MERFISH/Slide-seq data analysis, spatial gene expression mapping, spatial clustering, and tissue region deconvolution.
---

# Scientific Spatial Transcriptomics

（10x Visium, MERFISH, Slide-seq, STARmap ） 
retrievaldata'sgene expressionanalysispipeline is provided。
deconvolutionligand-expressionhandles。

## When to Use

- Visium / MERFISH 'sspatial transcriptomics data's analysiswhen needed
- gene（SVG: Spatially Variable Genes）when needed
- tissue's automatedwhen needed
- 's celltype deconvolution is performedand
- ligand-interaction is evaluatedand

---

## Quick Start

## 1. datapreprocessing

```python
import scanpy as sc
import squidpy as sq
import numpy as np
import pandas as pd

def spatial_preprocessing(adata, min_counts=500, min_genes=200,
 max_pct_mito=25, n_top_genes=3000):
 """
 preprocessingpipeline。

 procedure:
 1. QC metricscalculation
 2. /cellfilter
 3. normalization + log1p
 4. HVG selection
 5. graphconstruction
 """
 # gene
 adata.var["mt"] = adata.var_names.str.startswith(("MT-", "mt-"))
 sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

 n_before = adata.n_obs
 sc.pp.filter_cells(adata, min_counts=min_counts)
 sc.pp.filter_cells(adata, min_genes=min_genes)
 adata = adata[adata.obs["pct_counts_mt"] <= max_pct_mito].copy
 sc.pp.filter_genes(adata, min_cells=10)
 print(f" QC: {n_before} → {adata.n_obs} spots")

 # normalization
 adata.layers["counts"] = adata.X.copy
 sc.pp.normalize_total(adata, target_sum=1e4)
 sc.pp.log1p(adata)
 sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, flavor="seurat_v3",
 layer="counts")

 # graph
 sq.gr.spatial_neighbors(adata, coord_type="grid", n_neighs=6)
 print(f" Spatial neighbors: {adata.obsp['spatial_connectivities'].nnz} edges")

 return adata
```

## 2. gene（SVG）

```python
def spatially_variable_genes(adata, method="moran", n_perms=100,
 fdr_threshold=0.05):
 """
 gene.

 method:
 - "moran": Moran's I correlationamount
 I = (N / W) * Σᵢ Σⱼ wᵢⱼ (xᵢ - x̄)(xⱼ - x̄) / Σᵢ (xᵢ - x̄)²
 - "sepal": SEPAL（）

 Moran's I:
 - I ≈ 1: 'scorrelation（valueclustering）
 - I ≈ 0: distribution
 - I ≈ -1: 'scorrelation（）
 """
 if method == "moran":
 sq.gr.spatial_autocorr(adata, mode="moran", n_perms=n_perms, n_jobs=-1)
 svg_df = adata.uns["moranI"].copy
 svg_df["significant"] = svg_df["pval_norm_fdr_bh"] < fdr_threshold
 svg_df = svg_df.sort_values("I", ascending=False)
 elif method == "sepal":
 sq.gr.spatial_autocorr(adata, mode="geary", n_perms=n_perms, n_jobs=-1)
 svg_df = adata.uns["gearyC"].copy
 svg_df["significant"] = svg_df["pval_norm_fdr_bh"] < fdr_threshold

 n_sig = svg_df["significant"].sum
 print(f" SVG ({method}): {n_sig} significant spatially variable genes")
 return svg_df
```

## 3. 

```python
def spatial_domain_detection(adata, n_domains=7, method="leiden", resolution=0.8):
 """
 （tissue）automated.

 method:
 - "leiden": graph Leiden clustering
 - "bayesspace": BayesSpace（Bayesian、Visium ）

 clustering than、gene expressionalso
 loop.
 """
 sc.pp.scale(adata, max_value=10)
 sc.tl.pca(adata, n_comps=30)

 if method == "leiden":
 # graphuse
 sc.tl.leiden(adata, resolution=resolution, adjacency=adata.obsp["spatial_connectivities"])
 adata.obs["spatial_domain"] = adata.obs["leiden"]
 elif method == "bayesspace":
 from bayesspace import BayesSpace
 bs = BayesSpace(adata, n_clusters=n_domains)
 bs.fit
 adata.obs["spatial_domain"] = bs.labels_.astype(str)

 n_domains_found = adata.obs["spatial_domain"].nunique
 print(f" Domains: {n_domains_found} spatial domains detected ({method})")
 return adata
```

## 4. Cell-type Deconvolution

```python
def spatial_deconvolution(adata_spatial, adata_sc, cell_type_col="cell_type",
 method="cell2location"):
 """
 's celltype scRNA-seq referencedatafrom.

 method:
 - "cell2location": Bayesian （recommended、high-accuracy）
 - "rctd": RCTD（ deconvolution）

 cell2location :
 y_s ~ NB(μ_s, α)
 μ_s = Σ_f w_sf * g_f
 w_sf: s incelltype f 's amount
 g_f: celltype f 's gene expression
 """
 import cell2location

 # 's
 cell2location.models.RegressionModel.setup_anndata(adata_sc, labels_key=cell_type_col)
 ref_model = cell2location.models.RegressionModel(adata_sc)
 ref_model.train(max_epochs=250)
 inf_aver = ref_model.export_posterior(adata_sc)

 # Spatial mapping
 cell2location.models.Cell2location.setup_anndata(adata_spatial)
 mod = cell2location.models.Cell2location(adata_spatial,
 cell_state_df=inf_aver)
 mod.train(max_epochs=30000)

 adata_spatial = mod.export_posterior(adata_spatial)
 print(f" Deconvolution: {len(inf_aver.columns)} cell types mapped to "
 f"{adata_spatial.n_obs} spots")
 return adata_spatial
```

## 5. ligand-analysis

```python
def spatial_ligand_receptor(adata, cluster_key="spatial_domain",
 n_perms=1000, fdr_threshold=0.01):
 """
 'sligand-interactiontesting.

 Squidpy 's permutation test:
 each L-R about、 's expression
 and comparisonsignificant hightesting.
 """
 sq.gr.ligrec(adata, n_perms=n_perms, cluster_key=cluster_key,
 copy=False, use_raw=False, transmitter_params={"categories": "ligand"},
 receiver_params={"categories": "receptor"})

 lr_results = adata.uns["ligrec"]
 pvals = lr_results["pvalues"]
 sig_count = (pvals < fdr_threshold).sum.sum
 print(f" L-R analysis: {sig_count} significant spatial interactions")
 return lr_results
```

## 6. visualization

```python
def spatial_visualization_panel(adata, svg_df=None, save_dir="figures"):
 """
 visualization。

 generationfigure:
 1. gene expression（top SVG）
 2. 
 3. Deconvolution results
 4. Spatial autocorrelation heatmap
 """
 import matplotlib.pyplot as plt
 import os
 os.makedirs(save_dir, exist_ok=True)

 # 1. 'sgene expression
 if svg_df is not None:
 top_svgs = svg_df[svg_df["significant"]].head(6).index.tolist
 sq.pl.spatial_scatter(adata, color=top_svgs, ncols=3,
 save=f"{save_dir}/spatial_svgs.png")

 # 2. 
 if "spatial_domain" in adata.obs.columns:
 sq.pl.spatial_scatter(adata, color="spatial_domain",
 save=f"{save_dir}/spatial_domains.png")

 # 3. Moran's I distribution
 if svg_df is not None:
 fig, ax = plt.subplots(figsize=(8, 4))
 ax.hist(svg_df["I"], bins=50, color="steelblue", alpha=0.7)
 ax.axvline(x=0, color="red", linestyle="--", label="Random (I=0)")
 ax.set_xlabel("Moran's I")
 ax.set_ylabel("Count")
 ax.set_title("Distribution of Spatial Autocorrelation")
 ax.legend
 plt.tight_layout
 plt.savefig(f"{save_dir}/morans_i_dist.png", dpi=300, bbox_inches="tight")
 plt.close

 print(f" Figures saved to {save_dir}/")
```

## References

### Output Files

| File | Format |
|---|---|
| `results/svg_results.csv` | CSV |
| `results/spatial_domains.json` | JSON |
| `results/deconvolution_proportions.csv` | CSV |
| `results/ligrec_results.json` | JSON |
| `figures/spatial_svgs.png` | PNG |
| `figures/spatial_domains.png` | PNG |
| `figures/morans_i_dist.png` | PNG |

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
| [scientific-single-cell-genomics](../scientific-single-cell-genomics/SKILL.md) | scRNA-seq referencedatadeconvolution |
| [scientific-bioinformatics](../scientific-bioinformatics/SKILL.md) | geneannotationpathway |
| [scientific-image-analysis](../scientific-image-analysis/SKILL.md) | tissue |
| [scientific-network-analysis](../scientific-network-analysis/SKILL.md) | networkanalysis |
| [scientific-bayesian-statistics](../scientific-bayesian-statistics/SKILL.md) | BayesSpace |

#### Dependencies

- squidpy, scanpy, anndata, cell2location, bayesspace, SpatialDE
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
