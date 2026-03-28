---
name: scientific-data-preprocessing
description: |
 Data preprocessing skill. Missing value imputation, outlier detection, normalization, feature scaling, encoding, and data cleaning pipelines for scientific datasets.
tu_tools:
 - key: biotools
 name: bio.tools
 description: datapreprocessingTool Registry Search
---

# Scientific Data Preprocessing

dataanalysisinpreprocessing'sStandard Pipeline。data、transformation、normalization's
's procedure itemspossibleshape implementationfortemplate。
all Exp-01〜13 asforskill。

## When to Use

- CSV / DataFrame 's data analysistransformationwhen needed
- value's selectionnecessary and
- number/count'sencodingwhen needed
- number/countvaluedata'snormalizationwhen needed
- value'swhen needed

## Quick Start

## 1. preprocessingpipelineoverview

```
Raw Data
 ├─ Step 1: data
 ├─ Step 2: value
 ├─ Step 3: value
 ├─ Step 4: encoding
 ├─ Step 5: / transformation
 └─ Step 6: verificationreport
```

## 2. data

```python
import pandas as pd
import numpy as np

def data_quality_report(df, name="dataset"):
 """
 datareportoutput.
 preprocessing's as executes and。
 """
 report = pd.DataFrame({
 "dtype": df.dtypes,
 "nunique": df.nunique,
 "missing_count": df.isnull.sum,
 "missing_pct": (df.isnull.sum / len(df) * 100).round(2),
 "zeros_count": (df == 0).sum,
 })

 # number/countvalue column's
 numeric_cols = df.select_dtypes(include=[np.number]).columns
 for col in numeric_cols:
 report.loc[col, "mean"] = df[col].mean
 report.loc[col, "std"] = df[col].std
 report.loc[col, "skewness"] = df[col].skew
 report.loc[col, "kurtosis"] = df[col].kurtosis

 print(f"=== Data Quality Report: {name} ===")
 print(f"Shape: {df.shape}")
 print(f"Duplicated rows: {df.duplicated.sum}")
 print(f"Columns with >50% missing: "
 f"{report[report['missing_pct'] > 50].index.tolist}")
 print(report.to_string)

 return report
```

## 3. value — selection

| method | | cautionpoint |
|---|---|---|
| `dropna` | allanalysis、 <5% | sample size |
| `fillna(median)` | number/countvaluedata、value | distribution |
| `fillna(mean)` | number/countvaluedata、normal distribution | value |
| `SimpleImputer(strategy='most_frequent')` | number/count | |
| `KNNImputer(n_neighbors=5)` | number/count correlation | calculationhigh |
| `IterativeImputer` | amount (MICE) | scikit-learn experimental |

```python
from sklearn.impute import SimpleImputer, KNNImputer

def handle_missing_values(df, strategy="auto", numeric_cols=None, categorical_cols=None):
 """
 valuepipeline。

 strategy:
 "auto" — rateautomatedselection
 "drop" — 
 "median" — median
 "knn" — KNN (n_neighbors=5)
 """
 df = df.copy

 if numeric_cols is None:
 numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist
 if categorical_cols is None:
 categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist

 if strategy == "auto":
 missing_pct = df[numeric_cols].isnull.mean
 # columnand for
 low_missing = missing_pct[missing_pct < 0.05].index.tolist
 mid_missing = missing_pct[(missing_pct >= 0.05) & (missing_pct < 0.30)].index.tolist
 high_missing = missing_pct[missing_pct >= 0.30].index.tolist

 # Low: median
 if low_missing:
 imp = SimpleImputer(strategy="median")
 df[low_missing] = imp.fit_transform(df[low_missing])

 # Mid: KNN 
 if mid_missing:
 imp = KNNImputer(n_neighbors=5)
 df[mid_missing] = imp.fit_transform(df[mid_missing])

 # High: warningtable's (recommended)
 if high_missing:
 print(f"WARNING: High missing rate columns ({'>30%'}): {high_missing}")
 print("Consider dropping these columns or using domain-specific imputation.")

 elif strategy == "drop":
 df = df.dropna(subset=numeric_cols)

 elif strategy == "median":
 imp = SimpleImputer(strategy="median")
 df[numeric_cols] = imp.fit_transform(df[numeric_cols])

 elif strategy == "knn":
 imp = KNNImputer(n_neighbors=5)
 df[numeric_cols] = imp.fit_transform(df[numeric_cols])

 # number/count → value
 if categorical_cols:
 imp_cat = SimpleImputer(strategy="most_frequent")
 df[categorical_cols] = imp_cat.fit_transform(df[categorical_cols])

 return df
```

