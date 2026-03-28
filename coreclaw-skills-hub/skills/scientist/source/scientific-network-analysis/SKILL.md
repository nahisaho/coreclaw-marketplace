---
name: scientific-network-analysis
description: |
 networkanalysiscorrelationnetworkconstruction'sskill。NetworkX usinggraphconstruction、
 analysis、、networkvisualization is performedfor。
 Scientific Skills Exp-04, 07 。PSP also for。
---

# Scientific Network Analysis

NetworkX usingnetworkanalysispipelineskill。PPI network、
correlationnetwork、PSP etc.'s constructionanalysisvisualization is provided。

## When to Use

- proteininteractionnetworkconstructionanalysiswhen needed
- correlationfromnetworkconstructionwhen needed
- node's important（、） evaluationwhen needed
- （module）when needed
- PSP （） visualizationwhen needed

## Quick Start

## Standard Pipeline

### 1. networkconstruction

```python
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def build_network_from_edgelist(edges_df, source_col, target_col,
 weight_col=None, directed=False):
 """edge DataFrame fromnetwork is built。"""
 if directed:
 G = nx.DiGraph
 else:
 G = nx.Graph

 for _, row in edges_df.iterrows:
 kwargs = {}
 if weight_col and weight_col in row:
 kwargs["weight"] = row[weight_col]
 G.add_edge(row[source_col], row[target_col], **kwargs)

 return G

def build_correlation_network(corr_matrix, threshold=0.5, absolute=True):
 """
 correlationfromthresholdabove/more's edge itemsnetwork is built。
 's correlationnetwork for（Exp-07）。
 """
 G = nx.Graph
 variables = corr_matrix.columns

 for i, var1 in enumerate(variables):
 for j, var2 in enumerate(variables):
 if i < j:
 r = corr_matrix.iloc[i, j]
 if absolute:
 if abs(r) >= threshold:
 G.add_edge(var1, var2, weight=abs(r),
 correlation=r, sign="+" if r > 0 else "-")
 else:
 if r >= threshold:
 G.add_edge(var1, var2, weight=r)

 return G
```

### 2. analysis

```python
def comprehensive_centrality(G):
 """Compute four centrality metrics at once."""
 centrality = pd.DataFrame(index=list(G.nodes))
 centrality["Degree"] = pd.Series(dict(G.degree))
 centrality["Betweenness"] = pd.Series(nx.betweenness_centrality(G))
 centrality["Closeness"] = pd.Series(nx.closeness_centrality(G))

 try:
 centrality["Eigenvector"] = pd.Series(
 nx.eigenvector_centrality(G, max_iter=1000)
 )
 except nx.PowerIterationFailedConvergence:
 centrality["Eigenvector"] = np.nan

 centrality = centrality.sort_values("Degree", ascending=False)
 centrality.to_csv("results/centrality_measures.csv")
 return centrality

def identify_hubs(centrality_df, top_n=10):
 """node（number/count+）."""
 # Degree and Betweenness 's top'snode
 degree_top = set(centrality_df.nlargest(top_n, "Degree").index)
 between_top = set(centrality_df.nlargest(top_n, "Betweenness").index)
 hubs = degree_top & between_top
 return list(hubs), centrality_df.loc[list(hubs)]
```

### 3. 

```python
def detect_communities(G, method="louvain"):
 """
 is executed。
 method: 'louvain', 'greedy', 'label_propagation'
 """
 if method == "louvain":
 try:
 import community as community_louvain
 partition = community_louvain.best_partition(G, random_state=42)
 except ImportError:
 # 
 from networkx.algorithms.community import greedy_modularity_communities
 communities = list(greedy_modularity_communities(G))
 partition = {node: i for i, comm in enumerate(communities)
 for node in comm}
 elif method == "greedy":
 from networkx.algorithms.community import greedy_modularity_communities
 communities = list(greedy_modularity_communities(G))
 partition = {node: i for i, comm in enumerate(communities)
 for node in comm}
 elif method == "label_propagation":
 from networkx.algorithms.community import label_propagation_communities
 communities = list(label_propagation_communities(G))
 partition = {node: i for i, comm in enumerate(communities)
 for node in comm}

 nx.set_node_attributes(G, partition, "community")
 modularity = nx.community.modularity(
 G, [{n for n, c in partition.items if c == i}
 for i in set(partition.values)]
 )

 return partition, modularity
```

### 4. networkvisualization

