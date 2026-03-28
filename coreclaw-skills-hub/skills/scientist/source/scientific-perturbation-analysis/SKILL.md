---
name: scientific-perturbation-analysis
description: |
 single-cellanalysisskill。pertpy by/via CRISPR analysis
 minscGen predictionAugur 
 scIB integrationpipeline。
tu_tools:
 - key: cellxgene
 name: CellxGene
 description: analysisDataset Search
---

# Scientific Perturbation Analysis

pertpy / Augur / scIB utilizingsingle-cell'sanalysis
pipeline is provided。CRISPR 、、
geneetc.'s perturbation data's integrated analysis。

## When to Use

- CRISPR data (Perturb-seq) analysiswhen needed
- 'ssingle-cellexpression is evaluatedand
- 's celltypespecificity amountwhen needed
- multiple's batchintegrationmethodwhen needed (scIB)
- 's in silico predictionwhen needed (scGen)
- degree (Augur) 's highcelltype is identifiedand

---

## Quick Start

## 1. pertpy & data

```python
import pertpy as pt
import scanpy as sc
import anndata as ad
import pandas as pd
import numpy as np


def load_perturbation_data(adata_path, perturbation_key="perturbation",
 control_label="control"):
 """
 experiment AnnData & preprocessing。

 Parameters:
 adata_path: str — AnnData file path
 perturbation_key: str — perturbation labelcolumn
 control_label: str — control label

 K-Dense: pertpy
 """
 adata = sc.read_h5ad(adata_path)

 # basicpreprocessing
 sc.pp.filter_cells(adata, min_genes=200)
 sc.pp.filter_genes(adata, min_cells=3)
 sc.pp.normalize_total(adata, target_sum=1e4)
 sc.pp.log1p(adata)

 n_perturbations = adata.obs[perturbation_key].nunique
 n_control = (adata.obs[perturbation_key] == control_label).sum
 n_perturbed = len(adata) - n_control

 print(f"Loaded: {len(adata)} cells, {n_perturbations} perturbations")
 print(f"Control: {n_control}, Perturbed: {n_perturbed}")
 return adata
```

## 2. gene expression ( vs )

```python
def differential_perturbation(adata, perturbation_key="perturbation",
 control="control", target=None):
 """
 -expressionanalysis。

 Parameters:
 adata: AnnData — perturbation data
 perturbation_key: str — perturbation label
 control: str — control label
 target: str — comparison (None all)
 """
 if target:
 mask = adata.obs[perturbation_key].isin([control, target])
 adata_sub = adata[mask].copy
 else:
 adata_sub = adata.copy

 sc.tl.rank_genes_groups(
 adata_sub,
 groupby=perturbation_key,
 reference=control,
 method="wilcoxon",
 )

 results = {}
 for group in adata_sub.obs[perturbation_key].unique:
 if group == control:
 continue
 try:
 degs = sc.get.rank_genes_groups_df(adata_sub, group=group)
 degs_sig = degs[degs["pvals_adj"] < 0.05]
 results[group] = {
 "n_degs": len(degs_sig),
 "n_up": (degs_sig["logfoldchanges"] > 0).sum,
 "n_down": (degs_sig["logfoldchanges"] < 0).sum,
 "top_genes": degs_sig.head(10)["names"].tolist,
 }
 except Exception:
 continue

 print(f"DE results: {len(results)} perturbations analyzed")
 return results
```

## 3. Augur 

```python
def augur_prioritization(adata, perturbation_key="perturbation",
 cell_type_key="cell_type", control="control"):
 """
 Augur celltype and 's。

 Parameters:
 adata: AnnData — perturbation data
 perturbation_key: str — perturbation label
 cell_type_key: str — celltypelabel
 control: str — control label

 K-Dense: augur (via pertpy)
 """
 ag = pt.tl.Augur(estimator="random_forest_classifier")

 # vs eachcelltype'sAUCcalculation
 adata_augur, results = ag.predict(
 adata,
 condition_key=perturbation_key,
 cell_type_key=cell_type_key,
 control_label=control,
 )

 # results DataFrame
 auc_df = results["summary_metrics"]
 auc_df = auc_df.sort_values("auc", ascending=False)

 print(f"Augur prioritization:")
 for _, row in auc_df.head(5).iterrows:
 print(f" {row['cell_type']}: AUC={row['auc']:.3f}")

 return auc_df
```

