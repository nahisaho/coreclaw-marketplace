---
name: scientific-bioinformatics
description: |
 analysispipeline'sskill。scRNA-seq（Scanpy）、genomesequenceanalysis
 （BioPython）、PPI networkanalysis（NetworkX）、'spreprocessing is performedfor。
 Scientific Skills Exp-01, 04, 07, 09 。
---

# Scientific Bioinformatics Pipelines

data'sanalysispipelineskill。scRNA-seq、genomesequenceanalysis、PPI network、
's 4 type's workflow integrationprovides。

## When to Use

- scRNA-seq data's QCpreprocessingclusteringDEG analysis
- genome/proteinsequence's phylogenyanalysisforanalysis
- proteininteractionnetwork's constructionanalysis
- 'spreprocessing（transformation）PLS-DA

## Quick Start

## 1. scRNA-seq pipeline（Exp-01）

### Scanpy standardworkflow

```python
import scanpy as sc

def scrnaseq_pipeline(adata, min_genes=200, max_genes=5000,
 max_pct_mito=20, n_hvg=2000, resolution=0.5):
 """
 Scanpy 's standard scRNA-seq analysispipeline。
 QC → normalization → HVG → PCA → Neighbors → Leiden → UMAP
 """
 # QC filter
 sc.pp.filter_cells(adata, min_genes=min_genes)
 sc.pp.filter_genes(adata, min_cells=3)

 adata.var["mt"] = adata.var_names.str.startswith("MT-")
 sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"],
 percent_top=None, inplace=True)
 adata = adata[adata.obs["pct_counts_mt"] < max_pct_mito].copy
 adata = adata[adata.obs["n_genes_by_counts"] < max_genes].copy

 # normalization & Log transformation
 sc.pp.normalize_total(adata, target_sum=1e4)
 sc.pp.log1p(adata)

 # HVG selection
 sc.pp.highly_variable_genes(adata, n_top_genes=n_hvg)
 adata.raw = adata
 adata = adata[:, adata.var["highly_variable"]].copy

 # PCA → Neighbors → UMAP → Leiden
 sc.pp.scale(adata, max_value=10)
 sc.tl.pca(adata, n_comps=50)
 sc.pp.neighbors(adata, n_pcs=30)
 sc.tl.umap(adata)
 sc.tl.leiden(adata, resolution=resolution)

 return adata
```

### cell typeannotation

```python
CELL_MARKERS = {
 "CD4+ T": ["IL7R", "CD4"],
 "CD8+ T": ["CD8A", "CD8B"],
 "B cell": ["MS4A1", "CD79A"],
 "NK": ["GNLY", "NKG7"],
 "Monocyte": ["CD14", "LYZ"],
 "DC": ["FCER1A", "CST3"],
 "Platelet": ["PPBP"],
}

def annotate_clusters(adata, marker_dict=None):
 """gene'sannotation。"""
 if marker_dict is None:
 marker_dict = CELL_MARKERS
 # and 'smeanexpression levelcelltype
 cluster_annotations = {}
 for cluster in adata.obs["leiden"].unique:
 mask = adata.obs["leiden"] == cluster
 best_score = -1
 best_type = "Unknown"
 for cell_type, markers in marker_dict.items:
 available = [m for m in markers if m in adata.raw.var_names]
 if available:
 score = adata.raw[mask][:, available].X.mean
 if score > best_score:
 best_score = score
 best_type = cell_type
 cluster_annotations[cluster] = best_type
 adata.obs["cell_type"] = adata.obs["leiden"].map(cluster_annotations)
 return adata
```

## 2. genomesequenceanalysispipeline（Exp-09）

