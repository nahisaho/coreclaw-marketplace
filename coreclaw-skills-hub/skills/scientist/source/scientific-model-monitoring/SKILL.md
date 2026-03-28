---
name: scientific-model-monitoring
description: |
 MLOps skill。data (Evidently/NannyML)
 features
 A/B testingregistry。
tu_tools:
 - key: openml
 name: OpenML
 description: 
---

# Scientific Model Monitoring

papersenvironment's ML pipeline providing、
data.

## When to Use

- 's predictionwhen needed
- data (covariates) when needed
- (P(Y|X) 's) when needed
- A/B testing is comparedand
- featuresdistribution'swhen needed
- 's automatedsettingswhen needed

---

## Quick Start

## 1. data

```python
import numpy as np
import pandas as pd
from scipy import stats


def detect_data_drift(reference_df, current_df,
 method="ks", threshold=0.05):
 """
 data — referencedata vs data。

 Parameters:
 reference_df: pd.DataFrame — data (reference)
 current_df: pd.DataFrame — inferencedata 
 method: str — "ks" (KS testing) / "psi" (PSI) / "wasserstein"
 threshold: float — significance level or PSI threshold
 """
 numeric_cols = reference_df.select_dtypes(include=[np.number]).columns
 common_cols = [c for c in numeric_cols if c in current_df.columns]

 drift_results = []

 for col in common_cols:
 ref_vals = reference_df[col].dropna.values
 cur_vals = current_df[col].dropna.values

 if method == "ks":
 stat, p_value = stats.ks_2samp(ref_vals, cur_vals)
 is_drift = p_value < threshold
 drift_results.append({
 "feature": col, "statistic": stat,
 "p_value": p_value, "is_drift": is_drift})

 elif method == "psi":
 # Population Stability Index
 psi_val = _compute_psi(ref_vals, cur_vals)
 is_drift = psi_val > 0.2 # >0.2 = significant shift
 drift_results.append({
 "feature": col, "psi": psi_val,
 "is_drift": is_drift,
 "severity": "high" if psi_val > 0.25 else
 "medium" if psi_val > 0.1 else "low"})

 elif method == "wasserstein":
 w_dist = stats.wasserstein_distance(ref_vals, cur_vals)
 ref_std = np.std(ref_vals)
 normalized = w_dist / ref_std if ref_std > 0 else w_dist
 is_drift = normalized > 0.1
 drift_results.append({
 "feature": col, "wasserstein": w_dist,
 "normalized": normalized, "is_drift": is_drift})

 result_df = pd.DataFrame(drift_results)
 n_drift = result_df["is_drift"].sum
 print(f"Data Drift ({method}): {n_drift}/{len(common_cols)} features drifted")
 return result_df


def _compute_psi(expected, actual, n_bins=10):
 """PSI (Population Stability Index) calculation。"""
 breakpoints = np.quantile(expected, np.linspace(0, 1, n_bins + 1))
 breakpoints[0] = -np.inf
 breakpoints[-1] = np.inf

 expected_pct = np.histogram(expected, bins=breakpoints)[0] / len(expected)
 actual_pct = np.histogram(actual, bins=breakpoints)[0] / len(actual)

 expected_pct = np.clip(expected_pct, 1e-4, None)
 actual_pct = np.clip(actual_pct, 1e-4, None)

 psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
 return psi
```

## 2. 

```python
def detect_performance_degradation(y_true_batches, y_pred_batches,
 metric="accuracy",
 window_size=10, alert_threshold=0.05):
 """
 's 。

 Parameters:
 y_true_batches: list[np.ndarray] — batchand 's value
 y_pred_batches: list[np.ndarray] — batchand 's predictionvalue
 metric: str — "accuracy" / "f1" / "rmse" / "auc"
 window_size: int — mean
 alert_threshold: float — alertthreshold
 """
 from sklearn.metrics import accuracy_score, f1_score, mean_squared_error
 from sklearn.metrics import roc_auc_score
 import matplotlib.pyplot as plt

 metric_funcs = {
 "accuracy": accuracy_score,
 "f1": lambda y, p: f1_score(y, p, average="macro"),
 "rmse": lambda y, p: -np.sqrt(mean_squared_error(y, p)),
 "auc": lambda y, p: roc_auc_score(y, p)
 }

 func = metric_funcs[metric]
 scores = [func(yt, yp) for yt, yp in zip(y_true_batches, y_pred_batches)]

 # mean
 scores_arr = np.array(scores)
 if len(scores_arr) >= window_size:
 ma = np.convolve(scores_arr, np.ones(window_size)/window_size, mode="valid")
 else:
 ma = scores_arr

 # ('s window_size batch)
 baseline = np.mean(scores_arr[:window_size])
 current = np.mean(scores_arr[-window_size:])
 degradation = baseline - current

 is_degraded = degradation > alert_threshold

 # visualization
 fig, ax = plt.subplots(figsize=(12, 5))
 ax.plot(scores, "b-o", markersize=3, alpha=0.5, label="Batch score")
 if len(ma) > 0:
 ax.plot(range(window_size - 1, window_size - 1 + len(ma)),
 ma, "r-", linewidth=2, label=f"MA({window_size})")
 ax.axhline(baseline, color="g", linestyle="--",
 label=f"Baseline={baseline:.4f}")
 ax.axhline(baseline - alert_threshold, color="orange", linestyle="--",
 label=f"Alert={baseline - alert_threshold:.4f}")
 ax.set_xlabel("Batch")
 ax.set_ylabel(metric)
 ax.set_title(f"Model Performance Monitoring ({metric})")
 ax.legend

 path = "performance_monitoring.png"
 plt.savefig(path, dpi=150, bbox_inches="tight")
 plt.close

 status = "DEGRADED ⚠️" if is_degraded else "OK ✓"
 print(f"Performance ({metric}): baseline={baseline:.4f}, "
 f"current={current:.4f}, Δ={degradation:.4f} → {status}")
 return {"baseline": baseline, "current": current,
 "degradation": degradation, "is_degraded": is_degraded,
 "scores": scores, "fig": path}
```

## 3. A/B testing

```python
def ab_test_models(y_true, preds_a, preds_b, metric="accuracy",
 n_bootstrap=10000, alpha=0.05):
 """
 A/B testing — 2 'scomparison。

 Parameters:
 y_true: np.ndarray — value
 preds_a: np.ndarray — A prediction
 preds_b: np.ndarray — B prediction
 metric: str — evaluation metric
 n_bootstrap: int — timesnumber/count
 alpha: float — significance level
 """
 from sklearn.metrics import accuracy_score, f1_score, mean_squared_error

 metric_funcs = {
 "accuracy": accuracy_score,
 "f1": lambda y, p: f1_score(y, p, average="macro"),
 "rmse": lambda y, p: np.sqrt(mean_squared_error(y, p))
 }

 func = metric_funcs[metric]
 score_a = func(y_true, preds_a)
 score_b = func(y_true, preds_b)

 # Bootstrap confidence interval for difference
 diffs = []
 n = len(y_true)
 rng = np.random.RandomState(42)

 for _ in range(n_bootstrap):
 idx = rng.choice(n, n, replace=True)
 sa = func(y_true[idx], preds_a[idx])
 sb = func(y_true[idx], preds_b[idx])
 diffs.append(sb - sa)

 diffs = np.array(diffs)
 ci_lower = np.percentile(diffs, 100 * alpha / 2)
 ci_upper = np.percentile(diffs, 100 * (1 - alpha / 2))
 p_value = np.mean(diffs <= 0) # P(B ≤ A)

 winner = "B" if ci_lower > 0 else ("A" if ci_upper < 0 else "Tie")

 print(f"A/B Test ({metric}): A={score_a:.4f}, B={score_b:.4f}")
 print(f" Δ(B-A)={score_b - score_a:.4f}, "
 f"95% CI=[{ci_lower:.4f}, {ci_upper:.4f}], "
 f"p={p_value:.4f} → Winner: {winner}")
 return {"score_a": score_a, "score_b": score_b,
 "diff": score_b - score_a, "ci": (ci_lower, ci_upper),
 "p_value": p_value, "winner": winner}
```

---

## Pipeline Integration

```
ensemble-methods → model-monitoring → anomaly-detection
 (construction)  (anomaly detection)
 │ │ ↓
 automl ──────────────┘ active-learning
 (AutoML) 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `drift_report.csv` | results | → |
| `performance_monitoring.png` | | → reporting |
| `ab_test_result.json` | A/B testingresults | → |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | |
