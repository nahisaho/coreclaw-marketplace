---
name: scientific-active-learning
description: |
 Active learning skill. Uncertainty sampling, Query-by-Committee, expected model change, pool-based/stream-based, batch active learning, GP-based active learning with ARD-RBF kernel, dimension-adaptive convergence, stopping criteria, and model improvement pipeline.
tu_tools:
 - key: openml
 name: OpenML
 description: active learning datasets and metrics
---

# Scientific Active Learning

labeldegree maximize
's designevaluationpipeline is provided。

## When to Use

- amount's labeldata rate improvementwhen needed
- labelhighexperimentdatawhen handling
- uncertaintysampling's point is identifiedand
- Query-by-Committee minselectionwhen needed
- batchmultipleretrievalwhen needed
- criteria (convergence) when needed

---

## Quick Start

## 1. uncertaintysampling

```python
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def uncertainty_sampling(model, X_pool, strategy="entropy"):
 """
 uncertainty sampling。

 Parameters:
 model: fitted sklearn classifier
 X_pool: np.ndarray — unlabeled pool
 strategy: str — "entropy" / "margin" / "least_confident"
 Returns:
 indices: np.ndarray — uncertainty's
 """
 proba = model.predict_proba(X_pool)

 if strategy == "entropy":
 scores = -np.sum(proba * np.log(proba + 1e-10), axis=1)
 elif strategy == "margin":
 sorted_p = np.sort(proba, axis=1)
 scores = 1.0 - (sorted_p[:, -1] - sorted_p[:, -2])
 elif strategy == "least_confident":
 scores = 1.0 - np.max(proba, axis=1)
 else:
 raise ValueError(f"Unknown strategy: {strategy}")

 indices = np.argsort(scores)[::-1]
 print(f"Uncertainty ({strategy}): top score = {scores[indices[0]]:.4f}")
 return indices


def query_by_committee(models, X_pool, n_members=5):
 """
 Query-by-Committee sampling。

 Parameters:
 models: list — classification
 X_pool: np.ndarray — unlabeled pool
 n_members: int — number/count
 """
 predictions = np.array([m.predict(X_pool) for m in models[:n_members]])
 # Vote entropy
 n_samples = X_pool.shape[0]
 n_classes = len(np.unique(predictions))
 scores = np.zeros(n_samples)

 for i in range(n_samples):
 votes = predictions[:, i]
 _, counts = np.unique(votes, return_counts=True)
 proba = counts / len(votes)
 scores[i] = -np.sum(proba * np.log(proba + 1e-10))

 indices = np.argsort(scores)[::-1]
 print(f"QBC: top disagreement = {scores[indices[0]]:.4f}")
 return indices
```

## 2. batch

```python
def batch_active_learning(model, X_pool, batch_size=10,
 strategy="entropy", diversity_weight=0.5):
 """
 batch。

 Parameters:
 model: fitted classifier
 X_pool: np.ndarray — unlabeled pool
 batch_size: int — batch size
 strategy: str — uncertainty
 diversity_weight: float — (0-1)
 """
 from sklearn.metrics.pairwise import euclidean_distances

 # uncertainty
 indices = uncertainty_sampling(model, X_pool, strategy)

 # pool (top batch_size * 3)
 candidate_size = min(batch_size * 3, len(indices))
 candidates = indices[:candidate_size]

 # selection (k-center greedy)
 selected = [candidates[0]]
 for _ in range(batch_size - 1):
 remaining = [c for c in candidates if c not in selected]
 if not remaining:
 break

 dists = euclidean_distances(
 X_pool[remaining], X_pool[selected])
 min_dists = dists.min(axis=1)

 # uncertaintynormalization
 uncertainty_ranks = np.array([
 np.where(indices == r)[0][0] for r in remaining])
 uncertainty_scores = 1.0 - uncertainty_ranks / len(indices)

 # 
 combined = (diversity_weight * min_dists / (min_dists.max + 1e-10)
 + (1 - diversity_weight) * uncertainty_scores)

 best_idx = remaining[np.argmax(combined)]
 selected.append(best_idx)

 print(f"Batch AL: selected {len(selected)} diverse-uncertain samples")
 return np.array(selected)
```

