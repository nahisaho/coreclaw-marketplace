---
name: scientific-pipeline-scaffold
description: |
 dataanalysispipeline'sskill。directorystructure'sautomatedconstruction、reproducibilityfor、
 logoutput、time、JSON summarygeneration、dashboardfigure's is performedfor。
 all 13 experimentintegration。
tu_tools:
 - key: biotools
 name: bio.tools
 description: pipelineconfigurationtoolsearch
---

# Scientific Pipeline Scaffold

all Exp-01〜13 「（scaffold）」 integrationskill。
experimentpipeline for、reproducibilitystructure.

## When to Use

- analysisexperiment's and
- possibleexperimentpipeline is builtand
- analysisresultsJSON summaryasexportwhen needed
- dashboardfigureautomatedgenerationwhen needed

## Quick Start

## 1. headertemplate

```python
#!/usr/bin/env python3
"""
Exp-XX: [experimenttitle]
Scientific Skills Series

Description:
 [1-2'soverview]

Author: [Name]
Date: [YYYY-MM-DD]
"""

import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg") # headless environmentsupport

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import time

# === Reproducibility Settings ===
SEED = 42
np.random.seed(SEED)

# === Directory Structure ===
BASE_DIR = Path(__file__).resolve.parent
DATA_DIR = BASE_DIR / "data"
FIG_DIR = BASE_DIR / "figures"
RESULTS_DIR = BASE_DIR / "results"

for d in [DATA_DIR, FIG_DIR, RESULTS_DIR]:
 d.mkdir(parents=True, exist_ok=True)

# === Publication-Quality Style ===
# ⚠️ RULE: All graph text (titles, axis labels, legends, annotations) MUST be in English.
plt.rcParams.update({
 "font.family": "sans-serif",
 "font.sans-serif": ["Noto Sans CJK JP", "IPAGothic", "Arial", "Helvetica", "DejaVu Sans"],
 "font.size": 10,
 "axes.titlesize": 12,
 "axes.labelsize": 11,
 "axes.spines.top": False,
 "axes.spines.right": False,
 "savefig.dpi": 300,
 "savefig.bbox": "tight",
 "figure.facecolor": "white",
})
```

## 2. number/counttemplate

```python
def main:
 """pipelinenumber/count。"""
 start_time = time.time
 print("=" * 60)
 print("Exp-XX: [experimenttitle]")
 print("=" * 60)

 # ──── Step 0: Saving hypothesis/workflow definitions ────
 print("\n[Step 0] Saving hypothesis/workflow definitions...")
 # → see scientific-hypothesis-pipeline skill
 # save_hypothesis_markdown(HYPOTHESIS)
 # save_hypothesis_json(HYPOTHESIS)
 # save_workflow_design(HYPOTHESIS, workflow_steps)
 # save_workflow_json(HYPOTHESIS, workflow_steps)

 # ──── Step 1: Data loading / generation ────
 print("\n[Step 1] Loading data...")
 # df = pd.read_csv(DATA_DIR / "dataset.csv")
 # df = generate_dataset
 # df.to_csv(DATA_DIR / "dataset.csv", index=False)

 # ──── Step 2: EDA ────
 print("\n[Step 2] search/explorationdataanalysis...")
 # → scientific-eda-correlation skillreference

 # ──── Step 3: preprocessing ────
 print("\n[Step 3] preprocessing...")
 # → scientific-data-preprocessing skillreference

 # ──── Step 4: ────
 print("\n[Step 4]...")
 # → scientific-ml-regression / ml-classification skillreference

 # ──── Step 5: visualization ────
 print("\n[Step 5] visualization...")
 # → scientific-publication-figures skillreference

 # ──── Step 6: hypothesis ────
 print("\n[Step 6] hypothesis...")
 # → see scientific-hypothesis-pipeline skill
 # hypothesis_verdict = evaluate_hypothesis(result, HYPOTHESIS)

 # ──── Step 7: summary ────
 elapsed = time.time - start_time
 print(f"\n[Step 7] summarygeneration... (elapsed: {elapsed:.1f}s)")
 # → generate_summary 

 # ──── Step 8: paperwriting ────
 print("\n[Step 8] paperwriting...")
 # → scientific-academic-writing skill
 # → scientific-critical-review skillfix

 print("\n" + "=" * 60)
 print(f"Done! ({elapsed:.1f} sec)")
 print("=" * 60)


if __name__ == "__main__":
 main
```

