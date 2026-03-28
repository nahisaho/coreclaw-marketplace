---
name: scientific-image-analysis
description: |
 Image analysis skill. Scientific image processing, segmentation, morphological analysis, particle detection, colocalization analysis, and quantitative microscopy pipelines.
tu_tools:
 - key: biotools
 name: bio.tools
 description: analysisTool Registry Search
---

# Scientific Image Analysis

（SEM / TEM / ） and medical imagingdata's amountanalysispipeline。
preprocessing→→shape→analysis'sstandardworkflow is provided。

## When to Use

- 's structure'swhen needed
- distributionshapeparameters（surface、degreeetc.）amountwhen needed
- features（GLCM / LBP） is extractedand
- 's synthesisintensityamountwhen needed

---

## Quick Start

## 1. loadpreprocessing

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, filters, morphology, measure, exposure, color
from skimage.segmentation import watershed, felzenszwalb
from scipy import ndimage

def load_and_preprocess(filepath, target_size=None):
 """
 's load andpreprocessing。

 Steps:
 1. transformation
 2. (CLAHE)
 3. (Gaussian)
 """
 img = io.imread(filepath)

 if img.ndim == 3:
 gray = color.rgb2gray(img)
 else:
 gray = img.astype(float)

 # CLAHE (Contrast Limited Adaptive Histogram Equalization)
 enhanced = exposure.equalize_adapthist(gray, clip_limit=0.03)

 # 
 denoised = filters.gaussian(enhanced, sigma=1)

 if target_size is not None:
 from skimage.transform import resize
 denoised = resize(denoised, target_size, anti_aliasing=True)

 return img, gray, denoised
```

## 2. 

### 2.1 Otsu + shape

```python
def otsu_segmentation(image, min_size=50, closing_disk=3):
 """
 Otsu threshold + shapeby/via。
 """
 threshold = filters.threshold_otsu(image)
 binary = image > threshold

 # shape
 binary = morphology.binary_closing(binary, morphology.disk(closing_disk))
 binary = morphology.remove_small_objects(binary, min_size=min_size)
 binary = ndimage.binary_fill_holes(binary)

 # 
 labels = measure.label(binary)

 return binary, labels, threshold
```

### 2.2 Watershed 

```python
from skimage.feature import peak_local_max

def watershed_segmentation(image, min_distance=10, footprint_size=3):
 """
 Watershed by/via's min。
 """
 threshold = filters.threshold_otsu(image)
 binary = image > threshold
 binary = ndimage.binary_fill_holes(binary)

 # transformation
 distance = ndimage.distance_transform_edt(binary)

 # 
 coords = peak_local_max(distance, min_distance=min_distance,
 labels=binary)
 mask = np.zeros(distance.shape, dtype=bool)
 mask[tuple(coords.T)] = True
 markers = measure.label(mask)

 # Watershed
 labels = watershed(-distance, markers, mask=binary)

 return labels, distance
```

## 3. shape

```python
def morphometric_analysis(labels, pixel_size_um=1.0):
 """
 labelfromeach's shapeparameters.

 item:
 - area: surface (μm²)
 - perimeter: (μm)
 - equivalent_diameter: (μm)
 - circularity: degree 4π·A/P²
 - aspect_ratio: (major/minor axis)
 - solidity: rate (area/convex_area)
 - eccentricity: rate
 """
 import pandas as pd

 props = measure.regionprops(labels)
 records = []

 for p in props:
 area = p.area * (pixel_size_um ** 2)
 perimeter = p.perimeter * pixel_size_um
 eq_diameter = p.equivalent_diameter * pixel_size_um
 circularity = (4 * np.pi * p.area) / (p.perimeter**2 + 1e-10)
 aspect_ratio = p.major_axis_length / (p.minor_axis_length + 1e-10)

 records.append({
 "label": p.label,
 "area_um2": area,
 "perimeter_um": perimeter,
 "equivalent_diameter_um": eq_diameter,
 "circularity": circularity,
 "aspect_ratio": aspect_ratio,
 "solidity": p.solidity,
 "eccentricity": p.eccentricity,
 "centroid_y": p.centroid[0],
 "centroid_x": p.centroid[1],
 })

 return pd.DataFrame(records)
