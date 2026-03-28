---
name: scientific-scvi-integration
description: |
 scvi-tools single-cellintegrationskill。scVI variationalautoencoderintegration
 scANVI annotationtotalVI CITE-seq
 RNA+proteinbindinganalysisSOLO analysis。
---

# Scientific scVI Integration

scvi-tools utilizingsingle-cellrateintegration
pipeline is provided。scVI/scANVI/totalVI/SOLO by/via
batchintegration、annotation、analysis。

## When to Use

- multiplebatch's scRNA-seq data integrationwhen needed (scVI)
- celltypeannotationwhen needed (scANVI)
- CITE-seq (RNA + ADT) data bindinganalysiswhen needed (totalVI)
- (doublet) when needed (SOLO)
- expression ratetestingwhen needed
- usingclustering is performedand

---

## Quick Start

## 1. scVI & training

```python
import scvi
import scanpy as sc
import anndata as ad
import numpy as np
import pandas as pd


def setup_scvi(adata, batch_key="batch", layer=None, n_latent=30,
 n_hidden=128, n_layers=2):
 """
 scVI variationalautoencoder's & training。

 Parameters:
 adata: AnnData — input data (raw counts)
 batch_key: str — batch
 layer: str — layer
 n_latent: int — number/count
 n_hidden: int — number/count
 n_layers: int — layernumber/count

 K-Dense: scvi-tools
 """
 # scVI data
 scvi.model.SCVI.setup_anndata(
 adata,
 batch_key=batch_key,
 layer=layer,
 )

 # construction
 model = scvi.model.SCVI(
 adata,
 n_latent=n_latent,
 n_hidden=n_hidden,
 n_layers=n_layers,
 gene_likelihood="zinb", # zero-inflated negative binomial
 )

 # training
 model.train(max_epochs=400, early_stopping=True)

 # retrieval
 latent = model.get_latent_representation
 adata.obsm["X_scVI"] = latent

 print(f"scVI trained: {len(adata)} cells → {n_latent}D latent space")
 print(f" Batches: {adata.obs[batch_key].nunique}")
 return model
```

## 2. scVI batchintegration & UMAP

```python
def scvi_integration(adata, model, resolution=1.0):
 """
 scVI batchintegration & clustering。

 Parameters:
 adata: AnnData — scVI-registered data
 model: scvi.model.SCVI — training
 resolution: float — Leiden resolution
 """
 # fromgraph
 sc.pp.neighbors(adata, use_rep="X_scVI")
 sc.tl.umap(adata)
 sc.tl.leiden(adata, resolution=resolution)

 n_clusters = adata.obs["leiden"].nunique
 print(f"scVI integration: {n_clusters} clusters (resolution={resolution})")
 return adata
```

## 3. scANVI annotation

```python
def scanvi_annotation(adata, scvi_model, labels_key="cell_type",
 unlabeled_category="Unknown", n_epochs=20):
 """
 scANVI celltypeannotation。

 Parameters:
 adata: AnnData — scVI-registered data
 scvi_model: scvi.model.SCVI — training scVI
 labels_key: str — knownlabelcolumn
 unlabeled_category: str — unknownlabelvalue
 n_epochs: int — additiontraining
 """
 # scANVI = scVI + 
 scanvi_model = scvi.model.SCANVI.from_scvi_model(
 scvi_model,
 unlabeled_category=unlabeled_category,
 labels_key=labels_key,
 )

 scanvi_model.train(max_epochs=n_epochs)

 # predictionlabel
 predictions = scanvi_model.predict
 adata.obs["scANVI_prediction"] = predictions

 # predictionrate
 soft_predictions = scanvi_model.predict(soft=True)
 adata.obs["scANVI_confidence"] = soft_predictions.max(axis=1)

 n_labeled = (adata.obs[labels_key] != unlabeled_category).sum
 n_unlabeled = (adata.obs[labels_key] == unlabeled_category).sum
 mean_conf = adata.obs["scANVI_confidence"].mean

 print(f"scANVI annotation:")
 print(f" Labeled: {n_labeled}, Unlabeled: {n_unlabeled}")
 print(f" Mean confidence: {mean_conf:.3f}")
 return scanvi_model
```

## 4. totalVI CITE-seq integration

```python
def totalvi_citeseq(adata, protein_expression_obsm="protein_expression",
 batch_key="batch", n_latent=20, n_epochs=400):
 """
 totalVI RNA + ADT (CITE-seq) bindinganalysis。

 Parameters:
 adata: AnnData — RNA counts + protein expression
 protein_expression_obsm: str — ADT obsm 
 batch_key: str — batch
 n_latent: int — number/count
 """
 scvi.model.TOTALVI.setup_anndata(
 adata,
 batch_key=batch_key,
 protein_expression_obsm_key=protein_expression_obsm,
 )

 model = scvi.model.TOTALVI(
 adata,
 n_latent=n_latent,
 latent_distribution="normal",
 )

 model.train(max_epochs=n_epochs, early_stopping=True)

 # 
 latent = model.get_latent_representation
 adata.obsm["X_totalVI"] = latent

 # proteinrate (denoised)
 _, protein_fore = model.get_normalized_expression(
 n_samples=25,
 return_mean=True,
 )

 n_proteins = protein_fore.shape[1] if hasattr(protein_fore, 'shape') else 0
 print(f"totalVI: {len(adata)} cells, {n_proteins} proteins")
 print(f" Latent dim: {n_latent}")
 return model
```

