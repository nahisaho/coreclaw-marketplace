---
name: scientific-spatial-multiomics
description: |
 multi-omics integrationskill。MERFISH/Visium 's
 transcriptomeand proteomics's
 integrationanalysiscellgraphconstructionpipeline。
---

# Scientific Spatial Multi-omics

MERFISHVisiumCODEX 'smulti-omicsdataintegration、
alignmentanalysisgraph's
pipeline is provided。

## When to Use

- transcriptome and proteomicsintegrationwhen needed
- MERFISH + CODEX dataalignmentwhen needed
- moleculewhen needed
- cellgraphfrom/ is extractedand
- multi-omics's preprocessingpipeline is builtand

---

## Quick Start

## 1. Loading data

```python
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


def load_spatial_modality(coord_file, expr_file,
 modality_name="RNA"):
 """
 Loading data。

 Parameters:
 coord_file: str — coordinates CSV (cell_id, x, y)
 expr_file: str — expression/protein CSV
 (cell_id, features...)
 modality_name: str — 
 """
 coords = pd.read_csv(coord_file, index_col="cell_id")
 expr = pd.read_csv(expr_file, index_col="cell_id")

 common = coords.index.intersection(expr.index)
 coords = coords.loc[common]
 expr = expr.loc[common]

 print(f"Spatial {modality_name}: "
 f"{len(common)} cells, "
 f"{expr.shape[1]} features")
 return coords, expr


def spatial_alignment(coords_a, coords_b,
 max_distance=50.0):
 """
 coordinatesalignment 。

 Parameters:
 coords_a: DataFrame — A coordinates (x, y)
 coords_b: DataFrame — B coordinates (x, y)
 max_distance: float — (μm)
 """
 tree_b = cKDTree(coords_b[["x", "y"]].values)
 dists, idxs = tree_b.query(
 coords_a[["x", "y"]].values, k=1)

 mask = dists < max_distance
 matched_a = coords_a.index[mask]
 matched_b = coords_b.index[idxs[mask]]

 alignment = pd.DataFrame({
 "cell_a": matched_a,
 "cell_b": matched_b,
 "distance": dists[mask],
 })

 print(f"Alignment: {len(alignment)} matched pairs "
 f"(max_dist={max_distance}μm)")
 return alignment
```

## 2. analysis

```python
def spatial_codetection(expr_a, expr_b, alignment,
 method="pearson", top_n=50):
 """
 correlationanalysis。

 Parameters:
 expr_a: DataFrame — A expression
 expr_b: DataFrame — B expression
 alignment: DataFrame — alignmentresults
 method: str — correlation
 (pearson / spearman)
 top_n: int — topnumber/count
 """
 from itertools import product
 from scipy import stats

 a_matched = expr_a.loc[alignment["cell_a"]]
 b_matched = expr_b.loc[alignment["cell_b"]]
 a_matched.index = range(len(a_matched))
 b_matched.index = range(len(b_matched))

 results = []
 for fa, fb in product(a_matched.columns[:100],
 b_matched.columns[:100]):
 va = a_matched[fa].values
 vb = b_matched[fb].values
 mask = np.isfinite(va) & np.isfinite(vb)
 if mask.sum < 30:
 continue

 if method == "spearman":
 r, p = stats.spearmanr(va[mask], vb[mask])
 else:
 r, p = stats.pearsonr(va[mask], vb[mask])

 results.append({
 "feature_a": fa,
 "feature_b": fb,
 "correlation": r,
 "p_value": p,
 })

 df = pd.DataFrame(results)
 df.sort_values("correlation", ascending=False,
 key=abs, inplace=True)
 top = df.head(top_n)

 print(f"Codetection: {len(df)} pairs, "
 f"top r={top.iloc[0]['correlation']:.3f}")
 return top
```

## 3. cellgraph

```python
def cell_neighborhood_graph(coords, k_neighbors=15):
 """
 cellgraphconstruction。

 Parameters:
 coords: DataFrame — coordinates (x, y)
 k_neighbors: int — k number/count
 """
 tree = cKDTree(coords[["x", "y"]].values)
 dists, idxs = tree.query(
 coords[["x", "y"]].values,
 k=k_neighbors + 1)

 edges = []
 for i in range(len(coords)):
 for j_idx in range(1, k_neighbors + 1):
 j = idxs[i, j_idx]
 edges.append({
 "source": coords.index[i],
 "target": coords.index[j],
 "distance": dists[i, j_idx],
 })

 edge_df = pd.DataFrame(edges)
 print(f"Neighborhood graph: "
 f"{len(coords)} nodes, "
 f"{len(edge_df)} edges (k={k_neighbors})")
 return edge_df


def spatial_community_detection(edge_df, coords,
 resolution=1.0):
 """
 (Leiden)。

 Parameters:
 edge_df: DataFrame — edge
 coords: DataFrame — coordinates
 resolution: float — Leiden resolution
 """
 try:
 import igraph as ig
 import leidenalg
 except ImportError:
 print("pip install igraph leidenalg")
 return pd.DataFrame

 nodes = list(coords.index)
 node_map = {n: i for i, n in enumerate(nodes)}

 g = ig.Graph(directed=False)
 g.add_vertices(len(nodes))
 edges = [
 (node_map[r["source"]], node_map[r["target"]])
 for _, r in edge_df.iterrows
 if r["source"] in node_map
 and r["target"] in node_map
 ]
 g.add_edges(edges)

 part = leidenalg.find_partition(
 g, leidenalg.RBConfigurationVertexPartition,
 resolution_parameter=resolution)

 result = pd.DataFrame({
 "cell_id": nodes,
 "community": part.membership,
 "x": coords["x"].values,
 "y": coords["y"].values,
 })

 n_comm = result["community"].nunique
 print(f"Communities: {n_comm} spatial niches "
 f"(resolution={resolution})")
 return result
```

## 4. multi-omics integrationpipeline

```python
def spatial_multiomics_pipeline(
 rna_coords, rna_expr,
 protein_coords, protein_expr,
 output_dir="results",
):
 """
 multi-omics integrationpipeline。

 Parameters:
 rna_coords: str — RNA coordinatesfile
 rna_expr: str — RNA expressionfile
 protein_coords: str — proteomicscoordinatesfile
 protein_expr: str — proteomicsexpressionfile
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) Loading data
 rc, re = load_spatial_modality(
 rna_coords, rna_expr, "RNA")
 pc, pe = load_spatial_modality(
 protein_coords, protein_expr, "Protein")

 # 2) alignment
 alignment = spatial_alignment(rc, pc)
 alignment.to_csv(output_dir / "alignment.csv",
 index=False)

 # 3) analysis
 codet = spatial_codetection(re, pe, alignment)
 codet.to_csv(output_dir / "codetection.csv",
 index=False)

 # 4) graph + 
 edges = cell_neighborhood_graph(rc)
 comms = spatial_community_detection(edges, rc)
 comms.to_csv(output_dir / "communities.csv",
 index=False)

 print(f"Spatial multiomics pipeline → {output_dir}")
 return {
 "alignment": alignment,
 "codetection": codet,
 "communities": comms,
 }
```

---

## Pipeline Integration

```
spatial-transcriptomics → spatial-multiomics → multi-omics
 (Visium/MERFISH) (integration) (integrationomics)
 │ │ ↓
 human-cell-atlas ─────────────┘ single-cell-rnaseq
 (HCA atlas) (scRNA-seq reference)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/alignment.csv` | alignment | → multi-omics |
| `results/codetection.csv` | | → pathway-analysis |
| `results/communities.csv` | | → spatial-transcriptomics |

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
