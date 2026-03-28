---
name: scientific-publication-figures
description: |
 Publication figures skill. Journal-specification figure generation, multi-panel layout, color-blind safe palettes, resolution/DPI compliance, and figure annotation.
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
| `figures/*.png` | PNG (300 DPI) |
| `figures/*.svg` | SVG（、for） |
| `figures/*.pdf` | PDF（、LaTeX for） |

#### Reference Experiments

- **Exp-10**: 15 type'sfigures/tablestemplate's all
- **Exp-11〜13**: rcParams settings and color palette's
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Visualization)

Before execution, define:
- [ ] **Target audience**: journal / conference / dashboard / internal
- [ ] **Figure dimensions**: width x height, DPI requirement
- [ ] **Color scheme**: colorblind-safe palette confirmed
- [ ] **Data-ink ratio**: minimize non-data elements

#### Pass Criteria
- All figures saved to disk (never plt.show())
- Figures embedded in report.md with captions
- Text is English-only, font size >= 8pt
- Accessibility: contrast ratio >= 4.5:1
- Vector format (SVG/PDF) provided when requested
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
