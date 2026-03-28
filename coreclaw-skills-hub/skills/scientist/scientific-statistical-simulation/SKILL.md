---
name: scientific-statistical-simulation
description: |
 Statistical simulation skill. Monte Carlo methods, bootstrap confidence intervals, permutation tests, power simulation, and simulation-based inference.
---

# Scientific Statistical Simulation

's simulation than、
inference's uncertaintyamountpowerdesignevaluation is performed。

## When to Use

- Monte Carlo simulation probability distribution is estimatedand
- Bootstrap confidence interval is computedand
- Permutation Test testing is performedand
- experimentnecessarysample sizepowermin and
- 's rateevaluation is performedand

---

## Quick Start

## 1. Monte Carlo simulation

```python
import numpy as np
import pandas as pd
from typing import Callable, Dict, Any


def monte_carlo_simulation(func, param_distributions,
 n_simulations=10000, seed=42,
 summary_quantiles=None):
 """
 Monte Carlo simulation。

 Parameters:
 func: Callable — simulationnumber/count (dict → float)
 param_distributions: dict — {param_name: scipy.stats distribution}
 n_simulations: int — simulationtimesnumber/count
 seed: int — random seed
 summary_quantiles: list[float] | None — summaryminpoint
 """
 rng = np.random.default_rng(seed)
 if summary_quantiles is None:
 summary_quantiles = [0.025, 0.25, 0.5, 0.75, 0.975]

 results = []
 param_samples = {}

 # parameterssampling
 for name, dist in param_distributions.items:
 param_samples[name] = dist.rvs(
 size=n_simulations, random_state=rng)

 # simulation
 for i in range(n_simulations):
 params = {name: samples[i]
 for name, samples in param_samples.items}
 results.append(func(params))

 results = np.array(results)

 # summary
 summary = {
 "mean": np.mean(results),
 "std": np.std(results),
 "min": np.min(results),
 "max": np.max(results),
 }
 for q in summary_quantiles:
 summary[f"q{q:.3f}"] = np.quantile(results, q)

 print(f"Monte Carlo ({n_simulations} runs):")
 print(f" Mean={summary['mean']:.4f} ± {summary['std']:.4f}")
 print(f" 95% CI: [{summary.get('q0.025', 'N/A'):.4f}, "
 f"{summary.get('q0.975', 'N/A'):.4f}]")

 return {"results": results, "summary": summary,
 "param_samples": param_samples}
```

## 2. Bootstrap inference

```python
def bootstrap_inference(data, statistic_fn, n_bootstrap=10000,
 confidence_level=0.95, method="bca",
 seed=42):
 """
 Bootstrap confidence interval。

 Parameters:
 data: np.ndarray — data
 statistic_fn: Callable — amountcalculationnumber/count (data → float)
 n_bootstrap: int — Bootstrap timesnumber/count
 confidence_level: float — levels
 method: str — "percentile" / "bca" / "basic"
 seed: int — random seed
 """
 rng = np.random.default_rng(seed)
 n = len(data)
 observed = statistic_fn(data)

 # Bootstrap sample
 boot_stats = np.array([
 statistic_fn(data[rng.integers(0, n, size=n)])
 for _ in range(n_bootstrap)])

 alpha = 1 - confidence_level
 if method == "percentile":
 ci_low = np.quantile(boot_stats, alpha / 2)
 ci_high = np.quantile(boot_stats, 1 - alpha / 2)
 elif method == "bca":
 from scipy import stats as sp_stats
 # Bias correction
 z0 = sp_stats.norm.ppf(np.mean(boot_stats < observed))
 # Acceleration (jackknife)
 jack_stats = np.array([
 statistic_fn(np.delete(data, i)) for i in range(n)])
 jack_mean = jack_stats.mean
 a = (np.sum((jack_mean - jack_stats) ** 3) /
 (6 * np.sum((jack_mean - jack_stats) ** 2) ** 1.5 + 1e-10))
 z_alpha = sp_stats.norm.ppf([alpha / 2, 1 - alpha / 2])
 adjusted = sp_stats.norm.cdf(
 z0 + (z0 + z_alpha) / (1 - a * (z0 + z_alpha)))
 ci_low = np.quantile(boot_stats, adjusted[0])
 ci_high = np.quantile(boot_stats, adjusted[1])
 else: # basic
 ci_low = 2 * observed - np.quantile(boot_stats, 1 - alpha / 2)
 ci_high = 2 * observed - np.quantile(boot_stats, alpha / 2)

 result = {
 "observed": observed,
 "boot_mean": np.mean(boot_stats),
 "boot_std": np.std(boot_stats),
 "ci_low": ci_low, "ci_high": ci_high,
 "method": method,
 "confidence_level": confidence_level,
 }
 print(f"Bootstrap ({method}): {observed:.4f} "
 f"[{ci_low:.4f}, {ci_high:.4f}] ({confidence_level:.0%} CI)")
 return result, boot_stats
```

## 3. powermin

```python
def power_analysis(effect_size_range=None, n_range=None,
 alpha=0.05, test_type="two-sample-t",
 n_simulations=5000, seed=42):
 """
 simulationpowermin。

 Parameters:
 effect_size_range: list[float] | None — effect size's range
 n_range: list[int] | None — sample size's range
 alpha: float — significance level
 test_type: str — "two-sample-t" / "paired-t" / "chi-square"
 n_simulations: int — eachcondition's simulationtimesnumber/count
 seed: int — random seed
 """
 from scipy import stats as sp_stats

 rng = np.random.default_rng(seed)
 if effect_size_range is None:
 effect_size_range = [0.2, 0.5, 0.8]
 if n_range is None:
 n_range = [10, 20, 30, 50, 100, 200]

 records = []
 for es in effect_size_range:
 for n in n_range:
 rejections = 0
 for _ in range(n_simulations):
 if test_type == "two-sample-t":
 x = rng.normal(0, 1, n)
 y = rng.normal(es, 1, n)
 _, p = sp_stats.ttest_ind(x, y)
 elif test_type == "paired-t":
 diff = rng.normal(es, 1, n)
 _, p = sp_stats.ttest_1samp(diff, 0)
 else:
 raise ValueError(f"Unknown test: {test_type}")

 if p < alpha:
 rejections += 1

 power = rejections / n_simulations
 records.append({
 "effect_size": es, "n": n,
 "power": power, "alpha": alpha,
 })

 df = pd.DataFrame(records)
 for es in effect_size_range:
 sub = df[df["effect_size"] == es]
 adequate = sub[sub["power"] >= 0.8]
 if len(adequate) > 0:
 min_n = adequate["n"].min
 print(f"d={es}: min N={min_n} for power≥0.80")
 else:
 print(f"d={es}: power<0.80 for all tested N")

 return df
```

---

## Pipeline Integration

```
[hypothesisdesign] → statistical-simulation → statistical-testing
 (simulation) (papersanalysis)
 │
 doe ← adaptive-experiments
 (Experimental Design) (experiment)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `mc_results.npz` | Monte Carlo results | → evaluation |
| `bootstrap_ci.csv` | confidence interval | → report |
| `power_analysis.csv` | power | → DOE sample size |

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
