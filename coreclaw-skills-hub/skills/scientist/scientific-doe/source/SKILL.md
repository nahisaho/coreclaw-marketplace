---
name: scientific-doe
description: |
 Design of Experiments (DOE) skill. Factorial design, response surface methodology, Latin hypercube sampling with auto-sized pool generation, Taguchi methods, ARD-RBF Bayesian optimization, and optimal experimental design generation.
---

# Scientific Design of Experiments (DOE)

Skill for systematic DOE and optimization. From factor screening with orthogonal arrays
to RSM optimal condition search and Bayesian sequential optimization,
providing templates for each experimental stage.

## When to Use

- When multi-factor experiment planning (factor/level design) is needed
- When minimizing experiment count with orthogonal arrays or CCD
- When quantifying main effect and interaction contributions
- When searching for optimal conditions via response surface
- When performing sequential experiments via Bayesian optimization

---

## Quick Start

## 1. Factor Design Template

```python
import numpy as np
import pandas as pd

def define_factors(factor_dict):
 """
 Factor definition template.

 factor_dict example:
 {
 "Temperature": {"levels": [200, 250, 300], "unit": "°C", "type": "continuous"},
 "Pressure": {"levels": [1, 5, 10], "unit": "mTorr", "type": "continuous"},
 "Gas_Ratio": {"levels": [0.2, 0.5, 0.8], "unit": "-", "type": "continuous"},
 "Material": {"levels": ["ZnO", "ITO", "TiO2"], "unit": "-", "type": "categorical"},
 }
 """
 summary = pd.DataFrame([
 {"Factor": k, "Levels": len(v["levels"]), "Values": str(v["levels"]),
 "Unit": v["unit"], "Type": v["type"]}
 for k, v in factor_dict.items
 ])
 print("=== Factor Design ===")
 print(summary.to_string(index=False))
 return summary
```

## 2. Orthogonal Arrays

