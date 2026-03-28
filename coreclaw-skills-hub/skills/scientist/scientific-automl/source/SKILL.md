---
name: scientific-automl
description: |
 AutoML pipeline skill. Optuna hyperparameter optimization, FLAML fast AutoML, Auto-sklearn model selection, NAS, automated feature engineering, and model comparison pipelines.
tu_tools:
 - key: openml
 name: OpenML
 description: AutoML taskreference
---

# Scientific AutoML

hyperparametersoptimizationselectionfeatures
automated AutoML pipeline is provided。

## When to Use

- Optuna/Hyperopt hyperparametersoptimizationwhen needed
- multiple's automatedcomparisonselection is performedand
- FLAML/Auto-sklearn high-speed AutoML is executedand
- featuresautomatedwhen needed
- Neural Architecture Search (NAS) is designedand
- selectionbasis'sreport is generatedand

---

## Quick Start

## 1. Optuna hyperparametersoptimization

```python
import optuna
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import (
 RandomForestClassifier, GradientBoostingClassifier)
from sklearn.svm import SVC
from sklearn.metrics import make_scorer, f1_score


def optuna_optimize(X, y, model_type="rf", n_trials=100,
 cv=5, scoring="f1_macro", direction="maximize"):
 """
 Optuna hyperparametersoptimization。

 Parameters:
 X: np.ndarray — features
 y: np.ndarray — label
 model_type: str — "rf" / "gbm" / "svm"
 n_trials: int — number of trials
 cv: int — CV fold count
 scoring: str — evaluation metric
 direction: str — "maximize" / "minimize"
 """
 def objective(trial):
 if model_type == "rf":
 params = {
 "n_estimators": trial.suggest_int("n_estimators", 50, 500),
 "max_depth": trial.suggest_int("max_depth", 3, 20),
 "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
 "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
 "max_features": trial.suggest_categorical(
 "max_features", ["sqrt", "log2", None]),
 }
 model = RandomForestClassifier(**params, random_state=42)

 elif model_type == "gbm":
 params = {
 "n_estimators": trial.suggest_int("n_estimators", 50, 500),
 "max_depth": trial.suggest_int("max_depth", 3, 10),
 "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
 "subsample": trial.suggest_float("subsample", 0.5, 1.0),
 "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
 }
 model = GradientBoostingClassifier(**params, random_state=42)

 elif model_type == "svm":
 params = {
 "C": trial.suggest_float("C", 0.01, 100, log=True),
 "kernel": trial.suggest_categorical(
 "kernel", ["rbf", "poly", "sigmoid"]),
 "gamma": trial.suggest_categorical("gamma", ["scale", "auto"]),
 }
 model = SVC(**params, probability=True, random_state=42)

 scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
 return scores.mean

 optuna.logging.set_verbosity(optuna.logging.WARNING)
 study = optuna.create_study(direction=direction)
 study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

 print(f"Optuna ({model_type}): best {scoring} = {study.best_value:.4f}")
 print(f" Best params: {study.best_params}")
 return study
```

## 2. AutoML pipeline

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier


def automl_model_selection(X, y, cv=5, scoring="f1_macro",
 n_trials_per_model=50):
 """
 AutoML selectionpipeline。

 Parameters:
 X: np.ndarray — features
 y: np.ndarray — label
 cv: int — CV fold count
 scoring: str — evaluation metric
 n_trials_per_model: int — rows
 """
 model_types = ["rf", "gbm", "svm"]
 results = []

 for mt in model_types:
 study = optuna_optimize(
 X, y, model_type=mt,
 n_trials=n_trials_per_model, cv=cv, scoring=scoring)
 results.append({
 "model_type": mt,
 "best_score": round(study.best_value, 4),
 "best_params": study.best_params,
 "n_trials": len(study.trials),
 })

 # 
 baselines = [
 ("logistic", LogisticRegression(max_iter=1000, random_state=42)),
 ("knn", KNeighborsClassifier),
 ("dt", DecisionTreeClassifier(random_state=42)),
 ]
 for name, model in baselines:
 scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
 results.append({
 "model_type": name,
 "best_score": round(scores.mean, 4),
 "best_params": {},
 "n_trials": 1,
 })

 df = pd.DataFrame(results).sort_values("best_score", ascending=False)
 best = df.iloc[0]
 print(f"AutoML: best = {best['model_type']} "
 f"({scoring} = {best['best_score']})")
 return df
```

## 3. automatedfeatures

```python
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif


def auto_feature_engineering(X, y, max_poly_degree=2,
 top_k=None, interactions_only=False):
 """
 automatedfeatures。

 Parameters:
 X: np.ndarray — features
 y: np.ndarray — label
 max_poly_degree: int — termformulanumber/count
 top_k: int | None — selectionfeaturesnumber/count
 interactions_only: bool — interaction's
 """
 scaler = StandardScaler
 X_scaled = scaler.fit_transform(X)

 # termformulafeatures
 poly = PolynomialFeatures(
 degree=max_poly_degree,
 interaction_only=interactions_only,
 include_bias=False)
 X_poly = poly.fit_transform(X_scaled)

 # featuresselection
 if top_k is None:
 top_k = min(X_poly.shape[1], X.shape[1] * 3)

 selector = SelectKBest(mutual_info_classif, k=min(top_k, X_poly.shape[1]))
 X_selected = selector.fit_transform(X_poly, y)

 print(f"Feature engineering: {X.shape[1]} → {X_poly.shape[1]} "
 f"→ {X_selected.shape[1]} features")
 return X_selected, poly, selector
```

## 4. Optuna visualizationreport

```python
def automl_report(study, output_dir="results"):
 """
 Optuna Study visualizationreport。

 Parameters:
 study: optuna.Study — optimizationresults
 output_dir: str — output directory
 """
 from pathlib import Path
 import matplotlib.pyplot as plt

 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 # parametersimportantdegree
 try:
 importances = optuna.importance.get_param_importances(study)
 fig, ax = plt.subplots(figsize=(8, 5))
 params = list(importances.keys)
 values = list(importances.values)
 ax.barh(params, values)
 ax.set_xlabel("Importance")
 ax.set_title("Hyperparameter Importance")
 fig.tight_layout
 fig.savefig(out / "param_importance.png", dpi=150)
 plt.close(fig)
 except Exception:
 pass

 # optimization
 trials_df = study.trials_dataframe
 trials_df.to_csv(out / "optuna_trials.csv", index=False)

 # parameters
 best = {
 "best_value": study.best_value,
 "best_params": study.best_params,
 "n_trials": len(study.trials),
 }

 print(f"AutoML report → {out}")
 return best
```

---

## Pipeline Integration

```
eda-correlation → automl → ensemble-methods
 (datasearch/exploration) (selection) (ensemble)
 │ │ ↓
 feature-importance ──┘ uncertainty-quantification
 (features) (uncertaintyamount)
 │
 active-learning
 (active learning)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `optuna_trials.csv` | | → visualization |
| `param_importance.png` | parametersimportantdegree | → report |
| `model_comparison.csv` | comparison | → ensemble-methods |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | AutoML taskreference |
---

## Harness Optimization (v0.4.0)

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
