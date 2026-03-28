---
name: scientific-transfer-learning
description: |
 transfer learningskill。tuning
 Few-shot / Zero-shot (DA)
 task。
tu_tools:
 - key: papers_with_code
 name: Papers with Code
 description: transfer learningsearch
---

# Scientific Transfer Learning

's data to 's
Few-shot pipeline is provided。

## When to Use

- (ImageNet/BERT) tuningwhen needed
- small-scaledatasethigh-accuracywhen needed
- differentdatadistribution's and
- Few-shot number/countexamplefromclassificationwhen needed
- large-scaleamountwhen needed
- task multipletaskwhen needed

---

## Quick Start

## 1. Vision tuning

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np


def finetune_vision_model(train_loader, val_loader,
 model_name="resnet50",
 num_classes=10, epochs=20,
 lr=1e-4, freeze_backbone=True):
 """
 Vision tuning。

 Parameters:
 train_loader: DataLoader — data
 val_loader: DataLoader — validation data
 model_name: str — "resnet50" / "vit_b_16" / "efficientnet_b0"
 num_classes: int — number/count
 epochs: int — number of epochs
 lr: float — learning rate
 freeze_backbone: bool — 
 """
 import torchvision.models as models

 # 
 model_fn = getattr(models, model_name)
 weights_name = model_name.replace("_", "").title + "_Weights"
 try:
 weights = getattr(models, weights_name).DEFAULT
 except AttributeError:
 weights = "DEFAULT"
 model = model_fn(weights=weights)

 # 
 if hasattr(model, "fc"):
 in_features = model.fc.in_features
 model.fc = nn.Linear(in_features, num_classes)
 elif hasattr(model, "classifier"):
 if isinstance(model.classifier, nn.Sequential):
 in_features = model.classifier[-1].in_features
 model.classifier[-1] = nn.Linear(in_features, num_classes)
 else:
 in_features = model.classifier.in_features
 model.classifier = nn.Linear(in_features, num_classes)
 elif hasattr(model, "heads"):
 in_features = model.heads.head.in_features
 model.heads.head = nn.Linear(in_features, num_classes)

 # 
 if freeze_backbone:
 for name, param in model.named_parameters:
 if "fc" not in name and "classifier" not in name and "heads" not in name:
 param.requires_grad = False

 device = torch.device("cuda" if torch.cuda.is_available else "cpu")
 model = model.to(device)

 optimizer = torch.optim.AdamW(
 filter(lambda p: p.requires_grad, model.parameters), lr=lr)
 criterion = nn.CrossEntropyLoss
 scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, epochs)

 best_acc = 0.0
 history = []

 for epoch in range(epochs):
 model.train
 train_loss = 0.0
 for X_batch, y_batch in train_loader:
 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
 optimizer.zero_grad
 outputs = model(X_batch)
 loss = criterion(outputs, y_batch)
 loss.backward
 optimizer.step
 train_loss += loss.item
 scheduler.step

 # Validation
 model.eval
 correct = total = 0
 with torch.no_grad:
 for X_batch, y_batch in val_loader:
 X_batch, y_batch = X_batch.to(device), y_batch.to(device)
 outputs = model(X_batch)
 _, predicted = outputs.max(1)
 total += y_batch.size(0)
 correct += predicted.eq(y_batch).sum.item

 val_acc = correct / total
 history.append({"epoch": epoch, "train_loss": train_loss / len(train_loader),
 "val_acc": val_acc})
 if val_acc > best_acc:
 best_acc = val_acc

 print(f"Finetune {model_name}: best val acc = {best_acc:.4f}")
 return model, history
