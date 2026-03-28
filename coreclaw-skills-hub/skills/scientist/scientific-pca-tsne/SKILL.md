---
name: scientific-pca-tsne
description: |
 Dimensionality reduction skill. PCA, t-SNE, UMAP, MDS implementations with visualization, parameter tuning, and biological interpretation of reduced dimensions.
tu_tools:
 - key: biotools
 name: bio.tools
 description: dimensionality reductionvisualizationtoolsearch
---

# Scientific Dimensionality Reduction & Space Mapping

data 2D/3D structure visualizationskill。
PCA（lineshape）、t-SNE（lineshape、structuresave）、UMAP（lineshape、+）'s 
3 method min。

## When to Use

- data's structure 2D visualizationwhen needed
- compound's structurewhen needed
- method's measurementdataintegrationwhen needed
- min'scontribution rateand amountwhen needed

## Quick Start

## methodselection

| method | | recommendedsurface |
|---|---|---|
| PCA | lineshapecontribution rate | 's 、PC amount's |
| t-SNE | lineshapestructuresave | min'svisualization |
| UMAP | lineshape+ | large-scaledata、gradient'svisualization |

## Standard Pipeline

### 1. PCA + plot

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def pca_analysis(df, feature_cols, n_components=None, figsize=(14, 5)):
 """PCA 、plot and PC1-PC2 scatter plot drawing/plotting."""
 scaler = StandardScaler
 X_sc = scaler.fit_transform(df[feature_cols])

 if n_components is None:
 n_components = min(len(feature_cols), 10)

 pca = PCA(n_components=n_components)
 pcs = pca.fit_transform(X_sc)

 # plot
 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

 cumvar = np.cumsum(pca.explained_variance_ratio_) * 100
 ax1.bar(range(1, n_components + 1), pca.explained_variance_ratio_ * 100,
 color="steelblue", edgecolor="black")
 ax1.plot(range(1, n_components + 1), cumvar, "ro-", linewidth=2)
 ax1.set_xlabel("Principal Component")
 ax1.set_ylabel("Explained Variance (%)")
 ax1.set_title("Scree Plot", fontweight="bold")
 ax1.axhline(y=80, color="gray", linestyle="--", alpha=0.5)

 # PC1 vs PC2
 ax2.scatter(pcs[:, 0], pcs[:, 1], alpha=0.6, s=30, edgecolors="k", linewidth=0.3)
 ax2.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
 ax2.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
 ax2.set_title("PCA Projection", fontweight="bold")

 plt.tight_layout
 plt.savefig("figures/pca_screeplot.png", dpi=300, bbox_inches="tight")
 plt.close

 return pca, pcs


def pca_loading_plot(pca, feature_names, figsize=(10, 8)):
 """PC1-PC2 's amount（loading）plotdrawing/plotting."""
 loadings = pca.components_[:2].T

 fig, ax = plt.subplots(figsize=figsize)
 for i, name in enumerate(feature_names):
 ax.arrow(0, 0, loadings[i, 0], loadings[i, 1],
 head_width=0.02, head_length=0.01, fc="red", ec="red", alpha=0.7)
 ax.text(loadings[i, 0] * 1.1, loadings[i, 1] * 1.1, name,
 fontsize=8, ha="center")
 ax.set_xlabel(f"PC1 Loading")
 ax.set_ylabel(f"PC2 Loading")
 ax.set_title("PCA Loading Plot (Biplot)", fontweight="bold")
 ax.axhline(0, color="gray", linewidth=0.5)
 ax.axvline(0, color="gray", linewidth=0.5)
 plt.tight_layout
 plt.savefig("figures/pca_loadings.png", dpi=300, bbox_inches="tight")
 plt.close
```

### 2. t-SNE visualization

```python
from sklearn.manifold import TSNE

def tsne_visualization(X_scaled, labels, label_name="Group",
 perplexity=30, random_state=42, figsize=(8, 8)):
 """t-SNE 2D drawing/plotting."""
 tsne = TSNE(n_components=2, perplexity=perplexity,
 random_state=random_state, n_iter=1000)
 coords = tsne.fit_transform(X_scaled)

 fig, ax = plt.subplots(figsize=figsize)
 for label in sorted(set(labels)):
 mask = labels == label
 ax.scatter(coords[mask, 0], coords[mask, 1],
 label=label, alpha=0.7, s=40, edgecolors="k", linewidth=0.3)
 ax.set_xlabel("t-SNE 1")
 ax.set_ylabel("t-SNE 2")
 ax.set_title("t-SNE Projection", fontweight="bold")
 ax.legend(title=label_name, bbox_to_anchor=(1.05, 1))
 plt.tight_layout
 plt.savefig("figures/tsne_projection.png", dpi=300, bbox_inches="tight")
 plt.close
 return coords