## 4. scGen prediction

```python
def scgen_perturbation_prediction(adata, perturbation_key="perturbation",
 cell_type_key="cell_type",
 control="control", target_perturbation=None,
 target_cell_type=None):
 """
 scGen by/via's in silico prediction。

 Parameters:
 adata: AnnData — training data
 target_perturbation: str — prediction's
 target_cell_type: str — prediction's celltype
 """
 import scgen

 # training
 scg = scgen.SCGEN(adata)
 scg.train(max_epochs=100, batch_size=32)

 # prediction
 pred, delta = scg.predict(
 ctrl_key=control,
 stim_key=target_perturbation,
 celltype_to_predict=target_cell_type,
 )

 print(f"scGen prediction: {target_cell_type} under {target_perturbation}")
 print(f" Predicted cells: {pred.shape[0]}")
 return pred, delta
```

## 5. scIB integration

```python
def benchmark_integration(adata, batch_key="batch", label_key="cell_type",
 methods=None):
 """
 scIB batchintegrationmethod。

 Parameters:
 adata: AnnData — batchdata
 batch_key: str — batchlabel
 label_key: str — celltypelabel
 methods: list — evaluatesmetrics

 K-Dense: scib
 """
 import scib

 if methods is None:
 methods = ["scib"]

 # basicmetrics
 metrics = {}

 # batch correction metrics
 metrics["batch_kbet"] = scib.me.kBET(
 adata, batch_key=batch_key, label_key=label_key
 )
 metrics["batch_silhouette"] = scib.me.silhouette_batch(
 adata, batch_key=batch_key, label_key=label_key, embed="X_pca"
 )

 # bio conservation metrics
 metrics["bio_nmi"] = scib.me.nmi(adata, label_key, "leiden")
 metrics["bio_ari"] = scib.me.ari(adata, label_key, "leiden")
 metrics["bio_silhouette"] = scib.me.silhouette(
 adata, label_key=label_key, embed="X_pca"
 )

 # 
 metrics["overall"] = 0.6 * np.mean([
 metrics["bio_nmi"], metrics["bio_ari"], metrics["bio_silhouette"]
 ]) + 0.4 * np.mean([
 metrics["batch_kbet"], metrics["batch_silhouette"]
 ])

 print(f"scIB benchmark:")
 for k, v in metrics.items:
 print(f" {k}: {v:.4f}")
 return metrics
```

## 6. analysis

```python
def perturbation_signature(adata, perturbation_key="perturbation",
 control="control", n_top_genes=50):
 """
 geneextraction。

 Parameters:
 adata: AnnData — perturbation data
 perturbation_key: str — perturbation label
 control: str — control label
 n_top_genes: int — genenumber/count
 """
 perturbations = [p for p in adata.obs[perturbation_key].unique
 if p != control]

 signatures = {}
 ctrl_mean = adata[adata.obs[perturbation_key] == control].X.mean(axis=0)
 ctrl_mean = np.asarray(ctrl_mean).flatten

 for pert in perturbations:
 pert_mask = adata.obs[perturbation_key] == pert
 pert_mean = adata[pert_mask].X.mean(axis=0)
 pert_mean = np.asarray(pert_mean).flatten

 delta = pert_mean - ctrl_mean
 gene_indices = np.argsort(np.abs(delta))[::-1][:n_top_genes]

 signatures[pert] = {
 "top_genes": adata.var_names[gene_indices].tolist,
 "deltas": delta[gene_indices].tolist,
 "n_cells": int(pert_mask.sum),
 }

 print(f"Signatures extracted: {len(signatures)} perturbations, "
 f"{n_top_genes} genes each")
 return signatures
```

---

## Pipeline Integration

```
single-cell-genomics → perturbation-analysis → pathway-enrichment
 (scRNA-seq QC) ( DE/Augur/scGen) (KEGG/Reactome)
 │ │ ↓
spatial-transcriptomics ──┘ │ disease-research
 (Visium/MERFISH) ↓ (GWAS/DisGeNET)
 drug-target-profiling
 (evaluation)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/perturbation_de.json` | expressionresults | → pathway-enrichment |
| `results/augur_scores.csv` | Augur | → single-cell-genomics |
| `results/perturbation_signatures.json` | | → drug-target-profiling |
| `results/scib_benchmark.json` | integration | → spatial-transcriptomics |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `cellxgene` | CellxGene | analysisDataset Search |
