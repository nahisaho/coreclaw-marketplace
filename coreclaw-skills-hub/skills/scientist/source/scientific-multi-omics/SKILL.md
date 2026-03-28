---
name: scientific-multi-omics
description: |
 multi-omics integrationanalysisskill。genometranscriptomeproteomemetabolome
 data's integrationmethod（MOFA/SNF/DIABLO）、omicscorrelationanalysis、CCA/PLS integration、
 pathwayintegration、networkintegration's templateproviding。
---

# Scientific Multi-Omics Integration

multiple'somicslayer（、、proteomics、
）'s data integration analysisforskill。eachomics's unitsanalysis
'sskill（bioinformatics, metabolomics）itemsitems、papersskill
**integration**.

## When to Use

- frommultipleomicsdataintegrationwhen needed
- omics's correlationstructurewhen needed
- multi-omicsbiomarkerwhen needed
- pathway'sintegrated analysiswhen needed

---

## Quick Start

## 1. dataconsistency check

```python
import numpy as np
import pandas as pd

def check_multiomics_alignment(omics_dict, sample_col="Sample_ID"):
 """
 multi-omicsdata's consistency check。

 Parameters:
 omics_dict: {"transcriptomics": df, "proteomics": df, "metabolomics": df}
 """
 all_samples = {}
 for name, df in omics_dict.items:
 all_samples[name] = set(df[sample_col])

 # 
 common = set.intersection(*all_samples.values)
 report = {
 "n_omics_layers": len(omics_dict),
 "layers": list(omics_dict.keys),
 "samples_per_layer": {k: len(v) for k, v in all_samples.items},
 "common_samples": len(common),
 "features_per_layer": {k: df.shape[1] - 1 for k, df in omics_dict.items},
 }

 # filter
 aligned = {}
 for name, df in omics_dict.items:
 aligned[name] = df[df[sample_col].isin(common)].sort_values(sample_col).reset_index(drop=True)

 print(f"=== Multi-Omics Alignment ===")
 print(f"Common samples: {len(common)} / {max(report['samples_per_layer'].values)}")
 for k, v in report["features_per_layer"].items:
 print(f" {k}: {v} features")

 return aligned, report
```

## 2. omicscorrelationanalysis

```python
from scipy.stats import spearmanr

def cross_omics_correlation(omics1_df, omics2_df, name1="Omics1", name2="Omics2",
 top_n=50, method="spearman"):
 """
 2 items's omicslayer's featurescorrelationcalculation.

 Parameters:
 omics1_df: DataFrame (samples × features), no sample_col
 omics2_df: DataFrame (samples × features), no sample_col
 top_n: top's correlation is returnednumber/count
 """
 features1 = omics1_df.columns.tolist
 features2 = omics2_df.columns.tolist

 correlations = []
 for f1 in features1:
 for f2 in features2:
 if method == "spearman":
 r, p = spearmanr(omics1_df[f1], omics2_df[f2])
 else:
 from scipy.stats import pearsonr
 r, p = pearsonr(omics1_df[f1], omics2_df[f2])
 correlations.append({
 f"{name1}_feature": f1,
 f"{name2}_feature": f2,
 "correlation": r,
 "p_value": p,
 "abs_correlation": abs(r),
 })

 corr_df = pd.DataFrame(correlations).sort_values("abs_correlation", ascending=False)

 return corr_df.head(top_n)
```

## 3. CCA (Canonical Correlation Analysis)

