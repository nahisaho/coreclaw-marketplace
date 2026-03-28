---
name: scientific-ml-classification
description: |
 machine learningclassificationpipeline's skill。multiple's classification（Logistic Regression, Random Forest,
 SVM, XGBoost） StratifiedKFold verification comparison、ROC curveline evaluates for。
 Scientific Skills Exp-03, 05 。
---

# Scientific ML Classification Pipeline

/classificationtaskfor ML pipeline。
StratifiedKFold verification multiple comparison、ROC-AUC andevaluates。

## When to Use

- predictiontask（valueclassificationclassification）
- cancerclassification、toxicityprediction、classificationetc.'s problem
- multipleclassification'scomparisonwhen needed

## Quick Start

## Standard Pipeline

### 1. Model Definition

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
 f1_score, roc_auc_score, roc_curve,
 confusion_matrix, classification_report)

MODEL_DEFS = {
 "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
 "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=15,
 random_state=42),
 "Gradient Boosting": GradientBoostingClassifier(n_estimators=200,
 random_state=42),
 "SVM": SVC(kernel="rbf", probability=True, random_state=42),
}
```

### 2. StratifiedKFold & evaluation

```python
import numpy as np
import pandas as pd

def train_evaluate_classifiers(X_train, X_test, y_train, y_test,
 model_defs=None, n_splits=5):
 """allclassification StratifiedKFold evaluates。"""
 if model_defs is None:
 model_defs = MODEL_DEFS

 scaler = StandardScaler
 X_train_sc = scaler.fit_transform(X_train)
 X_test_sc = scaler.transform(X_test)

 skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
 results = []
 trained_models = {}

 for name, model in model_defs.items:
 import copy
 m = copy.deepcopy(model)
 m.fit(X_train_sc, y_train)
 y_pred = m.predict(X_test_sc)
 y_proba = m.predict_proba(X_test_sc)[:, 1] if hasattr(m, "predict_proba") else None

 cv_scores = cross_val_score(copy.deepcopy(model), X_train_sc, y_train,
 cv=skf, scoring="accuracy")

 results.append({
 "Model": name,
 "Accuracy": accuracy_score(y_test, y_pred),
 "Precision": precision_score(y_test, y_pred, average="weighted"),
 "Recall": recall_score(y_test, y_pred, average="weighted"),
 "F1": f1_score(y_test, y_pred, average="weighted"),
 "ROC_AUC": roc_auc_score(y_test, y_proba) if y_proba is not None else np.nan,
 "CV_Accuracy_mean": cv_scores.mean,
 "CV_Accuracy_std": cv_scores.std,
 })
 trained_models[name] = {"model": m, "y_pred": y_pred, "y_proba": y_proba}

 results_df = pd.DataFrame(results)
 results_df.to_csv("results/classification_metrics.csv", index=False)
 return results_df, trained_models
```

### 3. ROC curveline

```python
import matplotlib.pyplot as plt

