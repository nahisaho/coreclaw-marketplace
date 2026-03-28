---
name: scientific-protein-interaction-network
description: |
 Protein interaction network skill. STRING/BioGRID PPI data integration, interaction confidence scoring, network topology analysis, and protein complex identification.
---

# Scientific Protein Interaction Network

STRING / IntAct / BioGRID / STITCH 's 4 PPI databaseintegration
proteininteractionnetworkanalysispipeline is provided。

## When to Use

- DEG and variant/mutationgene's PPI network is builtand
- protein and 'swhen needed
- compoundand protein'sinteraction is investigatedand
- tissueinteractionnetwork is evaluatedand
- PPI data-based GO/KEGG andmoduleanalysis is performedand

---

## Quick Start

## 1. STRING PPI networkretrieval

```python
import requests
import pandas as pd
import networkx as nx


def string_get_interactions(proteins, species=9606,
 score_threshold=400,
 network_type="functional"):
 """
 STRING API v12 by/via PPI networkretrieval。

 Parameters:
 proteins: list — protein/UniProt ID 
 species: int — NCBI Taxonomy ID (9606=Homo sapiens)
 score_threshold: int — threshold (0-1000)
 network_type: "functional" or "physical"
 """
 base = "https://string-db.org/api/json"

 # protein ID 
 resolve_url = f"{base}/get_string_ids"
 resolved = []
 for batch in [proteins[i:i+10] for i in range(0, len(proteins), 10)]:
 params = {
 "identifiers": "\r".join(batch),
 "species": species,
 "limit": 1,
 }
 resp = requests.get(resolve_url, params=params)
 for r in resp.json:
 resolved.append(r["stringId"])

 if not resolved:
 print("No proteins resolved")
 return pd.DataFrame, nx.Graph

 # interactionretrieval
 interaction_url = f"{base}/network"
 params = {
 "identifiers": "\r".join(resolved),
 "species": species,
 "required_score": score_threshold,
 "network_type": network_type,
 }
 resp = requests.get(interaction_url, params=params)
 interactions = resp.json

 edges = []
 for i in interactions:
 edges.append({
 "protein_a": i["preferredName_A"],
 "protein_b": i["preferredName_B"],
 "score": i["score"],
 "nscore": i.get("nscore", 0),
 "fscore": i.get("fscore", 0),
 "pscore": i.get("pscore", 0),
 "ascore": i.get("ascore", 0),
 "escore": i.get("escore", 0),
 "dscore": i.get("dscore", 0),
 "tscore": i.get("tscore", 0),
 })

 df = pd.DataFrame(edges)

 # NetworkX graphconstruction
 G = nx.Graph
 for _, row in df.iterrows:
 G.add_edge(row["protein_a"], row["protein_b"],
 weight=row["score"] / 1000.0)

 print(f"STRING network: {G.number_of_nodes} nodes, "
 f"{G.number_of_edges} edges (score ≥ {score_threshold})")
 return df, G
```

## 2. IntAct molecular interaction search

```python
def intact_search_interactions(query, species="human",
 interaction_type=None,
 max_results=200):
 """
 IntAct REST API by/viamolecular interaction search。

 Parameters:
 query: str — protein/UniProt ID
 species: str or int — "human" or taxonomy ID
 interaction_type: str — MI term (e.g., "MI:0407" physical association)
 """
 url = "https://www.ebi.ac.uk/intact/ws/interaction/findInteractions"
 params = {
 "query": query,
 "maxResults": max_results,
 }
 if species:
 params["species"] = species

 resp = requests.get(url, params=params)
 if resp.status_code != 200:
 print(f"IntAct error: {resp.status_code}")
 return pd.DataFrame

 data = resp.json
 interactions = data.get("content", [])

 results = []
 for ix in interactions:
 interactor_a = ix.get("interactorA", {})
 interactor_b = ix.get("interactorB", {})
 results.append({
 "interactor_a": interactor_a.get("preferredIdentifier", ""),
 "interactor_a_name": interactor_a.get("shortLabel", ""),
 "interactor_b": interactor_b.get("preferredIdentifier", ""),
 "interactor_b_name": interactor_b.get("shortLabel", ""),
 "interaction_type": ix.get("interactionType", ""),
 "detection_method": ix.get("detectionMethod", ""),
 "confidence": ix.get("confidenceValue", 0),
 "publication": ix.get("pubmedId", ""),
 })

 df = pd.DataFrame(results)
 print(f"IntAct: {len(df)} interactions for '{query}'")
 return df
```

## 3. STITCH compound-proteininteraction

