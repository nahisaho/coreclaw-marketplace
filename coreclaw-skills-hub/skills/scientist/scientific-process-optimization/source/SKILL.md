---
name: scientific-process-optimization
description: |
 Process optimization skill. Industrial process optimization, response surface methodology, constraint optimization, and process parameter tuning pipelines.
---

# Scientific Process Optimization (RSM & Pareto)

machine learning'sresponse surfacemethod（ML-Response Surface Methodology） and 
purposeoptimization for、processparameters'soptimal conditions is exploredskill。
process（、）and synthesis's optimization for。

## When to Use

- processparameters's optimal conditions search/explorationwhen needed
- 2 number/count'sresponse surface（） visualizationwhen needed
- multiple'sobjective function's minwhen needed
- Optimal solution（）and

## Quick Start

## Standard Pipeline

### 1. ML response surface（）

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor

def response_surface_2d(model, X_train, feature_names,
 var1_name, var2_name, target_name,
 fixed_values=None, resolution=50, figsize=(8, 7)):
 """
 for 2 number/count'sresponse surface drawing/plotting.
 's number/countmedian（or fixed_values specification）。
 """
 var1_idx = list(feature_names).index(var1_name)
 var2_idx = list(feature_names).index(var2_name)

 # value：median
 if fixed_values is None:
 fixed_values = np.median(X_train, axis=0)
 else:
 fixed_values = np.array(fixed_values)

 # griddefinition
 v1_range = np.linspace(X_train[:, var1_idx].min,
 X_train[:, var1_idx].max, resolution)
 v2_range = np.linspace(X_train[:, var2_idx].min,
 X_train[:, var2_idx].max, resolution)
 V1, V2 = np.meshgrid(v1_range, v2_range)

 # predictionforinputconstruction
 X_grid = np.tile(fixed_values, (resolution * resolution, 1))
 X_grid[:, var1_idx] = V1.ravel
 X_grid[:, var2_idx] = V2.ravel

 Z = model.predict(X_grid).reshape(V1.shape)

 # drawing/plotting
 fig, ax = plt.subplots(figsize=figsize)
 cf = ax.contourf(V1, V2, Z, levels=20, cmap="viridis")
 cs = ax.contour(V1, V2, Z, levels=10, colors="white", linewidths=0.5, alpha=0.5)
 ax.clabel(cs, inline=True, fontsize=8, fmt="%.1f")
 plt.colorbar(cf, ax=ax, label=target_name)
 ax.set_xlabel(var1_name)
 ax.set_ylabel(var2_name)
 ax.set_title(f"Response Surface: {target_name}", fontweight="bold")
 plt.tight_layout
 plt.savefig(f"figures/response_surface_{var1_name}_{var2_name}.png",
 dpi=300, bbox_inches="tight")
 plt.close
 return V1, V2, Z
```

### 2. processvisualization

```python
def process_window(models, X_train, feature_names,
 var1_name, var2_name, targets_specs,
 resolution=50, figsize=(8, 7)):
 """
 multiple's range processvisualization.
 targets_specs: [(model, target_name, min_val, max_val),...]
 """
 var1_idx = list(feature_names).index(var1_name)
 var2_idx = list(feature_names).index(var2_name)
 fixed = np.median(X_train, axis=0)

 v1_range = np.linspace(X_train[:, var1_idx].min,
 X_train[:, var1_idx].max, resolution)
 v2_range = np.linspace(X_train[:, var2_idx].min,
 X_train[:, var2_idx].max, resolution)
 V1, V2 = np.meshgrid(v1_range, v2_range)

 X_grid = np.tile(fixed, (resolution * resolution, 1))
 X_grid[:, var1_idx] = V1.ravel
 X_grid[:, var2_idx] = V2.ravel

 feasible = np.ones(resolution * resolution, dtype=bool)
 for model, tname, tmin, tmax in targets_specs:
 pred = model.predict(X_grid)
 feasible &= (pred >= tmin) & (pred <= tmax)

 feasible_map = feasible.reshape(V1.shape).astype(float)

 fig, ax = plt.subplots(figsize=figsize)
 ax.contourf(V1, V2, feasible_map, levels=[0.5, 1.5],
 colors=["#90EE90"], alpha=0.5)
 ax.contour(V1, V2, feasible_map, levels=[0.5], colors=["green"], linewidths=2)
 ax.set_xlabel(var1_name)
 ax.set_ylabel(var2_name)
 ax.set_title("Process Window (Feasible Region)", fontweight="bold")
 plt.tight_layout
 plt.savefig("figures/process_window.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 3. purposeoptimization

```python
def pareto_optimization(df, obj1_col, obj2_col, obj1_minimize=True,
 obj2_minimize=True, figsize=(8, 7)):
 """
 2 purpose's extractionvisualization.
 """
 points = df[[obj1_col, obj2_col]].values.copy

 # shapeformula
 if not obj1_minimize:
 points[:, 0] = -points[:, 0]
 if not obj2_minimize:
 points[:, 1] = -points[:, 1]

 # 'sextraction
 is_pareto = np.ones(len(points), dtype=bool)
 for i in range(len(points)):
 if is_pareto[i]:
 is_pareto[i] = True
 for j in range(len(points)):
 if i != j and is_pareto[j]:
 if np.all(points[j] <= points[i]) and np.any(points[j] < points[i]):
 is_pareto[i] = False
 break

 pareto_df = df[is_pareto].copy
 pareto_df = pareto_df.sort_values(obj1_col)
 pareto_df.to_csv("results/pareto_optimal.csv", index=False)

 # drawing/plotting
 fig, ax = plt.subplots(figsize=figsize)
 ax.scatter(df[obj1_col], df[obj2_col], alpha=0.3, s=20,
 color="gray", label="All solutions")
 ax.scatter(pareto_df[obj1_col], pareto_df[obj2_col],
 color="red", s=80, zorder=5, edgecolors="black",
 linewidth=1, label=f"Pareto front (n={len(pareto_df)})")
 ax.plot(pareto_df[obj1_col], pareto_df[obj2_col],
 "r--", linewidth=1.5, alpha=0.7)

 ax.set_xlabel(obj1_col)
 ax.set_ylabel(obj2_col)
 ax.set_title("Pareto Front", fontweight="bold")
 ax.legend
 plt.tight_layout
 plt.savefig("figures/pareto_front.png", dpi=300, bbox_inches="tight")
 plt.close

 return pareto_df


def pareto_optimization_3d(df, obj1_col, obj2_col, obj3_col,
 obj1_minimize=True, obj2_minimize=True,
 obj3_minimize=True):
 """
 3 purpose's is extracted。
 """
 points = df[[obj1_col, obj2_col, obj3_col]].values.copy

 if not obj1_minimize:
 points[:, 0] = -points[:, 0]
 if not obj2_minimize:
 points[:, 1] = -points[:, 1]
 if not obj3_minimize:
 points[:, 2] = -points[:, 2]

 is_pareto = np.ones(len(points), dtype=bool)
 for i in range(len(points)):
 if is_pareto[i]:
 for j in range(len(points)):
 if i != j and is_pareto[j]:
 if np.all(points[j] <= points[i]) and np.any(points[j] < points[i]):
 is_pareto[i] = False
 break

 pareto_df = df[is_pareto].copy
 pareto_df = pareto_df.sort_values(obj1_col)
 pareto_df.to_csv("results/pareto_optimal_3d.csv", index=False)

 print(f" 3D Pareto front: {len(pareto_df)} non-dominated solutions "
 f"from {len(df)} total")
 return pareto_df
```

### 4. by/viaoptimal conditionssearch/exploration

```python
def random_search_optimum(model, feature_names, bounds,
 target_name, maximize=True, n_points=10000):
 """
 Random sampling optimization optimal conditions is explored。
 bounds: {feature_name: (min, max)} 's
 """
 rng = np.random.default_rng(42)
 for f in feature_names:
 if f not in bounds:
 raise ValueError(f"Missing bounds for feature '{f}'. All features must have (min, max) bounds.")
 X_search = np.column_stack([
 rng.uniform(bounds[f][0], bounds[f][1], n_points)
 for f in feature_names
 ])

 predictions = model.predict(X_search)
 best_idx = np.argmax(predictions) if maximize else np.argmin(predictions)

 optimal_conditions = {f: X_search[best_idx, i]
 for i, f in enumerate(feature_names)}
 optimal_conditions[f"predicted_{target_name}"] = predictions[best_idx]

 return optimal_conditions
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
| `results/pareto_optimal.csv` | CSV |
| `figures/response_surface_*.png` | PNG |
| `figures/process_window.png` | PNG |
| `figures/pareto_front.png` | PNG |

#### Reference Experiments

- **Exp-12**: degree vs selection'soptimization、ML-RSM
- **Exp-13**: TCO 's vs rateoptimization、condition RSM
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
