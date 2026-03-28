---
name: scientific-gpu-singlecell
description: |
 GPU single-cellanalysisskill。
 rapids-singlecell / cuML / cuGraph by/via GPU 。
 large-scale (>1M cells) data's high-speedpreprocessingclustering
 dimensionality reduction。K-Dense: rapids-singlecell。
---

# Scientific GPU Single-Cell

rapids-singlecell / cuML / cuGraph utilizing GPU 
supportsingle-cellanalysispipeline is provided。100cell
's large-scaledataset's high-speed。

## When to Use

- large-scalesingle-celldata (>100k cells) 's high-speedpreprocessingwhen needed
- GPU clustering (Leiden/Louvain) is executedand
- GPU UMAP/t-SNE dimensionality reduction high-speedwhen needed
- CPU scanpy time for and
- multipleintegration GPU utilizingwhen needed
- (CPU vs GPU) comparison is performedand

---

## Quick Start

## 1. rapids-singlecell preprocessing

```python
import rapids_singlecell as rsc
import scanpy as sc
import anndata as ad
import cupy as cp
import numpy as np
import pandas as pd
import time
from pathlib import Path


def gpu_preprocessing(adata, min_genes=200, min_cells=3,
 n_top_genes=2000, target_sum=10000):
 """
 rapids-singlecell — GPU preprocessingpipeline。

 Parameters:
 adata: AnnData — input data
 min_genes: int — genenumber/count
 min_cells: int — cellnumber/count
 n_top_genes: int — number of HVGs
 target_sum: float — normalization
 """
 t0 = time.time

 # GPU data
 rsc.get.anndata_to_GPU(adata)

 # QC
 rsc.pp.calculate_qc_metrics(adata)
 rsc.pp.filter_cells(adata, min_genes=min_genes)
 rsc.pp.filter_genes(adata, min_cells=min_cells)

 # normalization
 rsc.pp.normalize_total(adata, target_sum=target_sum)
 rsc.pp.log1p(adata)

 # HVG selection
 rsc.pp.highly_variable_genes(
 adata,
 n_top_genes=n_top_genes,
 flavor="seurat_v3",
 )

 # 
 rsc.pp.scale(adata, max_value=10)

 elapsed = time.time - t0
 print(f"GPU preprocessing: {adata.n_obs} cells × {adata.n_vars} genes "
 f"({elapsed:.1f}s)")
 return adata
```

## 2. GPU PCA & graph

```python
def gpu_pca_neighbors(adata, n_comps=50, n_neighbors=15):
 """
 GPU PCA + graphconstruction。

 Parameters:
 adata: AnnData — preprocessingdata (GPU)
 n_comps: int — PCA minnumber/count
 n_neighbors: int — kNN number/count
 """
 t0 = time.time

 # GPU PCA
 rsc.pp.pca(adata, n_comps=n_comps)

 # GPU kNN
 rsc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=n_comps)

 elapsed = time.time - t0
 print(f"GPU PCA + kNN: {n_comps} PCs, k={n_neighbors} ({elapsed:.1f}s)")
 return adata
```

## 3. GPU clustering (Leiden/Louvain)

```python
def gpu_clustering(adata, method="leiden", resolution=1.0):
 """
 cuGraph — GPU Leiden/Louvain clustering。

 Parameters:
 adata: AnnData — graphdata
 method: str — "leiden" or "louvain"
 resolution: float — clusteringdegree
 """
 t0 = time.time

 if method == "leiden":
 rsc.tl.leiden(adata, resolution=resolution)
 else:
 rsc.tl.louvain(adata, resolution=resolution)

 n_clusters = adata.obs[method].nunique
 elapsed = time.time - t0

 print(f"GPU {method}: {n_clusters} clusters, "
 f"resolution={resolution} ({elapsed:.1f}s)")
 return adata
```

## 4. GPU UMAP / t-SNE

```python
def gpu_embedding(adata, method="umap", n_components=2, **kwargs):
 """
 GPU UMAP / t-SNE dimensionality reduction。

 Parameters:
 adata: AnnData — graphdata
 method: str — "umap" or "tsne"
 n_components: int — outputnumber/count
 """
 t0 = time.time

 if method == "umap":
 rsc.tl.umap(adata, n_components=n_components, **kwargs)
 else:
 rsc.tl.tsne(adata, n_pcs=n_components, **kwargs)

 elapsed = time.time - t0
 print(f"GPU {method.upper}: {n_components}D ({elapsed:.1f}s)")
 return adata
```

## 5. CPU vs GPU 

