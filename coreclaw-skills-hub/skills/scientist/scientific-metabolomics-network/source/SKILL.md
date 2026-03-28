---
name: scientific-metabolomics-network
description: |
 Metabolomics network skill. Metabolite correlation networks, pathway-level network analysis, metabolite-gene interaction mapping, and multi-omics network integration.
tu_tools:
 - key: hmdb
 name: HMDB
 description: metabolitenetworkmetabolic pathway search
---

# Scientific Metabolomics Network

KEGG/Reactome metabolismpathwayfrom's networkconstruction、
metabolitecorrelationanalysis (Gaussian Graphical Model / WGCNA)、
metabolite、MetaboAnalyst integration's
pipeline.

## When to Use

- metabolitecorrelationnetwork (partial correlation) is builtand
- KEGG/Reactome metabolismpathwaygraphwhen needed
- metabolite (degree) when needed
- metabolismpathwayanalysis is performedand
- metabolomedata's networkvisualization

---

## Quick Start

## 1. metabolitecorrelationnetwork

```python
import numpy as np
import pandas as pd
import networkx as nx
from sklearn.covariance import GraphicalLassoCV


def metabolite_correlation_network(
 data, method="glasso", threshold=0.1):
 """
 metabolitecorrelationnetworkconstruction。

 Parameters:
 data: pd.DataFrame — metabolite concentration matrix
 (=, =metabolite)
 method: str — "glasso" (Graphical Lasso) or
 "pearson" (Pearson partial)
 threshold: float — edgethreshold
 """
 metabolites = data.columns.tolist

 if method == "glasso":
 model = GraphicalLassoCV(cv=5)
 model.fit(data.values)
 precision = model.precision_
 # Partial correlation from precision matrix
 diag = np.sqrt(np.diag(precision))
 partial_corr = -(precision /
 np.outer(diag, diag))
 np.fill_diagonal(partial_corr, 1.0)
 else:
 partial_corr = data.corr.values

 # Build network
 G = nx.Graph
 G.add_nodes_from(metabolites)

 for i in range(len(metabolites)):
 for j in range(i + 1, len(metabolites)):
 w = abs(partial_corr[i, j])
 if w > threshold:
 G.add_edge(
 metabolites[i],
 metabolites[j],
 weight=round(w, 4),
 sign=("+" if partial_corr[i, j]
 > 0 else "-"))

 print(f"Metabolite network: "
 f"{G.number_of_nodes} nodes, "
 f"{G.number_of_edges} edges "
 f"(threshold={threshold})")
 return G


def hub_metabolites(G, top_n=10):
 """
 metabolite (number/count) 。

 Parameters:
 G: nx.Graph — metabolitenetwork
 top_n: int — top count
 """
 degree_cent = nx.degree_centrality(G)
 betweenness = nx.betweenness_centrality(G)

 rows = []
 for node in G.nodes:
 rows.append({
 "metabolite": node,
 "degree": G.degree(node),
 "degree_centrality": round(
 degree_cent[node], 4),
 "betweenness": round(
 betweenness[node], 4),
 })

 df = pd.DataFrame(rows).sort_values(
 "degree_centrality",
 ascending=False).head(top_n)
 print(f"Top {top_n} hub metabolites:")
 for _, row in df.iterrows:
 print(f" {row['metabolite']}: "
 f"deg={row['degree']}, "
 f"bc={row['betweenness']}")
 return df
```

## 2. KEGG metabolismpathwaygraph

```python
def kegg_pathway_graph(pathway_id):
 """
 KEGG — metabolismpathway networkgraphasretrieval。

 Parameters:
 pathway_id: str — KEGG pathway ID
 (example: "hsa00010")
 """
 import requests

 # KGML retrieval
 url = (f"https://rest.kegg.jp/get/"
 f"{pathway_id}/kgml")
 resp = requests.get(url, timeout=30)
 resp.raise_for_status

 import xml.etree.ElementTree as ET
 root = ET.fromstring(resp.text)

 G = nx.DiGraph

 # nodeaddition
 entry_map = {}
 for entry in root.findall("entry"):
 eid = entry.get("id")
 name = entry.get("name", "")
 etype = entry.get("type", "")
 graphics = entry.find("graphics")
 label = (graphics.get("name", name)
 if graphics is not None else name)
 entry_map[eid] = label
 G.add_node(label, entry_type=etype)

 # edgeaddition
 for relation in root.findall("relation"):
 e1 = relation.get("entry1")
 e2 = relation.get("entry2")
 rtype = relation.get("type", "")
 if e1 in entry_map and e2 in entry_map:
 G.add_edge(entry_map[e1],
 entry_map[e2],
 relation_type=rtype)

 for reaction in root.findall("reaction"):
 rname = reaction.get("name", "")
 substrates = [s.get("name", "")
 for s in reaction.findall(
 "substrate")]
 products = [p.get("name", "")
 for p in reaction.findall(
 "product")]
 for s in substrates:
 for p in products:
 G.add_edge(s, p,
 reaction=rname)

 print(f"KEGG pathway {pathway_id}: "
 f"{G.number_of_nodes} nodes, "
 f"{G.number_of_edges} edges")
 return G
```

