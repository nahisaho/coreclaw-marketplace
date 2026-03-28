---
name: scientific-anomaly-detection
description: |
 Anomaly detection skill. Isolation Forest, LOF, One-Class SVM, autoencoders, statistical control charts, time-series anomaly detection, and multivariate outlier analysis.
---

# Scientific Anomaly Detection

datainvaluevalue's and
 (SPC) pipeline is provided。

## When to Use

- experimentdata's valuewhen needed
- process's (SPC) when needed
- amountdatawhen needed
- Autoencoder when needed
- 's thresholdoptimizationwhen needed
- multiplemethod'sensembleanomaly detection when needed

---

## Quick Start

## 1. anomaly detectionensemble

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


def anomaly_detection_ensemble(X, contamination=0.05,
 methods=None, threshold_vote=2):
 """
 multiplemethodensembleanomaly detection。

 Parameters:
 X: np.ndarray | pd.DataFrame — input data
 contamination: float — rate
 methods: list[str] | None — formethod ("iforest", "lof", "ocsvm")
 threshold_vote: int — number/count (number/count)
 """
 if methods is None:
 methods = ["iforest", "lof", "ocsvm"]

 if isinstance(X, pd.DataFrame):
 feature_names = X.columns.tolist
 X_arr = X.values
 else:
 feature_names = [f"f{i}" for i in range(X.shape[1])]
 X_arr = X

 scaler = StandardScaler
 X_scaled = scaler.fit_transform(X_arr)

 results = {}
 predictions = {}

 for method in methods:
 if method == "iforest":
 model = IsolationForest(
 contamination=contamination, random_state=42, n_jobs=-1)
 preds = model.fit_predict(X_scaled)
 scores = -model.score_samples(X_scaled)
 elif method == "lof":
 model = LocalOutlierFactor(
 n_neighbors=20, contamination=contamination)
 preds = model.fit_predict(X_scaled)
 scores = -model.negative_outlier_factor_
 elif method == "ocsvm":
 model = OneClassSVM(kernel="rbf", nu=contamination)
 preds = model.fit_predict(X_scaled)
 scores = -model.decision_function(X_scaled)
 else:
 continue

 is_anomaly = (preds == -1).astype(int)
 predictions[method] = is_anomaly
 results[method] = {
 "n_anomalies": int(is_anomaly.sum),
 "scores": scores
 }

 # ensemblenumber/count
 vote_matrix = np.column_stack(list(predictions.values))
 ensemble_votes = vote_matrix.sum(axis=1)
 ensemble_anomaly = (ensemble_votes >= threshold_vote).astype(int)

 result_df = pd.DataFrame(X_arr, columns=feature_names)
 for method, preds in predictions.items:
 result_df[f"anomaly_{method}"] = preds
 result_df["ensemble_votes"] = ensemble_votes
 result_df["is_anomaly"] = ensemble_anomaly

 n_ens = ensemble_anomaly.sum
 print(f"Anomaly Ensemble ({len(methods)} methods, vote≥{threshold_vote}): "
 f"{n_ens}/{len(X_arr)} anomalies ({n_ens/len(X_arr)*100:.1f}%)")

 for m, r in results.items:
 print(f" {m}: {r['n_anomalies']} anomalies")

 return result_df, results
```

## 2. Autoencoder anomaly detection

```python
def autoencoder_anomaly(X, encoding_dim=8, epochs=100,
 threshold_percentile=95):
 """
 Autoencoder anomaly detection。

 Parameters:
 X: np.ndarray — input data (data)
 encoding_dim: int — number/count
 epochs: int — training epochs
 threshold_percentile: float — configuration's threshold
 """
 import torch
 import torch.nn as nn
 from torch.utils.data import DataLoader, TensorDataset

 scaler = StandardScaler
 X_scaled = scaler.fit_transform(X)
 n_features = X_scaled.shape[1]

 # Autoencoder definition
 class AE(nn.Module):
 def __init__(self):
 super.__init__
 self.encoder = nn.Sequential(
 nn.Linear(n_features, 64), nn.ReLU,
 nn.Linear(64, 32), nn.ReLU,
 nn.Linear(32, encoding_dim))
 self.decoder = nn.Sequential(
 nn.Linear(encoding_dim, 32), nn.ReLU,
 nn.Linear(32, 64), nn.ReLU,
 nn.Linear(64, n_features))

 def forward(self, x):
 z = self.encoder(x)
 return self.decoder(z)

 device = torch.device("cuda" if torch.cuda.is_available else "cpu")
 model = AE.to(device)
 optimizer = torch.optim.Adam(model.parameters, lr=1e-3)
 criterion = nn.MSELoss

 X_tensor = torch.FloatTensor(X_scaled).to(device)
 dataset = TensorDataset(X_tensor, X_tensor)
 loader = DataLoader(dataset, batch_size=64, shuffle=True)

 model.train
 for epoch in range(epochs):
 total_loss = 0
 for batch_x, _ in loader:
 optimizer.zero_grad
 recon = model(batch_x)
 loss = criterion(recon, batch_x)
 loss.backward
 optimizer.step
 total_loss += loss.item

 # configuration
 model.eval
 with torch.no_grad:
 recon = model(X_tensor).cpu.numpy

 recon_errors = np.mean((X_scaled - recon) ** 2, axis=1)
 threshold = np.percentile(recon_errors, threshold_percentile)
 is_anomaly = (recon_errors > threshold).astype(int)

 print(f"Autoencoder Anomaly: threshold={threshold:.4f} (P{threshold_percentile}), "
 f"{is_anomaly.sum} anomalies")
 return {"reconstruction_error": recon_errors, "threshold": threshold,
 "is_anomaly": is_anomaly, "model": model}
