---
name: scientific-uncertainty-quantification
description: |
 Uncertainty quantification skill. Aleatory/epistemic uncertainty estimation, ensemble uncertainty, conformal prediction, calibration, and uncertainty propagation.
---

# Scientific Uncertainty Quantification

machine learningprediction's uncertainty amount、prediction interval and 
proofreadingrate is provided。

## When to Use

- prediction's degree amountwhen needed
- prediction intervalconfidence interval is estimatedand
- proofreadingcurveline 's rate is evaluatedand
- Conformal Prediction distribution's and
- MC Dropout Bayesianinferencewhen needed
- / uncertainty minwhen needed

---

## Quick Start

## 1. Conformal Prediction

```python
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator


def conformal_prediction(model, X_calib, y_calib, X_test,
 alpha=0.1, method="quantile"):
 """
 Conformal Prediction — distribution'sprediction interval。

 Parameters:
 model: BaseEstimator — 
 X_calib: np.ndarray — proofreadingdatafeatures
 y_calib: np.ndarray — proofreadingdataobjective variable
 X_test: np.ndarray — test datafeatures
 alpha: float — significance level (1-α )
 method: str — "quantile" / "cqr" (Conformalized Quantile Regression)
 """
 # classification or regressionautomated
 if hasattr(model, "predict_proba"):
 return _conformal_classification(model, X_calib, y_calib, X_test, alpha)
 else:
 return _conformal_regression(model, X_calib, y_calib, X_test, alpha, method)


def _conformal_regression(model, X_calib, y_calib, X_test, alpha, method):
 if method == "cqr":
 # Conformalized Quantile Regression
 q_low = model.predict_quantile(X_calib, quantile=alpha/2)
 q_high = model.predict_quantile(X_calib, quantile=1-alpha/2)
 scores = np.maximum(q_low - y_calib, y_calib - q_high)
 q = np.quantile(scores, (1-alpha)*(1+1/len(scores)))
 # Apply to test
 q_low_test = model.predict_quantile(X_test, quantile=alpha/2)
 q_high_test = model.predict_quantile(X_test, quantile=1-alpha/2)
 preds_test = model.predict(X_test)
 lower = q_low_test - q
 upper = q_high_test + q
 else:
 preds_calib = model.predict(X_calib)
 residuals = np.abs(y_calib - preds_calib)

 # (1-α)(1 + 1/n) minpoint
 n = len(residuals)
 q = np.quantile(residuals, np.ceil((1 - alpha) * (n + 1)) / n)

 preds_test = model.predict(X_test)
 lower = preds_test - q
 upper = preds_test + q

 coverage = None
 width = np.mean(upper - lower)

 result_df = pd.DataFrame({
 "prediction": preds_test,
 "lower": lower,
 "upper": upper,
 "interval_width": upper - lower
 })

 print(f"Conformal Prediction ({method}, α={alpha}): "
 f"mean width = {width:.4f}")
 return {"intervals": result_df, "coverage": coverage, "mean_width": width}


def _conformal_classification(model, X_calib, y_calib, X_test, alpha):
 proba_calib = model.predict_proba(X_calib)
 n_classes = proba_calib.shape[1]

 # Non-conformity score = 1 - 's rate
 scores = 1 - proba_calib[np.arange(len(y_calib)), y_calib]
 n = len(scores)
 q = np.quantile(scores, np.ceil((1 - alpha) * (n + 1)) / n)

 proba_test = model.predict_proba(X_test)
 prediction_sets = []
 for i in range(len(X_test)):
 pred_set = np.where(proba_test[i] >= 1 - q)[0].tolist
 prediction_sets.append(pred_set)

 avg_size = np.mean([len(s) for s in prediction_sets])
 print(f"Conformal Classification (α={alpha}): "
 f"avg set size = {avg_size:.2f}")
 return prediction_sets
```

## 2. MC Dropout

```python
def mc_dropout_predict(model, X, n_forward=100, dropout_rate=0.1):
 """
 MC Dropout — Bayesianinference。

 Parameters:
 model: nn.Module — dropout
 X: torch.Tensor — input tensor
 n_forward: int — timesnumber/count
 dropout_rate: float — dropoutrate
 """
 import torch
 import torch.nn.functional as F

 has_dropout = any(isinstance(m, torch.nn.Dropout) for m in model.modules)

 model.train # Dropout effective

 # Wrap model to apply dropout if not built-in
 class _MCDropoutWrapper(torch.nn.Module):
 def __init__(self, base_model, rate):
 super.__init__
 self.base_model = base_model
 self.rate = rate
 def forward(self, x):
 out = self.base_model(x)
 return F.dropout(out, p=self.rate, training=True)

 forward_model = model if has_dropout else _MCDropoutWrapper(model, dropout_rate)

 predictions = []
 with torch.no_grad:
 for _ in range(n_forward):
 pred = forward_model(X)
 if pred.dim > 1 and pred.shape[1] > 1:
 pred = torch.softmax(pred, dim=1)
 predictions.append(pred.cpu.numpy)

 model.eval # Restore eval mode

 predictions = np.array(predictions) # (n_forward, n_samples,...)
 mean_pred = predictions.mean(axis=0)
 std_pred = predictions.std(axis=0)

 # uncertainty: prediction's items
 epistemic = std_pred
 # classificationcase: prediction
 if mean_pred.ndim == 2 and mean_pred.shape[1] > 1:
 entropy = -np.sum(mean_pred * np.log(mean_pred + 1e-10), axis=1)
 else:
 entropy = None

 print(f"MC Dropout: {n_forward} passes, "
 f"mean epistemic unc = {epistemic.mean:.4f}")
 return {"mean": mean_pred, "std": std_pred,
 "epistemic": epistemic, "entropy": entropy}
```

