---
name: scientific-statistical-testing
description: |
 Statistical testing skill. Frequentist hypothesis testing (t-test, ANOVA, chi-square, nonparametric tests), multiple testing correction, effect size calculation, and power analysis.
tu_tools:
 - key: biotools
 name: bio.tools
 description: testingtoolregistry
---

# Scientific Statistical Testing & Enrichment Analysis

hypothesistesting、multiple comparisoncorrection、analysisforpipelineskill。
frequencytesting andBayesian inference's 's is provided。

## When to Use

- 2 group's significanttestingwhen needed（t testing、Mann-Whitney U）
- group'scomparison（ANOVA、Kruskal-Wallis）
- multiple comparison's correction（Bonferroni、Benjamini-Hochberg）
- pathwayanalysis（Fisher testing）
- Bayesian inference（Beta-Binomial ）

## Quick Start

## Standard Pipeline

### 1. 2 grouptesting

```python
from scipy import stats
import numpy as np
import pandas as pd

def two_group_test(group1, group2, test="auto", alternative="two-sided"):
 """
 2 group'stesting is executed。
 test='auto' case、testing t testing or Mann-Whitney U selection。
 """
 # testing（Shapiro-Wilk）
 if test == "auto":
 _, p1 = stats.shapiro(group1) if len(group1) <= 5000 else (0, 0.05)
 _, p2 = stats.shapiro(group2) if len(group2) <= 5000 else (0, 0.05)
 test = "ttest" if (p1 > 0.05 and p2 > 0.05) else "mannwhitney"

 if test == "ttest":
 stat, pval = stats.ttest_ind(group1, group2, alternative=alternative)
 test_name = "Welch's t-test"
 elif test == "mannwhitney":
 stat, pval = stats.mannwhitneyu(group1, group2, alternative=alternative)
 test_name = "Mann-Whitney U"
 else:
 raise ValueError(f"Unknown test: {test}")

 # effect size（Cohen's d）
 pooled_std = np.sqrt((np.var(group1, ddof=1) + np.var(group2, ddof=1)) / 2)
 cohens_d = (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0

 return {
 "test": test_name,
 "statistic": stat,
 "p_value": pval,
 "cohens_d": cohens_d,
 "effect_size": ("large" if abs(cohens_d) > 0.8 else
 "medium" if abs(cohens_d) > 0.5 else "small"),
 }
```

### 2. multiple comparisoncorrection

```python
from statsmodels.stats.multitest import multipletests

def multiple_testing_correction(p_values, method="fdr_bh", alpha=0.05):
 """
 multiple comparisoncorrection is applied。
 method: 'bonferroni', 'fdr_bh' (Benjamini-Hochberg), 'holm'
 """
 reject, p_corrected, _, _ = multipletests(p_values, alpha=alpha, method=method)
 return reject, p_corrected
```

### 3. ANOVA / Kruskal-Wallis

```python
def multi_group_test(groups, test="auto"):
 """
 group'scomparison is executed。
 groups: [array1, array2,...] 's
 """
 # 
 normal = all(stats.shapiro(g)[1] > 0.05 for g in groups if len(g) <= 5000)

 if test == "auto":
 test = "anova" if normal else "kruskal"

 if test == "anova":
 stat, pval = stats.f_oneway(*groups)
 test_name = "One-way ANOVA"
 elif test == "kruskal":
 stat, pval = stats.kruskal(*groups)
 test_name = "Kruskal-Wallis"

 return {"test": test_name, "statistic": stat, "p_value": pval}
```

### 4. Fisher testingpathway（Exp-04, 07）

