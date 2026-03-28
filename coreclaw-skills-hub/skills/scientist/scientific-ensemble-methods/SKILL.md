---
name: scientific-ensemble-methods
description: |
 Ensemble methods skill. Random forests, gradient boosting (XGBoost/LightGBM/CatBoost), stacking, blending, voting classifiers, and ensemble model interpretation.
---

# Scientific Ensemble Methods

multiple'sby/viapredictiondegree
ensemblemethod's designevaluationpipeline is provided。

## When to Use

- XGBoost/LightGBM/CatBoost gradientboosting is executedand
- Stacking/Blending ensemble is builtand
- multiple's Voting/Averaging prediction and
- ensemble's is evaluatedand
- Out-of-Fold prediction is performedand
- 's degree minwhen needed

---

## Quick Start

## 1. gradientboostingcomparison

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score


def compare_boosting(X, y, cv=5, scoring="f1_macro",
 task="classification"):
 """
 XGBoost / LightGBM / CatBoost comparison。

 Parameters:
 X: np.ndarray — features
 y: np.ndarray — label
 cv: int — CV fold count
 scoring: str — evaluation metric
 task: str — "classification" / "regression"
 """
 results = []

 try:
 from xgboost import XGBClassifier, XGBRegressor
 model = (XGBClassifier(n_estimators=200, max_depth=6,
 learning_rate=0.1, random_state=42,
 use_label_encoder=False, eval_metric="logloss")
 if task == "classification"
 else XGBRegressor(n_estimators=200, max_depth=6,
 learning_rate=0.1, random_state=42))
 scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
 results.append({"model": "XGBoost", "mean": scores.mean,
 "std": scores.std})
 except ImportError:
 pass

 try:
 from lightgbm import LGBMClassifier, LGBMRegressor
 model = (LGBMClassifier(n_estimators=200, max_depth=6,
 learning_rate=0.1, random_state=42, verbose=-1)
 if task == "classification"
 else LGBMRegressor(n_estimators=200, max_depth=6,
 learning_rate=0.1, random_state=42, verbose=-1))
 scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
 results.append({"model": "LightGBM", "mean": scores.mean,
 "std": scores.std})
 except ImportError:
 pass

 try:
 from catboost import CatBoostClassifier, CatBoostRegressor
 model = (CatBoostClassifier(iterations=200, depth=6,
 learning_rate=0.1, random_seed=42, verbose=0)
 if task == "classification"
 else CatBoostRegressor(iterations=200, depth=6,
 learning_rate=0.1, random_seed=42, verbose=0))
 scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
 results.append({"model": "CatBoost", "mean": scores.mean,
 "std": scores.std})
 except ImportError:
 pass

 df = pd.DataFrame(results).sort_values("mean", ascending=False)
 if not df.empty:
 print(f"Boosting: best = {df.iloc[0]['model']} "
 f"({scoring} = {df.iloc[0]['mean']:.4f})")
 return df
```

## 2. Stacking ensemble

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC


def stacking_ensemble(X_train, y_train, X_test,
 base_models=None, meta_model=None,
 n_folds=5):
 """
 Stacking ensemble (Out-of-Fold prediction)。

 Parameters:
 X_train: np.ndarray — data
 y_train: np.ndarray — label
 X_test: np.ndarray — test data
 base_models: list | None — 
 meta_model: classifier | None — 
 n_folds: int — CV fold count
 """
 if base_models is None:
 base_models = [
 ("rf", RandomForestClassifier(n_estimators=200, random_state=42)),
 ("gbm", GradientBoostingClassifier(n_estimators=200, random_state=42)),
 ("svm", SVC(probability=True, random_state=42)),
 ]
 if meta_model is None:
 meta_model = LogisticRegression(max_iter=1000, random_state=42)

 kf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
 n_classes = len(np.unique(y_train))

 # Out-of-Fold predictions
 oof_preds = np.zeros((len(y_train), len(base_models) * n_classes))
 test_preds = np.zeros((len(X_test), len(base_models) * n_classes))

 for i, (name, model) in enumerate(base_models):
 col_start = i * n_classes
 col_end = (i + 1) * n_classes
 test_fold_preds = np.zeros((len(X_test), n_classes, n_folds))

 for fold, (train_idx, val_idx) in enumerate(kf.split(X_train, y_train)):
 m = model.__class__(**model.get_params).fit(
 X_train[train_idx], y_train[train_idx])
 oof_preds[val_idx, col_start:col_end] = m.predict_proba(
 X_train[val_idx])
 test_fold_preds[:, :, fold] = m.predict_proba(X_test)

 test_preds[:, col_start:col_end] = test_fold_preds.mean(axis=2)
 print(f" Stacking base: {name} done")

 # Meta-model
 meta_model.fit(oof_preds, y_train)
 final_pred = meta_model.predict(test_preds)
 final_proba = meta_model.predict_proba(test_preds)

 print(f"Stacking: {len(base_models)} base models → meta-model")
 return final_pred, final_proba, meta_model
```

