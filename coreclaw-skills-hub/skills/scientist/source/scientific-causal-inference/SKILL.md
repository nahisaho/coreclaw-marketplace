---
name: scientific-causal-inference
description: |
 causal inferenceskill。（PSM）、rate（IPW / IPTW）、
 number/countmethod（2SLS）、min's minmethod（DID）、regression（RDD）、
 DAG 'scovariatesselection（backdoor criterion）、sensitivity analysistemplate providing。
---

# Scientific Causal Inference

observationdatafrom is estimatedformethodpipeline。
RCT confounding factors、 possible.

## When to Use

- observationdatafrom（ATE / ATT）when needed
- confounding factors'swhen needed
- by/viaandwhen needed
- experimentdata（DID / RDD）minwhen needed
- DAG structure explicitwhen needed

---

## Quick Start

## 1. DAG（timesgraph）'s definition

```python
import networkx as nx
import matplotlib.pyplot as plt

def define_causal_dag(edges, treatment, outcome, figsize=(10, 6)):
 """
 DAG definitionvisualization.

 Parameters:
 edges: list of (cause, effect) tuples
 treatment: number/count
 outcome: number/count

 Example:
 edges = [("Age", "Treatment"), ("Age", "Outcome"),
 ("Treatment", "Outcome"), ("Gender", "Treatment")]
 """
 G = nx.DiGraph
 G.add_edges_from(edges)

 # min
 color_map = []
 for node in G.nodes:
 if node == treatment:
 color_map.append("#FF6B6B")
 elif node == outcome:
 color_map.append("#4ECDC4")
 else:
 color_map.append("#95E1D3")

 fig, ax = plt.subplots(figsize=figsize)
 pos = nx.spring_layout(G, k=2, seed=42)
 nx.draw(G, pos, ax=ax, with_labels=True, node_color=color_map,
 node_size=2000, font_size=11, font_weight="bold",
 edge_color="gray", arrows=True, arrowsize=20, width=2)
 ax.set_title("Causal DAG", fontweight="bold", fontsize=14)
 plt.tight_layout
 plt.savefig("figures/causal_dag.png", dpi=300, bbox_inches="tight")
 plt.close

 return G


def identify_confounders(dag, treatment, outcome):
 """
 Backdoor criterion -basedcovariates's 。
 →'s number/count is returned。
 """
 # : treatment 's node's、outcome also number/count
 parents_of_treatment = set(dag.predecessors(treatment))
 confounders = set

 for parent in parents_of_treatment:
 if nx.has_path(dag, parent, outcome):
 confounders.add(parent)

 return confounders
```

## 2. (PSM)

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.spatial.distance import cdist

def propensity_score_matching(df, treatment_col, covariates, outcome_col,
 caliper=0.2, n_matches=1):
 """
 。

 Steps:
 1. regression P(T=1|X) 
 2. （）
 3. 's covariates
 4. ATE / ATT 's

 Parameters:
 caliper: （'sstandard deviation's rate）
 """
 # Step 1: 
 X = df[covariates].values
 T = df[treatment_col].values

 lr = LogisticRegression(max_iter=1000, random_state=42)
 lr.fit(X, T)
 ps = lr.predict_proba(X)[:, 1]
 df = df.copy
 df["propensity_score"] = ps

 # Step 2: 
 treated_idx = df[df[treatment_col] == 1].index
 control_idx = df[df[treatment_col] == 0].index

 ps_treated = ps[treated_idx]
 ps_control = ps[control_idx]

 caliper_val = caliper * np.std(ps)
 matched_pairs = []

 for i, t_idx in enumerate(treated_idx):
 distances = np.abs(ps_treated[i] - ps_control)
 within_caliper = np.where(distances <= caliper_val)[0]
 if len(within_caliper) > 0:
 best = within_caliper[np.argmin(distances[within_caliper])]
 matched_pairs.append((t_idx, control_idx[best]))

 print(f" Matched {len(matched_pairs)} / {len(treated_idx)} treated units")

 # Step 3: (SMD)
 matched_treated = df.loc[[p[0] for p in matched_pairs]]
 matched_control = df.loc[[p[1] for p in matched_pairs]]

 balance = []
 for cov in covariates:
 smd_before = _standardized_mean_diff(
 df[df[treatment_col]==1][cov], df[df[treatment_col]==0][cov])
 smd_after = _standardized_mean_diff(
 matched_treated[cov], matched_control[cov])
 balance.append({
 "covariate": cov,
 "SMD_before": smd_before,
 "SMD_after": smd_after,
 "balanced": abs(smd_after) < 0.1,
 })

 balance_df = pd.DataFrame(balance)

 # Step 4: ATT 
 att = matched_treated[outcome_col].mean - matched_control[outcome_col].mean

 return {
 "ATT": att,
 "n_matched": len(matched_pairs),
 "balance": balance_df,
 "propensity_scores": ps,
 "matched_pairs": matched_pairs,
 }


def _standardized_mean_diff(x1, x2):
 """Standardized Mean Difference (SMD) = |μ1 - μ2| / sqrt((s1² + s2²)/2)"""
 return abs(x1.mean - x2.mean) / np.sqrt((x1.var + x2.var) / 2 + 1e-10)
