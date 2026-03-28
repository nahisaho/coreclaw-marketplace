---
name: scientific-deep-learning
description: |
 deep learningskill。PyTorch LightningHugging Face Transformerstimm utilizing、
 NN designtransfer learningvariancehyperparametersoptimization
 support。
 「 」「Transformer Fine-tune 」「deep learningconstruction」 。
tu_tools:
 - key: papers_with_code
 name: Papers with Code
 description: deep learningsearch
---

# Scientific Deep Learning

deep learningforintegrationskill。datafor/against
NN designevaluation is supported。

## When to Use

- CNN / RNN / Transformer design
- transfer learningFine-tuning（）
- variance（ GPU / node）
- hyperparametersoptimization (Optuna / Ray Tune)
- data（protein Transformer ）
- exportinferencepipeline

## Quick Start

### deep learningpipeline

```
Phase 1: Data Preparation
 - datasetconstruction (Dataset / DataLoader)
 - data (Augmentation)
 - normalizationpreprocessing
 ↓
Phase 2: Architecture Design
 - (ResNet/ViT/BERT/etc.)
 - design (classification/regression/generation)
 - loss functionselection
 ↓
Phase 3: Training
 - Lightning Trainer settings
 - 
 - Mixed Precision (AMP)
 - 
 ↓
Phase 4: Hyperparameter Optimization
 - Optuna / Ray Tune
 - search/explorationdefinition
 - Pruning (Median / Hyperband)
 ↓
Phase 5: Evaluation
 - testingevaluation
 - curveline
 - min (→ XAI skill)
 ↓
Phase 6: Deployment
 - ONNX / TorchScript export
 - batchinferencepipeline
 - 
```

## Workflow

### 1. PyTorch Lightning: structurepipeline

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset
from torchmetrics import Accuracy, AUROC, MeanSquaredError

# === Lightning Module ===
class ScientificModel(pl.LightningModule):
 def __init__(self, model, lr=1e-3, weight_decay=1e-5, task="classification"):
 super.__init__
 self.save_hyperparameters(ignore=["model"])
 self.model = model
 self.lr = lr
 self.weight_decay = weight_decay
 self.task = task

 if task == "classification":
 self.criterion = nn.CrossEntropyLoss
 self.train_acc = Accuracy(task="binary")
 self.val_acc = Accuracy(task="binary")
 self.val_auroc = AUROC(task="binary")
 else:
 self.criterion = nn.MSELoss
 self.val_rmse = MeanSquaredError(squared=False)

 def forward(self, x):
 return self.model(x)

 def training_step(self, batch, batch_idx):
 x, y = batch
 logits = self(x)
 loss = self.criterion(logits, y)
 self.log("train/loss", loss, prog_bar=True)
 if self.task == "classification":
 preds = torch.argmax(logits, dim=1)
 self.train_acc(preds, y)
 self.log("train/acc", self.train_acc, prog_bar=True)
 return loss

 def validation_step(self, batch, batch_idx):
 x, y = batch
 logits = self(x)
 loss = self.criterion(logits, y)
 self.log("val/loss", loss, prog_bar=True)
 if self.task == "classification":
 preds = torch.argmax(logits, dim=1)
 self.val_acc(preds, y)
 self.val_auroc(logits[:, 1], y)
 self.log("val/acc", self.val_acc, prog_bar=True)
 self.log("val/auroc", self.val_auroc, prog_bar=True)
 else:
 self.val_rmse(logits.squeeze, y)
 self.log("val/rmse", self.val_rmse, prog_bar=True)

 def configure_optimizers(self):
 optimizer = torch.optim.AdamW(self.parameters, lr=self.lr,
 weight_decay=self.weight_decay)
 scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
 optimizer, T_max=self.trainer.max_epochs)
 return {"optimizer": optimizer, "lr_scheduler": scheduler}


# === ===
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint, LearningRateMonitor

