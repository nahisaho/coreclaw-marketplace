---
name: scientific-string-network-api
description: |
 STRING/BioGRID/STITCH networkanalysisskill。STRING proteininteraction
 network API、BioGRID experiment PPI、STITCH -proteinnetwork、
 networkanalysisintegrationpipeline。
tu_tools:
 - key: ppi
 name: STRING/BioGRID PPI
 description: proteininteractionnetwork
---

# Scientific STRING Network API

STRING v12 / BioGRID / STITCH API utilizing PPIcompound-protein
networkanalysispipeline is provided。existing's protein-interaction-network
skill (IntAct/HumanBase) 、STRING API 's advanced
networkminintegration。

## When to Use

- STRING API proteininteractionnetworkconstructionwhen needed
- BioGRID fromexperiment's PPI is retrievedand
- STITCH compound-proteinnetwork is searchedand
- network (number/countdistribution) calculationwhen needed
- PPI network is performedand
- analysis (STRING enrichment) networkwhen needed

---

## Quick Start

## 1. STRING PPI networkretrieval

```python
import requests
import pandas as pd
import networkx as nx

STRING_API = "https://string-db.org/api"
OUTPUT_FORMAT = "json"


def get_string_network(proteins, species=9606, score_threshold=400,
 network_type="functional", limit=50):
 """
 STRING PPI networkretrieval。

 Parameters:
 proteins: list — protein (example: ["TP53", "MDM2", "BRCA1"])
 species: int — NCBI Taxonomy ID (9606=human)
 score_threshold: int — threshold (0-1000)
 network_type: str — "functional" or "physical"
 limit: int — interactor number/count

 ToolUniverse:
 STRING_get_protein_interactions(
 protein_ids=proteins, species=species,
 confidence_score=score_threshold/1000,
 network_type=network_type, limit=limit
 )
 """
 url = f"{STRING_API}/{OUTPUT_FORMAT}/network"
 params = {
 "identifiers": "\r".join(proteins),
 "species": species,
 "required_score": score_threshold,
 "network_type": network_type,
 "limit": limit,
 }

 resp = requests.post(url, data=params)
 resp.raise_for_status
 interactions = resp.json

 rows = []
 for i in interactions:
 rows.append({
 "protein_a": i.get("preferredName_A"),
 "protein_b": i.get("preferredName_B"),
 "combined_score": i.get("score"),
 "nscore": i.get("nscore"),
 "fscore": i.get("fscore"),
 "pscore": i.get("pscore"),
 "ascore": i.get("ascore"),
 "escore": i.get("escore"),
 "dscore": i.get("dscore"),
 "tscore": i.get("tscore"),
 })

 df = pd.DataFrame(rows)
 print(f"STRING network: {len(df)} interactions "
 f"(score ≥ {score_threshold/1000})")
 return df
```

## 2. BioGRID experiment PPI retrieval

```python
def get_biogrid_interactions(genes, organism=9606, evidence_type=None,
 api_key="YOUR_KEY", limit=500):
 """
 BioGRID experiment PPI Data Retrieval。

 Parameters:
 genes: list — gene name
 organism: int — NCBI Taxonomy ID
 evidence_type: str — "physical" or "genetic"
 api_key: str — BioGRID API key (https://webservice.thebiogrid.org)
 limit: int — maximum retrieval count

 ToolUniverse:
 BioGRID_get_interactions(
 gene_names=genes, organism=organism,
 interaction_type=evidence_type, limit=limit
 )
 """
 url = "https://webservice.thebiogrid.org/interactions"
 params = {
 "accessKey": api_key,
 "geneList": "|".join(genes),
 "organism": organism,
 "format": "json",
 "max": limit,
 "searchNames": "true",
 "includeInteractors": "true",
 }
 if evidence_type:
 params["interSpeciesExcluded"] = "true"

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 rows = []
 for _, interaction in data.items:
 rows.append({
 "gene_a": interaction.get("OFFICIAL_SYMBOL_A"),
 "gene_b": interaction.get("OFFICIAL_SYMBOL_B"),
 "experimental_system": interaction.get("EXPERIMENTAL_SYSTEM"),
 "throughput": interaction.get("THROUGHPUT"),
 "pubmed_id": interaction.get("PUBMED_ID"),
 "source_db": "BioGRID",
 })

 df = pd.DataFrame(rows)
 print(f"BioGRID: {len(df)} interactions for {genes}")
 return df
```

## 3. STITCH compound-proteinnetwork

```python
def get_stitch_interactions(identifiers, species=9606, score=400, limit=20):
 """
 STITCH compound-proteininteractionretrieval。

 Parameters:
 identifiers: list — CID (compound) orgene name
 species: int — NCBI Taxonomy ID
 score: int — threshold
 limit: int — maximum results

 ToolUniverse:
 STITCH_get_chemical_protein_interactions(
 identifiers=identifiers, species=species,
 required_score=score, limit=limit
 )
 STITCH_get_interaction_partners(identifiers=identifiers)
 STITCH_resolve_identifier(identifiers=identifiers)
 """
 url = f"https://stitch.embl.de/api/{OUTPUT_FORMAT}/interactionsList"
 params = {
 "identifiers": "\r".join(identifiers),
 "species": species,
 "required_score": score,
 "limit": limit,
 }

 resp = requests.post(url, data=params)
 resp.raise_for_status
 interactions = resp.json

 rows = []
 for i in interactions:
 rows.append({
 "interactor_a": i.get("preferredName_A", i.get("stringId_A")),
 "interactor_b": i.get("preferredName_B", i.get("stringId_B")),
 "combined_score": i.get("score"),
 "is_chemical": "CID" in str(i.get("stringId_A", ""))
 or "CID" in str(i.get("stringId_B", "")),
 })

 df = pd.DataFrame(rows)
 print(f"STITCH: {len(df)} chemical-protein interactions")
 return df
```

