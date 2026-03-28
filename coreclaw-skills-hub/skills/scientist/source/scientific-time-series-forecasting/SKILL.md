---
name: scientific-time-series-forecasting
description: |
 ML time seriespredictionskill。Prophet/NeuralProphetN-BEATS
 Temporal Fusion Transformer (TFT)time seriesfeatures
 testingpredictionensembleprediction。
---

# Scientific Time Series Forecasting

deep learningML 'stime seriespredictionpipelineproviding、
Prophet from Transformer to/untillatestmethod.

## When to Use

- Prophet/NeuralProphet time series predictionwhen needed
- deep learning (N-BEATS/TFT) high-accuracypredictionwhen needed
- time seriesfeatures is generatedand
- testing predictionevaluationwhen needed
- multiple's ensemblepredictionwhen needed
- amountpredictionwhen needed

> **Note**: time series (ARIMA/STL/FFT) `scientific-time-series` reference。

---

## Quick Start

## 1. Prophet / NeuralProphet

```python
import numpy as np
import pandas as pd


def prophet_forecast(df, date_col, value_col, periods=30,
 freq="D", yearly=True, weekly=True,
 changepoint_prior=0.05):
 """
 Prophet time seriesprediction。

 Parameters:
 df: pd.DataFrame — time series data
 date_col: str — date column
 value_col: str — value column
 periods: int — predictionperiod
 freq: str — frequency ("D" / "H" / "M")
 yearly: bool — 
 weekly: bool — 
 changepoint_prior: float — pointdegree
 """
 from prophet import Prophet

 prophet_df = df[[date_col, value_col]].rename(
 columns={date_col: "ds", value_col: "y"})

 model = Prophet(
 yearly_seasonality=yearly,
 weekly_seasonality=weekly,
 changepoint_prior_scale=changepoint_prior)
 model.fit(prophet_df)

 future = model.make_future_dataframe(periods=periods, freq=freq)
 forecast = model.predict(future)

 # evaluation
 merged = forecast.merge(prophet_df, on="ds", how="left")
 valid = merged.dropna(subset=["y"])
 mae = np.mean(np.abs(valid["y"] - valid["yhat"]))
 mape = np.mean(np.abs((valid["y"] - valid["yhat"]) / valid["y"])) * 100

 fig1 = model.plot(forecast)
 fig1.savefig("prophet_forecast.png", dpi=150, bbox_inches="tight")

 fig2 = model.plot_components(forecast)
 fig2.savefig("prophet_components.png", dpi=150, bbox_inches="tight")

 print(f"Prophet: {periods} periods, MAE={mae:.4f}, MAPE={mape:.1f}%")
 return {"forecast": forecast, "model": model,
 "mae": mae, "mape": mape}


def neuralprophet_forecast(df, date_col, value_col, periods=30,
 n_lags=60, n_forecasts=30):
 """
 NeuralProphet time seriesprediction (AR-Net)。

 Parameters:
 df: pd.DataFrame — time series data
 date_col: str — date column
 value_col: str — value column
 periods: int — predictionperiod
 n_lags: int — regressionnumber/count
 n_forecasts: int — predictionstep
 """
 from neuralprophet import NeuralProphet

 np_df = df[[date_col, value_col]].rename(
 columns={date_col: "ds", value_col: "y"})

 model = NeuralProphet(
 n_lags=n_lags, n_forecasts=n_forecasts,
 yearly_seasonality=True, weekly_seasonality=True,
 learning_rate=0.01, epochs=100)

 metrics = model.fit(np_df, freq="D")

 future = model.make_future_dataframe(np_df, periods=periods, n_historic_predictions=True)
 forecast = model.predict(future)

 fig = model.plot(forecast)
 fig.savefig("neuralprophet_forecast.png", dpi=150, bbox_inches="tight")

 print(f"NeuralProphet: lags={n_lags}, forecasts={n_forecasts}")
 return {"forecast": forecast, "model": model, "metrics": metrics}
```

## 2. time seriesfeatures

