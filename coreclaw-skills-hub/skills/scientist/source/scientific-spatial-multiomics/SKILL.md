---
name: scientific-spatial-multiomics
description: |
 multi-omics integrationskill。MERFISH/Visium 's
 transcriptomeand proteomics's
 integrationanalysiscellgraphconstructionpipeline。
tu_tools:
 - key: cellxgene
 name: CellxGene
 description: multi-omicsdatasearch
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `cellxgene` | CellxGene | multi-omicsdatasearch |