## 3. Voting ensemble

```python
from sklearn.ensemble import VotingClassifier, VotingRegressor


def voting_ensemble(X, y, models=None, voting="soft",
 cv=5, scoring="f1_macro"):
 """
 Voting ensemble。

 Parameters:
 X: np.ndarray — features
 y: np.ndarray — label
 models: list | None — (name, model) 
 voting: str — "soft" / "hard"
 cv: int — CV fold count
 scoring: str — evaluation metric
 """
 if models is None:
 models = [
 ("rf", RandomForestClassifier(n_estimators=200, random_state=42)),
 ("gbm", GradientBoostingClassifier(n_estimators=200, random_state=42)),
 ("lr", LogisticRegression(max_iter=1000, random_state=42)),
 ]

 # unitsevaluation
 results = []
 for name, model in models:
 scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
 results.append({"model": name, "mean": scores.mean, "std": scores.std})

 # Voting
 vc = VotingClassifier(estimators=models, voting=voting)
 scores = cross_val_score(vc, X, y, cv=cv, scoring=scoring)
 results.append({"model": f"Voting({voting})",
 "mean": scores.mean, "std": scores.std})

 df = pd.DataFrame(results).sort_values("mean", ascending=False)
 print(f"Voting ensemble: {scoring} = {scores.mean:.4f} ± {scores.std:.4f}")
 return df
```

## 4. ensembleevaluation

```python
def ensemble_diversity(models, X, y):
 """
 ensemble (Q-statistic / Disagreement)。

 Parameters:
 models: list — 
 X: np.ndarray — evaluationdata
 y: np.ndarray — label
 """
 predictions = np.array([m.predict(X) for m in models])
 n_models = len(models)
 correct = (predictions == y).astype(int)

 # all's Q-statistic
 q_stats = []
 disagree_rates = []
 for i in range(n_models):
 for j in range(i + 1, n_models):
 n11 = np.sum((correct[i] == 1) & (correct[j] == 1))
 n00 = np.sum((correct[i] == 0) & (correct[j] == 0))
 n10 = np.sum((correct[i] == 1) & (correct[j] == 0))
 n01 = np.sum((correct[i] == 0) & (correct[j] == 1))

 denom = n11 * n00 - n10 * n01
 numer = n11 * n00 + n10 * n01
 q = denom / numer if numer != 0 else 0
 q_stats.append(q)
 disagree_rates.append((n10 + n01) / len(y))

 result = {
 "mean_q_statistic": round(np.mean(q_stats), 4),
 "mean_disagreement": round(np.mean(disagree_rates), 4),
 "n_models": n_models,
 }
 print(f"Diversity: Q={result['mean_q_statistic']:.3f}, "
 f"Disagree={result['mean_disagreement']:.3f}")
 return result
```

---

## Pipeline Integration

```
automl → ensemble-methods → uncertainty-quantification
 (selection) (ensemble) (uncertaintyamount)
 │ │ ↓
 feature-importance ┘ explainable-ai
 (featuresimportantdegree) (possible AI)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `stacking_meta.pkl` | Stacking | → prediction |
| `boosting_comparison.csv` | boostingcomparison | → report |
| `ensemble_diversity.json` | | → improvement |

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