```python
def compute_sequence_statistics(sequence):
 """DNA sequence's basicamount is computed。"""
 from collections import Counter
 seq_str = str(sequence).upper
 counts = Counter(seq_str)
 length = len(seq_str)
 gc_content = (counts.get("G", 0) + counts.get("C", 0)) / length * 100
 return {
 "Length": length,
 "GC_Content": gc_content,
 "A": counts.get("A", 0), "T": counts.get("T", 0),
 "G": counts.get("G", 0), "C": counts.get("C", 0),
 }

def codon_usage_rscu(coding_sequence):
 """RSCU（Relative Synonymous Codon Usage） is computed。"""
 from collections import Counter
 codons = [coding_sequence[i:i+3] for i in range(0, len(coding_sequence)-2, 3)]
 codon_counts = Counter(codons)
 # RSCU = observed / expected_if_uniform
 # group andcalculation
 return codon_counts # 、all Exp-09 reference
```

## 3. PPI networkanalysis（Exp-04）

```python
import networkx as nx

def build_ppi_network(interactions_df, source_col, target_col,
 weight_col=None):
 """PPI network is built。"""
 G = nx.Graph
 for _, row in interactions_df.iterrows:
 if weight_col:
 G.add_edge(row[source_col], row[target_col],
 weight=row[weight_col])
 else:
 G.add_edge(row[source_col], row[target_col])
 return G

def centrality_analysis(G):
 """Compute four centrality metrics at once."""
 centralities = pd.DataFrame({
 "Degree": dict(G.degree),
 "Betweenness": nx.betweenness_centrality(G),
 "Closeness": nx.closeness_centrality(G),
 "Eigenvector": nx.eigenvector_centrality(G, max_iter=1000),
 })
 centralities.to_csv("results/centrality_measures.csv")
 return centralities

def community_detection(G, method="louvain"):
 """。"""
 if method == "louvain":
 import community as community_louvain
 partition = community_louvain.best_partition(G)
 nx.set_node_attributes(G, partition, "community")
 return partition
 elif method == "greedy":
 from networkx.algorithms.community import greedy_modularity_communities
 communities = list(greedy_modularity_communities(G))
 partition = {}
 for i, comm in enumerate(communities):
 for node in comm:
 partition[node] = i
 return partition
```

## 4. preprocessing（Exp-07）

```python
from sklearn.impute import KNNImputer

def metabolomics_preprocessing(df, metabolite_cols, group_col=None):
 """
 'sstandardpreprocessingpipeline。
 KNN → Log2 transformation → Pareto 
 """
 X = df[metabolite_cols].values.copy

 # KNN 
 imputer = KNNImputer(n_neighbors=5)
 X_imputed = imputer.fit_transform(X)

 # Log2 transformation（value 's value）
 X_log = np.log2(X_imputed + 1)

 # Pareto 
 means = X_log.mean(axis=0)
 stds = X_log.std(axis=0)
 X_pareto = (X_log - means) / np.sqrt(stds + 1e-10)

 result_df = pd.DataFrame(X_pareto, columns=metabolite_cols, index=df.index)
 if group_col:
 result_df[group_col] = df[group_col].values

 return result_df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/centrality_measures.csv` | CSV |
| `results/community_pathway_mapping.csv` | CSV |
| `results/codon_usage.csv` | CSV |
| `figures/umap_clusters.png` | PNG |
| `figures/network_visualization.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| MyGene | `MyGene_get_gene_annotation` | geneannotation |
| UniProt | `UniProt_search` | protein search |
| KEGG | `kegg_get_pathway_info` | pathway informationretrieval |
| Reactome | `Reactome_map_uniprot_to_pathways` | UniProt→pathway mapping |
| GO | `GO_get_annotations_for_gene` | GO annotation |
| GEO | `geo_search_datasets` | expressionDataset Search |

#### Reference Experiments

- **Exp-01**: scRNA-seq（Scanpy + PyDESeq2 + KEGG）
- **Exp-04**: PPI network（NetworkX + Louvain）
- **Exp-07**: （KNN + PLS-DA + VIP）
- **Exp-09**: genomesequence（BioPython + phylogeny + RSCU）
