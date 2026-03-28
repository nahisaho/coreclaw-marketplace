---
name: scientific-network-visualization
description: |
 Network visualization skill. Interactive network plots (Cytoscape.js/D3/NetworkX), layout algorithms, edge bundling, node clustering visualization, and publication-quality network figures.
---

# Scientific Network Visualization

network/graphdata's analysis
visualizationpipeline is provided。

## When to Use

- interaction's networkstructureanalysiswhen needed
-  when needed
- node is identifiedand
- PyVis networkfigure is createdand
- correlationfromnetwork is builtand
- timenetworkanalysiswhen needed

> **Note**: protein PPI network `scientific-protein-interaction-network` reference。

---

## Quick Start

## 1. networkconstructionbasic

```python
import numpy as np
import pandas as pd
import networkx as nx


def build_network_from_edgelist(edges_df, source_col, target_col,
 weight_col=None, directed=False):
 """
 edgefromnetworkconstruction + basic。

 Parameters:
 edges_df: pd.DataFrame — edge
 source_col: str — nodecolumn
 target_col: str — nodecolumn
 weight_col: str | None — column
 directed: bool — graph
 """
 if directed:
 G = nx.DiGraph
 else:
 G = nx.Graph

 for _, row in edges_df.iterrows:
 kwargs = {}
 if weight_col and pd.notna(row[weight_col]):
 kwargs["weight"] = row[weight_col]
 G.add_edge(row[source_col], row[target_col], **kwargs)

 stats = {
 "n_nodes": G.number_of_nodes,
 "n_edges": G.number_of_edges,
 "density": nx.density(G),
 "is_connected": nx.is_connected(G) if not directed else nx.is_weakly_connected(G),
 "n_components": nx.number_connected_components(G) if not directed
 else nx.number_weakly_connected_components(G),
 "avg_degree": np.mean([d for _, d in G.degree]),
 "avg_clustering": nx.average_clustering(G) if not directed else None,
 }

 if stats["is_connected"] and not directed:
 stats["avg_path_length"] = nx.average_shortest_path_length(G)
 stats["diameter"] = nx.diameter(G)

 print(f"Network: {stats['n_nodes']} nodes, {stats['n_edges']} edges, "
 f"density={stats['density']:.4f}")
 return G, stats


def build_network_from_correlation(df, threshold=0.5,
 method="pearson"):
 """
 correlationfromnetworkconstruction。

 Parameters:
 df: pd.DataFrame — number/countvaluedata
 threshold: float — correlationthreshold (|r| ≥ threshold edge)
 method: str — "pearson" / "spearman"
 """
 corr = df.corr(method=method)
 G = nx.Graph

 for i, col_i in enumerate(corr.columns):
 G.add_node(col_i)
 for j, col_j in enumerate(corr.columns):
 if i < j and abs(corr.iloc[i, j]) >= threshold:
 G.add_edge(col_i, col_j,
 weight=abs(corr.iloc[i, j]),
 correlation=corr.iloc[i, j])

 print(f"Correlation Network (|r|≥{threshold}): "
 f"{G.number_of_nodes} nodes, {G.number_of_edges} edges")
 return G
```

## 2. 

```python
def detect_communities(G, method="louvain", resolution=1.0):
 """
 。

 Parameters:
 G: nx.Graph — network
 method: str — "louvain" / "leiden" / "label_propagation" / "girvan_newman"
 resolution: float — degreeparameters (Louvain/Leiden)
 """
 import matplotlib.pyplot as plt

 if method == "louvain":
 communities = nx.community.louvain_communities(
 G, resolution=resolution, seed=42)
 elif method == "leiden":
 try:
 import leidenalg
 import igraph as ig
 ig_graph = ig.Graph.from_networkx(G)
 partition = leidenalg.find_partition(
 ig_graph, leidenalg.RBConfigurationVertexPartition,
 resolution_parameter=resolution, seed=42)
 communities = [set(ig_graph.vs[c]["_nx_name"] for c in comm)
 for comm in partition]
 except ImportError:
 communities = nx.community.louvain_communities(
 G, resolution=resolution, seed=42)
 elif method == "label_propagation":
 communities = list(nx.community.label_propagation_communities(G))
 elif method == "girvan_newman":
 comp = nx.community.girvan_newman(G)
 communities = next(comp) # 's min

 # node ID 
 node_community = {}
 for i, comm in enumerate(communities):
 for node in comm:
 node_community[node] = i
 nx.set_node_attributes(G, node_community, "community")

 # 
 modularity = nx.community.modularity(G, communities)

 # visualization
 fig, ax = plt.subplots(figsize=(12, 10))
 pos = nx.spring_layout(G, k=1/np.sqrt(G.number_of_nodes), seed=42)
 colors = [node_community.get(n, 0) for n in G.nodes]

 nx.draw_networkx(G, pos, ax=ax, node_color=colors,
 cmap=plt.cm.Set3, node_size=100,
 font_size=6, edge_color="gray", alpha=0.7,
 with_labels=G.number_of_nodes < 100)
 ax.set_title(f"Communities ({method}): {len(communities)} clusters, "
 f"Q={modularity:.4f}")
 plt.tight_layout

 path = "network_communities.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 print(f"Communities ({method}): {len(communities)} clusters, "
 f"modularity={modularity:.4f}")
 return {"communities": communities, "modularity": modularity,
 "node_community": node_community, "fig": path}
```

