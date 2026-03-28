---
name: scientific-data-profiling
description: |
 dataskill。ydata-profiling automated EDA 
 Great Expectations datadata
 typeinferencecorrelationvaluedataloggeneration。
---

# Scientific Data Profiling

dataset's evaluation
automated EDA reportpipeline is provided。

## When to Use

- dataset's allwhen needed
- datacriteriawhen needed
- ydata-profiling automated EDA report is generatedand
- Great Expectations data is definedand
- datalog  automatedgenerationwhen needed
- correlationvaluediagnosiswhen needed

---

## Quick Start

## 1. ydata-profiling automated EDA

```python
import numpy as np
import pandas as pd


def auto_profile_report(df, title="Data Profile Report",
 minimal=False, output="profile_report.html"):
 """
 ydata-profiling automated EDA report。

 Parameters:
 df: pd.DataFrame — input data
 title: str — reporttitle
 minimal: bool — amount
 output: str — output HTML 
 """
 from ydata_profiling import ProfileReport

 profile = ProfileReport(
 df, title=title, minimal=minimal,
 correlations={"pearson": {"calculate": True},
 "spearman": {"calculate": True},
 "kendall": {"calculate": True}},
 missing_diagrams={"bar": True, "matrix": True, "heatmap": True})

 profile.to_file(output)

 # summaryextraction
 desc = profile.get_description
 summary = {
 "n_rows": len(df),
 "n_cols": len(df.columns),
 "n_numeric": len(df.select_dtypes(include=[np.number]).columns),
 "n_categorical": len(df.select_dtypes(include=["object", "category"]).columns),
 "total_missing": int(df.isnull.sum.sum),
 "missing_pct": float(df.isnull.sum.sum / (len(df) * len(df.columns)) * 100),
 "n_duplicates": int(df.duplicated.sum),
 }

 print(f"Profile Report → {output}")
 print(f" {summary['n_rows']} rows × {summary['n_cols']} cols, "
 f"{summary['missing_pct']:.1f}% missing, "
 f"{summary['n_duplicates']} duplicates")
 return {"report_path": output, "summary": summary}
```

## 2. data

```python
def data_quality_score(df, rules=None):
 """
 data (0-100)。

 Parameters:
 df: pd.DataFrame — input data
 rules: dict | None — custom
 """
 scores = {}

 # 1. all (Completeness) — rate
 completeness = 1.0 - df.isnull.sum.sum / (len(df) * len(df.columns))
 scores["completeness"] = completeness

 # 2. (Uniqueness) — rate
 uniqueness = 1.0 - df.duplicated.sum / len(df) if len(df) > 0 else 1.0
 scores["uniqueness"] = uniqueness

 # 3. (Consistency) — type
 type_consistent = 0
 for col in df.columns:
 non_null = df[col].dropna
 if len(non_null) == 0:
 type_consistent += 1
 continue
 try:
 inferred = pd.api.types.infer_dtype(non_null, skipna=True)
 if inferred not in ["mixed", "mixed-integer"]:
 type_consistent += 1
 except Exception:
 pass
 consistency = type_consistent / len(df.columns) if len(df.columns) > 0 else 1.0
 scores["consistency"] = consistency

 # 4. (Timeliness) — date column's
 date_cols = df.select_dtypes(include=["datetime64"]).columns
 if len(date_cols) > 0:
 max_date = df[date_cols[0]].max
 freshness = 1.0 # Placeholder
 scores["timeliness"] = freshness
 else:
 scores["timeliness"] = 1.0

 # 5. (Validity) — number/countvalue column's
 numeric_cols = df.select_dtypes(include=[np.number]).columns
 if len(numeric_cols) > 0:
 finite_rate = df[numeric_cols].apply(lambda x: np.isfinite(x.dropna).mean).mean
 scores["validity"] = float(finite_rate)
 else:
 scores["validity"] = 1.0

 # 
 weights = {"completeness": 0.3, "uniqueness": 0.2,
 "consistency": 0.2, "timeliness": 0.1, "validity": 0.2}
 total_score = sum(scores[k] * weights[k] for k in weights) * 100

 # custom
 rule_results = []
 if rules:
 for rule_name, rule_fn in rules.items:
 try:
 passed = rule_fn(df)
 rule_results.append({"rule": rule_name, "passed": passed})
 except Exception as e:
 rule_results.append({"rule": rule_name, "passed": False,
 "error": str(e)})

 print(f"Data Quality Score: {total_score:.1f}/100")
 for k, v in scores.items:
 print(f" {k}: {v:.3f}")

 return {"total_score": total_score, "dimension_scores": scores,
 "rule_results": rule_results}
```

## 3. Great Expectations 

```python
def great_expectations_validate(df, expectations=None):
 """
 Great Expectations 's data。

 Parameters:
 df: pd.DataFrame — input data
 expectations: list[dict] | None — 
 """
 if expectations is None:
 expectations = _auto_generate_expectations(df)

 results = []
 for exp in expectations:
 exp_type = exp["type"]
 col = exp.get("column")
 kwargs = exp.get("kwargs", {})

 try:
 if exp_type == "expect_column_to_exist":
 success = col in df.columns
 elif exp_type == "expect_column_values_to_not_be_null":
 max_pct = kwargs.get("mostly", 1.0)
 non_null_pct = df[col].notnull.mean
 success = non_null_pct >= max_pct
 elif exp_type == "expect_column_values_to_be_between":
 min_val, max_val = kwargs["min_value"], kwargs["max_value"]
 vals = df[col].dropna
 success = bool((vals >= min_val).all and (vals <= max_val).all)
 elif exp_type == "expect_column_values_to_be_unique":
 success = not df[col].duplicated.any
 elif exp_type == "expect_column_values_to_be_in_set":
 valid_set = set(kwargs["value_set"])
 success = df[col].dropna.isin(valid_set).all
 elif exp_type == "expect_table_row_count_to_be_between":
 success = kwargs["min_value"] <= len(df) <= kwargs["max_value"]
 else:
 success = None

 results.append({"expectation": exp_type, "column": col,
 "success": success})
 except Exception as e:
 results.append({"expectation": exp_type, "column": col,
 "success": False, "error": str(e)})

 results_df = pd.DataFrame(results)
 n_pass = results_df["success"].sum
 n_total = len(results_df)
 print(f"Validation: {n_pass}/{n_total} expectations passed "
 f"({n_pass/n_total*100:.0f}%)")
 return results_df


def _auto_generate_expectations(df):
 """automatedinference。"""
 expectations = []
 for col in df.columns:
 expectations.append({"type": "expect_column_to_exist", "column": col})
 expectations.append({
 "type": "expect_column_values_to_not_be_null",
 "column": col,
 "kwargs": {"mostly": 0.9}})

 if df[col].dtype in [np.float64, np.int64]:
 q1, q3 = df[col].quantile([0.01, 0.99])
 iqr = q3 - q1
 expectations.append({
 "type": "expect_column_values_to_be_between",
 "column": col,
 "kwargs": {"min_value": float(q1 - 3 * iqr),
 "max_value": float(q3 + 3 * iqr)}})
 return expectations
```

---

## Pipeline Integration

```
[Data Retrieval] → data-profiling → eda-correlation
 (diagnosis) (search/explorationanalysis)
 │ ↓
 missing-data-analysis anomaly-detection
  (anomaly detection)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `profile_report.html` | ydata-profiling report | → EDA |
| `quality_score.json` | data | → quality control |
| `validation_results.csv` | results | → datafix |

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

---

## Harness Optimization (v0.5.0)

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
