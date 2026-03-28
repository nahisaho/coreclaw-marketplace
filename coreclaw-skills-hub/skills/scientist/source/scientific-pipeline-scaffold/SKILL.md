---
name: scientific-pipeline-scaffold
description: |
 dataanalysispipeline'sskill。directorystructure'sautomatedconstruction、reproducibilityfor、
 logoutput、time、JSON summarygeneration、dashboardfigure's is performedfor。
 all 13 experimentintegration。
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
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
