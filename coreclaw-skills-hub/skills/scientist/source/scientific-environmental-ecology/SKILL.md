---
name: scientific-environmental-ecology
description: |
 environmentecologyanalysisskill。typedistribution（SDM / MaxEnt）
 （α/β/γ ）groupstructureanalysis（NMDS/CCA/RDA）
 ecologyallevaluationOBIS/GBIF dataintegrationpipeline。
 ToolUniverse integration: gbif。
tu_tools:
 - key: gbif
 name: GBIF
 description: information
---

# Scientific Environmental Ecology

environmentecologyanalysispipeline is provided。
typedistribution、evaluation、groupstructureanalysis、
all、/'s systemdataintegrationhandles。

## When to Use

- typedistribution（SDM）construction is estimatedand
- group'scomparisonwhen needed
- groupstructure's environment to 'sanalysiswhen needed（CCA / RDA）
- GBIF / OBIS fromdata retrievalanalysis is performedand
- all's evaluation is performedand

---

## Quick Start

## 1. typedistribution（SDM）

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score

def species_distribution_model(occurrences, background, env_layers,
 method="maxent", n_folds=5):
 """
 typedistribution（SDM）pipeline。

 method:
 - "maxent": MaxEnt — （data's）
 - "rf": Random Forest — /data
 - "gbm": Gradient Boosting — ensemble
 - "ensemble": multiple'smean

 MaxEnt :
 P(x) environmentnumber/count x 's number/countas。
 information maximizedistributionselection:
 H(P) = -Σ P(x) log P(x) → maximize
 : E_P[fⱼ] = E_data[fⱼ] (features's value)

 input:
 - occurrences: type'scoordinates (lon, lat)
 - background: point (lon, lat)
 - env_layers: environmentnumber/count（Bio1-Bio19 ）
 """
 # environmentnumber/count/pointextraction
 X_pres = extract_env_values(occurrences, env_layers)
 X_bg = extract_env_values(background, env_layers)
 X = np.vstack([X_pres, X_bg])
 y = np.concatenate([np.ones(len(X_pres)), np.zeros(len(X_bg))])

 if method == "maxent":
 from elapid import MaxentModel
 model = MaxentModel
 model.fit(X_pres, X_bg)
 pred = model.predict(env_layers)

 elif method == "rf":
 model = RandomForestClassifier(n_estimators=500, random_state=42)
 model.fit(X, y)
 auc_scores = cross_val_score(model, X, y, cv=n_folds, scoring="roc_auc")
 print(f" RF AUC: {np.mean(auc_scores):.3f} ± {np.std(auc_scores):.3f}")
 pred = model.predict_proba(env_layers.reshape(-1, env_layers.shape[-1]))[:, 1]

 elif method == "gbm":
 model = GradientBoostingClassifier(n_estimators=300, max_depth=5,
 random_state=42)
 model.fit(X, y)
 auc_scores = cross_val_score(model, X, y, cv=n_folds, scoring="roc_auc")
 print(f" GBM AUC: {np.mean(auc_scores):.3f} ± {np.std(auc_scores):.3f}")

 return model, pred


def extract_env_values(coords, env_layers):
 """coordinatesfromenvironmentnumber/countvalue is extracted。"""
 import rasterio
 values = []
 for lon, lat in coords:
 row, col = env_layers.index(lon, lat)
 values.append(env_layers.read[:, row, col])
 return np.array(values)
```

## 2. 

```python
from scipy.stats import entropy

def biodiversity_indices(community_matrix, metadata=None):
 """
 group's 。

 α （）:
 - Species richness: S = typenumber/count
 - Shannon: H' = -Σ pᵢ ln(pᵢ)
 - Simpson: D = 1 - Σ pᵢ²
 - Pielou's Evenness: J = H' / ln(S)
 - Chao1: S_est = S_obs + f₁²/(2·f₂)

 β （）:
 - Bray-Curtis dissimilarity
 - Jaccard distance
 - Sørensen index
 - Whittaker's β: γ/ᾱ - 1

 γ （all）:
 - all's typenumber/count
 """
 results = []
 for idx, row in community_matrix.iterrows:
 counts = row[row > 0].values
 freqs = counts / counts.sum
 S = len(counts)

 H = entropy(freqs)
 D_simpson = 1 - np.sum(freqs ** 2)
 J = H / np.log(S) if S > 1 else 0

 f1 = np.sum(counts == 1)
 f2 = max(np.sum(counts == 2), 1)
 chao1 = S + (f1 ** 2) / (2 * f2)

 results.append({
 "site": idx,
 "richness": S,
 "shannon": round(H, 4),
 "simpson": round(D_simpson, 4),
 "evenness": round(J, 4),
 "chao1": round(chao1, 1),
 "total_abundance": int(counts.sum),
 })

 alpha_df = pd.DataFrame(results).set_index("site")

 # γ 
 gamma = (community_matrix > 0).any(axis=0).sum
 mean_alpha = alpha_df["richness"].mean
 beta_whittaker = gamma / mean_alpha - 1

 summary = {
 "gamma_diversity": gamma,
 "mean_alpha": round(mean_alpha, 2),
 "beta_whittaker": round(beta_whittaker, 3),
 }

 print(f" Biodiversity: γ={gamma}, ᾱ={mean_alpha:.1f}, β_w={beta_whittaker:.3f}")
 return alpha_df, summary
