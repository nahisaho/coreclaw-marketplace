---
name: scientific-text-mining-nlp
description: |
 Text mining and NLP skill. Scientific text mining, named entity recognition, relation extraction, topic modeling, and biomedical NLP pipelines.
---

# Scientific Text Mining & NLP

literaturefor/against（NLP）pipeline is provided。
、extraction、graphconstruction、
、automated systematichandles。

## When to Use

- amount's literaturefromgenediseasedrugautomatedextractionwhen needed
- protein-proteininteraction（PPI）'sliteraturefromextractionwhen needed
- literature'sgraph is builtand
- research's is performedand
- citationnetworkmin 's paperwhen needed

---

## Quick Start

## 1. NER（Named Entity Recognition）

```python
import numpy as np
import pandas as pd
import re


def _regex_ner_fallback(texts):
 """Regex-based NER fallback for common chemical/material patterns."""
 patterns = {
 "Chemical": r'\b[A-Z][a-z]?(?:\d+[A-Z][a-z]?)*\d*(?:\s*[\-·]\s*[A-Z][a-z]?\d*)*\b',
 "Gene": r'\b[A-Z][A-Z0-9]{1,5}\d*\b',
 "Disease": r'\b[A-Z][a-z]+(?:\s+[a-z]+)*\s+(?:disease|syndrome|disorder|cancer)\b',
 }
 all_entities = []
 for i, text in enumerate(texts):
 for label, pattern in patterns.items:
 for m in re.finditer(pattern, text):
 all_entities.append({
 "doc_id": i, "text": m.group,
 "label": label,
 "start": m.start, "end": m.end,
 "kb_id": None, "confidence": None,
 })
 return pd.DataFrame(all_entities)


def biomedical_ner(texts, model="biobert", entity_types=None):
 """
 from's。

 model:
 - "biobert": BioBERT — PubMed BERT
 - "scispacy": SciSpaCy — spaCy
 - "pubtator": PubTator3 API — NCBI 's NER 

 entity_types:
 - Gene/Protein: geneprotein
 - Disease: disease（MESH / OMIM ID）
 - Chemical/Drug: compounddrug（MeSH / DrugBank ID）
 - Species: organism/species
 - Mutation: variant/mutation（tmVar shapeformula）
 - Cell Line / Cell Type
 """
 if entity_types is None:
 entity_types = ["Gene", "Disease", "Chemical", "Species", "Mutation"]

 if model == "scispacy":
 try:
 import spacy
 nlp = spacy.load("en_core_sci_lg")
 from scispacy.linking import EntityLinker
 nlp.add_pipe("scispacy_linker", config={
 "resolve_abbreviations": True,
 "linker_name": "umls"
 })
 except (ImportError, OSError):
 # Fallback: regex-based NER for common chemical/material patterns
 # when scispacy model is unavailable in the environment
 return _regex_ner_fallback(texts)

 all_entities = []
 for i, text in enumerate(texts):
 doc = nlp(text)
 for ent in doc.ents:
 all_entities.append({
 "doc_id": i,
 "text": ent.text,
 "label": ent.label_,
 "start": ent.start_char,
 "end": ent.end_char,
 "kb_id": ent._.kb_ents[0][0] if ent._.kb_ents else None,
 "confidence": ent._.kb_ents[0][1] if ent._.kb_ents else None,
 })

 df = pd.DataFrame(all_entities)
 print(f" NER: {len(df)} entities from {len(texts)} documents")
 return df

 elif model == "biobert":
 try:
 from transformers import pipeline
 ner_pipeline = pipeline("ner", model="dmis-lab/biobert-large-cased-v1.1-ner",
 aggregation_strategy="simple")
 except (ImportError, OSError):
 # Fallback: regex-based NER for common chemical/material patterns
 # when BioBERT model is unavailable in the environment
 return _regex_ner_fallback(texts)

 all_entities = []
 for i, text in enumerate(texts):
 entities = ner_pipeline(text)
 for ent in entities:
 all_entities.append({
 "doc_id": i, "text": ent["word"],
 "label": ent["entity_group"],
 "score": ent["score"],
 })

 return pd.DataFrame(all_entities)
```