## 3. ensembleuncertainty

```python
def deep_ensemble_uncertainty(models, X, task="classification"):
 """
 ensembleuncertainty (Lakshminarayanan+ 2017)。

 Parameters:
 models: list[nn.Module] — ensemble
 X: torch.Tensor — input tensor
 task: str — "classification" / "regression"
 """
 import torch

 all_preds = []
 for m in models:
 m.eval
 with torch.no_grad:
 pred = m(X)
 if task == "classification":
 pred = torch.softmax(pred, dim=1)
 all_preds.append(pred.cpu.numpy)

 all_preds = np.array(all_preds) # (M, N,...)

 # meanprediction
 mean_pred = all_preds.mean(axis=0)

 if task == "classification":
 # : mean
 aleatoric = np.mean([
 -np.sum(p * np.log(p + 1e-10), axis=1) for p in all_preds
 ], axis=0)
 # all
 total_entropy = -np.sum(mean_pred * np.log(mean_pred + 1e-10), axis=1)
 # = all - (phaseinformationamount)
 epistemic = total_entropy - aleatoric
 else:
 # regression: variancedegradation
 aleatoric = np.zeros(len(X)) # each'svariance 
 epistemic = all_preds.var(axis=0).squeeze
 total_entropy = None

 result = {
 "mean_prediction": mean_pred,
 "aleatoric": aleatoric,
 "epistemic": epistemic,
 "total_uncertainty": (aleatoric + epistemic) if task == "regression" else total_entropy
 }

 print(f"Deep Ensemble ({len(models)} models): "
 f"epistemic={epistemic.mean:.4f}, "
 f"aleatoric={aleatoric.mean:.4f}")
 return result
```

## 4. Calibration evaluation

```python
def calibration_analysis(y_true, y_proba, n_bins=10):
 """
 proofreadingcurveline andECE (Expected Calibration Error) calculation。

 Parameters:
 y_true: np.ndarray — 'slabel (0/1)
 y_proba: np.ndarray — predictionrate
 n_bins: int — number/count
 """
 import matplotlib.pyplot as plt
 from sklearn.calibration import calibration_curve

 # proofreadingcurveline
 frac_pos, mean_pred = calibration_curve(
 y_true, y_proba, n_bins=n_bins, strategy="uniform")

 # ECE
 bin_edges = np.linspace(0, 1, n_bins + 1)
 ece = 0.0
 bin_stats = []
 for i in range(n_bins):
 mask = (y_proba >= bin_edges[i]) & (y_proba < bin_edges[i + 1])
 if mask.sum == 0:
 continue
 bin_acc = y_true[mask].mean
 bin_conf = y_proba[mask].mean
 bin_count = mask.sum
 ece += (bin_count / len(y_true)) * abs(bin_acc - bin_conf)
 bin_stats.append({
 "bin": f"[{bin_edges[i]:.1f}, {bin_edges[i+1]:.1f})",
 "count": int(bin_count),
 "accuracy": bin_acc,
 "confidence": bin_conf,
 "gap": abs(bin_acc - bin_conf)
 })

 # visualization
 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

 # proofreadingcurveline
 ax1.plot([0, 1], [0, 1], "k--", label="Perfect calibration")
 ax1.plot(mean_pred, frac_pos, "o-", label=f"Model (ECE={ece:.4f})")
 ax1.set_xlabel("Mean predicted probability")
 ax1.set_ylabel("Fraction of positives")
 ax1.set_title("Calibration Curve")
 ax1.legend

 # degreehistogram
 ax2.hist(y_proba, bins=n_bins, edgecolor="black", alpha=0.7)
 ax2.set_xlabel("Predicted probability")
 ax2.set_ylabel("Count")
 ax2.set_title("Confidence Histogram")

 plt.tight_layout
 plt.savefig("calibration_analysis.png", dpi=150, bbox_inches="tight")
 plt.close

 stats_df = pd.DataFrame(bin_stats)
 print(f"Calibration: ECE = {ece:.4f}, {n_bins} bins")
 return {"ece": ece, "bin_stats": stats_df, "fig": "calibration_analysis.png"}
```

---

## Pipeline Integration

```
ensemble-methods → uncertainty-quantification → explainable-ai
 (ensemble) (uncertaintyamount) (possible AI)
 │ │ ↓
 active-learning ──────────┘ bayesian-statistics
 (active learning) (Bayesian)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `conformal_intervals.csv` | Conformal prediction interval | → reporting |
| `mc_dropout_uncertainty.csv` | MC Dropout uncertainty | → active-learning |
| `calibration_analysis.png` | proofreadingcurveline | → presentation |
| `uncertainty_decomposition.json` | minresults | → explainable-ai |

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