def plot_roc_curves(y_test, trained_models, figsize=(8, 8)):
 """all's ROC curvelinedrawing/plotting."""
 fig, ax = plt.subplots(figsize=figsize)

 for name, info in trained_models.items:
 if info["y_proba"] is not None:
 fpr, tpr, _ = roc_curve(y_test, info["y_proba"])
 auc = roc_auc_score(y_test, info["y_proba"])
 ax.plot(fpr, tpr, linewidth=2, label=f"{name} (AUC={auc:.3f})")

 ax.plot([0, 1], [0, 1], "k--", linewidth=1)
 ax.set_xlabel("False Positive Rate")
 ax.set_ylabel("True Positive Rate")
 ax.set_title("ROC Curves", fontweight="bold")
 ax.legend
 plt.tight_layout
 plt.savefig("figures/roc_curves.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 4. 

```python
import seaborn as sns

def plot_confusion_matrices(y_test, trained_models, class_names=None,
 ncols=2, figsize=(14, 12)):
 """all's gridtable."""
 n_models = len(trained_models)
 nrows = (n_models + ncols - 1) // ncols
 fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
 axes = axes.flatten

 for i, (name, info) in enumerate(trained_models.items):
 cm = confusion_matrix(y_test, info["y_pred"])
 sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[i],
 xticklabels=class_names, yticklabels=class_names)
 axes[i].set_title(name, fontweight="bold")
 axes[i].set_xlabel("Predicted")
 axes[i].set_ylabel("Actual")

 for j in range(i + 1, len(axes)):
 axes[j].set_visible(False)

 plt.tight_layout
 plt.savefig("figures/confusion_matrices.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 5. Precision-Recall curveline

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

def plot_precision_recall_curves(y_test, trained_models, figsize=(8, 8)):
 """all's Precision-Recall curvelinedrawing/plotting.
 data ROC than also PR curvelineevaluation metricand 。"""
 fig, ax = plt.subplots(figsize=figsize)

 for name, info in trained_models.items:
 if info["y_proba"] is not None:
 precision, recall, _ = precision_recall_curve(y_test, info["y_proba"])
 ap = average_precision_score(y_test, info["y_proba"])
 ax.plot(recall, precision, linewidth=2,
 label=f"{name} (AP={ap:.3f})")

 # （rate）
 baseline = y_test.mean
 ax.axhline(baseline, color="gray", linestyle="--", linewidth=1,
 label=f"Baseline ({baseline:.3f})")

 ax.set_xlabel("Recall")
 ax.set_ylabel("Precision")
 ax.set_title("Precision-Recall Curves", fontweight="bold")
 ax.legend
 ax.set_xlim([0, 1])
 ax.set_ylim([0, 1.05])
 plt.tight_layout
 plt.savefig("figures/precision_recall_curves.png", dpi=300,
 bbox_inches="tight")
 plt.close
```

### 6. Partial Dependence Plot (PDP)

```python
from sklearn.inspection import PartialDependenceDisplay

def plot_partial_dependence(model, X_train_scaled, feature_names,
 top_n=6, figsize=(14, 8)):
 """importantfeatures's partialdependencyplotdrawing/plotting.
 's prediction eachfeatures 'svisualization。"""
 fig, ax = plt.subplots(figsize=figsize)
 features_idx = list(range(min(top_n, len(feature_names))))
 PartialDependenceDisplay.from_estimator(
 model, X_train_scaled, features=features_idx,
 feature_names=feature_names,
 ax=ax, grid_resolution=50
 )
 plt.suptitle("Partial Dependence Plots", fontweight="bold", y=1.02)
 plt.tight_layout
 plt.savefig("figures/partial_dependence.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 7. Volcano Plot（expression/features）

```python
from scipy import stats

def volcano_plot(df, group_col, value_cols, group1, group2,
 fc_threshold=1.0, p_threshold=0.05, figsize=(10, 8)):
 """Fold Change and p-valueby/via Volcano Plot drawing/plotting."""
 results = []
 g1 = df[df[group_col] == group1]
 g2 = df[df[group_col] == group2]

 for col in value_cols:
 stat, pval = stats.mannwhitneyu(g1[col].dropna, g2[col].dropna,
 alternative="two-sided")
 fc = g2[col].mean - g1[col].mean # or log2FC
 results.append({"Feature": col, "log2FC": fc, "pvalue": pval,
 "neg_log10p": -np.log10(pval + 1e-300)})

 vdf = pd.DataFrame(results)

 fig, ax = plt.subplots(figsize=figsize)
 # min: significant up / down / ns
 sig_up = (vdf["log2FC"] > fc_threshold) & (vdf["pvalue"] < p_threshold)
 sig_down = (vdf["log2FC"] < -fc_threshold) & (vdf["pvalue"] < p_threshold)
 ns = ~(sig_up | sig_down)

 ax.scatter(vdf.loc[ns, "log2FC"], vdf.loc[ns, "neg_log10p"],
 c="gray", alpha=0.5, s=20, label="NS")
 ax.scatter(vdf.loc[sig_up, "log2FC"], vdf.loc[sig_up, "neg_log10p"],
 c="red", alpha=0.7, s=30, label="Up")
 ax.scatter(vdf.loc[sig_down, "log2FC"], vdf.loc[sig_down, "neg_log10p"],
 c="blue", alpha=0.7, s=30, label="Down")
 ax.axhline(-np.log10(p_threshold), color="gray", linestyle="--")
 ax.axvline(fc_threshold, color="gray", linestyle="--")
 ax.axvline(-fc_threshold, color="gray", linestyle="--")
 ax.set_xlabel("log₂ Fold Change")
 ax.set_ylabel("-log₁₀(p-value)")
 ax.set_title("Volcano Plot", fontweight="bold")
 ax.legend
 plt.tight_layout
 plt.savefig("figures/volcano_plot.png", dpi=300, bbox_inches="tight")
 plt.close
 return vdf
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
| `results/classification_metrics.csv` | CSV |
| `figures/roc_curves.png` | PNG |
| `figures/precision_recall_curves.png` | PNG |
| `figures/confusion_matrices.png` | PNG |
| `figures/partial_dependence.png` | PNG |
| `figures/volcano_plot.png` | PNG |

#### Reference Experiments

- **Exp-03**: cancergene expression's 4 classification + ROC + 
- **Exp-05**: toxicityprediction's valueclassification + Volcano Plot + PR curveline + PDP
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
