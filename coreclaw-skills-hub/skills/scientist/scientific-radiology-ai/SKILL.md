---
name: scientific-radiology-ai
description: |
 Radiology AI skill. Medical image classification, detection, and segmentation for radiology, DICOM handling, radiomics, and clinical AI model evaluation.
---

# Scientific Radiology AI

radiology（CT/MRI/X line）for/against AI diagnosissupport
pipeline is provided。MONAI 's inference
explainabilitystructurereportgenerationincluding。

## When to Use

- CT/MRI/X line's AI classification is performedand
- CADe  / CADx (diagnosis) pipeline is builtand
- Grad-CAM AI 's explainabilitywhen needed
- structureradiologyreportautomatedgenerationwhen needed
- AI-RADS implementationwhen needed

---

## Quick Start

## 1. MONAI radiology AI classificationpipeline

```python
import numpy as np
import torch
import torch.nn as nn


def build_radiology_classifier(in_channels=1, num_classes=2,
 spatial_dims=3,
 architecture="densenet121"):
 """
 MONAI radiologyclassification。

 Parameters:
 in_channels: int — inputnumber/count (CT=1, MRI multimodal=4)
 num_classes: int — number/count
 spatial_dims: int — 2 (2D ) or 3 (3D )
 architecture: str — "densenet121" / "resnet50" / "efficientnet"
 """
 import monai.networks.nets as nets

 models = {
 "densenet121": nets.DenseNet121(
 spatial_dims=spatial_dims,
 in_channels=in_channels,
 out_channels=num_classes),
 "resnet50": nets.ResNet(
 block="bottleneck", layers=[3, 4, 6, 3],
 block_inplanes=[64, 128, 256, 512],
 spatial_dims=spatial_dims,
 n_input_channels=in_channels,
 num_classes=num_classes),
 "efficientnet": nets.EfficientNetBN(
 "efficientnet-b0",
 spatial_dims=spatial_dims,
 in_channels=in_channels,
 num_classes=num_classes),
 }
 model = models.get(architecture, models["densenet121"])
 total_params = sum(p.numel for p in model.parameters)
 print(f"Radiology classifier: {architecture} | "
 f"{total_params:,} params | {spatial_dims}D")
 return model


def train_radiology_model(model, train_loader, val_loader,
 epochs=50, lr=1e-4, device="cuda"):
 """
 radiology AI 。

 Parameters:
 model: nn.Module — classification
 train_loader: DataLoader — training data
 val_loader: DataLoader — validation data
 epochs: int — training epochs
 lr: float — learning rate
 device: str — device
 """
 import pandas as pd
 from monai.utils import set_determinism
 set_determinism(seed=42)

 model.to(device)
 optimizer = torch.optim.AdamW(model.parameters, lr=lr,
 weight_decay=1e-4)
 scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
 optimizer, T_max=epochs)
 criterion = nn.CrossEntropyLoss
 history = []

 best_val_acc = 0
 for epoch in range(epochs):
 model.train
 train_loss, correct, total = 0, 0, 0
 for batch in train_loader:
 images = batch["image"].to(device)
 labels = batch["label"].to(device)
 optimizer.zero_grad
 outputs = model(images)
 loss = criterion(outputs, labels)
 loss.backward
 optimizer.step
 train_loss += loss.item
 correct += (outputs.argmax(1) == labels).sum.item
 total += len(labels)

 scheduler.step

 # Validation
 model.eval
 val_loss, val_correct, val_total = 0, 0, 0
 with torch.no_grad:
 for batch in val_loader:
 images = batch["image"].to(device)
 labels = batch["label"].to(device)
 outputs = model(images)
 val_loss += criterion(outputs, labels).item
 val_correct += (outputs.argmax(1) == labels).sum.item
 val_total += len(labels)

 val_acc = val_correct / val_total
 if val_acc > best_val_acc:
 best_val_acc = val_acc
 torch.save(model.state_dict, "best_radiology_model.pt")

 history.append({
 "epoch": epoch + 1,
 "train_loss": train_loss / len(train_loader),
 "train_acc": correct / total,
 "val_loss": val_loss / len(val_loader),
 "val_acc": val_acc,
 })

 if (epoch + 1) % 10 == 0:
 print(f"Epoch {epoch+1}: train_acc={correct/total:.3f}, "
 f"val_acc={val_acc:.3f}")

 print(f"Best val_acc: {best_val_acc:.4f}")
 return pd.DataFrame(history)
```

