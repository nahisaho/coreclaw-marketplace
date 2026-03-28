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