```python
# Taguchi orthogonal arrays
# L4 (2^3 → 4 rows, 3 columns of 2 levels)
L4 = np.array([
 [0,0,0],
 [0,1,1],
 [1,0,1],
 [1,1,0],
])

# L9 (3^4 → 9 rows, 3 columns of 3 levels)
L9 = np.array([
 [0, 0, 0],
 [0, 1, 1],
 [0, 2, 2],
 [1, 0, 1],
 [1, 1, 2],
 [1, 2, 0],
 [2, 0, 2],
 [2, 1, 0],
 [2, 2, 1],
])

# L16 (2^15 → 16 rows, 15 columns of 2 levels)
L16 = np.array([
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
 [0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
 [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
 [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
 [0,1,1,0,0,1,1,1,1,0,0,1,1,0,0],
 [0,1,1,1,1,0,0,0,0,1,1,1,1,0,0],
 [0,1,1,1,1,0,0,1,1,0,0,0,0,1,1],
 [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
 [1,0,1,0,1,0,1,1,0,1,0,1,0,1,0],
 [1,0,1,1,0,1,0,0,1,0,1,1,0,1,0],
 [1,0,1,1,0,1,0,1,0,1,0,0,1,0,1],
 [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0],
 [1,1,0,0,1,1,0,1,0,0,1,1,0,0,1],
 [1,1,0,1,0,0,1,0,1,1,0,1,0,0,1],
 [1,1,0,1,0,0,1,1,0,0,1,0,1,1,0],
])

# L18 (2^1 × 3^7 → 18 rows, 8 columns: 1 col of 2 levels + 7 cols of 3 levels)
L18 = np.array([
 [0,0,0,0,0,0,0,0],
 [0,0,1,1,1,1,1,1],
 [0,0,2,2,2,2,2,2],
 [0,1,0,0,1,1,2,2],
 [0,1,1,1,2,2,0,0],
 [0,1,2,2,0,0,1,1],
 [0,2,0,1,0,2,1,2],
 [0,2,1,2,1,0,2,0],
 [0,2,2,0,2,1,0,1],
 [1,0,0,2,2,1,1,0],
 [1,0,1,0,0,2,2,1],
 [1,0,2,1,1,0,0,2],
 [1,1,0,1,2,0,2,1],
 [1,1,1,2,0,1,0,2],
 [1,1,2,0,1,2,1,0],
 [1,2,0,2,1,2,0,1],
 [1,2,1,0,2,0,1,2],
 [1,2,2,1,0,1,2,0],
])

# L27 (3^13 → 27 rows, 13 columns of 3 levels)
L27 = np.array([
 [0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,1,1,1,1,1,1,1,1,1],
 [0,0,0,0,2,2,2,2,2,2,2,2,2],
 [0,1,1,1,0,0,0,1,1,1,2,2,2],
 [0,1,1,1,1,1,1,2,2,2,0,0,0],
 [0,1,1,1,2,2,2,0,0,0,1,1,1],
 [0,2,2,2,0,0,0,2,2,2,1,1,1],
 [0,2,2,2,1,1,1,0,0,0,2,2,2],
 [0,2,2,2,2,2,2,1,1,1,0,0,0],
 [1,0,1,2,0,1,2,0,1,2,0,1,2],
 [1,0,1,2,1,2,0,1,2,0,1,2,0],
 [1,0,1,2,2,0,1,2,0,1,2,0,1],
 [1,1,2,0,0,1,2,1,2,0,2,0,1],
 [1,1,2,0,1,2,0,2,0,1,0,1,2],
 [1,1,2,0,2,0,1,0,1,2,1,2,0],
 [1,2,0,1,0,1,2,2,0,1,1,2,0],
 [1,2,0,1,1,2,0,0,1,2,2,0,1],
 [1,2,0,1,2,0,1,1,2,0,0,1,2],
 [2,0,2,1,0,2,1,0,2,1,0,2,1],
 [2,0,2,1,1,0,2,1,0,2,1,0,2],
 [2,0,2,1,2,1,0,2,1,0,2,1,0],
 [2,1,0,2,0,2,1,1,0,2,2,1,0],
 [2,1,0,2,1,0,2,2,1,0,0,2,1],
 [2,1,0,2,2,1,0,0,2,1,1,0,2],
 [2,2,1,0,0,2,1,2,1,0,1,0,2],
 [2,2,1,0,1,0,2,0,2,1,2,1,0],
 [2,2,1,0,2,1,0,1,0,2,0,2,1],
])

def generate_taguchi_design(factor_dict, array="L9"):
 """
 Generate experimental design from Taguchi orthogonal array.

 Available arrays:
 L4 (2^3) — 4 runs, up to 3 two-level factors
 L9 (3^4) — 9 runs, up to 3 three-level factors
 L16 (2^15) — 16 runs, up to 15 two-level factors
 L18 (2^1 × 3^7) — 18 runs, 1 two-level + up to 7 three-level factors
 L27 (3^13) — 27 runs, up to 13 three-level factors
 """
 arrays = {
 "L4": L4,
 "L9": L9,
 "L16": L16,
 "L18": L18,
 "L27": L27,
 }
 if array not in arrays:
 raise ValueError(
 f"Unknown orthogonal array '{array}'. "
 f"Available arrays: {', '.join(sorted(arrays.keys))}"
 )
 oa = arrays[array]
 factors = list(factor_dict.keys)

 runs = []
 for row in oa:
 run = {}
 for i, factor in enumerate(factors[:oa.shape[1]]):
 levels = factor_dict[factor]["levels"]
 run[factor] = levels[row[i] % len(levels)]
 runs.append(run)

 design_df = pd.DataFrame(runs)
 design_df.index.name = "Run"
 design_df.index += 1
 return design_df
```

## 3. Central Composite Design (CCD)

```python
from itertools import product

def central_composite_design(factor_dict, alpha="rotatable", center_points=3):
 """
 Generate Central Composite Design (CCD).

 Components:
 - 2^k full factorial design (cube points)
 - 2k axial/star points (axial/star points)
 - n_c center points

 alpha:
 "rotatable" — α = (2^k)^(1/4) (rotatable)
 "face" — α = 1 (face-centered)
 float — custom value
 """
 continuous_factors = {k: v for k, v in factor_dict.items
 if v["type"] == "continuous"}
 factor_names = list(continuous_factors.keys)
 k = len(factor_names)

 if alpha == "rotatable":
 alpha_val = (2 ** k) ** 0.25
 elif alpha == "face":
 alpha_val = 1.0
 else:
 alpha_val = float(alpha)

 # Coding: -1, 0, +1
 midpoints = {}
 half_ranges = {}
 for name, info in continuous_factors.items:
 levels = info["levels"]
 mid = (max(levels) + min(levels)) / 2
 half = (max(levels) - min(levels)) / 2
 midpoints[name] = mid
 half_ranges[name] = half

 runs = []

 # Cube points (2^k)
 for combo in product([-1, 1], repeat=k):
 run = {factor_names[i]: midpoints[factor_names[i]] + combo[i] * half_ranges[factor_names[i]]
 for i in range(k)}
 run["_type"] = "cube"
 runs.append(run)

 # Axial points (2k)
 for i in range(k):
 for direction in [-1, 1]:
 run = {name: midpoints[name] for name in factor_names}
 run[factor_names[i]] = midpoints[factor_names[i]] + direction * alpha_val * half_ranges[factor_names[i]]
 run["_type"] = "axial"
 runs.append(run)

 # Center points
 for _ in range(center_points):
 run = {name: midpoints[name] for name in factor_names}
 run["_type"] = "center"
 runs.append(run)

 design_df = pd.DataFrame(runs)
 design_df.index.name = "Run"
 design_df.index += 1
 return design_df
```