## 2. extraction

```python
def relation_extraction(texts, relation_type="ppi", model="biobert_re"):
 """
 literaturefrom'sextraction。

 relation_type:
 - "ppi": Protein-Protein Interaction
 - "ddi": Drug-Drug Interaction
 - "gda": Gene-Disease Association
 - "chem_disease": Chemical-Disease Relation
 - "chem_gene": Chemical-Gene Interaction

 pipeline:
 1. NER extraction
 2. 's as
 3. each'sclassification（BERT ）
 4. degreefilter
 """
 from transformers import pipeline

 if relation_type == "ppi":
 re_model = "dmis-lab/biobert-v1.1" # Fine-tuned for PPI
 elif relation_type == "ddi":
 re_model = "dmis-lab/biobert-v1.1"

 classifier = pipeline("text-classification", model=re_model)

 relations = []
 for i, text in enumerate(texts):
 # Select NER backend to match the relation extraction model
 if model == "biobert_re":
 ner_results = biomedical_ner([text], model="biobert")
 elif model == "scispacy":
 ner_results = biomedical_ner([text], model="scispacy")
 else:
 ner_results = biomedical_ner([text], model="scispacy")
 entities = ner_results[ner_results["doc_id"] == 0]

 # all'sclassification
 for idx_a, ent_a in entities.iterrows:
 for idx_b, ent_b in entities.iterrows:
 if idx_a < idx_b:
 # 
 marked_text = mark_entities(text, [ent_a.to_dict, ent_b.to_dict])
 pred = classifier(marked_text[:512])

 if pred[0]["score"] > 0.7:
 relations.append({
 "doc_id": i,
 "entity_a": ent_a["text"],
 "entity_b": ent_b["text"],
 "relation": pred[0]["label"],
 "confidence": pred[0]["score"],
 })

 df = pd.DataFrame(relations)
 print(f" RE: {len(df)} relations from {len(texts)} documents")
 return df


def mark_entities(text, entities):
 """Annotate entities in text using span-based insertion (avoids overlaps)."""
 sorted_ents = sorted(entities, key=lambda e: e["start"], reverse=True)
 chars = list(text)
 for ent in sorted_ents:
 start, end = ent["start"], ent["end"]
 label = ent.get("label", "ENTITY")
 markup = f"[{text[start:end]}]({label})"
 chars[start:end] = list(markup)
 return "".join(chars)
```

## 3. graphconstruction

```python
def build_knowledge_graph(entities_df, relations_df, min_confidence=0.7):
 """
 literature'sgraphconstruction。

 node: （gene、disease、drug、 etc.）
 edge: （interacts_with, treats, causes, associated_with etc.）

 pipeline:
 1. normalization（UMLS CUI / MeSH ）
 2. 
 3. （frequency + degree）
 4. graphconstruction + 
 """
 import networkx as nx
 from collections import Counter

 # degreefilter
 rel_filtered = relations_df[relations_df["confidence"] >= min_confidence]

 # graphconstruction
 G = nx.MultiDiGraph

 # nodeaddition
 for _, ent in entities_df.iterrows:
 G.add_node(ent["text"], type=ent["label"],
 kb_id=ent.get("kb_id", None))

 # edgeaddition
 edge_counts = Counter
 for _, rel in rel_filtered.iterrows:
 key = (rel["entity_a"], rel["entity_b"], rel["relation"])
 edge_counts[key] += 1
 G.add_edge(rel["entity_a"], rel["entity_b"],
 relation=rel["relation"],
 confidence=rel["confidence"],
 frequency=edge_counts[key])

 # 
 G_simple = nx.Graph(G)
 from networkx.algorithms.community import louvain_communities
 communities = louvain_communities(G_simple, resolution=1.0)

 print(f" KG: {G.number_of_nodes} nodes, {G.number_of_edges} edges, "
 f"{len(communities)} communities")
 return G, communities
```

## 4. 