## 4. value

```python
def detect_outliers(df, columns, method="iqr", threshold=1.5):
 """
 value.

 method:
 "iqr" — IQRmethod (Q1 - threshold*IQR, Q3 + threshold*IQR)
 "zscore" — Z-score method (|z| > threshold; default threshold=3)
 "mad" — MAD (Median Absolute Deviation) method
 """
 outlier_mask = pd.DataFrame(False, index=df.index, columns=columns)

 for col in columns:
 vals = df[col].dropna
 if method == "iqr":
 Q1, Q3 = vals.quantile(0.25), vals.quantile(0.75)
 IQR = Q3 - Q1
 lower, upper = Q1 - threshold * IQR, Q3 + threshold * IQR
 outlier_mask[col] = (df[col] < lower) | (df[col] > upper)

 elif method == "zscore":
 z = np.abs((df[col] - vals.mean) / vals.std)
 outlier_mask[col] = z > (threshold if threshold != 1.5 else 3)

 elif method == "mad":
 median = vals.median
 mad = np.median(np.abs(vals - median))
 modified_z = 0.6745 * (df[col] - median) / (mad + 1e-10)
 outlier_mask[col] = np.abs(modified_z) > (threshold if threshold != 1.5 else 3.5)

 summary = pd.DataFrame({
 "outlier_count": outlier_mask.sum,
 "outlier_pct": (outlier_mask.sum / len(df) * 100).round(2),
 })

 return outlier_mask, summary


def handle_outliers(df, columns, method="iqr", action="clip"):
 """
 value is processed。

 action:
 "clip" — value
 "remove" — value
 "nan" — NaN （）
 """
 outlier_mask, summary = detect_outliers(df, columns, method=method)
 df = df.copy

 if action == "remove":
 any_outlier = outlier_mask.any(axis=1)
 df = df[~any_outlier]

 elif action == "clip":
 for col in columns:
 vals = df[col].dropna
 Q1, Q3 = vals.quantile(0.25), vals.quantile(0.75)
 IQR = Q3 - Q1
 lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
 df[col] = df[col].clip(lower, upper)

 elif action == "nan":
 for col in columns:
 df.loc[outlier_mask[col], col] = np.nan

 return df, summary
```

## 5. encoding — selection

| method | | forexample |
|---|---|---|
| `LabelEncoder` | 、system | crystal structure → 0,1,2 |
| `pd.get_dummies` | 、lineshape | → number/count |
| `OrdinalEncoder` | 's（explicit） | // → 0,1,2 |
| `TargetEncoder` | | compound ID |

```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

def encode_categorical(df, columns, method="auto"):
 """
 number/count'sencoding。

 method:
 "auto" — nunique automatedselection
 "label" — LabelEncoder
 "onehot" — pd.get_dummies
 "ordinal" — OrdinalEncoder
 """
 df = df.copy
 encoders = {}

 for col in columns:
 n_unique = df[col].nunique

 if method == "auto":
 chosen = "onehot" if n_unique <= 10 else "label"
 else:
 chosen = method

 if chosen == "label":
 le = LabelEncoder
 df[col] = le.fit_transform(df[col].astype(str))
 encoders[col] = le

 elif chosen == "onehot":
 dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
 df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

 elif chosen == "ordinal":
 oe = OrdinalEncoder
 df[col] = oe.fit_transform(df[[col]])
 encoders[col] = oe

 return df, encoders
```

## 6. transformation — selection

| method | number/countformula | |
|---|---|---|
| `StandardScaler` | $(x - \mu) / \sigma$ | PCA 、normal distribution |
| `MinMaxScaler` | $(x - x_{min}) / (x_{max} - x_{min})$ | NN input、0〜1 normalization |
| `RobustScaler` | $(x - Q_2) / (Q_3 - Q_1)$ | value |
| Pareto Scaling | $(x - \bar{x}) / \sqrt{s}$ | (Exp-07) |
| Log2 Transform | $\log_2(x + 1)$ | expression leveldata |
| Box-Cox | $(x^\lambda - 1)/\lambda$ | improvement（value's） |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def scale_features(df, columns, method="standard"):
 """
 features。

 method:
 "standard" — StandardScaler (z-score)
 "minmax" — MinMaxScaler (0-1)
 "robust" — RobustScaler (IQR-based)
 "pareto" — Pareto scaling (metabolomics )
 "log2" — log2(x + 1) transformation
 """
 df = df.copy
 scaler = None

 if method == "standard":
 scaler = StandardScaler
 df[columns] = scaler.fit_transform(df[columns])

 elif method == "minmax":
 scaler = MinMaxScaler
 df[columns] = scaler.fit_transform(df[columns])

 elif method == "robust":
 scaler = RobustScaler
 df[columns] = scaler.fit_transform(df[columns])

 elif method == "pareto":
 # Pareto scaling: (x - mean) / sqrt(std)
 for col in columns:
 mean = df[col].mean
 std = df[col].std
 df[col] = (df[col] - mean) / np.sqrt(std + 1e-10)

 elif method == "log2":
 for col in columns:
 df[col] = np.log2(df[col] + 1)

 return df, scaler
