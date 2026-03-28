---
name: scientific-neural-architecture-search
description: |
 search/exploration (NAS) skill。DARTS minpossible NAS
 Optuna NAS integrationratenetworkdesignsearch/explorationdefinition
 Pareto optimization (degree vs FLOPS)。
tu_tools:
 - key: papers_with_code
 name: Papers with Code
 description: NAS search/explorationsearch
---

# Scientific Neural Architecture Search

networkstructure'sautomatedsearch/explorationoptimizationpipeline is provided。

## When to Use

- NN automatedoptimizationwhen needed
- degree and calculation's Pareto Optimal solution is exploredand
- search/explorationdefinitionratestructuresearch/exploration is performedand
- DARTS system's minpossible NAS implementationwhen needed
- rate automatedwhen needed

---

## Quick Start

## 1. Optuna NAS — networkstructuresearch/exploration

```python
import optuna
import torch
import torch.nn as nn
from typing import Dict, Any


def optuna_nas(train_loader, val_loader, search_space=None,
 n_trials=50, n_epochs=10, device="cpu",
 direction="maximize", metric="accuracy"):
 """
 Optuna by/viasearch/exploration。

 Parameters:
 train_loader: DataLoader — training data
 val_loader: DataLoader — validation data
 search_space: dict | None — customsearch/exploration
 n_trials: int — number of trials
 n_epochs: int — each'straining epochs
 device: str — "cpu" / "cuda"
 direction: str — "maximize" / "minimize"
 metric: str — optimization
 """
 input_dim = next(iter(train_loader))[0].shape[1]
 n_classes = len(torch.unique(
 torch.cat([y for _, y in train_loader])))

 def build_model(trial):
 n_layers = trial.suggest_int("n_layers", 1, 5)
 layers = []
 in_features = input_dim

 for i in range(n_layers):
 out_features = trial.suggest_int(
 f"n_units_l{i}", 16, 512, log=True)
 layers.append(nn.Linear(in_features, out_features))

 activation = trial.suggest_categorical(
 f"activation_l{i}", ["relu", "gelu", "silu"])
 act_map = {"relu": nn.ReLU, "gelu": nn.GELU,
 "silu": nn.SiLU}
 layers.append(act_map[activation])

 dropout = trial.suggest_float(
 f"dropout_l{i}", 0.0, 0.5)
 if dropout > 0:
 layers.append(nn.Dropout(dropout))

 use_bn = trial.suggest_categorical(
 f"batchnorm_l{i}", [True, False])
 if use_bn:
 layers.append(nn.BatchNorm1d(out_features))

 in_features = out_features

 layers.append(nn.Linear(in_features, n_classes))
 return nn.Sequential(*layers)

 def objective(trial):
 model = build_model(trial).to(device)
 lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
 optimizer_name = trial.suggest_categorical(
 "optimizer", ["Adam", "AdamW", "SGD"])

 opt_cls = getattr(torch.optim, optimizer_name)
 optimizer = opt_cls(model.parameters, lr=lr)
 criterion = nn.CrossEntropyLoss

 for epoch in range(n_epochs):
 model.train
 for X, y in train_loader:
 X, y = X.to(device), y.to(device)
 optimizer.zero_grad
 loss = criterion(model(X), y)
 loss.backward
 optimizer.step

 # 
 model.eval
 correct, total = 0, 0
 with torch.no_grad:
 for X, y in val_loader:
 X, y = X.to(device), y.to(device)
 correct += (model(X).argmax(1) == y).sum.item
 total += len(y)

 trial.report(correct / total, epoch)
 if trial.should_prune:
 raise optuna.TrialPruned

 return correct / total

 study = optuna.create_study(
 direction=direction,
 pruner=optuna.pruners.MedianPruner(n_warmup_steps=3))
 study.optimize(objective, n_trials=n_trials)

 print(f"Best {metric}: {study.best_value:.4f}")
 print(f"Best params: {study.best_params}")
 return study


def nas_pareto_search(train_loader, val_loader,
 n_trials=100, device="cpu"):
 """
 purpose NAS — degree vs 's Pareto optimization。

 Parameters:
 train_loader: DataLoader — training data
 val_loader: DataLoader — validation data
 n_trials: int — number of trials
 device: str — device
 """

 def objective(trial):
 n_layers = trial.suggest_int("n_layers", 1, 4)
 total_params = 0
 in_f = next(iter(train_loader))[0].shape[1]
 n_classes = len(torch.unique(
 torch.cat([y for _, y in val_loader])))

 layers = []
 for i in range(n_layers):
 out_f = trial.suggest_int(f"units_{i}", 8, 256, log=True)
 layers.append(nn.Linear(in_f, out_f))
 layers.append(nn.ReLU)
 total_params += in_f * out_f + out_f
 in_f = out_f
 layers.append(nn.Linear(in_f, n_classes))
 total_params += in_f * n_classes + n_classes

 model = nn.Sequential(*layers).to(device)
 optimizer = torch.optim.Adam(model.parameters, lr=1e-3)
 criterion = nn.CrossEntropyLoss

 for _ in range(5):
 model.train
 for X, y in train_loader:
 X, y = X.to(device), y.to(device)
 optimizer.zero_grad
 criterion(model(X), y).backward
 optimizer.step

 model.eval
 correct, total = 0, 0
 with torch.no_grad:
 for X, y in val_loader:
 X, y = X.to(device), y.to(device)
 correct += (model(X).argmax(1) == y).sum.item
 total += len(y)

 return correct / total, total_params

 study = optuna.create_study(
 directions=["maximize", "minimize"])
 study.optimize(objective, n_trials=n_trials)

 print(f"Pareto front: {len(study.best_trials)} solutions")
 return study
```

---

## Pipeline Integration

```
[taskdefinition] → neural-architecture-search → deep-learning
 (structuresearch/exploration) (papers)
 │
 automl ← ensemble-methods
 (HPO) (ensemble)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `nas_study.pkl` | Optuna Study | → structureextraction |
| `pareto_front.csv` | Pareto Optimal solutiongroup | → selection |
| `best_architecture.json` | | → deep-learning |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `papers_with_code` | Papers with Code | NAS search/explorationsearch |
