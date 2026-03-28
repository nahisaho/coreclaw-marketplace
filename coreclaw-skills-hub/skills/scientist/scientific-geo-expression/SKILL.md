---
name: scientific-geo-expression
description: |
 GEO expression skill. Gene Expression Omnibus data retrieval, microarray/RNA-seq dataset processing, GEO2R analysis, and cross-platform data normalization.
tu_tools:
 - key: geo
 name: GEO (Gene Expression Omnibus)
 description: GEO datasetinformationexpressiondatasearch
---

# Scientific GEO Expression

GEO REST API utilizingtranscriptomeexpressionfile
analysis pipeline.

## When to Use

- GEO dataset (GDS/GSE) searchwhen needed
- /RNA-seq expression is retrievedand
- conditionexpressionanalysis (DEG) is executedand
- multiple GEO dataset cross-cuttingcomparisonwhen needed
- GEO datafromexperimentcondition structurewhen needed
- analysispipeline GEO datausewhen needed

---

## Quick Start

## 1. GEO Dataset Search

```python
import requests
import pandas as pd
import GEOparse
from io import StringIO

GEO_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def geo_search_datasets(query, organism="Homo sapiens",
 study_type=None, limit=20):
 """
 GEO — Dataset Search (E-utilities)。

 Parameters:
 query: str — search query (example: "breast cancer RNA-seq")
 organism: str — organism/species
 study_type: str — research ("Expression profiling by array" etc.)
 limit: int — maximum results
 """
 search_term = f"{query} AND {organism}[Organism]"
 if study_type:
 search_term += f' AND "{study_type}"[Study Type]'

 # ESearch
 url = f"{GEO_BASE}/esearch.fcgi"
 params = {
 "db": "gds",
 "term": search_term,
 "retmax": limit,
 "retmode": "json",
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 ids = resp.json.get("esearchresult", {}).get("idlist", [])

 if not ids:
 print("No GEO datasets found")
 return pd.DataFrame

 # ESummary
 url = f"{GEO_BASE}/esummary.fcgi"
 params = {"db": "gds", "id": ",".join(ids), "retmode": "json"}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 summaries = resp.json.get("result", {})

 results = []
 for gds_id in ids:
 info = summaries.get(gds_id, {})
 results.append({
 "accession": info.get("accession", ""),
 "title": info.get("title", ""),
 "summary": info.get("summary", "")[:200],
 "organism": info.get("taxon", ""),
 "platform": info.get("gpl", ""),
 "sample_count": info.get("n_samples", 0),
 "series_type": info.get("gdstype", ""),
 "pub_date": info.get("pdat", ""),
 })

 df = pd.DataFrame(results)
 print(f"GEO search: {len(df)} datasets")
 return df
```

## 2. GEO expressionretrieval

```python
def geo_get_expression_matrix(gse_id, log2_transform=True):
 """
 GEO — GSE expressionretrieval (GEOparse)。

 Parameters:
 gse_id: str — GSE accession (example: "GSE12345")
 log2_transform: bool — log2 transformation is applied
 """
 import numpy as np

 gse = GEOparse.get_GEO(geo=gse_id, destdir="/tmp", silent=True)

 # data
 samples = []
 for gsm_name, gsm in gse.gsms.items:
 meta = gsm.metadata
 samples.append({
 "sample_id": gsm_name,
 "title": meta.get("title", [""])[0],
 "source": meta.get("source_name_ch1", [""])[0],
 "characteristics": "; ".join(
 meta.get("characteristics_ch1", [])),
 "platform": meta.get("platform_id", [""])[0],
 })
 sample_df = pd.DataFrame(samples)

 # expression
 pivoted = gse.pivot_samples("VALUE")
 if pivoted.empty:
 print(f"No expression data in {gse_id}")
 return sample_df, pd.DataFrame

 if log2_transform:
 pivoted = np.log2(pivoted.astype(float) + 1)

 print(f"GEO {gse_id}: {pivoted.shape[0]} probes × "
 f"{pivoted.shape[1]} samples")
 return sample_df, pivoted
```

