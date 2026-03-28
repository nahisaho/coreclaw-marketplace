---
name: scientific-time-series
description: |
 time seriesanalysispredictionskill。ARIMA/SARIMA/Prophet 、point（PELT/Bayesian）、
 analysis（FFT/）、degradation（STL）、、Granger testing's
 template providing。experimentdata's analysisprediction for。
---

# Scientific Time Series Analysis

time series data's degradationpredictionpipeline。
process、environmentmeasurement、、experimenttime series dataetc.for.

## When to Use

- time series's degradationvisualizationwhen needed
- ARIMA / Prophet by/viaprediction is builtand
- point and value datafromwhen needed
- （） analysiswhen needed
- Granger etc.time series's is investigatedand

---

## Quick Start

## 1. STL degradation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

def stl_decomposition(series, period, robust=True, figsize=(12, 10)):
 """
 STL (Seasonal and Trend decomposition using Loess) by/viadegradation。

 Components:
 - Trend: 
 - Seasonal: min
 - Residual: residual

 Parameters:
 series: pd.Series with DatetimeIndex
 period: （datanumber/count）
 """
 stl = STL(series, period=period, robust=robust)
 result = stl.fit

 fig, axes = plt.subplots(4, 1, figsize=figsize, sharex=True)
 components = [("Observed", series), ("Trend", result.trend),
 ("Seasonal", result.seasonal), ("Residual", result.resid)]

 for ax, (name, data) in zip(axes, components):
 ax.plot(data, linewidth=1)
 ax.set_ylabel(name)
 ax.grid(alpha=0.3)

 plt.suptitle("STL Decomposition", fontweight="bold", y=1.01)
 plt.tight_layout
 plt.savefig("figures/stl_decomposition.png", dpi=300, bbox_inches="tight")
 plt.close

 return result
```

## 2. ARIMA / SARIMA 

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

def adf_stationarity_test(series, significance=0.05):
 """ADF testingby/via。"""
 result = adfuller(series.dropna)
 return {
 "adf_statistic": result[0],
 "p_value": result[1],
 "used_lag": result[2],
 "n_obs": result[3],
 "is_stationary": result[1] < significance,
 "critical_values": result[4],
 }


def fit_sarima(series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
 forecast_steps=24):
 """
 SARIMA 's andprediction。

 Parameters:
 order: (p, d, q) — ARnumber/count, minnumber/count, MAnumber/count
 seasonal_order: (P, D, Q, s) — AR/min/MA number/count + 
 forecast_steps: predictionperiodnumber/count
 """
 model = SARIMAX(series, order=order, seasonal_order=seasonal_order,
 enforce_stationarity=False, enforce_invertibility=False)
 fitted = model.fit(disp=False)

 # prediction
 forecast = fitted.get_forecast(steps=forecast_steps)
 pred_mean = forecast.predicted_mean
 conf_int = forecast.conf_int

 # diagnosis
 diagnostics = {
 "aic": fitted.aic,
 "bic": fitted.bic,
 "ljung_box_p": fitted.test_serial_correlation("ljungbox")[0][0, 1],
 }

 return fitted, pred_mean, conf_int, diagnostics


def plot_forecast(series, pred_mean, conf_int, title="SARIMA Forecast",
 figsize=(12, 5)):
 """time series's value and predictiondrawing/plotting."""
 fig, ax = plt.subplots(figsize=figsize)
 ax.plot(series.index, series.values, "b-", label="Observed", linewidth=1)
 ax.plot(pred_mean.index, pred_mean.values, "r--", label="Forecast",
 linewidth=2)
 ax.fill_between(conf_int.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1],
 color="red", alpha=0.1, label="95% CI")
 ax.set_title(title, fontweight="bold")
 ax.legend
 ax.grid(alpha=0.3)
 plt.tight_layout
 plt.savefig("figures/time_series_forecast.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 3. point

```python
def detect_changepoints(series, method="pelt", penalty="bic", min_size=10):
 """
 point。

 method:
 "pelt" — PELT (ruptures)
 "cusum" — CUSUM 
 "bayesian" — Bayesianpoint

 Returns:
 list of changepoint indices
 """
 import ruptures as rpt

 signal = series.values

 if method == "pelt":
 algo = rpt.Pelt(model="rbf", min_size=min_size).fit(signal)
 cps = algo.predict(pen=10)
 elif method == "cusum":
 algo = rpt.Binseg(model="l2", min_size=min_size).fit(signal)
 cps = algo.predict(n_bkps=5)
 elif method == "bayesian":
 algo = rpt.BottomUp(model="l2", min_size=min_size).fit(signal)
 cps = algo.predict(n_bkps=5)

 # 's element (n) 
 cps = [cp for cp in cps if cp < len(signal)]

 return cps


