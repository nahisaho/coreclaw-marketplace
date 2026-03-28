---
name: scientific-ml-regression
description: |
 ML regression skill. Linear/nonlinear regression, regularization (L1/L2/ElasticNet), polynomial features, cross-validation, and regression diagnostics pipelines.
---

# Scientific ML Regression Pipeline

multiple's regression framework evaluationcomparespipeline。
regression（multiple's outputnumber/countprediction） support。

## When to Use

- value'spredictiontask
- multiple'scomparisonwhen needed
- regression（multipleoutputnumber/count'sprediction）
- verificationby/viageneralization'sevaluation

## Quick Start

## Standard Pipeline

### 1. Model Definition

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import (RandomForestRegressor,
 GradientBoostingRegressor,
 ExtraTreesRegressor)
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np
import pandas as pd

MODEL_DEFS = {
 "Ridge": Ridge(alpha=1.0),
 "Lasso": Lasso(alpha=0.1, max_iter=10000),
 "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=15,
 random_state=42),
 "Gradient Boosting": GradientBoostingRegressor(n_estimators=200,
 random_state=42),
 "Extra Trees": ExtraTreesRegressor(n_estimators=200, max_depth=15,
 random_state=42),
}
```

### 2. & evaluation

```python
def train_evaluate_models(X_train, X_test, y_train, y_test,
 target_names, model_defs=None, n_splits=5):
 """
 all × all's evaluationexecutes。
 Returns: results_df (×'sevaluation metric), best_models dict
 """
 if model_defs is None:
 model_defs = MODEL_DEFS

 scaler = StandardScaler
 X_train_sc = scaler.fit_transform(X_train)
 X_test_sc = scaler.transform(X_test)

 results = []
 best_models = {}
 kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

 for target in target_names:
 y_tr = y_train[target].values
 y_te = y_test[target].values
 best_r2 = -np.inf

 for name, model in model_defs.items:
 import copy
 m = copy.deepcopy(model)
 m.fit(X_train_sc, y_tr)
 y_pred = m.predict(X_test_sc)

 r2 = r2_score(y_te, y_pred)
 rmse = np.sqrt(mean_squared_error(y_te, y_pred))
 mae = mean_absolute_error(y_te, y_pred)

 # verification
 cv_scores = cross_val_score(
 copy.deepcopy(model), X_train_sc, y_tr,
 cv=kf, scoring="neg_root_mean_squared_error"
 )
 cv_rmse_mean = -cv_scores.mean
 cv_rmse_std = cv_scores.std

 results.append({
 "Target": target,
 "Model": name,
 "R2": r2,
 "RMSE": rmse,
 "MAE": mae,
 "CV_RMSE_mean": cv_rmse_mean,
 "CV_RMSE_std": cv_rmse_std,
 })

 if r2 > best_r2:
 best_r2 = r2
 best_models[target] = {"model": m, "name": name, "r2": r2}

 results_df = pd.DataFrame(results)
 results_df.to_csv("results/model_metrics.csv", index=False)
 return results_df, best_models
```

### 3. comparisonvisualization（R² chart）

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_model_comparison_r2(results_df, figsize=(14, 6)):
 """R² 's grouped bar chart drawing/plotting."""
 pivot = results_df.pivot(index="Target", columns="Model", values="R2")
 ax = pivot.plot(kind="bar", figsize=figsize, colormap="Set2", edgecolor="black")
 ax.set_ylabel("R² Score")
 ax.set_title("Model Comparison: R² by Target", fontweight="bold")
 ax.set_ylim(0, 1.05)
 ax.legend(title="Model", bbox_to_anchor=(1.05, 1))
 ax.axhline(y=0.8, color="gray", linestyle="--", alpha=0.5, label="R²=0.8")
 plt.xticks(rotation=45, ha="right")
 plt.tight_layout
 plt.savefig("figures/model_comparison_r2.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 4. Actual vs Predicted plot

```python
def plot_actual_vs_predicted(X_test_sc, y_test, best_models, target_names,
 ncols=3, figsize=(18, 12)):
 """'s value vs predictionvalueplotdrawing/plotting."""
 nrows = (len(target_names) + ncols - 1) // ncols
 fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
 axes = axes.flatten

 for i, target in enumerate(target_names):
 m = best_models[target]["model"]
 y_pred = m.predict(X_test_sc)
 y_true = y_test[target].values
 r2 = best_models[target]["r2"]

 axes[i].scatter(y_true, y_pred, alpha=0.5, s=20, edgecolors="k", linewidth=0.3)
 lims = [min(y_true.min, y_pred.min), max(y_true.max, y_pred.max)]
 axes[i].plot(lims, lims, "r--", linewidth=1.5)
 axes[i].set_xlabel("Actual")
 axes[i].set_ylabel("Predicted")
 axes[i].set_title(f"{target}\n({best_models[target]['name']}, R²={r2:.3f})",
 fontsize=10, fontweight="bold")

 for j in range(i + 1, len(axes)):
 axes[j].set_visible(False)

 plt.tight_layout
 plt.savefig("figures/actual_vs_predicted.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 5. chartcomparison（Exp-05 ）

```python
def plot_radar_comparison(results_df, target_name, figsize=(8, 8)):
 """specification's comparisonchartdrawing/plotting."""
 subset = results_df[results_df["Target"] == target_name]
 metrics = ["R2", "1-RMSE_norm", "1-MAE_norm", "Stability"]

 # normalization（all 0-1, high good ）
 subset = subset.copy
 for col in ["RMSE", "MAE"]:
 max_val = subset[col].max
 subset[f"1-{col}_norm"] = 1 - subset[col] / max_val if max_val > 0 else 1
 subset["Stability"] = 1 - subset["CV_RMSE_std"] / subset["CV_RMSE_mean"]

 N = len(metrics)
 angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist
 angles += angles[:1]

 fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

 for _, row in subset.iterrows:
 values = [row[m] for m in metrics] + [row[metrics[0]]]
 ax.plot(angles, values, "o-", linewidth=2, label=row["Model"])
 ax.fill(angles, values, alpha=0.1)

 ax.set_xticks(angles[:-1])
 ax.set_xticklabels(metrics)
 ax.set_title(f"Radar: {target_name}", fontweight="bold")
 ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
 plt.tight_layout
 plt.savefig(f"figures/radar_{target_name}.png", dpi=300, bbox_inches="tight")
 plt.close
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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

## References

### Output Files

| File | Format |
|---|---|
| `results/model_metrics.csv` | CSV |
| `figures/model_comparison_r2.png` | PNG |
| `figures/actual_vs_predicted.png` | PNG |
| `figures/radar_*.png` | PNG |

#### Reference Experiments

- **Exp-12**: 6 × 4 （）
- **Exp-13**: 5 × 6 （PSP structureproperties）
- **Exp-05**: chartby/viacomparison
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (ML/AI)

Before execution, define:
- [ ] **Task type**: classification / regression / generation / ranking
- [ ] **Baseline**: naive baseline metric to beat
- [ ] **Target metric**: specific threshold (e.g., AUC > 0.85, RMSE < 0.1)
- [ ] **Data split**: train/val/test ratios, stratification method

#### Pass Criteria
- Model performance exceeds baseline by defined margin
- Train/val/test metrics all reported (no data leakage)
- Hyperparameters logged with search method
- Overfitting check: train-val gap < 10% relative
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
