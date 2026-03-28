---
name: scientific-image-analysis
description: |
 Image analysis skill. Scientific image processing, segmentation, morphological analysis, particle detection, colocalization analysis, and quantitative microscopy pipelines.
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
3. Write `report.md` summarizing methods, results, and interpretation

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

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Visualization)

Before execution, define:
- [ ] **Target audience**: journal / conference / dashboard / internal
- [ ] **Figure dimensions**: width x height, DPI requirement
- [ ] **Color scheme**: colorblind-safe palette confirmed
- [ ] **Data-ink ratio**: minimize non-data elements

#### Pass Criteria
- All figures saved to disk (never plt.show())
- Figures embedded in report.md with captions
- Text is English-only, font size >= 8pt
- Accessibility: contrast ratio >= 4.5:1
- Vector format (SVG/PDF) provided when requested
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