```python
def benchmark_cpu_vs_gpu(adata_path, n_top_genes=2000, n_comps=50):
 """
 CPU (scanpy) vs GPU (rapids-singlecell) 。

 Parameters:
 adata_path: str — h5ad file path
 n_top_genes: int — number of HVGs
 n_comps: int — PCA minnumber/count
 """
 results = {}

 # === CPU (scanpy) ===
 adata_cpu = sc.read_h5ad(adata_path)
 t0 = time.time
 sc.pp.normalize_total(adata_cpu, target_sum=1e4)
 sc.pp.log1p(adata_cpu)
 sc.pp.highly_variable_genes(adata_cpu, n_top_genes=n_top_genes)
 adata_cpu = adata_cpu[:, adata_cpu.var["highly_variable"]].copy
 sc.pp.scale(adata_cpu, max_value=10)
 sc.pp.pca(adata_cpu, n_comps=n_comps)
 sc.pp.neighbors(adata_cpu)
 sc.tl.leiden(adata_cpu)
 sc.tl.umap(adata_cpu)
 cpu_time = time.time - t0
 results["cpu_seconds"] = cpu_time
 results["cpu_clusters"] = adata_cpu.obs["leiden"].nunique

 # === GPU (rapids-singlecell) ===
 adata_gpu = sc.read_h5ad(adata_path)
 t0 = time.time
 rsc.get.anndata_to_GPU(adata_gpu)
 rsc.pp.normalize_total(adata_gpu, target_sum=1e4)
 rsc.pp.log1p(adata_gpu)
 rsc.pp.highly_variable_genes(adata_gpu, n_top_genes=n_top_genes,
 flavor="seurat_v3")
 adata_gpu = adata_gpu[:, adata_gpu.var["highly_variable"]].copy
 rsc.pp.scale(adata_gpu, max_value=10)
 rsc.pp.pca(adata_gpu, n_comps=n_comps)
 rsc.pp.neighbors(adata_gpu)
 rsc.tl.leiden(adata_gpu)
 rsc.tl.umap(adata_gpu)
 gpu_time = time.time - t0
 results["gpu_seconds"] = gpu_time
 results["gpu_clusters"] = adata_gpu.obs["leiden"].nunique

 results["speedup"] = cpu_time / gpu_time
 results["n_cells"] = adata_cpu.n_obs

 print(f"Benchmark ({results['n_cells']} cells):")
 print(f" CPU: {cpu_time:.1f}s ({results['cpu_clusters']} clusters)")
 print(f" GPU: {gpu_time:.1f}s ({results['gpu_clusters']} clusters)")
 print(f" Speedup: {results['speedup']:.1f}x")
 return results
```

## 6. GPU single-cellintegrationpipeline

```python
def gpu_singlecell_pipeline(input_files, output_dir="results",
 n_top_genes=3000, resolution=1.0):
 """
 large-scale GPU single-cellintegrationpipeline。

 Parameters:
 input_files: list[str] — h5ad file
 output_dir: str — output directory
 n_top_genes: int — number of HVGs
 resolution: float — Leiden resolution
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 t_total = time.time

 # 1) Loading databinding
 adatas = []
 for i, f in enumerate(input_files):
 a = sc.read_h5ad(f)
 a.obs["sample"] = f"sample_{i}"
 adatas.append(a)
 adata = ad.concat(adatas, join="inner")
 print(f"Combined: {adata.n_obs} cells from {len(input_files)} samples")

 # 2) GPU preprocessing
 adata = gpu_preprocessing(adata, n_top_genes=n_top_genes)

 # 3) GPU PCA + kNN
 adata = gpu_pca_neighbors(adata)

 # 4) GPU clustering
 adata = gpu_clustering(adata, resolution=resolution)

 # 5) GPU UMAP
 adata = gpu_embedding(adata)

 # 6) CPU marker 
 rsc.get.anndata_to_CPU(adata)
 sc.tl.rank_genes_groups(adata, groupby="leiden", method="wilcoxon")

 # save
 adata.write(output_dir / "gpu_singlecell.h5ad")

 # geneexport
 markers = sc.get.rank_genes_groups_df(adata, group=None)
 markers.to_csv(output_dir / "markers.csv", index=False)

 total_time = time.time - t_total
 print(f"GPU pipeline: {adata.n_obs} cells, "
 f"{adata.obs['leiden'].nunique} clusters ({total_time:.1f}s)")
 return adata
```

---

## Pipeline Integration

```
single-cell-genomics → gpu-singlecell → scvi-integration
 (scanpy standard) (GPU high-speed) (deep learningintegration)
 │ │ ↓
 batch-correction ─────────┘ cell-type-annotation
 (Harmony/scVI) │ (automatedannotation)
 ↓
 atlas-construction
 (large-scale)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/gpu_singlecell.h5ad` | GPU AnnData | → scvi-integration |
| `results/markers.csv` | gene | → cell-type-annotation |
| `results/benchmark.json` | CPU/GPU comparisonresults | → atlas-construction |

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
