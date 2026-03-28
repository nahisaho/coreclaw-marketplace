---
name: scientific-scatac-signac
description: |
 scATAC-seq analysisskill (Signac/SnapATAC2/episcanpy)。
 peakanalysisGene Activity 
 RNA+ATAC integration (WNN)。K-Dense: signac。
---

# Scientific scATAC-seq / Signac

Signac / SnapATAC2 / episcanpy utilizing scATAC-seq (single-cell
ATAC-seq) analysispipeline is provided。chromatinaccessibility
analysis、、integration。

## When to Use

- scATAC-seq data's preprocessing and peak is performedand
- factor'sanalysis is executedand
- Gene Activity scATAC expressionwhen needed
- scRNA-seq + scATAC-seq 'sintegration is performedand
- chromatinaccessibility's celltypewhen needed
- epigenome (histone/DNAmethylation) and chromatinintegrationwhen needed

---

## Quick Start

## 1. scATAC-seq preprocessing (SnapATAC2)

```python
import snapatac2 as snap
import anndata as ad
import numpy as np
import pandas as pd
from pathlib import Path


def scatac_preprocessing(fragment_file, genome="hg38",
 min_tsse=5, min_fragments=1000):
 """
 SnapATAC2 — scATAC-seq preprocessingpipeline。

 Parameters:
 fragment_file: str — fragments.tsv.gz 
 genome: str — reference genome ("hg38", "mm10")
 min_tsse: float — TSS enrichment 
 min_fragments: int — number/count
 """
 # fileload
 adata = snap.pp.import_data(
 fragment_file,
 chrom_sizes=snap.genome(genome),
 sorted_by_barcode=False,
 )

 # QC metrics
 snap.metrics.tsse(adata, snap.genome(genome))
 snap.metrics.frag_size_distr(adata)

 # filter
 snap.pp.filter_cells(
 adata,
 min_counts=min_fragments,
 min_tsse=min_tsse,
 )

 print(f"scATAC preprocessing: {adata.n_obs} cells, "
 f"TSS enrichment ≥ {min_tsse}")
 return adata
```

## 2. peak & Tile Matrix

```python
def scatac_peak_calling(adata, genome="hg38", peak_method="macs2",
 n_features=50000):
 """
 scATAC-seq peak & accessibility。

 Parameters:
 adata: AnnData — preprocessing scATAC data
 genome: str — reference genome
 peak_method: str — "macs2" or "tile"
 n_features: int — feature selection topnumber/count
 """
 if peak_method == "tile":
 # Tile matrix (500bp bins)
 snap.pp.add_tile_matrix(adata, bin_size=500)
 else:
 # MACS2 peak calling 
 snap.pp.make_peak_matrix(adata)

 # Feature selection
 snap.pp.select_features(adata, n_features=n_features)

 # dimensionality reduction
 snap.tl.spectral(adata)
 snap.tl.umap(adata)

 # clustering
 snap.pp.knn(adata)
 snap.tl.leiden(adata)

 n_clusters = adata.obs["leiden"].nunique
 print(f"Peak calling ({peak_method}): {n_clusters} clusters, "
 f"{n_features} features")
 return adata
```

## 3. (chromVAR)

```python
def motif_enrichment(adata, genome="hg38", motif_db="JASPAR2022"):
 """
 chromVAR analysis。

 Parameters:
 adata: AnnData — peak scATAC data
 genome: str — reference genome
 motif_db: str — database
 """
 # 
 snap.tl.motif_enrichment(
 adata,
 motifs=motif_db,
 genome=genome,
 )

 # min
 cluster_motifs = {}
 for cluster in adata.obs["leiden"].unique:
 mask = adata.obs["leiden"] == cluster
 # chromVAR deviation retrieval
 if "chromvar" in adata.obsm:
 deviations = adata.obsm["chromvar"][mask].mean(axis=0)
 top_idx = np.argsort(deviations)[-10:]
 top_motifs = [adata.uns["motif_names"][i] for i in top_idx]
 cluster_motifs[cluster] = top_motifs

 results = []
 for cluster, motifs in cluster_motifs.items:
 for rank, motif in enumerate(motifs, 1):
 results.append({
 "cluster": cluster,
 "rank": rank,
 "motif": motif,
 })

 df = pd.DataFrame(results)
 print(f"Motif enrichment: {len(cluster_motifs)} clusters, "
 f"{len(df)} motif-cluster pairs")
 return df
```

## 4. Gene Activity 