trainer = pl.Trainer(
 max_epochs=100,
 accelerator="auto",
 devices="auto",
 precision="16-mixed", # AMP
 callbacks=[
 EarlyStopping(monitor="val/loss", patience=10, mode="min"),
 ModelCheckpoint(monitor="val/loss", save_top_k=3, mode="min"),
 LearningRateMonitor(logging_interval="epoch"),
 ],
 gradient_clip_val=1.0,
 deterministic=True,
)
# trainer.fit(model, train_loader, val_loader)
```

### 2. CNN (classification)

```python
import timm

# === timm: CNN ===
def create_cnn_model(model_name="resnet50", num_classes=10, pretrained=True):
 """timm libraryfrom"""
 model = timm.create_model(
 model_name,
 pretrained=pretrained,
 num_classes=num_classes,
 )
 return model

# usepossibleexample:
# - "resnet50", "resnet101"
# - "efficientnet_b0" ~ "efficientnet_b7"
# - "vit_base_patch16_224" (Vision Transformer)
# - "swin_base_patch4_window7_224" (Swin Transformer)
# - "convnext_base"

# === custom CNN ===
class ConvBlock(nn.Module):
 def __init__(self, in_ch, out_ch, kernel_size=3, stride=1):
 super.__init__
 self.conv = nn.Conv2d(in_ch, out_ch, kernel_size, stride, padding=kernel_size // 2)
 self.bn = nn.BatchNorm2d(out_ch)
 self.act = nn.GELU

 def forward(self, x):
 return self.act(self.bn(self.conv(x)))


class ScientificCNN(nn.Module):
 def __init__(self, in_channels=1, num_classes=10):
 super.__init__
 self.features = nn.Sequential(
 ConvBlock(in_channels, 32),
 ConvBlock(32, 64, stride=2),
 ConvBlock(64, 128, stride=2),
 ConvBlock(128, 256, stride=2),
 nn.AdaptiveAvgPool2d(1),
 )
 self.classifier = nn.Sequential(
 nn.Flatten,
 nn.Dropout(0.3),
 nn.Linear(256, num_classes),
 )

 def forward(self, x):
 return self.classifier(self.features(x))
```

### 3. Transformer / Fine-tuning

```python
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments

# === Hugging Face Transformer Fine-tuning ===
def finetune_transformer(model_name, train_dataset, val_dataset,
 num_labels=2, num_epochs=5, lr=2e-5):
 """classification's Transformer Fine-tuning"""
 tokenizer = AutoTokenizer.from_pretrained(model_name)
 model = AutoModelForSequenceClassification.from_pretrained(
 model_name, num_labels=num_labels
 )

 training_args = TrainingArguments(
 output_dir="./results/transformer_ft",
 num_train_epochs=num_epochs,
 per_device_train_batch_size=16,
 per_device_eval_batch_size=32,
 learning_rate=lr,
 weight_decay=0.01,
 warmup_ratio=0.1,
 evaluation_strategy="epoch",
 save_strategy="epoch",
 load_best_model_at_end=True,
 metric_for_best_model="eval_loss",
 fp16=True,
 dataloader_num_workers=4,
 )

 trainer = Trainer(
 model=model,
 args=training_args,
 train_dataset=train_dataset,
 eval_dataset=val_dataset,
 tokenizer=tokenizer,
 )

 trainer.train
 return trainer

# :
# - "allenai/scibert_scivocab_uncased" (SciBERT)
# - "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract" (BiomedBERT)
# - "ChemBERTa" ( SMILES)
# - "facebook/esm2_t33_650M_UR50D" (protein)
```

### 4. Optuna hyperparametersoptimization

```python
import optuna
from optuna.integration import PyTorchLightningPruningCallback

def optuna_optimization(train_loader, val_loader, n_trials=50):
 """Optuna by/viahyperparametersoptimization"""

 def objective(trial):
 # search/exploration
 lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
 weight_decay = trial.suggest_float("weight_decay", 1e-6, 1e-3, log=True)
 hidden_dim = trial.suggest_categorical("hidden_dim", [128, 256, 512])
 n_layers = trial.suggest_int("n_layers", 2, 6)
 dropout = trial.suggest_float("dropout", 0.1, 0.5)

 # construction
 model = build_model(hidden_dim, n_layers, dropout)
 lit_model = ScientificModel(model, lr=lr, weight_decay=weight_decay)

 # 
 trainer = pl.Trainer(
 max_epochs=30,
 callbacks=[
 PyTorchLightningPruningCallback(trial, monitor="val/loss"),
 EarlyStopping(monitor="val/loss", patience=5),
 ],
 enable_progress_bar=False,
 )

 trainer.fit(lit_model, train_loader, val_loader)
 return trainer.callback_metrics["val/loss"].item

 study = optuna.create_study(
 direction="minimize",
 pruner=optuna.pruners.HyperbandPruner,
 )
 study.optimize(objective, n_trials=n_trials)

 print(f"Best trial: {study.best_trial.value:.4f}")
 print(f"Best params: {study.best_trial.params}")

 # visualization
 optuna.visualization.plot_optimization_history(study).write_image(
 "figures/optuna_history.png")
 optuna.visualization.plot_param_importances(study).write_image(
 "figures/optuna_importance.png")

 return study
```

### 5. export

```python
def export_model(model, sample_input, export_dir="models"):
 """export (ONNX + TorchScript)"""
 import os
 os.makedirs(export_dir, exist_ok=True)

 model.eval

 # TorchScript
 scripted = torch.jit.trace(model, sample_input)
 scripted.save(f"{export_dir}/model.pt")

 # ONNX
 torch.onnx.export(
 model, sample_input,
 f"{export_dir}/model.onnx",
 input_names=["input"],
 output_names=["output"],
 dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
 opset_version=17,
 )

 print(f"Exported: {export_dir}/model.pt, {export_dir}/model.onnx")
```

---

## Best Practices

1. **PyTorch Lightning structure**: reproducibilityand 's Lightning Module for
2. **Mixed Precision**: `precision="16-mixed"` GPU rate and improvement
3. **Gradient Clipping**: `gradient_clip_val=1.0` gradient
4. **Cosine Annealing**: learning rateas
5. **Optuna + Pruning**: rate
6. **Scaffold Split** (moleculedata): min scaffold split for
7. **Model Card**: data documentation
8. **Seed **: `pl.seed_everything(42)` reproducibility

## Completeness Checklist

- [ ] Dataset / DataLoader construction
- [ ] design
- [ ] Training convergence check
- [ ] curvelineplot
- [ ] testingevaluationmetrics
- [ ] hyperparametersoptimization
- [ ] export (ONNX)
- [ ] 

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `papers_with_code` | Papers with Code | deep learningsearch |

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `results/dl_training_log.json` | log（JSON） | completion |
| `models/model.onnx` | ONNX | export |
| `figures/dl_learning_curve.png` | curveline | completion |
| `figures/optuna_history.png` | Optuna optimization | HPO completion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-ml-classification` | ← ML and 's comparison |
| `scientific-ml-regression` | ← regressiontask's DL |
| `scientific-explainable-ai` | → DeepSHAP/Captum by/via |
| `scientific-graph-neural-networks` | → graphdata's DL |
| `scientific-image-analysis` | ← data's CNN application |
| `scientific-medical-imaging` | → medical imaging's DL |
| `scientific-quantum-computing` | ← amount- ML |
| `scientific-neuroscience-electrophysiology` | ← neural/nerve DL |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (ML/AI)

Before execution, define:
- [ ] **Task type**: classification / regression / generation / ranking
- [ ] **Baseline**: naive baseline metric to beat
- [ ] **Target metric**: specific threshold (e.g., AUC > 0.85, RMSE < 0.1)
- [ ] **Data split**: train/val/test ratios, stratification method

#### Pass Criteria
- Model performance exceeds baseline by defined margin
- Train/val/test metrics all reported (no data leakage)
- Hyperparameters logged with search method
- Overfitting check: train-val gap < 10% relative
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
