---
name: scientific-human-cell-atlas
description: |
 Human Cell Atlas (HCA) dataskill。HCA Data Portal API
 searchfileCELLxGENE Census integration
 celltypeannotationconstruction。---

# Scientific Human Cell Atlas

HCA Data Portal / CELLxGENE Census utilizinglarge-scalesingle-cell
dataanalysispipeline is provided。

## When to Use

- HCA Data Portal fromexperimentdata is searchedand
- CELLxGENE Census large-scalesingle-cellwhen needed
- tissue/disease's celltypeconfiguration is investigatedand
- multiple HCA celltype is comparedand
- single-cell'smapping is performedand
- celltype'sannotation is performedand

---

## Quick Start

## 1. HCA Data Portal search

```python
import requests
import pandas as pd
import json

HCA_BASE = "https://service.azul.data.humancellatlas.org"
HCA_CATALOG = "dcp44"


def hca_search_projects(keyword=None, organ=None, disease=None,
 species="Homo sapiens", limit=25):
 """
 HCA Data Portal — search。

 Parameters:
 keyword: str — keyword search
 organ: str — organ (example: "lung", "heart")
 disease: str — disease (example: "COVID-19")
 species: str — organism/species
 limit: int — maximum results
 """
 url = f"{HCA_BASE}/index/projects"
 params = {"catalog": HCA_CATALOG, "size": limit}

 filters = {}
 if organ:
 filters["organ"] = {"is": [organ]}
 if disease:
 filters["disease"] = {"is": [disease]}
 if species:
 filters["genusSpecies"] = {"is": [species]}
 if keyword:
 params["q"] = keyword
 if filters:
 params["filters"] = json.dumps(filters)

 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 projects = []
 for hit in data.get("hits", []):
 proj = hit.get("projects", [{}])[0]
 samples = hit.get("samples", [{}])[0]
 protocols = hit.get("protocols", [{}])[0]
 projects.append({
 "project_id": proj.get("projectId", ""),
 "title": proj.get("projectTitle", ""),
 "organ": ", ".join(samples.get("organ", [])),
 "disease": ", ".join(samples.get("disease", [])),
 "species": ", ".join(samples.get("genusSpecies", [])),
 "cell_count": hit.get("cellSuspensions", [{}])[0].get(
 "totalCells", 0),
 "library_method": ", ".join(protocols.get(
 "libraryConstructionApproach", [])),
 "donor_count": samples.get("donorCount", 0),
 })

 df = pd.DataFrame(projects)
 print(f"HCA: {len(df)} projects found")
 return df
```

## 2. HCA fileretrieval

```python
def hca_get_project_files(project_id, file_format=None):
 """
 HCA — 'sfilelistretrieval。

 Parameters:
 project_id: str — UUID
 file_format: str — fileshapeformula (example: "h5ad", "loom", "csv")
 """
 url = f"{HCA_BASE}/index/files"
 filters = {"projectId": {"is": [project_id]}}
 if file_format:
 filters["fileFormat"] = {"is": [file_format]}

 params = {
 "catalog": HCA_CATALOG,
 "filters": json.dumps(filters),
 "size": 100,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 files = []
 for hit in data.get("hits", []):
 for f in hit.get("files", []):
 files.append({
 "file_id": f.get("uuid", ""),
 "name": f.get("name", ""),
 "format": f.get("format", ""),
 "size_bytes": f.get("size", 0),
 "url": f.get("url", ""),
 })

 df = pd.DataFrame(files)
 print(f"HCA files ({project_id[:8]}): {len(df)} files")
 return df
```

## 3. CELLxGENE Census 

