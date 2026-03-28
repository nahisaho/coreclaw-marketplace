---
name: scientific-semi-supervised-learning
description: |
 Semi-supervised learning skill. Self-training, co-training, label propagation, MixMatch/FixMatch, and semi-supervised model evaluation pipelines.
tu_tools:
 - key: openml
 name: OpenML
 description: semi-supervised learning
---

# Scientific Semi-Supervised Learning

amount's labeldata and amount's labeldatautilizes
semi-supervised learningpipeline is provided。

## When to Use

- labeldata amount and
- annotationallamount and
- Self-Training labelwhen needed
- graph's Label Propagation is appliedand
- Pseudo-Labeling 's degreethreshold is designedand

---

## Quick Start

## 1. Self-Training pipeline

```python
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score, classification_report


def self_training_pipeline(X_labeled, y_labeled, X_unlabeled,
 base_estimator=None, threshold=0.95,
 max_iterations=10, batch_size=None,
 X_test=None, y_test=None):
 """
 Self-Training semi-supervised learning。

 Parameters:
 X_labeled: np.ndarray — labelfeatures
 y_labeled: np.ndarray — label
 X_unlabeled: np.ndarray — labelfeatures
 base_estimator: sklearn estimator | None — classification
 threshold: float — Pseudo-Label forthreshold
 max_iterations: int — timesnumber/count
 batch_size: int | None — eachadditionnumber/count
 X_test: np.ndarray | None — testingfeatures
 y_test: np.ndarray | None — testinglabel
 """
 from sklearn.ensemble import GradientBoostingClassifier

 if base_estimator is None:
 base_estimator = GradientBoostingClassifier(
 n_estimators=100, random_state=42)

 X_train = X_labeled.copy
 y_train = y_labeled.copy
 X_pool = X_unlabeled.copy
 history = []

 for iteration in range(max_iterations):
 if len(X_pool) == 0:
 print(f"Iteration {iteration}: Pool exhausted")
 break

 model = clone(base_estimator)
 model.fit(X_train, y_train)
 proba = model.predict_proba(X_pool)
 max_proba = proba.max(axis=1)
 pseudo_labels = proba.argmax(axis=1)

 confident_mask = max_proba >= threshold
 n_confident = confident_mask.sum

 if batch_size and n_confident > batch_size:
 top_idx = np.argsort(max_proba)[-batch_size:]
 confident_mask = np.zeros(len(X_pool), dtype=bool)
 confident_mask[top_idx] = True
 n_confident = batch_size

 if n_confident == 0:
 print(f"Iteration {iteration}: No confident samples")
 break

 X_train = np.vstack([X_train, X_pool[confident_mask]])
 y_train = np.concatenate([
 y_train, pseudo_labels[confident_mask]])
 X_pool = X_pool[~confident_mask]

 record = {"iteration": iteration,
 "n_labeled": len(X_train),
 "n_pool": len(X_pool),
 "n_added": int(n_confident),
 "mean_confidence": float(max_proba[confident_mask].mean)}

 if X_test is not None and y_test is not None:
 test_acc = accuracy_score(y_test, model.predict(X_test))
 record["test_accuracy"] = test_acc

 history.append(record)
 print(f"Iter {iteration}: +{n_confident} samples, "
 f"total={len(X_train)}, pool={len(X_pool)}")

 final_model = clone(base_estimator)
 final_model.fit(X_train, y_train)
 return final_model, pd.DataFrame(history)
```

## 2. Label Propagation

```python
def label_propagation_ssl(X_all, y_partial, kernel="rbf",
 gamma=20, n_neighbors=7,
 max_iter=1000):
 """
 graph Label Propagation。

 Parameters:
 X_all: np.ndarray — allfeatures (label+label)
 y_partial: np.ndarray — label (-1 = label)
 kernel: str — "rbf" / "knn"
 gamma: float — RBF kernel's γ
 n_neighbors: int — KNN kernel's k
 max_iter: int — timesnumber/count
 """
 from sklearn.semi_supervised import (
 LabelPropagation, LabelSpreading)

 models = {
 "propagation": LabelPropagation(
 kernel=kernel, gamma=gamma,
 n_neighbors=n_neighbors, max_iter=max_iter),
 "spreading": LabelSpreading(
 kernel=kernel, gamma=gamma,
 n_neighbors=n_neighbors, max_iter=max_iter, alpha=0.2),
 }

 results = {}
 for name, model in models.items:
 model.fit(X_all, y_partial)
 y_pred = model.transduction_
 n_propagated = (y_partial == -1).sum
 results[name] = {
 "model": model,
 "predictions": y_pred,
 "n_propagated": int(n_propagated),
 "label_distributions": model.label_distributions_,
 }
 print(f"{name}: propagated {n_propagated} labels")

 return results
```

## 3. Pseudo-Labeling evaluation

```python
def evaluate_pseudo_labels(y_true_unlabeled, pseudo_labels,
 confidences, thresholds=None):
 """
 Pseudo-Label 'sevaluation。

 Parameters:
 y_true_unlabeled: np.ndarray — 'slabel (evaluationfor)
 pseudo_labels: np.ndarray — predictionlabel
 confidences: np.ndarray — eachprediction's degree
 thresholds: list[float] | None — threshold
 """
 if thresholds is None:
 thresholds = [0.5, 0.7, 0.8, 0.9, 0.95, 0.99]

 records = []
 for t in thresholds:
 mask = confidences >= t
 if mask.sum == 0:
 continue
 acc = accuracy_score(y_true_unlabeled[mask],
 pseudo_labels[mask])
 records.append({
 "threshold": t,
 "n_selected": int(mask.sum),
 "coverage": float(mask.mean),
 "pseudo_accuracy": acc,
 })
 print(f"τ={t:.2f}: {mask.sum} samples, "
 f"coverage={mask.mean:.1%}, acc={acc:.3f}")

 return pd.DataFrame(records)
```

---

## Pipeline Integration

```
[amountlabel] → semi-supervised-learning → ml-classification
 (label) (papersclassification)
 │
 active-learning ← data-profiling
 (active learning) (data)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `self_training_history.csv` | | → convergencemin |
| `pseudo_label_quality.csv` | label | → thresholdselection |
| `propagated_labels.npy` | label | → ml-classification |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | semi-supervised learning |
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