```

## 2. NLP tuning

```python
def finetune_text_classifier(train_texts, train_labels,
 val_texts, val_labels,
 model_name="dmis-lab/biobert-base-cased-v1.2",
 num_labels=2, epochs=5, lr=2e-5):
 """
 BERT/BioBERT classificationtuning。

 Parameters:
 train_texts: list[str] — 
 train_labels: list[int] — label
 val_texts: list[str] — verification
 val_labels: list[int] — verificationlabel
 model_name: str — HuggingFace model name
 num_labels: int — labelnumber/count
 epochs: int — number of epochs
 lr: float — learning rate
 """
 from transformers import (
 AutoTokenizer, AutoModelForSequenceClassification,
 TrainingArguments, Trainer)
 from datasets import Dataset

 tokenizer = AutoTokenizer.from_pretrained(model_name)
 model = AutoModelForSequenceClassification.from_pretrained(
 model_name, num_labels=num_labels)

 def tokenize(examples):
 return tokenizer(examples["text"], truncation=True,
 padding="max_length", max_length=512)

 train_ds = Dataset.from_dict({"text": train_texts, "label": train_labels})
 val_ds = Dataset.from_dict({"text": val_texts, "label": val_labels})
 train_ds = train_ds.map(tokenize, batched=True)
 val_ds = val_ds.map(tokenize, batched=True)

 args = TrainingArguments(
 output_dir="./ft_output", num_train_epochs=epochs,
 per_device_train_batch_size=16, learning_rate=lr,
 evaluation_strategy="epoch", save_strategy="epoch",
 load_best_model_at_end=True, metric_for_best_model="accuracy")

 def compute_metrics(eval_pred):
 preds = np.argmax(eval_pred.predictions, axis=-1)
 acc = (preds == eval_pred.label_ids).mean
 return {"accuracy": acc}

 trainer = Trainer(model=model, args=args, train_dataset=train_ds,
 eval_dataset=val_ds, compute_metrics=compute_metrics)
 trainer.train

 metrics = trainer.evaluate
 print(f"Finetune {model_name}: val acc = {metrics['eval_accuracy']:.4f}")
 return model, tokenizer, metrics
```

## 3. Few-shot 

```python
def prototypical_network(support_X, support_y, query_X,
 feature_extractor=None):
 """
 Prototypical Network — Few-shot classification。

 Parameters:
 support_X: np.ndarray — features
 support_y: np.ndarray — label
 query_X: np.ndarray — features
 feature_extractor: callable | None — featuresextraction
 """
 if feature_extractor is not None:
 support_emb = feature_extractor(support_X)
 query_emb = feature_extractor(query_X)
 else:
 support_emb = support_X
 query_emb = query_X

 classes = np.unique(support_y)
 prototypes = np.array([
 support_emb[support_y == c].mean(axis=0) for c in classes])

 # 
 dists = np.array([
 np.linalg.norm(query_emb - p, axis=1) for p in prototypes]).T

 predictions = classes[np.argmin(dists, axis=1)]
 confidences = np.exp(-dists.min(axis=1))

 print(f"Few-shot: {len(classes)} classes, "
 f"{len(support_y)} support → {len(query_X)} query")
 return predictions, confidences
```

## 4. 

```python
def knowledge_distillation(teacher, student, train_loader,
 epochs=20, temperature=4.0, alpha=0.7,
 lr=1e-3):
 """
 (Teacher → Student)。

 Parameters:
 teacher: nn.Module — (frozen)
 student: nn.Module — 
 train_loader: DataLoader — data
 epochs: int — number of epochs
 temperature: float — temperature
 alpha: float — soft loss 's
 lr: float — learning rate
 """
 device = torch.device("cuda" if torch.cuda.is_available else "cpu")
 teacher = teacher.to(device).eval
 student = student.to(device)

 optimizer = torch.optim.AdamW(student.parameters, lr=lr)
 ce_loss = nn.CrossEntropyLoss
 kl_loss = nn.KLDivLoss(reduction="batchmean")

 for epoch in range(epochs):
 student.train
 total_loss = 0.0
 for X_batch, y_batch in train_loader:
 X_batch, y_batch = X_batch.to(device), y_batch.to(device)

 with torch.no_grad:
 teacher_logits = teacher(X_batch)

 student_logits = student(X_batch)

 soft_loss = kl_loss(
 nn.functional.log_softmax(student_logits / temperature, dim=1),
 nn.functional.softmax(teacher_logits / temperature, dim=1)
 ) * (temperature ** 2)

 hard_loss = ce_loss(student_logits, y_batch)
 loss = alpha * soft_loss + (1 - alpha) * hard_loss

 optimizer.zero_grad
 loss.backward
 optimizer.step
 total_loss += loss.item

 print(f" Epoch {epoch}: loss = {total_loss / len(train_loader):.4f}")

 print(f"Distillation: T={temperature}, α={alpha}, {epochs} epochs")
 return student
```

---

## Pipeline Integration

```
deep-learning → transfer-learning → active-learning
 (design)  (ratelabel)
 │ │ ↓
 healthcare-ai ───────┘ ensemble-methods
 ( AI) (ensemble)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `ft_model.pt` | tuning | → inference |
| `ft_history.csv` | | → visualization |
| `few_shot_predictions.csv` | Few-shot prediction | → evaluation |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `papers_with_code` | Papers with Code | transfer learningsearch |