```python
def cellxgene_census_query(organism="homo_sapiens", tissue=None,
 disease=None, cell_type=None,
 gene_list=None, max_cells=50000):
 """
 CELLxGENE Census — large-scalesingle-cell。

 Parameters:
 organism: str — organism/species
 tissue: str — tissue
 disease: str — disease
 cell_type: str — celltype
 gene_list: list[str] — retrievalgene list
 max_cells: int — cellnumber/count
 """
 import cellxgene_census

 census = cellxgene_census.open_soma

 # observationfilterconstruction
 obs_filters = []
 if tissue:
 obs_filters.append(f"tissue == '{tissue}'")
 if disease:
 obs_filters.append(f"disease == '{disease}'")
 if cell_type:
 obs_filters.append(f"cell_type == '{cell_type}'")

 obs_filter = " and ".join(obs_filters) if obs_filters else None

 # genefilter
 var_filter = None
 if gene_list:
 genes_str = "', '".join(gene_list)
 var_filter = f"feature_name in ['{genes_str}']"

 adata = cellxgene_census.get_anndata(
 census,
 organism=organism,
 obs_value_filter=obs_filter,
 var_value_filter=var_filter,
 obs_column_names=[
 "cell_type", "tissue", "disease",
 "donor_id", "dataset_id", "assay",
 ],
 )

 if adata.n_obs > max_cells:
 import numpy as np
 idx = np.random.choice(adata.n_obs, max_cells, replace=False)
 adata = adata[idx].copy

 census.close
 print(f"CELLxGENE Census: {adata.n_obs} cells × {adata.n_vars} genes")
 return adata
```

## 4. celltypeconfigurationanalysis

```python
import scanpy as sc


def cell_type_composition(adata, groupby="tissue", cell_type_col="cell_type"):
 """
 celltypeconfiguration's amountcomparison。

 Parameters:
 adata: AnnData — single-celldata
 groupby: str — loopnumber/count
 cell_type_col: str — celltypecolumn
 """
 # configurationcalculation
 composition = (
 adata.obs.groupby([groupby, cell_type_col])
.size
.unstack(fill_value=0)
 )
 composition_pct = composition.div(composition.sum(axis=1), axis=0) * 100

 print(f"Cell type composition: {composition.shape[0]} groups × "
 f"{composition.shape[1]} cell types")
 return composition_pct
```

## 5. HCA integrationpipeline

```python
def hca_atlas_pipeline(organ, disease=None, output_dir="results"):
 """
 HCA + CELLxGENE integrationpipeline。

 Parameters:
 organ: str — organ
 disease: str — disease
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) HCA search
 projects = hca_search_projects(organ=organ, disease=disease)
 projects.to_csv(output_dir / "hca_projects.csv", index=False)

 # 2) CELLxGENE Census 
 adata = cellxgene_census_query(tissue=organ, disease=disease)

 # 3) preprocessing
 sc.pp.normalize_total(adata, target_sum=1e4)
 sc.pp.log1p(adata)
 sc.pp.highly_variable_genes(adata, n_top_genes=2000)
 adata = adata[:, adata.var["highly_variable"]].copy
 sc.pp.pca(adata)
 sc.pp.neighbors(adata)
 sc.tl.umap(adata)

 # 4) celltypeconfiguration
 composition = cell_type_composition(adata)
 composition.to_csv(output_dir / "cell_type_composition.csv")

 # 5) save
 adata.write(output_dir / "hca_atlas.h5ad")

 print(f"HCA atlas pipeline: {output_dir}")
 return {"projects": projects, "adata": adata, "composition": composition}
```

---

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
3. Write `report.md` summarizing methods, results, and interpretation

## Pipeline Integration

```
single-cell-genomics → human-cell-atlas → scvi-integration
 (scanpy standard) (HCA/CELLxGENE) (scVI integration)
 │ │ ↓
 spatial-transcriptomics ───┘ cell-type-annotation
 (Visium/MERFISH) │ (mapping)
 ↓
 gpu-singlecell
 (large-scale)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/hca_projects.csv` | HCA list | → single-cell-genomics |
| `results/hca_atlas.h5ad` | AnnData | → scvi-integration |
| `results/cell_type_composition.csv` | celltypeconfiguration | → spatial-transcriptomics |
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
