---
name: scientific-metabolic-atlas
description: |
 Metabolic atlas skill. Genome-scale metabolic model queries, metabolic pathway visualization, flux balance analysis results, and cross-species metabolic comparison.
tu_tools: []
kdense_ref: metabolic-atlas
tu_tools:
 - key: metabolic_atlas
 name: Metabolic Atlas
 description: genomemetabolismsearch
---

# Scientific Metabolic Atlas

Metabolic Atlas REST API utilizinggenomemetabolism
(GEM) analysispipeline is provided。

## When to Use

- metabolismreactionmetabolism is searchedand
- Human-GEM 's information is retrievedand
- metabolic pathway's networkstructureanalysiswhen needed
- analysis (FBA) 's inputwhen needed
- metabolismvisualizationwhen needed
- tissuemetabolism is builtand

---

## Quick Start

## 1. metabolismreactionsearch

```python
import requests
import pandas as pd
import numpy as np

MA_BASE = "https://metabolicatlas.org/api/v2"


def metabolic_atlas_search_reactions(query, model="Human-GEM",
 compartment=None, limit=50):
 """
 Metabolic Atlas — metabolismreactionsearch。

 Parameters:
 query: str — search query (example: "glycolysis", "citrate")
 model: str — GEM model name
 compartment: str — (example: "cytosol", "mitochondria")
 limit: int — maximum results
 """
 url = f"{MA_BASE}/search"
 params = {
 "query": query,
 "model": model,
 "type": "reaction",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for r in data.get("results", data) if isinstance(data, dict) else data:
 rxn = r if isinstance(r, dict) else {}
 row = {
 "reaction_id": rxn.get("id", ""),
 "name": rxn.get("name", ""),
 "equation": rxn.get("equation", ""),
 "subsystem": rxn.get("subsystem", ""),
 "compartment": rxn.get("compartment", ""),
 "gene_rule": rxn.get("geneRule", ""),
 "lower_bound": rxn.get("lowerBound", None),
 "upper_bound": rxn.get("upperBound", None),
 }
 if compartment and compartment.lower not in str(
 row.get("compartment", "")).lower:
 continue
 results.append(row)

 df = pd.DataFrame(results[:limit])
 print(f"Metabolic Atlas reactions: {len(df)} results "
 f"(query={query})")
 return df
```

## 2. metabolismsearch

```python
def metabolic_atlas_search_metabolites(query, model="Human-GEM",
 limit=50):
 """
 Metabolic Atlas — metabolismsearch。

 Parameters:
 query: str — search query (example: "glucose", "ATP")
 model: str — GEM model name
 limit: int — maximum results
 """
 url = f"{MA_BASE}/search"
 params = {
 "query": query,
 "model": model,
 "type": "metabolite",
 "limit": limit,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for m in data.get("results", data) if isinstance(data, dict) else data:
 met = m if isinstance(m, dict) else {}
 results.append({
 "metabolite_id": met.get("id", ""),
 "name": met.get("name", ""),
 "formula": met.get("formula", ""),
 "charge": met.get("charge", None),
 "compartment": met.get("compartment", ""),
 "chebi_id": met.get("chebiId", ""),
 "kegg_id": met.get("keggId", ""),
 })

 df = pd.DataFrame(results[:limit])
 print(f"Metabolic Atlas metabolites: {len(df)} results "
 f"(query={query})")
 return df
```

## 3. metabolismnetworkanalysis

```python
import networkx as nx


def metabolic_atlas_network(subsystem, model="Human-GEM"):
 """
 Metabolic Atlas — metabolismnetworkconstruction。

 Parameters:
 subsystem: str — (example: "Glycolysis")
 model: str — GEM model name
 """
 reactions = metabolic_atlas_search_reactions(
 subsystem, model=model, limit=200)

 G = nx.DiGraph

 for _, rxn in reactions.iterrows:
 rxn_id = rxn["reaction_id"]
 equation = str(rxn.get("equation", ""))

 # : "A + B => C + D"
 if "=>" in equation:
 substrates_str, products_str = equation.split("=>", 1)
 elif "=" in equation:
 substrates_str, products_str = equation.split("=", 1)
 else:
 continue

 substrates = [s.strip for s in substrates_str.split("+")
 if s.strip]
 products = [p.strip for p in products_str.split("+")
 if p.strip]

 G.add_node(rxn_id, type="reaction",
 name=rxn.get("name", ""))

 for s in substrates:
 G.add_node(s, type="metabolite")
 G.add_edge(s, rxn_id)

 for p in products:
 G.add_node(p, type="metabolite")
 G.add_edge(rxn_id, p)

 # network
 n_reactions = sum(1 for _, d in G.nodes(data=True)
 if d.get("type") == "reaction")
 n_metabolites = sum(1 for _, d in G.nodes(data=True)
 if d.get("type") == "metabolite")

 print(f"Metabolic network: {n_reactions} reactions, "
 f"{n_metabolites} metabolites, {G.number_of_edges} edges")
 return G
```

## 4. metabolismintegrationpipeline

```python
def metabolic_atlas_pipeline(query, model="Human-GEM",
 output_dir="results"):
 """
 metabolismintegrationpipeline。

 Parameters:
 query: str — metabolic pathway/
 model: str — GEM model name
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) reactionsearch
 reactions = metabolic_atlas_search_reactions(query, model=model)
 reactions.to_csv(output_dir / "reactions.csv", index=False)

 # 2) metabolismsearch
 metabolites = metabolic_atlas_search_metabolites(query, model=model)
 metabolites.to_csv(output_dir / "metabolites.csv", index=False)

 # 3) networkconstruction
 G = metabolic_atlas_network(query, model=model)
 nx.write_graphml(G, str(output_dir / "metabolic_network.graphml"))

 # 4) metabolism
 met_nodes = [n for n, d in G.nodes(data=True)
 if d.get("type") == "metabolite"]
 hub_scores = {n: G.degree(n) for n in met_nodes}
 hub_df = pd.DataFrame([
 {"metabolite": k, "degree": v}
 for k, v in sorted(hub_scores.items,
 key=lambda x: -x[1])[:20]
 ])
 hub_df.to_csv(output_dir / "hub_metabolites.csv", index=False)

 print(f"Metabolic Atlas pipeline: {output_dir}")
 return {
 "reactions": reactions,
 "metabolites": metabolites,
 "network": G,
 "hubs": hub_df,
 }
```

---

## K-Dense Integration

| K-Dense Key | Reference |
|-------------|---------|
| `metabolic-atlas` | metabolismstructurereactiondatabase |

## Pipeline Integration

```
metabolic-modeling → metabolic-atlas → systems-biology
 (COBRA/FBA) (Human-GEM) (integration)
 │ │ ↓
 pathway-enrichment ─────┘ gene-expression
 (KEGG/Reactome) │ (expressiondata)
 ↓
 multi-omics
 (integration)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/reactions.csv` | metabolismreactionlist | → metabolic-modeling |
| `results/metabolites.csv` | metabolismlist | → pathway-enrichment |
| `results/metabolic_network.graphml` | metabolismnetwork | → systems-biology |
| `results/hub_metabolites.csv` | metabolism | → multi-omics |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `metabolic_atlas` | Metabolic Atlas | genomemetabolismsearch |

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