## 3. log

```python
class StepLogger:
 """log。"""

 def __init__(self, experiment_name):
 self.experiment_name = experiment_name
 self.step_count = 0
 self.start_time = time.time
 self.step_times = {}
 print("=" * 60)
 print(f"{experiment_name}")
 print("=" * 60)

 def step(self, description):
 """ Step start."""
 self.step_count += 1
 step_start = time.time
 if self.step_count > 1:
 prev = self.step_count - 1
 self.step_times[prev] = time.time - self._current_step_start
 self._current_step_start = step_start
 print(f"\n[Step {self.step_count}] {description}...")

 def finish(self):
 """pipelinecompletion."""
 elapsed = time.time - self.start_time
 if self.step_count > 0:
 self.step_times[self.step_count] = time.time - self._current_step_start
 print(f"\n{'=' * 60}")
 print(f"Done! ( {elapsed:.1f} sec)")
 for step_num, t in self.step_times.items:
 print(f" Step {step_num}: {t:.1f}s")
 print(f"{'=' * 60}")
 return elapsed
```

## 4. JSON summarygeneration

allexperiment `analysis_summary.json` 's schema。

```python
def generate_summary(results_dict, experiment_name, elapsed_seconds,
 output_path=None):
 """
 standard's analysis_summary.json is generated。

 results_dict 's resultsincluding。
 's number/count information automatedaddition.
 """
 import datetime

 summary = {
 "experiment": experiment_name,
 "timestamp": datetime.datetime.now.isoformat,
 "elapsed_seconds": round(elapsed_seconds, 2),
 "environment": {
 "python": __import__("sys").version,
 "seed": SEED,
 },
 "data": {
 "n_samples": results_dict.get("n_samples"),
 "n_features": results_dict.get("n_features"),
 "source": results_dict.get("data_source", "simulation"),
 },
 "results": results_dict,
 }

 if output_path is None:
 output_path = RESULTS_DIR / "analysis_summary.json"

 with open(output_path, "w", encoding="utf-8") as f:
 json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

 print(f" → Summary saved: {output_path}")
 return summary
```

### JSON summarystandardlist

| | type | | required |
|---|---|---|---|
| `experiment` | str | experiment | ✅ |
| `timestamp` | str | ISO 8601 datetime | ✅ |
| `elapsed_seconds` | float | time | ✅ |
| `environment.python` | str | Python | ✅ |
| `environment.seed` | int | random seed | ✅ |
| `data.n_samples` | int | number/count | ✅ |
| `data.n_features` | int | featuresnumber/count | ○ |
| `data.source` | str | data | ○ |
| `results.best_model` | str | | ○ |
| `results.best_r2` / `best_auc` | float | | ○ |
| `results.n_figures` | int | generationfigurenumber/count | ○ |

## 5. dashboard

