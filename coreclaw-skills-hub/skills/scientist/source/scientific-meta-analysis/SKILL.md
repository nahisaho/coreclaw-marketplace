---
name: scientific-meta-analysis
description: |
 analysisskill。（DerSimonian-Laird）、Forest plot、
 evaluation（I²/Q testing/τ²）、publication（Funnel plot/Egger/Begg testing）、
 loopanalysis、regression、analysis's templateproviding。
---

# Scientific Meta-Analysis

multiple's researchresults integration、all amountforskill。
effect size（SMD / OR / RR / MD）'s integration、evaluation、publication's pipeline
is provided.

## When to Use

- multiple's researchexperimentresults integrationevaluationwhen needed
- effect size（Hedges' g / Cohen's d / SMD） is computedand
- Forest plot / Funnel plot drawing/plottingwhen needed
- research's amountwhen needed（I² / Q / τ²）
- publication'stestingwhen needed

---

## Quick Start

## 1. effect size's

```python
import numpy as np
import pandas as pd
from scipy.stats import norm

def compute_effect_sizes(studies_df, effect_type="SMD"):
 """
 eachresearch's effect size and variance is computed。

 effect_type:
 "SMD" — Standardized Mean Difference (Hedges' g)
 "MD" — Mean Difference 
 "OR" — Odds Ratio (log transformation)
 "RR" — Risk Ratio (log transformation)

 Input columns (SMD/MD):
 mean1, sd1, n1, mean2, sd2, n2

 Input columns (OR/RR):
 events1, total1, events2, total2
 """
 df = studies_df.copy

 if effect_type == "SMD":
 # Cohen's d → Hedges' g (samplecorrection)
 pooled_sd = np.sqrt(
 ((df["n1"]-1)*df["sd1"]**2 + (df["n2"]-1)*df["sd2"]**2) /
 (df["n1"] + df["n2"] - 2)
 )
 d = (df["mean1"] - df["mean2"]) / pooled_sd
 # Hedges' correction factor
 J = 1 - 3 / (4*(df["n1"]+df["n2"]-2) - 1)
 df["effect_size"] = d * J
 df["variance"] = (df["n1"]+df["n2"])/(df["n1"]*df["n2"]) + \
 df["effect_size"]**2 / (2*(df["n1"]+df["n2"]))

 elif effect_type == "MD":
 df["effect_size"] = df["mean1"] - df["mean2"]
 df["variance"] = df["sd1"]**2/df["n1"] + df["sd2"]**2/df["n2"]

 elif effect_type == "OR":
 a = df["events1"]; b = df["total1"] - df["events1"]
 c = df["events2"]; d_val = df["total2"] - df["events2"]
 df["effect_size"] = np.log((a * d_val) / (b * c + 1e-10) + 1e-10)
 df["variance"] = 1/a + 1/b + 1/c + 1/d_val

 elif effect_type == "RR":
 p1 = df["events1"] / df["total1"]
 p2 = df["events2"] / df["total2"]
 df["effect_size"] = np.log(p1 / (p2 + 1e-10) + 1e-10)
 df["variance"] = (1-p1)/(df["events1"]+1e-10) + \
 (1-p2)/(df["events2"]+1e-10)

 df["se"] = np.sqrt(df["variance"])
 df["ci_lower"] = df["effect_size"] - 1.96 * df["se"]
 df["ci_upper"] = df["effect_size"] + 1.96 * df["se"]
 df["weight"] = 1 / df["variance"]

 return df
```

## 2. / 

