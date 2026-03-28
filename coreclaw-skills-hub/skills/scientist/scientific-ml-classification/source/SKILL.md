---
name: scientific-ml-classification
description: |
 ML classification skill. Binary/multi-class classification, model selection, hyperparameter tuning, cross-validation, metrics evaluation, and classification pipeline orchestration.
tu_tools:
 - key: openml
 name: OpenML
 description: classificationdatasetretrieval
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | classificationdatasetretrieval |

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
