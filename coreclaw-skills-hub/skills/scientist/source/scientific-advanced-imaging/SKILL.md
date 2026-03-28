---
name: scientific-advanced-imaging
description: |
 advancedanalysisskill。CellProfiler by/via
 Cell Painting analysis、Cellpose by/viadeep learning
 cell、napari by/via 3D visualization。
tu_tools:
 - key: biotools
 name: bio.tools
 description: advancedtoolsearch
---

# Scientific Advanced Imaging

CellProfiler / Cellpose / napari utilizingadvanced
analysispipeline is provided。cell、shape
feature extraction、Cell Painting analysis、3D visualization。

## When to Use

- Cell Painting analysiswhen needed
- deep learningby/viacellwhen needed (Cellpose)
- shapefeatures (surface、degree、) amountwhen needed
- 3D visualizationwhen needed
- custom Cellpose when needed
- (HCS) data is processedand

---

## Quick Start

## 1. Cellpose cell

```python
from cellpose import models, io
import numpy as np
from pathlib import Path


def cellpose_segmentation(image_path, model_type="cyto2", diameter=None,
 channels=None, gpu=True):
 """
 Cellpose cell。

 Parameters:
 image_path: str — file path
 model_type: str — ("cyto", "cyto2", "nuclei")
 diameter: float — cell (None automated)
 channels: list — [cytoplasm, nuclei]
 gpu: bool — GPU for

 K-Dense: cellpose
 """
 model = models.Cellpose(model_type=model_type, gpu=gpu)

 if channels is None:
 channels = [0, 0] # grayscale

 img = io.imread(str(image_path))
 masks, flows, styles, diams = model.eval(
 img, diameter=diameter, channels=channels
 )

 n_cells = len(np.unique(masks)) - 1 # background
 print(f"Cellpose: {n_cells} cells detected (model={model_type})")
 print(f" Auto diameter: {diams:.1f}")
 return masks, flows, styles
```

## 2. batch

```python
def batch_segmentation(image_dir, output_dir, model_type="cyto2",
 image_pattern="*.tif", diameter=None):
 """
 directory's batch。

 Parameters:
 image_dir: str — inputdirectory
 output_dir: str — output directory
 model_type: str — Cellpose 
 """
 model = models.Cellpose(model_type=model_type, gpu=True)
 image_dir = Path(image_dir)
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 image_files = sorted(image_dir.glob(image_pattern))
 results = []

 for img_path in image_files:
 img = io.imread(str(img_path))
 masks, flows, styles, diams = model.eval(
 img, diameter=diameter, channels=[0, 0]
 )
 n_cells = len(np.unique(masks)) - 1

 # save
 out_path = output_dir / f"{img_path.stem}_masks.npy"
 np.save(str(out_path), masks)

 results.append({
 "image": img_path.name,
 "n_cells": n_cells,
 "diameter": float(diams),
 })

 print(f"Batch: {len(results)} images, "
 f"{sum(r['n_cells'] for r in results)} total cells")
 return results
```

## 3. CellProfiler shape

```python
import skimage.measure as measure
import pandas as pd


def morphological_profiling(image, masks, channel_names=None):
 """
 CellProfiler 's shapefeaturesextraction。

 Parameters:
 image: np.ndarray — (H, W) or (H, W, C)
 masks: np.ndarray — segmentation masks
 channel_names: list — 

 K-Dense: cellprofiler
 """
 if image.ndim == 2:
 image = image[..., np.newaxis]
 if channel_names is None:
 channel_names = [f"ch{i}" for i in range(image.shape[-1])]

 props = measure.regionprops(masks, intensity_image=image[..., 0])

 features = []
 for prop in props:
 feat = {
 "cell_id": prop.label,
 "area": prop.area,
 "perimeter": prop.perimeter,
 "eccentricity": prop.eccentricity,
 "solidity": prop.solidity,
 "major_axis": prop.major_axis_length,
 "minor_axis": prop.minor_axis_length,
 }
 # degree
 if prop.perimeter > 0:
 feat["circularity"] = (4 * np.pi * prop.area) / (prop.perimeter ** 2)
 else:
 feat["circularity"] = 0.0

 # andintensity
 for ch_idx, ch_name in enumerate(channel_names):
 ch_props = measure.regionprops(
 masks, intensity_image=image[..., ch_idx]
 )
 for cp in ch_props:
 if cp.label == prop.label:
 feat[f"{ch_name}_mean"] = cp.mean_intensity
 feat[f"{ch_name}_max"] = cp.max_intensity
 feat[f"{ch_name}_min"] = cp.min_intensity
 break

 features.append(feat)

 df = pd.DataFrame(features)
 print(f"Morphological profiling: {len(df)} cells, {len(df.columns)} features")
 return df
```

## 4. Cell Painting analysis

