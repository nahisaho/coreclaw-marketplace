---
name: scientific-clinical-pharmacology
description: |
 skill。PopPK (NLME )
 PBPK simulationTDM amountoptimization
 Emax/Sigmoid PD druginteractionprediction
 pipeline。
 TU skill (Python + nlmixr2/mrgsolve )。
tu_tools:
 - key: drugbank
 name: DrugBank
 description: druginteractiondatasearch
---

# Scientific Clinical Pharmacology

populationdrug (PopPK)drug (PBPK)
 (PD) integration
analysis pipeline.

## When to Use

- population PK (PopPK) 's NLME analysis is performedand
- PBPK drugsimulationwhen needed
- TDM (Therapeutic Drug Monitoring) amountoptimizationwhen needed
- Emax/Sigmoid PD and
- druginteraction (DDI) 'spredictionwhen needed
- 's foramountwhen needed

---

## Quick Start

## 1. PK 

```python
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize


def one_compartment_iv(y, t, cl, v):
 """1- IV ODE。"""
 return [-cl / v * y[0]]


def two_compartment_iv(y, t, cl, v1, q, v2):
 """2- IV ODE。"""
 c1 = y[0] / v1
 c2 = y[1] / v2
 dy1 = -cl * c1 - q * (c1 - c2)
 dy2 = q * (c1 - c2)
 return [dy1, dy2]


def simulate_pk(dose, model="1cmt",
 params=None,
 times=None):
 """
 PK simulation。

 Parameters:
 dose: float — amount (mg)
 model: str — "1cmt" or "2cmt"
 params: dict — PK parameters
 1cmt: {cl, v}
 2cmt: {cl, v1, q, v2}
 times: array — timepoint (h)
 """
 if times is None:
 times = np.linspace(0, 24, 241)
 if params is None:
 params = ({"cl": 5.0, "v": 50.0}
 if model == "1cmt"
 else {"cl": 5.0, "v1": 50.0,
 "q": 2.0, "v2": 30.0})

 if model == "1cmt":
 y0 = [dose]
 sol = odeint(one_compartment_iv, y0,
 times,
 args=(params["cl"],
 params["v"]))
 conc = sol[:, 0] / params["v"]
 else:
 y0 = [dose, 0.0]
 sol = odeint(two_compartment_iv, y0,
 times,
 args=(params["cl"],
 params["v1"],
 params["q"],
 params["v2"]))
 conc = sol[:, 0] / params["v1"]

 df = pd.DataFrame({
 "time": times, "concentration": conc})
 cmax = conc.max
 t_half = 0.693 * params.get(
 "v", params.get("v1", 50)) / params["cl"]
 print(f"PK sim ({model}): Cmax={cmax:.2f}, "
 f"t1/2={t_half:.1f}h")
 return df
```

## 2. population PK (PopPK) 

```python
def popk_estimation(data, model="1cmt"):
 """
 population PK parameters ( NLME)。

 Parameters:
 data: pd.DataFrame — unitsdegreedata
 columns: [id, time, dv, dose, (covariates)]
 model: str — "1cmt" or "2cmt"
 """
 subjects = data["id"].unique

 def _objective(theta):
 """objective function (OFV)。"""
 tv_cl = np.exp(theta[0])
 tv_v = np.exp(theta[1])
 omega_cl = np.exp(theta[2])
 omega_v = np.exp(theta[3])
 sigma = np.exp(theta[4])

 ofv = 0.0
 for subj in subjects:
 sdata = data[data["id"] == subj]
 dose = sdata["dose"].iloc[0]
 times = sdata["time"].values
 obs = sdata["dv"].values

 # unitsparameters (EBE )
 eta_cl = 0.0
 eta_v = 0.0
 cl_i = tv_cl * np.exp(eta_cl)
 v_i = tv_v * np.exp(eta_v)

 pred = dose / v_i * np.exp(
 -cl_i / v_i * times)
 pred = np.maximum(pred, 1e-10)

 # OFV element
 residual = np.log(obs + 1e-10) - np.log(
 pred)
 ofv += np.sum(
 residual**2 / sigma**2
 + np.log(sigma**2))

 return ofv

 # initialvalue
 x0 = [np.log(5), np.log(50),
 np.log(0.3), np.log(0.3),
 np.log(0.2)]

 result = minimize(_objective, x0,
 method="Nelder-Mead",
 options={"maxiter": 5000})

 estimates = {
 "tv_cl": round(np.exp(result.x[0]), 3),
 "tv_v": round(np.exp(result.x[1]), 3),
 "omega_cl": round(np.exp(result.x[2]), 3),
 "omega_v": round(np.exp(result.x[3]), 3),
 "sigma": round(np.exp(result.x[4]), 3),
 "ofv": round(result.fun, 2),
 "converged": result.success,
 }

 print(f"PopPK: CL={estimates['tv_cl']} L/h, "
 f"V={estimates['tv_v']} L, "
 f"OFV={estimates['ofv']}")
 return estimates
```

## 3. TDM amountoptimization