## 2. Grad-CAM explainability

```python
def radiology_gradcam(model, image_tensor, target_layer=None,
 target_class=None, device="cuda"):
 """
 radiologyfor/against Grad-CAM visualization。

 Parameters:
 model: nn.Module — classification
 image_tensor: torch.Tensor — input [1, C, H, W] or [1, C, D, H, W]
 target_layer: nn.Module | None — CAM 
 target_class: int | None — (None=prediction)
 device: str — device
 """
 import matplotlib.pyplot as plt
 from monai.visualize import GradCAM

 model.to(device).eval
 image_tensor = image_tensor.to(device)

 if target_layer is None:
 # DenseNet 's features for
 for name, module in model.named_modules:
 if "features" in name or "layer4" in name:
 target_layer = name
 if target_layer is None:
 target_layer = list(model.named_modules)[-2][0]

 cam = GradCAM(nn_module=model, target_layers=target_layer)

 if target_class is None:
 with torch.no_grad:
 target_class = model(image_tensor).argmax(1).item

 result = cam(x=image_tensor, class_idx=target_class)
 cam_map = result.squeeze.cpu.numpy

 # 2D visualization
 if cam_map.ndim == 3:
 mid_slice = cam_map.shape[0] // 2
 cam_map_2d = cam_map[mid_slice]
 img_2d = image_tensor.squeeze.cpu.numpy[mid_slice]
 else:
 cam_map_2d = cam_map
 img_2d = image_tensor.squeeze.cpu.numpy

 fig, axes = plt.subplots(1, 3, figsize=(15, 5))
 axes[0].imshow(img_2d, cmap="gray")
 axes[0].set_title("Original")
 axes[1].imshow(cam_map_2d, cmap="jet")
 axes[1].set_title(f"Grad-CAM (class={target_class})")
 axes[2].imshow(img_2d, cmap="gray")
 axes[2].imshow(cam_map_2d, cmap="jet", alpha=0.4)
 axes[2].set_title("Overlay")
 for ax in axes:
 ax.axis("off")
 plt.tight_layout
 plt.savefig("gradcam_radiology.png", dpi=150, bbox_inches="tight")
 print(f"Grad-CAM saved → gradcam_radiology.png (class={target_class})")
 return cam_map
```

## 3. structureradiologyreport

```python
def generate_structured_report(predictions, patient_info=None,
 modality="CT", body_part="Chest"):
 """
 AI supportstructureradiologyreportgeneration。

 Parameters:
 predictions: dict — {"finding": str, "probability": float,...}
 patient_info: dict | None — patientinformation
 modality: str — "CT" / "MRI" / "XR"
 body_part: str — 
 """
 if patient_info is None:
 patient_info = {"id": "ANON", "age": "N/A", "sex": "N/A"}

 findings = []
 for finding, prob in predictions.items:
 if prob >= 0.5:
 confidence = "High" if prob >= 0.8 else "Moderate"
 findings.append(f"- {finding}: {prob:.1%} ({confidence} confidence)")

 report = f"""## Structured Radiology Report (AI-Assisted)

**Patient**: {patient_info.get('id', 'N/A')} | \
Age: {patient_info.get('age', 'N/A')} | Sex: {patient_info.get('sex', 'N/A')}
**Modality**: {modality} | **Body Part**: {body_part}

### AI Findings

{chr(10).join(findings) if findings else '- No significant findings detected'}

### AI Confidence Summary

| Finding | Probability | AI-RADS |
|---------|:-----------:|:-------:|
"""
 for finding, prob in sorted(predictions.items,
 key=lambda x: x[1], reverse=True):
 rads = 5 if prob >= 0.9 else 4 if prob >= 0.7 else \
 3 if prob >= 0.5 else 2 if prob >= 0.3 else 1
 report += f"| {finding} | {prob:.1%} | {rads} |\n"

 report += """
### Disclaimer
> This report was generated with AI assistance and requires
> review by a qualified radiologist before clinical use.
"""
 print(report)
 return report
```

---

## Pipeline Integration

```
[DICOM retrieval] → medical-imaging → radiology-ai → clinical-report
 (preprocessing/Radiomics) (AI diagnosis) (report)
 │
 explainable-ai ← deep-learning
 (explainability) 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `best_radiology_model.pt` | classification | → inference |
| `gradcam_radiology.png` | Grad-CAM visualization | → report |
| `structured_report.md` | structurereport | → clinical-report |

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