## 4. networkconstruction & analysis

```python
def build_network(interaction_df, source_col="protein_a", target_col="protein_b",
 weight_col="combined_score"):
 """
 NetworkX graphconstruction & analysis。

 Parameters:
 interaction_df: DataFrame — interactiondata
 source_col, target_col: str — nodecolumn
 weight_col: str — edgecolumn
 """
 G = nx.Graph
 for _, row in interaction_df.iterrows:
 G.add_edge(
 row[source_col], row[target_col],
 weight=row.get(weight_col, 1.0),
 )

 # 
 degree = dict(G.degree)
 betweenness = nx.betweenness_centrality(G)
 closeness = nx.closeness_centrality(G)
 clustering = nx.clustering(G)

 metrics = pd.DataFrame({
 "node": list(degree.keys),
 "degree": list(degree.values),
 "betweenness": [betweenness[n] for n in degree],
 "closeness": [closeness[n] for n in degree],
 "clustering": [clustering[n] for n in degree],
 }).sort_values("betweenness", ascending=False)

 print(f"Network: {G.number_of_nodes} nodes, "
 f"{G.number_of_edges} edges, "
 f"density={nx.density(G):.4f}")
 return G, metrics
```

## 5. 

```python
from networkx.algorithms.community import greedy_modularity_communities


def detect_communities(G, resolution=1.0):
 """
 network's (module) 。

 Parameters:
 G: nx.Graph — networkgraph
 resolution: float — degreeparameters
 """
 communities = list(greedy_modularity_communities(G, resolution=resolution))
 modularity = nx.algorithms.community.modularity(G, communities)

 comm_data = []
 for i, comm in enumerate(communities):
 for node in comm:
 comm_data.append({"node": node, "community": i})

 df = pd.DataFrame(comm_data)
 print(f"Communities: {len(communities)} detected, "
 f"modularity={modularity:.4f}")
 return df, modularity
```

## 6. STRING analysis

```python
def string_enrichment(proteins, species=9606):
 """
 STRING API analysis (GO/KEGG/Reactome/InterPro)。

 Parameters:
 proteins: list — protein
 species: int — NCBI Taxonomy ID
 """
 url = f"{STRING_API}/{OUTPUT_FORMAT}/enrichment"
 params = {
 "identifiers": "\r".join(proteins),
 "species": species,
 }

 resp = requests.post(url, data=params)
 resp.raise_for_status
 enrichment = resp.json

 rows = []
 for e in enrichment:
 rows.append({
 "category": e.get("category"),
 "term": e.get("term"),
 "description": e.get("description"),
 "p_value": e.get("p_value"),
 "fdr": e.get("fdr"),
 "number_of_genes": e.get("number_of_genes"),
 "input_genes": e.get("inputGenes", ""),
 })

 df = pd.DataFrame(rows)
 if not df.empty:
 df = df.sort_values("fdr")
 print(f"Enrichment: {len(df)} terms, "
 f"{df[df['fdr'] < 0.05].shape[0]} significant (FDR<0.05)")
 return df
```

## 7. integration PPI analysispipeline

```python
def integrated_ppi_pipeline(genes, species=9606, score=700):
 """
 STRING + BioGRID + STITCH integration PPI pipeline。

 Pipeline:
 STRING network → BioGRID validation → topology → communities →
 enrichment
 """
 # STRING network
 string_df = get_string_network(genes, species, score)

 # networkconstruction & 
 G, metrics = build_network(string_df)

 # 
 comm_df, modularity = detect_communities(G)

 # STRING analysis
 all_nodes = list(G.nodes)
 enrichment = string_enrichment(all_nodes[:500], species)

 result = {
 "n_nodes": G.number_of_nodes,
 "n_edges": G.number_of_edges,
 "density": round(nx.density(G), 4),
 "n_communities": comm_df["community"].nunique,
 "modularity": round(modularity, 4),
 "hub_genes": metrics.head(10)["node"].tolist,
 "n_enriched_terms": len(enrichment[enrichment["fdr"] < 0.05])
 if not enrichment.empty else 0,
 }

 print(f"\n=== Integrated PPI Pipeline ===")
 print(f"Nodes: {result['n_nodes']}, Edges: {result['n_edges']}")
 print(f"Hub genes: {', '.join(result['hub_genes'][:5])}")
 return result
```

---

## Pipeline Integration

```
drug-target-profiling → string-network-api → pathway-enrichment
  (STRING PPI construction) (GO/KEGG )
 │ │ ↓
protein-interaction ───┘ │ ontology-enrichment
 (IntAct/HumanBase) ↓ (EFO/Enrichr)
 network-analysis
 (existingskill)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/string_network.csv` | STRING PPI network | → network-analysis |
| `results/ppi_topology.csv` | | → drug-target-profiling |
| `results/ppi_communities.csv` | | → pathway-enrichment |
| `results/string_enrichment.csv` | results | → ontology-enrichment |

## usepossibletool (ToolUniverse SMCP)

| Tool Name | Usage |
|---------|------|
| `STRING_get_protein_interactions` | STRING PPI retrieval |
| `BioGRID_get_interactions` | BioGRID experiment PPI |
| `STITCH_get_chemical_protein_interactions` | STITCH compound-protein |
| `STITCH_get_interaction_partners` | STITCH interaction |
| `STITCH_resolve_identifier` | STITCH ID |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