```python
def create_ts_features(df, date_col, value_col,
 lags=None, rolling_windows=None):
 """
 time seriesfeatures。

 Parameters:
 df: pd.DataFrame — time series data
 date_col: str — date column
 value_col: str — value column
 lags: list[int] | None — features (e.g., [1,7,14,28])
 rolling_windows: list[int] | None — (e.g., [7,14,30])
 """
 if lags is None:
 lags = [1, 3, 7, 14, 28]
 if rolling_windows is None:
 rolling_windows = [7, 14, 30]

 result = df.copy
 result[date_col] = pd.to_datetime(result[date_col])
 result = result.sort_values(date_col)

 # features
 result["dayofweek"] = result[date_col].dt.dayofweek
 result["dayofyear"] = result[date_col].dt.dayofyear
 result["month"] = result[date_col].dt.month
 result["quarter"] = result[date_col].dt.quarter
 result["is_weekend"] = (result[date_col].dt.dayofweek >= 5).astype(int)

 # encoding
 result["sin_day"] = np.sin(2 * np.pi * result["dayofyear"] / 365.25)
 result["cos_day"] = np.cos(2 * np.pi * result["dayofyear"] / 365.25)
 result["sin_week"] = np.sin(2 * np.pi * result["dayofweek"] / 7)
 result["cos_week"] = np.cos(2 * np.pi * result["dayofweek"] / 7)

 # features
 for lag in lags:
 result[f"lag_{lag}"] = result[value_col].shift(lag)

 # amount
 for window in rolling_windows:
 result[f"rolling_mean_{window}"] = result[value_col].rolling(window).mean
 result[f"rolling_std_{window}"] = result[value_col].rolling(window).std
 result[f"rolling_min_{window}"] = result[value_col].rolling(window).min
 result[f"rolling_max_{window}"] = result[value_col].rolling(window).max

 # minfeatures
 result["diff_1"] = result[value_col].diff(1)
 result["diff_7"] = result[value_col].diff(7)

 n_features = len(result.columns) - len(df.columns)
 print(f"TS Features: {n_features} features created "
 f"(lags={lags}, windows={rolling_windows})")
 return result


def ts_backtest(df, date_col, value_col, model_fn,
 n_splits=5, horizon=30, gap=0):
 """
 time seriestesting (Walk-forward validation)。

 Parameters:
 df: pd.DataFrame — time series data
 date_col: str — date column
 value_col: str — value column
 model_fn: callable — predictionnumber/count (train_df → forecast_df)
 n_splits: int — minnumber/count
 horizon: int — prediction
 gap: int — -testing
 """
 from sklearn.metrics import mean_absolute_error, mean_squared_error

 sorted_df = df.sort_values(date_col).reset_index(drop=True)
 n = len(sorted_df)
 fold_size = (n - horizon) // n_splits

 results = []

 for i in range(n_splits):
 train_end = fold_size * (i + 1)
 test_start = train_end + gap
 test_end = min(test_start + horizon, n)

 if test_end > n:
 break

 train_df = sorted_df.iloc[:train_end]
 test_df = sorted_df.iloc[test_start:test_end]

 forecast = model_fn(train_df)
 y_true = test_df[value_col].values[:len(forecast)]
 y_pred = forecast[:len(y_true)]

 mae = mean_absolute_error(y_true, y_pred)
 rmse = np.sqrt(mean_squared_error(y_true, y_pred))
 mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100

 results.append({
 "fold": i, "train_size": train_end,
 "test_size": test_end - test_start,
 "mae": mae, "rmse": rmse, "mape": mape})

 results_df = pd.DataFrame(results)
 print(f"Backtest ({n_splits} folds, h={horizon}): "
 f"MAE={results_df['mae'].mean:.4f} ± {results_df['mae'].std:.4f}")
 return results_df
```

---

## Pipeline Integration

```
time-series → time-series-forecasting → model-monitoring
 (analysis) (ML prediction) 
 │ │ ↓
 spectral-signal ────┘ anomaly-detection
 (frequencyanalysis) (anomaly detection)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `prophet_forecast.png` | Prophet predictionresults | → presentation |
| `ts_features.csv` | time seriesfeatures | → ml-regression |
| `backtest_results.csv` | testingresults | → model selection |

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
