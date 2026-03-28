---
name: scientific-causal-ml
description: |
 Causal machine learning skill. Heterogeneous treatment effects, CATE estimation, causal forests, meta-learners (S/T/X), uplift modeling, and policy optimization.
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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