## 5. SOLO 

```python
def solo_doublet_detection(adata, scvi_model, threshold=0.5):
 """
 SOLO 。

 Parameters:
 adata: AnnData — scVI-registered data
 scvi_model: scvi.model.SCVI — training scVI
 threshold: float — threshold
 """
 solo_model = scvi.external.SOLO.from_scvi_model(scvi_model)
 solo_model.train

 # prediction
 predictions = solo_model.predict
 predictions["label"] = predictions.apply(
 lambda x: "doublet" if x["doublet"] > threshold else "singlet",
 axis=1,
 )

 adata.obs["solo_doublet"] = predictions["label"].values
 adata.obs["solo_score"] = predictions["doublet"].values

 n_doublets = (adata.obs["solo_doublet"] == "doublet").sum
 doublet_rate = n_doublets / len(adata) * 100

 print(f"SOLO doublet detection:")
 print(f" Doublets: {n_doublets} ({doublet_rate:.1f}%)")
 print(f" Singlets: {len(adata) - n_doublets}")
 return predictions
```

## 6. scVI expression

```python
def scvi_differential_expression(model, adata, groupby="leiden",
 group1="0", group2="1",
 delta=0.25, batch_size=256):
 """
 scVI by/viarateexpression。

 Parameters:
 model: scvi.model.SCVI — training
 adata: AnnData — input data
 groupby: str — loopcolumn
 group1: str — comparisonloop1
 group2: str — comparisonloop2
 delta: float — LFC threshold
 """
 de_results = model.differential_expression(
 groupby=groupby,
 group1=group1,
 group2=group2,
 delta=delta,
 batch_size=batch_size,
 )

 # significantgenefilter
 sig_genes = de_results[
 (de_results["is_de_fdr_0.05"])
 & (de_results["lfc_mean"].abs > delta)
 ]

 sig_genes = sig_genes.sort_values("lfc_mean", ascending=False)

 print(f"scVI DE: {group1} vs {group2}")
 print(f" Significant genes: {len(sig_genes)}")
 print(f" Up in {group1}: {(sig_genes['lfc_mean'] > 0).sum}")
 print(f" Up in {group2}: {(sig_genes['lfc_mean'] < 0).sum}")
 return sig_genes
```

## 7. integrationpipeline

```python
def scvi_pipeline(adata_paths, batch_labels=None, labels_key="cell_type",
 output_dir="results"):
 """
 scVI → scANVI → SOLO integrationpipeline。

 Parameters:
 adata_paths: list — AnnData file path
 batch_labels: list — batchlabel
 labels_key: str — celltypelabelcolumn
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) databinding
 adatas = []
 for i, path in enumerate(adata_paths):
 a = sc.read_h5ad(path)
 a.obs["batch"] = batch_labels[i] if batch_labels else f"batch_{i}"
 adatas.append(a)

 adata = ad.concat(adatas, join="inner")
 adata.obs_names_make_unique

 # 2) preprocessing
 sc.pp.highly_variable_genes(
 adata, n_top_genes=2000, batch_key="batch", flavor="seurat_v3"
 )
 adata = adata[:, adata.var["highly_variable"]].copy

 # 3) scVI training
 scvi_model = setup_scvi(adata, batch_key="batch")

 # 4) SOLO 
 solo_results = solo_doublet_detection(adata, scvi_model)
 adata = adata[adata.obs["solo_doublet"] == "singlet"].copy

 # 5) training 
 scvi_model = setup_scvi(adata, batch_key="batch")

 # 6) scANVI annotation
 if labels_key in adata.obs.columns:
 scanvi_model = scanvi_annotation(adata, scvi_model, labels_key=labels_key)

 # 7) UMAP & clustering
 scvi_integration(adata, scvi_model)

 # save
 adata.write(output_dir / "integrated.h5ad")
 scvi_model.save(str(output_dir / "scvi_model"))

 print(f"Pipeline complete: {len(adata)} cells integrated")
 return adata, scvi_model
```

---

## Pipeline Integration

```
single-cell-genomics → scvi-integration → spatial-transcriptomics
 (scRNA-seq QC) (scVI/scANVI/totalVI) (Visium/MERFISH)
 │ │ ↓
perturbation-analysis ────────┘ gene-expression
 (Perturb-seq) │ (DEG/)
 ↓
 expression-comparison
 (Expression Atlas comparison)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/integrated.h5ad` | integration AnnData | → spatial-transcriptomics |
| `results/scvi_model/` | scVI training | → perturbation-analysis |
| `results/de_results.csv` | expressionresults | → gene-expression |
| `results/annotations.csv` | scANVI annotation | → expression-comparison |

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
