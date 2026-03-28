---
name: scientific-medical-imaging
description: |
 Medical imaging skill. DICOM processing, image segmentation (U-Net), classification, registration, radiomics feature extraction, and clinical imaging pipeline development.
---

# Scientific Medical Imaging

forforanalysisskill。
DICOM / NIfTI 's radiology and WSI (Whole Slide Image) 's 
tissue andanalysispipeline is provided。

## When to Use

- DICOM / NIfTI medical imaging's loadpreprocessing
- CT / MRI / PET 's
- WSI (Whole Slide Image) tissueanalysis
- radiology'sfeaturesextraction (Radiomics)
- medical imaging's deep learning (MONAI)
- 3D visualization

## Quick Start

### forpipeline

```
Phase 1: Data Ingestion
 - DICOM / NIfTI fileload
 - dataextraction (patientinformationcondition)
 - 
 ↓
Phase 2: Preprocessing
 - sampling (Isotropic spacing)
 - normalization (Windowing / Z-score)
 - Registration 
 ↓
Phase 3: Segmentation
 - U-Net / nnU-Net / Swin UNETR
 - organ/
 - postprocessing (shape)
 ↓
Phase 4: Feature Extraction
 - Radiomics (PyRadiomics)
 - shapeintensityfeatures
 - WSI features
 ↓
Phase 5: Analysis
 - tumorratecalculation
 - radiologytreatmentdesignsupport
 - tissueclassification
 ↓
Phase 6: Reporting
 - DICOM-SR (Structured Report)
 - analysisreportgeneration
 - 3D visualization
```

## Workflow

### 1. DICOM 

```python
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# === DICOM load ===
def load_dicom_series(dicom_dir):
 """DICOM → 3D """
 dicom_dir = Path(dicom_dir)
 slices = []

 for dcm_file in sorted(dicom_dir.glob("*.dcm")):
 ds = pydicom.dcmread(dcm_file)
 slices.append(ds)

 # 
 slices.sort(key=lambda s: float(s.ImagePositionPatient[2]))

 # data
 metadata = {
 "patient_id": slices[0].PatientID,
 "modality": slices[0].Modality,
 "rows": slices[0].Rows,
 "cols": slices[0].Columns,
 "n_slices": len(slices),
 "pixel_spacing": list(slices[0].PixelSpacing),
 "slice_thickness": float(slices[0].SliceThickness),
 }

 # 3D volume construction
 volume = np.stack([s.pixel_array for s in slices])

 # HU (Hounsfield Unit) transformation
 slope = float(slices[0].RescaleSlope)
 intercept = float(slices[0].RescaleIntercept)
 volume_hu = volume * slope + intercept

 print(f"Volume shape: {volume_hu.shape}")
 print(f"HU range: [{volume_hu.min}, {volume_hu.max}]")

 return volume_hu, metadata


# === Windowing  ===
def apply_window(volume, window_center, window_width):
 """CT settings"""
 # standardsettings:
 # Lung: WC=-600, WW=1500
 # Bone: WC=300, WW=1500
 # Brain: WC=40, WW=80
 # Liver: WC=50, WW=350
 lower = window_center - window_width / 2
 upper = window_center + window_width / 2
 volume_windowed = np.clip(volume, lower, upper)
 volume_windowed = (volume_windowed - lower) / (upper - lower)
 return volume_windowed
```

### 2. NIfTI (SimpleITK)

```python
import SimpleITK as sitk

def load_nifti(filepath):
 """NIfTI load"""
 img = sitk.ReadImage(filepath)
 array = sitk.GetArrayFromImage(img)
 spacing = img.GetSpacing
 origin = img.GetOrigin
 direction = img.GetDirection

 return {
 "array": array,
 "spacing": spacing,
 "origin": origin,
 "direction": direction,
 "shape": array.shape,
 }


def resample_isotropic(image, new_spacing=(1.0, 1.0, 1.0)):
 """Isotropic sampling"""
 original_spacing = image.GetSpacing
 original_size = image.GetSize

 new_size = [
 int(round(osz * osp / nsp))
 for osz, osp, nsp in zip(original_size, original_spacing, new_spacing)
 ]

 resampler = sitk.ResampleImageFilter
 resampler.SetOutputSpacing(new_spacing)
 resampler.SetSize(new_size)
 resampler.SetOutputDirection(image.GetDirection)
 resampler.SetOutputOrigin(image.GetOrigin)
 resampler.SetTransform(sitk.Transform)
 resampler.SetDefaultPixelValue(image.GetPixelIDValue)
 resampler.SetInterpolator(sitk.sitkBSpline)

 return resampler.Execute(image)


def registration(fixed_image, moving_image):
 """ """
 registration_method = sitk.ImageRegistrationMethod

 # Similarity metric
 registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
 registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
 registration_method.SetMetricSamplingPercentage(0.01)

 # Optimizer
 registration_method.SetOptimizerAsGradientDescent(
 learningRate=1.0, numberOfIterations=100,
 convergenceMinimumValue=1e-6, convergenceWindowSize=10)

 # Transform
 initial_transform = sitk.CenteredTransformInitializer(
 fixed_image, moving_image, sitk.Euler3DTransform,
 sitk.CenteredTransformInitializerFilter.GEOMETRY)
 registration_method.SetInitialTransform(initial_transform, inPlace=False)

 final_transform = registration_method.Execute(fixed_image, moving_image)
 return final_transform
```