```python
def meta_analysis(studies_df, model="random"):
 """
 analysisintegration。

 model:
 "fixed" — (Inverse-Variance weighted)
 "random" — (DerSimonian-Laird)

 Input: DataFrame with columns: study, effect_size, variance
 """
 es = studies_df["effect_size"].values
 var = studies_df["variance"].values
 w = 1 / var
 k = len(es)

 # 
 theta_fixed = np.sum(w * es) / np.sum(w)
 se_fixed = 1 / np.sqrt(np.sum(w))

 # 
 Q = np.sum(w * (es - theta_fixed)**2)
 df_Q = k - 1
 p_Q = 1 - __import__("scipy").stats.chi2.cdf(Q, df_Q)
 I2 = max(0, (Q - df_Q) / Q * 100) if Q > 0 else 0

 if model == "random":
 # DerSimonian-Laird τ² 
 C = np.sum(w) - np.sum(w**2) / np.sum(w)
 tau2 = max(0, (Q - df_Q) / C)

 # 
 w_re = 1 / (var + tau2)
 theta_random = np.sum(w_re * es) / np.sum(w_re)
 se_random = 1 / np.sqrt(np.sum(w_re))

 summary_effect = theta_random
 summary_se = se_random
 else:
 tau2 = 0
 summary_effect = theta_fixed
 summary_se = se_fixed

 z = summary_effect / summary_se
 p_val = 2 * (1 - norm.cdf(abs(z)))

 return {
 "model": model,
 "summary_effect": summary_effect,
 "se": summary_se,
 "ci_lower": summary_effect - 1.96 * summary_se,
 "ci_upper": summary_effect + 1.96 * summary_se,
 "z_value": z,
 "p_value": p_val,
 "Q_statistic": Q,
 "Q_p_value": p_Q,
 "I_squared": I2,
 "tau_squared": tau2,
 "k_studies": k,
 }
```

## 3. Forest plot

