---
name: scientific-feature-importance
description: |
 featuresimportantdegreemin'sskill。Tree-based Feature Importance and Permutation Importance 
 forprediction's explainability for。
 Scientific Skills Exp-05, 12, 13 。
---

# Scientific Feature Importance Analysis

machine learning's 「's features prediction also」 amountskill。
Tree-based Importance（MDI） and Permutation Importance 's 2 method for
 is provided。

## When to Use

- machine learning's predictionresultswhen needed
- 's processparameters also items and
- featuresselection's basiswhen needed
- multiplenumber/countfor/againstimportantdegree'scomparison

## Quick Start

## Standard Pipeline

### 1. Tree-based Feature Importance（MDI）

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def tree_feature_importance(model, feature_names, target_name,
 top_n=10, figsize=(10, 6)):
 """
 Tree 's.feature_importances_ retrievalbar chart drawing/plotting.
 RandomForest, GradientBoosting, ExtraTrees support。
 """
 importances = model.feature_importances_
 fi_df = pd.DataFrame({
 "Feature": feature_names,
 "Importance": importances,
 }).sort_values("Importance", ascending=False)

 fig, ax = plt.subplots(figsize=figsize)
 top = fi_df.head(top_n)
 ax.barh(range(len(top)), top["Importance"].values[::-1],
 color="steelblue", edgecolor="black")
 ax.set_yticks(range(len(top)))
 ax.set_yticklabels(top["Feature"].values[::-1])
 ax.set_xlabel("Feature Importance (MDI)")
 ax.set_title(f"Feature Importance: {target_name}", fontweight="bold")
 plt.tight_layout
 plt.savefig(f"figures/feature_importance_{target_name}.png",
 dpi=300, bbox_inches="tight")
 plt.close

 return fi_df
```

### 2. Permutation Importance

```python
from sklearn.inspection import permutation_importance

def permutation_feature_importance(model, X_test, y_test, feature_names,
 target_name, n_repeats=10,
 top_n=10, figsize=(10, 6)):
 """
 Permutation Importance 。's type forpossible。
 """
 result = permutation_importance(model, X_test, y_test,
 n_repeats=n_repeats, random_state=42)
 pi_df = pd.DataFrame({
 "Feature": feature_names,
 "Importance_mean": result.importances_mean,
 "Importance_std": result.importances_std,
 }).sort_values("Importance_mean", ascending=False)

 fig, ax = plt.subplots(figsize=figsize)
 top = pi_df.head(top_n)
 ax.barh(range(len(top)), top["Importance_mean"].values[::-1],
 xerr=top["Importance_std"].values[::-1],
 color="coral", edgecolor="black", capsize=3)
 ax.set_yticks(range(len(top)))
 ax.set_yticklabels(top["Feature"].values[::-1])
 ax.set_xlabel("Permutation Importance")
 ax.set_title(f"Permutation Importance: {target_name}", fontweight="bold")
 plt.tight_layout
 plt.savefig(f"figures/permutation_importance_{target_name}.png",
 dpi=300, bbox_inches="tight")
 plt.close

 return pi_df
```

### 3. importantdegree（Exp-13 ）

```python
def multi_target_importance_panel(models_dict, feature_names,
 top_n=10, ncols=3, figsize=(20, 16)):
 """
 multiple's featuresimportantdegree items's Figure anddrawing/plotting.
 models_dict: {target_name: fitted_model}
 """
 targets = list(models_dict.keys)
 nrows = (len(targets) + ncols - 1) // ncols
 fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
 axes = axes.flatten

 all_importances = []

 for i, target in enumerate(targets):
 model = models_dict[target]
 if not hasattr(model, "feature_importances_"):
 axes[i].text(0.5, 0.5, f"{target}\n(No FI available)",
 ha="center", va="center", transform=axes[i].transAxes)
 continue

 importances = model.feature_importances_
 fi_df = pd.DataFrame({
 "Feature": feature_names,
 "Importance": importances,
 "Target": target,
 }).sort_values("Importance", ascending=False)

 all_importances.append(fi_df)

 top = fi_df.head(top_n)
 axes[i].barh(range(len(top)), top["Importance"].values[::-1],
 color="steelblue", edgecolor="black")
 axes[i].set_yticks(range(len(top)))
 axes[i].set_yticklabels(top["Feature"].values[::-1], fontsize=8)
 axes[i].set_xlabel("Importance", fontsize=9)
 axes[i].set_title(target, fontweight="bold", fontsize=10)

 for j in range(i + 1, len(axes)):
 axes[j].set_visible(False)

 plt.suptitle("Feature Importance by Target", fontsize=14, fontweight="bold")
 plt.tight_layout
 plt.savefig("figures/feature_importance_panel.png", dpi=300, bbox_inches="tight")
 plt.close

 # allimportantdegree CSV save
 if all_importances:
 combined = pd.concat(all_importances, ignore_index=True)
 combined.to_csv("results/feature_importance.csv", index=False)
 return combined
 return pd.DataFrame
```

### 4. partialdependencyplot（PDP）

```python
from sklearn.inspection import PartialDependenceDisplay

def partial_dependence_plots(model, X_train, feature_names,
 top_features, target_name, figsize=(16, 10)):
 """topfeatures's partialdependencyplotdrawing/plotting."""
 feature_indices = [list(feature_names).index(f) for f in top_features
 if f in feature_names]

 fig, ax = plt.subplots(figsize=figsize)
 PartialDependenceDisplay.from_estimator(
 model, X_train, feature_indices,
 feature_names=feature_names, ax=ax
 )
 plt.suptitle(f"Partial Dependence: {target_name}", fontweight="bold")
 plt.tight_layout
 plt.savefig(f"figures/pdp_{target_name}.png", dpi=300, bbox_inches="tight")
 plt.close
```

## parameters–propertiesmappingtable's automatedgeneration

```python
def generate_importance_mapping_table(all_fi_df, top_n=3):
 """each'stop N featuresandsupporttable is generated。"""
 mapping = []
 for target in all_fi_df["Target"].unique:
 subset = all_fi_df[all_fi_df["Target"] == target].nlargest(top_n, "Importance")
 for rank, (_, row) in enumerate(subset.iterrows, 1):
 mapping.append({
 "Target": target,
 f"Rank_{rank}": row["Feature"],
 f"Importance_{rank}": f"{row['Importance']:.4f}",
 })
 return pd.DataFrame(mapping)
```

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

## References

### Output Files

| File | Format |
|---|---|
| `results/feature_importance.csv` | CSV |
| `figures/feature_importance_*.png` | PNG |
| `figures/permutation_importance_*.png` | PNG |
| `figures/feature_importance_panel.png` | PNG |
| `figures/pdp_*.png` | PNG |

#### Reference Experiments

- **Exp-05**: Tree-based + Permutation Importance（toxicityprediction）
- **Exp-12**: 6 's featuresimportantdegreecomparison（）
- **Exp-13**: + parameters–propertiesmappingtable
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