```

## 7. preprocessingPipeline Integrationtemplate

```python
def preprocessing_pipeline(df, target_col=None, config=None):
 """
 allpreprocessingpipeline。settings possible。

 config example:
 {
 "drop_duplicates": True,
 "missing_strategy": "auto",
 "outlier_method": "iqr",
 "outlier_action": "clip",
 "encoding_method": "auto",
 "scaling_method": "standard",
 }
 """
 if config is None:
 config = {
 "drop_duplicates": True,
 "missing_strategy": "auto",
 "outlier_method": "iqr",
 "outlier_action": "clip",
 "encoding_method": "auto",
 "scaling_method": "standard",
 }

 n_original = len(df)

 # Step 0: 
 if config.get("drop_duplicates", True):
 df = df.drop_duplicates
 print(f" Removed {n_original - len(df)} duplicate rows")

 # Step 1: columnclassification
 numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist
 categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist
 if target_col and target_col in numeric_cols:
 numeric_cols.remove(target_col)
 if target_col and target_col in categorical_cols:
 categorical_cols.remove(target_col)

 # Step 2: value
 df = handle_missing_values(
 df,
 strategy=config.get("missing_strategy", "auto"),
 numeric_cols=numeric_cols,
 categorical_cols=categorical_cols,
 )

 # Step 3: value
 if numeric_cols:
 df, outlier_summary = handle_outliers(
 df, numeric_cols,
 method=config.get("outlier_method", "iqr"),
 action=config.get("outlier_action", "clip"),
 )

 # Step 4: encoding
 if categorical_cols:
 df, encoders = encode_categorical(
 df, categorical_cols,
 method=config.get("encoding_method", "auto"),
 )
 else:
 encoders = {}

 # Step 5: 
 final_numeric = df.select_dtypes(include=[np.number]).columns.tolist
 if target_col and target_col in final_numeric:
 final_numeric.remove(target_col)
 if final_numeric:
 df, scaler = scale_features(
 df, final_numeric,
 method=config.get("scaling_method", "standard"),
 )
 else:
 scaler = None

 print(f" Preprocessing complete: {df.shape}")

 # : preprocessingdata（Pipeline Integrationfor）
 from pathlib import Path
 results_dir = Path("results")
 results_dir.mkdir(parents=True, exist_ok=True)
 df.to_csv(results_dir / "preprocessed_data.csv", index=False)
 print(f" ✔ Preprocessed data saved: results/preprocessed_data.csv ({df.shape})")

 # preprocessingsummaryJSONsave
 import json
 summary = {
 "original_shape": [n_original, len(df.columns)],
 "processed_shape": list(df.shape),
 "duplicates_removed": n_original - len(df) if config.get("drop_duplicates", True) else 0,
 "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
 "categorical_columns": len(df.select_dtypes(include=["object", "category"]).columns),
 "scaling_method": config.get("scaling_method", "standard"),
 "missing_strategy": config.get("missing_strategy", "auto"),
 }
 with open(results_dir / "preprocessing_summary.json", "w") as f:
 json.dump(summary, f, indent=2, ensure_ascii=False)
 print(f" ✔ Preprocessing summary saved: results/preprocessing_summary.json")

 return df, {"encoders": encoders, "scaler": scaler}
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | datapreprocessingTool Registry Search |

## References

- **Exp-01**: `sc.pp.normalize_total`, `sc.pp.log1p` — scRNA-seq 'snormalization
- **Exp-02**: `LabelEncoder`, `pd.get_dummies` — compoundencoding
- **Exp-03**: `StandardScaler` + `log2(x+1)` — cancerdatapreprocessing
- **Exp-05**: `StandardScaler`, `KNNImputer` — toxicitypredictiondata
- **Exp-07**: Pareto scaling — data
- **Exp-12**: `MinMaxScaler`, `RobustScaler` — processdata
- **Exp-13**: `LabelEncoder`, number/count — encoding
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