```python
import matplotlib.gridspec as gridspec

def create_summary_panel(panel_data, experiment_name, figsize=(20, 14)):
 """
 analysisresults's dashboard 1 sheets's Figure and 。

 panel_data: [
 {"type": "table", "title": "...", "data": df_or_dict},
 {"type": "plot_func", "title": "...", "func": callable, "kwargs": {}},
 {"type": "text", "title": "...", "text": "..."},
 {"type": "metrics_bar", "title": "...", "names": [...], "values": [...]},
 ]
 """
 n_panels = len(panel_data)
 ncols = min(3, n_panels)
 nrows = (n_panels + ncols - 1) // ncols

 fig = plt.figure(figsize=figsize)
 gs = gridspec.GridSpec(nrows, ncols, figure=fig, hspace=0.4, wspace=0.3)

 for i, panel in enumerate(panel_data):
 row, col = divmod(i, ncols)
 ax = fig.add_subplot(gs[row, col])

 ptype = panel["type"]
 title = panel.get("title", f"Panel {chr(65 + i)}")

 if ptype == "metrics_bar":
 ax.barh(panel["names"], panel["values"],
 color="steelblue", edgecolor="black")
 ax.set_xlabel("Value")

 elif ptype == "text":
 ax.text(0.05, 0.95, panel["text"], transform=ax.transAxes,
 fontsize=9, verticalalignment="top", fontfamily="monospace",
 bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
 ax.axis("off")

 elif ptype == "table":
 ax.axis("off")
 if isinstance(panel["data"], pd.DataFrame):
 tbl = ax.table(cellText=panel["data"].values,
 colLabels=panel["data"].columns,
 cellLoc="center", loc="center")
 tbl.auto_set_font_size(False)
 tbl.set_fontsize(8)
 elif isinstance(panel["data"], dict):
 rows = [[k, str(v)] for k, v in panel["data"].items]
 tbl = ax.table(cellText=rows, colLabels=["Metric", "Value"],
 cellLoc="center", loc="center")
 tbl.auto_set_font_size(False)
 tbl.set_fontsize(9)

 elif ptype == "plot_func":
 panel["func"](ax=ax, **panel.get("kwargs", {}))

 # label (A, B, C,...)
 ax.set_title(f"({chr(65 + i)}) {title}", fontsize=11, fontweight="bold")

 fig.suptitle(f"Summary: {experiment_name}", fontsize=14, fontweight="bold")
 plt.savefig(FIG_DIR / "summary_panel.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 6. 

```python
def save_fig(fig, filename, dpi=300, formats=("png",)):
 """figuresavenumber/count。"""
 for fmt in formats:
 fig.savefig(FIG_DIR / f"{filename}.{fmt}",
 dpi=dpi, bbox_inches="tight",
 facecolor="white", edgecolor="none")
 plt.close(fig)
 print(f" → Figure saved: {filename}")


def save_results(df, filename, index=False):
 """DataFrame results/ savenumber/count。"""
 path = RESULTS_DIR / filename
 df.to_csv(path, index=index)
 print(f" → Results saved: {filename}")
```

## directorystructure's standard

```
Exp-XX/
├── exp_analysis.py # 
├── qiita-exp-analysis.md # Qiita 
├── data/
│ └── dataset.csv # input data
├── figures/
│ ├── Fig01_*.png # unitsfigure（Fig + + ）
│ ├── Fig02_*.png
│ └── summary_panel.png # dashboard
└── results/
 ├── descriptive_statistics.csv
 ├── model_metrics.csv
 ├── feature_importance.csv
 └── analysis_summary.json # JSON summary
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | pipelineconfigurationtoolsearch |

## References

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-hypothesis-pipeline` | Step 0: hypothesisworkflowdesign'ssave |
| `scientific-data-preprocessing` | Step 1/3: Loading datapreprocessing |
| `scientific-eda-correlation` | Step 2: search/explorationdataanalysiscorrelationmin |
| `scientific-ml-regression` | Step 4: regression |
| `scientific-ml-classification` | Step 4: classification |
| `scientific-publication-figures` | Step 5: paper'sfigures/tablesgeneration |
| `scientific-academic-writing` | Step 8: paperwriting |
| `scientific-critical-review` | Step 8: 's fix |

### Exp reference

- **all 13 experiment**: directorystructure、、warnings 
- **Exp-12, 13**: `main` + time + JSON summary + 
- **Exp-10**: `save_fig` / `write_summary` 
