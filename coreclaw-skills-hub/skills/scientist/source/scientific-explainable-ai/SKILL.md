---
name: scientific-explainable-ai
description: |
 possible AI (XAI) skill。SHAPLIMECaptumInterpretML utilizing、
 prediction's basisfeaturesdegradationauditsupport。
 「's prediction」「SHAP value calculation」「LIME 」 。
---

# Scientific Explainable AI

possible AI (Explainable AI / XAI) foranalysisskill。
's predictionbasis visualizationamount、
's extraction andverification is supported。

## When to Use

- ML/DL prediction's basis
- SHAP valueby/viafeatures'squantitativedegradation
- LIME by/viageneration
- （Counterfactual Explanation）
- audit
- support's（FDA/EMA AI ）

## Quick Start

### XAI pipeline

```
Phase 1: Model Training
 - 's
 - testingpredictionresults
 ↓
Phase 2: Global Explanation
 - SHAP summary plot (allfeaturesimportantdegree)
 - Permutation importance
 - Partial Dependence Plot (PDP)
 ↓
Phase 3: Local Explanation
 - SHAP force/waterfall plot (unitsprediction's)
 - LIME (lineshape)
 - Anchor (mincondition)
 ↓
Phase 4: Interaction Analysis
 - SHAP interaction values
 - features's dependency
 - lineshape'svisualization
 ↓
Phase 5: Counterfactual Analysis
 - What-if 
 - 
 - Action recommendation
 ↓
Phase 6: Fairness & Audit
 - loop's
 - 
 - verification
```

## Workflow

### 1. SHAP (SHapley Additive exPlanations)

```python
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# === ===
# example: classification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# === TreeSHAP (forhigh-speed) ===
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Global: Summary Plot
fig, ax = plt.subplots(figsize=(10, 8))
shap.summary_plot(shap_values, X_test, feature_names=feature_names,
 show=False)
plt.tight_layout
plt.savefig("figures/shap_summary.png", dpi=300, bbox_inches="tight")
plt.show

# Global: Bar Plot (mean |SHAP|)
shap.summary_plot(shap_values, X_test, feature_names=feature_names,
 plot_type="bar", show=False)
plt.savefig("figures/shap_importance.png", dpi=300, bbox_inches="tight")
plt.show

# Local: Waterfall Plot (units)
shap.waterfall_plot(shap.Explanation(
 values=shap_values[0],
 base_values=explainer.expected_value,
 data=X_test.iloc[0],
 feature_names=feature_names,
))
plt.savefig("figures/shap_waterfall.png", dpi=300, bbox_inches="tight")
plt.show
```

### 2. SHAP Interaction Values

```python
# === SHAP Interaction Effects ===
shap_interaction = explainer.shap_interaction_values(X_test)

# Interaction heatmap
interaction_matrix = np.abs(shap_interaction).mean(axis=0)
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(interaction_matrix, cmap="YlOrRd")
ax.set_xticks(range(len(feature_names)))
ax.set_yticks(range(len(feature_names)))
ax.set_xticklabels(feature_names, rotation=45, ha="right")
ax.set_yticklabels(feature_names)
plt.colorbar(im, label="Mean |SHAP Interaction|")
ax.set_title("Feature Interaction Heatmap")
plt.tight_layout
plt.savefig("figures/shap_interaction.png", dpi=300, bbox_inches="tight")
plt.show

# Dependence plot with interaction
shap.dependence_plot(
 "feature_A", shap_values, X_test,
 interaction_index="feature_B",
 feature_names=feature_names,
)
```

### 3. LIME (Local Interpretable Model-agnostic Explanations)

```python
from lime.lime_tabular import LimeTabularExplainer

# === LIME Explainer ===
lime_explainer = LimeTabularExplainer(
 training_data=X_train.values,
 feature_names=feature_names,
 class_names=["Negative", "Positive"],
 mode="classification",
 discretize_continuous=True,
)

# unitsprediction's
def explain_instance_lime(idx, num_features=10):
 """LIME 1 's prediction"""
 exp = lime_explainer.explain_instance(
 X_test.iloc[idx].values,
 model.predict_proba,
 num_features=num_features,
 num_samples=5000,
 )

 # table
 explanation_df = pd.DataFrame(
 exp.as_list,
 columns=["Feature Rule", "Weight"]
 )
 explanation_df["Abs_Weight"] = explanation_df["Weight"].abs
 explanation_df = explanation_df.sort_values("Abs_Weight", ascending=False)

 # R² (degree)
 local_fidelity = exp.score

 return {
 "prediction": model.predict_proba(X_test.iloc[idx:idx+1])[0],
 "local_fidelity_r2": round(local_fidelity, 4),
 "explanation": explanation_df,
 }

result = explain_instance_lime(0)
print(f"Local fidelity (R²): {result['local_fidelity_r2']}")
print(result["explanation"])
```

### 4. DeepSHAP / GradientSHAP (Deep Learning)

