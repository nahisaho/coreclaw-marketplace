---
name: scientific-radiology-ai
description: |
 radiologydiagnosissupport AI skill。CADe/CADx pipeline
 CT/MRI classificationGrad-CAM explainability
 structurereportAI-RADS 。
 ※ scientific-medical-imaging (DICOM/WSI/Radiomics) 's 
 radiologydiagnosis AI 。
tu_tools:
 - key: tcia
 name: TCIA
 description: radiologyDataset Search
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `tcia` | TCIA | radiologyDataset Search |
