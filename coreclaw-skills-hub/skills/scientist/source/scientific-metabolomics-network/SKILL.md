---
name: scientific-metabolomics-network
description: |
 metabolitenetworkconstructionskill。KEGG/Reactome metabolismpathway
 graphextractionmetabolitecorrelationnetworkconstruction (GGM/WGCNA)
 metaboliteMetaboAnalyst integration
 pipeline。
 TU skill ( Python library + REST API)。
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

## Harness Optimization (v0.4.0)

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
