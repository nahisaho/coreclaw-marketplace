---
name: scientific-nci60-screening
description: |
 NCI-60 cancercellskill。CellMiner API 
 NCI-60 GI50/LC50 dataDepMap cancer dependency integration
 -moleculecorrelationcellcomparisonanalysis。
tu_tools:
 - key: nci60
 name: NCI-60
 description: cancercelldatasearch
---

# Scientific NCI-60 Screening

CellMiner / NCI-60 / DepMap utilizingcancercell
pipeline is provided。loopdata's
integrated analysis、、comparison。

## When to Use

- NCI-60 cell's (GI50) analysiswhen needed
- CellMiner fromcompoundactivitydata is retrievedand
- and molecule (variant/mutation/expression) 's correlation is investigatedand
- DepMap CRISPR/RNAi dependencydata forwhen needed
- cell's is comparedand
- novelcompound's results NCI-60 and comparisonwhen needed

---

## Quick Start

## 1. CellMiner Data Retrieval

```python
import requests
import pandas as pd
import numpy as np
from io import StringIO

CELLMINER_BASE = "https://discover.nci.nih.gov/cellminer/api"


def cellminer_drug_activity(nsc_id=None, drug_name=None):
 """
 CellMiner — NCI-60 activityData Retrieval。

 Parameters:
 nsc_id: str — NSC ID (example: "740")
 drug_name: str — (example: "Paclitaxel")
 """
 if nsc_id:
 url = f"{CELLMINER_BASE}/compound/{nsc_id}/activity"
 elif drug_name:
 url = f"{CELLMINER_BASE}/compound/search"
 params = {"name": drug_name}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 compounds = resp.json
 if not compounds:
 print(f"Drug not found: {drug_name}")
 return pd.DataFrame
 nsc_id = compounds[0].get("nsc", "")
 url = f"{CELLMINER_BASE}/compound/{nsc_id}/activity"

 resp = requests.get(url, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for cell_line, values in data.get("activity", {}).items:
 results.append({
 "cell_line": cell_line,
 "tissue": values.get("tissue", ""),
 "gi50_log": values.get("gi50", None),
 "tgi_log": values.get("tgi", None),
 "lc50_log": values.get("lc50", None),
 })

 df = pd.DataFrame(results)
 print(f"CellMiner: NSC {nsc_id} → {len(df)} cell lines")
 return df
```

## 2. NCI-60 bulkData Retrieval

```python
def nci60_bulk_download(data_type="drug_activity"):
 """
 NCI-60 bulkdatasetretrieval。

 Parameters:
 data_type: str — "drug_activity", "gene_expression",
 "mutation", "copy_number"
 """
 urls = {
 "drug_activity": "https://discover.nci.nih.gov/cellminer/download/DTP_NCI60_ZSCORE.csv",
 "gene_expression": "https://discover.nci.nih.gov/cellminer/download/GeneExpr_RMA.csv",
 "mutation": "https://discover.nci.nih.gov/cellminer/download/Exome_Mutation.csv",
 }

 url = urls.get(data_type)
 if not url:
 raise ValueError(f"Unknown data type: {data_type}")

 resp = requests.get(url, timeout=120)
 resp.raise_for_status

 df = pd.read_csv(StringIO(resp.text))
 print(f"NCI-60 bulk: {data_type} → {df.shape}")
 return df
```

## 3. -moleculecorrelation

```python
from scipy import stats


def drug_marker_correlation(drug_activity, molecular_data,
 marker_type="expression", top_n=50):
 """
 and molecule'scorrelationanalysis。

 Parameters:
 drug_activity: pd.DataFrame — GI50 data (cell_line, gi50)
 molecular_data: pd.DataFrame — moleculedata (cell_line, gene, value)
 marker_type: str — "expression", "mutation", "copy_number"
 top_n: int — topcorrelationgenenumber/count
 """
 # cell
 common_lines = set(drug_activity["cell_line"]) & set(molecular_data["cell_line"])
 drug_sub = drug_activity[drug_activity["cell_line"].isin(common_lines)]
 mol_sub = molecular_data[molecular_data["cell_line"].isin(common_lines)]

 # geneand 'scorrelation
 correlations = []
 genes = mol_sub["gene"].unique if "gene" in mol_sub.columns else mol_sub.columns[1:]

 drug_values = drug_sub.set_index("cell_line")["gi50_log"]

 for gene in genes:
 if "gene" in mol_sub.columns:
 gene_data = mol_sub[mol_sub["gene"] == gene].set_index("cell_line")["value"]
 else:
 gene_data = mol_sub.set_index("cell_line")[gene]

 common = drug_values.index.intersection(gene_data.index)
 if len(common) < 10:
 continue

 r, p = stats.pearsonr(drug_values[common], gene_data[common])
 correlations.append({
 "gene": gene,
 "pearson_r": r,
 "p_value": p,
 "n_samples": len(common),
 })

 corr_df = pd.DataFrame(correlations)
 corr_df["adj_p"] = corr_df["p_value"] * len(corr_df) # Bonferroni
 corr_df = corr_df.sort_values("p_value")

 print(f"Drug-marker correlation: {len(corr_df)} genes tested, "
 f"top |r| = {corr_df['pearson_r'].abs.max:.3f}")
 return corr_df.head(top_n)
```