```python
import matplotlib.pyplot as plt

def forest_plot(studies_df, meta_result, effect_label="SMD",
 figsize=(10, None)):
 """
 Forest plot drawing/plotting.

 studies_df: study, effect_size, ci_lower, ci_upper, weight
 meta_result: meta_analysis 's output
 """
 k = len(studies_df)
 if figsize[1] is None:
 figsize = (figsize[0], max(4, k * 0.4 + 2))

 fig, ax = plt.subplots(figsize=figsize)

 y_positions = range(k, 0, -1)

 # unitsresearch
 for i, (_, row) in enumerate(studies_df.iterrows):
 y = list(y_positions)[i]
 ax.plot([row["ci_lower"], row["ci_upper"]], [y, y],
 "b-", linewidth=1.5)
 size = row.get("weight", 1) / studies_df["weight"].max * 200 + 20
 ax.plot(row["effect_size"], y, "bs", markersize=np.sqrt(size),
 markerfacecolor="steelblue")
 ax.text(-0.05, y, row.get("study", f"Study {i+1}"),
 ha="right", va="center", fontsize=9,
 transform=ax.get_yaxis_transform)

 # summary
 y_summary = 0
 diamond_x = [meta_result["ci_lower"], meta_result["summary_effect"],
 meta_result["ci_upper"], meta_result["summary_effect"]]
 diamond_y = [y_summary, y_summary + 0.3, y_summary, y_summary - 0.3]
 ax.fill(diamond_x, diamond_y, color="red", alpha=0.7)
 ax.text(-0.05, y_summary, "Summary",
 ha="right", va="center", fontsize=9, fontweight="bold",
 transform=ax.get_yaxis_transform)

 # referenceline
 ax.axvline(0, color="black", linestyle="-", linewidth=0.5)

 ax.set_xlabel(effect_label)
 ax.set_yticks([])
 ax.set_title(f"Forest Plot (I²={meta_result['I_squared']:.1f}%, "
 f"p={meta_result['p_value']:.4f})", fontweight="bold")

 # number/countvalue
 for i, (_, row) in enumerate(studies_df.iterrows):
 y = list(y_positions)[i]
 ax.text(1.02, y, f"{row['effect_size']:.2f} [{row['ci_lower']:.2f}, "
 f"{row['ci_upper']:.2f}]",
 ha="left", va="center", fontsize=8,
 transform=ax.get_yaxis_transform)

 plt.tight_layout
 plt.savefig("figures/forest_plot.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 4. publication

### 4.1 Funnel plot

```python
def funnel_plot(studies_df, meta_result, figsize=(8, 6)):
 """
 Funnel plot drawing/plotting.
 publication's。
 """
 fig, ax = plt.subplots(figsize=figsize)

 ax.scatter(studies_df["effect_size"], studies_df["se"],
 c="steelblue", s=50, edgecolors="black", zorder=5)

 # referenceline
 ax.axvline(meta_result["summary_effect"], color="red", linestyle="--")

 # 95% confidence interval
 se_range = np.linspace(0, studies_df["se"].max * 1.1, 100)
 ax.plot(meta_result["summary_effect"] - 1.96 * se_range, se_range,
 "gray", linestyle="--", alpha=0.5)
 ax.plot(meta_result["summary_effect"] + 1.96 * se_range, se_range,
 "gray", linestyle="--", alpha=0.5)

 ax.set_xlabel("Effect Size")
 ax.set_ylabel("Standard Error")
 ax.set_title("Funnel Plot", fontweight="bold")
 ax.invert_yaxis
 plt.tight_layout
 plt.savefig("figures/funnel_plot.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 4.2 Egger testing

```python
import statsmodels.api as sm

def egger_test(studies_df):
 """
 Egger regressiontesting — Funnel plot'stesting。

 y = effect_size / se
 x = 1 / se
 ≠ 0 → publication
 """
 precision = 1 / studies_df["se"]
 z_score = studies_df["effect_size"] / studies_df["se"]

 X = sm.add_constant(precision)
 model = sm.OLS(z_score, X).fit

 return {
 "intercept": model.params["const"],
 "intercept_se": model.bse["const"],
 "intercept_p": model.pvalues["const"],
 "publication_bias": model.pvalues["const"] < 0.05,
 }
```

## 5. loopanalysis

```python
def subgroup_analysis(studies_df, subgroup_col, model="random"):
 """loop and analysis、looptesting."""
 subgroups = studies_df[subgroup_col].unique
 results = []

 for sg in subgroups:
 subset = studies_df[studies_df[subgroup_col] == sg]
 if len(subset) >= 2:
 ma = meta_analysis(subset, model=model)
 ma["subgroup"] = sg
 ma["k"] = len(subset)
 results.append(ma)

 results_df = pd.DataFrame(results)

 # looptesting (Q_between)
 overall = meta_analysis(studies_df, model=model)
 Q_within = sum(r["Q_statistic"] for r in results)
 Q_between = overall["Q_statistic"] - Q_within
 df_between = len(results) - 1
 p_between = 1 - __import__("scipy").stats.chi2.cdf(Q_between, df_between)

 return {
 "subgroup_results": results_df,
 "Q_between": Q_between,
 "df_between": df_between,
 "p_between": p_between,
 }
```

## 6. analysis

```python
def cumulative_meta_analysis(studies_df, sort_by="year", model="random"):
 """
 researchadditionanalysis is executed。
 'svisualization。
 """
 sorted_df = studies_df.sort_values(sort_by)
 cumulative_results = []

 for i in range(2, len(sorted_df) + 1):
 subset = sorted_df.iloc[:i]
 ma = meta_analysis(subset, model=model)
 ma["n_studies"] = i
 ma["last_added"] = sorted_df.iloc[i-1].get("study", f"Study {i}")
 cumulative_results.append(ma)

 return pd.DataFrame(cumulative_results)
```

## References

### Output Files

| File | Format |
|---|---|
| `results/meta_analysis_summary.csv` | CSV |
| `results/effect_sizes.csv` | CSV |
| `results/publication_bias_tests.csv` | CSV |
| `results/subgroup_analysis.csv` | CSV |
| `figures/forest_plot.png` | PNG |
| `figures/funnel_plot.png` | PNG |
| `figures/cumulative_meta.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| PubMed | `PubMed_search_articles` | literaturesearch |
| PubMed | `PubMed_get_article` | article metadata retrieval |
| EuropePMC | `EuropePMC_search_articles` | European literature search |
| Crossref | `Crossref_search_works` | publication information search |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-survival-clinical` | ← analysisvalue HR |
| `scientific-statistical-testing` | ← hypothesistestingeffect size |
| `scientific-deep-research` | ← phylogenyliteraturesearch |
| `scientific-clinical-trials-analytics` | ← clinical trialresults'sintegration |
| `scientific-academic-writing` | → paper |

#### Dependencies

```
scipy>=1.10
statsmodels>=0.14
```
---

## Harness Optimization (v0.4.0)

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
