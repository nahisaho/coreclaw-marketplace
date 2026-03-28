---
name: scientific-streaming-analytics
description: |
 Streaming analytics skill. Real-time data processing, stream windowing, online learning, event-driven analysis, and streaming aggregation pipelines.
---

# Scientific Streaming Analytics

datafor/againstanomaly detection
pipeline is provided。

## When to Use

- dataenvironment's and
- when needed
- anomaly detectionimplementationwhen needed
- supportwhen needed
- min amountcalculationwhen needed

---

## Quick Start

## 1. River 

```python
from river import (
 compose, preprocessing, linear_model, metrics,
 tree, ensemble, drift)
import pandas as pd
import numpy as np


def online_learning_pipeline(stream_data, model_type="ht",
 target_col="y",
 feature_cols=None):
 """
 River pipeline。

 Parameters:
 stream_data: iterable — (X_dict, y) 's or DataFrame
 model_type: str — "ht" (Hoeffding Tree) / "lr" / "arf"
 target_col: str — targetnumber/count
 feature_cols: list[str] | None — featurescolumn
 """
 models = {
 "ht": tree.HoeffdingTreeClassifier,
 "lr": compose.Pipeline(
 preprocessing.StandardScaler,
 linear_model.LogisticRegression),
 "arf": ensemble.AdaptiveRandomForestClassifier(
 n_models=10, seed=42),
 }
 model = models.get(model_type, models["ht"])
 metric = metrics.Accuracy
 history = []

 if isinstance(stream_data, pd.DataFrame):
 if feature_cols is None:
 feature_cols = [c for c in stream_data.columns
 if c != target_col]
 iterator = (
 (row[feature_cols].to_dict, row[target_col])
 for _, row in stream_data.iterrows)
 else:
 iterator = stream_data

 for i, (x, y) in enumerate(iterator):
 y_pred = model.predict_one(x)
 if y_pred is not None:
 metric.update(y, y_pred)
 model.learn_one(x, y)

 if (i + 1) % 100 == 0:
 history.append({
 "step": i + 1,
 "accuracy": metric.get,
 })

 print(f"Online {model_type}: {metric}")
 return model, pd.DataFrame(history)
```

## 2. anomaly detection

```python
def streaming_anomaly_detection(stream_data, window_size=100,
 threshold_sigma=3.0,
 method="zscore"):
 """
 anomaly detection。

 Parameters:
 stream_data: iterable — number/countvalue
 window_size: int — 
 threshold_sigma: float — 's σ threshold
 method: str — "zscore" / "iqr" / "ewma"
 """
 from collections import deque

 window = deque(maxlen=window_size)
 results = []
 ewma_mean = None
 ewma_var = None
 alpha = 2.0 / (window_size + 1)

 for i, value in enumerate(stream_data):
 is_anomaly = False

 if method == "zscore" and len(window) >= 10:
 mean = np.mean(window)
 std = np.std(window) + 1e-10
 z = abs(value - mean) / std
 is_anomaly = z > threshold_sigma

 elif method == "iqr" and len(window) >= 10:
 q1, q3 = np.percentile(window, [25, 75])
 iqr = q3 - q1
 lower = q1 - 1.5 * iqr
 upper = q3 + 1.5 * iqr
 is_anomaly = value < lower or value > upper

 elif method == "ewma":
 if ewma_mean is None:
 ewma_mean = value
 ewma_var = 0
 else:
 ewma_mean = alpha * value + (1 - alpha) * ewma_mean
 ewma_var = alpha * (value - ewma_mean) ** 2 + \
 (1 - alpha) * ewma_var
 ewma_std = np.sqrt(ewma_var) + 1e-10
 is_anomaly = abs(value - ewma_mean) / ewma_std > threshold_sigma

 window.append(value)
 results.append({
 "step": i, "value": value,
 "is_anomaly": is_anomaly,
 })

 df = pd.DataFrame(results)
 n_anomalies = df["is_anomaly"].sum
 print(f"Streaming anomaly ({method}): "
 f"{n_anomalies}/{len(df)} anomalies detected "
 f"({n_anomalies/len(df):.1%})")
 return df
```

## 3. 

```python
def concept_drift_detection(stream_data, target_col="y",
 feature_cols=None,
 detector_type="adwin"):
 """
 。

 Parameters:
 stream_data: pd.DataFrame — data
 target_col: str — targetnumber/count
 feature_cols: list[str] | None — featurescolumn
 detector_type: str — "adwin" / "ddm" / "eddm"
 """
 detectors = {
 "adwin": drift.ADWIN(delta=0.002),
 "ddm": drift.DDM(min_num_instances=30),
 "eddm": drift.EDDM,
 }
 detector = detectors.get(detector_type, detectors["adwin"])

 model = tree.HoeffdingTreeClassifier
 metric = metrics.Accuracy
 drift_points = []

 if feature_cols is None:
 feature_cols = [c for c in stream_data.columns
 if c != target_col]

 for i, (_, row) in enumerate(stream_data.iterrows):
 x = row[feature_cols].to_dict
 y = row[target_col]
 y_pred = model.predict_one(x)

 if y_pred is not None:
 is_correct = int(y_pred == y)
 metric.update(y, y_pred)
 detector.update(is_correct)

 if detector.drift_detected:
 drift_points.append({
 "step": i,
 "accuracy_at_drift": metric.get,
 })
 print(f"⚠ Drift at step {i}, acc={metric.get:.3f}")

 model.learn_one(x, y)

 print(f"Total drifts: {len(drift_points)}")
 return pd.DataFrame(drift_points)
```

---

## Pipeline Integration

```
[data] → streaming-analytics → model-monitoring
  
 │
 anomaly-detection ← data-profiling
 (batchanomaly detection) (data)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `online_model.pkl` | | → inference |
| `stream_anomalies.csv` | anomaly detectionresults | → alerting |
| `drift_report.csv` | point | → model-monitoring |

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