```

## 4. distribution

```python
def particle_size_distribution(morpho_df, diameter_col="equivalent_diameter_um",
 bins=30, figsize=(10, 6)):
 """
 distribution's histogram and amount is computed。

 output:
 - histogram + kerneldegree
 - D10, D50 (median), D90
 - mean, standard deviation, number/count CV
 """
 diameters = morpho_df[diameter_col].values

 d10 = np.percentile(diameters, 10)
 d50 = np.percentile(diameters, 50)
 d90 = np.percentile(diameters, 90)
 span = (d90 - d10) / d50

 stats = {
 "count": len(diameters),
 "mean_um": np.mean(diameters),
 "std_um": np.std(diameters),
 "cv_pct": np.std(diameters) / np.mean(diameters) * 100,
 "d10_um": d10,
 "d50_um": d50,
 "d90_um": d90,
 "span": span,
 }

 fig, ax = plt.subplots(figsize=figsize)
 ax.hist(diameters, bins=bins, density=True, alpha=0.7, color="steelblue",
 edgecolor="black", linewidth=0.5)

 # KDE
 from scipy.stats import gaussian_kde
 kde = gaussian_kde(diameters)
 x_range = np.linspace(diameters.min, diameters.max, 200)
 ax.plot(x_range, kde(x_range), "r-", linewidth=2, label="KDE")

 # D10/D50/D90 line
 for d, label in [(d10, "D10"), (d50, "D50"), (d90, "D90")]:
 ax.axvline(d, color="gray", linestyle="--", alpha=0.7)
 ax.text(d, ax.get_ylim[1]*0.95, f" {label}={d:.1f}", fontsize=9)

 ax.set_xlabel("Diameter (μm)")
 ax.set_ylabel("Density")
 ax.set_title("Particle Size Distribution", fontweight="bold")
 ax.legend
 plt.tight_layout
 plt.savefig("figures/particle_size_distribution.png", dpi=300,
 bbox_inches="tight")
 plt.close

 return stats
```

## 5. analysis (GLCM)

```python
from skimage.feature import graycomatrix, graycoprops

def glcm_texture_features(image, distances=[1, 3, 5], angles=[0, np.pi/4,
 np.pi/2, 3*np.pi/4], levels=256):
 """
 GLCM (Gray-Level Co-occurrence Matrix) features is extracted。

 Features: contrast, dissimilarity, homogeneity, energy, correlation, ASM
 """
 img_uint8 = (image * 255).astype(np.uint8) if image.max <= 1 else image.astype(np.uint8)

 glcm = graycomatrix(img_uint8, distances=distances, angles=angles,
 levels=levels, symmetric=True, normed=True)

 features = {}
 for prop in ["contrast", "dissimilarity", "homogeneity", "energy",
 "correlation", "ASM"]:
 values = graycoprops(glcm, prop)
 features[f"{prop}_mean"] = values.mean
 features[f"{prop}_std"] = values.std

 return features
```

## 6. synthesis

```python
def merge_fluorescence_channels(channels, colors=None, figsize=(10, 10)):
 """
 'ssynthesis.

 Parameters:
 channels: dict {"DAPI": array, "GFP": array, "RFP": array}
 colors: dict {"DAPI": [0,0,1], "GFP": [0,1,0], "RFP": [1,0,0]}
 """
 if colors is None:
 colors = {"DAPI": [0, 0, 1], "GFP": [0, 1, 0], "RFP": [1, 0, 0],
 "Cy5": [1, 0, 1]}

 ch_names = list(channels.keys)
 shape = list(channels.values)[0].shape
 merged = np.zeros((*shape, 3))

 n = len(ch_names) + 1
 fig, axes = plt.subplots(1, n, figsize=(5*n, 5))

 for i, (name, img) in enumerate(channels.items):
 # normalization
 norm_img = (img - img.min) / (img.max - img.min + 1e-10)

 # unitstable
 ch_color = np.array(colors.get(name, [1, 1, 1]))
 colored = norm_img[:, :, np.newaxis] * ch_color
 axes[i].imshow(np.clip(colored, 0, 1))
 axes[i].set_title(name, fontweight="bold")
 axes[i].axis("off")

 # 
 merged += colored

 # synthesis
 axes[-1].imshow(np.clip(merged, 0, 1))
 axes[-1].set_title("Merged", fontweight="bold")
 axes[-1].axis("off")

 plt.tight_layout
 plt.savefig("figures/fluorescence_merged.png", dpi=300, bbox_inches="tight")
 plt.close

 return np.clip(merged, 0, 1)
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | analysisTool Registry Search |

## References

### Output Files

| File | Format |
|---|---|
| `results/morphometric_data.csv` | CSV |
| `results/particle_size_stats.csv` | CSV |
| `results/glcm_texture_features.csv` | CSV |
| `figures/segmentation_result.png` | PNG |
| `figures/particle_size_distribution.png` | PNG |
| `figures/fluorescence_merged.png` | PNG |

#### Dependencies

```
scikit-image>=0.21
scipy>=1.10
```

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
