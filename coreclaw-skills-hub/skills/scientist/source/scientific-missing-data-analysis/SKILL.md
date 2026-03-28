---
name: scientific-missing-data-analysis
description: |
 dataanalysisskill。diagnosis (MCAR/MAR/MNAR) 
 Little's MCAR testingmethod (MICE) KNN 
 MissForestVAE/GAIN visualizationRubin's Rules。
tu_tools:
 - key: biotools
 name: bio.tools
 description: datatoolsearch
---

# Scientific Missing Data Analysis

data's diagnosissensitivity analysispipelineproviding、
's inference.

## When to Use

- dataset'sdiagnosiswhen needed
- MCAR / MAR / MNAR 'swhen needed
- method (MICE) valuewhen needed
- KNN / MissForest / deep learning'swhen needed
- multiple's results Rubin's Rules integrationwhen needed
- visualizationwhen needed

---

## Quick Start

## 1. diagnosis

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def diagnose_missing_patterns(df, output_prefix="missing"):
 """
 diagnosis — MCAR/MAR/MNAR support。

 Parameters:
 df: pd.DataFrame — input data
 output_prefix: str — output file
 """
 n_rows, n_cols = df.shape
 missing_counts = df.isnull.sum
 missing_pct = (missing_counts / n_rows * 100).round(2)

 summary = pd.DataFrame({
 "column": df.columns,
 "n_missing": missing_counts.values,
 "pct_missing": missing_pct.values,
 "dtype": df.dtypes.values
 }).sort_values("pct_missing", ascending=False)

 # (msno )
 fig, axes = plt.subplots(2, 2, figsize=(16, 12))

 # (1) 
 ax = axes[0, 0]
 missing_matrix = df.isnull.astype(int)
 ax.imshow(missing_matrix.values[:200], aspect="auto", cmap="Greys",
 interpolation="none")
 ax.set_xlabel("Features")
 ax.set_ylabel("Samples")
 ax.set_title("Missing Pattern Matrix (first 200 rows)")

 # (2) rate
 ax = axes[0, 1]
 cols_with_missing = summary[summary["pct_missing"] > 0]
 ax.barh(cols_with_missing["column"], cols_with_missing["pct_missing"])
 ax.set_xlabel("Missing %")
 ax.set_title("Missing Rate per Column")

 # (3) correlationheatmap
 ax = axes[1, 0]
 miss_corr = df.isnull.corr
 sns.heatmap(miss_corr, ax=ax, cmap="RdBu_r", center=0,
 square=True, cbar_kws={"shrink": 0.8})
 ax.set_title("Missing Correlation")

 # (4) top
 ax = axes[1, 1]
 patterns = df.isnull.apply(lambda x: tuple(x), axis=1)
 pattern_counts = patterns.value_counts.head(10)
 ax.barh(range(len(pattern_counts)),
 pattern_counts.values)
 ax.set_yticks(range(len(pattern_counts)))
 ax.set_yticklabels([str(p)[:40] for p in pattern_counts.index],
 fontsize=7)
 ax.set_xlabel("Count")
 ax.set_title("Top 10 Missing Patterns")

 plt.tight_layout
 path = f"{output_prefix}_diagnosis.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 print(f"Missing Diagnosis: {n_cols} cols, "
 f"{missing_counts.sum} total missing ({(missing_counts.sum/(n_rows*n_cols)*100):.1f}%)")
 return {"summary": summary, "fig": path}
```

## 2. Little's MCAR testing

```python
def littles_mcar_test(df):
 """
 Little's MCAR testing — all'stesting。

 Parameters:
 df: pd.DataFrame — number/countvaluedata's
 Returns:
 dict — chi2 amount, p-value, 
 """
 from scipy import stats

 numeric_df = df.select_dtypes(include=[np.number])
 n_rows, n_cols = numeric_df.shape

 # and
 patterns = numeric_df.isnull.apply(tuple, axis=1)
 unique_patterns = patterns.unique

 # allmean and allvariance
 global_mean = numeric_df.mean
 global_cov = numeric_df.cov

 chi2_stat = 0.0
 df_stat = 0

 for pattern in unique_patterns:
 mask = patterns == pattern
 sub_df = numeric_df[mask]
 n_j = len(sub_df)
 if n_j < 2:
 continue

 # 'scolumn
 obs_cols = [i for i, m in enumerate(pattern) if not m]
 if len(obs_cols) == 0:
 continue

 obs_mean = sub_df.iloc[:, obs_cols].mean.values
 exp_mean = global_mean.iloc[obs_cols].values
 diff = obs_mean - exp_mean

 obs_cov = global_cov.iloc[obs_cols, obs_cols].values
 try:
 cov_inv = np.linalg.pinv(obs_cov / n_j)
 except np.linalg.LinAlgError:
 continue

 chi2_stat += diff @ cov_inv @ diff
 df_stat += len(obs_cols)

 df_stat -= n_cols # degreecorrection

 if df_stat <= 0:
 return {"chi2": np.nan, "p_value": np.nan,
 "conclusion": " (degree)"}

 p_value = 1 - stats.chi2.cdf(chi2_stat, df_stat)
 conclusion = "MCAR (p > 0.05)" if p_value > 0.05 else "Not MCAR (p ≤ 0.05)"

 print(f"Little's MCAR test: χ²={chi2_stat:.2f}, df={df_stat}, "
 f"p={p_value:.4f} → {conclusion}")
 return {"chi2": chi2_stat, "df": df_stat,
 "p_value": p_value, "conclusion": conclusion}