```python
def stitch_chemical_protein(chemicals, species=9606,
 score_threshold=400):
 """
 STITCH API by/viacompound-proteininteractionsearch。

 Parameters:
 chemicals: list — compound/CID 
 species: int — NCBI Taxonomy ID
 score_threshold: int — threshold
 """
 url = "http://stitch.embl.de/api/json/interactionsList"
 params = {
 "identifiers": "\r".join(chemicals),
 "species": species,
 "required_score": score_threshold,
 }

 resp = requests.get(url, params=params)
 interactions = resp.json

 results = []
 for i in interactions:
 results.append({
 "chemical": i.get("preferredName_A", ""),
 "protein": i.get("preferredName_B", ""),
 "score": i.get("score", 0),
 "type_a": "chemical" if i.get("ncbiTaxonId_A") == -1 else "protein",
 })

 df = pd.DataFrame(results)
 print(f"STITCH: {len(df)} chemical-protein interactions")
 return df
```

## 4. PPI networkanalysis (module)

```python
def analyze_ppi_network(G, community_method="louvain"):
 """
 PPI network'sanalysis。

 Parameters:
 G: nx.Graph — PPI network
 community_method: "louvain" or "label_propagation"
 """
 if G.number_of_nodes == 0:
 return {}

 # 
 degree_cent = nx.degree_centrality(G)
 betweenness = nx.betweenness_centrality(G)
 closeness = nx.closeness_centrality(G)

 # protein (degree top 10)
 hubs = sorted(degree_cent.items, key=lambda x: -x[1])[:10]

 # (betweenness top 10)
 bottlenecks = sorted(betweenness.items, key=lambda x: -x[1])[:10]

 # 
 if community_method == "louvain":
 from community import community_louvain
 partition = community_louvain.best_partition(G)
 else:
 communities = nx.community.label_propagation_communities(G)
 partition = {}
 for i, comm in enumerate(communities):
 for node in comm:
 partition[node] = i

 n_communities = len(set(partition.values))

 stats = {
 "nodes": G.number_of_nodes,
 "edges": G.number_of_edges,
 "density": round(nx.density(G), 4),
 "avg_clustering": round(nx.average_clustering(G), 4),
 "connected_components": nx.number_connected_components(G),
 "communities": n_communities,
 "hub_proteins": [h[0] for h in hubs],
 "bottleneck_proteins": [b[0] for b in bottlenecks],
 }

 centrality_df = pd.DataFrame({
 "protein": list(degree_cent.keys),
 "degree_centrality": list(degree_cent.values),
 "betweenness": [betweenness[n] for n in degree_cent.keys],
 "closeness": [closeness[n] for n in degree_cent.keys],
 "community": [partition.get(n, -1) for n in degree_cent.keys],
 }).sort_values("degree_centrality", ascending=False)

 print(f"PPI analysis: {stats['nodes']} nodes, {stats['edges']} edges, "
 f"{n_communities} communities")
 return stats, centrality_df, partition
```

## 5. PPI networkvisualization

```python
def visualize_ppi_network(G, partition=None, hub_proteins=None,
 output="figures/ppi_network.png",
 layout="spring"):
 """
 PPI network's visualization。
 """
 import matplotlib.pyplot as plt
 import os
 os.makedirs(os.path.dirname(output), exist_ok=True)

 fig, ax = plt.subplots(figsize=(14, 14))

 if layout == "spring":
 pos = nx.spring_layout(G, k=1.5, seed=42)
 elif layout == "kamada_kawai":
 pos = nx.kamada_kawai_layout(G)

 # node = number/count
 node_sizes = [300 + 100 * G.degree(n) for n in G.nodes]

 # color
 if partition:
 import matplotlib.cm as cm
 n_comm = len(set(partition.values))
 colors = [cm.Set3(partition.get(n, 0) / max(n_comm, 1)) for n in G.nodes]
 else:
 colors = "steelblue"

 nx.draw_networkx_edges(G, pos, alpha=0.2, ax=ax)
 nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
 node_color=colors, alpha=0.8, ax=ax)

 # protein'slabel
 if hub_proteins:
 labels = {n: n for n in G.nodes if n in hub_proteins}
 else:
 labels = {n: n for n in G.nodes if G.degree(n) >= 5}
 nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)

 ax.set_title(f"PPI Network ({G.number_of_nodes} proteins, "
 f"{G.number_of_edges} interactions)")
 ax.axis("off")
 plt.tight_layout
 plt.savefig(output, dpi=300, bbox_inches="tight")
 plt.close
 print(f"Saved: {output}")
```

## References

### Output Files

| File | Format |
|---|---|
| `results/string_interactions.csv` | CSV |
| `results/intact_interactions.csv` | CSV |
| `results/stitch_interactions.csv` | CSV |
| `results/ppi_centrality.csv` | CSV |
| `results/ppi_network.graphml` | GraphML |
| `figures/ppi_network.png` | PNG |

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

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-drug-target-profiling` | protein → PPI |
| `scientific-network-analysis` | fornetworkanalysismethod |
| `scientific-pathway-enrichment` | PPI module → pathway |
| `scientific-protein-structure-analysis` | structureinformation → interactionsurface |
| `scientific-systems-biology` | GRN ↔ PPI integration |

### Dependencies

`networkx`, `requests`, `pandas`, `matplotlib`, `python-louvain` (community)
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
