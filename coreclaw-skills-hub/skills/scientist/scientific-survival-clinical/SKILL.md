---
name: scientific-survival-clinical
description: |
 Survival and clinical analysis skill. Kaplan-Meier estimation, Cox proportional hazards, time-to-event analysis, competing risks, and clinical outcome modeling.
---

# Scientific Survival & Clinical Statistics

clinical trialdata'sanalysispipelineskill。timeanalysis、powermin、
allanalysis'sstandardworkflow is provided。

## When to Use

- timeanalysis（Kaplan-Meier, Cox PH）and
- clinical trial's sample sizepowercalculationwhen needed
- 's allanalysis（RR, OR, NNT, NNH）and
- Bayesianby/via

## Quick Start

## Standard Pipeline

### 1. powerminsample size

```python
from statsmodels.stats.power import TTestIndPower
import numpy as np

def power_analysis(effect_size, alpha=0.05, power=0.80, ratio=1.0):
 """
 2 group t testing's powermin。
 necessarysample sizeorpower is computed。
 """
 analysis = TTestIndPower

 # sample size
 n = analysis.solve_power(effect_size=effect_size, alpha=alpha,
 power=power, ratio=ratio, alternative="two-sided")

 # power
 n_range = np.arange(10, 500, 10)
 powers = [analysis.solve_power(effect_size=effect_size, nobs1=n1,
 alpha=alpha, ratio=ratio)
 for n1 in n_range]

 return {
 "required_n_per_group": int(np.ceil(n)),
 "effect_size": effect_size,
 "alpha": alpha,
 "target_power": power,
 "power_curve": {"n": n_range.tolist, "power": powers},
 }
```

### 2. Kaplan-Meier + Log-rank testing

```python
import matplotlib.pyplot as plt

def kaplan_meier_analysis(df, time_col, event_col, group_col,
 figsize=(10, 7)):
 """
 Perform Kaplan-Meier survival curves and Log-rank tests.
 """
 from lifelines import KaplanMeierFitter
 from lifelines.statistics import logrank_test

 fig, ax = plt.subplots(figsize=figsize)
 groups = sorted(df[group_col].unique)
 results = {}

 kmf = KaplanMeierFitter
 for group in groups:
 mask = df[group_col] == group
 kmf.fit(df.loc[mask, time_col],
 event_observed=df.loc[mask, event_col],
 label=str(group))
 kmf.plot_survival_function(ax=ax, ci_show=True)
 results[group] = {
 "median_survival": kmf.median_survival_time_,
 "n": mask.sum,
 }

 # Log-rank testing
 if len(groups) == 2:
 g1 = df[df[group_col] == groups[0]]
 g2 = df[df[group_col] == groups[1]]
 lr = logrank_test(
 g1[time_col], g2[time_col],
 event_observed_A=g1[event_col],
 event_observed_B=g2[event_col]
 )
 results["logrank_p"] = lr.p_value
 ax.text(0.65, 0.85, f"Log-rank p = {lr.p_value:.4f}",
 transform=ax.transAxes, fontsize=11,
 bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat"))

 ax.set_xlabel("Time", fontsize=12)
 ax.set_ylabel("Survival Probability", fontsize=12)
 ax.set_title("Kaplan-Meier Survival Curves", fontsize=14, fontweight="bold")
 ax.set_ylim(0, 1.05)
 plt.tight_layout
 plt.savefig("figures/kaplan_meier.png", dpi=300, bbox_inches="tight")
 plt.close
 return results
```

### 3. Cox example

```python
def cox_proportional_hazard(df, time_col, event_col, covariates):
 """
 Cox example 、 is computed。
 """
 from lifelines import CoxPHFitter

 cph = CoxPHFitter
 cox_df = df[[time_col, event_col] + covariates].dropna
 cph.fit(cox_df, duration_col=time_col, event_col=event_col)

 # 
 summary = cph.summary
 summary.to_csv("results/cox_ph_results.csv")

 # Forest plot shapeformula'svisualization
 fig, ax = plt.subplots(figsize=(10, max(4, len(covariates) * 0.8)))
 cph.plot(ax=ax)
 ax.set_title("Cox PH: Hazard Ratios", fontweight="bold")
 ax.axvline(x=0, color="gray", linestyle="--")
 plt.tight_layout
 plt.savefig("figures/cox_ph_forest.png", dpi=300, bbox_inches="tight")
 plt.close

 return cph, summary
```