```python
def gene_activity_score(adata, genome="hg38", upstream=2000, body=True):
 """
 Gene Activity calculation — ATAC → expression level。

 Parameters:
 adata: AnnData — scATAC data
 genome: str — reference genome
 upstream: int — promoter (bp)
 body: bool — genepapersincluding
 """
 snap.pp.make_gene_matrix(
 adata,
 gene_anno=snap.genome(genome),
 upstream=upstream,
 include_body=body,
 )

 # Gene Activity.layers save
 if hasattr(adata, "uns") and "gene_activity" in adata.uns:
 gene_act = adata.uns["gene_activity"]
 else:
 gene_act = adata.X # Gene matrix mode

 # normalization
 gene_act_norm = gene_act / gene_act.sum(axis=1, keepdims=True) * 10000
 gene_act_log = np.log1p(gene_act_norm)

 print(f"Gene activity: {gene_act_log.shape[1]} genes, "
 f"{gene_act_log.shape[0]} cells")
 return gene_act_log
```

## 5. RNA + ATAC integration (WNN)

```python
import scanpy as sc


def multimodal_wnn(adata_atac, adata_rna, n_neighbors=20):
 """
 Weighted Nearest Neighbor (WNN) — RNA + ATAC integration。

 Parameters:
 adata_atac: AnnData — scATAC data (LSI )
 adata_rna: AnnData — scRNA data (PCA )
 n_neighbors: int — number/count
 """
 # 
 common_bc = list(
 set(adata_atac.obs_names) & set(adata_rna.obs_names)
 )
 atac_sub = adata_atac[common_bc].copy
 rna_sub = adata_rna[common_bc].copy

 print(f"Common barcodes: {len(common_bc)}")

 # each's kNN
 sc.pp.neighbors(rna_sub, use_rep="X_pca", key_added="rna")
 sc.pp.neighbors(atac_sub, use_rep="X_spectral", key_added="atac")

 # WNN integration (muon)
 try:
 import muon as mu
 mdata = mu.MuData({"rna": rna_sub, "atac": atac_sub})
 mu.pp.neighbors(mdata, key="wnn")
 mu.tl.umap(mdata, neighbors_key="wnn")
 mu.tl.leiden(mdata, neighbors_key="wnn")

 n_clusters = mdata.obs["leiden"].nunique
 print(f"WNN integration: {n_clusters} clusters")
 return mdata
 except ImportError:
 print("muon not installed — falling back to concatenation")
 # Fallback: 
 combined = ad.concat([rna_sub, atac_sub], axis=1, merge="same")
 sc.pp.neighbors(combined)
 sc.tl.leiden(combined)
 return combined
```

## 6. scATAC-seq integrationpipeline

```python
def scatac_pipeline(fragment_file, rna_h5ad=None, genome="hg38",
 output_dir="results"):
 """
 scATAC-seq integrated analysispipeline。

 Parameters:
 fragment_file: str — fragments.tsv.gz
 rna_h5ad: str — scRNA-seq h5ad (for, optional)
 genome: str — reference genome
 output_dir: str — output directory
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) preprocessing
 adata = scatac_preprocessing(fragment_file, genome=genome)

 # 2) peak & clustering
 adata = scatac_peak_calling(adata, genome=genome)
 adata.write(output_dir / "scatac_clustered.h5ad")

 # 3) 
 motifs = motif_enrichment(adata, genome=genome)
 motifs.to_csv(output_dir / "motif_enrichment.csv", index=False)

 # 4) Gene Activity
 gene_act = gene_activity_score(adata, genome=genome)

 # 5) integration
 if rna_h5ad:
 adata_rna = sc.read_h5ad(rna_h5ad)
 mdata = multimodal_wnn(adata, adata_rna)
 mdata.write(output_dir / "multimodal_wnn.h5mu")

 print(f"scATAC pipeline: {output_dir}")
 return adata
```

---

## Pipeline Integration

```
epigenomics-chromatin → scatac-signac → single-cell-genomics
 (ChIP/ATAC bulk) (scATAC-seq) (scRNA integration)
 │ │ ↓
 peak-annotation ──────────┘ spatial-transcriptomics
 (ENCODE/ChIPAtlas) │ (Visium/MERFISH)
 ↓
 gene-regulatory-network
 (GRN )
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/scatac_clustered.h5ad` | clustering scATAC | → single-cell-genomics |
| `results/motif_enrichment.csv` | | → gene-regulatory-network |
| `results/multimodal_wnn.h5mu` | RNA+ATAC integration | → spatial-transcriptomics |

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