```

## 3. method (MICE)

```python
def mice_imputation(df, n_imputations=5, max_iter=10, random_state=42):
 """
 MICE (Multiple Imputation by Chained Equations)。

 Parameters:
 df: pd.DataFrame — data with missing values
 n_imputations: int — datasetnumber/count
 max_iter: int — timesnumber/count
 random_state: int — random seed
 """
 from sklearn.experimental import enable_iterative_imputer # noqa
 from sklearn.impute import IterativeImputer

 numeric_cols = df.select_dtypes(include=[np.number]).columns
 cat_cols = df.select_dtypes(exclude=[np.number]).columns

 imputed_datasets = []

 for i in range(n_imputations):
 imputer = IterativeImputer(
 max_iter=max_iter,
 random_state=random_state + i,
 sample_posterior=True)

 imputed_numeric = pd.DataFrame(
 imputer.fit_transform(df[numeric_cols]),
 columns=numeric_cols, index=df.index)

 imputed_df = imputed_numeric.copy
 for col in cat_cols:
 imputed_df[col] = df[col].fillna(df[col].mode.iloc[0]
 if not df[col].mode.empty else "UNKNOWN")

 imputed_datasets.append(imputed_df)

 print(f"MICE: {n_imputations} datasets × {max_iter} iterations, "
 f"{len(numeric_cols)} numeric cols")
 return imputed_datasets


def rubins_rules(estimates, variances):
 """
 Rubin's Rules — results'sintegration。

 Parameters:
 estimates: list[float] — eachdatasetfrom's value
 variances: list[float] — eachdatasetfrom'svariance
 """
 m = len(estimates)
 Q_bar = np.mean(estimates)
 U_bar = np.mean(variances) # Within-imputation variance
 B = np.var(estimates, ddof=1) # Between-imputation variance
 T = U_bar + (1 + 1 / m) * B # Total variance

 # degree (Barnard-Rubin)
 r = (1 + 1 / m) * B / U_bar if U_bar > 0 else np.inf
 df_old = (m - 1) * (1 + 1 / r) ** 2 if r > 0 else np.inf

 print(f"Rubin's Rules: Q̄={Q_bar:.4f}, T={T:.4f}, "
 f"within={U_bar:.4f}, between={B:.4f}")
 return {"pooled_estimate": Q_bar, "total_variance": T,
 "within_variance": U_bar, "between_variance": B,
 "df": df_old}
```

## 4. KNN / MissForest 

```python
def knn_imputation(df, n_neighbors=5):
 """
 KNN value。

 Parameters:
 df: pd.DataFrame — data with missing values
 n_neighbors: int — number/count
 """
 from sklearn.impute import KNNImputer

 numeric_cols = df.select_dtypes(include=[np.number]).columns
 imputer = KNNImputer(n_neighbors=n_neighbors)
 imputed = pd.DataFrame(
 imputer.fit_transform(df[numeric_cols]),
 columns=numeric_cols, index=df.index)

 n_imputed = df[numeric_cols].isnull.sum.sum
 print(f"KNN Imputation (k={n_neighbors}): {n_imputed} values imputed")
 return imputed


def missforest_imputation(df, n_estimators=100, max_iter=10):
 """
 MissForest (Random Forest 's)。

 Parameters:
 df: pd.DataFrame — data with missing values
 n_estimators: int — Random Forest 's 's number/count
 max_iter: int — timesnumber/count
 """
 from sklearn.experimental import enable_iterative_imputer # noqa
 from sklearn.impute import IterativeImputer
 from sklearn.ensemble import RandomForestRegressor

 numeric_cols = df.select_dtypes(include=[np.number]).columns

 imputer = IterativeImputer(
 estimator=RandomForestRegressor(n_estimators=n_estimators,
 random_state=42, n_jobs=-1),
 max_iter=max_iter, random_state=42)

 imputed = pd.DataFrame(
 imputer.fit_transform(df[numeric_cols]),
 columns=numeric_cols, index=df.index)

 n_imputed = df[numeric_cols].isnull.sum.sum
 print(f"MissForest (n_trees={n_estimators}, iter={max_iter}): "
 f"{n_imputed} values imputed")
 return imputed
```

---

## Pipeline Integration

```
eda-correlation → missing-data-analysis → ml-classification
 (search/explorationanalysis) (diagnosis) 
 │ │ ↓
 statistical-testing ────┘ advanced-visualization
 (testing) (resultsvisualization)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `missing_diagnosis.png` | visualization | → reporting |
| `mcar_test_result.json` | Little's MCAR testing | → selection |
| `imputed_datasets/` | MICE data | → ml-classification |
| `imputation_comparison.csv` | methodcomparison | → selection |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | datatoolsearch |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Data Analysis)

Before execution, define:
- [ ] **Input schema**: column names, types, expected ranges
- [ ] **Output schema**: expected result shape, key metrics to produce
- [ ] **Statistical validity**: significance level (alpha), power target, effect size threshold
- [ ] **Reproducibility**: random seed set, deterministic pipeline

#### Pass Criteria
- All statistical tests report p-values and confidence intervals
- Effect sizes reported alongside significance
- Multiple comparison corrections applied when > 2 tests
- Missing data handling documented (method + % impacted)
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