```python
def topic_modeling(abstracts, n_topics=10, method="bertopic"):
 """
 literature's。

 method:
 - "bertopic": BERTopic — BERT + HDBSCAN + c-TF-IDF
 - "lda": LDA (Latent Dirichlet Allocation) — rate
 - "nmf": NMF (Non-negative Matrix Factorization)

 BERTopic pipeline:
 1. BERT / SPECTER 
 2. UMAP dimensionality reduction
 3. HDBSCAN clustering
 4. c-TF-IDF extraction
 """
 if method == "bertopic":
 from bertopic import BERTopic
 from sentence_transformers import SentenceTransformer

 embedding_model = SentenceTransformer("allenai-specter")
 topic_model = BERTopic(embedding_model=embedding_model,
 nr_topics=n_topics,
 calculate_probabilities=True)

 topics, probs = topic_model.fit_transform(abstracts)

 topic_info = topic_model.get_topic_info
 print(f" Topics: {len(topic_info) - 1} topics from {len(abstracts)} documents")
 return topic_model, topics, probs

 elif method == "lda":
 from sklearn.decomposition import LatentDirichletAllocation
 from sklearn.feature_extraction.text import CountVectorizer

 vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
 dtm = vectorizer.fit_transform(abstracts)

 lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
 lda.fit(dtm)

 feature_names = vectorizer.get_feature_names_out
 topics = {}
 for i, topic_dist in enumerate(lda.components_):
 top_words = [feature_names[j] for j in topic_dist.argsort[-10:]]
 topics[f"Topic_{i}"] = top_words

 return lda, topics
```

## 5. citationnetworkmin

```python
def citation_network_analysis(papers_df, citations_df):
 """
 citationnetworkmin。

 :
 - In-degree: citationnumber/count → 
 - PageRank: citation's
 - Hub/Authority (HITS): Hub=number/countcitation、Authority=number/countcitation
 - Citation burst: citation（）
 - Bibliographic coupling: samepaper citation
 - Co-citation: citation
 """
 import networkx as nx

 G = nx.DiGraph
 for _, paper in papers_df.iterrows:
 G.add_node(paper["paper_id"], title=paper["title"],
 year=paper["year"])

 for _, cite in citations_df.iterrows:
 G.add_edge(cite["citing"], cite["cited"])

 # PageRank
 pagerank = nx.pagerank(G, alpha=0.85)

 # HITS
 hubs, authorities = nx.hits(G, max_iter=100)

 # results
 metrics_df = pd.DataFrame({
 "paper_id": list(G.nodes),
 "in_degree": [G.in_degree(n) for n in G.nodes],
 "out_degree": [G.out_degree(n) for n in G.nodes],
 "pagerank": [pagerank.get(n, 0) for n in G.nodes],
 "hub_score": [hubs.get(n, 0) for n in G.nodes],
 "authority_score": [authorities.get(n, 0) for n in G.nodes],
 })
 metrics_df = metrics_df.sort_values("pagerank", ascending=False)

 print(f" Citation network: {G.number_of_nodes} papers, "
 f"{G.number_of_edges} citations")
 return G, metrics_df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/ner_entities.csv` | CSV |
| `results/relations.csv` | CSV |
| `results/knowledge_graph.json` | JSON |
| `results/topic_model_info.csv` | CSV |
| `results/citation_metrics.csv` | CSV |
| `figures/kg_visualization.png` | PNG |
| `figures/topic_distribution.png` | PNG |
| `figures/citation_network.png` | PNG |

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

| Skill | Integration |
|---|---|
| [scientific-deep-research](../scientific-deep-research/SKILL.md) | literatureinvestigation |
| [scientific-citation-checker](../scientific-citation-checker/SKILL.md) | citationverification |
| [scientific-network-analysis](../scientific-network-analysis/SKILL.md) | networkanalysis |
| [scientific-meta-analysis](../scientific-meta-analysis/SKILL.md) | phylogenyliterature |
| [scientific-graph-neural-networks](../scientific-graph-neural-networks/SKILL.md) | graphinference |

#### Dependencies

- scispacy, spacy, transformers, bertopic, sentence-transformers, networkx
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