```python
def visualize_network(G, partition=None, node_size_attr="Degree",
 title="Network", figsize=(12, 12)):
 """network spring layout visualization."""
 fig, ax = plt.subplots(figsize=figsize)
 pos = nx.spring_layout(G, seed=42, k=2/np.sqrt(len(G.nodes)))

 # node
 if node_size_attr == "Degree":
 sizes = np.array([G.degree(n) for n in G.nodes])
 else:
 sizes = np.array([G.nodes[n].get(node_size_attr, 1) for n in G.nodes])
 sizes = 100 + sizes / sizes.max * 500

 # node（）
 if partition:
 colors = [partition.get(n, 0) for n in G.nodes]
 cmap = plt.cm.Set2
 else:
 colors = "steelblue"
 cmap = None

 nx.draw_networkx_edges(G, pos, alpha=0.2, ax=ax)
 nodes = nx.draw_networkx_nodes(G, pos, node_size=sizes,
 node_color=colors, cmap=cmap,
 alpha=0.8, ax=ax)
 nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)

 ax.set_title(title, fontsize=14, fontweight="bold")
 ax.axis("off")
 plt.tight_layout
 plt.savefig("figures/network_visualization.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 5. PSP （Exp-13 ）

```python
def psp_path_diagram(ps_corr, sp_corr, pp_corr,
 threshold=0.3, figsize=(14, 10)):
 """
 Process → Structure → Property 'sdrawing/plotting.
 's: ='scorrelation、='scorrelation、=|r| example。
 """
 fig, ax = plt.subplots(figsize=figsize)

 # node（3 ）
 process_vars = list(ps_corr.index)
 structure_vars = list(ps_corr.columns)
 property_vars = list(sp_corr.columns)

 def place_nodes(names, x, color):
 positions = {}
 n = len(names)
 for i, name in enumerate(names):
 y = (n - 1 - i) / max(n - 1, 1)
 positions[name] = (x, y)
 ax.scatter(x, y, s=300, c=color, zorder=5, edgecolors="black")
 ax.text(x, y, name, ha="center", va="center", fontsize=7,
 fontweight="bold", zorder=6)
 return positions

 pos_p = place_nodes(process_vars, 0, "#FFB3BA")
 pos_s = place_nodes(structure_vars, 1, "#BAE1FF")
 pos_pr = place_nodes(property_vars, 2, "#BAFFC9")

 # edgedrawing/plotting
 def draw_edges(corr_df, pos_from, pos_to):
 for var1 in corr_df.index:
 for var2 in corr_df.columns:
 r = corr_df.loc[var1, var2]
 if abs(r) >= threshold:
 color = "red" if r > 0 else "blue"
 width = abs(r) * 3
 ax.annotate("", xy=pos_to[var2], xytext=pos_from[var1],
 arrowprops=dict(arrowstyle="->", color=color,
 lw=width, alpha=0.6))

 draw_edges(ps_corr, pos_p, pos_s)
 draw_edges(sp_corr, pos_s, pos_pr)

 # label
 ax.text(0, -0.1, "Process", ha="center", fontsize=12,
 fontweight="bold", color="#FF6B6B")
 ax.text(1, -0.1, "Structure", ha="center", fontsize=12,
 fontweight="bold", color="#4ECDC4")
 ax.text(2, -0.1, "Property", ha="center", fontsize=12,
 fontweight="bold", color="#45B7D1")

 ax.set_xlim(-0.3, 2.3)
 ax.set_ylim(-0.2, 1.1)
 ax.axis("off")
 ax.set_title("PSP Linkage Path Diagram", fontweight="bold", fontsize=14)
 plt.tight_layout
 plt.savefig("figures/psp_path_diagram.png", dpi=300, bbox_inches="tight")
 plt.close
```

## References

### Output Files

| File | Format |
|---|---|
| `results/centrality_measures.csv` | CSV |
| `results/edge_list.csv` | CSV |
| `results/node_attributes.csv` | CSV |
| `figures/network_visualization.png` | PNG |
| `figures/psp_path_diagram.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| STRING | `STRING_get_protein_interactions` | proteininteractionnetwork |
| IntAct | `intact_search_interactions` | molecular interaction search |
| IntAct | `intact_get_interaction_network` | PPI networkretrieval |
| Reactome | `Reactome_map_uniprot_to_pathways` | pathway mapping |
| KEGG | `kegg_get_pathway_info` | pathway information |
| GO | `GO_get_annotations_for_gene` | GO annotation |

#### Reference Experiments

- **Exp-04**: PPI network（71 protein、4 type、Louvain ）
- **Exp-07**: Spearman correlationnetwork（）
- **Exp-13**: PSP （Process→Structure→Property ）