### 3. MONAI: medical imagingdeep learning

```python
import monai
from monai.networks.nets import UNet, SwinUNETR
from monai.losses import DiceLoss, DiceCELoss
from monai.metrics import DiceMetric
from monai.transforms import (
 Compose, LoadImaged, EnsureChannelFirstd, Spacingd,
 ScaleIntensityRanged, CropForegroundd, RandCropByPosNegLabeld,
 RandFlipd, RandRotate90d,
)

# === MONAI Transform pipeline ===
train_transforms = Compose([
 LoadImaged(keys=["image", "label"]),
 EnsureChannelFirstd(keys=["image", "label"]),
 Spacingd(keys=["image", "label"], pixdim=(1.5, 1.5, 2.0), mode=("bilinear", "nearest")),
 ScaleIntensityRanged(keys=["image"], a_min=-175, a_max=250, b_min=0.0, b_max=1.0, clip=True),
 CropForegroundd(keys=["image", "label"], source_key="image"),
 RandCropByPosNegLabeld(
 keys=["image", "label"], label_key="label",
 spatial_size=(96, 96, 96), pos=1, neg=1, num_samples=4,
 ),
 RandFlipd(keys=["image", "label"], prob=0.5, spatial_axis=0),
 RandRotate90d(keys=["image", "label"], prob=0.5),
])

# === U-Net for 3D Segmentation ===
model = UNet(
 spatial_dims=3,
 in_channels=1,
 out_channels=14, # organnumber/count
 channels=(16, 32, 64, 128, 256),
 strides=(2, 2, 2, 2),
 num_res_units=2,
 dropout=0.2,
)

# === Swin UNETR (Transformer ) ===
model_swin = SwinUNETR(
 img_size=(96, 96, 96),
 in_channels=1,
 out_channels=14,
 feature_size=48,
 use_checkpoint=True,
)

# Loss + Optimizer
loss_fn = DiceCELoss(to_onehot_y=True, softmax=True)
dice_metric = DiceMetric(include_background=False, reduction="mean")
```

### 4. WSI (Whole Slide Image) analysis

```python
# === openslide WSI load ===
import openslide

def load_wsi(wsi_path):
 """WSI (svs/ndpi/tiff) load"""
 slide = openslide.OpenSlide(wsi_path)

 metadata = {
 "dimensions": slide.dimensions, # (width, height) at level 0
 "level_count": slide.level_count,
 "level_dimensions": slide.level_dimensions,
 "level_downsamples": slide.level_downsamples,
 "properties": dict(slide.properties),
 }

 print(f"WSI size: {slide.dimensions[0]:,} x {slide.dimensions[1]:,} pixels")
 print(f"Levels: {slide.level_count}")

 return slide, metadata


def extract_tissue_patches(slide, patch_size=256, level=0, threshold=0.7):
 """
 tissuefromextraction。
 Otsu thresholdbackground 、tissuerate threshold above/more's 'sretrieval。
 """
 from skimage.filters import threshold_otsu
 from skimage.color import rgb2gray

 # retrieval (tissuefor)
 thumb_level = min(slide.level_count - 1, 4)
 thumbnail = slide.get_thumbnail(
 (slide.level_dimensions[thumb_level][0], slide.level_dimensions[thumb_level][1])
 )
 thumb_gray = rgb2gray(np.array(thumbnail))
 thresh = threshold_otsu(thumb_gray)
 tissue_mask = thumb_gray < thresh

 # coordinatescalculation
 downsample = slide.level_downsamples[thumb_level]
 patches = []
 w, h = slide.level_dimensions[level]

 for y in range(0, h, patch_size):
 for x in range(0, w, patch_size):
 # 's support
 tx = int(x / downsample)
 ty = int(y / downsample)
 tw = int(patch_size / downsample)
 th = int(patch_size / downsample)

 if tx + tw <= tissue_mask.shape[1] and ty + th <= tissue_mask.shape[0]:
 tissue_ratio = tissue_mask[ty:ty+th, tx:tx+tw].mean
 if tissue_ratio >= threshold:
 patch = slide.read_region((x, y), level, (patch_size, patch_size))
 patches.append({
 "image": np.array(patch.convert("RGB")),
 "x": x, "y": y,
 "tissue_ratio": round(tissue_ratio, 3),
 })

 print(f"Extracted {len(patches)} tissue patches from WSI")
 return patches
```