## 3. pathway

```python
def metabolite_pathway_enrichment(
 metabolite_list, organism="hsa"):
 """
 metabolitepathway (KEGG)。

 Parameters:
 metabolite_list: list[str] — KEGG compound ID
 (example: ["C00031", "C00158"])
 organism: str — organism/species
 """
 import requests
 from scipy.stats import hypergeom

 # KEGG compound→pathway mapping
 url = "https://rest.kegg.jp/link/pathway/compound"
 resp = requests.get(url, timeout=30)
 resp.raise_for_status

 cpd_to_pw = {}
 pw_to_cpd = {}
 for line in resp.text.strip.split("\n"):
 if not line:
 continue
 parts = line.split("\t")
 if len(parts) != 2:
 continue
 cpd = parts[0].replace("cpd:", "")
 pw = parts[1].replace("path:", "")
 if not pw.startswith("map"):
 continue
 cpd_to_pw.setdefault(cpd, set).add(pw)
 pw_to_cpd.setdefault(pw, set).add(cpd)

 # calculation
 query_set = set(metabolite_list)
 all_cpds = set(cpd_to_pw.keys)
 M = len(all_cpds)
 n = len(query_set & all_cpds)

 results = []
 for pw, pw_cpds in pw_to_cpd.items:
 N = len(pw_cpds)
 k = len(query_set & pw_cpds)
 if k == 0:
 continue
 pval = hypergeom.sf(k - 1, M, N, n)
 results.append({
 "pathway": pw,
 "overlap": k,
 "pathway_size": N,
 "pvalue": pval,
 "metabolites": ", ".join(
 query_set & pw_cpds),
 })

 df = pd.DataFrame(results).sort_values("pvalue")
 print(f"Pathway enrichment: "
 f"{len(df)} pathways (p<0.05: "
 f"{(df['pvalue'] < 0.05).sum})")
 return df
```

## 4. metabolismnetworkintegrationpipeline

```python
def metabolomics_network_pipeline(
 data, metabolite_ids=None,
 output_dir="results"):
 """
 metabolismnetworkintegrationpipeline。

 Parameters:
 data: pd.DataFrame — metabolite concentration matrix
 metabolite_ids: list[str] | None — KEGG
 compound ID (for)
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) correlationnetwork
 G = metabolite_correlation_network(data)
 nx.write_graphml(
 G, str(output_dir / "metabolite_network.graphml"))

 # 2) metabolite
 hubs = hub_metabolites(G)
 hubs.to_csv(
 output_dir / "hub_metabolites.csv",
 index=False)

 # 3) pathway
 if metabolite_ids:
 enrich = metabolite_pathway_enrichment(
 metabolite_ids)
 enrich.to_csv(
 output_dir / "pathway_enrichment.csv",
 index=False)

 print(f"Metabolomics network pipeline → "
 f"{output_dir}")
 return {"network": G, "hubs": hubs}
```

---

## Pipeline Integration

```
metabolomics → metabolomics-network → pathway-enrichment
 (LC-MS/NMR) (GGM/graphconstruction) (KEGG/Reactome)
 │ │ ↓
 lipidomics ────────────┘ systems-biology
 (lipid) (multi-omics integration)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/metabolite_network.graphml` | correlationnetwork | → systems-biology |
| `results/hub_metabolites.csv` | metabolite | → biomarker-discovery |
| `results/pathway_enrichment.csv` | pathway | → pathway-enrichment |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `hmdb` | HMDB | metabolitenetworkmetabolic pathway search |

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
