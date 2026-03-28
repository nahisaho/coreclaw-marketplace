---
name: scientific-federated-learning
description: |
 federated learningskill。Flower frameworkby/via FL pipeline
 FedAvg/FedProx/FedOpt min (DP-SGD)
 IID dataminrate。
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
