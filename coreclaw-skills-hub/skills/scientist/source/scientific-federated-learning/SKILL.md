---
name: scientific-federated-learning
description: |
 federated learningskill。Flower frameworkby/via FL pipeline
 FedAvg/FedProx/FedOpt min (DP-SGD)
 IID dataminrate。
tu_tools:
 - key: papers_with_code
 name: Papers with Code
 description: federated learningframework
---

# Scientific Federated Learning

typevariancemachine learningfederated learningpipeline is provided。

## When to Use

- multipletissue's datawhen needed
- dataunitsinformationincludingdata ML is performedand
- min forwhen needed
- IID datamin 'sfederated learning is designedand
- rate variance is builtand

---

## Quick Start

## 1. Flower federated learningpipeline

```python
import flwr as fl
import numpy as np
from typing import Dict, List, Tuple, Optional


def create_fl_client(model, train_loader, val_loader,
 device="cpu"):
 """
 Flower generation。

 Parameters:
 model: nn.Module — PyTorch model
 train_loader: DataLoader — training data
 val_loader: DataLoader — validation data
 device: str — "cpu" / "cuda"
 """
 import torch

 class SatoriFlClient(fl.client.NumPyClient):
 def get_parameters(self, config):
 return [val.cpu.numpy
 for val in model.parameters]

 def set_parameters(self, parameters):
 for param, new_val in zip(model.parameters, parameters):
 param.data = torch.tensor(new_val).to(device)

 def fit(self, parameters, config):
 self.set_parameters(parameters)
 model.train
 optimizer = torch.optim.Adam(model.parameters, lr=1e-3)
 criterion = torch.nn.CrossEntropyLoss

 epochs = config.get("local_epochs", 1)
 for _ in range(epochs):
 for X, y in train_loader:
 X, y = X.to(device), y.to(device)
 optimizer.zero_grad
 loss = criterion(model(X), y)
 loss.backward
 optimizer.step

 return self.get_parameters(config), len(train_loader.dataset), {}

 def evaluate(self, parameters, config):
 self.set_parameters(parameters)
 model.eval
 criterion = torch.nn.CrossEntropyLoss
 total_loss, correct, total = 0.0, 0, 0

 with torch.no_grad:
 for X, y in val_loader:
 X, y = X.to(device), y.to(device)
 preds = model(X)
 total_loss += criterion(preds, y).item * len(y)
 correct += (preds.argmax(1) == y).sum.item
 total += len(y)

 return total_loss / total, total, {"accuracy": correct / total}

 return SatoriFlClient


def create_fl_strategy(algorithm="fedavg", min_clients=2,
 fraction_fit=1.0, fraction_evaluate=1.0,
 proximal_mu=0.1):
 """
 federated learning'sselection。

 Parameters:
 algorithm: str — "fedavg" / "fedprox" / "fedopt" / "fedadam"
 min_clients: int — number/count
 fraction_fit: float — rate
 fraction_evaluate: float — evaluationrate
 proximal_mu: float — FedProx term'sintensity
 """
 common = dict(
 min_fit_clients=min_clients,
 min_evaluate_clients=min_clients,
 min_available_clients=min_clients,
 fraction_fit=fraction_fit,
 fraction_evaluate=fraction_evaluate,
 )

 strategies = {
 "fedavg": fl.server.strategy.FedAvg(**common),
 "fedprox": fl.server.strategy.FedProx(
 proximal_mu=proximal_mu, **common),
 "fedadam": fl.server.strategy.FedAdam(
 eta=1e-1, eta_l=1e-1, tau=1e-9, **common),
 }

 strategy = strategies.get(algorithm, strategies["fedavg"])
 print(f"FL Strategy: {algorithm} | min_clients={min_clients}")
 return strategy
```

## 2. min (DP-SGD)

```python
def apply_differential_privacy(model, train_loader,
 target_epsilon=1.0,
 target_delta=1e-5,
 max_grad_norm=1.0,
 noise_multiplier=1.1,
 epochs=10, lr=1e-3):
 """
 Opacus DP-SGD by/viamin。

 Parameters:
 model: nn.Module — PyTorch model
 train_loader: DataLoader — training data
 target_epsilon: float — ε
 target_delta: float — parameters δ
 max_grad_norm: float — gradient
 noise_multiplier: float — number/count σ
 epochs: int — training epochs
 lr: float — learning rate
 """
 import torch
 from opacus import PrivacyEngine

 optimizer = torch.optim.SGD(model.parameters, lr=lr)
 privacy_engine = PrivacyEngine

 model, optimizer, train_loader = privacy_engine.make_private_with_epsilon(
 module=model,
 optimizer=optimizer,
 data_loader=train_loader,
 epochs=epochs,
 target_epsilon=target_epsilon,
 target_delta=target_delta,
 max_grad_norm=max_grad_norm,
 )

 criterion = torch.nn.CrossEntropyLoss
 history = []

 for epoch in range(epochs):
 model.train
 total_loss = 0
 for X, y in train_loader:
 optimizer.zero_grad
 loss = criterion(model(X), y)
 loss.backward
 optimizer.step
 total_loss += loss.item

 epsilon = privacy_engine.get_epsilon(delta=target_delta)
 history.append({"epoch": epoch + 1,
 "loss": total_loss / len(train_loader),
 "epsilon": epsilon})
 print(f"Epoch {epoch+1}: loss={total_loss/len(train_loader):.4f}, "
 f"ε={epsilon:.2f}")

 import pandas as pd
 return pd.DataFrame(history)
```

## 3. IID datamin

```python
def create_non_iid_splits(dataset_labels, n_clients=5,
 alpha=0.5, seed=42):
 """
 Dirichlet distribution's IID datamin。

 Parameters:
 dataset_labels: np.ndarray — alldata's labelsequence
 n_clients: int — number/count
 alpha: float — Dirichlet α (small large)
 seed: int — random seed
 """
 rng = np.random.default_rng(seed)
 n_classes = len(np.unique(dataset_labels))
 client_indices = [[] for _ in range(n_clients)]

 for c in range(n_classes):
 class_idx = np.where(dataset_labels == c)[0]
 proportions = rng.dirichlet(np.repeat(alpha, n_clients))
 split_points = (np.cumsum(proportions) * len(class_idx)).astype(int)
 splits = np.split(class_idx, split_points[:-1])
 for i, split in enumerate(splits):
 client_indices[i].extend(split.tolist)

 # distributionsummary
 for i, indices in enumerate(client_indices):
 labels = dataset_labels[indices]
 unique, counts = np.unique(labels, return_counts=True)
 dist = dict(zip(unique.tolist, counts.tolist))
 print(f"Client {i}: {len(indices)} samples, dist={dist}")

 return client_indices
```

---

## Pipeline Integration

```
[items] → federated-learning → model-monitoring
 (federated learning) 
 │
 deep-learning ← transfer-learning
 ( NN) (transfer learning)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `fl_strategy_config.json` | FL settings | → |
| `dp_training_history.csv` | DP | → model-monitoring |
| `client_splits.json` | IID mininformation | → FL |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `papers_with_code` | Papers with Code | federated learningframework |