```python
def pathway_enrichment(deg_list, pathway_dict, background_size,
 method="fisher", correction="fdr_bh"):
 """
 Fisher testingby/viapathwayanalysis。
 deg_list: expressiongene list
 pathway_dict: {pathway_name: [gene1, gene2,...]} 's
 background_size: genenumber/count
 """
 results = []
 deg_set = set(deg_list)

 for pathway, genes in pathway_dict.items:
 gene_set = set(genes)
 overlap = deg_set & gene_set

 # 2×2 mintable
 a = len(overlap) # DEG ∩ Pathway
 b = len(deg_set) - a # DEG ∩ ~Pathway
 c = len(gene_set) - a # ~DEG ∩ Pathway
 d = background_size - a - b - c # ~DEG ∩ ~Pathway

 _, pval = stats.fisher_exact([[a, b], [c, d]], alternative="greater")
 fold_enrichment = (a / len(deg_set)) / (len(gene_set) / background_size) \
 if len(gene_set) > 0 and len(deg_set) > 0 else 0

 results.append({
 "Pathway": pathway,
 "Overlap": a,
 "Pathway_Size": len(gene_set),
 "Fold_Enrichment": fold_enrichment,
 "p_value": pval,
 "Genes": ", ".join(sorted(overlap)),
 })

 results_df = pd.DataFrame(results)

 # testingcorrection
 if len(results_df) > 0:
 reject, p_adj = multiple_testing_correction(
 results_df["p_value"].values, method=correction
 )
 results_df["p_adjusted"] = p_adj
 results_df["Significant"] = reject

 results_df = results_df.sort_values("p_value")
 results_df.to_csv("results/pathway_enrichment.csv", index=False)
 return results_df
```

### 5. Bayesian inference（Beta-Binomial, Exp-06 ）

```python
def bayesian_beta_binomial(successes, trials, prior_alpha=1, prior_beta=1):
 """
 Beta-Binomial by/viaBayesian inference。
 prior distribution: Beta(alpha, beta), prior distribution。
 """
 post_alpha = prior_alpha + successes
 post_beta = prior_beta + (trials - successes)

 from scipy.stats import beta
 posterior = beta(post_alpha, post_beta)

 return {
 "posterior_mean": posterior.mean,
 "posterior_std": posterior.std,
 "95%_CI": (posterior.ppf(0.025), posterior.ppf(0.975)),
 "MAP": (post_alpha - 1) / (post_alpha + post_beta - 2)
 if post_alpha > 1 and post_beta > 1 else posterior.mean,
 "posterior_alpha": post_alpha,
 "posterior_beta": post_beta,
 }
```

### 6. analysis（Kaplan-Meier + Cox PH, Exp-03/06）

```python
def survival_analysis(df, time_col, event_col, group_col):
 """
 Perform Kaplan-Meier survival curves and Log-rank tests.
 lifelines librarynecessary。
 """
 from lifelines import KaplanMeierFitter, CoxPHFitter
 from lifelines.statistics import logrank_test
 import matplotlib.pyplot as plt

 groups = df[group_col].unique
 fig, ax = plt.subplots(figsize=(8, 6))
 kmf = KaplanMeierFitter

 for group in sorted(groups):
 mask = df[group_col] == group
 kmf.fit(df.loc[mask, time_col], event_observed=df.loc[mask, event_col],
 label=str(group))
 kmf.plot_survival_function(ax=ax)

 # Log-rank testing（2 groupcase）
 if len(groups) == 2:
 g1 = df[df[group_col] == groups[0]]
 g2 = df[df[group_col] == groups[1]]
 lr = logrank_test(g1[time_col], g2[time_col],
 event_observed_A=g1[event_col],
 event_observed_B=g2[event_col])
 ax.text(0.7, 0.9, f"Log-rank p={lr.p_value:.4f}",
 transform=ax.transAxes, fontsize=10)

 ax.set_xlabel("Time")
 ax.set_ylabel("Survival Probability")
 ax.set_title("Kaplan-Meier Survival Curves", fontweight="bold")
 plt.tight_layout
 plt.savefig("figures/kaplan_meier.png", dpi=300, bbox_inches="tight")
 plt.close

 return lr.p_value if len(groups) == 2 else None
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | testingtoolregistry |

## References

### Output Files

| File | Format |
|---|---|
| `results/pathway_enrichment.csv` | CSV |
| `results/statistical_tests.csv` | CSV |
| `figures/kaplan_meier.png` | PNG |
| `figures/enrichment_dotplot.png` | PNG |

#### Reference Experiments

- **Exp-03**: Mann-Whitney U + Volcano Plot + analysis
- **Exp-04**: Fisher pathway + Louvain 
- **Exp-06**: frequency + Bayesian inference + powermin
- **Exp-07**: Welch t testing + BH correction + PLS-DA VIP

---

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