```python
from sklearn.cross_decomposition import CCA

def canonical_correlation_analysis(X1, X2, n_components=2):
 """
 correlationmin: 2 items's omicsdata's correlationdirection items。

 Returns:
 cca_model, scores_X1, scores_X2, canonical_correlations
 """
 cca = CCA(n_components=n_components)
 scores_X1, scores_X2 = cca.fit_transform(X1, X2)

 # correlation coefficient
 canonical_corrs = []
 for i in range(n_components):
 r = np.corrcoef(scores_X1[:, i], scores_X2[:, i])[0, 1]
 canonical_corrs.append(r)

 return cca, scores_X1, scores_X2, canonical_corrs


def plot_cca_scores(scores_X1, scores_X2, labels, name1="Omics1",
 name2="Omics2", figsize=(12, 5)):
 """CCA plotdrawing/plotting."""
 import matplotlib.pyplot as plt

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

 unique_labels = np.unique(labels)
 colors = plt.cm.Set1(np.linspace(0, 0.5, len(unique_labels)))

 for color, label in zip(colors, unique_labels):
 mask = labels == label
 ax1.scatter(scores_X1[mask, 0], scores_X1[mask, 1],
 c=[color], label=label, alpha=0.7, edgecolors="black")
 ax2.scatter(scores_X2[mask, 0], scores_X2[mask, 1],
 c=[color], label=label, alpha=0.7, edgecolors="black")

 ax1.set_title(f"CCA — {name1}", fontweight="bold")
 ax1.set_xlabel("CC1"); ax1.set_ylabel("CC2")
 ax2.set_title(f"CCA — {name2}", fontweight="bold")
 ax2.set_xlabel("CC1"); ax2.set_ylabel("CC2")
 ax1.legend; ax2.legend
 plt.tight_layout
 plt.savefig("figures/cca_scores.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 4. SNF (Similarity Network Fusion)

```python
def similarity_network_fusion(omics_list, k_neighbors=20, n_iterations=20):
 """
 Similarity Network Fusion — multipleomics's degreenetwork.

 Wang et al., Nature Methods 2014

 Parameters:
 omics_list: list of np.arrays [(n_samples, p1), (n_samples, p2),...]
 k_neighbors: KNN 's K
 n_iterations: timesnumber/count

 Returns:
 fused_similarity: (n_samples, n_samples) degree
 """
 from sklearn.metrics import pairwise_distances

 n = omics_list[0].shape[0]
 n_views = len(omics_list)

 # each's degree
 similarities = []
 for X in omics_list:
 D = pairwise_distances(X, metric="euclidean")
 mu = np.mean(np.sort(D, axis=1)[:, 1:k_neighbors+1], axis=1)
 S = np.exp(-D**2 / (mu[:, None] * mu[None, :] + 1e-10))
 np.fill_diagonal(S, 0)
 # normalization
 S = S / (S.sum(axis=1, keepdims=True) + 1e-10)
 similarities.append(S)

 # KNN 
 knn_masks = []
 for X in omics_list:
 D = pairwise_distances(X, metric="euclidean")
 mask = np.zeros_like(D, dtype=bool)
 for i in range(n):
 nn = np.argsort(D[i])[:k_neighbors+1]
 mask[i, nn] = True
 knn_masks.append(mask)

 # 
 P = [s.copy for s in similarities]
 for _ in range(n_iterations):
 P_new = []
 for v in range(n_views):
 # 's 'smean
 other_avg = np.mean([P[j] for j in range(n_views) if j != v], axis=0)
 # structure's
 S_local = similarities[v] * knn_masks[v]
 S_local = S_local / (S_local.sum(axis=1, keepdims=True) + 1e-10)
 P_updated = S_local @ other_avg @ S_local.T
 P_updated = P_updated / (P_updated.sum(axis=1, keepdims=True) + 1e-10)
 P_new.append(P_updated)
 P = P_new

 fused = np.mean(P, axis=0)
 fused = (fused + fused.T) / 2

 return fused
```

## 5. pathwayintegration

```python
def pathway_level_integration(omics_dict, pathway_mapping, pathway_col="Pathway",
 feature_col="Feature"):
 """
 pathwayomicsdataintegration.
 eachpathway's activity PCA min 。

 Parameters:
 omics_dict: {"transcriptomics": df, "proteomics": df}
 pathway_mapping: DataFrame (Feature, Pathway, Omics_Layer)
 """
 from sklearn.decomposition import PCA

 pathway_scores = {}
 pathways = pathway_mapping[pathway_col].unique

 for pw in pathways:
 pw_features = pathway_mapping[pathway_mapping[pathway_col] == pw]
 combined_data = []

 for omics_name, df in omics_dict.items:
 features_in_omics = pw_features[pw_features["Omics_Layer"] == omics_name][feature_col]
 available = [f for f in features_in_omics if f in df.columns]
 if available:
 combined_data.append(df[available].values)

 if combined_data:
 X = np.hstack(combined_data)
 if X.shape[1] >= 2:
 pca = PCA(n_components=1)
 score = pca.fit_transform(X).ravel
 pathway_scores[pw] = {
 "score": score,
 "explained_variance": pca.explained_variance_ratio_[0],
 "n_features": X.shape[1],
 }

 return pathway_scores
```

## 6. multi-omicsclustering

```python
from sklearn.cluster import SpectralClustering

def multiomics_clustering(fused_similarity, n_clusters, labels_true=None):
 """degree-basedclustering。"""
 from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

 clustering = SpectralClustering(n_clusters=n_clusters, affinity="precomputed",
 random_state=42)
 cluster_labels = clustering.fit_predict(fused_similarity)

 metrics = {"n_clusters": n_clusters}
 if labels_true is not None:
 metrics["ARI"] = adjusted_rand_score(labels_true, cluster_labels)
 metrics["NMI"] = normalized_mutual_info_score(labels_true, cluster_labels)

 return cluster_labels, metrics
```

## References

### Output Files

| File | Format |
|---|---|
| `results/cross_omics_correlation.csv` | CSV |
| `results/canonical_correlations.csv` | CSV |
| `results/pathway_activity_scores.csv` | CSV |
| `results/multiomics_clusters.csv` | CSV |
| `figures/cca_scores.png` | PNG |
| `figures/snf_heatmap.png` | PNG |
| `figures/multiomics_umap.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| HPA | `HPA_get_rna_expression_by_source` | tissue RNA expression |
| GEO | `geo_search_datasets` | omicsDataset Search |
| CELLxGENE | `CELLxGENE_get_expression_data` | singlecellexpressiondata |
| Reactome | `Reactome_map_uniprot_to_pathways` | pathway mapping |
| KEGG | `kegg_get_pathway_info` | pathway information |
| UniProt | `UniProt_search` | protein search |

#### Dependencies

```
scikit-learn>=1.3
scipy>=1.10
```
