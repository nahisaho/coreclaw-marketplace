---
name: scientific-publication-figures
description: |
 Publication figures skill. Journal-specification figure generation, multi-panel layout, color-blind safe palettes, resolution/DPI compliance, and figure annotation.
tu_tools:
 - key: biotools
 name: bio.tools
 description: visualizationTool Registry Search
---

# Scientific Publication-Quality Figure Generation

Nature/Science/Cell 'sfigures/tables matplotlib/seaborn skill。
Exp-10 15 type'sfigures/tablestemplateand 、allexperimentsettings is provided。

## When to Use

- paperfor'sfigures/tables is createdand
- multiple's composite figure configurationwhen needed
- DPI 300 above/more、fontcolor palettewhen needed
- figures/tables's necessary and

## Quick Start

> **⚠️ RULE: All figure text must be in English.**
> This applies to all titles, axis labels, legends, tick labels, annotations, and captions.
> Never use Japanese or any other language in graph text elements.

## settings

below/following's settings 's for.

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

def setup_publication_style:
 """Nature/Science 's matplotlib rcParams settings."""
 plt.rcParams.update({
 # font
 "font.family": "sans-serif",
 "font.sans-serif": ["Noto Sans CJK JP", "IPAGothic", "Arial", "Helvetica", "DejaVu Sans"],
 "font.size": 10,
 "axes.titlesize": 12,
 "axes.labelsize": 11,
 "xtick.labelsize": 9,
 "ytick.labelsize": 9,
 "legend.fontsize": 9,

 # line
 "axes.linewidth": 1.2,
 "lines.linewidth": 1.5,
 "lines.markersize": 6,

 # 
 "axes.spines.top": False,
 "axes.spines.right": False,

 # grid
 "axes.grid": False,

 # savesettings
 "savefig.dpi": 300,
 "savefig.bbox": "tight",
 "savefig.transparent": False,

 # Figure background
 "figure.facecolor": "white",
 "axes.facecolor": "white",
 })
```

## color palette

```python
# Nature-inspired （Exp-10）
NATURE_PALETTE = [
 "#E64B35", # 
 "#4DBBD5", # 
 "#00A087", # 
 "#3C5488", # 
 "#F39B7F", # 
 "#8491B4", # 
 "#91D1C2", # 
 "#DC9C6D", # 
]

# groupfor
MATERIAL_PALETTE = {
 "Set2": "seaborn Set2（ 8 、 and）",
 "tab10": "matplotlib tab10（ 10 ）",
 "Paired": "seaborn Paired（ 12 、comparison）",
}

# valuefor
CONTINUOUS_CMAPS = {
 "viridis": "（recommended）",
 "RdBu_r": "correlationheatmap（=0）",
 "YlOrRd": "direction'sintensity（degree、temperature）",
 "coolwarm": "direction（'s vs ）",
}
```

## savenumber/count

```python
def save_fig(fig, filename, dpi=300, formats=("png",)):
 """figurespecificationshapeformulasave."""
 for fmt in formats:
 filepath = f"figures/{filename}.{fmt}"
 fig.savefig(filepath, dpi=dpi, bbox_inches="tight",
 facecolor="white", edgecolor="none")
 plt.close(fig)
```

## keyfigures/tablestemplate

### 1. Violin + Strip Plot（significant）

```python
import seaborn as sns
from scipy import stats

def plot_violin_with_significance(df, x, y, pairs=None, figsize=(10, 6)):
 fig, ax = plt.subplots(figsize=figsize)
 sns.violinplot(data=df, x=x, y=y, palette=NATURE_PALETTE,
 inner=None, alpha=0.3, ax=ax)
 sns.stripplot(data=df, x=x, y=y, palette=NATURE_PALETTE,
 size=3, alpha=0.5, ax=ax)

 # significant（pairs specification）
 if pairs:
 y_max = df[y].max
 for i, (g1, g2) in enumerate(pairs):
 d1 = df[df[x] == g1][y]
 d2 = df[df[x] == g2][y]
 stat, pval = stats.mannwhitneyu(d1, d2)
 stars = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else "ns"
 h = y_max * (1.05 + i * 0.08)
 # drawing/plotting adjustText manual annotate
 ax.text((list(df[x].unique).index(g1) +
 list(df[x].unique).index(g2)) / 2,
 h, stars, ha="center", fontsize=12, fontweight="bold")
 save_fig(fig, f"violin_{y}")
```

### 2. Forest Plot（min）

```python
def plot_forest(effects, ci_lower, ci_upper, labels, figsize=(10, 8)):
 fig, ax = plt.subplots(figsize=figsize)
 y_pos = range(len(labels))
 ax.errorbar(effects, y_pos, xerr=[np.array(effects) - np.array(ci_lower),
 np.array(ci_upper) - np.array(effects)],
 fmt="D", color=NATURE_PALETTE[0], markersize=8,
 capsize=4, linewidth=2)
 ax.axvline(0, color="gray", linestyle="--", linewidth=1)
 ax.set_yticks(y_pos)
 ax.set_yticklabels(labels)
 ax.set_xlabel("Effect Size")
 ax.set_title("Forest Plot", fontweight="bold")
 save_fig(fig, "forest_plot")
```

### 3. Composite Figure

```python
import matplotlib.gridspec as gridspec

def create_composite_figure(plot_functions, layout=(2, 3),
 figsize=(18, 12), panel_labels=True):
 """
 multiple'sdrawing/plottingnumber/count composite figure and 。
 plot_functions: [(func, kwargs),...] 's
 """
 fig = plt.figure(figsize=figsize)
 gs = gridspec.GridSpec(*layout, figure=fig, hspace=0.35, wspace=0.3)

 for i, (func, kwargs) in enumerate(plot_functions):
 row, col = divmod(i, layout[1])
 ax = fig.add_subplot(gs[row, col])
 func(ax=ax, **kwargs)

 if panel_labels:
 ax.text(-0.1, 1.1, chr(65 + i), # A, B, C,...
 transform=ax.transAxes, fontsize=16,
 fontweight="bold", va="top")

 save_fig(fig, "composite_figure")
```

## figure's

| for | (inches) | remarks |
|---|---|---|
| 1 column | (3.5, 3.0) | Nature 1 column ≈ 89 mm |
| 1.5 column | (5.5, 4.0) | |
| 2 column | (7.0, 5.0) | Nature 2 column ≈ 183 mm |
| | (7.0, 9.0) | A4 's |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | visualizationTool Registry Search |

## References

### Output Files

| File | Format |
|---|---|
| `figures/*.png` | PNG (300 DPI) |
| `figures/*.svg` | SVG（、for） |
| `figures/*.pdf` | PDF（、LaTeX for） |

#### Reference Experiments

- **Exp-10**: 15 type'sfigures/tablestemplate's all
- **Exp-11〜13**: rcParams settings and color palette's

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
