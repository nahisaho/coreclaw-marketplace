---
name: scientific-active-learning
description: |
 (active learning) skill。uncertaintysampling
 Query-by-Committeepooltype/type
 batchcriteria
 improvementpipeline。
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
 model=None, n_rounds=20, batch_size=10,
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
 X_test, y_test, n_rounds=20, batch_size=10):
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

## 4. criteria

```python
def stopping_criterion(history_df, patience=5, min_improvement=0.001):
 """
 criteria。

 Parameters:
 history_df: pd.DataFrame — AL 
 patience: int — improvementnumber of rounds
 min_improvement: float — improvement
 """
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
| `selected_samples.csv` | selection | → label |
| `strategy_comparison.csv` | comparison | → advanced-visualization |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | active learning datasets and metrics |