## 4. tissue

```python
def tissue_response_pattern(drug_activity, min_lines=3):
 """
 tissue'sanalysis。

 Parameters:
 drug_activity: pd.DataFrame — GI50 data
 min_lines: int — cellnumber/count
 """
 tissue_stats = drug_activity.groupby("tissue").agg(
 n_lines=("gi50_log", "count"),
 mean_gi50=("gi50_log", "mean"),
 std_gi50=("gi50_log", "std"),
 min_gi50=("gi50_log", "min"),
 max_gi50=("gi50_log", "max"),
 ).reset_index

 tissue_stats = tissue_stats[tissue_stats["n_lines"] >= min_lines]
 tissue_stats = tissue_stats.sort_values("mean_gi50")

 # /
 overall_mean = drug_activity["gi50_log"].mean
 tissue_stats["sensitivity_z"] = (
 (tissue_stats["mean_gi50"] - overall_mean)
 / drug_activity["gi50_log"].std
 )

 print(f"Tissue patterns: {len(tissue_stats)} tissues")
 for _, row in tissue_stats.iterrows:
 label = "Sensitive" if row["sensitivity_z"] < -0.5 else (
 "Resistant" if row["sensitivity_z"] > 0.5 else "Neutral"
 )
 print(f" {row['tissue']}: GI50={row['mean_gi50']:.2f} ({label})")
 return tissue_stats
```

## 5. DepMap integration

```python
DEPMAP_BASE = "https://depmap.org/portal/api"


def depmap_gene_dependency(gene_symbol, dataset="Chronos_Combined"):
 """
 DepMap — CRISPR/RNAi genedependencyretrieval。

 Parameters:
 gene_symbol: str — gene symbol
 dataset: str — dataset name
 """
 url = f"{DEPMAP_BASE}/download/custom"
 params = {
 "gene": gene_symbol,
 "dataset": dataset,
 }
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for entry in data.get("data", []):
 results.append({
 "cell_line": entry.get("cell_line_name", ""),
 "lineage": entry.get("lineage", ""),
 "dependency_score": entry.get("score", None),
 })

 df = pd.DataFrame(results)
 if len(df) > 0:
 n_dependent = (df["dependency_score"] < -0.5).sum
 print(f"DepMap {gene_symbol}: {len(df)} lines, "
 f"{n_dependent} dependent (score < -0.5)")
 return df
```

## 6. NCI-60 integrationpipeline

```python
def nci60_screening_pipeline(drug_name=None, nsc_id=None,
 target_gene=None, output_dir="results"):
 """
 NCI-60 + DepMap integrationpipeline。

 Parameters:
 drug_name: str — 
 nsc_id: str — NSC ID
 target_gene: str — gene (DepMap integration)
 output_dir: str — output directory
 """
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) NCI-60 activity
 drug_data = cellminer_drug_activity(nsc_id=nsc_id, drug_name=drug_name)
 drug_data.to_csv(output_dir / "drug_activity.csv", index=False)

 # 2) tissue
 tissue_patterns = tissue_response_pattern(drug_data)
 tissue_patterns.to_csv(output_dir / "tissue_patterns.csv", index=False)

 # 3) expressioncorrelation
 expr_data = nci60_bulk_download("gene_expression")
 correlations = drug_marker_correlation(drug_data, expr_data)
 correlations.to_csv(output_dir / "marker_correlations.csv", index=False)

 # 4) DepMap integration (gene)
 if target_gene:
 depmap_data = depmap_gene_dependency(target_gene)
 depmap_data.to_csv(output_dir / "depmap_dependency.csv", index=False)

 print(f"Pipeline complete: {output_dir}")
 return {
 "drug_activity": drug_data,
 "tissue_patterns": tissue_patterns,
 "correlations": correlations,
 }
```

---

## Pipeline Integration

```
compound-screening → nci60-screening → precision-oncology
 (ZINC/VS) (NCI-60/DepMap) (MTB report)
 │ │ ↓
drug-target-profiling ──────┘ cancer-genomics
 (ChEMBL/DGIdb) │ (COSMIC/DepMap)
 ↓
 cell-line-resources
 (Cellosaurus)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/drug_activity.csv` | NCI-60 GI50 data | → precision-oncology |
| `results/tissue_patterns.csv` | tissue | → cancer-genomics |
| `results/marker_correlations.csv` | -correlation | → drug-target-profiling |
| `results/depmap_dependency.csv` | DepMap dependency | → cell-line-resources |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `nci60` | NCI-60 | cancercelldatasearch |
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
