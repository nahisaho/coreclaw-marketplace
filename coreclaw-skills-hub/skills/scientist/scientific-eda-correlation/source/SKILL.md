---
name: scientific-eda-correlation
description: |
 EDA and correlation analysis skill. Exploratory data analysis, correlation matrices, distribution visualization, multivariate analysis, and automated EDA report generation.
tu_tools:
 - key: biotools
 name: bio.tools
 description: analysistoolsearch
---

# Scientific EDA & Correlation Analysis

search/explorationdataanalysis（Exploratory Data Analysis）'s pipelineskill。
data's initial for、distributionvaluenumber/countcorrelation.

## When to Use

- dataset and
- number/count'swhen needed
- correlationheatmapwhen needed
- group'splotcomparisonwhen needed

## Quick Start

## Standard Pipeline

### 1. amount's

```python
import pandas as pd
import numpy as np

def descriptive_statistics(df, numeric_cols, group_col=None):
 """amount CSV save."""
 if group_col:
 stats = df.groupby(group_col)[numeric_cols].describe
 else:
 stats = df[numeric_cols].describe
 stats.to_csv("results/descriptive_statistics.csv")
 return stats
```

### 2. distributionvisualization（plot + plot）

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_distributions(df, variables, group_col, figsize=(20, 16), ncols=3):
 """group's plot number/count anddrawing/plotting."""
 nrows = (len(variables) + ncols - 1) // ncols
 fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
 axes = axes.flatten

 for i, var in enumerate(variables):
 sns.boxplot(data=df, x=group_col, y=var, ax=axes[i],
 palette="Set2", showfliers=True)
 axes[i].set_title(var, fontsize=12, fontweight="bold")
 axes[i].tick_params(axis="x", rotation=45)

 for j in range(i + 1, len(axes)):
 axes[j].set_visible(False)

 plt.tight_layout
 plt.savefig("figures/distribution_boxplots.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 3. correlationheatmap（Exp-02 / Exp-13 ）

```python
def plot_correlation_heatmap(df, numeric_cols, block_boundaries=None,
 figsize=(14, 12), method="pearson"):
 """
 correlationheatmap drawing/plotting.
 block_boundaries: PSP etc.'s line's（option）。
 """
 corr = df[numeric_cols].corr(method=method)

 fig, ax = plt.subplots(figsize=figsize)
 mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
 sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
 cmap="RdBu_r", center=0, vmin=-1, vmax=1,
 square=True, linewidths=0.5, ax=ax,
 annot_kws={"size": 8})

 # line（PSP blockmin）
 if block_boundaries:
 for b in block_boundaries:
 ax.axhline(y=b, color="black", linewidth=2)
 ax.axvline(x=b, color="black", linewidth=2)

 ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
 plt.tight_layout
 plt.savefig("figures/correlation_heatmap.png", dpi=300, bbox_inches="tight")
 plt.close
 return corr
```

### 4. scatter plot

```python
def plot_scatter_matrix(df, variables, hue_col, figsize=(16, 14)):
 """keynumber/count'sscatter plotdrawing/plotting."""
 g = sns.pairplot(df[variables + [hue_col]], hue=hue_col,
 diag_kind="kde", palette="Set2",
 plot_kws={"alpha": 0.6, "s": 30})
 g.fig.suptitle("Scatter Matrix", y=1.02, fontsize=14, fontweight="bold")
 plt.savefig("figures/scatter_matrix.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 5. PSP blockcorrelationmin（Exp-13 ）

```python
def psp_block_correlation(df, process_cols, structure_cols, property_cols):
 """Process→Structure→Property 's 3 blockcorrelationunits."""
 ps_corr = df[process_cols + structure_cols].corr.loc[process_cols, structure_cols]
 sp_corr = df[structure_cols + property_cols].corr.loc[structure_cols, property_cols]
 pp_corr = df[process_cols + property_cols].corr.loc[process_cols, property_cols]

 ps_corr.to_csv("results/PSP_process_structure_corr.csv")
 sp_corr.to_csv("results/PSP_structure_property_corr.csv")
 pp_corr.to_csv("results/PSP_process_property_corr.csv")

 return ps_corr, sp_corr, pp_corr
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | analysistoolsearch |

## References

### Output Files

| File | Format |
|---|---|
| `results/descriptive_statistics.csv` | CSV |
| `figures/distribution_boxplots.png` | PNG (300 DPI) |
| `figures/correlation_heatmap.png` | PNG (300 DPI) |
| `figures/scatter_matrix.png` | PNG (300 DPI) |

#### Reference Experiments

- **Exp-02**: `sns.heatmap` correlationheatmap's basic
- **Exp-12**: 8 processparameters's EDA
- **Exp-13**: PSP 3 blockcorrelation

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