```

## 3. groupstructureanalysis（NMDS / CCA / RDA）

```python
def community_ordination(community_matrix, env_df=None, method="nmds",
 n_dims=2, distance="bray"):
 """
 groupstructure's（Ordination）。

 method:
 - "nmds": Non-metric Multidimensional Scaling — 
 - "cca": Canonical Correspondence Analysis — （type）
 - "rda": Redundancy Analysis — （lineshape）
 - "dca": Detrended Correspondence Analysis — gradientevaluation

 NMDS stress criteria:
 - < 0.05: Excellent
 - < 0.10: Good
 - < 0.20: Acceptable
 - > 0.20: Poor（number/count）
 """
 from skbio.stats.ordination import pcoa
 from skbio.diversity import beta_diversity
 from scipy.spatial.distance import squareform

 if method == "nmds":
 from sklearn.manifold import MDS
 dm = beta_diversity(distance, community_matrix.values,
 community_matrix.index)
 mds = MDS(n_components=n_dims, dissimilarity="precomputed",
 metric=False, random_state=42, max_iter=500)
 coords = mds.fit_transform(squareform(dm.data))
 stress = mds.stress_
 print(f" NMDS: stress={stress:.4f} ({n_dims}D)")
 return coords, stress

 elif method == "pcoa":
 dm = beta_diversity(distance, community_matrix.values,
 community_matrix.index)
 result = pcoa(dm)
 return result.samples.values[:, :n_dims], result.proportion_explained[:n_dims]
```

## 4. type's allevaluation

```python
def conservation_priority(species_data, criteria_weights=None):
 """
 all's criteriaevaluation。

 IUCN criteria:
 - CR: Critically Endangered
 - EN: Endangered
 - VU: Vulnerable
 - NT: Near Threatened

 evaluationcriteria:
 1. （IUCN ）
 2. phylogeny（Evolutionary Distinctiveness）
 3. surfacerate
 4. Endemic （type）
 5. system
 """
 if criteria_weights is None:
 criteria_weights = {
 "iucn_score": 0.30,
 "evolutionary_distinctiveness": 0.20,
 "habitat_loss_rate": 0.20,
 "endemism": 0.15,
 "ecosystem_service": 0.15,
 }

 iucn_mapping = {"CR": 5, "EN": 4, "VU": 3, "NT": 2, "LC": 1, "DD": 0}
 species_data["iucn_score"] = species_data["iucn_category"].map(iucn_mapping)

 # normalization
 for col in criteria_weights:
 if col in species_data.columns:
 min_v = species_data[col].min
 max_v = species_data[col].max
 if max_v > min_v:
 species_data[f"{col}_norm"] = (species_data[col] - min_v) / (max_v - min_v)

 # Composite score
 species_data["priority_score"] = sum(
 w * species_data.get(f"{col}_norm", 0) for col, w in criteria_weights.items
 )
 species_data = species_data.sort_values("priority_score", ascending=False)

 print(f" Conservation: {len(species_data)} species ranked")
 return species_data
```

## References

### Output Files

| File | Format |
|---|---|
| `results/sdm_predictions.tif` | GeoTIFF |
| `results/biodiversity_indices.csv` | CSV |
| `results/ordination_scores.csv` | CSV |
| `results/conservation_priority.csv` | CSV |
| `figures/sdm_map.png` | PNG |
| `figures/nmds_plot.png` | PNG |
| `figures/diversity_comparison.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| OBIS | `OBIS_search_taxa` | classificationsearch |
| OBIS | `OBIS_search_occurrences` | data |
| GBIF | `GBIF_search_species` | species namesearch |
| GBIF | `GBIF_search_occurrences` | search |
| Paleobiology | `Paleobiology_get_fossils` | data |
| OLS | `ols_search_terms` | ecologysearch |
| PubMed | `PubMed_search_articles` | ecologyliteraturesearch |

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-statistical-testing](../scientific-statistical-testing/SKILL.md) | significanttesting |
| [scientific-pca-tsne](../scientific-pca-tsne/SKILL.md) | dimensionality reduction |
| [scientific-ml-classification](../scientific-ml-classification/SKILL.md) | SDM （RF/GBM） |
| [scientific-image-analysis](../scientific-image-analysis/SKILL.md) | analysis |
| [scientific-time-series](../scientific-time-series/SKILL.md) | systemtime series |

#### Dependencies

- scikit-bio, rasterio, geopandas, elapid, shapely, pygbif