## 3. expressionanalysis

```python
from scipy import stats
import numpy as np


def geo_differential_expression(expr_matrix, group_a_samples,
 group_b_samples, method="ttest",
 fdr_threshold=0.05, lfc_threshold=1.0):
 """
 GEO — expressionanalysis。

 Parameters:
 expr_matrix: pd.DataFrame — expression (genes × samples)
 group_a_samples: list[str] — loop A ID
 group_b_samples: list[str] — loop B ID
 method: str — "ttest" or "wilcoxon"
 fdr_threshold: float — FDR threshold
 lfc_threshold: float — log2FC threshold
 """
 a_data = expr_matrix[group_a_samples]
 b_data = expr_matrix[group_b_samples]

 results = []
 for gene in expr_matrix.index:
 a_vals = a_data.loc[gene].dropna.values
 b_vals = b_data.loc[gene].dropna.values

 if len(a_vals) < 2 or len(b_vals) < 2:
 continue

 lfc = b_vals.mean - a_vals.mean

 if method == "ttest":
 stat, pval = stats.ttest_ind(a_vals, b_vals)
 else:
 stat, pval = stats.mannwhitneyu(a_vals, b_vals,
 alternative="two-sided")

 results.append({
 "gene": gene,
 "log2fc": lfc,
 "mean_a": a_vals.mean,
 "mean_b": b_vals.mean,
 "statistic": stat,
 "p_value": pval,
 })

 df = pd.DataFrame(results)

 # FDR correction (Benjamini-Hochberg)
 from statsmodels.stats.multitest import multipletests
 _, df["fdr"], _, _ = multipletests(df["p_value"], method="fdr_bh")

 # DEG filter
 df["is_deg"] = (df["fdr"] < fdr_threshold) & (df["log2fc"].abs > lfc_threshold)
 n_deg = df["is_deg"].sum
 n_up = ((df["is_deg"]) & (df["log2fc"] > 0)).sum
 n_down = ((df["is_deg"]) & (df["log2fc"] < 0)).sum

 print(f"DEG: {n_deg} genes (↑{n_up} / ↓{n_down}), "
 f"FDR<{fdr_threshold}, |LFC|>{lfc_threshold}")
 return df.sort_values("p_value")
```

## 4. GEO expressionpipeline

```python
def geo_expression_pipeline(gse_id, group_col="condition",
 group_a="control", group_b="treatment",
 output_dir="results"):
 """
 GEO expressionintegrationpipeline。

 Parameters:
 gse_id: str — GSE accession
 group_col: str — loopcolumn
 group_a: str — loop
 group_b: str — loop
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) Data Retrieval
 sample_df, expr = geo_get_expression_matrix(gse_id)
 sample_df.to_csv(output_dir / "samples.csv", index=False)

 # 2) loopmin
 a_samples = sample_df[
 sample_df["source"].str.contains(group_a, case=False)
 ]["sample_id"].tolist
 b_samples = sample_df[
 sample_df["source"].str.contains(group_b, case=False)
 ]["sample_id"].tolist

 # 3) expression
 deg = geo_differential_expression(expr, a_samples, b_samples)
 deg.to_csv(output_dir / "deg_results.csv", index=False)

 print(f"GEO pipeline: {output_dir}")
 return {"samples": sample_df, "expression": expr, "deg": deg}
```

---

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|---------|
| `geo` | GEO | Dataset Searchinformationexpressiondata |

## Pipeline Integration

```
ebi-databases → geo-expression → gene-expression-transcriptomics
 (ENA/EBI Search) (GEO data) (DESeq2/GTEx)
 │ │ ↓
 literature-search ────┘ pathway-enrichment
 (PubMed/OpenAlex) │ (KEGG/Reactome/GO)
 ↓
 multi-omics
 (integrated analysis)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/samples.csv` | data | → gene-expression-transcriptomics |
| `results/deg_results.csv` | expressionresults | → pathway-enrichment |
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
