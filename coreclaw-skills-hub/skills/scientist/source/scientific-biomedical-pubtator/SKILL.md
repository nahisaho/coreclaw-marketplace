---
name: scientific-biomedical-pubtator
description: |
 skill。PubTator3 API by/via
 genediseasecompoundvariant/mutationtype's 、extraction、
 literatureannotationautomatedpipeline。
---

# Scientific Biomedical PubTator

PubTator3 API utilizingliterature
extractionpipeline is provided。

## When to Use

- PubMed paperfromgenediseasecompound'sautomatedextractionwhen needed
- NER (Named Entity Recognition) is executedand
- gene-diseasedrug-'sliteraturefromextractionwhen needed
- large-scaleliterature'sannotation is performedand
- resultsknowledge graph integrationwhen needed

---

## Quick Start

## 1. PubTator3 annotation

```python
import requests
import pandas as pd
import json
import time

PUBTATOR_API = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api"


def annotate_pmids(pmids, concepts=None):
 """
 PubTator3 — PMID list'sannotation。

 Parameters:
 pmids: list — PMID list (e.g., [12345678, 23456789])
 concepts: list — 
 "gene", "disease", "chemical", "mutation", "species", "cellline"

 """
 if concepts is None:
 concepts = ["gene", "disease", "chemical", "mutation", "species"]

 pmid_str = ",".join(str(p) for p in pmids)
 params = {
 "pmids": pmid_str,
 "concepts": ",".join(concepts),
 "format": "biocjson",
 }

 resp = requests.get(f"{PUBTATOR_API}/publications/export/biocjson", params=params)
 resp.raise_for_status
 data = resp.json

 # Parse annotations
 all_annotations = []
 for doc in data.get("PubTator3", []) if isinstance(data, dict) else [data]:
 pmid = doc.get("pmid", doc.get("id", ""))
 for passage in doc.get("passages", []):
 for annotation in passage.get("annotations", []):
 infons = annotation.get("infons", {})
 all_annotations.append({
 "pmid": pmid,
 "text": annotation.get("text", ""),
 "type": infons.get("type", ""),
 "identifier": infons.get("identifier", ""),
 "offset": annotation.get("locations", [{}])[0].get("offset", ""),
 "length": annotation.get("locations", [{}])[0].get("length", ""),
 "passage_type": passage.get("infons", {}).get("type", ""),
 })

 df = pd.DataFrame(all_annotations)
 type_counts = df["type"].value_counts.to_dict if not df.empty else {}
 print(f"PubTator annotation: {len(pmids)} PMIDs → "
 f"{len(df)} entities {type_counts}")
 return df
```

## 2. PubTator3 search

```python
def search_pubtator(query, max_results=100):
 """
 PubTator3 search — papersearch。

 Parameters:
 query: str — search query (gene name、disease、compound)
 max_results: int — maximum retrieval count
 """
 params = {
 "text": query,
 "sort": "score",
 "page_size": min(max_results, 100),
 }
 resp = requests.get(f"{PUBTATOR_API}/search/", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for hit in data.get("results", []):
 results.append({
 "pmid": hit.get("pmid", ""),
 "title": hit.get("title", ""),
 "journal": hit.get("journal", ""),
 "year": hit.get("year", ""),
 "score": hit.get("score", 0),
 "genes": hit.get("genes", []),
 "diseases": hit.get("diseases", []),
 "chemicals": hit.get("chemicals", []),
 "mutations": hit.get("mutations", []),
 })

 df = pd.DataFrame(results)
 total = data.get("count", 0)
 print(f"PubTator search '{query}': {total} total, {len(df)} returned")
 return df
```

## 3. extraction

```python
def extract_entity_relations(pmids, relation_types=None):
 """
 PubTator3 — (gene-disease, drug-target ) extraction。

 Parameters:
 pmids: list — PMID list
 relation_types: list — filter
 "GDA" (gene-disease), "CDA" (chemical-disease),
 "CGA" (chemical-gene), "PPI" (protein-protein)
 """
 # Get annotations with relations
 df_annotations = annotate_pmids(pmids)

 # Extract co-occurrences within same passage
 relations = []
 for pmid in df_annotations["pmid"].unique:
 pmid_df = df_annotations[df_annotations["pmid"] == pmid]

 # Gene-Disease relations
 genes = pmid_df[pmid_df["type"] == "Gene"]
 diseases = pmid_df[pmid_df["type"] == "Disease"]
 chemicals = pmid_df[pmid_df["type"] == "Chemical"]

 if not relation_types or "GDA" in relation_types:
 for _, gene in genes.iterrows:
 for _, disease in diseases.iterrows:
 relations.append({
 "pmid": pmid,
 "relation_type": "GDA",
 "entity1_type": "Gene",
 "entity1_text": gene["text"],
 "entity1_id": gene["identifier"],
 "entity2_type": "Disease",
 "entity2_text": disease["text"],
 "entity2_id": disease["identifier"],
 })

 if not relation_types or "CGA" in relation_types:
 for _, chem in chemicals.iterrows:
 for _, gene in genes.iterrows:
 relations.append({
 "pmid": pmid,
 "relation_type": "CGA",
 "entity1_type": "Chemical",
 "entity1_text": chem["text"],
 "entity1_id": chem["identifier"],
 "entity2_type": "Gene",
 "entity2_text": gene["text"],
 "entity2_id": gene["identifier"],
 })

 if not relation_types or "CDA" in relation_types:
 for _, chem in chemicals.iterrows:
 for _, disease in diseases.iterrows:
 relations.append({
 "pmid": pmid,
 "relation_type": "CDA",
 "entity1_type": "Chemical",
 "entity1_text": chem["text"],
 "entity1_id": chem["identifier"],
 "entity2_type": "Disease",
 "entity2_text": disease["text"],
 "entity2_id": disease["identifier"],
 })

 rel_df = pd.DataFrame(relations)
 rel_counts = rel_df["relation_type"].value_counts.to_dict if not rel_df.empty else {}
 print(f"Entity relations: {len(rel_df)} total {rel_counts}")
 return rel_df
```