### 5. Radiomics featuresextraction

```python
from radiomics import featureextractor

def extract_radiomics(image_path, mask_path, params=None):
 """
 PyRadiomics radiologyfeaturesextraction。
 Shape, First-Order, GLCM, GLRLM, GLSZM, GLDM, NGTDM
 """
 if params is None:
 params = {
 "setting": {
 "binWidth": 25,
 "resampledPixelSpacing": [1, 1, 1],
 "interpolator": "sitkBSpline",
 "normalize": True,
 },
 "featureClass": {
 "shape": None,
 "firstorder": None,
 "glcm": None,
 "glrlm": None,
 "glszm": None,
 },
 }

 extractor = featureextractor.RadiomicsFeatureExtractor
 for key, val in params.get("setting", {}).items:
 extractor.settings[key] = val

 features = extractor.execute(image_path, mask_path)

 # diagnostics 
 radiomic_features = {
 k: float(v) for k, v in features.items
 if not k.startswith("diagnostics_")
 }

 print(f"Extracted {len(radiomic_features)} radiomic features")
 return radiomic_features
```

### 6. reportgeneration

```python
import json

def generate_imaging_report(patient_id, modality, findings,
 segmentation_results=None, radiomics=None,
 output_dir="results"):
 """medical imaginganalysisreport"""
 report = {
 "patient_id": patient_id,
 "modality": modality,
 "analysis_date": pd.Timestamp.now.isoformat if "pd" in dir else "",
 "findings": findings,
 }

 if segmentation_results:
 report["segmentation"] = {
 "model": segmentation_results.get("model", ""),
 "dice_scores": segmentation_results.get("dice_scores", {}),
 "volumes_ml": segmentation_results.get("volumes", {}),
 }

 if radiomics:
 report["radiomics"] = {
 "n_features": len(radiomics),
 "top_features": dict(sorted(
 radiomics.items, key=lambda x: abs(x[1]), reverse=True
 )[:20]),
 }

 with open(f"{output_dir}/imaging_report.json", "w") as f:
 json.dump(report, f, indent=2, default=str)

 md = f"# Medical Imaging Report\n\n"
 md += f"**Patient**: {patient_id} | **Modality**: {modality}\n\n"
 md += f"## Findings\n\n"
 for finding in findings:
 md += f"- {finding}\n"

 if segmentation_results:
 md += f"\n## Segmentation Results\n\n"
 md += "| Structure | Dice Score | Volume (ml) |\n|---|---|---|\n"
 for struct, dice in segmentation_results.get("dice_scores", {}).items:
 vol = segmentation_results.get("volumes", {}).get(struct, "")
 md += f"| {struct} | {dice:.3f} | {vol} |\n"

 with open(f"{output_dir}/imaging_report.md", "w") as f:
 f.write(md)

 return report
```

---

## Best Practices

1. **Isotropic sampling**: cellfromanalysis
2. **Windowing**: CT tissue settings for (tissue)
3. **nnU-Net**: task nnU-Net automatedsettings SOTA 
4. **WSI analysis**: pixel
5. **Dice + Hausdorff**: evaluation Dice and Hausdorff Distance for
6. ****: DICOM data's patientinformation
7. **3D context**: 2D 3D 's analysisrecommended

## Completeness Checklist

- [ ] DICOM/NIfTI loaddataextraction
- [ ] preprocessing（samplingnormalization）
- [ ] Dice evaluation
- [ ] Radiomics featuresextraction（）
- [ ] WSI extractiontissue（case）
- [ ] 3D visualization
- [ ] report（JSON + Markdown）generation

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

| File | Format | Generated When |
|---|---|---|
| `results/imaging_report.json` | analysisreport（JSON） | analysiscompletion |
| `results/imaging_report.md` | analysisreport（Markdown） | reportgeneration |
| `results/radiomics_features.json` | Radiomics features（JSON） | featuresextraction |
| `figures/segmentation_overlay.png` | resultsfigure | |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-image-analysis` | ← |
| `scientific-deep-learning` | ← U-Net/SwinUNETR 's |
| `scientific-ml-classification` | ← Radiomics featuresusingclassification |
| `scientific-precision-oncology` | → tumor'sintegration |
| `scientific-clinical-decision-support` | → 'sclinical decision support |
| `scientific-explainable-ai` | → for AI 's explainability (GradCAM) |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
