---
name: scientific-multi-task-learning
description: |
 Multi-task learning skill. Shared representation learning, task-specific heads, gradient balancing, auxiliary task selection, and multi-task model evaluation.
tu_tools:
 - key: openml
 name: OpenML
 description: taskdatasetreference
---

# Scientific Multi-Task Learning

multiple's task、table utilizing
eachtask's generalizationpipeline is provided。

## When to Use

- multiple's predictiontaskwhen needed
- table datarate and
- task + task's configurationwhen needed
- task's gradientwhen needed
- outputregressionclassification is designedand

---

## Quick Start

## 1. Hard Parameter Sharing MTL

```python
import torch
import torch.nn as nn
from typing import Dict, List, Tuple


class HardSharingMTL(nn.Module):
 """
 Hard Parameter Sharing task。

 encoder + task'sconfiguration。
 """

 def __init__(self, input_dim, shared_dims, task_configs):
 """
 Parameters:
 input_dim: int — input
 shared_dims: list[int] — 's number/count
 task_configs: dict — {task_name: {"output_dim": int, "head_dims": [int]}}
 """
 super.__init__

 # encoder
 layers = []
 in_d = input_dim
 for d in shared_dims:
 layers.extend([nn.Linear(in_d, d), nn.ReLU,
 nn.BatchNorm1d(d), nn.Dropout(0.2)])
 in_d = d
 self.shared_encoder = nn.Sequential(*layers)

 # task
 self.task_heads = nn.ModuleDict
 for name, config in task_configs.items:
 head_layers = []
 h_in = in_d
 for h_d in config.get("head_dims", [64]):
 head_layers.extend([nn.Linear(h_in, h_d), nn.ReLU])
 h_in = h_d
 head_layers.append(nn.Linear(h_in, config["output_dim"]))
 self.task_heads[name] = nn.Sequential(*head_layers)

 def forward(self, x):
 shared = self.shared_encoder(x)
 return {name: head(shared) for name, head in self.task_heads.items}


def train_mtl_model(model, train_loader, task_losses,
 task_weights=None, epochs=50,
 lr=1e-3, device="cpu"):
 """
 MTL 's 。

 Parameters:
 model: HardSharingMTL — MTL 
 train_loader: DataLoader — {task_name: (X, y)} batch
 task_losses: dict — {task_name: loss_fn}
 task_weights: dict | None — {task_name: float} task
 epochs: int — training epochs
 lr: float — learning rate
 device: str — device
 """
 import pandas as pd

 if task_weights is None:
 task_weights = {name: 1.0 for name in task_losses}

 model.to(device)
 optimizer = torch.optim.Adam(model.parameters, lr=lr)
 history = []

 for epoch in range(epochs):
 model.train
 epoch_losses = {name: 0.0 for name in task_losses}

 for batch in train_loader:
 X = batch["X"].to(device)
 outputs = model(X)
 optimizer.zero_grad

 total_loss = 0
 for name, loss_fn in task_losses.items:
 y = batch[name].to(device)
 task_loss = loss_fn(outputs[name], y)
 total_loss += task_weights[name] * task_loss
 epoch_losses[name] += task_loss.item

 total_loss.backward
 optimizer.step

 record = {"epoch": epoch + 1}
 for name in task_losses:
 record[f"loss_{name}"] = epoch_losses[name] / len(train_loader)
 history.append(record)

 if (epoch + 1) % 10 == 0:
 losses_str = " | ".join(
 f"{n}={epoch_losses[n]/len(train_loader):.4f}"
 for n in task_losses)
 print(f"Epoch {epoch+1}: {losses_str}")

 return pd.DataFrame(history)
```

## 2. GradNorm — task

```python
def gradnorm_balance(model, task_losses, train_loader,
 alpha=1.5, epochs=50, lr=1e-3, device="cpu"):
 """
 GradNorm by/viatask。

 Parameters:
 model: HardSharingMTL — MTL 
 task_losses: dict — {task_name: loss_fn}
 train_loader: DataLoader
 alpha: float — GradNorm degreeparameters
 epochs: int — 
 lr: float — learning rate
 device: str — device
 """
 import pandas as pd

 task_names = list(task_losses.keys)
 n_tasks = len(task_names)
 log_weights = torch.zeros(n_tasks, requires_grad=True, device=device)

 model.to(device)
 optimizer = torch.optim.Adam(model.parameters, lr=lr)
 weight_optimizer = torch.optim.Adam([log_weights], lr=0.025)

 initial_losses = None
 history = []

 for epoch in range(epochs):
 model.train
 epoch_losses = {n: 0.0 for n in task_names}

 for batch in train_loader:
 X = batch["X"].to(device)
 outputs = model(X)

 weights = torch.softmax(log_weights, dim=0) * n_tasks
 losses = []
 for i, name in enumerate(task_names):
 y = batch[name].to(device)
 task_loss = task_losses[name](outputs[name], y)
 losses.append(task_loss)
 epoch_losses[name] += task_loss.item

 if initial_losses is None:
 initial_losses = [l.item for l in losses]

 total_loss = sum(w * l for w, l in zip(weights, losses))

 optimizer.zero_grad
 weight_optimizer.zero_grad
 total_loss.backward(retain_graph=True)

 # GradNorm 
 shared_params = list(model.shared_encoder.parameters)
 norms = []
 for l in losses:
 g = torch.autograd.grad(l, shared_params[-1],
 retain_graph=True)[0]
 norms.append(torch.norm(g))

 avg_norm = torch.stack(norms).mean
 loss_ratios = torch.tensor(
 [l.item / il for l, il in
 zip(losses, initial_losses)], device=device)
 relative_inv = loss_ratios / loss_ratios.mean
 target_norms = avg_norm * (relative_inv ** alpha)

 gradnorm_loss = sum(
 torch.abs(n - t) for n, t in
 zip(norms, target_norms))
 gradnorm_loss.backward

 optimizer.step
 weight_optimizer.step

 record = {"epoch": epoch + 1}
 for i, name in enumerate(task_names):
 record[f"loss_{name}"] = epoch_losses[name] / len(train_loader)
 record[f"weight_{name}"] = (
 torch.softmax(log_weights, 0) * n_tasks)[i].item
 history.append(record)

 return pd.DataFrame(history)
```

---

## Pipeline Integration

```
[multipletaskdefinition] → multi-task-learning → feature-importance
 (table) (features)
 │
 deep-learning ← transfer-learning
 ( NN) (transfer learning)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `mtl_model.pt` | MTL | → inference |
| `mtl_history.csv` | task | → visualization |
| `gradnorm_weights.csv` | task | → min |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | taskdatasetreference |

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