## 3. 

```python
def centrality_analysis(G, top_n=20):
 """
 surfaceanalysis。

 Parameters:
 G: nx.Graph — network
 top_n: int — topnodenumber/count
 """
 centralities = {
 "degree": nx.degree_centrality(G),
 "betweenness": nx.betweenness_centrality(G),
 "closeness": nx.closeness_centrality(G),
 "eigenvector": nx.eigenvector_centrality(G, max_iter=1000),
 "pagerank": nx.pagerank(G)
 }

 # DataFrame 
 cent_df = pd.DataFrame(centralities)
 cent_df.index.name = "node"

 # 
 rankings = {}
 for metric in centralities:
 top = cent_df[metric].nlargest(top_n)
 rankings[metric] = top.index.tolist

 # (multiple'sintegration)
 for metric in centralities:
 cent_df[f"{metric}_rank"] = cent_df[metric].rank(ascending=False)
 cent_df["hub_score"] = cent_df[[f"{m}_rank" for m in centralities]].mean(axis=1)
 cent_df = cent_df.sort_values("hub_score")

 print(f"Centrality: {len(G.nodes)} nodes analyzed")
 print(f" Top hubs: {cent_df.head(5).index.tolist}")
 return {"centrality_df": cent_df, "rankings": rankings}
```

## 4. PyVis visualization

```python
def interactive_network(G, output="network_interactive.html",
 height="700px", width="100%"):
 """
 PyVis networkfigure。

 Parameters:
 G: nx.Graph — network
 output: str — output HTML 
 height: str — 
 width: str — 
 """
 from pyvis.network import Network

 nt = Network(height=height, width=width, notebook=False,
 bgcolor="#ffffff", font_color="black")

 # color
 community_map = nx.get_node_attributes(G, "community")
 colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
 "#ff7f00", "#ffff33", "#a65628", "#f781bf"]

 for node in G.nodes:
 comm = community_map.get(node, 0)
 degree = G.degree(node)
 nt.add_node(str(node), label=str(node),
 color=colors[comm % len(colors)],
 size=max(5, min(degree * 3, 50)),
 title=f"{node}\nDegree: {degree}\nCommunity: {comm}")

 for u, v, data in G.edges(data=True):
 weight = data.get("weight", 1)
 nt.add_edge(str(u), str(v), value=weight)

 nt.toggle_physics(True)
 nt.show_buttons(filter_=["physics"])
 nt.save_graph(output)

 print(f"Interactive Network → {output} "
 f"({G.number_of_nodes} nodes, {G.number_of_edges} edges)")
 return output
```

---

## Pipeline Integration

```
eda-correlation → network-visualization → advanced-visualization
 (correlationanalysis) (networkanalysis) (advancedvisualization)
 │ │ ↓
 graph-neural-networks ───┘ interactive-dashboard
 (GNN) (dashboard)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `network_communities.png` | structure | → presentation |
| `centrality_analysis.csv` | | → feature-importance |
| `network_interactive.html` | PyVis figure | → dashboard |

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

### Eval Criteria (Visualization)

Before execution, define:
- [ ] **Target audience**: journal / conference / dashboard / internal
- [ ] **Figure dimensions**: width x height, DPI requirement
- [ ] **Color scheme**: colorblind-safe palette confirmed
- [ ] **Data-ink ratio**: minimize non-data elements

#### Pass Criteria
- All figures saved to disk (never plt.show())
- Figures embedded in report.md with captions
- Text is English-only, font size >= 8pt
- Accessibility: contrast ratio >= 4.5:1
- Vector format (SVG/PDF) provided when requested
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