## 4. annotationdashboard

```python
def annotation_summary_dashboard(pmids, output_prefix="pubtator"):
 """
 PubTator annotationvisualization。

 Parameters:
 pmids: list — PMID list
 output_prefix: str — output file
 """
 import matplotlib.pyplot as plt

 # Get annotations
 df = annotate_pmids(pmids)
 if df.empty:
 print("No annotations found")
 return {}

 # Entity type distribution
 fig, axes = plt.subplots(1, 3, figsize=(15, 5))

 # 1. Entity type counts
 type_counts = df["type"].value_counts
 type_counts.plot(kind="bar", ax=axes[0], color="#2196F3")
 axes[0].set_title("Entity Type Distribution")
 axes[0].set_ylabel("Count")

 # 2. Top entities per type
 for entity_type in ["Gene", "Disease", "Chemical"]:
 sub = df[df["type"] == entity_type]
 top = sub["text"].value_counts.head(10)
 if not top.empty:
 print(f"\nTop {entity_type}s: {top.to_dict}")

 # 3. Articles per entity count
 per_article = df.groupby("pmid")["type"].count
 per_article.hist(ax=axes[1], bins=20, color="#4CAF50")
 axes[1].set_title("Entities per Article")
 axes[1].set_xlabel("Number of entities")

 # Entity type per article
 pivot = df.groupby(["pmid", "type"]).size.unstack(fill_value=0)
 pivot.plot(kind="box", ax=axes[2])
 axes[2].set_title("Entity Types per Article")

 plt.tight_layout
 fig_path = f"figures/{output_prefix}_dashboard.png"
 plt.savefig(fig_path, dpi=150, bbox_inches="tight")
 plt.close

 # Save results
 df.to_csv(f"results/{output_prefix}_annotations.csv", index=False)

 summary = {
 "total_pmids": df["pmid"].nunique,
 "total_annotations": len(df),
 "entity_types": type_counts.to_dict,
 "unique_entities": df.groupby("type")["text"].nunique.to_dict,
 }
 print(f"\nSummary: {summary}")
 return summary
```

## 5. knowledge graphconstructionfornetwork

```python
def build_entity_network(pmids, min_cooccurrence=2):
 """
 PubTator networkconstruction。

 Parameters:
 pmids: list — PMID list
 min_cooccurrence: int — timesnumber/count
 """
 import networkx as nx
 from collections import Counter

 rel_df = extract_entity_relations(pmids)
 if rel_df.empty:
 return nx.Graph

 # Count co-occurrences
 edge_counter = Counter
 for _, row in rel_df.iterrows:
 key = tuple(sorted([
 f"{row['entity1_type']}:{row['entity1_text']}",
 f"{row['entity2_type']}:{row['entity2_text']}",
 ]))
 edge_counter[key] += 1

 # Build network
 G = nx.Graph
 for (node1, node2), count in edge_counter.items:
 if count >= min_cooccurrence:
 G.add_edge(node1, node2, weight=count)

 print(f"Entity network: {G.number_of_nodes} nodes, "
 f"{G.number_of_edges} edges "
 f"(min cooccurrence = {min_cooccurrence})")
 return G
```

---

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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/pubtator_annotations.csv` | annotation | → text-mining-nlp, knowledge-graph |
| `results/entity_relations.csv` | | → network-analysis, disease-research |
| `results/entity_network.graphml` | network | → graph-neural-networks |
| `figures/pubtator_dashboard.png` | annotation | → publication-figures |

## Pipeline Integration

```
literature-search ──→ biomedical-pubtator ──→ text-mining-nlp
 (PubMed/OpenAlex) (PubTator NER) (KG construction)
 │
 ├──→ disease-research (GDA )
 ├──→ drug-target-profiling (CGA )
 └──→ preprint-archive ( NER)
```
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