## 4. variancemin (ANOVA) — factor effect analysis

```python
from scipy.stats import f_oneway

def anova_factor_effects(design_df, response_col, factor_cols):
 """
 Evaluate main effects of each factor using ANOVA.

 Returns:
 DataFrame with Factor, SS, DF, MS, F_value, p_value, contribution_pct
 """
 ss_total = np.sum((design_df[response_col] - design_df[response_col].mean)**2)
 results = []

 for factor in factor_cols:
 groups = [group[response_col].values
 for _, group in design_df.groupby(factor)]
 if len(groups) < 2:
 continue
 f_val, p_val = f_oneway(*groups)

 # SS_factor
 grand_mean = design_df[response_col].mean
 ss_factor = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
 df_factor = len(groups) - 1
 ms_factor = ss_factor / df_factor

 results.append({
 "Factor": factor,
 "SS": ss_factor,
 "DF": df_factor,
 "MS": ms_factor,
 "F_value": f_val,
 "p_value": p_val,
 "Contribution_pct": ss_factor / ss_total * 100 if ss_total > 0 else 0,
 })

 return pd.DataFrame(results).sort_values("Contribution_pct", ascending=False)
```

## 5. Main Effect Plot

```python
import matplotlib.pyplot as plt

def main_effects_plot(design_df, response_col, factor_cols, figsize=None):
 """Draw main effects plot for all factors."""
 n = len(factor_cols)
 if figsize is None:
 figsize = (4 * n, 4)

 fig, axes = plt.subplots(1, n, figsize=figsize, sharey=True)
 if n == 1:
 axes = [axes]

 grand_mean = design_df[response_col].mean

 for ax, factor in zip(axes, factor_cols):
 means = design_df.groupby(factor)[response_col].mean
 ax.plot(range(len(means)), means.values, "bo-", linewidth=2, markersize=8)
 ax.axhline(grand_mean, color="gray", linestyle="--", alpha=0.5)
 ax.set_xticks(range(len(means)))
 ax.set_xticklabels(means.index, rotation=45)
 ax.set_xlabel(factor)
 ax.grid(alpha=0.3)

 axes[0].set_ylabel(response_col)
 plt.suptitle("Main Effects Plot", fontweight="bold", y=1.02)
 plt.tight_layout
 plt.savefig("figures/main_effects_plot.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 6. LHS Initial Pool Generation

```python
from scipy.stats.qmc import LatinHypercube

def generate_lhs_pool(bounds, n_iterations=100, batch_size=5, n_pool=None, seed=42):
 """
 Generate initial candidate pool via Latin Hypercube Sampling.

 Pool size auto-calculation:
 N >= n_iterations × batch_size × 3
 Fixed 20 points causes pool exhaustion, so size is auto-calculated
 based on iteration count and batch size. Manual specification also possible.

 Parameters:
 bounds: dict {"param": (low, high)}
 n_iterations: int — optimization steps
 batch_size: int — batch size
 n_pool: int or None — manual pool size (None for auto-calculation)
 seed: int — random seed (for reproducibility)
 Returns:
 np.ndarray (N, d) — LHS pool
 """
 param_names = list(bounds.keys)
 d = len(param_names)
 lows = np.array([bounds[p][0] for p in param_names])
 highs = np.array([bounds[p][1] for p in param_names])

 if n_pool is None:
 n_pool = max(n_iterations * batch_size * 3, 400)

 sampler = LatinHypercube(d=d, seed=seed)
 sample = sampler.random(n=n_pool)
 pool = lows + sample * (highs - lows)

 print(f"LHS pool: {n_pool} points in {d}D space "
 f"(auto: {n_iterations}×{batch_size}×3={n_iterations*batch_size*3})")
 return pool