### 4. allanalysis（RR, OR, NNT, NNH）

```python
def safety_analysis(n_event_treatment, n_total_treatment,
 n_event_control, n_total_control, event_name="AE"):
 """'s all is computed。"""
 p_t = n_event_treatment / n_total_treatment
 p_c = n_event_control / n_total_control

 # phase
 rr = p_t / p_c if p_c > 0 else np.inf

 # 
 odds_t = p_t / (1 - p_t) if p_t < 1 else np.inf
 odds_c = p_c / (1 - p_c) if p_c < 1 else np.inf
 odds_ratio = odds_t / odds_c if odds_c > 0 else np.inf

 # NNT / NNH
 ard = abs(p_t - p_c)
 nnt_nnh = 1 / ard if ard > 0 else np.inf
 metric = "NNH" if p_t > p_c else "NNT"

 return {
 "Event": event_name,
 "Rate_Treatment": f"{p_t:.3f}",
 "Rate_Control": f"{p_c:.3f}",
 "Relative_Risk": f"{rr:.3f}",
 "Odds_Ratio": f"{odds_ratio:.3f}",
 "ARD": f"{ard:.3f}",
 metric: f"{nnt_nnh:.1f}",
 }
```

### 5. Bayesian（Exp-06 ）

```python
from scipy.stats import beta as beta_dist

def bayesian_sequential_update(successes_list, trials_list,
 prior_alpha=1, prior_beta=1,
 figsize=(12, 6)):
 """
 Beta-Binomial by/viaBayesian'svisualization。
 successes_list / trials_list: eachanalysispoint's value
 """
 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
 x = np.linspace(0, 1, 500)

 alpha, beta = prior_alpha, prior_beta

 for i, (s, n) in enumerate(zip(successes_list, trials_list)):
 alpha_post = alpha + s
 beta_post = beta + (n - s)

 posterior = beta_dist(alpha_post, beta_post)
 ax1.plot(x, posterior.pdf(x), linewidth=2,
 label=f"Interim {i+1} (n={n})")

 alpha, beta = alpha_post, beta_post

 ax1.set_xlabel("Response Rate")
 ax1.set_ylabel("Density")
 ax1.set_title("Bayesian Sequential Update", fontweight="bold")
 ax1.legend

 # for's
 ci_lower = [beta_dist(prior_alpha + s, prior_beta + n - s).ppf(0.025)
 for s, n in zip(successes_list, trials_list)]
 ci_upper = [beta_dist(prior_alpha + s, prior_beta + n - s).ppf(0.975)
 for s, n in zip(successes_list, trials_list)]
 means = [beta_dist(prior_alpha + s, prior_beta + n - s).mean
 for s, n in zip(successes_list, trials_list)]

 ax2.fill_between(range(1, len(means) + 1), ci_lower, ci_upper,
 alpha=0.3, color="steelblue")
 ax2.plot(range(1, len(means) + 1), means, "bo-", linewidth=2)
 ax2.set_xlabel("Interim Analysis")
 ax2.set_ylabel("Posterior Mean (95% CI)")
 ax2.set_title("Credible Interval Evolution", fontweight="bold")

 plt.tight_layout
 plt.savefig("figures/bayesian_update.png", dpi=300, bbox_inches="tight")
 plt.close
```

## References

### Output Files

| File | Format |
|---|---|
| `results/cox_ph_results.csv` | CSV |
| `results/safety_analysis.csv` | CSV |
| `figures/kaplan_meier.png` | PNG |
| `figures/cox_ph_forest.png` | PNG |
| `figures/bayesian_update.png` | PNG |

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

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-causal-inference` | ← causal inference |
| `scientific-meta-analysis` | ← integrated analysisintegration |
| `scientific-statistical-testing` | ← hypothesistestingmultiple comparison |
| `scientific-clinical-trials-analytics` | ← ClinicalTrials.gov data |
| `scientific-pharmacovigilance` | → AE data's allanalysis |
| `scientific-clinical-decision-support` | → analysisresults's application |

#### Reference Experiments

- **Exp-03**: Kaplan-Meier + Cox PH（canceranalysis）
- **Exp-06**: Phase III RCT analysis（power、frequency+Bayesian、all）
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