## 3. loop

```python
def active_learning_loop(X_labeled, y_labeled, X_pool, y_pool_true,
 X_test, y_test,
 model=None, n_rounds=100, batch_size=5,
 strategy="entropy"):
 """
 experimentloop。

 Parameters:
 X_labeled: np.ndarray — initiallabeldata
 y_labeled: np.ndarray — initiallabel
 X_pool: np.ndarray — unlabeled pool
 y_pool_true: np.ndarray — pool'slabel (Oracle)
 X_test: np.ndarray — test data
 y_test: np.ndarray — testinglabel
 model: sklearn classifier (default: RF)
 n_rounds: int — number of rounds
 batch_size: int — batch size
 strategy: str — sampling
 """
 if model is None:
 model = RandomForestClassifier(n_estimators=100, random_state=42)

 X_l = X_labeled.copy
 y_l = y_labeled.copy
 X_p = X_pool.copy
 y_p = y_pool_true.copy

 history = []
 for rnd in range(n_rounds):
 m = clone(model).fit(X_l, y_l)
 acc = accuracy_score(y_test, m.predict(X_test))
 history.append({
 "round": rnd,
 "n_labeled": len(y_l),
 "accuracy": round(acc, 4),
 "pool_size": len(y_p),
 })

 if len(X_p) == 0:
 break

 # batchselection
 selected = batch_active_learning(
 m, X_p, batch_size, strategy)

 # Oracle 
 X_l = np.vstack([X_l, X_p[selected]])
 y_l = np.concatenate([y_l, y_p[selected]])

 mask = np.ones(len(X_p), dtype=bool)
 mask[selected] = False
 X_p = X_p[mask]
 y_p = y_p[mask]

 df = pd.DataFrame(history)
 improvement = df["accuracy"].iloc[-1] - df["accuracy"].iloc[0]
 print(f"AL loop: {n_rounds} rounds, "
 f"acc {df['accuracy'].iloc[0]:.3f} → {df['accuracy'].iloc[-1]:.3f} "
 f"(+{improvement:.3f})")
 return df


def compare_strategies(X_labeled, y_labeled, X_pool, y_pool_true,
 X_test, y_test, n_rounds=100, batch_size=5):
 """
 multiple'scomparison。

 Parameters: 
 """
 strategies = ["entropy", "margin", "least_confident"]
 results = {}

 for strat in strategies:
 history = active_learning_loop(
 X_labeled, y_labeled, X_pool, y_pool_true,
 X_test, y_test,
 n_rounds=n_rounds, batch_size=batch_size,
 strategy=strat)
 results[strat] = history

 # 
 np.random.seed(42)
 random_history = active_learning_loop(
 X_labeled, y_labeled,
 X_pool[np.random.permutation(len(X_pool))],
 y_pool_true[np.random.permutation(len(y_pool_true))],
 X_test, y_test,
 n_rounds=n_rounds, batch_size=batch_size,
 strategy="least_confident")
 results["random"] = random_history

 print(f"Strategy comparison: {len(strategies) + 1} methods evaluated")
 return results
```

## 4. GP-Based Active Learning with ARD-RBF Kernel

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel


