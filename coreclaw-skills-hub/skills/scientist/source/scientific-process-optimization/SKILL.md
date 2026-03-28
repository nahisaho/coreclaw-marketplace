---
name: scientific-process-optimization
description: |
 response surfacemethod（ML-RSM）and purposeoptimization'sskill。processparameters'soptimal conditionssearch/exploration、
 、processvisualization is performedfor。
 Scientific Skills Exp-12, 13 。
tu_tools:
 - key: biotools
 name: bio.tools
 description: processoptimizationtoolsearch
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
```

### 4. gridby/viaoptimal conditionssearch/exploration

```python
def grid_search_optimum(model, feature_names, bounds,
 target_name, maximize=True, n_points=10000):
 """
 gridoptimal conditions is explored。
 bounds: {feature_name: (min, max)} 's
 """
 rng = np.random.default_rng(42)
 X_search = np.column_stack([
 rng.uniform(bounds[f][0], bounds[f][1], n_points)
 if f in bounds
 else np.full(n_points, bounds.get(f, (0, 0))[0])
 for f in feature_names
 ])

 predictions = model.predict(X_search)
 best_idx = np.argmax(predictions) if maximize else np.argmin(predictions)

 optimal_conditions = {f: X_search[best_idx, i]
 for i, f in enumerate(feature_names)}
 optimal_conditions[f"predicted_{target_name}"] = predictions[best_idx]

 return optimal_conditions
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | processoptimizationtoolsearch |

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