```python
def cell_painting_analysis(image_5ch, masks, normalize=True):
 """
 Cell Painting 5 analysis。

 Channels:
 ch0: DNA (Hoechst), ch1: ER (ConA), ch2: RNA (SYTO14),
 ch3: AGP (Phalloidin), ch4: Mito (MitoTracker)

 Parameters:
 image_5ch: np.ndarray — (H, W, 5) 
 masks: np.ndarray — segmentation masks
 normalize: bool — Z-score normalization
 """
 channel_names = ["DNA", "ER", "RNA", "AGP", "Mito"]

 # shape + featuresextraction
 features_df = morphological_profiling(image_5ch, masks, channel_names)

 # features (Haralick-like)
 from skimage.feature import graycomatrix, graycoprops

 texture_features = []
 for prop in measure.regionprops(masks):
 cell_mask = masks == prop.label
 bbox = prop.bbox
 cell_region = image_5ch[bbox[0]:bbox[2], bbox[1]:bbox[3], 0]
 cell_mask_crop = cell_mask[bbox[0]:bbox[2], bbox[1]:bbox[3]]
 cell_region = (cell_region * cell_mask_crop).astype(np.uint8)

 if cell_region.max > 0:
 glcm = graycomatrix(cell_region, [1], [0], levels=256, symmetric=True)
 texture_features.append({
 "cell_id": prop.label,
 "contrast": graycoprops(glcm, "contrast")[0, 0],
 "homogeneity": graycoprops(glcm, "homogeneity")[0, 0],
 "energy": graycoprops(glcm, "energy")[0, 0],
 "correlation": graycoprops(glcm, "correlation")[0, 0],
 })

 texture_df = pd.DataFrame(texture_features)
 combined = features_df.merge(texture_df, on="cell_id", how="left")

 if normalize:
 numeric_cols = combined.select_dtypes(include=[np.number]).columns
 numeric_cols = [c for c in numeric_cols if c != "cell_id"]
 combined[numeric_cols] = (
 (combined[numeric_cols] - combined[numeric_cols].mean)
 / combined[numeric_cols].std
 )

 print(f"Cell Painting: {len(combined)} cells, {len(combined.columns)} features")
 return combined
```

## 5. napari 3D visualization

```python
def napari_visualization(image, masks=None, points=None, labels=None):
 """
 napari 3D visualization。

 Parameters:
 image: np.ndarray — (Z, Y, X) or (Z, Y, X, C)
 masks: np.ndarray — segmentation masks
 points: np.ndarray — coordinatespoint (N, 3)
 labels: list — label

 K-Dense: napari
 """
 import napari

 viewer = napari.Viewer

 # layer
 if image.ndim == 4:
 for ch in range(image.shape[-1]):
 viewer.add_image(
 image[..., ch],
 name=f"Channel-{ch}",
 blending="additive",
 )
 else:
 viewer.add_image(image, name="Image")

 # layer
 if masks is not None:
 viewer.add_labels(masks, name="Segmentation")

 # layer
 if points is not None:
 properties = {"label": labels} if labels else None
 viewer.add_points(
 points,
 properties=properties,
 name="Points",
 size=5,
 )

 print(f"napari viewer: {image.shape}, "
 f"masks={'Yes' if masks is not None else 'No'}")
 return viewer
```

## 6. Cellpose custom

```python
def finetune_cellpose(train_dir, model_type="cyto2", n_epochs=100,
 learning_rate=0.1):
 """
 Cellpose 's 。

 Parameters:
 train_dir: str — training data ( + _masks)
 model_type: str — 
 n_epochs: int — number of epochs
 learning_rate: float — learning rate
 """
 from cellpose import train

 train_dir = Path(train_dir)
 image_files = sorted(train_dir.glob("*.tif"))
 mask_files = sorted(train_dir.glob("*_masks.tif"))

 images = [io.imread(str(f)) for f in image_files]
 labels = [io.imread(str(f)) for f in mask_files]

 model = models.CellposeModel(model_type=model_type, gpu=True)
 model_path = model.train(
 images, labels,
 channels=[0, 0],
 n_epochs=n_epochs,
 learning_rate=learning_rate,
 save_path=str(train_dir / "models"),
 )

 print(f"Fine-tuned model saved: {model_path}")
 print(f" Base: {model_type}, Epochs: {n_epochs}")
 return model_path
```

## 7. integrationpipeline

```python
def imaging_pipeline(image_dir, output_dir, model_type="cyto2",
 channels_5=True):
 """
 + featuresextraction integrationpipeline。

 Parameters:
 image_dir: str — inputdirectory
 output_dir: str — output directory
 model_type: str — Cellpose 
 channels_5: bool — 5ch Cell Painting
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) batch
 seg_results = batch_segmentation(
 image_dir, output_dir / "masks", model_type=model_type
 )

 # 2) featuresextraction
 all_features = []
 for res in seg_results:
 img_path = Path(image_dir) / res["image"]
 mask_path = output_dir / "masks" / f"{img_path.stem}_masks.npy"

 img = io.imread(str(img_path))
 masks = np.load(str(mask_path))

 if channels_5 and img.ndim == 3 and img.shape[-1] == 5:
 feats = cell_painting_analysis(img, masks)
 else:
 feats = morphological_profiling(img, masks)

 feats["image"] = res["image"]
 all_features.append(feats)

 combined = pd.concat(all_features, ignore_index=True)
 combined.to_csv(output_dir / "features.csv", index=False)

 print(f"Pipeline complete: {len(seg_results)} images, "
 f"{len(combined)} cells profiled")
 return combined
```

---

## Pipeline Integration

```
image-analysis → advanced-imaging → medical-imaging
 (OpenCV/basic) (Cellpose/CellProfiler) (DICOM/MONAI)
 │ │ ↓
fluorescence-microscopy ──┘ drug-target-profiling
 (retrieval) │ (Cell Painting hit)
 ↓
 cheminformatics
 (Cell Painting → compoundactivity)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/masks/` | segmentation masksgroup | → medical-imaging |
| `results/features.csv` | shapefeatures | → cheminformatics |
| `results/cell_painting.csv` | Cell Painting file | → drug-target-profiling |
| `results/model/` | Cellpose | — |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | advancedtoolsearch |