```

### 3. PCA + t-SNE （Exp-11, 13 ）

```python
def pca_tsne_panel(df, feature_cols, hue_col, figsize=(16, 7)):
 """PCA and t-SNE drawing/plotting."""
 scaler = StandardScaler
 X_sc = scaler.fit_transform(df[feature_cols])

 pca = PCA(n_components=2)
 pcs = pca.fit_transform(X_sc)

 tsne = TSNE(n_components=2, perplexity=30, random_state=42)
 tsne_coords = tsne.fit_transform(X_sc)

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
 labels = df[hue_col].values

 for label in sorted(set(labels)):
 mask = labels == label
 ax1.scatter(pcs[mask, 0], pcs[mask, 1], label=label,
 alpha=0.7, s=40, edgecolors="k", linewidth=0.3)
 ax2.scatter(tsne_coords[mask, 0], tsne_coords[mask, 1], label=label,
 alpha=0.7, s=40, edgecolors="k", linewidth=0.3)

 ev = pca.explained_variance_ratio_ * 100
 ax1.set_xlabel(f"PC1 ({ev[0]:.1f}%)")
 ax1.set_ylabel(f"PC2 ({ev[1]:.1f}%)")
 ax1.set_title("(A) PCA", fontweight="bold")
 ax1.legend(title=hue_col)

 ax2.set_xlabel("t-SNE 1")
 ax2.set_ylabel("t-SNE 2")
 ax2.set_title("(B) t-SNE", fontweight="bold")
 ax2.legend(title=hue_col)

 plt.tight_layout
 plt.savefig("figures/pca_tsne_panel.png", dpi=300, bbox_inches="tight")
 plt.close

 # coordinates save
 coords_df = pd.DataFrame({
 "PC1": pcs[:, 0], "PC2": pcs[:, 1],
 "tSNE1": tsne_coords[:, 0], "tSNE2": tsne_coords[:, 1],
 hue_col: labels,
 })
 coords_df.to_csv("results/pca_tsne_coordinates.csv", index=False)
 return pca, tsne_coords
```

### 4. clustering + Silhouette k

```python
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics import silhouette_score

def hierarchical_clustering(X_scaled, method="ward", max_k=10, figsize=(12, 5)):
 """clustering and number/count's。"""
 Z = linkage(X_scaled, method=method)

 # Silhouette k search/exploration
 sil_scores = []
 for k in range(2, max_k + 1):
 labels = fcluster(Z, k, criterion="maxclust")
 sil = silhouette_score(X_scaled, labels)
 sil_scores.append({"k": k, "silhouette": sil})

 sil_df = pd.DataFrame(sil_scores)
 best_k = sil_df.loc[sil_df["silhouette"].idxmax, "k"]

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

 # log
 dendrogram(Z, ax=ax1, truncate_mode="lastp", p=30, leaf_rotation=90)
 ax1.set_title("Dendrogram", fontweight="bold")
 ax1.set_ylabel("Distance")

 # Silhouette 
 ax2.plot(sil_df["k"], sil_df["silhouette"], "bo-", linewidth=2)
 ax2.axvline(best_k, color="red", linestyle="--", label=f"Best k={int(best_k)}")
 ax2.set_xlabel("Number of Clusters (k)")
 ax2.set_ylabel("Silhouette Score")
 ax2.set_title("Optimal k (Silhouette)", fontweight="bold")
 ax2.legend

 plt.tight_layout
 plt.savefig("figures/clustering_analysis.png", dpi=300, bbox_inches="tight")
 plt.close
 return Z, int(best_k)
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | dimensionality reductionvisualizationtoolsearch |

## References

### Output Files

| File | Format |
|---|---|
| `results/pca_tsne_coordinates.csv` | CSV |
| `figures/pca_screeplot.png` | PNG |
| `figures/pca_loadings.png` | PNG |
| `figures/tsne_projection.png` | PNG |
| `figures/pca_tsne_panel.png` | PNG |
| `figures/clustering_analysis.png` | PNG |

#### Reference Experiments

- **Exp-02**: PCA/t-SNE（EGFR inhibition）
- **Exp-03**: PCA / UMAP / t-SNE 3 methodcomparison
- **Exp-07**: PLS-DA + PCA 
- **Exp-11**: spectrum's PCA/t-SNE + clustering
- **Exp-13**: method PCA/t-SNE（XRD+AFM++）

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
