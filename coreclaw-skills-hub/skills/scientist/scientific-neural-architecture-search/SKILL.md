---
name: scientific-neural-architecture-search
description: |
 Neural architecture search (NAS) skill. Architecture space definition, search strategy implementation, performance estimation, and efficient NAS methods (DARTS/ENAS).
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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
