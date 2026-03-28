---
name: scientific-feature-importance
description: |
 featuresimportantdegreemin'sskill。Tree-based Feature Importance and Permutation Importance 
 forprediction's explainability for。
 Scientific Skills Exp-05, 12, 13 。
tu_tools:
 - key: openml
 name: OpenML
 description: featuresselectionreference
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | featuresselectionreference |

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
