---
name: scientific-nci60-screening
description: |
 NCI-60 screening skill. NCI-60 cancer cell line panel data analysis, drug sensitivity profiling, COMPARE algorithm, and multi-drug response comparison.
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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
