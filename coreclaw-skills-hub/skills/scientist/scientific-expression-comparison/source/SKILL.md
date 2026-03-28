---
name: scientific-expression-comparison
description: |
 Gene expression comparison skill. Differential expression analysis (DESeq2/edgeR/limma), multi-condition comparison, volcano plots, and enrichment analysis pipelines.
---

# Scientific Expression Comparison

EBI Expression Atlas API as GTEx/HPA dataand integration
gene expressioncomparisonpipeline is provided。expressionexpression
experimentdatacross-cuttingsearchcomparison。

## When to Use

- EBI Expression Atlas gene's expression is investigatedand
- disease vs 'sexpressiondata is searchedand
- multiple'stissue/celltypeexpressioncomparison is performedand
- Expression Atlas 's experimentdata is retrievedand
- GTEx/HPA 's expressiondata and integrationcomparisonminwhen needed

---

## Quick Start

## 1. expressionsearch

```python
import requests
import pandas as pd

ATLAS_API = "https://www.ebi.ac.uk/gxa/json"
ATLAS_REST = "https://www.ebi.ac.uk/gxa"


def get_baseline_expression(gene, species="homo sapiens"):
 """
 Expression Atlas expressionfileretrieval。

 Parameters:
 gene: str — gene symbolor Ensembl ID
 species: str — organism/species

 """
 url = f"{ATLAS_REST}/json/baseline_expression"
 params = {"gene": gene, "species": species}
 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 profiles = data.get("profiles", {}).get("rows", [])
 rows = []
 for profile in profiles:
 gene_name = profile.get("name", gene)
 for exp in profile.get("expressions", []):
 rows.append({
 "gene": gene_name,
 "factor_value": exp.get("factorValue", ""),
 "expression_level": exp.get("value"),
 "unit": "TPM",
 })

 df = pd.DataFrame(rows)
 print(f"Baseline expression for {gene}: {len(df)} tissue/cell profiles")
 return df
```

## 2. expressionsearch

```python
def search_differential_expression(gene, condition=None, species="homo sapiens"):
 """
 expressionexperiment'ssearch。

 Parameters:
 gene: str — gene symbolor Ensembl ID
 condition: str — condition (example: "cancer", "inflammation")
 species: str — organism/species

 ExpressionAtlas_search_differential(
 gene=gene, condition=condition, species=species
 )
 """
 url = f"{ATLAS_REST}/json/search"
 params = {"geneQuery": gene, "species": species}
 if condition:
 params["conditionQuery"] = condition

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 results = data.get("results", [])
 rows = []
 for r in results:
 rows.append({
 "experiment_accession": r.get("experimentAccession"),
 "experiment_description": r.get("experimentDescription", "")[:200],
 "experiment_type": r.get("experimentType"),
 "species": r.get("species"),
 "contrast": r.get("contrastId", ""),
 "log2_fold_change": r.get("foldChange"),
 "p_value": r.get("pValue"),
 })

 df = pd.DataFrame(rows)
 print(f"Differential expression for {gene}: {len(df)} contrasts found")
 return df
```

## 3. experimentData Retrieval

```python
def get_experiment_details(accession):
 """
 Expression Atlas experimentdetailsretrieval。

 Parameters:
 accession: str — experiment ID (example: "E-MTAB-5214")

 """
 url = f"{ATLAS_REST}/json/experiments/{accession}"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 experiment = data.get("experiment", {})
 info = {
 "accession": experiment.get("accession"),
 "description": experiment.get("description"),
 "type": experiment.get("type"),
 "species": experiment.get("species", []),
 "pubmed_ids": experiment.get("pubmedIds", []),
 "n_assays": experiment.get("numberOfAssays"),
 "n_contrasts": experiment.get("numberOfContrasts"),
 "last_updated": experiment.get("lastUpdate"),
 }

 print(f"Experiment: {info['accession']} — {info['description'][:100]}")
 return info
```

## 4. experimentsearch

```python
def search_experiments(gene=None, condition=None, species="homo sapiens"):
 """
 Expression Atlas experimentsearch。

 Parameters:
 gene: str — gene
 condition: str — condition
 species: str — organism/species

 ExpressionAtlas_search_experiments(
 gene=gene, condition=condition, species=species
 )
 """
 url = f"{ATLAS_REST}/json/search"
 params = {"species": species}
 if gene:
 params["geneQuery"] = gene
 if condition:
 params["conditionQuery"] = condition

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 experiments = data.get("matchingExperiments", [])
 rows = []
 for e in experiments:
 rows.append({
 "accession": e.get("experimentAccession"),
 "description": e.get("experimentDescription", "")[:200],
 "type": e.get("experimentType"),
 "species": e.get("species"),
 "n_assays": e.get("numberOfAssays"),
 })

 df = pd.DataFrame(rows)
 print(f"Experiments found: {len(df)}")
 return df
```

## 5. tissuecross-cuttingexpressioncomparison

```python
def cross_tissue_comparison(genes, species="homo sapiens"):
 """
 multiplegene'stissuecross-cuttingexpressioncomparison。

 Parameters:
 genes: list — gene list
 species: str — organism/species

 Returns:
 DataFrame — genes × tissues expression
 """
 all_data = []
 for gene in genes:
 df = get_baseline_expression(gene, species)
 if not df.empty:
 df["gene_query"] = gene
 all_data.append(df)

 if not all_data:
 print("No expression data found")
 return pd.DataFrame

 combined = pd.concat(all_data, ignore_index=True)

 # table (genes × tissues)
 matrix = combined.pivot_table(
 index="gene",
 columns="factor_value",
 values="expression_level",
 aggfunc="mean",
 )

 print(f"Expression matrix: {matrix.shape[0]} genes × "
 f"{matrix.shape[1]} tissues/conditions")
 return matrix
```

## 6. expressionheatmap

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_expression_heatmap(matrix, title="Gene Expression Comparison",
 figsize=(14, 8), save_path=None):
 """
 expression'sheatmapdrawing/plotting。

 Parameters:
 matrix: DataFrame — cross_tissue_comparison 's output
 title: str — figuretitle
 figsize: tuple — figure
 save_path: str — save
 """
 log_matrix = np.log2(matrix.fillna(0) + 1)

 fig, ax = plt.subplots(figsize=figsize)
 sns.heatmap(
 log_matrix,
 cmap="viridis",
 xticklabels=True,
 yticklabels=True,
 ax=ax,
 )
 ax.set_title(title)
 ax.set_xlabel("Tissue / Condition")
 ax.set_ylabel("Gene")
 plt.tight_layout

 if save_path:
 fig.savefig(save_path, dpi=150, bbox_inches="tight")
 print(f"Saved: {save_path}")
 plt.show
```

---

## Pipeline Integration

```
gene-expression-transcriptomics → expression-comparison → multi-omics
 (GEO/GTEx/DESeq2) (Atlas expressioncomparison) (integrated analysis)
 │ │ ↓
human-protein-atlas ────────────┘ │ pathway-enrichment
 (HPA tissue/cancerexpression) ↓ (KEGG/GO)
 ontology-enrichment
 (EFO shapemapping)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/baseline_expression.csv` | expression | → gene-expression |
| `results/differential_expression.csv` | expression | → pathway-enrichment |
| `results/expression_matrix.csv` | expression | → multi-omics |
| `figures/expression_heatmap.png` | heatmap | → publication-figures |

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
