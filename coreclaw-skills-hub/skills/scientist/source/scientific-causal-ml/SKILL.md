---
name: scientific-causal-ml
description: |
 machine learningskill。DoWhy EconML CATE 
 Double/Debiased MLCausal Forest (S/T/X)
 (HTE)featuresselection。
tu_tools:
 - key: openml
 name: OpenML
 description: causal inference ML datasetreference
---

# Scientific Causal ML

machine learning'scausal inferencepipelineproviding、
 (HTE) 's and features.

## When to Use

- units/loop different and (HTE )
- Causal Forest is estimatedand
- Double ML data's is estimatedand
- (S/T/X-learner) CATE is estimatedand
- DoWhy 'swhen needed
- featuresselection importantfactorwhen needed

> **Note**: causal inference (PSM/IPW/DID/RDD) `scientific-causal-inference` reference。

---

## Quick Start

## 1. DoWhy 

```python
import numpy as np
import pandas as pd


def dowhy_causal_model(df, treatment, outcome, common_causes,
 effect_modifiers=None, method="backdoor.linear_regression"):
 """
 DoWhy causal inferencepipeline (→→)。

 Parameters:
 df: pd.DataFrame — data
 treatment: str — number/count
 outcome: str — outcome variable
 common_causes: list[str] — covariates
 effect_modifiers: list[str] | None — factor
 method: str — method
 """
 import dowhy

 model = dowhy.CausalModel(
 data=df,
 treatment=treatment,
 outcome=outcome,
 common_causes=common_causes,
 effect_modifiers=effect_modifiers)

 # 
 estimand = model.identify_effect(proceed_when_unidentifiable=True)
 print(f"Identified estimand: {estimand.get_frontdoor_variables}")

 # 
 estimate = model.estimate_effect(
 estimand, method_name=method)
 print(f"ATE = {estimate.value:.4f} (95% CI: [{estimate.get_confidence_intervals[0]:.4f}, "
 f"{estimate.get_confidence_intervals[1]:.4f}])")

 # testing
 refutations = {}
 for refuter_name in ["random_common_cause", "placebo_treatment_refuter",
 "data_subset_refuter"]:
 try:
 refutation = model.refute_estimate(
 estimand, estimate, method_name=refuter_name)
 refutations[refuter_name] = {
 "new_effect": float(refutation.new_effect),
 "p_value": getattr(refutation, "refutation_result", {}).get("p_value", None)
 }
 except Exception:
 pass

 print(f"Refutation tests: {len(refutations)} passed")
 return {"model": model, "estimand": estimand,
 "estimate": estimate, "refutations": refutations}
```

## 2. EconML Double ML / Causal Forest

```python
def double_ml_estimate(df, treatment, outcome, features,
 n_splits=5, model_type="linear"):
 """
 Double/Debiased ML by/via。

 Parameters:
 df: pd.DataFrame — data
 treatment: str — number/count
 outcome: str — outcome variable
 features: list[str] — covariates
 n_splits: int — minnumber/count
 model_type: str — "linear" / "forest"
 """
 from econml.dml import LinearDML, CausalForestDML

 Y = df[outcome].values
 T = df[treatment].values
 X = df[features].values

 if model_type == "linear":
 est = LinearDML(cv=n_splits, random_state=42)
 else:
 est = CausalForestDML(
 n_estimators=200, cv=n_splits, random_state=42)

 est.fit(Y, T, X=X)

 ate = est.ate(X)
 ate_ci = est.ate_interval(X, alpha=0.05)

 # CATE (units)
 cate = est.effect(X)
 cate_ci = est.effect_interval(X, alpha=0.05)

 result_df = pd.DataFrame(X, columns=features)
 result_df["cate"] = cate
 result_df["cate_lower"] = cate_ci[0]
 result_df["cate_upper"] = cate_ci[1]

 print(f"Double ML ({model_type}): ATE={ate:.4f} "
 f"[{ate_ci[0]:.4f}, {ate_ci[1]:.4f}]")
 print(f" CATE range: [{cate.min:.4f}, {cate.max:.4f}]")
 return {"ate": ate, "ate_ci": ate_ci,
 "cate_df": result_df, "model": est}


def causal_forest(df, treatment, outcome, features,
 n_estimators=500):
 """
 Causal Forest — HTE 。

 Parameters:
 df: pd.DataFrame — data
 treatment: str — number/count (binary)
 outcome: str — outcome variable
 features: list[str] — covariates
 n_estimators: int — 's number/count
 """
 from econml.dml import CausalForestDML

 Y = df[outcome].values
 T = df[treatment].values
 X = df[features].values

 cf = CausalForestDML(
 n_estimators=n_estimators, random_state=42,
 min_samples_leaf=10)
 cf.fit(Y, T, X=X)

 cate = cf.effect(X)
 cate_ci = cf.effect_interval(X, alpha=0.05)

 # featuresimportantdegree 
 importances = cf.feature_importances_
 feat_imp = pd.DataFrame({
 "feature": features,
 "causal_importance": importances
 }).sort_values("causal_importance", ascending=False)

 print(f"Causal Forest: {n_estimators} trees, "
 f"CATE median={np.median(cate):.4f}")
 print(f" Top causal features: {feat_imp.head(5).to_dict('records')}")
 return {"cate": cate, "cate_ci": cate_ci,
 "feature_importance": feat_imp, "model": cf}
```

## 3. (S/T/X-Learner)

```python
def meta_learner(df, treatment, outcome, features,
 learner_type="t", base_model=None):
 """
 by/via CATE 。

 Parameters:
 df: pd.DataFrame — data
 treatment: str — number/count (binary 0/1)
 outcome: str — outcome variable
 features: list[str] — covariates
 learner_type: str — "s" / "t" / "x"
 base_model: BaseEstimator | None — 
 """
 from econml.metalearners import SLearner, TLearner, XLearner
 from sklearn.ensemble import GradientBoostingRegressor

 if base_model is None:
 base_model = GradientBoostingRegressor(
 n_estimators=200, max_depth=5, random_state=42)

 Y = df[outcome].values
 T = df[treatment].values
 X = df[features].values

 learners = {"s": SLearner, "t": TLearner, "x": XLearner}
 LearnerClass = learners[learner_type]

 if learner_type == "s":
 est = LearnerClass(overall_model=base_model)
 else:
 est = LearnerClass(models=base_model)

 est.fit(Y, T, X=X)
 cate = est.effect(X)

 result_df = pd.DataFrame(X, columns=features)
 result_df["cate"] = cate

 print(f"{learner_type.upper}-Learner: "
 f"CATE mean={cate.mean:.4f}, std={cate.std:.4f}")
 return {"cate": cate, "cate_df": result_df, "model": est}
```

---

## Pipeline Integration

```
causal-inference → causal-ml → feature-importance
  ( ML) (features)
 │ │ ↓
 clinical-trial ───────┘ explainable-ai
 (clinical trial) (possible AI)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `dowhy_causal_model.json` | DoWhy | → reporting |
| `cate_estimates.csv` | CATE value | → precision-medicine |
| `causal_feature_importance.csv` | featuresimportantdegree | → explainable-ai |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | causal inference ML datasetreference |
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
