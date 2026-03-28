---
name: scientific-eda-correlation
description: |
 EDA and correlation analysis skill. Exploratory data analysis, correlation matrices, distribution visualization, multivariate analysis, and automated EDA report generation.
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
| `results/descriptive_statistics.csv` | CSV |
| `figures/distribution_boxplots.png` | PNG (300 DPI) |
| `figures/correlation_heatmap.png` | PNG (300 DPI) |
| `figures/scatter_matrix.png` | PNG (300 DPI) |

#### Reference Experiments

- **Exp-02**: `sns.heatmap` correlationheatmap's basic
- **Exp-12**: 8 processparameters's EDA
- **Exp-13**: PSP 3 blockcorrelation
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Data Analysis)

Before execution, define:
- [ ] **Input schema**: column names, types, expected ranges
- [ ] **Output schema**: expected result shape, key metrics to produce
- [ ] **Statistical validity**: significance level (alpha), power target, effect size threshold
- [ ] **Reproducibility**: random seed set, deterministic pipeline

#### Pass Criteria
- All statistical tests report p-values and confidence intervals
- Effect sizes reported alongside significance
- Multiple comparison corrections applied when > 2 tests
- Missing data handling documented (method + % impacted)
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