```python
def tdm_dose_optimization(
 current_conc, current_dose,
 target_range, pk_params,
 interval=12):
 """
 TDM amountoptimization。

 Parameters:
 current_conc: float — degree
 current_dose: float — amount (mg)
 target_range: tuple — targetdegreerange (min, max)
 pk_params: dict — {cl, v} PK parameters
 interval: float — interval (h)
 """
 cl = pk_params["cl"]
 v = pk_params["v"]
 ke = cl / v
 target_mid = (target_range[0]
 + target_range[1]) / 2

 # lineshape PK : foramountexample
 ratio = target_mid / max(current_conc, 0.01)
 new_dose = current_dose * ratio

 # simulationverification
 times = np.linspace(0, interval, 100)
 conc_profile = (new_dose / v
 * np.exp(-ke * times))
 cmax = conc_profile[0]
 ctrough = conc_profile[-1]

 in_range = (target_range[0] <= ctrough
 <= target_range[1])

 result = {
 "current_dose": current_dose,
 "current_trough": current_conc,
 "recommended_dose": round(new_dose, 1),
 "predicted_cmax": round(cmax, 2),
 "predicted_trough": round(ctrough, 2),
 "target_range": target_range,
 "in_target": in_range,
 }

 status = "✓" if in_range else "✗"
 print(f"TDM: {current_dose}mg → "
 f"{new_dose:.1f}mg "
 f"(trough {ctrough:.2f}) {status}")
 return result
```

## 4. Emax PD 

```python
def emax_model(conc, emax, ec50, hill=1):
 """Emax / Sigmoid Emax 。"""
 return emax * conc**hill / (
 ec50**hill + conc**hill)


def fit_emax(conc_data, effect_data,
 sigmoid=False):
 """
 Emax 。

 Parameters:
 conc_data: array — degreedata
 effect_data: array — data
 sigmoid: bool — Sigmoid (Hill) 
 """
 from scipy.optimize import curve_fit

 conc = np.array(conc_data)
 effect = np.array(effect_data)

 if sigmoid:
 def _model(c, emax, ec50, hill):
 return emax_model(c, emax, ec50, hill)
 p0 = [max(effect), np.median(conc), 1.0]
 bounds = ([0, 0, 0.1], [np.inf, np.inf, 10])
 else:
 def _model(c, emax, ec50):
 return emax_model(c, emax, ec50, 1)
 p0 = [max(effect), np.median(conc)]
 bounds = ([0, 0], [np.inf, np.inf])

 popt, pcov = curve_fit(
 _model, conc, effect, p0=p0,
 bounds=bounds, maxfev=5000)

 perr = np.sqrt(np.diag(pcov))

 result = {
 "emax": round(popt[0], 3),
 "ec50": round(popt[1], 3),
 "emax_se": round(perr[0], 3),
 "ec50_se": round(perr[1], 3),
 }
 if sigmoid:
 result["hill"] = round(popt[2], 3)
 result["hill_se"] = round(perr[2], 3)

 print(f"PD fit: Emax={result['emax']}, "
 f"EC50={result['ec50']}"
 + (f", Hill={result['hill']}"
 if sigmoid else ""))
 return result
```

## 5. integrationpipeline

```python
def clinical_pharmacology_pipeline(
 pk_data, pd_data=None,
 target_range=(10, 20),
 output_dir="results"):
 """
 integrationpipeline。

 Parameters:
 pk_data: pd.DataFrame — PK degreedata
 pd_data: pd.DataFrame | None — PD data
 target_range: tuple — targetrange
 output_dir: str — output directory
 """
 from pathlib import Path
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 # 1) PopPK 
 pk_est = popk_estimation(pk_data)

 # 2) TDM optimization (latest)
 latest = pk_data.sort_values("time").iloc[-1]
 tdm = tdm_dose_optimization(
 latest["dv"], latest["dose"],
 target_range,
 {"cl": pk_est["tv_cl"],
 "v": pk_est["tv_v"]})

 # 3) PD (data)
 pd_result = None
 if pd_data is not None:
 pd_result = fit_emax(
 pd_data["concentration"],
 pd_data["effect"],
 sigmoid=True)

 # 4) simulation
 sim = simulate_pk(
 tdm["recommended_dose"],
 params={"cl": pk_est["tv_cl"],
 "v": pk_est["tv_v"]})
 sim.to_csv(out / "pk_simulation.csv",
 index=False)

 print(f"Clinical PK pipeline → {out}")
 return {
 "popk": pk_est,
 "tdm": tdm,
 "pd": pd_result,
 "simulation": sim,
 }
```

---

## Pipeline Integration

```
admet-pharmacokinetics → clinical-pharmacology → pharmacogenomics
 (ADMET prediction) ( PK/PD) 
 │ │ ↓
 drug-repurposing ────────────┘ clinical-decision-support
  (clinical decision support)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `pk_simulation.csv` | PK simulation | → dose-response |
| `popk_estimates.json` | PopPK parameters | → pharmacogenomics |
| `tdm_recommendation.json` | TDM recommendedforamount | → clinical-decision |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `drugbank` | DrugBank | druginteractiondatasearch |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