```python
import torch

# === DeepSHAP for Neural Networks ===
def deepshap_explain(model, background_data, test_data, feature_names):
 """Deep SHAP: DeepLIFT + SHAP"""
 background = torch.tensor(background_data[:100].values, dtype=torch.float32)
 test_tensor = torch.tensor(test_data.values, dtype=torch.float32)

 explainer = shap.DeepExplainer(model, background)
 shap_values = explainer.shap_values(test_tensor)

 return shap_values


# === GradientSHAP ===
def gradient_shap_explain(model, background_data, test_data):
 """Gradient SHAP: Integrated Gradients + SHAP"""
 explainer = shap.GradientExplainer(model, background_data)
 shap_values = explainer.shap_values(test_data, nsamples=200)
 return shap_values


# === Captum (PyTorch formula XAI) ===
from captum.attr import IntegratedGradients, LayerConductance, NeuronConductance

def captum_integrated_gradients(model, inputs, target_class=None):
 """Integrated Gradients for PyTorch model"""
 ig = IntegratedGradients(model)
 attributions = ig.attribute(inputs, target=target_class, n_steps=200)
 return attributions
```

### 5. (Counterfactual Explanation)

```python
def counterfactual_explanation(model, instance, desired_class,
 feature_names, feature_ranges,
 n_cf=5, max_iter=1000):
 """
 : 「 prediction」
 's featureschange predictionsearch/exploration
 """
 from scipy.optimize import differential_evolution

 original_pred = model.predict(instance.reshape(1, -1))[0]

 def objective(x):
 # prediction desired_class and
 pred_proba = model.predict_proba(x.reshape(1, -1))[0]
 class_loss = -pred_proba[desired_class] # target's ratemaximize

 # changeamount (L1 )
 change_loss = np.sum(np.abs(x - instance) / (np.array(feature_ranges) + 1e-8))

 # 
 sparsity_loss = np.sum(np.abs(x - instance) > 1e-3) * 0.1

 return class_loss + 0.5 * change_loss + sparsity_loss

 bounds = [(r[0], r[1]) for r in feature_ranges]
 result = differential_evolution(objective, bounds, maxiter=max_iter, seed=42)

 cf_instance = result.x
 cf_pred = model.predict(cf_instance.reshape(1, -1))[0]

 # changefeatures
 changes = []
 for i, (orig, cf) in enumerate(zip(instance, cf_instance)):
 if abs(orig - cf) > 1e-3:
 changes.append({
 "feature": feature_names[i],
 "original": round(orig, 4),
 "counterfactual": round(cf, 4),
 "change": round(cf - orig, 4),
 })

 return {
 "original_prediction": int(original_pred),
 "counterfactual_prediction": int(cf_pred),
 "changes": changes,
 "n_features_changed": len(changes),
 }
```

### 6. audit

```python
def fairness_audit(model, X_test, y_test, sensitive_feature,
 feature_names):
 """
 audit: loop's prediction
 """
 from sklearn.metrics import accuracy_score, recall_score, precision_score

 predictions = model.predict(X_test)
 proba = model.predict_proba(X_test)[:, 1]

 groups = X_test[sensitive_feature].unique
 metrics = {}

 for group in groups:
 mask = X_test[sensitive_feature] == group
 metrics[group] = {
 "n": int(mask.sum),
 "accuracy": round(accuracy_score(y_test[mask], predictions[mask]), 4),
 "recall": round(recall_score(y_test[mask], predictions[mask]), 4),
 "precision": round(precision_score(y_test[mask], predictions[mask], zero_division=0), 4),
 "positive_rate": round(predictions[mask].mean, 4),
 "avg_score": round(proba[mask].mean, 4),
 }

 # Demographic Parity Difference
 rates = [m["positive_rate"] for m in metrics.values]
 dp_diff = max(rates) - min(rates)

 # Equalized Odds Difference
 recalls = [m["recall"] for m in metrics.values]
 eo_diff = max(recalls) - min(recalls)

 audit_result = {
 "group_metrics": metrics,
 "demographic_parity_diff": round(dp_diff, 4),
 "equalized_odds_diff": round(eo_diff, 4),
 "fair_threshold": 0.1, # < 0.1 is considered fair
 "is_fair_dp": dp_diff < 0.1,
 "is_fair_eo": eo_diff < 0.1,
 }

 return audit_result
```

---

## Best Practices

1. ** + 's for**: SHAP summary (all) + waterfall (units) 
2. **SHAP > LIME**: SHAP  
3. **backgrounddata'sselection**: KernelSHAP backgrounddatanumber/count results (100-1000 recommended)
4. **LIME 's degreeverification**: `exp.score` (R²) 0.8 above/moreandverification
5. **'s possible**: changeimpossible（）
6. **dependency vs **: TreeSHAP for、DeepSHAP NN for
7. ****: AI FDA/EMA 's explainabilityitemssupport

## Completeness Checklist

- [ ] SHAP summary plot (importantdegree)
- [ ] SHAP waterfall/force plot 
- [ ] SHAP interaction values (featuresinteraction)
- [ ] LIME (degree R² verification)
- [ ] PDP (partialdependencyplot)
- [ ] （necessary）
- [ ] audit（）
- [ ] reportgeneration

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

| File | Format | Generation Timing |
|---|---|---|
| `results/xai_report.json` | XAI resultssummary（JSON） | mincompletion |
| `figures/shap_summary.png` | SHAP summary plot | |
| `figures/shap_waterfall.png` | SHAP waterfall plot | |
| `figures/shap_interaction.png` | interactionheatmap | Interaction min |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-feature-importance` | ← Permutation/Tree importance and 'scomparison |
| `scientific-ml-classification` | ← classification's |
| `scientific-ml-regression` | ← regression's |
| `scientific-deep-learning` | ← DNN 's DeepSHAP/Captum |
| `scientific-graph-neural-networks` | ← GNN 's GNNExplainer |
| `scientific-clinical-decision-support` | → AI 's |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
