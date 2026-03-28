---
name: scientific-bioinformatics
description: |
 analysispipeline'sskill。scRNA-seq（Scanpy）、genomesequenceanalysis
 （BioPython）、PPI networkanalysis（NetworkX）、'spreprocessing is performedfor。
 Scientific Skills Exp-01, 04, 07, 09 。
---

# Scientific Bioinformatics Pipelines

data'sanalysispipelineskill。scRNA-seq、genomesequenceanalysis、PPI network、
's 4 type's workflow integrationprovides。

## When to Use

- scRNA-seq data's QCpreprocessingclusteringDEG analysis
- genome/proteinsequence's phylogenyanalysisforanalysis
- proteininteractionnetwork's constructionanalysis
- 'spreprocessing（transformation）PLS-DA

## Quick Start

## 1. scRNA-seq pipeline（Exp-01）

### Scanpy standardworkflow

```python
import scanpy as sc

def scrnaseq_pipeline(adata, min_genes=200, max_genes=5000,
 max_pct_mito=20, n_hvg=2000, resolution=0.5):
 """
 Scanpy 's standard scRNA-seq analysispipeline。
 QC → normalization → HVG → PCA → Neighbors → Leiden → UMAP
 """
 # QC filter
 sc.pp.filter_cells(adata, min_genes=min_genes)
 sc.pp.filter_genes(adata, min_cells=3)

 adata.var["mt"] = adata.var_names.str.startswith("MT-")
 sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"],
 percent_top=None, inplace=True)
 adata = adata[adata.obs["pct_counts_mt"] < max_pct_mito].copy
 adata = adata[adata.obs["n_genes_by_counts"] < max_genes].copy

 # normalization & Log transformation
 sc.pp.normalize_total(adata, target_sum=1e4)
 sc.pp.log1p(adata)

 # HVG selection
 sc.pp.highly_variable_genes(adata, n_top_genes=n_hvg)
 adata.raw = adata
 adata = adata[:, adata.var["highly_variable"]].copy

 # PCA → Neighbors → UMAP → Leiden
 sc.pp.scale(adata, max_value=10)
 sc.tl.pca(adata, n_comps=50)
 sc.pp.neighbors(adata, n_pcs=30)
 sc.tl.umap(adata)
 sc.tl.leiden(adata, resolution=resolution)

 return adata
```

### cell typeannotation

```python
CELL_MARKERS = {
 "CD4+ T": ["IL7R", "CD4"],
 "CD8+ T": ["CD8A", "CD8B"],
 "B cell": ["MS4A1", "CD79A"],
 "NK": ["GNLY", "NKG7"],
 "Monocyte": ["CD14", "LYZ"],
 "DC": ["FCER1A", "CST3"],
 "Platelet": ["PPBP"],
}

def annotate_clusters(adata, marker_dict=None):
 """gene'sannotation。"""
 if marker_dict is None:
 marker_dict = CELL_MARKERS
 # and 'smeanexpression levelcelltype
 cluster_annotations = {}
 for cluster in adata.obs["leiden"].unique:
 mask = adata.obs["leiden"] == cluster
 best_score = -1
 best_type = "Unknown"
 for cell_type, markers in marker_dict.items:
 available = [m for m in markers if m in adata.raw.var_names]
 if available:
 score = adata.raw[mask][:, available].X.mean
 if score > best_score:
 best_score = score
 best_type = cell_type
 cluster_annotations[cluster] = best_type
 adata.obs["cell_type"] = adata.obs["leiden"].map(cluster_annotations)
 return adata
```

## 2. genomesequenceanalysispipeline（Exp-09）

```python
def compute_sequence_statistics(sequence):
 """DNA sequence's basicamount is computed。"""
 from collections import Counter
 seq_str = str(sequence).upper
 counts = Counter(seq_str)
 length = len(seq_str)
 gc_content = (counts.get("G", 0) + counts.get("C", 0)) / length * 100
 return {
 "Length": length,
 "GC_Content": gc_content,
 "A": counts.get("A", 0), "T": counts.get("T", 0),
 "G": counts.get("G", 0), "C": counts.get("C", 0),
 }

def codon_usage_rscu(coding_sequence):
 """RSCU（Relative Synonymous Codon Usage） is computed。"""
 from collections import Counter
 codons = [coding_sequence[i:i+3] for i in range(0, len(coding_sequence)-2, 3)]
 codon_counts = Counter(codons)
 # RSCU = observed / expected_if_uniform
 # group andcalculation
 return codon_counts # 、all Exp-09 reference
```

## 3. PPI networkanalysis（Exp-04）

```python
import networkx as nx

def build_ppi_network(interactions_df, source_col, target_col,
 weight_col=None):
 """PPI network is built。"""
 G = nx.Graph
 for _, row in interactions_df.iterrows:
 if weight_col:
 G.add_edge(row[source_col], row[target_col],
 weight=row[weight_col])
 else:
 G.add_edge(row[source_col], row[target_col])
 return G

def centrality_analysis(G):
 """Compute four centrality metrics at once."""
 centralities = pd.DataFrame({
 "Degree": dict(G.degree),
 "Betweenness": nx.betweenness_centrality(G),
 "Closeness": nx.closeness_centrality(G),
 "Eigenvector": nx.eigenvector_centrality(G, max_iter=1000),
 })
 centralities.to_csv("results/centrality_measures.csv")
 return centralities

def community_detection(G, method="louvain"):
 """。"""
 if method == "louvain":
 import community as community_louvain
 partition = community_louvain.best_partition(G)
 nx.set_node_attributes(G, partition, "community")
 return partition
 elif method == "greedy":
 from networkx.algorithms.community import greedy_modularity_communities
 communities = list(greedy_modularity_communities(G))
 partition = {}
 for i, comm in enumerate(communities):
 for node in comm:
 partition[node] = i
 return partition
```

## 4. preprocessing（Exp-07）

```python
from sklearn.impute import KNNImputer

def metabolomics_preprocessing(df, metabolite_cols, group_col=None):
 """
 'sstandardpreprocessingpipeline。
 KNN → Log2 transformation → Pareto 
 """
 X = df[metabolite_cols].values.copy

 # KNN 
 imputer = KNNImputer(n_neighbors=5)
 X_imputed = imputer.fit_transform(X)

 # Log2 transformation（value 's value）
 X_log = np.log2(X_imputed + 1)

 # Pareto 
 means = X_log.mean(axis=0)
 stds = X_log.std(axis=0)
 X_pareto = (X_log - means) / np.sqrt(stds + 1e-10)

 result_df = pd.DataFrame(X_pareto, columns=metabolite_cols, index=df.index)
 if group_col:
 result_df[group_col] = df[group_col].values

 return result_df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/centrality_measures.csv` | CSV |
| `results/community_pathway_mapping.csv` | CSV |
| `results/codon_usage.csv` | CSV |
| `figures/umap_clusters.png` | PNG |
| `figures/network_visualization.png` | PNG |

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
