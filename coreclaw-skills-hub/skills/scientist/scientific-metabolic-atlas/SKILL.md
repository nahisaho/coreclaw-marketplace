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
