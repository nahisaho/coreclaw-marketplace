---
name: scientific-scatac-signac
description: |
 scATAC-seq Signac skill. Single-cell ATAC-seq analysis with Signac/ArchR, peak calling, motif enrichment, chromatin accessibility clustering, and gene activity scoring.
tu_tools:
 - key: encode
 name: ENCODE
 description: scATAC-seq referenceepigenomedata
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `encode` | ENCODE | scATAC-seq referenceepigenomedata |

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