def gp_active_learning(X_labeled, y_labeled, X_pool,
 n_rounds=100, batch_size=5):
 """
 Gaussian Process active learning with ARD-RBF kernel.

 ARD-RBF assigns a per-dimension length_scale, enabling
 automatic relevance determination for high-dimensional spaces
 (d >= 10). Isotropic RBF or Matern kernels fail to converge
 in such settings because they cannot distinguish informative
 from uninformative dimensions.

 Parameters:
 X_labeled: np.ndarray (n, d)
 y_labeled: np.ndarray (n,)
 X_pool: np.ndarray (m, d)
 n_rounds: int
 batch_size: int
 Returns:
 dict with gp_model, history, X_final, y_final
 """
 d = X_labeled.shape[1]
 # ARD-RBF: one length_scale per dimension
 kernel = RBF(length_scale=np.ones(d)) + WhiteKernel(noise_level=1e-3)

 X_l = X_labeled.copy
 y_l = y_labeled.copy
 X_p = X_pool.copy

 history = []
 for rnd in range(n_rounds):
 gp = GaussianProcessRegressor(
 kernel=kernel, n_restarts_optimizer=5, random_state=42)
 gp.fit(X_l, y_l)

 mu, sigma = gp.predict(X_p, return_std=True)
 mean_var = np.mean(sigma ** 2)

 # dimension-adaptive convergence threshold
 threshold = 0.3 * d
 history.append({
 "round": rnd,
 "n_labeled": len(y_l),
 "mean_variance": round(float(mean_var), 6),
 "threshold": threshold,
 "pool_remaining": len(X_p),
 })

 if mean_var < threshold:
 print(f"GP-AL converged at round {rnd}: "
 f"mean_var={mean_var:.4f} < threshold={threshold:.1f}")
 break

 if len(X_p) < batch_size:
 print(f"Pool exhausted at round {rnd}")
 break

 # Select highest-variance points
 top_idx = np.argsort(sigma)[::-1][:batch_size]
 X_l = np.vstack([X_l, X_p[top_idx]])
 y_l = np.concatenate([y_l, mu[top_idx]]) # surrogate label

 mask = np.ones(len(X_p), dtype=bool)
 mask[top_idx] = False
 X_p = X_p[mask]

 print(f"GP-AL: {len(history)} rounds, "
 f"final mean_var={history[-1]['mean_variance']:.4f}, "
 f"ARD length_scales={gp.kernel_.k1.length_scale}")
 return {
 "gp_model": gp,
 "history": pd.DataFrame(history),
 "X_final": X_l,
 "y_final": y_l,
 }
```

## 5. criteria

```python
def stopping_criterion(history_df, patience=5, min_improvement=0.001,
 n_dims=None):
 """
 criteria。

 Parameters:
 history_df: pd.DataFrame — AL 
 patience: int — improvementnumber of rounds
 min_improvement: float — improvement
 n_dims: int or None — inputnumber/count (variance-based convergence)
 """
 # variance-based convergence (for GP-AL)
 if "mean_variance" in history_df.columns and n_dims is not None:
 threshold = 0.3 * n_dims
 last_var = history_df["mean_variance"].iloc[-1]
 if last_var < threshold:
 return True, (f"variance converged: {last_var:.4f} "
 f"< threshold={threshold:.1f} (d={n_dims})")

 # accuracy-based convergence
 if "accuracy" in history_df.columns:
 accs = history_df["accuracy"].values
 if len(accs) < patience + 1:
 return False, "insufficient rounds"

 recent = accs[-patience:]
 best_before = accs[:-patience].max
 improvement = recent.max - best_before

 if improvement < min_improvement:
 return True, (f"converged: improvement {improvement:.5f} "
 f"< threshold {min_improvement}")

 return False, f"continuing: improvement {improvement:.5f}"

 return False, "no convergence metric found"
```

---

## Pipeline Integration

```
eda-correlation → active-learning → ml-classification
 (datasearch/exploration) (selection) (construction)
 │ │ ↓
 missing-data ─────────┘ ensemble-methods
 (value) (ensemble)
 ↓
 uncertainty-quantification
 (uncertaintyamount)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `al_history.csv` | AL | → |
| `gp_al_history.csv` | GP-AL (ARD-RBF) | → |
| `selected_samples.csv` | selection | → label |
| `strategy_comparison.csv` | comparison | → advanced-visualization |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | active learning datasets and metrics |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Experimental Design)

Before execution, define:
- [ ] **Factors and levels**: complete factor list with ranges
- [ ] **Response variable**: measurement method, precision
- [ ] **Design type**: factorial / fractional / RSM / sequential
- [ ] **Sample size**: power analysis with effect size justification

#### Pass Criteria
- Design matrix is orthogonal or near-orthogonal
- All factors have >= 2 levels with scientific justification
- Randomization order specified
- Blocking/stratification applied for known confounders
- Statistical model specified before data collection
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
