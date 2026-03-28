---
name: scientific-survival-clinical
description: |
 analysis and 'sskill。Kaplan-Meier curveline、Cox example、Log-rank testing、
 powermin、NNT/NNH is performedfor。
 Scientific Skills Exp-03, 06 。
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

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| ClinicalTrials | `search_clinical_trials` | clinical trial search |
| ClinicalTrials | `clinical_trials_get_details` | trial detail retrieval |
| FAERS | `FAERS_count_reactions_by_drug_event` | adverse event data |
| GDC | `GDC_search_cases` | TCGA data |
| PubMed | `PubMed_search_articles` | literaturesearch |

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
