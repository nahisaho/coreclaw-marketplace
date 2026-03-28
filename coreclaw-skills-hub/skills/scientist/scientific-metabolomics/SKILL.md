---
name: scientific-metabolomics
description: |
 Metabolomics skill. LC-MS/GC-MS data processing, metabolite identification, pathway mapping, biomarker discovery, and metabolomics statistical analysis pipelines.
tu_tools:
 - key: hmdb
 name: HMDB
 description: metabolomedatabase
 - key: metabolomics_workbench
 name: Metabolomics Workbench
 description: Metabolomics Workbench REST API metabolomedataRefMet
---

# Scientific Metabolomics Analysis

LC-MS / GC-MS / NMR 's data、quality control→preprocessing→
amountanalysis→amountanalysis→pathway analysis's Standard Pipeline is provided。
's method（PLS-DA、VIP ）.

## When to Use

- data'sanalysispipelinewhen needed
- PLS-DA by/viagroup＋VIP by/viabiomarker is computedand
- metabolismpathwayanalysiswhen needed
- Pareto andmetabolitecorrelationnetworkwhen needed

---

## Quick Start

## 1. preprocessing

```python
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

def metabolomics_preprocessing(df, sample_col="Sample_ID", group_col="Group",
 min_detect_pct=0.5):
 """
 standardpreprocessingpipeline。
 1. ratemetabolite's
 2. KNN value
 3. log2 transformation
 4. Pareto 
 """
 metabolite_cols = [c for c in df.columns if c not in [sample_col, group_col]]

 # Step 1: ratefilter
 detect_rate = df[metabolite_cols].notna.mean
 keep = detect_rate[detect_rate >= min_detect_pct].index.tolist
 removed = len(metabolite_cols) - len(keep)
 print(f" Removed {removed} metabolites with <{min_detect_pct*100:.0f}% detection rate")
 metabolite_cols = keep

 # Step 2: KNN 
 imputer = KNNImputer(n_neighbors=5)
 df[metabolite_cols] = imputer.fit_transform(df[metabolite_cols])

 # Step 3: log2 transformation
 df[metabolite_cols] = np.log2(df[metabolite_cols].clip(lower=1e-10) + 1)

 # Step 4: Pareto 
 for col in metabolite_cols:
 mean = df[col].mean
 std = df[col].std
 df[col] = (df[col] - mean) / np.sqrt(std + 1e-10)

 return df, metabolite_cols
```

## 2. amountanalysis — metabolite

```python
from scipy.stats import mannwhitneyu, ttest_ind
from statsmodels.stats.multitest import multipletests

def univariate_analysis(df, metabolite_cols, group_col, group1, group2,
 test="mannwhitneyu", correction="fdr_bh"):
 """
 2 group's metabolite.

 Returns:
 DataFrame with columns: metabolite, log2FC, pvalue, padj, significant
 """
 g1 = df[df[group_col] == group1]
 g2 = df[df[group_col] == group2]

 results = []
 for met in metabolite_cols:
 v1 = g1[met].dropna
 v2 = g2[met].dropna

 if test == "mannwhitneyu":
 stat, pval = mannwhitneyu(v1, v2, alternative="two-sided")
 else:
 stat, pval = ttest_ind(v1, v2)

 log2fc = v2.mean - v1.mean
 results.append({"metabolite": met, "log2FC": log2fc, "pvalue": pval})

 results_df = pd.DataFrame(results)

 # testingcorrection
 reject, padj, _, _ = multipletests(results_df["pvalue"], method=correction)
 results_df["padj"] = padj
 results_df["significant"] = reject
 results_df["neg_log10p"] = -np.log10(results_df["pvalue"] + 1e-300)

 results_df = results_df.sort_values("pvalue")
 return results_df
```

## 3. PLS-DA + VIP 