def plot_changepoints(series, changepoints, figsize=(12, 4)):
 """pointtime seriesvisualization."""
 fig, ax = plt.subplots(figsize=figsize)
 ax.plot(series.index, series.values, "b-", linewidth=1)
 for cp in changepoints:
 ax.axvline(series.index[cp], color="red", linestyle="--",
 alpha=0.7, linewidth=1.5)
 ax.set_title(f"Changepoint Detection ({len(changepoints)} points found)",
 fontweight="bold")
 ax.grid(alpha=0.3)
 plt.tight_layout
 plt.savefig("figures/changepoints.png", dpi=300, bbox_inches="tight")
 plt.close
```

## 4. analysis（FFT / ）

```python
def fft_periodicity(series, fs=1.0, top_n=5, figsize=(10, 5)):
 """
 FFT by/viaspectrum and 'sextraction。
 """
 signal = series.values - np.mean(series.values)
 N = len(signal)
 fft_vals = np.fft.rfft(signal)
 fft_power = np.abs(fft_vals)**2
 freqs = np.fft.rfftfreq(N, d=1/fs)

 # DCmin
 fft_power[0] = 0

 # Top-N 
 top_idx = np.argsort(fft_power)[::-1][:top_n]
 dominant_periods = []
 for idx in top_idx:
 if freqs[idx] > 0:
 dominant_periods.append({
 "frequency": freqs[idx],
 "period": 1 / freqs[idx],
 "power": fft_power[idx],
 })

 fig, ax = plt.subplots(figsize=figsize)
 ax.plot(freqs[1:], fft_power[1:], "b-", linewidth=1)
 for dp in dominant_periods:
 ax.axvline(dp["frequency"], color="red", linestyle="--", alpha=0.5)
 ax.set_xlabel("Frequency")
 ax.set_ylabel("Power")
 ax.set_title("FFT Power Spectrum", fontweight="bold")
 plt.tight_layout
 plt.savefig("figures/fft_spectrum.png", dpi=300, bbox_inches="tight")
 plt.close

 return dominant_periods
```

## 5. Granger testing

```python
from statsmodels.tsa.stattools import grangercausalitytests

def granger_causality(df, cause_col, effect_col, max_lag=10,
 significance=0.05):
 """
 Granger testing: cause → effect 'stesting.

 Returns:
 dict with optimal_lag, p_values, is_causal
 """
 data = df[[effect_col, cause_col]].dropna
 results = grangercausalitytests(data, maxlag=max_lag, verbose=False)

 p_values = {}
 for lag in range(1, max_lag + 1):
 p_val = results[lag][0]["ssr_ftest"][1]
 p_values[lag] = p_val

 optimal_lag = min(p_values, key=p_values.get)

 return {
 "cause": cause_col,
 "effect": effect_col,
 "optimal_lag": optimal_lag,
 "p_value_at_optimal": p_values[optimal_lag],
 "is_causal": p_values[optimal_lag] < significance,
 "all_p_values": p_values,
 }
```

## 6. 

```python
def anomaly_detection_zscore(series, window=30, threshold=3.0):
 """
 mean's Z-score 。
 """
 rolling_mean = series.rolling(window=window, center=True).mean
 rolling_std = series.rolling(window=window, center=True).std
 z_scores = (series - rolling_mean) / (rolling_std + 1e-10)
 anomalies = series[np.abs(z_scores) > threshold]
 return anomalies, z_scores
```

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

## References

### Output Files

| File | Format |
|---|---|
| `results/stationarity_test.csv` | CSV |
| `results/forecast_results.csv` | CSV |
| `results/changepoints.csv` | CSV |
| `results/dominant_periods.csv` | CSV |
| `results/granger_causality.csv` | CSV |
| `figures/stl_decomposition.png` | PNG |
| `figures/time_series_forecast.png` | PNG |
| `figures/changepoints.png` | PNG |
| `figures/fft_spectrum.png` | PNG |

#### Dependencies

```
statsmodels>=0.14
ruptures>=1.1
```
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