```

## 7. Bayesianoptimization（ARD-RBF Gaussian Process）

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

def bayesian_optimization(objective_func, bounds, n_initial=None,
 n_iterations=100, kappa=2.576, batch_size=1):
 """
 Bayesian Optimization (ARD-RBF GP + UCB acquisition).

 v0.3.0: Kernel changed from isotropic Matern to ARD-RBF.
 ARD-RBF uses per-dimension length_scale, enabling convergence
 in high-dimensional spaces (d >= 10) where isotropic kernels fail.

 Initial points are generated via LHS (auto-sized) instead of
 fixed-size random uniform to ensure space-filling coverage.

 Parameters:
 objective_func: callable f(x) → y (maximize)
 bounds: dict {"param": (low, high)}
 n_initial: int or None — LHS initial points (None for auto-calculation)
 n_iterations: optimization steps
 kappa: exploration-exploitation tradeoff (UCB 's κ)
 batch_size: int — evaluations per step
 """
 from scipy.optimize import minimize as scipy_minimize
 from scipy.stats import norm

 param_names = list(bounds.keys)
 d = len(param_names)
 lows = np.array([bounds[p][0] for p in param_names])
 highs = np.array([bounds[p][1] for p in param_names])

 # Auto-sized LHS initial sampling
 if n_initial is None:
 n_initial = max(2 * d, 5)
 X_init = generate_lhs_pool(bounds, n_iterations=1, batch_size=n_initial,
 n_pool=n_initial)
 y_init = np.array([objective_func(dict(zip(param_names, x))) for x in X_init])

 X_observed = X_init.tolist
 y_observed = y_init.tolist

 # ARD-RBF: per-dimension length_scale
 kernel = RBF(length_scale=np.ones(d)) + WhiteKernel(noise_level=1e-3)
 gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5,
 random_state=42)

 for i in range(n_iterations):
 X_arr = np.array(X_observed)
 y_arr = np.array(y_observed)
 gp.fit(X_arr, y_arr)

 # UCB acquisition function
 def neg_ucb(x):
 mu, sigma = gp.predict(x.reshape(1, -1), return_std=True)
 return -(mu + kappa * sigma)

 # Optimize from multiple starting points
 best_x = None
 best_val = float("inf")
 for _ in range(10):
 x0 = np.random.uniform(lows, highs)
 res = scipy_minimize(neg_ucb, x0, bounds=list(zip(lows, highs)),
 method="L-BFGS-B")
 if res.fun < best_val:
 best_val = res.fun
 best_x = res.x

 # Evaluate new point
 y_new = objective_func(dict(zip(param_names, best_x)))
 X_observed.append(best_x.tolist)
 y_observed.append(y_new)

 # Optimal solution
 best_idx = np.argmax(y_observed)
 best_params = dict(zip(param_names, X_observed[best_idx]))
 best_y = y_observed[best_idx]

 return {
 "best_params": best_params,
 "best_value": best_y,
 "X_history": np.array(X_observed),
 "y_history": np.array(y_observed),
 "gp_model": gp,
 }
```

## 8. Interaction Plot

```python
def interaction_plot(design_df, response_col, factor1, factor2, figsize=(8, 6)):
 """Draw interaction plot between two factors."""
 fig, ax = plt.subplots(figsize=figsize)

 for level2, group in design_df.groupby(factor2):
 means = group.groupby(factor1)[response_col].mean
 ax.plot(range(len(means)), means.values, "o-", linewidth=2,
 markersize=8, label=f"{factor2}={level2}")

 ax.set_xticks(range(len(means)))
 ax.set_xticklabels(means.index)
 ax.set_xlabel(factor1)
 ax.set_ylabel(response_col)
 ax.set_title(f"Interaction Plot: {factor1} × {factor2}", fontweight="bold")
 ax.legend
 ax.grid(alpha=0.3)
 plt.tight_layout
 plt.savefig("figures/interaction_plot.png", dpi=300, bbox_inches="tight")
 plt.close
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

### Output Files

| File | Format |
|---|---|
| `results/experimental_design.csv` | CSV |
| `results/anova_factor_effects.csv` | CSV |
| `results/bayesian_optimization_history.csv` | CSV |
| `figures/main_effects_plot.png` | PNG |
| `figures/interaction_plot.png` | PNG |
| `figures/bayesian_convergence.png` | PNG |

## 9. dependencypackage

```
scipy>=1.10
scikit-learn>=1.3
```
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Experimental Design)

Before execution, define:
- [ ] **Factors and levels**: complete factor list with ranges
- [ ] **Response variable**: measurement method, precision
- [ ] **Design type**: factorial / fractional / RSM / sequential
- [ ] **Sample size**: power analysis with effect size justification

#### Pass Criteria
- Design matrix is orthogonal or near-orthogonal
- All factors have >= 2 levels with scientific justification
- Randomization order specified
- Blocking/stratification applied for known confounders
- Statistical model specified before data collection
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