```

## 3. rate (IPW / IPTW)

```python
def inverse_probability_weighting(df, treatment_col, covariates, outcome_col):
 """
 rateamount (IPTW - Inverse Probability of Treatment Weighting)。

 ATE = E[Y(1)] - E[Y(0)]
 = Σ (T·Y/PS) / Σ (T/PS) - Σ ((1-T)·Y/(1-PS)) / Σ ((1-T)/(1-PS))
 """
 X = df[covariates].values
 T = df[treatment_col].values
 Y = df[outcome_col].values

 # 
 lr = LogisticRegression(max_iter=1000, random_state=42)
 lr.fit(X, T)
 ps = lr.predict_proba(X)[:, 1]

 # calculation（）
 w_treated = T / (ps + 1e-10)
 w_control = (1 - T) / (1 - ps + 1e-10)

 # ATE
 E_Y1 = np.sum(w_treated * Y) / np.sum(w_treated)
 E_Y0 = np.sum(w_control * Y) / np.sum(w_control)
 ate = E_Y1 - E_Y0

 # ATT
 att = np.mean(T * Y) - np.sum((1-T) * ps / (1-ps+1e-10) * Y) / np.sum((1-T) * ps / (1-ps+1e-10))

 return {
 "ATE": ate,
 "ATT": att,
 "E_Y1": E_Y1,
 "E_Y0": E_Y0,
 "propensity_scores": ps,
 "weights_treated": w_treated,
 "weights_control": w_control,
 }
```

## 4. min's minmethod (DID)

```python
import statsmodels.api as sm

def difference_in_differences(df, time_col, treatment_col, outcome_col,
 covariates=None):
 """
 min's minmethod (Difference-in-Differences)。

 Y = β0 + β1·Post + β2·Treat + β3·(Post × Treat) + ε
 β3 （DID amount）
 """
 df = df.copy
 df["interaction"] = df[time_col] * df[treatment_col]

 X_cols = [time_col, treatment_col, "interaction"]
 if covariates:
 X_cols += covariates

 X = sm.add_constant(df[X_cols])
 model = sm.OLS(df[outcome_col], X).fit

 return {
 "DID_estimate": model.params["interaction"],
 "DID_se": model.bse["interaction"],
 "DID_pvalue": model.pvalues["interaction"],
 "DID_ci_95": model.conf_int.loc["interaction"].tolist,
 "model_summary": model.summary2.tables[1],
 }
```

## 5. regression (RDD)

```python
def regression_discontinuity(df, running_var, outcome_col, cutoff,
 bandwidth=None, kernel="triangular"):
 """
 regression (Sharp RDD)。

 'sregressionby/via's 。

 Parameters:
 running_var: number/count（running variable）
 cutoff: value
 bandwidth: （None = IK ）
 """
 df = df.copy
 df["centered"] = df[running_var] - cutoff
 df["treated"] = (df[running_var] >= cutoff).astype(int)

 if bandwidth is None:
 bandwidth = 1.5 * df["centered"].std

 # 'sdata
 in_band = df[df["centered"].abs <= bandwidth]

 # kernel
 if kernel == "triangular":
 weights = 1 - np.abs(in_band["centered"]) / bandwidth
 else:
 weights = np.ones(len(in_band))

 # lineshaperegression
 X = sm.add_constant(in_band[["centered", "treated"]])
 X["interaction"] = in_band["centered"] * in_band["treated"]
 model = sm.WLS(in_band[outcome_col], X, weights=weights).fit

 return {
 "RDD_estimate": model.params["treated"],
 "RDD_se": model.bse["treated"],
 "RDD_pvalue": model.pvalues["treated"],
 "RDD_ci_95": model.conf_int.loc["treated"].tolist,
 "bandwidth": bandwidth,
 "n_in_bandwidth": len(in_band),
 }
```

## 6. sensitivity analysis（Rosenbaum Bounds）

```python
def rosenbaum_sensitivity(matched_outcomes_treated, matched_outcomes_control,
 gamma_range=None):
 """
 Rosenbaum sensitivity analysis。
 's degree Γ for/against'sevaluation。

 Γ = 1: 
 Γ > 1: Γ's items
 """
 from scipy.stats import norm

 if gamma_range is None:
 gamma_range = np.arange(1.0, 3.1, 0.1)

 diffs = matched_outcomes_treated - matched_outcomes_control
 n = len(diffs)
 signs = (diffs > 0).astype(int)
 T_obs = np.sum(signs)

 results = []
 for gamma in gamma_range:
 p_upper = gamma / (1 + gamma)
 E_T = n * p_upper
 Var_T = n * p_upper * (1 - p_upper)
 z = (T_obs - E_T) / np.sqrt(Var_T + 1e-10)
 p_value = 1 - norm.cdf(z)
 results.append({"gamma": gamma, "z_statistic": z, "p_value": p_value})

 return pd.DataFrame(results)
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
| `results/causal_estimates.csv` | CSV |
| `results/covariate_balance.csv` | CSV |
| `results/sensitivity_analysis.csv` | CSV |
| `figures/causal_dag.png` | PNG |
| `figures/propensity_distribution.png` | PNG |
| `figures/rdd_plot.png` | PNG |

#### Dependencies

```
statsmodels>=0.14
scikit-learn>=1.3
networkx>=3.0
```
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
