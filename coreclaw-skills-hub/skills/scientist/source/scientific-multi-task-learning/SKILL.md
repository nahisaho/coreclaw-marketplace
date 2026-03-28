---
name: scientific-multi-task-learning
description: |
 taskskill。Hard/Soft Parameter Sharing
 GradNorm gradientnormalizationPCGrad gradient
 tasktaskdesign。
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