```

## 3. (SPC)

```python
def spc_control_chart(data, column, subgroup_size=1,
 chart_type="individuals"):
 """
 SPC figure (X-bar, R, Individuals-MR)。

 Parameters:
 data: pd.DataFrame | pd.Series — time series data
 column: str — column
 subgroup_size: int — loop
 chart_type: str — "individuals" / "xbar_r" / "cusum"
 """
 import matplotlib.pyplot as plt

 if isinstance(data, pd.DataFrame):
 values = data[column].values
 else:
 values = data.values

 if chart_type == "individuals":
 x_bar = np.mean(values)
 mr = np.abs(np.diff(values))
 mr_bar = np.mean(mr)
 d2 = 1.128 # d2 for n=2

 ucl = x_bar + 3 * (mr_bar / d2)
 lcl = x_bar - 3 * (mr_bar / d2)

 fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

 # Individuals chart
 ax1.plot(values, "b-o", markersize=3)
 ax1.axhline(x_bar, color="g", linestyle="-", label=f"CL={x_bar:.3f}")
 ax1.axhline(ucl, color="r", linestyle="--", label=f"UCL={ucl:.3f}")
 ax1.axhline(lcl, color="r", linestyle="--", label=f"LCL={lcl:.3f}")

 # OOC points
 ooc = np.where((values > ucl) | (values < lcl))[0]
 if len(ooc) > 0:
 ax1.scatter(ooc, values[ooc], c="red", s=50, zorder=5,
 label=f"OOC ({len(ooc)})")
 ax1.set_title("Individuals Chart")
 ax1.legend(fontsize=8)

 # Moving Range chart
 mr_ucl = 3.267 * mr_bar
 ax2.plot(mr, "b-o", markersize=3)
 ax2.axhline(mr_bar, color="g", linestyle="-")
 ax2.axhline(mr_ucl, color="r", linestyle="--")
 ax2.set_title("Moving Range Chart")

 plt.tight_layout
 path = "spc_control_chart.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 print(f"SPC Individuals: CL={x_bar:.3f}, UCL={ucl:.3f}, "
 f"LCL={lcl:.3f}, OOC={len(ooc)}")
 return {"cl": x_bar, "ucl": ucl, "lcl": lcl,
 "ooc_indices": ooc, "fig": path}

 elif chart_type == "cusum":
 target = np.mean(values)
 se = np.std(values)
 k = 0.5 * se
 h = 5 * se

 cusum_pos = np.zeros(len(values))
 cusum_neg = np.zeros(len(values))

 for i in range(1, len(values)):
 cusum_pos[i] = max(0, cusum_pos[i-1] + (values[i] - target) - k)
 cusum_neg[i] = min(0, cusum_neg[i-1] + (values[i] - target) + k)

 fig, ax = plt.subplots(figsize=(12, 5))
 ax.plot(cusum_pos, "b-", label="CUSUM+")
 ax.plot(cusum_neg, "r-", label="CUSUM-")
 ax.axhline(h, color="b", linestyle="--", alpha=0.5)
 ax.axhline(-h, color="r", linestyle="--", alpha=0.5)
 ax.set_title("CUSUM Control Chart")
 ax.legend

 path = "cusum_chart.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 print(f"CUSUM: target={target:.3f}, k={k:.3f}, h={h:.3f}")
 return {"target": target, "k": k, "h": h,
 "cusum_pos": cusum_pos, "cusum_neg": cusum_neg, "fig": path}
```

---

## Pipeline Integration

```
eda-correlation → anomaly-detection → ml-classification
 (search/explorationanalysis) (value) 
 │ │ ↓
 data-profiling ────────┘ model-monitoring
 (data) 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `anomaly_ensemble.csv` | ensembleanomaly detectionresults | → EDA |
| `autoencoder_anomaly.json` | AE | → reporting |
| `spc_control_chart.png` | SPC figure | → process-optimization |

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

### Eval Criteria (Data Analysis)

Before execution, define:
- [ ] **Input schema**: column names, types, expected ranges
- [ ] **Output schema**: expected result shape, key metrics to produce
- [ ] **Statistical validity**: significance level (alpha), power target, effect size threshold
- [ ] **Reproducibility**: random seed set, deterministic pipeline

#### Pass Criteria
- All statistical tests report p-values and confidence intervals
- Effect sizes reported alongside significance
- Multiple comparison corrections applied when > 2 tests
- Missing data handling documented (method + % impacted)
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