```python
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import LabelEncoder

def plsda_analysis(X, y, n_components=2):
 """
 PLS-DA 、VIP is computed。

 VIP (Variable Importance in Projection):
 VIP_j = sqrt(p * Σ(q²_a * w²_ja) / Σ(q²_a))
 VIP > 1 's number/count biomarker

 Parameters:
 X: metabolitedata (n_samples, n_metabolites)
 y: looplabel

 Returns:
 pls_model, scores, vip_scores
 """
 le = LabelEncoder
 y_encoded = le.fit_transform(y).astype(float)

 pls = PLSRegression(n_components=n_components, scale=True)
 pls.fit(X, y_encoded)

 # （number/count）
 scores = pls.transform(X)

 # VIP 
 T = pls.x_scores_ # (n, n_comp)
 W = pls.x_weights_ # (p, n_comp)
 Q = pls.y_loadings_ # (1, n_comp)

 p = X.shape[1]
 vip = np.zeros(p)

 ss_total = np.sum(Q**2 * np.sum(T**2, axis=0))
 for j in range(p):
 ss_j = np.sum(Q**2 * np.sum(T**2, axis=0) * W[j, :]**2)
 vip[j] = np.sqrt(p * ss_j / ss_total)

 return pls, scores, vip


def plot_plsda_scores(scores, y, group_names=None, figsize=(8, 6)):
 """PLS-DA plotdrawing/plotting."""
 import matplotlib.pyplot as plt

 fig, ax = plt.subplots(figsize=figsize)
 unique = np.unique(y)
 colors = plt.cm.Set1(np.linspace(0, 0.5, len(unique)))

 for color, group in zip(colors, unique):
 mask = y == group
 label = group_names[group] if group_names else str(group)
 ax.scatter(scores[mask, 0], scores[mask, 1],
 c=[color], label=label, s=60, alpha=0.7, edgecolors="black")
 # 95% 
 from matplotlib.patches import Ellipse
 cov = np.cov(scores[mask, 0], scores[mask, 1])
 vals, vecs = np.linalg.eigh(cov)
 angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
 w, h = 2 * np.sqrt(vals * 5.991) # chi2(2, 0.95) = 5.991
 ell = Ellipse(xy=(scores[mask, 0].mean, scores[mask, 1].mean),
 width=w, height=h, angle=angle,
 fill=False, color=color, linewidth=2, linestyle="--")
 ax.add_patch(ell)

 ax.set_xlabel("PLS Component 1")
 ax.set_ylabel("PLS Component 2")
 ax.set_title("PLS-DA Score Plot", fontweight="bold")
 ax.legend
 plt.tight_layout
 plt.savefig("figures/plsda_scores.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 4. testing（PLS-DA ）

```python
def permutation_test_plsda(X, y, n_components=2, n_permutations=100):
 """
 PLS-DA 'stesting。
 Q² and R²Y 's distribution generation、's 's significant is evaluated。
 """
 from sklearn.model_selection import cross_val_predict
 le = LabelEncoder
 y_enc = le.fit_transform(y).astype(float)

 # 's
 pls_true = PLSRegression(n_components=n_components, scale=True)
 y_pred = cross_val_predict(pls_true, X, y_enc, cv=5)
 ss_res = np.sum((y_enc - y_pred.ravel)**2)
 ss_tot = np.sum((y_enc - y_enc.mean)**2)
 q2_true = 1 - ss_res / ss_tot

 # 
 q2_perm = []
 for _ in range(n_permutations):
 y_perm = np.random.permutation(y_enc)
 pls_p = PLSRegression(n_components=n_components, scale=True)
 y_pred_p = cross_val_predict(pls_p, X, y_perm, cv=5)
 ss_res_p = np.sum((y_perm - y_pred_p.ravel)**2)
 ss_tot_p = np.sum((y_perm - y_perm.mean)**2)
 q2_perm.append(1 - ss_res_p / ss_tot_p)

 p_value = np.mean(np.array(q2_perm) >= q2_true)

 return {
 "Q2_true": q2_true,
 "Q2_perm_mean": np.mean(q2_perm),
 "Q2_perm_std": np.std(q2_perm),
 "p_value": p_value,
 "significant": p_value < 0.05,
 }
```

## 5. metabolismpathwayanalysis

```python
from scipy.stats import fisher_exact

def pathway_enrichment(significant_metabolites, pathway_annotations,
 metabolite_col="Metabolite", pathway_col="Pathway",
 total_metabolites=None):
 """
 Fisher testingby/viametabolismpathwayanalysis。

 Parameters:
 significant_metabolites: list of significant metabolite names
 pathway_annotations: DataFrame with metabolite-pathway mapping
 total_metabolites: analysis's allmetabolitenumber/count
 """
 sig_set = set(significant_metabolites)
 all_annotated = set(pathway_annotations[metabolite_col])
 if total_metabolites is None:
 total_metabolites = len(all_annotated)

 pathways = pathway_annotations[pathway_col].unique
 results = []

 for pw in pathways:
 pw_members = set(
 pathway_annotations[pathway_annotations[pathway_col] == pw][metabolite_col]
 )
 k = len(sig_set & pw_members) # hit
 K = len(pw_members) # pathway size
 n = len(sig_set) # significant
 N = total_metabolites # total

 # 2x2 mintable
 table = [[k, K - k], [n - k, N - K - n + k]]
 odds_ratio, p_value = fisher_exact(table, alternative="greater")

 results.append({
 "Pathway": pw,
 "Hits": k,
 "Pathway_Size": K,
 "Significant_Total": n,
 "Odds_Ratio": odds_ratio,
 "p_value": p_value,
 })

 results_df = pd.DataFrame(results).sort_values("p_value")
 _, padj, _, _ = multipletests(results_df["p_value"], method="fdr_bh")
 results_df["padj"] = padj

 results_df.to_csv("results/pathway_enrichment.csv", index=False)
 return results_df
```

## 6. metabolitecorrelationnetwork

```python
def metabolite_correlation_network(df, metabolite_cols, method="spearman",
 threshold=0.7):
 """
 metabolite'scorrelationfromnetwork is built。

 Parameters:
 threshold: |r| ≥ threshold 's 's edgeasfor
 """
 import networkx as nx

 corr = df[metabolite_cols].corr(method=method)

 G = nx.Graph
 for i, met_i in enumerate(metabolite_cols):
 G.add_node(met_i)
 for j, met_j in enumerate(metabolite_cols):
 if i < j:
 r = corr.iloc[i, j]
 if abs(r) >= threshold:
 G.add_edge(met_i, met_j, weight=abs(r),
 sign="positive" if r > 0 else "negative")

 return G, corr
```

## References

### Output Files

| File | Format |
|---|---|
| `results/univariate_results.csv` | CSV |
| `results/vip_scores.csv` | CSV |
| `results/pathway_enrichment.csv` | CSV |
| `figures/plsda_scores.png` | PNG |
| `figures/vip_barplot.png` | PNG |
| `figures/metabolite_network.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| HMDB | `HMDB_search` | metabolite search |
| HMDB | `HMDB_get_metabolite` | metabolite detail retrieval |
| HMDB | `HMDB_get_diseases` | metabolite-disease |
| KEGG | `kegg_get_pathway_info` | metabolic pathway information |
| MetaCyc | `MetaCyc_search_pathways` | metabolic pathway search |
| MetabolomicsWB | `MetabolomicsWorkbench_search_compound_by_name` | metabolitedatabasesearch |

#### Reference Experiments

- **Exp-07**: PLS-DA + VIP、Pareto 、pathway、correlationnetwork

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
